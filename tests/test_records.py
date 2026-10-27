"""Tests for the record format prototype (h_transport_materials.records)."""

import shutil
import typing

import pytest

pytest.importorskip("pydantic")
pytest.importorskip("yaml")

import numpy as np
import yaml

import h_transport_materials as htm
from h_transport_materials.records import build, compat, models, schema, transforms

M_LI, M_PB = 0.006941, 0.2072  # kg/mol

# records whose values intentionally differ from the current database
EXPECTED_DIFFERENCES = {
    # single value at 450 degC, was a fake 722-724 K range
    "htm:LiPb-D-H-fauvet1988": "range",
    "htm:LiPb-S-H-fauvet1988": "range",
    # the authors' fit is used; the current entry refits the digitised points
    "htm:Li50Pb50-S-H-schumacher1990": "author_fit",
}


@pytest.fixture(scope="module")
def db():
    return build.build()


@pytest.fixture(scope="module")
def group(db):
    return compat.to_properties_group(db)


def _legacy_match(prop):
    matches = [
        p
        for p in htm.database
        if type(p) is type(prop) and p.source == prop.source and p.isotope == prop.isotope
    ]
    assert len(matches) == 1, f"{prop.record_id}: {len(matches)} matches"
    return matches[0]


def test_all_records_built(db):
    assert len(db["records"]) == 12


def test_equivalence_with_current_database(group):
    """Each record reproduces the current database entry, except listed differences"""
    for new in group:
        old = _legacy_match(new)
        difference = EXPECTED_DIFFERENCES.get(new.record_id)
        assert new.material == old.material
        new_range = [T.m_as("K") for T in new.range]
        old_range = [T.m_as("K") for T in old.range]

        if difference == "author_fit":
            # different parameters, same law within 3% over the measured range
            T = np.linspace(*old_range, 50) * htm.ureg.K
            ratio = (new.value(T) / old.value(T)).to("dimensionless").magnitude
            assert np.abs(ratio - 1).max() < 0.03
            assert new_range == pytest.approx(old_range, rel=1e-12)
            continue

        assert new.pre_exp.to(old.pre_exp.units).magnitude == pytest.approx(
            old.pre_exp.magnitude, rel=1e-12
        )
        assert new.act_energy.m_as("eV/particle") == pytest.approx(
            old.act_energy.m_as("eV/particle"), rel=1e-12, abs=1e-15
        )
        if difference == "range":
            assert new_range != pytest.approx(old_range)
        else:
            assert new_range == pytest.approx(old_range, rel=1e-12)


def test_lipb_density_and_molar_mass_come_from_registry(db):
    """Fauvet: Pb-17Li density at 300 K and Pb-17Li molar mass from the element table"""
    derived = next(r for r in db["records"] if r["id"] == "htm:LiPb-S-H-fauvet1988")["derived"]
    assert derived["density"]["value"] == pytest.approx(10163.197, rel=1e-12)
    assert derived["molar_mass"]["value"] == pytest.approx(0.17 * M_LI + 0.83 * M_PB, rel=1e-12)


def test_fauvet_is_a_single_temperature(group):
    fauvet = [p for p in group if "fauvet" in p.record_id]
    for prop in fauvet:
        assert [T.m_as("K") for T in prop.range] == pytest.approx([723.15, 723.15])


def test_schumacher_uses_author_fit_and_keeps_both(db):
    record = next(r for r in db["records"] if "schumacher" in r["id"])
    n = record["normalized"]
    assert n["selected"] == "author_fit"
    assert n["pre_exp"] == n["author_fit"]["pre_exp"]
    assert "htm_refit" in n
    assert n["fit_discrepancy"]["max_relative"] < build.FIT_TOLERANCE
    assert len(n["points"]["T"]["value"]) == len(n["points"]["y"]["value"]) > 0
    assert [a["op"] for a in record["htm_assumptions"]] == ["atom_fraction_to_concentration"]


def test_heinola_range_is_an_htm_assumption(db):
    record = next(r for r in db["records"] if "heinola" in r["id"])
    assert record["reported"]["range"] is None
    assert record["htm_assumptions"][0]["op"] == "assume_range"


def test_registry_matches_schema():
    assert set(transforms.REGISTRY) == set(typing.get_args(models.TransformationOp))


def test_json_schema_validates_yaml_records():
    jsonschema = pytest.importorskip("jsonschema")
    record_schema = schema.json_schemas()["record"]
    for path in (build.DATA_DIR / "records").glob("*.yaml"):
        jsonschema.validate(yaml.safe_load(path.read_text(encoding="utf-8")), record_schema)

    bad = yaml.safe_load(
        (build.DATA_DIR / "records" / "W-D-H-heinola2010.yaml").read_text(encoding="utf-8")
    )
    bad["transformations"][0]["op"] = "make_it_up"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(bad, record_schema)


# --- invalid records are rejected ---------------------------------------------


@pytest.fixture
def data_copy(tmp_path):
    shutil.copytree(build.DATA_DIR, tmp_path / "data")
    return tmp_path / "data"


def _edit(data_dir, name, fn):
    path = data_dir / "records" / f"{name}.yaml"
    content = yaml.safe_load(path.read_text(encoding="utf-8"))
    fn(content)
    path.write_text(yaml.safe_dump(content, sort_keys=False), encoding="utf-8")


def _set(path, value):
    def fn(content):
        target = content
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value

    return fn


@pytest.mark.parametrize(
    "name,edit,message",
    [
        (
            "W-D-H-heinola2010",
            _set(["transformations", 0, "op"], "make_it_up"),
            "transformations",
        ),
        (
            "W-D-H-esteban2001",
            _set(["reported", "pre_exp", "unit"], "m^2"),
            "not compatible with a diffusivity",
        ),
        (
            "W-D-H-esteban2001",
            _set(["reported", "range", "value"], [1073, 673]),
            "strictly increasing",
        ),
        (
            "W-D-H-esteban2001",
            _set(["property"], "solubility"),
            "does not match property",
        ),
        (
            "W-D-H-esteban2001",
            _set(["material"], "copper"),
            "unknown material",
        ),
        (
            "W-D-H-esteban2001",
            _set(
                ["transformations"],
                [
                    {
                        "op": "assume_range",
                        "params": {"range": [300, 1200]},
                        "origin": "htm",
                        "rationale": "test",
                    }
                ],
            ),
            "assume_range is not allowed",
        ),
        (
            "W-S-H-esteban2001",
            _set(["law"], None),
            "need a law",
        ),
        (
            "LiPb-S-H-fauvet1988",
            _set(["transformations", 0, "params"], {}),
            "depends on temperature: set density_at",
        ),
        (
            "Li50Pb50-S-H-schumacher1990",
            _set(["transformations", 1, "params"], {"density_at": "300 K"}),
            "li50pb50 has no density",
        ),
        (
            "LiPb-S-H-fauvet1988",
            _set(["sample", "composition"], {"Li": 17, "Pb": 80}),
            "must sum to 100",
        ),
    ],
)
def test_invalid_record_rejected(data_copy, name, edit, message):
    _edit(data_copy, name, edit)
    with pytest.raises(build.BuildError, match=message):
        build.build(data_copy)


def test_unknown_unit_rejected(data_copy):
    _edit(data_copy, "W-D-H-esteban2001", _set(["reported", "pre_exp", "unit"], "furlongs^2/fortnite"))
    with pytest.raises(build.BuildError, match="cannot parse unit"):
        build.build(data_copy)


def test_record_copied_under_other_name_rejected(data_copy):
    records = data_copy / "records"
    shutil.copy(records / "W-D-H-esteban2001.yaml", records / "W-D-H-esteban2001-copy.yaml")
    with pytest.raises(build.BuildError, match="duplicate id|file name must match"):
        build.build(data_copy)


# --- choosing between the author fit and the data points ---------------------

SCHUMACHER = "Li50Pb50-S-H-schumacher1990"


def _shift_author_fit(content):
    # exp(0.7) ~ 2: the author fit no longer matches the points
    content["reported"]["author_fit"]["intercept"] = -8.17 + 0.7


def test_disagreeing_author_fit_needs_a_choice(data_copy):
    _edit(data_copy, SCHUMACHER, _shift_author_fit)
    with pytest.raises(build.BuildError, match="disagree by .* Set reported.selected"):
        build.build(data_copy)


def test_curator_can_select_the_refit(data_copy):
    note = "author fit inconsistent with Fig. 3 points; cannot tell which is wrong"

    def choose_refit(content):
        _shift_author_fit(content)
        content["reported"]["selected"] = "htm_refit"
        content["reported"]["selection_note"] = note

    _edit(data_copy, SCHUMACHER, choose_refit)
    record = next(r for r in build.build(data_copy)["records"] if "schumacher" in r["id"])
    n = record["normalized"]
    assert n["selected"] == "htm_refit"
    assert n["pre_exp"] == n["htm_refit"]["pre_exp"]
    assert n["fit_discrepancy"]["max_relative"] > build.FIT_TOLERANCE
    assert {"op": "htm_refit", "rationale": note} in record["htm_assumptions"]


def test_explicit_selection_needs_a_note(data_copy):
    _edit(data_copy, SCHUMACHER, _set(["reported", "selected"], "htm_refit"))
    with pytest.raises(build.BuildError, match="needs a selection_note"):
        build.build(data_copy)
