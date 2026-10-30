"""The record report posted on pull requests that touch ``data/``.

Compares two compiled databases (the PR's base and head) and writes, for each
record added or changed, a plot of it next to the other records of the same
material, its values as typed and as normalised,
and checks a reviewer should look at. The checks only warn: the build has
already rejected what is invalid.

Usage::

    htm report --base base.json --head head.json --out report.md --plots plots/
"""

import argparse
import json
import math
from pathlib import Path

from scipy import constants

MARKER = "<!-- htm-record-report -->"
K_B = constants.k / constants.e  # eV/K, same CODATA value as htm.k_B
MAX_PLOTS = 12
MAX_CHARS = 60000  # GitHub comments are limited to 65536 characters

LABELS = {
    ("diffusivity", None): "Diffusivity (m$^2$ s$^{-1}$)",
    ("solubility", "sieverts"): "Solubility (m$^{-3}$ Pa$^{-0.5}$)",
    ("solubility", "henry"): "Solubility (m$^{-3}$ Pa$^{-1}$)",
    ("permeability", "sieverts"): "Permeability (m$^{-1}$ s$^{-1}$ Pa$^{-0.5}$)",
    ("permeability", "henry"): "Permeability (m$^{-1}$ s$^{-1}$ Pa$^{-1}$)",
    ("recombination_coeff", None): "Recombination coefficient (m$^4$ s$^{-1}$)",
    ("dissociation_coeff", None): "Dissociation coefficient (m$^{-2}$ s$^{-1}$ Pa$^{-1}$)",
}
ISOTOPE_MARKERS = {"H": "o", "D": "s", "T": "^"}
# not compared: computed by the build from what is compared
DERIVED_KEYS = ("normalized", "htm_assumptions", "transformation_log", "derived")


def law(rec):
    """(pre_exp, act_energy in eV, range in K or None) of a built record"""
    n = rec["normalized"]
    if n["selected"] == "constant":
        T = n["temperature"]["value"]
        return n["value"]["value"], 0.0, (T, T)
    r = n.get("range")
    return n["pre_exp"]["value"], n["act_energy"]["value"], tuple(r["value"]) if r else None


def value(rec, T):
    A, E, _ = law(rec)
    return A * math.exp(-E / (K_B * T))


def mid_temperature(*recs):
    for rec in recs:
        r = law(rec)[2]
        if r:
            return 0.5 * (r[0] + r[1])
    return 600.0


def diff(base, head):
    """Records added, changed and removed between two compiled databases

    Returns:
        dict: ``added`` (head records), ``changed`` ((base, head) pairs) and
            ``removed`` (base records)
    """
    before = {r["id"]: r for r in base["records"]}
    after = {r["id"]: r for r in head["records"]}
    stored = lambda r: {k: v for k, v in r.items() if k not in DERIVED_KEYS}  # noqa: E731
    return {
        "added": [r for i, r in after.items() if i not in before],
        "changed": [
            (before[i], r)
            for i, r in after.items()
            if i in before and (stored(before[i]) != stored(r) or law(before[i]) != law(r))
        ],
        "removed": [r for i, r in before.items() if i not in after],
    }


def _same_kind(a, b):
    return a["property"] == b["property"] and a.get("law") == b.get("law")


def same_material(rec, db):
    """The other records of the same material, property and law (all isotopes)"""
    return [
        r for r in db["records"] if r["id"] != rec["id"] and r["material"] == rec["material"] and _same_kind(r, rec)
    ]


def _source_label(rec, sources):
    s = sources.get(_source_key(rec, sources))
    if not s:
        return rec["id"]
    people = s.get("authors") or s.get("editors") or [{"family": "?"}]
    return f"{people[0]['family']} {s['year']}"


def _source_key(rec, sources):
    ref = rec["source"]
    if ref.get("key"):
        return ref["key"]
    doi = (ref.get("doi") or "").lower()
    return next((k for k, s in sources.items() if (s.get("doi") or "").lower() == doi), None)


def plot_record(rec, db, path, before=None):
    """Plots a record against the other records of the same material

    Args:
        rec (dict): the built record
        db (dict): the compiled database it belongs to
        path (Path): the PNG to write
        before (dict, optional): the record before a change, drawn dashed
    """
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    sources = {s["key"]: s for s in db["sources"]}
    same = same_material(rec, db)
    fig, ax = plt.subplots(figsize=(7.5, 4.8), dpi=110)

    def T_span(r):
        T_range = law(r)[2]
        return T_range or (300.0, 1200.0)

    # the window: this record and the others of its material
    spans = [T_span(r) for r in [rec, *same] + ([before] if before else [])]
    lo, hi = min(s[0] for s in spans), max(s[1] for s in spans)
    lo, hi = (lo - 50, hi + 50) if lo == hi else (lo, hi)

    def draw(r, **kwargs):
        A, E, T_range = law(r)
        if T_range and T_range[0] == T_range[1]:
            ax.plot([1000 / T_range[0]], [A], ls="none", marker=ISOTOPE_MARKERS[r["isotope"]], **kwargs)
            return
        T = np.linspace(*T_span(r), 60)
        ax.plot(1000 / T, A * np.exp(-E / (K_B * T)), ls=kwargs.pop("ls", "-" if T_range else ":"), **kwargs)

    colours = plt.get_cmap("tab10").colors
    for i, r in enumerate(sorted(same, key=lambda r: r["id"])):
        if len(same) <= 10:
            draw(r, color=colours[i], lw=1.3, zorder=2, label=f"{_source_label(r, sources)} ({r['isotope']})")
        else:
            draw(r, color=colours[0], lw=1.0, alpha=0.6, zorder=2, label=None if i else f"other {rec['material']} records")
    if before is not None:
        draw(before, color="black", lw=1.5, ls="--", zorder=3, label="before this PR")
    draw(rec, color="black", lw=2.8, zorder=4, label=f"{_source_label(rec, sources)} ({rec['isotope']}), this PR")
    pts = rec["normalized"].get("points")
    if pts:
        T, y = np.array(pts["T"]["value"]), np.array(pts["y"]["value"])
        ok = np.isfinite(T) & np.isfinite(y)
        ax.scatter(1000 / T[ok], y[ok], color="black", s=14, zorder=5, marker=ISOTOPE_MARKERS[rec["isotope"]])

    ax.set_yscale("log")
    ax.set_xlabel("1000 / T (K$^{-1}$)")
    ax.set_ylabel(LABELS[(rec["property"], rec.get("law"))])
    x0, x1 = 1000 / hi, 1000 / lo
    pad = 0.04 * (x1 - x0)
    ax.set_xlim(x0 - pad, x1 + pad)
    top = ax.twiny()
    top.set_xlim(ax.get_xlim())
    ticks = []
    for T in (200, 250, 300, 400, 500, 600, 700, 800, 1000, 1200, 1500, 2000, 2500, 3000, 4000):
        # at least 8% of the axis apart, so the labels do not overlap
        if lo <= T <= hi and (not ticks or 1000 / ticks[-1] - 1000 / T >= 0.08 * (x1 - x0)):
            ticks.append(T)
    top.set_xticks([1000 / T for T in ticks], [str(T) for T in ticks])
    top.set_xlabel("T (K)", fontsize=9)
    ax.set_title(
        f"{rec['id']}\n{len(same)} other {rec['material']} records with this property (all isotopes)",
        fontsize=8,
        loc="left",
    )
    ax.grid(True, which="major", alpha=0.3)
    ax.legend(fontsize=7, loc="center left", bbox_to_anchor=(1.01, 0.5), frameon=False)
    fig.tight_layout()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    plt.close(fig)
    return path


def checks(rec, db, base=None):
    """Warnings a reviewer should look at"""
    out = []
    A, E, T_range = law(rec)
    if not (A > 0 and math.isfinite(A)):
        out.append(f"the pre-exponential factor is {A:g}")
    low = 0.0 if rec["property"] == "diffusivity" else -3.0
    if not low <= E <= 3.0:
        out.append(f"the activation energy, {E:.3g} eV, is outside the usual {low:g} to 3 eV")
    if T_range and not (0 < T_range[0] and T_range[1] <= 4000):
        out.append(f"the range {T_range[0]:g} to {T_range[1]:g} K is outside 0 to 4000 K")
    if T_range is None:
        out.append("no temperature range")

    same = same_material(rec, db)
    if same:
        T = mid_temperature(rec)
        others = sorted(value(r, T) for r in same)
        half = len(others) // 2
        median = others[half] if len(others) % 2 else 0.5 * (others[half - 1] + others[half])
        ratio = value(rec, T) / median if median > 0 else math.inf
        if not 0.1 <= ratio <= 10:
            out.append(
                f"at {T:.0f} K it is {ratio:.3g} times the median of the {len(same)} other"
                f" {rec['material']} records: check the units"
            )
    sources = {s["key"]: s for s in db["sources"]}
    key = _source_key(rec, sources)
    twins = [
        r["id"]
        for r in same
        if _source_key(r, sources) == key and r["isotope"] == rec["isotope"] and (base is None or r["id"] in base)
    ]
    if twins:
        out.append(f"the same paper already gives {', '.join(f'`{t}`' for t in twins)}: is it a duplicate?")
    fd = rec["normalized"].get("fit_discrepancy")
    if fd and fd["max_relative"] > 0.03:
        out.append(f"the authors' fit and the points differ by up to {fd['max_relative']:.1%}")
    return out


def _fmt_reported(rec):
    rep = rec["reported"]
    q = lambda x: f"{x['value']:.4g} {x.get('unit_as_printed') or x['unit']}" if x else "not given"  # noqa: E731
    rng = lambda x: f"{x['value'][0]:g} to {x['value'][1]:g} {x.get('unit', 'K')}" if x else "not given"  # noqa: E731
    if rep["form"] == "arrhenius":
        return f"{q(rep['pre_exp'])}, {q(rep['act_energy'])}, {rng(rep.get('range'))}"
    if rep["form"] == "points":
        n = len(rec["normalized"]["points"]["T"]["value"])
        fit = rep.get("author_fit")
        fit_txt = ""
        if fit and fit["form"] == "arrhenius":
            fit_txt = f"; authors' fit {q(fit.get('pre_exp'))}, {q(fit.get('act_energy'))}"
        return f"{n} points from `{rep['file']}`{fit_txt}"
    if rep["form"] == "constant":
        return f"{q(rep['value'])} at {q(rep['temperature'])}"
    return rep["form"]


UNITS = {
    ("diffusivity", None): "m²/s",
    ("solubility", "sieverts"): "m⁻³ Pa⁻⁰·⁵",
    ("solubility", "henry"): "m⁻³ Pa⁻¹",
    ("permeability", "sieverts"): "m⁻¹ s⁻¹ Pa⁻⁰·⁵",
    ("permeability", "henry"): "m⁻¹ s⁻¹ Pa⁻¹",
    ("recombination_coeff", None): "m⁴/s",
    ("dissociation_coeff", None): "m⁻² s⁻¹ Pa⁻¹",
}


def _fmt_normalized(rec):
    A, E, T_range = law(rec)
    r = f", {T_range[0]:g} to {T_range[1]:g} K" if T_range else ""
    return f"{A:.4g} {UNITS[(rec['property'], rec.get('law'))]}, {E:.4g} eV{r}"


def _paths(a, b, prefix=""):
    """Paths of the leaves that differ between two stored records"""
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in list(a) + [k for k in b if k not in a]:
            out += _paths(a.get(k), b.get(k), f"{prefix}.{k}" if prefix else k)
        return out
    return [] if a == b else [(prefix, a, b)]


def _short(v):
    s = json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v
    return s if len(s) <= 80 else s[:77] + "..."


def _record_section(rec, db, base_db, plot_url, before=None):
    sources = {s["key"]: s for s in db["sources"]}
    key = _source_key(rec, sources)
    s = sources.get(key, {})
    people = s.get("authors") or s.get("editors") or []
    authors = ", ".join(p["family"] for p in people[:3]) + (" et al." if len(people) > 3 else "")
    new_source = key not in {x["key"] for x in base_db["sources"]}
    lines = [f"### {'Changed' if before else 'New'}: `{rec['id']}`", ""]
    if plot_url:
        lines += [f"![{rec['id']}]({plot_url})", ""]
    lines += [
        "| | |",
        "| --- | --- |",
        f"| Property | {rec['property'].replace('_', ' ')}{', ' + rec['law'] if rec.get('law') else ''},"
        f" {rec['isotope']} in {rec['material']} |",
        f"| Source | {authors} ({s.get('year', '?')}), *{s.get('title', '?')}*"
        f"{' (new source file: check it against the paper)' if new_source else ''} |",
        f"| Location | {rec['source'].get('location') or 'not given'} |",
        f"| As typed | {_fmt_reported(rec)} |",
        f"| Normalised | {_fmt_normalized(rec)} |",
    ]
    if before is not None:
        T = mid_temperature(rec, before)
        change = value(rec, T) / value(before, T) - 1
        lines.append(f"| Before | {_fmt_normalized(before)} |")
        lines.append(f"| Change at {T:.0f} K | {change:+.3g} ({change:+.1%}) |")
        stored = [(p, a, b) for p, a, b in _paths(
            {k: v for k, v in before.items() if k not in DERIVED_KEYS},
            {k: v for k, v in rec.items() if k not in DERIVED_KEYS},
        )]
        if stored:
            lines += ["", "<details><summary>Fields changed in the YAML</summary>", ""]
            lines += ["| Field | Before | After |", "| --- | --- | --- |"]
            lines += [f"| `{p}` | {_short(a)} | {_short(b)} |" for p, a, b in stored[:40]]
            lines += ["", "</details>"]
    warnings = checks(rec, db, base={r["id"] for r in base_db["records"]})
    if warnings:
        lines += ["", "**To check:**"] + [f"- {w}" for w in warnings]
    return "\n".join(lines)


def report_markdown(base, head, plot_urls=None):
    """The report comment

    Args:
        plot_urls (dict, optional): record id -> URL of its plot
    """
    d = diff(base, head)
    plot_urls = plot_urls or {}
    parts = [MARKER, "## Record report", ""]
    n_a, n_c, n_r = len(d["added"]), len(d["changed"]), len(d["removed"])
    if not (n_a or n_c or n_r):
        parts.append("No record is added, changed or removed.")
        return "\n".join(parts)
    parts.append(f"{n_a} added, {n_c} changed, {n_r} removed.")
    value_changes = []
    for b, h in d["changed"]:
        T = mid_temperature(h, b)
        change = value(h, T) / value(b, T) - 1
        if law(b) != law(h):
            value_changes.append(f"| `{h['id']}` | {change:+.3g} at {T:.0f} K | {_fmt_normalized(b)} | {_fmt_normalized(h)} |")
    if value_changes:
        parts += [
            "",
            "**Changes to normalised values** (to list in the commit and the PR):",
            "",
            "| Record | Relative change | Before | After |",
            "| --- | --- | --- | --- |",
            *value_changes,
        ]
    for rec in d["added"]:
        parts += ["", _record_section(rec, head, base, plot_urls.get(rec["id"]))]
    for b, h in d["changed"]:
        parts += ["", _record_section(h, head, base, plot_urls.get(h["id"]), before=b)]
    if d["removed"]:
        parts += ["", "### Removed", ""]
        parts += [f"- `{r['id']}`: record ids are permanent, is this intended?" for r in d["removed"]]
    parts += [
        "",
        "<sub>Plots: this record in black, the other records of the same material and property in colour"
        " (all isotopes); dotted where the paper gives no range. The checks only warn.</sub>",
    ]
    text = "\n".join(parts)
    if len(text) > MAX_CHARS:
        text = text[: MAX_CHARS - 200] + "\n\n... (truncated: see the job summary for the full report)"
    return text


def write_plots(base, head, folder):
    """Plots added and changed records. Returns record id -> PNG file name"""
    d = diff(base, head)
    todo = [(r, None) for r in d["added"]] + [(h, b) for b, h in d["changed"] if law(b) != law(h)]
    out = {}
    for rec, before in todo[:MAX_PLOTS]:
        name = rec["id"].removeprefix("htm:") + ".png"
        plot_record(rec, head, Path(folder) / name, before=before)
        out[rec["id"]] = name
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(prog="htm report", description=__doc__.splitlines()[0])
    parser.add_argument("--base", type=Path, required=True, help="compiled database of the PR's base")
    parser.add_argument("--head", type=Path, required=True, help="compiled database of the PR")
    parser.add_argument("--out", type=Path, default=Path("report.md"))
    parser.add_argument("--plots", type=Path, help="folder for the plots (none if omitted)")
    parser.add_argument("--plot-url", help="URL of the plots folder, to embed them in the report")
    args = parser.parse_args(argv)

    with open(args.base, encoding="utf-8") as f:
        base = json.load(f)
    with open(args.head, encoding="utf-8") as f:
        head = json.load(f)
    names = write_plots(base, head, args.plots) if args.plots else {}
    urls = {i: f"{args.plot_url.rstrip('/')}/{n}" for i, n in names.items()} if args.plot_url else {}
    text = report_markdown(base, head, urls)
    args.out.write_text(text + "\n", encoding="utf-8")
    print(f"report written to {args.out}: {len(names)} plots")
