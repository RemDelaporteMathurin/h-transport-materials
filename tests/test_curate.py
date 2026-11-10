"""Curation: /verify and /dispute, and verified records that change"""

import datetime
import shutil

import pytest
import yaml
from pydantic import ValidationError

from h_transport_materials.records import build, contribute, curate, report
from h_transport_materials.records.curate import CurationError
from h_transport_materials.records.models import Curation

TODAY = datetime.date(2026, 11, 10)
W = "htm:W-D-H-frauenfelder1969"
AG = "htm:Ag-S-H-mclellan1973"
RECORDS = ("W-D-H-frauenfelder1969", "Ag-S-H-mclellan1973", "Ni-D-H-louthan1975")


def _copy(target):
    shutil.copytree(build.DATA_DIR, target, ignore=shutil.ignore_patterns("records"))
    (target / "records").mkdir()
    for stem in RECORDS:
        for f in (build.DATA_DIR / "records").glob(stem + ".*"):
            shutil.copy(f, target / "records")
    return target


@pytest.fixture
def base(tmp_path):
    return _copy(tmp_path / "base" / "data")


@pytest.fixture
def data(tmp_path):
    return _copy(tmp_path / "head" / "data")


def _read(data, record_id):
    return yaml.safe_load(curate.record_path(data, record_id).read_text(encoding="utf-8"))


def _text(data, record_id):
    return curate.record_path(data, record_id).read_text(encoding="utf-8")


# --- verify and dispute ----------------------------------------------------------


def test_open_flags_need_a_note(data):
    with pytest.raises(CurationError, match="open flags") as e:
        curate.verify(W, "github:remi", data)
    assert "fill method and location" in str(e.value)
    assert _read(data, W)["curation"]["status"] == "draft"


def test_verify_resolves_the_flags_into_the_verification(data):
    before = _text(data, W)
    curate.verify(W, "github:remi", data, note="Table 1: gas permeation", pr=12, commit="abc1234", today=TODAY)
    rec = _read(data, W)
    assert rec["curation"] == {
        "status": "verified",
        "verifications": [
            {
                "by": "github:remi",
                "date": TODAY,
                "pr": 12,
                "commit": "abc1234",
                "note": "Table 1: gas permeation",
                "resolved_flags": ["fill method and location (table or equation) from the paper"],
            }
        ],
    }
    # only the curation block is rewritten
    after = _text(data, W)
    assert after.split("curation:")[0] == before.split("curation:")[0]
    assert "pre_exp: {value: 4.1e-3" in after


def test_verify_without_flags_needs_no_note(data):
    path = curate.record_path(data, W)
    path.write_text(path.read_text(encoding="utf-8").split("curation:")[0], encoding="utf-8")
    curate.verify("W-D-H-frauenfelder1969", "github:remi", data, today=TODAY)
    assert _read(data, W)["curation"] == {"status": "verified", "verifications": [{"by": "github:remi", "date": TODAY}]}


def test_contributors_cannot_verify(data):
    path = curate.record_path(data, W)
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("  status: draft\n", "  status: draft\n  contributed_by: [github:jane]\n"))
    with pytest.raises(CurationError, match="someone else"):
        curate.verify(W, "github:jane", data, note="ok")
    curate.verify(W, "github:remi", data, note="ok")


def test_the_same_person_does_not_verify_twice(data):
    curate.verify(W, "github:remi", data, note="ok")
    with pytest.raises(CurationError, match="already verified"):
        curate.verify(W, "github:remi", data)
    curate.verify(W, "github:jane", data)  # a second verifier
    assert [v["by"] for v in _read(data, W)["curation"]["verifications"]] == ["github:remi", "github:jane"]


def test_dispute_then_verify(data):
    curate.verify(W, "github:remi", data, note="ok")
    curate.dispute(W, "github:jane", "Fig. 3 gives\n another range", data, pr=4)
    cur = _read(data, W)["curation"]
    assert cur["status"] == "disputed"
    assert cur["flags"] == ["disputed by github:jane in PR #4: Fig. 3 gives another range"]
    with pytest.raises(CurationError, match="open flags"):
        curate.verify(W, "github:bob", data)
    curate.verify(W, "github:bob", data, note="Fig. 3 is for D, not H")
    assert _read(data, W)["curation"]["status"] == "verified"


def test_dispute_needs_a_reason(data):
    with pytest.raises(CurationError, match="why"):
        curate.dispute(W, "github:jane", "  ", data)


def test_unknown_record(data):
    with pytest.raises(CurationError, match="Did you mean `htm:W-D-H-frauenfelder1969`"):
        curate.verify("W-D-H-frauenfelder1968", "github:remi", data)


def test_a_verified_record_has_no_open_flag():
    Curation(status="verified", verifications=[{"by": "github:remi", "date": TODAY}])
    with pytest.raises(ValidationError, match="open flags"):
        Curation(status="verified", verifications=[{"by": "github:remi", "date": TODAY}], flags=["?"])
    with pytest.raises(ValidationError, match="verifications"):
        Curation(status="verified")


def test_replace_curation_keeps_what_follows():
    text = "id: x\ncuration:\n  status: draft\n  flags:\n    - a\n\n# about the next key\nnotes: kept\n"
    out = curate.replace_curation(text, {"status": "draft"})
    assert out == "id: x\ncuration:\n  status: draft\n\n# about the next key\nnotes: kept\n"
    assert curate.replace_curation("id: x\n", {"status": "draft"}) == "id: x\ncuration:\n  status: draft\n"


# --- the bot ----------------------------------------------------------------------


def _pr(author="jane", bot=False):
    return {"number": 7, "user": {"login": author, "type": "Bot" if bot else "User"}, "head": {"sha": "0123456789abc"}}


def _comment(body, login="remi"):
    return {"body": body, "user": {"login": login}}


def _change_W(data):
    path = curate.record_path(data, W)
    path.write_text(path.read_text(encoding="utf-8").replace("location: null", "location: Table 1"), encoding="utf-8")


def test_parse_comment():
    commands, note = curate.parse_comment("/verify htm:a htm:b\r\nChecked Table 2.\n\n/dispute htm:c wrong unit\n")
    assert commands == [("verify", "htm:a htm:b"), ("dispute", "htm:c wrong unit")]
    assert note == "Checked Table 2."
    assert curate.parse_comment("LGTM")[0] == []
    assert curate.parse_comment("see /verify in the docs")[0] == []  # only at the start of a line


def test_verify_all_from_a_comment(data, base):
    _change_W(data)
    result = curate.from_comment(_comment("/verify all\nTable 1, eq. 2"), _pr(), data, base, today=TODAY)
    assert result["ok"], result["comment"]
    assert list(result["files"]) == ["data/records/W-D-H-frauenfelder1969.yaml"]
    assert result["done"] == [f"verified `{W}` (1 flag resolved)"]
    v = _read(data, W)["curation"]["verifications"][0]
    assert v == {
        "by": "github:remi",
        "date": TODAY,
        "pr": 7,
        "commit": "0123456789abc",
        "note": "Table 1, eq. 2",
        "resolved_flags": ["fill method and location (table or equation) from the paper"],
    }
    assert "Done, as `github:remi` at 0123456" in result["comment"]


def test_the_author_of_a_change_cannot_verify_it(data, base):
    _change_W(data)
    result = curate.from_comment(_comment("/verify all\nok", login="jane"), _pr("jane"), data, base)
    assert not result["ok"] and "someone else" in result["comment"]
    # nor the author of the issue a bot PR comes from
    issue = {"user": {"login": "jane"}}
    bot_pr = _pr("htm-bot[bot]", bot=True)
    result = curate.from_comment(_comment("/verify all\nok", login="jane"), bot_pr, data, base, issue=issue)
    assert not result["ok"]
    # but the PR author can verify a record the PR does not change
    result = curate.from_comment(_comment(f"/verify {AG}\nok", login="jane"), _pr("jane"), data, base)
    assert result["ok"], result["comment"]


def test_a_comment_changes_all_or_nothing(data, base):
    before = _text(data, AG)
    result = curate.from_comment(_comment(f"/verify {AG}\n/verify htm:nope"), _pr(), data, base)
    assert not result["ok"]
    assert "There is no record `htm:nope`" in result["comment"]
    assert _text(data, AG) == before


def test_verify_all_with_nothing_changed(data, base):
    result = curate.from_comment(_comment("/verify all"), _pr(), data, base)
    assert not result["ok"] and "adds or changes no record" in result["comment"]


def test_dispute_from_a_comment(data, base):
    result = curate.from_comment(_comment(f"/dispute {AG} the unit is wrong\nsee Fig. 2"), _pr(), data, base, dry_run=True)
    assert result["ok"], result["comment"]
    cur = yaml.safe_load(result["files"]["data/records/Ag-S-H-mclellan1973.yaml"])["curation"]
    assert cur["status"] == "disputed"
    assert cur["flags"][-1] == "disputed by github:remi in PR #7: the unit is wrong see Fig. 2"
    assert _read(data, AG)["curation"]["status"] != "disputed"  # dry run


def test_cli_from_comment(data, base, tmp_path, capsys):
    import json

    _change_W(data)
    (tmp_path / "comment.json").write_text(json.dumps({"comment": _comment("/verify all\nok")}))
    (tmp_path / "pr.json").write_text(json.dumps(_pr()))
    curate.main([
        "from-comment", str(tmp_path / "comment.json"), "--pr", str(tmp_path / "pr.json"),
        "--data", str(data), "--base", str(base), "--result", str(tmp_path / "result.json"),
    ])
    result = json.loads((tmp_path / "result.json").read_text(encoding="utf-8"))
    assert result["ok"] and result["done"] == [f"verified `{W}` (1 flag resolved)"]
    assert "Done" in capsys.readouterr().out


# --- verified records that change -------------------------------------------------


def test_changed_records_ignore_curation(data, base):
    curate.verify(W, "github:remi", data, note="ok")
    assert curate.changed_records(base, data) == {}
    _change_W(data)
    csv = data / "records" / "Ag-S-H-mclellan1973.csv"
    csv.write_text(csv.read_text(encoding="utf-8") + "900,0.5\n", encoding="utf-8")
    assert curate.changed_records(base, data) == {W: "changed", AG: "changed"}


def test_stale_verification(data, base):
    curate.verify(W, "github:remi", base, note="ok")
    curate.verify(W, "github:remi", data, note="ok")
    assert curate.stale_verifications(base, data) == []
    _change_W(data)
    assert len(curate.stale_verifications(base, data)) == 1
    with pytest.raises(SystemExit):
        curate.main(["check", "--base", str(base), "--head", str(data)])
    curate.verify(W, "github:jane", data)  # verified again
    assert curate.stale_verifications(base, data) == []


def test_flagging_a_verified_record_takes_it_back_to_draft(data):
    curate.verify(W, "github:remi", data, note="ok")
    fields = {"record": W, "kind": "Only flag it for a verifier", "reason": "Is it really 1100 K?"}
    rec = yaml.safe_load(contribute.change_record(fields, data, issue=11).files["records/W-D-H-frauenfelder1969.yaml"])
    assert rec["curation"]["status"] == "draft"
    assert rec["curation"]["verifications"][0]["by"] == "github:remi"


def test_report_shows_curation(data, base, tmp_path):
    _change_W(data)
    curate.verify(W, "github:remi", data, note="ok", pr=7, today=TODAY)
    text = report.report_markdown(build.build(base), build.build(data))
    assert "| Curation | **verified**; verified by github:remi on 2026-11-10 (#7) |" in text
    assert f"| `{W}` | verified | 0 |" in text
    assert "/verify all" in text
    curate.dispute(W, "github:jane", "wrong range", data)
    text = report.report_markdown(build.build(base), build.build(data))
    assert "- disputed by github:jane: wrong range" in text
    assert f"| `{W}` | disputed | 1 |" in text


def test_report_says_when_to_verify_again(data, base):
    curate.verify(W, "github:remi", base, note="ok")
    curate.verify(W, "github:remi", data, note="ok")
    b = build.build(base)
    assert "### Curation" not in report.report_markdown(b, build.build(data))  # nothing changed
    _change_W(data)
    text = report.report_markdown(b, build.build(data))
    assert f"| `{W}` | verified, **needs verifying again**: its values changed | 0 |" in text
    curate.verify(W, "github:jane", data)
    assert f"| `{W}` | verified | 0 |" in report.report_markdown(b, build.build(data))
