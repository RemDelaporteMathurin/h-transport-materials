"""Turns GitHub issue forms into records: the contribution bot.

Two issue forms are generated from this module (``htm contribute form``):

- ``new-record.yml`` adds a record from a DOI and the values as printed;
- ``change-record.yml`` corrects an existing record, or flags it for a
  verifier.

``.github/workflows/contribute.yml`` runs ``htm contribute from-issue`` on
each new or edited issue. The issue body is parsed as text (nothing in it is
executed), the record files are written, and the whole database must still
build. Problems are reported back as sentences for the contributor, which
the workflow posts on the issue.
"""

import copy
import difflib
import json
import re
import shutil
import tempfile
import typing
import urllib.error
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from pydantic import ValidationError

from . import build, sources, units
from .doi import strip_doi
from .models import PROPERTY_CODES, Material, Method, Record

MARKER = "<!-- htm-contribution-bot -->"
MAX_BODY = 64 * 1024
MAX_POINTS = 1000

PROPERTIES = {
    "Diffusivity": "diffusivity",
    "Solubility": "solubility",
    "Permeability": "permeability",
    "Recombination coefficient": "recombination_coeff",
    "Dissociation coefficient": "dissociation_coeff",
}
LAWS = {
    "Sieverts' law (pressure^0.5)": "sieverts",
    "Henry's law (pressure)": "henry",
    "Not applicable (diffusivity and surface coefficients)": None,
}
FORMS = {
    "An Arrhenius law (pre-exponential factor and activation energy)": "arrhenius",
    "Data points": "points",
    "Data points and the authors' Arrhenius fit of them": "points_and_fit",
}
X_AXES = {
    "T (K)": {"quantity": "temperature", "unit": "K", "factor": 1.0},
    "T (°C)": {"quantity": "temperature", "unit": "degC", "factor": 1.0},
    "1000/T (1/K)": {"quantity": "inverse_temperature", "unit": "1/K", "factor": 1000.0},
    "10000/T (1/K)": {"quantity": "inverse_temperature", "unit": "1/K", "factor": 10000.0},
    "1/T (1/K)": {"quantity": "inverse_temperature", "unit": "1/K", "factor": 1.0},
}
Y_SCALES = {"the value": "linear", "ln(value)": "ln", "log10(value)": "log10"}
T_UNITS = {"K": "K", "°C": "degC"}
FIT_CHOICES = {
    "Let HTM decide: the authors' fit unless it is more than 10% away from the points": None,
    "Use the authors' fit": "author_fit",
    "Use HTM's fit of the points": "htm_refit",
}
CHANGE_KINDS = {"Change the values": "change", "Only flag it for a verifier": "flag"}
METHODS = list(typing.get_args(Method))
OTHER_MATERIAL = "other (describe it in the notes)"
EMPTY = ("", "_No response_", "None")

_UNSET = object()


class ContributionError(Exception):
    """Problems for the contributor (or a maintainer) to fix in the issue"""

    def __init__(self, problems, maintainer=False):
        self.problems = [problems] if isinstance(problems, str) else list(problems)
        self.maintainer = maintainer
        super().__init__("; ".join(self.problems))

    def markdown(self):
        lines = "\n".join(f"- {p}" for p in self.problems)
        if self.maintainer:
            return (
                "This needs a maintainer: the form cannot express it.\n\n"
                f"{lines}\n\nA maintainer will pick it up. You do not need to do anything."
            )
        return f"I could not turn this issue into a record yet:\n\n{lines}\n\nEdit the issue to fix it and I will try again."


@dataclass
class Contribution:
    kind: str  # "new" or "change"
    record_id: str
    title: str
    summary: str
    files: dict = field(default_factory=dict)  # path relative to the data folder -> text
    warnings: list = field(default_factory=list)

    def write(self, data_dir=build.DATA_DIR):
        for rel, text in self.files.items():
            path = Path(data_dir) / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)


# --- the issue forms -----------------------------------------------------------


def _attrs(label, description=None, placeholder=None):
    a = {"label": label}
    if description:
        a["description"] = description
    if placeholder:
        a["placeholder"] = placeholder
    return a


def _markdown(text):
    return {"type": "markdown", "attributes": {"value": text}}


def _input(id, label, description=None, placeholder=None, required=False):
    return {
        "type": "input",
        "id": id,
        "attributes": _attrs(label, description, placeholder),
        "validations": {"required": required},
    }


def _textarea(id, label, description=None, placeholder=None, render=None, required=False):
    item = {"type": "textarea", "id": id, "attributes": _attrs(label, description, placeholder)}
    if render:
        item["attributes"]["render"] = render
    item["validations"] = {"required": required}
    return item


def _dropdown(id, label, options, description=None, required=False, default=None):
    item = {"type": "dropdown", "id": id, "attributes": _attrs(label, description)}
    item["attributes"]["options"] = list(options)
    if default is not None:
        item["attributes"]["default"] = default
    item["validations"] = {"required": required}
    return item


def _value_fields():
    return [
        _markdown(
            "**Arrhenius law.** For an Arrhenius law, or for the authors' fit of their points:"
            " value = pre-exponential factor × exp(−E / k<sub>B</sub>T). Type the numbers and"
            " units exactly as printed: HTM converts them, and keeps what you typed."
        ),
        _input("pre_exp", "Pre-exponential factor", placeholder="4.1e-3"),
        _input(
            "pre_exp_unit",
            "Unit of the pre-exponential factor",
            "As printed, e.g. cm^2/s, mol/m^3/Pa^0.5, mol m^-1 s^-1 Pa^-0.5, m^4/s",
            "cm^2/s",
        ),
        _input("act_energy", "Activation energy", placeholder="0.39"),
        _input(
            "act_energy_unit",
            "Unit of the activation energy",
            "eV, kJ/mol, kcal/mol, or K when the paper gives E/k_B",
            "eV",
        ),
        _input("t_min", "Lowest temperature of the range", "Only if the paper gives it", "1100"),
        _input("t_max", "Highest temperature of the range", placeholder="2400"),
        _dropdown("t_unit", "Unit of the temperature range", T_UNITS),
        _markdown(
            "**Data points.** As read from a table or a figure (e.g. with"
            " [WebPlotDigitizer](https://automeris.io/WebPlotDigitizer)), before any conversion."
        ),
        _textarea(
            "points",
            "Data points",
            "Two columns, x then y, one row per point. Separate them with a comma, a semicolon, a tab or spaces.",
            "1.05, 3.2e-9\n1.10, 2.1e-9",
            render="csv",
        ),
        _dropdown("x_axis", "x column", X_AXES),
        _dropdown("y_scale", "y column", Y_SCALES),
        _input("y_unit", "Unit of y", "Unit of the value itself, also when the column is its logarithm", "m^2/s"),
        _input("digitised_from", "Points read from", placeholder="Fig. 5"),
        _dropdown(
            "fit_choice",
            "If the points and the authors' fit disagree",
            FIT_CHOICES,
            "Only for data points with the authors' fit",
        ),
        _input("fit_note", "Why that fit", "Needed if you chose a fit above", "the fit in Table 2 uses all the runs"),
    ]


def new_record_form(material_ids):
    """The issue form that adds a record"""
    return {
        "name": "New record",
        "description": "Add a property from a paper to HTM. A bot turns the issue into a pull request.",
        "title": "New record: ",
        "labels": ["new-record"],
        "body": [
            _markdown(
                "Thanks for adding to HTM! Fill in what the paper gives. A bot reads this issue,"
                " writes the record and opens a pull request with a plot of your record next to"
                " the ones already in HTM. If something is missing it says so here: edit the issue"
                " and it tries again."
            ),
            _input("doi", "DOI", "The paper the values come from", "10.1116/1.1492699", True),
            _input("location", "Where in the paper", "Table, equation or figure", "Table 2"),
            _dropdown("property", "Property", PROPERTIES, required=True),
            _dropdown(
                "law",
                "Law",
                LAWS,
                "Solubility and permeability scale with pressure^0.5 (Sieverts) or with pressure (Henry)",
                required=True,
            ),
            _dropdown("material", "Material", sorted(material_ids) + [OTHER_MATERIAL], required=True),
            _dropdown("isotope", "Isotope", ["H", "D", "T"], required=True),
            _dropdown("method", "Method", METHODS, required=True, default=METHODS.index("unknown")),
            _dropdown("form", "What the paper gives", FORMS, required=True),
            *_value_fields(),
            _input("sample_form", "Sample", placeholder="polycrystalline foil, 0.1 mm thick"),
            _input("sample_purity", "Purity", placeholder="99.95%"),
            _input("sample_surface", "Surface", placeholder="electropolished"),
            _textarea(
                "notes",
                "Notes",
                "Anything a verifier should know. If the material is not in the list, describe it here.",
            ),
            _input("orcid", "Your ORCID", "Optional, to credit you in the record", "0000-0002-1825-0097"),
            {
                "type": "checkboxes",
                "id": "checks",
                "attributes": {
                    "label": "Checks",
                    "options": [
                        {"label": "I typed the values and units as printed in the paper", "required": True},
                        {"label": "I checked that this record is not in HTM yet"},
                    ],
                },
            },
        ],
    }


def change_record_form():
    """The issue form that changes or flags a record"""
    return {
        "name": "Change a record",
        "description": "Correct a record, or flag it for a verifier. A bot turns the issue into a pull request.",
        "title": "Change: ",
        "labels": ["change-record"],
        "body": [
            _markdown(
                "Fill in only what is wrong: **an empty field keeps the current value**. Coming from the"
                " [explorer](https://remdelaportemathurin.github.io/h-transport-materials/), *Current values*"
                " shows what HTM holds now. A wrong material, isotope or property needs a new record: say so"
                " under *What is wrong* and choose *Only flag it*."
            ),
            _input("record", "Record", "The record id", "htm:W-D-H-frauenfelder1969", True),
            _dropdown("kind", "What to do", CHANGE_KINDS, required=True),
            _textarea(
                "current",
                "Current values",
                "For reference, as stored in the record. Editing this box changes nothing: use the fields below.",
                render="yaml",
            ),
            _textarea("reason", "What is wrong, and where in the paper", required=True),
            _input("location", "Where in the paper", "Table, equation or figure", "Table 2"),
            _dropdown("law", "Law", LAWS),
            _dropdown("method", "Method", METHODS),
            *_value_fields(),
            _input("orcid", "Your ORCID", "Optional, to credit you in the record", "0000-0002-1825-0097"),
        ],
    }


FORM_FILES = {"new-record.yml": "new", "change-record.yml": "change"}
_HEADER = (
    "# Generated by `htm contribute form` from h_transport_materials/records/contribute.py.\n"
    "# Edit that module, not this file: a test checks that the two agree.\n"
)


def form_yaml(kind, data_dir=build.DATA_DIR):
    form = new_record_form(_materials(data_dir)) if kind == "new" else change_record_form()
    return _HEADER + yaml.safe_dump(form, sort_keys=False, allow_unicode=True, width=1000)


# --- parsing the issue -------------------------------------------------------------


def parse_issue_body(body, form):
    """Field id -> text (None when empty) of an issue opened with an issue form.

    GitHub writes each field as ``### <label>`` followed by the answer.
    """
    if len(body.encode("utf-8")) > MAX_BODY:
        raise ContributionError("The issue is longer than 64 KB. Split the data points over several issues.")
    labels = {item["attributes"]["label"]: item["id"] for item in form["body"] if item.get("id")}
    parts = re.split(r"^###[ \t]+(.+?)[ \t]*$", body.replace("\r\n", "\n"), flags=re.M)
    fields = {}
    for label, text in zip(parts[1::2], parts[2::2]):
        fid = labels.get(label)
        if fid is not None and fid not in fields:
            fields[fid] = _clean(text)
    return fields


def render_issue_body(form, fields):
    """The issue body GitHub would write for these answers (for tests and previews)"""
    out = []
    for item in form["body"]:
        if not item.get("id"):
            continue
        value = fields.get(item["id"])
        if value is None:
            value = "_No response_"
        elif item["attributes"].get("render"):
            value = f"```{item['attributes']['render']}\n{value}\n```"
        out.append(f"### {item['attributes']['label']}\n\n{value}\n")
    return "\n".join(out)


def _clean(text):
    text = text.strip()
    fenced = re.fullmatch(r"```[\w-]*\n(.*?)\n?```", text, flags=re.S)
    if fenced:
        text = fenced.group(1).strip()
    return None if text in EMPTY else text


_SUPERSCRIPT_RUN = re.compile("[⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺]+(?:[·.][⁰¹²³⁴⁵⁶⁷⁸⁹]+)?")
_SUPERSCRIPTS = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺·", "0123456789-+.")


def _plain(text):
    """Typographic minus signs and superscripts as plain text: 10⁻³ -> 10^-3"""
    text = text.strip().translate(dict.fromkeys(map(ord, "−–‒"), "-"))
    return _SUPERSCRIPT_RUN.sub(lambda m: "^" + m.group(0).translate(_SUPERSCRIPTS), text)


def parse_number(text):
    """'4.1e-3', '4.1 × 10^-3', '4.1x10⁻³' or '4,1e-3' -> float (ValueError otherwise)"""
    s = re.sub(r"\s+", "", _plain(text))
    m = re.fullmatch(r"([-+]?\d*[.,]?\d+)(?:[x×·*]10\^?([-+]?\d+)|[eE]([-+]?\d+))?", s)
    if not m:
        raise ValueError(text)
    mantissa = m.group(1).replace(",", ".")
    exponent = m.group(2) or m.group(3)
    return float(f"{mantissa}e{exponent}" if exponent else mantissa)


def parse_unit(text):
    """A unit as typed -> (unit string pint reads, as printed or None). ValueError if unreadable"""
    printed = text.strip()
    s = _plain(printed).replace("·", "*").replace("⋅", "*").replace("°C", "degC").replace("ºC", "degC")
    s = re.sub(r"(?:cm\^?3|cc)\s*\(?STP\)?", "ccSTP", s, flags=re.I)
    s = re.sub(r"√\s*\(?Pa\)?", "Pa^0.5", s)
    s = re.sub(r"(?<=[A-Za-z\d])\.(?=[A-Za-z])", "*", s)  # m2.s-1
    s = re.sub(r"(?<=[A-Za-z])(-?\d+(?:[./]\d+)?)(?![\w.])", r"^\1", s)  # cm2, s-1, Pa0.5
    s = re.sub(r"\^\(?(-?)1/2\)?", lambda m: f"^{m.group(1)}0.5", s)
    units.unit(s)
    return s, (printed if printed != s else None)


def parse_points(text):
    """Rows of two numbers -> list of (x, y). Raises ContributionError"""
    rows, problems = [], []
    for n, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        cells = [c for c in re.split(r"[,;\t ]+", line) if c]
        try:
            if len(cells) != 2:
                raise ValueError
            rows.append(tuple(parse_number(c) for c in cells))
        except ValueError:
            if not rows and re.search(r"[A-DF-Za-df-z]", line):
                continue  # a header, e.g. "1000/T, log10 D" (letters other than e/E)
            problems.append(f"**Data points**, line {n}: expected two numbers, found `{line}`.")
    if problems:
        raise ContributionError(problems[:10])
    if len(rows) < 2:
        raise ContributionError("**Data points**: give at least two rows.")
    if len(rows) > MAX_POINTS:
        raise ContributionError(f"**Data points**: at most {MAX_POINTS} rows per record.")
    return rows


def points_csv(rows):
    # plain floats: numpy 2 scalars would write np.float64(...)
    return "".join(f"{float(x)!r},{float(y)!r}\n" for x, y in rows)


# --- shared helpers ----------------------------------------------------------------


def _materials(data_dir):
    out = {}
    for path in sorted((Path(data_dir) / "materials").glob("*.yaml")):
        with open(path, encoding="utf-8") as f:
            m = Material(**yaml.safe_load(f))
        out[m.id] = m
    return out


def _dump(content):
    return yaml.safe_dump(content, sort_keys=False, allow_unicode=True, width=100)


def _who(author, orcid):
    if orcid:
        m = re.search(r"(\d{4}-\d{4}-\d{4}-\d{3}[\dX])", orcid)
        if m:
            return f"https://orcid.org/{m.group(1)}"
    return f"github:{author}" if author else None


def _oneline(text):
    return re.sub(r"\s+", " ", text).strip()


class _Reader:
    """Reads form fields, collecting problems instead of stopping at the first"""

    def __init__(self, fields):
        self.fields = fields
        self.problems = []

    def text(self, fid, label, required=False):
        value = self.fields.get(fid)
        if value is None and required:
            self.problems.append(f"**{label}** is empty.")
        return value

    def choice(self, fid, label, options, required=False):
        """The mapped value of a dropdown, or _UNSET when not answered"""
        value = self.fields.get(fid)
        if value is None:
            if required:
                self.problems.append(f"**{label}**: choose one of the options.")
            return _UNSET
        if value not in options:
            self.problems.append(f"**{label}**: `{value}` is not one of the options.")
            return _UNSET
        return options[value] if isinstance(options, dict) else value

    def number(self, fid, label, required=False):
        text = self.text(fid, label, required)
        if text is None:
            return None
        try:
            return parse_number(text)
        except ValueError:
            self.problems.append(f"**{label}**: cannot read `{text}` as a number. Write it like 4.1e-3 or 4.1 × 10^-3.")
            return None

    def unit(self, fid, label, required=False):
        """(unit, as printed) or None"""
        text = self.text(fid, label, required)
        if text is None:
            return None
        try:
            return parse_unit(text)
        except ValueError:
            self.problems.append(
                f"**{label}**: cannot read the unit `{text}`. Write it like cm^2/s, mol/m^3/Pa^0.5 or kJ/mol."
            )
            return None

    def quantity(self, fid, label, required=False):
        """{value, unit[, unit_as_printed]} from the value and unit fields, or None"""
        value = self.number(fid, label, required)
        unit = self.unit(f"{fid}_unit", f"Unit of the {label.lower()}", required or value is not None)
        if value is None or unit is None:
            return None
        return _quantity(value, unit)

    def range(self):
        t_min, t_max = self.number("t_min", "Lowest temperature"), self.number("t_max", "Highest temperature")
        if t_min is None and t_max is None:
            return None
        if t_min is None or t_max is None:
            self.problems.append("**Temperature range**: give both the lowest and the highest temperature.")
            return None
        if not t_min < t_max:
            self.problems.append("**Temperature range**: the lowest temperature must be below the highest.")
            return None
        unit = self.choice("t_unit", "Unit of the temperature range", T_UNITS)
        return {"value": [t_min, t_max], "unit": "K" if unit is _UNSET else unit}

    def points(self):
        text = self.text("points", "Data points")
        if text is None:
            return None
        try:
            return parse_points(text)
        except ContributionError as e:
            self.problems.extend(e.problems)
            return None

    def axes(self):
        x = self.choice("x_axis", "x column", X_AXES)
        scale = self.choice("y_scale", "y column", Y_SCALES)
        y_unit = self.unit("y_unit", "Unit of y", required=True)
        x = X_AXES["T (K)"] if x is _UNSET else x
        y = {"column": 1, "quantity": "value", "unit": y_unit[0] if y_unit else "?"}
        if scale not in (_UNSET, "linear"):
            y["scale"] = scale
        return {"column": 0, **x}, y

    def check(self):
        if self.problems:
            raise ContributionError(self.problems)


def _quantity(value, unit):
    q = {"value": value, "unit": unit[0]}
    if unit[1]:
        q["unit_as_printed"] = unit[1]
    return q


def _validate(record):
    try:
        Record(**record)
    except ValidationError as e:
        raise ContributionError(
            [f"`{'.'.join(map(str, err['loc'])) or 'record'}`: {err['msg']}" for err in e.errors()]
        ) from e


def _check_build(data_dir, files):
    """Builds a copy of the data folder with the contribution in it"""
    with tempfile.TemporaryDirectory() as tmp:
        copy_dir = Path(tmp) / "data"
        shutil.copytree(data_dir, copy_dir)
        Contribution("", "", "", "", files).write(copy_dir)
        try:
            return build.build(copy_dir)
        except build.BuildError as e:
            message = str(e)
            if "author fit and the data points disagree" in message:
                message = (
                    message.split(". Set reported.selected")[0]
                    + ". Say which to use under **If the points and the authors' fit disagree**,"
                    " and why under **Why that fit**."
                )
            raise ContributionError(message) from e


def _fmt(q, printed=False):
    if q is None:
        return "not given"
    unit = (printed and q.get("unit_as_printed")) or q["unit"]
    if isinstance(q.get("value"), list):
        return f"{q['value'][0]:g} to {q['value'][1]:g} {unit}"
    return f"{q['value']:.4g} {unit}"


def _normalized_rows(built):
    n = built["normalized"]
    rows = []
    if "pre_exp" in n:
        rows += [("Pre-exponential factor", _fmt(n["pre_exp"])), ("Activation energy", f"{n['act_energy']['value']:.4g} eV")]
    if n.get("range"):
        rows.append(("Range", _fmt(n["range"])))
    if "points" in n:
        fit = {"author_fit": "the authors' fit", "htm_refit": "HTM's fit of the points"}[n["selected"]]
        rows.append(("Data points", f"{len(n['points']['T']['value'])}, law from {fit}"))
    if "fit_discrepancy" in n:
        rows.append(("Fits differ by", f"{n['fit_discrepancy']['max_relative']:.1%} at most"))
    return rows


def _table(rows, header=("", "")):
    out = [f"| {header[0]} | {header[1]} |", "| --- | --- |"]
    out += [f"| {a} | {b} |" for a, b in rows]
    return "\n".join(out)


NEXT_STEPS = (
    "**What happens next.** The record report on the pull request plots this record next to"
    " the others. A maintainer reviews and merges it. The record stays a *draft* until"
    " someone checks it against the paper."
)


# --- a new record ------------------------------------------------------------------


def new_record(fields, data_dir=build.DATA_DIR, author=None, issue=None, fetch=sources.fetch_csl):
    """Builds the files of a new record from the fields of a new-record issue

    Returns:
        Contribution
    """
    data_dir = Path(data_dir)
    materials = _materials(data_dir)
    r = _Reader(fields)

    doi = r.text("doi", "DOI", required=True)
    if doi is not None and not re.fullmatch(r"10\.\d{4,9}/\S+", strip_doi(doi)):
        r.problems.append(f"**DOI**: `{doi}` does not look like a DOI (10.xxxx/...).")
        doi = None
    prop = r.choice("property", "Property", PROPERTIES, required=True)
    law = r.choice("law", "Law", LAWS, required=True)
    if prop in ("solubility", "permeability") and law is None:
        r.problems.append(f"**Law**: a {prop} follows Sieverts' or Henry's law.")
    if prop not in (_UNSET, "solubility", "permeability") and law not in (_UNSET, None):
        r.problems.append(f"**Law**: choose *Not applicable* for a {prop}.")
    material = r.text("material", "Material", required=True)
    isotope = r.choice("isotope", "Isotope", ["H", "D", "T"], required=True)
    method = r.choice("method", "Method", METHODS)
    form = r.choice("form", "What the paper gives", FORMS, required=True)

    if material == OTHER_MATERIAL:
        raise ContributionError(
            "The material is not in HTM yet. A maintainer adds it to `data/materials`"
            " (composition, density), then edits this issue to pick it.",
            maintainer=True,
        )
    if material is not None and material not in materials:
        close = difflib.get_close_matches(material, list(materials), n=3)
        r.problems.append(
            f"**Material**: `{material}` is not in HTM." + (f" Did you mean {', '.join(close)}?" if close else "")
        )

    reported, csv_text = None, None
    if form == "arrhenius":
        pre_exp = r.quantity("pre_exp", "Pre-exponential factor", required=True)
        act_energy = r.quantity("act_energy", "Activation energy", required=True)
        reported = {"form": "arrhenius", "pre_exp": pre_exp, "act_energy": act_energy}
        T_range = r.range()
        if T_range:
            reported["range"] = T_range
    elif form in ("points", "points_and_fit"):
        rows = r.points()
        if rows is None and "points" not in fields:
            r.problems.append("**Data points** is empty.")
        x, y = r.axes()
        csv_text = points_csv(rows) if rows else None
        reported = {"form": "points", "file": None, "x": x, "y": y}
        digitised = r.text("digitised_from", "Points read from")
        if digitised:
            reported["digitised_from"] = digitised
        if form == "points_and_fit":
            fit = {
                "form": "arrhenius",
                "pre_exp": r.quantity("pre_exp", "Pre-exponential factor", required=True),
                "act_energy": r.quantity("act_energy", "Activation energy", required=True),
            }
            T_range = r.range()
            if T_range:
                fit["range"] = T_range
            reported["author_fit"] = fit
            choice = r.choice("fit_choice", "If the points and the authors' fit disagree", FIT_CHOICES)
            if choice not in (_UNSET, None):
                reported["selected"] = choice
                reported["selection_note"] = r.text("fit_note", "Why that fit", required=True)
    r.check()

    try:
        source, fetched = sources.find_or_fetch(doi, data_dir / "sources", fetch=fetch)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise ContributionError(f"**DOI**: doi.org does not know `{doi}`. Check it for typos.") from e
        raise
    except ValueError as e:
        raise ContributionError(f"The metadata of `{doi}` cannot make a source file: {e}", maintainer=True) from e

    mat = materials[material]
    base = f"htm:{mat.code}-{PROPERTY_CODES[prop]}-{isotope}-{source.key}"
    taken = {"htm:" + p.stem for p in (data_dir / "records").glob("*.yaml")}
    record_id, suffix = base, ord("b")
    while record_id in taken:
        record_id, suffix = f"{base}-{chr(suffix)}", suffix + 1
    stem = record_id.removeprefix("htm:")

    record = {"id": record_id, "property": prop}
    if law:
        record["law"] = law
    record.update(material=material, isotope=isotope, method="unknown" if method is _UNSET else method)
    sample = {k: fields.get(f"sample_{k}") for k in ("form", "purity", "surface") if fields.get(f"sample_{k}")}
    if sample:
        record["sample"] = sample
    record["source"] = {"doi": strip_doi(doi)}
    location = fields.get("location")
    if location:
        record["source"]["location"] = location
    if reported["form"] == "points":
        reported["file"] = f"{stem}.csv"
    record["reported"] = reported
    if fields.get("notes"):
        record["note"] = fields["notes"]
    flags = [f"submitted through issue #{issue}: check the values, units and location against the paper"]
    if not location:
        flags.append("the location in the paper (table, equation or figure) is not given")
    who = _who(author, fields.get("orcid"))
    record["curation"] = {"status": "draft", "contributed_by": [who] if who else [], "flags": flags}
    _validate(record)

    files = {f"records/{stem}.yaml": _dump(record)}
    if csv_text:
        files[f"records/{stem}.csv"] = csv_text
    if fetched:
        files[f"sources/{source.key}.yaml"] = sources.source_yaml(source)
    db = _check_build(data_dir, files)
    built = next(rec for rec in db["records"] if rec["id"] == record_id)

    warnings = []
    same = [
        rec["id"]
        for rec in db["records"]
        if rec["id"] != record_id
        and rec["id"].startswith(f"htm:{mat.code}-{PROPERTY_CODES[prop]}-{isotope}-{source.key}")
    ]
    if same:
        warnings.append(
            f"HTM already has {', '.join(f'`{i}`' for i in same)} from this paper for this property,"
            " material and isotope. If it is the same value, close this issue."
        )
    if reported["form"] == "arrhenius" and "range" not in reported:
        warnings.append("No temperature range: the record cannot say where the law is valid.")
    if not location:
        warnings.append("Where in the paper is empty: a verifier will need to find the values.")

    authors = source.authors or source.editors
    first = authors[0].family + (" et al." if len(authors) > 1 else "")
    src = f"{first} ({source.year}), *{source.title}*" + (f", {source.journal}" if source.journal else "")
    src += f", [doi:{source.doi}](https://doi.org/{source.doi})" if source.doi else ""
    fit = reported.get("author_fit", {})
    typed = [
        ("Pre-exponential factor", _fmt(reported.get("pre_exp") or fit.get("pre_exp"), printed=True)),
        ("Activation energy", _fmt(reported.get("act_energy") or fit.get("act_energy"), printed=True)),
    ]
    rng = reported.get("range") or reported.get("author_fit", {}).get("range")
    typed.append(("Range", _fmt(rng)))
    if csv_text:
        typed.append(("Data points", f"{len(csv_text.splitlines())} in `{stem}.csv`"))
    summary = "\n\n".join(
        [
            f"**New record** `{record_id}`: {prop.replace('_', ' ')} of {isotope} in {material}.",
            f"**Source**: {src}" + (" (new source file, from doi.org: check the title and authors)" if fetched else ""),
            "**As typed**\n\n" + _table([r_ for r_ in typed if r_[1] != "not given" or r_[0] == "Range"]),
            "**Normalised by HTM**\n\n" + _table(_normalized_rows(built)),
        ]
        + (["**Warnings**\n\n" + "\n".join(f"- {w}" for w in warnings)] if warnings else [])
        + [NEXT_STEPS]
    )
    title = f"Add {record_id}" + (f" (issue #{issue})" if issue else "")
    return Contribution("new", record_id, title, summary, files, warnings)


# --- a change to a record ---------------------------------------------------------------


def _axis_label(axis):
    for label, spec in X_AXES.items():
        if (
            axis.get("quantity") == spec["quantity"]
            and float(axis.get("factor", 1.0)) == spec["factor"]
            and axis.get("scale", "linear") == "linear"
            and _same_unit(axis.get("unit"), spec["unit"])
        ):
            return label
    return None


def _same_unit(a, b):
    try:
        return a is not None and units.unit(a) == units.unit(b)
    except ValueError:
        return False


def _law_block(rep):
    """The Arrhenius law the form edits: the reported law, or the authors' fit of points"""
    if rep["form"] == "arrhenius":
        return rep
    if rep["form"] == "points" and (rep.get("author_fit") or {}).get("form", "arrhenius") == "arrhenius":
        return rep.get("author_fit")
    return None


def prefill_new(rec):
    """Field id -> text prefilling the new-record form from a record (same paper, same material)"""
    out = {
        "doi": rec["source"].get("doi"),
        "property": _label(PROPERTIES, rec["property"]),
        "law": _label(LAWS, rec.get("law")),
        "material": rec["material"],
        "isotope": rec["isotope"],
        "method": rec.get("method"),
    }
    return {k: v for k, v in out.items() if v is not None}


def prefill_change(rec):
    """Field id -> text prefilling the change-record form: the record id and, for
    reference, its current values.

    The value fields are left empty (empty keeps the current value): GitHub's
    form kept reverting edits to fields prefilled through the URL.
    """
    current = {"location": rec["source"].get("location"), "method": rec.get("method")}
    if rec.get("law"):
        current["law"] = rec["law"]
    current["reported"] = rec["reported"]

    def drop_empty(node):
        if isinstance(node, dict):
            return {k: drop_empty(v) for k, v in node.items() if v is not None}
        return node

    return {
        "record": rec["id"],
        "kind": "Change the values",
        "current": yaml.safe_dump(drop_empty(current), sort_keys=False, allow_unicode=True, width=100).strip(),
    }


def _label(options, value):
    return next((label for label, v in options.items() if v == value), None)


def _changed_quantity(r, block, key, label, changes):
    """Updates block[key] from the value and unit fields, if they differ"""
    old = block.get(key)
    value = r.number(key, label)
    unit_text = r.text(f"{key}_unit", f"Unit of the {label.lower()}")
    if value is None and unit_text is None:
        return
    if old is None and (value is None or unit_text is None):
        r.problems.append(f"**{label}**: give the value and its unit.")
        return
    new = dict(old or {})
    if value is not None:
        new["value"] = value
    if unit_text is not None and not (old and unit_text.strip() in (old["unit"], old.get("unit_as_printed"))):
        unit = r.unit(f"{key}_unit", f"Unit of the {label.lower()}")
        if unit is None:
            return
        new.pop("unit_as_printed", None)
        new.update(_quantity(new.get("value"), unit))
    if new != old:
        block[key] = new
        changes.append((label, _fmt(old), _fmt(new)))


def change_record(fields, data_dir=build.DATA_DIR, author=None, issue=None):
    """Builds the files of a change to a record from the fields of a change-record issue

    Returns:
        Contribution
    """
    data_dir = Path(data_dir)
    r = _Reader(fields)
    record_id = (r.text("record", "Record", required=True) or "").strip("` ")
    record_id = record_id if record_id.startswith("htm:") else "htm:" + record_id
    stem = record_id.removeprefix("htm:")
    path = data_dir / "records" / f"{stem}.yaml"
    if not path.exists():
        stems = [p.stem for p in (data_dir / "records").glob("*.yaml")]
        close = difflib.get_close_matches(stem, stems, n=3)
        raise ContributionError(
            f"**Record**: there is no record `{record_id}`."
            + (f" Did you mean {', '.join(f'`htm:{c}`' for c in close)}?" if close else "")
        )
    kind = r.choice("kind", "What to do", CHANGE_KINDS, required=True)
    reason = r.text("reason", "What is wrong, and where in the paper", required=True)
    r.check()

    with open(path, encoding="utf-8") as f:
        content = yaml.safe_load(f)
    before = copy.deepcopy(content)
    curation = content.setdefault("curation", {})
    flags = curation.setdefault("flags", [])
    changes, files, values_changed = [], {}, False

    if kind == "flag":
        flags.append(f"issue #{issue}: {_oneline(reason)}")
    else:
        source = content["source"]
        location = r.text("location", "Where in the paper")
        if location is not None and location != source.get("location"):
            changes.append(("Where in the paper", source.get("location") or "not given", location))
            source["location"] = location
        method = r.choice("method", "Method", METHODS)
        if method is not _UNSET and method != content.get("method"):
            changes.append(("Method", content.get("method"), method))
            content["method"] = method
        law = r.choice("law", "Law", LAWS)
        if content["property"] in ("solubility", "permeability") and law not in (_UNSET, None, content.get("law")):
            changes.append(("Law", content.get("law"), law))
            content["law"] = law
            values_changed = True

        rep = content["reported"]
        n_before = len(changes)
        converted = False
        if rep["form"] != "points" and fields.get("points"):
            if rep["form"] != "arrhenius" or content.get("transformations") or any(
                rep.get(k) for k in ("pre_exp_uncertainty", "act_energy_uncertainty")
            ):
                raise ContributionError(
                    f"`{record_id}` cannot take data points from the form: it is a `{rep['form']}` record, or it"
                    " has transformations or uncertainties that must be told whether they apply to the points"
                    f" or to the fit. The change asked for: {_oneline(reason)}",
                    maintainer=True,
                )
            # the printed law becomes the authors' fit of the new points
            rows = r.points()
            x, y = r.axes()
            r.check()
            fit = {"form": "arrhenius", "pre_exp": rep["pre_exp"], "act_energy": rep["act_energy"]}
            if rep.get("range"):
                fit["range"] = rep["range"]
            rep = content["reported"] = {"form": "points", "file": f"{stem}.csv", "x": x, "y": y}
            digitised = r.text("digitised_from", "Points read from")
            if digitised:
                rep["digitised_from"] = digitised
            rep["author_fit"] = fit
            files[f"records/{stem}.csv"] = points_csv(rows)
            changes.append(("Data points", "none", f"{len(rows)} rows; the printed law becomes the authors' fit"))
            converted = True
        arrhenius_given = any(fields.get(k) for k in ("pre_exp", "act_energy", "t_min", "t_max"))
        block = _law_block(rep)
        if block is None and rep["form"] == "points" and "author_fit" not in rep and arrhenius_given:
            block = rep["author_fit"] = {"form": "arrhenius"}  # the paper also gives a fit
        if block is None and (arrhenius_given or (rep["form"] != "points" and fields.get("points"))):
            law_form = rep.get("author_fit", rep)["form"]
            raise ContributionError(
                f"`{record_id}` holds a `{law_form}` law, which the form cannot edit."
                f" The change asked for: {_oneline(reason)}",
                maintainer=True,
            )
        if block is not None:
            _changed_quantity(r, block, "pre_exp", "Pre-exponential factor", changes)
            _changed_quantity(r, block, "act_energy", "Activation energy", changes)
            T_range = r.range()
            if T_range is not None and T_range != block.get("range"):
                changes.append(("Range", _fmt(block.get("range")), _fmt(T_range)))
                block["range"] = T_range
                kept = [t for t in content.get("transformations", []) if t["op"] != "assume_range"]
                if len(kept) != len(content.get("transformations", [])):
                    content["transformations"] = kept
                    changes.append(("HTM's assumed range", "used", "removed: the paper gives a range"))
        if rep["form"] == "points":
            rows = None if converted else r.points()
            if rows is not None:
                files[f"records/{rep['file']}"] = points_csv(rows)
                old_rows = (path.parent / rep["file"]).read_text(encoding="utf-8").strip().splitlines()
                changes.append(("Data points", f"{len(old_rows)} rows", f"{len(rows)} rows, replaced"))
            x = r.choice("x_axis", "x column", X_AXES)
            if x is not _UNSET and x != {k: rep["x"].get(k, 1.0) for k in ("quantity", "unit", "factor")}:
                new_x = {"column": rep["x"].get("column", 0), **x}
                changes.append(("x column", _axis_label(rep["x"]) or str(rep["x"]), _label(X_AXES, x)))
                rep["x"] = new_x
            scale = r.choice("y_scale", "y column", Y_SCALES)
            if scale is not _UNSET and scale != rep["y"].get("scale", "linear"):
                changes.append(("y column", rep["y"].get("scale", "linear"), scale))
                rep["y"]["scale"] = scale
            y_unit = r.text("y_unit", "Unit of y")
            if y_unit is not None and y_unit != rep["y"]["unit"]:
                unit = r.unit("y_unit", "Unit of y")
                if unit:
                    changes.append(("Unit of y", rep["y"]["unit"], unit[0]))
                    rep["y"]["unit"] = unit[0]
            choice = r.choice("fit_choice", "If the points and the authors' fit disagree", FIT_CHOICES)
            if choice is not _UNSET and choice != rep.get("selected"):
                changes.append(("Fit used", rep.get("selected") or "HTM decides", choice or "HTM decides"))
                if choice is None:
                    rep.pop("selected", None)
                    rep.pop("selection_note", None)
                else:
                    rep["selected"] = choice
                    rep["selection_note"] = r.text("fit_note", "Why that fit", required=True)
        values_changed = values_changed or len(changes) > n_before
        r.check()
        if not changes:
            raise ContributionError(
                "Nothing differs from the record. Change at least one field, or choose *Only flag it for a verifier*."
            )
        if curation.get("status") == "verified" and values_changed:
            curation["status"] = "draft"
            flags.append(f"values changed through issue #{issue} after verification: verify again")
        flags.append(f"changed through issue #{issue} ({_oneline(reason)}): check against the paper")

    who = _who(author, fields.get("orcid"))
    if who and who not in curation.setdefault("contributed_by", []):
        curation["contributed_by"].append(who)
    if content == before:
        raise ContributionError("Nothing to change in the record.")
    _validate(content)
    files[f"records/{stem}.yaml"] = _dump(content)
    db = _check_build(data_dir, files)
    built = next(rec for rec in db["records"] if rec["id"] == record_id)

    parts = [f"**{'Flag on' if kind == 'flag' else 'Change to'}** `{record_id}`.", f"**Reason**: {_oneline(reason)}"]
    if changes:
        parts.append(
            "\n".join(["| Field | Before | After |", "| --- | --- | --- |"] + [f"| {a} | {b} | {c} |" for a, b, c in changes])
        )
        parts.append("**Normalised by HTM, after the change**\n\n" + _table(_normalized_rows(built)))
    if values_changed and content["curation"].get("migrated_from"):
        parts.append(
            "This record came from the legacy database, so the equivalence test in"
            " `tests/test_records.py` will fail until a maintainer lists it in"
            " `EXPECTED_DIFFERENCES` with the reason and the size of the change."
        )
    parts.append(
        "The record report on the pull request gives the change in the normalised values."
        " A maintainer reviews and merges it."
    )
    verb = "Flag" if kind == "flag" else "Change"
    title = f"{verb} {record_id}" + (f" (issue #{issue})" if issue else "")
    return Contribution("change", record_id, title, "\n\n".join(parts), files)


# --- from an issue, for the workflow --------------------------------------------------------


def from_issue(issue, data_dir=build.DATA_DIR, dry_run=False, fetch=sources.fetch_csl):
    """Handles one issue (as returned by the GitHub REST API)

    Returns:
        dict: the result the workflow acts on: ``ok``, and either ``title``,
            ``record_id``, ``files``, ``pr_body`` and ``comment``, or
            ``maintainer`` and ``comment`` explaining what to fix
    """
    labels = {label["name"] for label in issue.get("labels", [])}
    kind = "change" if "change-record" in labels else "new"
    author = (issue.get("user") or {}).get("login")
    number = issue.get("number")
    try:
        if kind == "new":
            form = new_record_form(_materials(data_dir))
            fields = parse_issue_body(issue.get("body") or "", form)
            c = new_record(fields, data_dir, author=author, issue=number, fetch=fetch)
        else:
            fields = parse_issue_body(issue.get("body") or "", change_record_form())
            c = change_record(fields, data_dir, author=author, issue=number)
    except ContributionError as e:
        return {"ok": False, "kind": kind, "maintainer": e.maintainer, "comment": f"{MARKER}\n{e.markdown()}"}
    if not dry_run:
        c.write(data_dir)
    return {
        "ok": True,
        "kind": kind,
        "record_id": c.record_id,
        "title": c.title,
        "files": [str(Path("data") / rel).replace("\\", "/") for rel in c.files],
        "pr_body": "\n\n".join(
            [c.summary, _yaml_details(c.files), f"Closes #{number}.", f"Opened by the contribution bot from issue #{number}."]
        ),
        "comment": f"{MARKER}\nThanks! I turned this issue into a pull request: PR_URL\n\n{c.summary}",
    }


def _yaml_details(files):
    yamls = [(rel, text) for rel, text in files.items() if rel.startswith("records/") and rel.endswith(".yaml")]
    return "\n\n".join(
        f"<details><summary><code>data/{rel}</code></summary>\n\n```yaml\n{text}```\n\n</details>" for rel, text in yamls
    )


def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(prog="htm contribute", description="the contribution bot")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("from-issue", help="turn an issue (REST API JSON) into record files")
    p.add_argument("issue", type=Path, help="issue JSON, e.g. from `gh api repos/OWNER/REPO/issues/N`")
    p.add_argument("--result", type=Path, help="where to write the result JSON for the workflow")
    p.add_argument("--data", type=Path, default=build.DATA_DIR)
    p.add_argument("--dry-run", action="store_true", help="check only, write no record file")
    f = sub.add_parser("form", help="write the issue forms")
    f.add_argument("--out", type=Path, default=Path(".github/ISSUE_TEMPLATE"))
    f.add_argument("--data", type=Path, default=build.DATA_DIR)
    args = parser.parse_args(argv)

    if args.command == "form":
        for name, kind in FORM_FILES.items():
            with open(args.out / name, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(form_yaml(kind, args.data))
            print(f"wrote {args.out / name}")
        return
    with open(args.issue, encoding="utf-8") as fh:
        issue = json.load(fh)
    result = from_issue(issue, args.data, dry_run=args.dry_run)
    if args.result:
        with open(args.result, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=1, ensure_ascii=False)
    print(result["comment"].removeprefix(MARKER).strip())
    if result["ok"] and not args.dry_run:
        print("\nfiles:", *result["files"], sep="\n  ")
