"""Curation: verifying and disputing records.

A record starts as a draft. Someone who did not contribute it checks it
against the paper and verifies it, which adds an entry to
``curation.verifications``. Open flags must be resolved first: verifying with
a note saying how moves them into that entry, so the record keeps both the
question and the answer. A verified record whose values change goes back to
draft: ``htm curate check`` fails on a pull request until it is verified again.

On a pull request, someone with write access to the repository comments::

    /verify htm:W-D-H-frauenfelder1969
    Checked Table 2 and eq. 3. The method is gas permeation (section 2).

The lines that are not commands are the note. ``/verify all`` verifies every
record the pull request adds or changes, and ``/dispute <id> <reason>`` marks
a record as disputed. ``.github/workflows/curate.yml`` runs
``htm curate from-comment`` and commits the result to the pull request.

    htm curate verify <id> --by <who> [--note ...]     from the command line
    htm curate dispute <id> --by <who> --reason ...
    htm curate from-comment comment.json --pr pr.json  the bot
    htm curate check --base base/data --head data      verified records changed since
"""

import argparse
import datetime
import difflib
import json
import re
import sys
from pathlib import Path

import yaml
from pydantic import ValidationError

from . import build
from .models import Curation, Record

MARKER = "<!-- htm-curation-bot -->"
COMMAND = re.compile(r"^[ \t]*/(verify|dispute)\b[ \t]*(.*?)[ \t]*$", re.M)
CURATION_KEYS = list(Curation.model_fields)


class CurationError(Exception):
    """Why a verification or a dispute was refused (markdown, shown to the curator)"""


# --- the record files -------------------------------------------------------------


def normalize_id(record_id):
    record_id = record_id.strip().strip("`")
    return record_id if record_id.startswith("htm:") else "htm:" + record_id


def record_path(data_dir, record_id):
    stem = normalize_id(record_id).removeprefix("htm:")
    path = Path(data_dir) / "records" / f"{stem}.yaml"
    if not path.exists():
        stems = [p.stem for p in (Path(data_dir) / "records").glob("*.yaml")]
        close = difflib.get_close_matches(stem, stems, n=3)
        raise CurationError(
            f"There is no record `htm:{stem}`."
            + (f" Did you mean {', '.join(f'`htm:{c}`' for c in close)}?" if close else "")
        )
    return path


def _dump(content):
    return yaml.safe_dump(content, sort_keys=False, allow_unicode=True, width=100)


def replace_curation(text, curation):
    """The YAML text of a record with its ``curation`` block replaced

    Only that block is rewritten, so the rest of the file keeps its layout
    (flow mappings, comments).
    """
    lines = text.splitlines(keepends=True)
    start = next((i for i, line in enumerate(lines) if re.match(r"curation:", line)), None)
    block = _dump({"curation": curation})
    if start is None:
        return text + ("" if text.endswith("\n") or not text else "\n") + block
    end = start + 1
    while end < len(lines) and (not lines[end].strip() or lines[end][0] in " \t"):
        end += 1
    # blank lines before the next key stay where they were
    while end > start + 1 and not lines[end - 1].strip():
        end -= 1
    return "".join(lines[:start]) + block + "".join(lines[end:])


def _ordered(curation):
    known = {k: curation[k] for k in CURATION_KEYS if k in curation}
    return known | {k: v for k, v in curation.items() if k not in known}


def _validate(record_id, text):
    try:
        Record(**yaml.safe_load(text))
    except ValidationError as e:
        problems = "; ".join(f"{'.'.join(map(str, err['loc']))}: {err['msg']}" for err in e.errors())
        raise CurationError(f"`{record_id}` would not be valid: {problems}") from e


# --- verify and dispute -----------------------------------------------------------


def verify_text(text, record_id, by, note=None, pr=None, commit=None, today=None, excluded=()):
    """Verifies a record given as YAML text

    Args:
        by (str): who verifies, ``https://orcid.org/...`` or ``github:<login>``
        note (str, optional): what was checked; required when flags are open,
            to say how they were resolved
        excluded (iterable of str): identities that may not verify this record
            (besides its contributors), e.g. the author of the pull request
            that changed it

    Returns:
        str: the new YAML text
    """
    record_id = normalize_id(record_id)
    content = yaml.safe_load(text)
    curation = dict(content.get("curation") or {})
    contributors = set(curation.get("contributed_by") or [])
    if by in contributors or by in set(excluded):
        raise CurationError(
            f"`{by}` contributed to `{record_id}` (or changed it in this pull request):"
            " someone else has to verify it."
        )
    if curation.get("status") == "verified" and any(v.get("by") == by for v in curation.get("verifications") or []):
        raise CurationError(f"`{record_id}` is already verified by `{by}`.")
    note = (note or "").strip() or None
    flags = list(curation.get("flags") or [])
    if flags and not note:
        listed = "\n".join(f"  - {f}" for f in flags)
        raise CurationError(
            f"`{record_id}` has open flags. Check them against the paper, then verify again with a note"
            f" (the lines after the command) saying how each was resolved, or fix the record and remove them:\n{listed}"
        )
    entry = {"by": by, "date": today or datetime.date.today()}
    if pr is not None:
        entry["pr"] = int(pr)
    if commit:
        entry["commit"] = commit
    if note:
        entry["note"] = note
    if flags:
        entry["resolved_flags"] = flags
    curation["status"] = "verified"
    curation["verifications"] = list(curation.get("verifications") or []) + [entry]
    curation.pop("flags", None)
    new = replace_curation(text, _ordered(curation))
    _validate(record_id, new)
    return new


def dispute_text(text, record_id, by, reason, pr=None):
    """Marks a record given as YAML text as disputed, with the reason as a flag"""
    record_id = normalize_id(record_id)
    reason = re.sub(r"\s+", " ", reason or "").strip()
    if not reason:
        raise CurationError(f"Say why `{record_id}` is disputed: `/dispute {record_id} <reason>`.")
    content = yaml.safe_load(text)
    curation = dict(content.get("curation") or {})
    where = f" in PR #{pr}" if pr is not None else ""
    curation["status"] = "disputed"
    curation["flags"] = list(curation.get("flags") or []) + [f"disputed by {by}{where}: {reason}"]
    new = replace_curation(text, _ordered(curation))
    _validate(record_id, new)
    return new


def verify(record_id, by, data_dir=build.DATA_DIR, **kwargs):
    """Verifies a record file in place (see :func:`verify_text`). Returns its path"""
    path = record_path(data_dir, record_id)
    text = verify_text(path.read_text(encoding="utf-8"), record_id, by, **kwargs)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def dispute(record_id, by, reason, data_dir=build.DATA_DIR, pr=None):
    """Marks a record file as disputed, in place. Returns its path"""
    path = record_path(data_dir, record_id)
    text = dispute_text(path.read_text(encoding="utf-8"), record_id, by, reason, pr=pr)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


# --- what a pull request changed --------------------------------------------------


def _records(data_dir):
    """record id -> (content without curation, data files, curation)"""
    out = {}
    folder = Path(data_dir) / "records"
    for path in sorted(folder.glob("*.yaml")):
        with open(path, encoding="utf-8") as f:
            content = yaml.safe_load(f) or {}
        curation = content.pop("curation", None) or {}
        files = {p.name: p.read_bytes() for p in folder.glob(path.stem + ".*") if p.suffix != ".yaml"}
        out[content.get("id") or "htm:" + path.stem] = (content, files, curation)
    return out


def changed_records(base_dir, head_dir):
    """Ids of the records added or changed between two data folders, curation aside

    Returns:
        dict: record id -> ``"added"`` or ``"changed"``
    """
    before, after = _records(base_dir), _records(head_dir)
    out = {}
    for i, (content, files, _) in after.items():
        if i not in before:
            out[i] = "added"
        elif before[i][:2] != (content, files):
            out[i] = "changed"
    return out


def stale_verifications(base_dir, head_dir):
    """Verified records whose values changed but that were not verified again

    Returns:
        list[str]: one message per record
    """
    before, after = _records(base_dir), _records(head_dir)
    out = []
    for i in changed_records(base_dir, head_dir):
        if i not in before:
            continue
        b, h = before[i][2], after[i][2]
        if b.get("status") != "verified" or h.get("status") != "verified":
            continue
        if len(h.get("verifications") or []) <= len(b.get("verifications") or []):
            out.append(
                f"`{i}` was verified and its values changed: set `curation.status` to draft,"
                " or have someone else check it and comment `/verify` on the pull request"
            )
    return out


# --- the bot ------------------------------------------------------------------------


def parse_comment(body):
    """The commands of a pull request comment and the note around them

    Returns:
        tuple: (list of (command, arguments), note)
    """
    body = (body or "").replace("\r\n", "\n")
    commands = [(m.group(1), m.group(2)) for m in COMMAND.finditer(body)]
    note = COMMAND.sub("", body)
    note = "\n".join(line.rstrip() for line in note.split("\n")).strip()
    note = re.sub(r"\n{3,}", "\n\n", note)
    return commands, note or None


def from_comment(comment, pr, data_dir, base_dir, issue=None, dry_run=False, today=None):
    """Handles a ``/verify`` or ``/dispute`` comment on a pull request

    The workflow has already checked that the commenter has write access.

    Args:
        comment (dict): the comment, as in the ``issue_comment`` event
        pr (dict): the pull request (REST API)
        data_dir (Path): ``data/`` at the head of the pull request
        base_dir (Path): ``data/`` at the merge base
        issue (dict, optional): the issue a contribution bot PR was opened
            from; its author cannot verify the records it adds or changes

    Returns:
        dict: ``ok``, ``files`` (path relative to the repository -> text),
            ``done`` (what was done, one line each) and ``comment``
    """
    login = (comment.get("user") or {}).get("login")
    by = f"github:{login}"
    number = pr.get("number")
    commit = (pr.get("head") or {}).get("sha")
    commands, note = parse_comment(comment.get("body"))
    changed = changed_records(base_dir, data_dir)
    excluded = set()
    author = pr.get("user") or {}
    if author.get("type") != "Bot":
        excluded.add(f"github:{author.get('login')}")
    if issue and (issue.get("user") or {}).get("login"):
        excluded.add(f"github:{issue['user']['login']}")

    texts, done, errors = {}, [], []

    def text_of(record_id):
        path = record_path(data_dir, record_id)
        if path not in texts:
            texts[path] = path.read_text(encoding="utf-8")
        return path

    for command, args in commands:
        try:
            if command == "verify":
                ids = [a for a in re.split(r"[\s,]+", args) if a]
                if not ids:
                    raise CurationError("Say which records: `/verify htm:<id>` or `/verify all`.")
                if ids == ["all"]:
                    ids = sorted(changed)
                    if not ids:
                        raise CurationError("This pull request adds or changes no record: name the records to verify.")
                for record_id in map(normalize_id, ids):
                    path = text_of(record_id)
                    n_flags = len((yaml.safe_load(texts[path]).get("curation") or {}).get("flags") or [])
                    texts[path] = verify_text(
                        texts[path], record_id, by, note=note, pr=number, commit=commit, today=today,
                        excluded=excluded if record_id in changed else (),
                    )
                    done.append(
                        f"verified `{record_id}`" + (f" ({n_flags} flag{'s' * (n_flags > 1)} resolved)" if n_flags else "")
                    )
            else:
                record_id, _, reason = args.partition(" ")
                if not record_id:
                    raise CurationError("Say which record: `/dispute htm:<id> <reason>`.")
                reason = " ".join(x for x in (reason, note) if x)
                path = text_of(record_id)
                texts[path] = dispute_text(texts[path], record_id, by, reason, pr=number)
                done.append(f"marked `{normalize_id(record_id)}` as disputed")
        except CurationError as e:
            errors.append(str(e))

    if not commands:
        errors.append("No command found: start a line with `/verify htm:<id>`, `/verify all` or `/dispute htm:<id> <reason>`.")
    if errors:
        body = "\n\n".join(["I did not change anything:", *[f"- {e}" for e in errors]])
        return {"ok": False, "files": {}, "done": [], "comment": f"{MARKER}\n{body}"}

    root = Path(data_dir).parent
    files = {path.relative_to(root).as_posix(): text for path, text in texts.items()}
    if not dry_run:
        for path, text in texts.items():
            path.write_text(text, encoding="utf-8", newline="\n")
    short = commit[:7] if commit else "the head of this pull request"
    body = "\n".join([f"Done, as `{by}` at {short}:", *[f"- {d}" for d in done]])
    if note:
        body += "\n\nNote recorded with " + ("them" if len(done) > 1 else "it") + ":\n\n" + "\n".join(
            "> " + line for line in note.split("\n")
        )
    return {"ok": True, "files": files, "done": done, "comment": f"{MARKER}\n{body}"}


def _yaml_details(files):
    return "\n\n".join(
        f"<details><summary><code>{rel}</code></summary>\n\n```yaml\n{text}```\n\n</details>"
        for rel, text in files.items()
    )


# --- command line -------------------------------------------------------------------


def main(argv=None):
    parser = argparse.ArgumentParser(prog="htm curate", description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    v = sub.add_parser("verify", help="verify records against their source")
    v.add_argument("record", nargs="+")
    v.add_argument("--by", required=True, help="https://orcid.org/... or github:<login>")
    v.add_argument("--note", help="what was checked; required when the record has open flags")
    v.add_argument("--pr", type=int)
    v.add_argument("--commit")
    v.add_argument("--data", type=Path, default=build.DATA_DIR)
    d = sub.add_parser("dispute", help="mark a record as disputed")
    d.add_argument("record")
    d.add_argument("--by", required=True)
    d.add_argument("--reason", required=True)
    d.add_argument("--pr", type=int)
    d.add_argument("--data", type=Path, default=build.DATA_DIR)
    c = sub.add_parser("from-comment", help="handle a /verify or /dispute comment on a pull request (the bot)")
    c.add_argument("comment", type=Path, help="the comment JSON (REST API or event payload)")
    c.add_argument("--pr", type=Path, required=True, help="the pull request JSON (REST API)")
    c.add_argument("--issue", type=Path, help="the issue a contribution bot PR comes from (REST API JSON)")
    c.add_argument("--data", type=Path, required=True, help="data/ at the head of the pull request")
    c.add_argument("--base", type=Path, required=True, help="data/ at the merge base")
    c.add_argument("--result", type=Path, help="where to write the result JSON for the workflow")
    c.add_argument("--dry-run", action="store_true")
    k = sub.add_parser("check", help="fail if a verified record changed without being verified again")
    k.add_argument("--base", type=Path, required=True, help="data/ at the merge base")
    k.add_argument("--head", type=Path, default=build.DATA_DIR)
    args = parser.parse_args(argv)

    try:
        if args.command == "verify":
            for record_id in args.record:
                path = verify(record_id, args.by, args.data, note=args.note, pr=args.pr, commit=args.commit)
                print(f"verified {normalize_id(record_id)} ({path})")
        elif args.command == "dispute":
            path = dispute(args.record, args.by, args.reason, args.data, pr=args.pr)
            print(f"marked {normalize_id(args.record)} as disputed ({path})")
    except CurationError as e:
        sys.exit(f"error: {e}")
    if args.command == "check":
        problems = stale_verifications(args.base, args.head)
        for p in problems:
            print(p.replace("`", ""))
        if problems:
            sys.exit(1)
        print("no verified record changed without being verified again")
    elif args.command == "from-comment":
        load = lambda p: json.loads(p.read_text(encoding="utf-8")) if p else None  # noqa: E731
        comment, pr, issue = load(args.comment), load(args.pr), load(args.issue)
        comment = comment.get("comment", comment)  # the whole event payload works too
        result = from_comment(comment, pr, args.data, args.base, issue=issue, dry_run=args.dry_run)
        result["files_details"] = _yaml_details(result["files"])
        if args.result:
            args.result.write_text(json.dumps(result, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
        print(result["comment"].removeprefix(MARKER).strip())
