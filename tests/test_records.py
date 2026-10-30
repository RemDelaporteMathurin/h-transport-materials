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

def _molar_mass(li, pb):
    return li * M_LI + pb * M_PB


# Records whose values intentionally differ from the current database.
# range: the range differs; ratio: expected new / old pre-exponential factor;
# rel: tolerance on it; author_fit: same law within 3%, different parameters
EXPECTED_DIFFERENCES = {
    # single value at 450 degC, was a fake 722-724 K range
    "htm:LiPb-D-H-fauvet1988": {"range": True},
    "htm:LiPb-S-H-fauvet1988": {"range": True},
    # single value at 573 K, was a fake 572-574 K range; converted with the
    # molar mass of the Pb-15.7Li sample instead of Pb-17Li
    "htm:LiPb-S-H-candido2022": {"range": True, "ratio": _molar_mass(17, 83) / _molar_mass(15.7, 84.3)},
    "htm:LiPb-S-H-candido2022-b": {"range": True, "ratio": _molar_mass(17, 83) / _molar_mass(15.7, 84.3)},
    # the authors' fit is used; the current entry refits the digitised points
    "htm:Li50Pb50-S-H-schumacher1990": {"author_fit": True},
    # registry densities are the cited values, the current code used values
    # derived from them (molar volume 1.3e-5 m3/mol, specific volume 8.32e-8 m3/g)
    "htm:Li-S-H-veleckis1974": {"rel": 2e-4},
    "htm:Li-S-H-smith1979": {"rel": 2e-4},
    "htm:Li-S-D-smith1979": {"rel": 2e-4},
    "htm:Li-S-T-smith1979": {"rel": 2e-4},
    "htm:Pd-S-T-favreau1954": {"rel": 1e-5},
    "htm:Pd-S-H-favreau1954": {"rel": 1e-5},
    # FLiBe molar mass from the atomic weight table instead of webqc.org values
    "htm:FLiBe-S-H-field1967": {"rel": 1e-6},
    "htm:FLiBe-S-D-field1967": {"rel": 1e-6},
    # used for testing the automated workflow + realised there was a typo in the original paper
    "htm:Fe-D-H-addach2005": {"ratio": 1e6}
}


@pytest.fixture(scope="module")
def db():
    return build.build()


@pytest.fixture(scope="module")
def group(db):
    return compat.to_properties_group(db)


@pytest.fixture(scope="module")
def manifest():
    """record id -> index of the property it replaces in htm.legacy_database()"""
    with open(build.DATA_DIR / "migration" / "legacy.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_every_record_is_in_the_manifest(db, manifest):
    """Every record that replaces a legacy property is in the manifest; records
    contributed since (never in the legacy database) are not"""
    ids = {r["id"] for r in db["records"]}
    assert set(manifest) <= ids
    for r in db["records"]:
        if r["id"] not in manifest:
            assert not r["curation"].get("migrated_from"), f"{r['id']} is migrated but not in the manifest"
    indices = [entry["index"] for entry in manifest.values()]
    assert len(indices) == len(set(indices)), "two records replace the same property"


def test_equivalence_with_current_database(group, manifest):
    """Each record reproduces the property it replaces, except listed differences"""
    for new in group:
        entry = manifest.get(new.record_id)
        if entry is None:  # contributed after the migration
            continue
        old = htm.legacy_database()[entry["index"]]
        assert type(old).__name__ == entry["class"], (
            f"{new.record_id}: the legacy database changed order, rerun htm migrate"
        )
        difference = EXPECTED_DIFFERENCES.get(new.record_id, {})
        assert new.material == old.material, new.record_id
        if old.source in htm.bib_database.entries:
            # (otherwise the current code cites free text, here a source file)
            assert new.source == old.source, new.record_id
        assert new.isotope == (old.isotope or "").upper(), new.record_id
        new_range = [T.m_as("K") for T in new.range] if new.range else None
        old_range = [T.m_as("K") for T in old.range] if old.range else None

        if difference.get("author_fit"):
            # different parameters, same law within 3% over the measured range
            T = np.linspace(*old_range, 50) * htm.ureg.K
            ratio = (new.value(T) / old.value(T)).to("dimensionless").magnitude
            assert np.abs(ratio - 1).max() < 0.03
            assert new_range == pytest.approx(old_range, rel=1e-12)
            continue

        assert new.pre_exp.to(old.pre_exp.units).magnitude == pytest.approx(
            old.pre_exp.magnitude * difference.get("ratio", 1), rel=difference.get("rel", 1e-12)
        ), new.record_id
        assert new.act_energy.m_as("eV/particle") == pytest.approx(
            old.act_energy.m_as("eV/particle"), rel=1e-12, abs=1e-15
        ), new.record_id
        if difference.get("range"):
            assert new_range != pytest.approx(old_range)
        elif old_range is None:
            assert new_range is None, new.record_id
        else:
            assert new_range == pytest.approx(old_range, rel=1e-12), new.record_id


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
    assert [a["op"] for a in record["htm_assumptions"]] == ["mole_fraction_to_concentration"]


def test_heinola_range_is_an_htm_assumption(db):
    record = next(r for r in db["records"] if "heinola" in r["id"])
    assert record["reported"]["range"] is None
    assert record["htm_assumptions"][0]["op"] == "assume_range"


def test_registry_matches_schema():
    assert set(transforms.REGISTRY) == set(typing.get_args(models.TransformationOp))


def test_json_schema_validates_yaml_records():
    jsonschema = pytest.importorskip("jsonschema")
    record_schema = schema.json_schemas()["record"]
    validator = jsonschema.validators.validator_for(record_schema)(record_schema)
    for path in (build.DATA_DIR / "records").glob("*.yaml"):
        validator.validate(yaml.safe_load(path.read_text(encoding="utf-8")))

    bad = yaml.safe_load(
        (build.DATA_DIR / "records" / "W-D-H-heinola2010.yaml").read_text(encoding="utf-8")
    )
    bad["transformations"][0]["op"] = "make_it_up"
    with pytest.raises(jsonschema.ValidationError):
        validator.validate(bad)


# --- invalid records are rejected ---------------------------------------------


@pytest.fixture
def data_copy(tmp_path):
    """A copy of data/ with only the hand-written records (fast to build)"""
    target = tmp_path / "data"
    shutil.copytree(build.DATA_DIR, target, ignore=shutil.ignore_patterns("records"))
    (target / "records").mkdir()
    for path in (build.DATA_DIR / "records").glob("*.yaml"):
        if "migrated_from:" not in path.read_text(encoding="utf-8"):
            for f in path.parent.glob(path.stem + ".*"):
                shutil.copy(f, target / "records")
    return target


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
            _set(["material"], "unobtainium"),
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


# --- forms, transformations and registries used by the migration -------------


def _law(**fields):
    return models.LogLinear(form="log_linear", y_unit="m^2/s", **fields)


def test_log_linear_base_10_with_slope():
    pre_exp, act_energy = build._arrhenius_law(
        _law(base="10", intercept=-2, slope={"value": -1000, "unit": "K"})
    )
    assert pre_exp.m_as("m^2/s") == pytest.approx(1e-2)
    assert act_energy.m_as("eV/particle") == pytest.approx(
        (1000 * np.log(10) * htm.ureg.K * htm.k_B).m_as("eV/particle")
    )


def test_log_linear_with_activation_energy():
    _, act_energy = build._arrhenius_law(
        _law(intercept=-14.5, act_energy={"value": -18.2, "unit": "kJ/mol"})
    )
    assert act_energy.m_as("kJ/mol") == pytest.approx(-18.2)


def test_log_linear_needs_slope_or_energy():
    with pytest.raises(ValueError, match="exactly one of slope or act_energy"):
        _law(intercept=1)
    with pytest.raises(ValueError, match="exactly one of slope or act_energy"):
        _law(intercept=1, slope={"value": 1, "unit": "K"}, act_energy={"value": 1, "unit": "eV"})


@pytest.fixture(scope="module")
def registry():
    elements, materials, _, _ = build.load()
    return elements, materials


def test_molar_mass_per_formula_unit(registry):
    """FLiBe and SiC molar masses from formulas match the values in the current code"""
    elements, materials = registry
    flibe = transforms.molar_mass(materials["flibe"].formula_units, elements).m_as("g/mol")
    assert flibe == pytest.approx(0.66 * 25.9394 + 0.34 * 47.0089884, rel=1e-6)
    sic = transforms.molar_mass(materials["sic"].formula_units, elements).m_as("g/mol")
    assert sic == pytest.approx(40.096, rel=1e-6)


@pytest.mark.parametrize("formula", ["Lif", "2LiF", "Li-F", ""])
def test_bad_formula_rejected(formula):
    with pytest.raises(ValueError, match="cannot parse chemical formula"):
        transforms.parse_formula(formula)


def test_density_correlation(registry):
    _, materials = registry
    rho = transforms.density(materials["flibe"], 873 * htm.ureg.K)
    assert rho.m_as("kg/m^3") == pytest.approx(2413 - 0.488 * 873)
    with pytest.raises(ValueError, match="set density_at"):
        transforms.density(materials["flibe"])


def test_registry_densities_match_current_code(registry):
    """Registry densities reproduce the constants hard-coded in the current modules"""
    from h_transport_materials.property_database import carbon, palladium, sic
    from h_transport_materials.property_database.lithium import lithium

    _, materials = registry

    def rho(name):
        return transforms.density(materials[name]).m_as("kg/m^3")

    assert rho("graphite") == pytest.approx(carbon.graphite_density.m_as("kg/m^3"), rel=1e-12)
    assert rho("sic") == pytest.approx(sic.sic_density.m_as("kg/m^3"), rel=1e-12)
    assert rho("palladium") == pytest.approx(
        (1 / palladium.PALLADIUM_VOLUMIC_DENSITY).m_as("kg/m^3"), rel=1e-5
    )
    molar_volume = (6.941 * htm.ureg.g / htm.ureg.mol) / (rho("lithium") * htm.ureg("kg/m^3"))
    assert molar_volume.m_as("m^3/mol") == pytest.approx(
        lithium.LITHIUM_MOLAR_VOLUME.m_as("m^3/mol"), rel=2e-4
    )


def test_isotope_scaling_factor(db):
    record = next(r for r in db["records"] if r["id"] == "htm:Ni-D-T-louthan1975")
    assert record["derived"]["isotope_factor"]["value"] == pytest.approx(3**-0.5)
    assert record["htm_assumptions"][0]["op"] == "isotope_scaling"


@pytest.mark.parametrize(
    "name,edit,message",
    [
        (
            "W-D-H-esteban2001",
            _set(
                ["transformations"],
                [{"op": "concentration_ratio_to_solubility", "origin": "paper", "rationale": "test"}],
            ),
            "needs data points or a constant",
        ),
        (
            "Li-S-H-veleckis1974",
            _set(["transformations", 0, "params"], {"per": "formula_unit"}),
            "no formula units",
        ),
        (
            "Li-S-H-veleckis1974",
            _set(["transformations", 0, "params"], {"per": "molecule"}),
            "per must be atom or formula_unit",
        ),
        (
            "Mo-D-H-katsuta1982",
            _set(["reported", "act_energy"], {"value": 1, "unit": "eV"}),
            "exactly one of slope or act_energy",
        ),
    ],
)
def test_invalid_migration_record_rejected(data_copy, name, edit, message):
    _edit(data_copy, name, edit)
    with pytest.raises(build.BuildError, match=message):
        build.build(data_copy)


def test_sieverts_constant_inversion_flips_the_activation_energy():
    """1 / (K0 exp(-E/kT)) = (1/K0) exp(E/kT)"""
    u = htm.ureg
    state = transforms.State(target_unit=u.dimensionless)
    state.reported = 2.0 * u.atm**0.5
    state.act_energy = 0.3 * u.eV / u.particle
    transforms.sieverts_constant_to_solubility(state, {"concentration_unit": "atfr"}, None)
    assert state.reported.m_as("atfr / atm^0.5") == pytest.approx(0.5)
    assert state.act_energy.m_as("eV/particle") == pytest.approx(-0.3)


# --- derived records -------------------------------------------------------------


def _derived(record_id, prop, factors, law=None, **extra):
    content = {
        "id": record_id,
        "property": prop,
        "material": "tungsten",
        "isotope": "H",
        "method": "unknown",
        "source": {"doi": "10.1016/S0022-3115(01)00486-X"},
        "reported": {
            "form": "derived",
            "factors": [{"record": r, "power": p} for r, p in factors],
            "origin": "htm",
            "rationale": "test",
        },
        **extra,
    }
    if law:
        content["law"] = law
    return content


def _add(data_dir, content):
    name = content["id"].removeprefix("htm:")
    (data_dir / "records" / f"{name}.yaml").write_text(yaml.safe_dump(content), encoding="utf-8")


ESTEBAN_D, ESTEBAN_S = "htm:W-D-H-esteban2001", "htm:W-S-H-esteban2001"


def test_derived_product(data_copy):
    _add(data_copy, _derived("htm:W-P-H-esteban2001", "permeability",
                             [(ESTEBAN_D, 1), (ESTEBAN_S, 1)], law="sieverts"))
    records = {r["id"]: r for r in build.build(data_copy)["records"]}
    D, S, P = (records[i]["normalized"] for i in (ESTEBAN_D, ESTEBAN_S, "htm:W-P-H-esteban2001"))
    assert P["pre_exp"]["value"] == pytest.approx(D["pre_exp"]["value"] * S["pre_exp"]["value"])
    assert P["act_energy"]["value"] == pytest.approx(
        D["act_energy"]["value"] + S["act_energy"]["value"]
    )
    assert P["range"]["value"] == pytest.approx([673, 1073])
    assert records["htm:W-P-H-esteban2001"]["htm_assumptions"][0]["op"] == "derived"


@pytest.mark.parametrize(
    "contents,message",
    [
        ([_derived("htm:W-P-H-esteban2001", "permeability", [(ESTEBAN_D, 1), ("htm:W-S-H-nobody2000", 1)],
                   law="sieverts")], "unknown input records"),
        ([_derived("htm:W-P-H-esteban2001", "permeability", [(ESTEBAN_D, 1), ("htm:W-P-H-esteban2001-b", 1)],
                   law="sieverts"),
          _derived("htm:W-P-H-esteban2001-b", "permeability", [(ESTEBAN_D, 1), ("htm:W-P-H-esteban2001", 1)],
                   law="sieverts")], "circular"),
        ([_derived("htm:W-D-H-esteban2001-b", "diffusivity", [(ESTEBAN_D, 1), (ESTEBAN_S, 1)])],
         "do not combine into a diffusivity"),
        ([_derived("htm:W-P-H-esteban2001", "permeability", [(ESTEBAN_D, 1), (ESTEBAN_S, 1)], law="sieverts",
                   transformations=[{"op": "assume_range", "params": {"range": [1, 2]},
                                     "origin": "htm", "rationale": "test"}])],
         "cannot have transformations"),
    ],
)
def test_invalid_derived_rejected(data_copy, contents, message):
    for content in contents:
        _add(data_copy, content)
    with pytest.raises(build.BuildError, match=message):
        build.build(data_copy)
