"""The contribution bot: issue forms -> records, and the record report"""

import io
import json
import shutil
import urllib.error
from pathlib import Path

import pytest
import yaml

from h_transport_materials.records import build, contribute, report
from h_transport_materials.records.contribute import ContributionError

HERE = Path(__file__).parent
FORMS = HERE.parent / ".github" / "ISSUE_TEMPLATE"

CSL = {
    "type": "journal-article",
    "title": "Hydrogen isotopes in metals, measured again",
    "author": [{"family": "Doe", "given": "Jane"}, {"family": "Roe", "given": "R."}],
    "issued": {"date-parts": [[2025]]},
    "container-title": "Journal of Nuclear Materials",
    "DOI": "10.9999/test.2025.002",
}
NA = "Not applicable (diffusivity, recombination, dissociation)"
ARRHENIUS = "An Arrhenius law (pre-exponential factor and activation energy)"
POINTS_AND_FIT = "Data points and the authors' Arrhenius fit of them"
FRAUENFELDER = {
    "doi": "https://doi.org/10.9999/test.2025.002",
    "location": "Table 2",
    "property": "Diffusivity",
    "law": NA,
    "material": "tungsten",
    "isotope": "H",
    "method": "gas-permeation",
    "form": ARRHENIUS,
    "pre_exp": "4.1 × 10⁻³",
    "pre_exp_unit": "cm²/s",
    "act_energy": "9000",
    "act_energy_unit": "cal/mol",
    "t_min": "1100",
    "t_max": "2400",
    "t_unit": "K",
    "orcid": "https://orcid.org/0000-0002-1825-0097",
}


def fetch(doi):
    return CSL


@pytest.fixture
def data(tmp_path):
    """A copy of data/ with the hand-written records and a few migrated ones (fast to build)"""
    target = tmp_path / "data"
    shutil.copytree(build.DATA_DIR, target, ignore=shutil.ignore_patterns("records"))
    (target / "records").mkdir()
    keep = {"Ag-S-H-mclellan1973", "Ni-D-H-louthan1975", "SS304-S-H-hawkins1953"}
    for path in (build.DATA_DIR / "records").glob("*.yaml"):
        if path.stem in keep or "migrated_from:" not in path.read_text(encoding="utf-8"):
            for f in path.parent.glob(path.stem + ".*"):
                shutil.copy(f, target / "records")
    return target


def _record(contribution):
    rel = next(r for r in contribution.files if r.startswith("records/") and r.endswith(".yaml"))
    return yaml.safe_load(contribution.files[rel])


# --- the forms ---------------------------------------------------------------------


@pytest.mark.parametrize("name,kind", contribute.FORM_FILES.items())
def test_issue_forms_are_up_to_date(name, kind):
    """Regenerate them with `htm contribute form` after changing contribute.py or data/materials"""
    assert (FORMS / name).read_text(encoding="utf-8") == contribute.form_yaml(kind)


def test_form_lists_every_material():
    form = contribute.new_record_form(contribute._materials(build.DATA_DIR))
    options = next(i for i in form["body"] if i.get("id") == "material")["attributes"]["options"]
    assert set(options) == {p.stem for p in (build.DATA_DIR / "materials").glob("*.yaml")} | {contribute.OTHER_MATERIAL}


def test_form_labels_are_unique():
    """parse_issue_body maps labels to field ids"""
    for form in (contribute.new_record_form(["tungsten"]), contribute.change_record_form()):
        labels = [i["attributes"]["label"] for i in form["body"] if i.get("id")]
        assert len(labels) == len(set(labels))


# --- parsing -----------------------------------------------------------------------


def test_parse_github_issue_body():
    body = (HERE / "contrib" / "new-record-points.md").read_text(encoding="utf-8")
    fields = contribute.parse_issue_body(body, contribute.new_record_form(["nickel"]))
    assert fields["doi"] == "10.9999/test.2025.002"
    assert fields["material"] == "nickel"
    assert fields["fit_note"] is None  # _No response_
    assert fields["points"].startswith("1000/T, log10 D\n2.00000, -11.03182")  # no code fence
    assert fields["checks"].startswith("- [X] I typed")


def test_parse_ignores_unknown_headings():
    fields = contribute.parse_issue_body("### DOI\n\n10.1/x\n\n### Something else\n\nhello\n", contribute.new_record_form([]))
    assert fields == {"doi": "10.1/x"}


def test_parse_rejects_huge_issue():
    with pytest.raises(ContributionError, match="64 KB"):
        contribute.parse_issue_body("x" * (contribute.MAX_BODY + 1), contribute.new_record_form([]))


@pytest.mark.parametrize(
    "text,expected",
    [("4.1e-3", 4.1e-3), ("4.1 × 10^-3", 4.1e-3), ("4.1x10⁻³", 4.1e-3), ("4,1E-3", 4.1e-3), ("-0.5", -0.5), (".5", 0.5)],
)
def test_parse_number(text, expected):
    assert contribute.parse_number(text) == pytest.approx(expected, rel=1e-15)


@pytest.mark.parametrize("text", ["four", "4.1e", "1-2", "10^-3"])
def test_parse_number_rejects(text):
    with pytest.raises(ValueError):
        contribute.parse_number(text)


@pytest.mark.parametrize(
    "text,unit",
    [
        ("cm^2/s", "cm^2/s"),
        ("cm²/s", "cm^2/s"),
        ("cm2/s", "cm^2/s"),
        ("m2.s-1", "m^2*s^-1"),
        ("mol/m3/Pa0.5", "mol/m^3/Pa^0.5"),
        ("mol m−1 s−1 Pa−1/2", "mol m^-1 s^-1 Pa^-0.5"),
        ("mol·m⁻³·Pa⁻⁰·⁵", "mol*m^-3*Pa^-0.5"),
        ("cm^3(STP)/cm^3/atm^0.5", "ccSTP/cm^3/atm^0.5"),
        ("kJ/mol", "kJ/mol"),
        ("°C", "degC"),
    ],
)
def test_parse_unit_keeps_what_was_typed(text, unit):
    assert contribute.parse_unit(text) == (unit, None if unit == text else text)


def test_parse_unit_rejects_nonsense():
    with pytest.raises(ValueError):
        contribute.parse_unit("bananas/s")


def test_parse_points_skips_header_and_reports_bad_lines():
    assert contribute.parse_points("T, D\n500; 1e-9\n600\t2e-9\n") == [(500, 1e-9), (600, 2e-9)]
    with pytest.raises(ContributionError, match="line 3"):
        contribute.parse_points("500, 1e-9\n600, 2e-9\n700, 3e-9, 4\n")


# --- new records -------------------------------------------------------------------------


def test_new_arrhenius_record(data):
    c = contribute.new_record(FRAUENFELDER, data, author="janedoe", issue=42, fetch=fetch)
    assert c.record_id == "htm:W-D-H-doe2025"
    assert set(c.files) == {"records/W-D-H-doe2025.yaml", "sources/doe2025.yaml"}
    rec = _record(c)
    assert rec["reported"]["pre_exp"] == {"value": 4.1e-3, "unit": "cm^2/s", "unit_as_printed": "cm²/s"}
    assert rec["reported"]["act_energy"] == {"value": 9000.0, "unit": "cal/mol"}
    assert rec["reported"]["range"] == {"value": [1100.0, 2400.0], "unit": "K"}
    assert rec["source"] == {"doi": "10.9999/test.2025.002", "location": "Table 2"}
    assert rec["curation"]["status"] == "draft"
    assert rec["curation"]["contributed_by"] == ["https://orcid.org/0000-0002-1825-0097"]
    assert "issue #42" in rec["curation"]["flags"][0]
    assert "0.3903 eV" in c.summary  # same as Frauenfelder 1969: 9000 cal/mol


def test_written_record_builds_and_loads(data):
    contribute.new_record(FRAUENFELDER, data, author="janedoe", issue=42, fetch=fetch).write(data)
    db = build.build(data)
    rec = next(r for r in db["records"] if r["id"] == "htm:W-D-H-doe2025")
    assert rec["normalized"]["pre_exp"]["value"] == pytest.approx(4.1e-7)


def test_new_points_record_from_github_body(data):
    body = (HERE / "contrib" / "new-record-points.md").read_text(encoding="utf-8")
    issue = {"number": 7, "body": body, "user": {"login": "janedoe"}, "labels": [{"name": "new-record"}]}
    result = contribute.from_issue(issue, data, fetch=fetch)
    assert result["ok"], result["comment"]
    assert result["files"] == [
        "data/records/Ni-D-D-doe2025.yaml",
        "data/records/Ni-D-D-doe2025.csv",
        "data/sources/doe2025.yaml",
    ]
    rec = yaml.safe_load((data / "records" / "Ni-D-D-doe2025.yaml").read_text(encoding="utf-8"))
    assert rec["reported"]["x"] == {"column": 0, "quantity": "inverse_temperature", "unit": "1/K", "factor": 1000.0}
    assert rec["reported"]["y"] == {"column": 1, "quantity": "value", "unit": "m^2/s", "scale": "log10"}
    assert rec["reported"]["author_fit"]["pre_exp"]["unit_as_printed"] == "m2.s-1"
    assert rec["curation"]["contributed_by"] == ["github:janedoe"]
    assert (data / "records" / "Ni-D-D-doe2025.csv").read_text(encoding="utf-8").startswith("2.0,-11.03182\n")
    assert "Closes #7." in result["pr_body"] and "```yaml" in result["pr_body"]
    db = build.build(data)
    n = next(r for r in db["records"] if r["id"] == "htm:Ni-D-D-doe2025")["normalized"]
    assert n["selected"] == "author_fit"
    assert n["act_energy"]["value"] == pytest.approx(0.4, rel=1e-3)


def _points_fields(**extra):
    body = (HERE / "contrib" / "new-record-points.md").read_text(encoding="utf-8")
    fields = contribute.parse_issue_body(body, contribute.new_record_form(["nickel"]))
    fields.update(extra)
    return fields


def test_disagreeing_fit_asks_the_contributor_to_choose(data):
    with pytest.raises(ContributionError, match="If the points and the authors' fit disagree"):
        contribute.new_record(_points_fields(pre_exp="3e-7"), data, fetch=fetch)
    c = contribute.new_record(
        _points_fields(pre_exp="3e-7", fit_choice="Use HTM's fit of the points", fit_note="the fit is for another sample"),
        data,
        fetch=fetch,
    )
    assert _record(c)["reported"]["selected"] == "htm_refit"


def test_all_problems_are_reported_at_once(data):
    fields = dict(FRAUENFELDER, property="Solubility", pre_exp="", pre_exp_unit="bananas", t_max="900")
    fields["pre_exp"] = None
    with pytest.raises(ContributionError) as e:
        contribute.new_record(fields, data, fetch=fetch)
    text = e.value.markdown()
    assert "**Law**" in text and "**Pre-exponential factor** is empty" in text
    assert "lowest temperature must be below" in text
    assert not e.value.maintainer


def test_unknown_material_suggests_close_ones(data):
    with pytest.raises(ContributionError, match="Did you mean tungsten"):
        contribute.new_record(dict(FRAUENFELDER, material="tungstem"), data, fetch=fetch)


def test_other_material_needs_a_maintainer(data):
    with pytest.raises(ContributionError) as e:
        contribute.new_record(dict(FRAUENFELDER, material=contribute.OTHER_MATERIAL), data, fetch=fetch)
    assert e.value.maintainer


def test_unit_of_the_wrong_kind_is_caught_by_the_build(data):
    with pytest.raises(ContributionError, match="not compatible with a diffusivity"):
        contribute.new_record(dict(FRAUENFELDER, pre_exp_unit="mol/m^3/Pa^0.5"), data, fetch=fetch)


def test_known_doi_reuses_the_source_and_suffixes_the_id(data):
    def no_fetch(doi):
        raise AssertionError("the source file exists, doi.org must not be called")

    c = contribute.new_record(dict(FRAUENFELDER, doi="https://doi.org/10.1116/1.1492699"), data, fetch=no_fetch)
    assert c.record_id == "htm:W-D-H-frauenfelder1969-b"
    assert not any(rel.startswith("sources/") for rel in c.files)
    assert any("htm:W-D-H-frauenfelder1969" in w for w in c.warnings)


def test_unknown_doi(data):
    def not_found(doi):
        raise urllib.error.HTTPError("https://doi.org/" + doi, 404, "Not Found", {}, io.BytesIO())

    with pytest.raises(ContributionError, match="doi.org does not know"):
        contribute.new_record(FRAUENFELDER, data, fetch=not_found)


def test_failed_issue_gives_a_comment_and_writes_nothing(data):
    form = contribute.new_record_form(contribute._materials(data))
    body = contribute.render_issue_body(form, dict(FRAUENFELDER, pre_exp_unit="bananas"))
    issue = {"number": 3, "body": body, "user": {"login": "x"}, "labels": [{"name": "new-record"}]}
    result = contribute.from_issue(issue, data, fetch=fetch)
    assert not result["ok"]
    assert result["comment"].startswith(contribute.MARKER) and "bananas" in result["comment"]
    assert not (data / "records" / "W-D-H-doe2025.yaml").exists()


# --- changes to records --------------------------------------------------------------------------


@pytest.fixture
def built(data):
    return {r["id"]: r for r in build.build(data)["records"]}


@pytest.mark.parametrize(
    "record_id",
    ["htm:W-D-H-frauenfelder1969", "htm:W-D-H-heinola2010", "htm:Ag-S-H-mclellan1973", "htm:Li50Pb50-S-H-schumacher1990"],
)
def test_prefilled_change_form_changes_nothing(data, built, record_id):
    """The explorer prefills the form with the current values: submitting it as is must not edit anything"""
    fields = contribute.prefill_change(built[record_id])
    fields["reason"] = "just looking"
    with pytest.raises(ContributionError, match="Nothing differs"):
        contribute.change_record(fields, data, author="x", issue=1)


def test_prefill_survives_the_issue_body(built):
    """Prefilled values go through GitHub's markdown and come back the same"""
    fields = contribute.prefill_change(built["htm:Li50Pb50-S-H-schumacher1990"])
    form = contribute.change_record_form()
    assert contribute.parse_issue_body(contribute.render_issue_body(form, fields), form) == {
        **{i["id"]: None for i in form["body"] if i.get("id")},
        **fields,
    }


def test_change_a_unit(data, built):
    fields = contribute.prefill_change(built["htm:W-D-H-frauenfelder1969"])
    old_unit = fields["pre_exp_unit"]
    fields.update(pre_exp_unit="mm^2/s", reason="Table 2 prints mm^2/s, not cm^2/s")
    c = contribute.change_record(fields, data, author="janedoe", issue=9)
    rec = _record(c)
    assert rec["reported"]["pre_exp"]["unit"] == "mm^2/s"
    assert "changed through issue #9 (Table 2 prints mm^2/s, not cm^2/s)" in rec["curation"]["flags"][-1]
    assert "github:janedoe" in rec["curation"]["contributed_by"]
    assert f"| Pre-exponential factor | 0.0041 {old_unit} | 0.0041 mm^2/s |" in c.summary
    assert "EXPECTED_DIFFERENCES" not in c.summary  # hand-written, not migrated


def test_change_adds_the_range_and_drops_the_assumed_one(data, built):
    fields = contribute.prefill_change(built["htm:W-D-H-heinola2010"])
    fields.update(t_min="300", t_max="2500", t_unit="K", reason="Fig. 4 spans 300 to 2500 K")
    rec = _record(contribute.change_record(fields, data, issue=2))
    assert rec["reported"]["range"] == {"value": [300.0, 2500.0], "unit": "K"}
    assert not any(t["op"] == "assume_range" for t in rec.get("transformations", []))


def test_change_points_of_a_migrated_record(data, built):
    fields = contribute.prefill_change(built["htm:Ag-S-H-mclellan1973"])
    fields.update(points="941, 0.6\n921, 0.58\n881, 0.41", reason="re-digitised Fig. 2")
    c = contribute.change_record(fields, data, issue=5)
    assert c.files["records/Ag-S-H-mclellan1973.csv"] == "941.0,0.6\n921.0,0.58\n881.0,0.41\n"
    assert "EXPECTED_DIFFERENCES" in c.summary


def test_flag_only(data, built):
    fields = {"record": "W-D-H-frauenfelder1969", "kind": "Only flag it for a verifier", "reason": "Is it  really\n 1100 K?"}
    c = contribute.change_record(fields, data, issue=11)
    rec = _record(c)
    assert rec["curation"]["flags"][-1] == "issue #11: Is it really 1100 K?"
    original = (build.DATA_DIR / "records" / "W-D-H-frauenfelder1969.yaml").read_text(encoding="utf-8")
    assert rec["reported"] == yaml.safe_load(original)["reported"]


def test_change_unknown_record(data):
    with pytest.raises(ContributionError, match="Did you mean `htm:W-D-H-frauenfelder1969`"):
        contribute.change_record({"record": "htm:W-D-H-frauenfelder1996", "kind": "Change the values", "reason": "x"}, data)


def test_change_of_a_derived_record_needs_a_maintainer(data):
    derived = next(
        (p for p in (build.DATA_DIR / "records").glob("*.yaml") if "form: derived" in p.read_text(encoding="utf-8")), None
    )
    if derived is None:
        pytest.skip("no derived record")
    shutil.copy(derived, data / "records")
    for rec in yaml.safe_load(derived.read_text(encoding="utf-8"))["reported"]["factors"]:
        for f in (build.DATA_DIR / "records").glob(rec["record"].removeprefix("htm:") + ".*"):
            shutil.copy(f, data / "records")
    fields = {"record": derived.stem, "kind": "Change the values", "reason": "wrong", "pre_exp": "1", "pre_exp_unit": "m^2/s"}
    with pytest.raises(ContributionError) as e:
        contribute.change_record(fields, data)
    assert e.value.maintainer


# --- the record report ------------------------------------------------------------------------------------


def test_report_on_a_new_and_a_changed_record(data, tmp_path):
    base = build.build(data)
    contribute.new_record(dict(FRAUENFELDER, pre_exp_unit="m^2/s"), data, fetch=fetch).write(data)  # 10^4 too high
    built_ = {r["id"]: r for r in base["records"]}
    fields = contribute.prefill_change(built_["htm:W-D-H-frauenfelder1969"])
    contribute.change_record(dict(fields, act_energy="9500", reason="typo"), data).write(data)
    head = build.build(data)

    d = report.diff(base, head)
    assert [r["id"] for r in d["added"]] == ["htm:W-D-H-doe2025"]
    assert [h["id"] for _, h in d["changed"]] == ["htm:W-D-H-frauenfelder1969"]

    names = report.write_plots(base, head, tmp_path / "plots")
    assert sorted(names.values()) == ["W-D-H-doe2025.png", "W-D-H-frauenfelder1969.png"]
    assert all((tmp_path / "plots" / n).stat().st_size > 10_000 for n in names.values())

    text = report.report_markdown(base, head, {i: f"https://example.org/{n}" for i, n in names.items()})
    assert text.startswith(report.MARKER)
    assert "1 added, 1 changed, 0 removed." in text
    assert "![htm:W-D-H-doe2025](https://example.org/W-D-H-doe2025.png)" in text
    assert "times the median" in text  # the unit mistake stands out
    assert "new source file" in text
    assert "**Changes to normalised values**" in text and "`htm:W-D-H-frauenfelder1969`" in text
    assert "`reported.act_energy.value` | 9000.0 | 9500.0" in text


def test_report_without_changes(data):
    db = build.build(data)
    assert "No record is added, changed or removed." in report.report_markdown(db, db)


def test_report_cli(data, tmp_path):
    db = build.build(data)
    (tmp_path / "base.json").write_text(json.dumps({**db, "records": db["records"][1:]}), encoding="utf-8")
    (tmp_path / "head.json").write_text(json.dumps(db), encoding="utf-8")
    report.main(["--base", str(tmp_path / "base.json"), "--head", str(tmp_path / "head.json"),
                 "--out", str(tmp_path / "r.md"), "--plots", str(tmp_path / "p"), "--plot-url", "https://x/y/"])
    name = db["records"][0]["id"].removeprefix("htm:")
    assert f"](https://x/y/{name}.png)" in (tmp_path / "r.md").read_text(encoding="utf-8")
