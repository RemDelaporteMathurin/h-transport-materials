"""Builds the compiled database from the YAML records.

Usage::

    python -m h_transport_materials.records.build --out dist/htm-data.json

Each record goes through: schema validation, unit parsing, the record's
transformations (in order), selection of the Arrhenius parameters, and
conversion to normalised SI units. Nothing in the YAML is modified.
"""

import argparse
import json
from pathlib import Path

import numpy as np
import pint
import yaml

import h_transport_materials as htm

from . import transforms
from .models import ID_PATTERN, SCHEMA_VERSION, ElementTable, Material, Record, Source
from .doi import normalize_doi
from .units import ENERGY_UNIT, NORMALIZED_UNITS, quantity, ureg

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

# largest relative difference allowed between an author fit and the fit of
# the points over the measured range before a curator has to choose
FIT_TOLERANCE = 0.10


class BuildError(Exception):
    pass


def _load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load(data_dir=DATA_DIR):
    """Loads and validates the element table, materials, sources and records.

    Returns:
        tuple: (elements, materials, sources, records) where records is a
            list of (Record, Path) tuples
    """
    data_dir = Path(data_dir)
    elements = ElementTable(**_load_yaml(data_dir / "elements.yaml"))
    materials = {}
    for path in sorted((data_dir / "materials").glob("*.yaml")):
        m = Material(**_load_yaml(path))
        materials[m.id] = m
    sources = {}
    for path in sorted((data_dir / "sources").glob("*.yaml")):
        s = Source(**_load_yaml(path))
        if path.stem != s.key:
            raise BuildError(f"{path.name}: file name must be the source key {s.key}")
        sources[s.key] = s

    dois = {normalize_doi(s.doi): k for k, s in sources.items() if s.doi}
    for m in materials.values():
        try:
            for composition in (m.composition, m.formula_units):
                if composition:
                    transforms.molar_mass(composition, elements)
        except ValueError as e:
            raise BuildError(f"material {m.id}: {e}") from e
        ref = m.density.source if m.density else None
        if ref and (normalize_doi(ref.doi) not in dois if ref.doi else ref.key not in sources):
            raise BuildError(
                f"material {m.id}: density source {ref.doi or ref.key} has no source file"
            )

    records, seen = [], set()
    for path in sorted((data_dir / "records").glob("*.yaml")):
        try:
            r = Record(**_load_yaml(path))
        except Exception as e:
            raise BuildError(f"{path.name}: {e}") from e
        if r.id in seen:
            raise BuildError(f"duplicate id {r.id}")
        seen.add(r.id)
        if path.stem != r.id.removeprefix("htm:"):
            raise BuildError(f"{path.name}: file name must match id {r.id}")
        if r.material not in materials:
            raise BuildError(f"{r.id}: unknown material {r.material!r}")
        r.source.key = _resolve_source(r, sources)
        if not r.id.split(":")[1].startswith(materials[r.material].code + "-"):
            raise BuildError(
                f"{r.id}: id must start with material code {materials[r.material].code}"
            )
        records.append((r, path))
    return elements, materials, sources, records


def _resolve_source(record, sources):
    """Returns the key of the source a record cites (by DOI or key)"""
    if record.source.doi is not None:
        doi = normalize_doi(record.source.doi)
        keys = [k for k, s in sources.items() if s.doi and normalize_doi(s.doi) == doi]
        if not keys:
            raise BuildError(
                f"{record.id}: no source file for DOI {doi}."
                f" Run: htm source add {doi}"
            )
        key = keys[0]
    else:
        key = record.source.key
        if key not in sources:
            raise BuildError(f"{record.id}: unknown source {key!r}")
    if ID_PATTERN.match(record.id)["source"] != key:
        raise BuildError(f"{record.id}: id does not match source key {key}")
    return key


def _read_points(reported, folder):
    data = np.genfromtxt(folder / reported.file, delimiter=",", ndmin=2)

    def physical(axis):
        col = data[:, axis.column]
        if axis.scale == "ln":
            col = np.exp(col)
        elif axis.scale == "log10":
            col = 10**col
        # Quantity() rather than multiplication: works with offset units (degC)
        return ureg.Quantity(col / axis.factor, ureg.Unit(axis.unit))

    x, y = physical(reported.x), physical(reported.y)
    if reported.x.quantity == "inverse_temperature":
        T = 1 / x
    elif reported.x.quantity == "temperature":
        T = x
    else:
        raise BuildError("x axis must be temperature or inverse_temperature")
    return T.to(ureg.K), y


def _arrhenius_law(law):
    """(pre_exp, act_energy) of an arrhenius or log_linear law"""
    if law.form == "arrhenius":
        return (
            quantity(law.pre_exp.value, law.pre_exp.unit),
            quantity(law.act_energy.value, law.act_energy.unit),
        )
    ln_base = 1.0 if law.base == "e" else np.log(10)
    pre_exp = np.exp(law.intercept * ln_base) * ureg.Unit(law.y_unit)
    if law.act_energy is not None:
        return pre_exp, quantity(law.act_energy.value, law.act_energy.unit)
    slope = quantity(law.slope.value, law.slope.unit).to(ureg.K)
    return pre_exp, -slope * ln_base * htm.k_B


def _q(q, unit):
    """Serialises a pint quantity in the given unit"""
    q = q.to(unit)
    mag = q.magnitude
    mag = mag.tolist() if isinstance(mag, np.ndarray) else float(mag)
    return {"value": mag, "unit": str(q.units)}


def _range(r):
    if r is None:
        return None
    return {"value": [float(r[0].to(ureg.K).magnitude), float(r[1].to(ureg.K).magnitude)], "unit": "kelvin"}


def build_record(record, folder, materials, elements):
    """Builds the normalised values of one record

    Args:
        record (Record): the validated record
        folder (Path): folder holding the record (for data files)
        materials (dict): material id -> Material
        elements (ElementTable): atomic weights

    Returns:
        dict: the record as stored plus a "normalized" block
    """
    law = record.law if record.property in ("solubility", "permeability") else None
    if law is None and record.law is not None:
        raise BuildError(f"{record.id}: law is only for solubility and permeability")
    target = NORMALIZED_UNITS[(record.property, law)]
    try:
        state = _initial_state(record, folder, target)
    except Exception as e:
        raise BuildError(f"{record.id}: {e}") from e
    state.context = {"record": record, "materials": materials, "elements": elements}

    for t in record.transformations:
        try:
            transforms.apply(state, t)
        except Exception as e:
            raise BuildError(f"{record.id}: transformation {t.op} failed: {e}") from e

    try:
        normalized = _normalize(record, state, target)
    except pint.DimensionalityError as e:
        raise BuildError(
            f"{record.id}: units are not compatible with a {record.property}"
            f" ({law or 'no law'}): {e}"
        ) from e

    out = record.model_dump(mode="json")
    out["normalized"] = normalized
    out["htm_assumptions"] = [
        {"op": t.op, "rationale": t.rationale}
        for t in record.transformations
        if t.origin == "htm"
    ]
    if normalized["selected"] == "htm_refit":
        out["htm_assumptions"].append(
            {
                "op": "htm_refit",
                "rationale": record.reported.selection_note
                or "the paper gives no fit; HTM fits the points (unweighted, ln y against 1/T)",
            }
        )
    out["transformation_log"] = state.log
    if state.derived:
        out["derived"] = {k: _q(v, v.units) for k, v in state.derived.items()}
    return out


def _initial_state(record, folder, target):
    """Parses the reported values into pint quantities"""
    state = transforms.State(target_unit=target)
    rep = record.reported
    if rep.form in ("arrhenius", "log_linear"):
        state.reported, state.act_energy = _arrhenius_law(rep)
        if rep.range is not None:
            state.range = tuple(quantity(v, rep.range.unit) for v in rep.range.value)
    elif rep.form == "constant":
        state.reported = quantity(rep.value.value, rep.value.unit)
        state.temperature = quantity(rep.temperature.value, rep.temperature.unit)
    else:
        state.points_T, state.points_y = _read_points(rep, folder)
        if rep.author_fit is not None:
            state.author_fit_pre_exp, state.author_fit_act_energy = _arrhenius_law(
                rep.author_fit
            )
    return state


def _normalize(record, state, target):
    rep = record.reported
    n = {}
    if rep.form in ("arrhenius", "log_linear"):
        n["selected"] = "reported"
        n["pre_exp"] = _q(state.reported, target)
        n["act_energy"] = _q(state.act_energy, ENERGY_UNIT)
        n["range"] = _range(state.range)
    elif rep.form == "constant":
        n["selected"] = "constant"
        n["value"] = _q(state.reported, target)
        n["temperature"] = _q(state.temperature, ureg.K)
    else:
        n.update(_select_fit(record, state, target))
    return n


def _law(fit, target):
    return {"pre_exp": _q(fit["pre_exp"], target), "act_energy": _q(fit["act_energy"], ENERGY_UNIT)}


def _select_fit(record, state, target):
    """Fits the points, compares with the author fit and selects one of them"""
    rep = record.reported
    n = {"points": {"T": _q(state.points_T, ureg.K), "y": _q(state.points_y, target)}}
    refit = transforms.fit_arrhenius(state.points_T, state.points_y, target)
    n["htm_refit"] = {**_law(refit, target), "rvalue": float(refit["rvalue"])}
    selected = rep.selected

    if state.author_fit_pre_exp is None:
        selected = "htm_refit"
    else:
        author = {"pre_exp": state.author_fit_pre_exp, "act_energy": state.author_fit_act_energy}
        n["author_fit"] = _law(author, target)
        diff, at_T = transforms.max_relative_difference(author, refit, refit["range"])
        n["fit_discrepancy"] = {"max_relative": diff, "at_T": _q(at_T, ureg.K)}
        if selected is None:
            if diff > FIT_TOLERANCE:
                raise BuildError(
                    f"{record.id}: the author fit and the data points disagree by"
                    f" {diff:.0%} at {at_T.m_as(ureg.K):.0f} K (tolerance"
                    f" {FIT_TOLERANCE:.0%}). Set reported.selected to author_fit or"
                    " htm_refit and explain why in reported.selection_note"
                )
            selected = "author_fit"

    n["selected"] = selected
    chosen = refit if selected == "htm_refit" else author
    n.update(_law(chosen, target))
    fit_range = rep.author_fit.range if selected == "author_fit" and rep.author_fit else None
    n["range"] = (
        {"value": list(fit_range.value), "unit": fit_range.unit}
        if fit_range
        else _range(state.range or refit["range"])
    )
    return n


def build(data_dir=DATA_DIR, data_version="dev"):
    """Builds all records

    Returns:
        dict: the compiled database
    """
    elements, materials, sources, records = load(data_dir)
    return {
        "schema_version": SCHEMA_VERSION,
        "data_version": data_version,
        "htm_version": htm.__version__,
        "elements": elements.model_dump(mode="json"),
        "materials": [m.model_dump(mode="json") for m in materials.values()],
        "sources": [s.model_dump(mode="json") for s in sources.values()],
        "records": [
            build_record(r, path.parent, materials, elements) for r, path in records
        ],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--data", default=DATA_DIR, type=Path)
    parser.add_argument("--out", default=Path("dist/htm-data.json"), type=Path)
    parser.add_argument("--data-version", default="dev")
    args = parser.parse_args(argv)

    db = build(args.data, args.data_version)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=1, ensure_ascii=False)
    print(f"{len(db['records'])} records written to {args.out}")


if __name__ == "__main__":
    main()
