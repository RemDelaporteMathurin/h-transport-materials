"""Builds the static HTM site (GitHub Pages) from the YAML records.

Usage::

    python pages/build.py --out _site [--branch NAME] [--commit SHA]

Writes:
    index.html                  the explorer (pages/template.html with the data inlined)
    records/<id>/index.html     one page per record, with schema.org metadata
    htm-data.json               the compiled database, as shipped in the wheel
    schema/*.schema.json        JSON Schemas of records, materials and sources

Needs the build extra (pydantic, pyyaml), not the rest of the library.
"""

import argparse
import html
import json
import math
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from h_transport_materials.records import build, schema  # noqa: E402

REPO = "https://github.com/RemDelaporteMathurin/h-transport-materials"

CLASSES = {
    "diffusivity": "Diffusivity",
    "solubility": "Solubility",
    "permeability": "Permeability",
    "recombination_coeff": "RecombinationCoeff",
    "dissociation_coeff": "DissociationCoeff",
}
UNITS = {
    ("diffusivity", None): "m²/s",
    ("solubility", "sieverts"): "m⁻³ Pa⁻⁰·⁵",
    ("solubility", "henry"): "m⁻³ Pa⁻¹",
    ("permeability", "sieverts"): "m⁻¹ s⁻¹ Pa⁻⁰·⁵",
    ("permeability", "henry"): "m⁻¹ s⁻¹ Pa⁻¹",
    ("recombination_coeff", None): "m⁴/s",
    ("dissociation_coeff", None): "m⁻² s⁻¹ Pa⁻¹",
}
LAWS = {"sieverts": "sievert", "henry": "henry", None: None}


def _people(source):
    people = source.get("authors") or source.get("editors") or []
    names = [p["family"] for p in people]
    return names, "; ".join(names[:4]) + (" et al." if len(names) > 4 else "")


def compact(db):
    """One small dict per record, with the fields the explorer uses"""
    materials = {m["id"]: m for m in db["materials"]}
    sources = {s["key"]: s for s in db["sources"]}
    out = []
    for r in db["records"]:
        n = r["normalized"]
        src = sources[r["source"]["key"]]
        names, authors = _people(src)
        if n["selected"] == "constant":
            T = n["temperature"]["value"]
            A, E, T_range = n["value"]["value"], 0.0, [T, T]
        else:
            A, E = n["pre_exp"]["value"], n["act_energy"]["value"]
            T_range = n["range"]["value"] if n.get("range") else None
        sample = r.get("sample") or {}
        entry = {
            "id": r["id"],
            "file": r["id"].removeprefix("htm:"),
            "t": CLASSES[r["property"]],
            "m": r["material"],
            "fam": materials[r["material"]].get("families", []),
            "a": names[0].lower() if names else "",
            "y": src["year"],
            "iso": r["isotope"],
            "A": A,
            "E": E,
            "u": UNITS[(r["property"], r.get("law"))],
            "law": LAWS[r.get("law")],
            "r": T_range,
            "doi": r["source"].get("doi") or src.get("doi"),
            "src": src["key"],
            "title": src["title"],
            "journal": src.get("journal"),
            "authors": authors,
            "loc": r["source"].get("location"),
            "note": r.get("note"),
            "method": r.get("method"),
            "sample": sample.get("form") or sample.get("surface"),
            "rep": r["reported"],
            "tr": r.get("transformations") or [],
            "asm": r.get("htm_assumptions") or [],
            "status": r["curation"]["status"],
            "flags": r["curation"].get("flags") or [],
            "sel": n["selected"],
        }
        if "points" in n:
            # some point files keep the legacy nan,nan padding rows; the
            # browser's JSON.parse rejects NaN, so they are left out here
            pairs = [(T, y) for T, y in zip(n["points"]["T"]["value"], n["points"]["y"]["value"])
                     if math.isfinite(T) and math.isfinite(y)]
            entry["dT"] = [round(T, 3) for T, _ in pairs]
            entry["dy"] = [float(f"{y:.5g}") for _, y in pairs]
        if "fit_discrepancy" in n:
            entry["fd"] = n["fit_discrepancy"]["max_relative"]
        out.append({k: v for k, v in entry.items() if v is not None})
    return out


def _git(*args):
    try:
        return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def record_page(rec, raw, branch):
    """A small static page per record: the citable URL, with schema.org metadata"""
    e = html.escape
    jsonld = {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "identifier": rec["id"],
        "name": f"{rec['t']} of hydrogen ({rec['iso']}) in {rec['m']}, {rec['a'].capitalize()} {rec['y']}",
        "description": f"{rec['t']} record of H-Transport Materials, as published in {rec['title']}",
        "isBasedOn": f"https://doi.org/{rec['doi']}" if rec.get("doi") else None,
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "url": f"{REPO}/blob/{branch}/data/records/{rec['file']}.yaml",
    }
    jsonld = {k: v for k, v in jsonld.items() if v is not None}
    body = json.dumps(raw, indent=1, ensure_ascii=False)
    flags = "".join(f"<li>{e(f)}</li>" for f in rec.get("flags", []))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(rec['id'])} | H-Transport Materials</title>
<meta name="description" content="{e(jsonld['name'])}">
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
<style>
:root {{ --bg: #f5f6f8; --fg: #16202c; --muted: #5b6878; --line: #dde2e9; --accent: #1f5fbf; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg: #0f141b; --fg: #e3e8ef; --muted: #93a0b1; --line: #2a3441; --accent: #7fb0ff; }} }}
body {{ background: var(--bg); color: var(--fg); font: 15px/1.5 system-ui, sans-serif; margin: 0; }}
main {{ max-width: 860px; margin: 0 auto; padding: 24px 16px; }}
a {{ color: var(--accent); }}
.muted {{ color: var(--muted); }}
pre {{ border: 1px solid var(--line); border-radius: 6px; padding: 12px; overflow-x: auto; font-size: 12.5px; }}
code {{ font-family: ui-monospace, Menlo, monospace; }}
</style>
</head>
<body>
<main>
<p><a href="../../#{e(rec['id'])}">Open in the explorer</a> · <a href="{e(jsonld['url'])}">YAML on GitHub</a></p>
<h1>{e(rec['a'].capitalize())} {rec['y']}: {e(rec['t'])}, {e(rec['m'])}, {e(rec['iso'])}</h1>
<p><code>{e(rec['id'])}</code> · status: <b>{e(rec['status'])}</b></p>
<p>{e(rec['title'])}{'. ' + e(rec['journal']) if rec.get('journal') else ''}. {e(rec['authors'])}.
{f'<a href="https://doi.org/{e(rec["doi"])}">doi:{e(rec["doi"])}</a>' if rec.get('doi') else ''}</p>
{f'<p class="muted">Note: {e(rec["note"])}</p>' if rec.get('note') else ''}
{f'<h2>Open questions</h2><ul>{flags}</ul>' if flags else ''}
<h2>Record</h2>
<p class="muted">As published (<code>reported</code>), what HTM did (<code>transformations</code>),
and the normalised values.</p>
<pre><code>{e(body)}</code></pre>
</main>
</body>
</html>
"""


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=Path("_site"))
    parser.add_argument("--data", type=Path, default=build.DATA_DIR)
    parser.add_argument("--branch", default=None)
    parser.add_argument("--commit", default=None)
    args = parser.parse_args(argv)

    branch = args.branch or _git("rev-parse", "--abbrev-ref", "HEAD")
    commit = (args.commit or _git("rev-parse", "HEAD"))[:7]
    db = build.build(args.data, data_version=f"{branch}@{commit}")
    records = compact(db)

    args.out.mkdir(parents=True, exist_ok=True)
    # allow_nan=False: a NaN or Infinity would stop the page's JSON.parse and
    # leave it blank, so fail the build instead
    payload = json.dumps(records, separators=(",", ":"), ensure_ascii=False, allow_nan=False).replace("</", "<\\/")
    page = (HERE / "template.html").read_text(encoding="utf-8")
    for key, value in (("__DB__", payload), ("__BRANCH__", branch), ("__COMMIT__", commit),
                       ("__VERSION__", f"{branch}@{commit}")):
        page = page.replace(key, value)
    (args.out / "index.html").write_text(page, encoding="utf-8")

    by_id = {r["id"]: r for r in db["records"]}
    for rec in records:
        folder = args.out / "records" / rec["file"]
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "index.html").write_text(record_page(rec, by_id[rec["id"]], branch), encoding="utf-8")

    (args.out / "htm-data.json").write_text(json.dumps(db, ensure_ascii=False), encoding="utf-8")
    (args.out / "schema").mkdir(exist_ok=True)
    for name, s in schema.json_schemas().items():
        (args.out / "schema" / f"{name}.schema.json").write_text(json.dumps(s, indent=1), encoding="utf-8")
    (args.out / ".nojekyll").write_text("", encoding="utf-8")
    print(f"site written to {args.out}: {len(records)} records, index.html {len(page) // 1024} KB")


if __name__ == "__main__":
    main()
