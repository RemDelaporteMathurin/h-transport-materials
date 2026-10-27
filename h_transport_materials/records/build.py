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
from .models import ID_PATTERN, SCHEMA_VERSION, Material, Record, Source
from .sources import normalize_doi
from .units import ENERGY_UNIT, NORMALIZED_UNITS, quantity, ureg

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


class BuildError(Exception):
    pass


def _load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load(data_dir=DATA_DIR):
    """Loads and validates materials, sources and records.

    Returns:
        tuple: (materials, sources, records) where records is a list of
            (Record, Path) tuples
    """
    data_dir = Path(data_dir)
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
    return materials, sources, records


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
        return col / axis.factor * ureg.Unit(axis.unit)

    x, y = physical(reported.x), physical(reported.y)
    if reported.x.quantity == "inverse_temperature":
        T = 1 / x
    elif reported.x.quantity == "temperature":
        T = x
    else:
        raise BuildError("x axis must be temperature or inverse_temperature")
    return T.to(ureg.K), y


def _author_fit(fit):
    if fit.form == "arrhenius":
        return (
            quantity(fit.pre_exp.value, fit.pre_exp.unit),
            quantity(fit.act_energy.value, fit.act_energy.unit),
        )
    slope = quantity(fit.slope.value, fit.slope.unit).to(ureg.K)
    return np.exp(fit.intercept) * ureg.Unit(fit.y_unit), -slope * htm.k_B


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


def build_record(record, folder):
    """Builds the normalised values of one record

    Args:
        record (Record): the validated record
        folder (Path): folder holding the record (for data files)

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
    out["transformation_log"] = state.log
    return out


def _initial_state(record, folder, target):
    """Parses the reported values into pint quantities"""
    state = transforms.State(target_unit=target)
    rep = record.reported
    if rep.form == "arrhenius":
        state.reported = quantity(rep.pre_exp.value, rep.pre_exp.unit)
        state.act_energy = quantity(rep.act_energy.value, rep.act_energy.unit)
        if rep.range is not None:
            state.range = tuple(quantity(v, rep.range.unit) for v in rep.range.value)
    elif rep.form == "constant":
        state.reported = quantity(rep.value.value, rep.value.unit)
        state.temperature = quantity(rep.temperature.value, rep.temperature.unit)
    else:
        state.points_T, state.points_y = _read_points(rep, folder)
        if rep.author_fit is not None:
            state.author_fit_pre_exp, state.author_fit_act_energy = _author_fit(
                rep.author_fit
            )
    return state


def _normalize(record, state, target):
    rep = record.reported
    n = {}
    if rep.form == "arrhenius":
        n["selected"] = "reported"
        n["pre_exp"] = _q(state.reported, target)
        n["act_energy"] = _q(state.act_energy, ENERGY_UNIT)
        n["range"] = _range(state.range)
    elif rep.form == "constant":
        n["selected"] = "constant"
        n["value"] = _q(state.reported, target)
        n["temperature"] = _q(state.temperature, ureg.K)
    else:
        n["points"] = {"T": _q(state.points_T, ureg.K), "y": _q(state.points_y, target)}
        if state.author_fit_pre_exp is not None:
            n["author_fit"] = {
                "pre_exp": _q(state.author_fit_pre_exp, target),
                "act_energy": _q(state.author_fit_act_energy, ENERGY_UNIT),
            }
        if state.refit is not None:
            n["selected"] = "htm_refit"
            n["pre_exp"] = _q(state.refit["pre_exp"], target)
            n["act_energy"] = _q(state.refit["act_energy"], ENERGY_UNIT)
            n["range"] = _range(state.range or state.refit["range"])
            n["refit_rvalue"] = float(state.refit["rvalue"])
        elif state.author_fit_pre_exp is not None:
            n["selected"] = "author_fit"
            n["pre_exp"] = n["author_fit"]["pre_exp"]
            n["act_energy"] = n["author_fit"]["act_energy"]
            fit_range = rep.author_fit.range
            n["range"] = (
                {"value": list(fit_range.value), "unit": fit_range.unit}
                if fit_range
                else _range((state.points_T.min(), state.points_T.max()))
            )
        else:
            raise BuildError(
                f"{record.id}: points without an author fit need refit_arrhenius"
            )
    return n


def build(data_dir=DATA_DIR, data_version="dev"):
    """Builds all records

    Returns:
        dict: the compiled database
    """
    materials, sources, records = load(data_dir)
    return {
        "schema_version": SCHEMA_VERSION,
        "data_version": data_version,
        "htm_version": htm.__version__,
        "materials": [m.model_dump(mode="json") for m in materials.values()],
        "sources": [s.model_dump(mode="json") for s in sources.values()],
        "records": [build_record(r, path.parent) for r, path in records],
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
