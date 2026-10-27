"""Migrates the Python property_database to YAML records (a one-off tool).

1. ``capture()`` imports the database in a subprocess with the property
   constructors wrapped, and returns where each property was created
   (file, line) with its final attributes and position in htm.database.
2. ``classify()`` reads the constructor call in the source. Calls made only
   of numbers and units are converted automatically (the values come from
   the source text, as typed, not from pint's converted quantities);
   anything else (variables, helper functions, data files) is listed for
   hand transcription with the reason.
"""

import ast
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

CLASSES = ["Diffusivity", "Solubility", "Permeability", "RecombinationCoeff", "DissociationCoeff"]

_CAPTURE = r"""
import importlib.abc, importlib.util, json, sys

CLASSES = %(classes)r
calls = []


class Hook(importlib.abc.MetaPathFinder):
    def find_spec(self, name, path, target=None):
        if name != "h_transport_materials.property":
            return None
        sys.meta_path.remove(self)
        spec = importlib.util.find_spec(name)
        exec_module = spec.loader.exec_module

        def patched(module):
            exec_module(module)
            for cls_name in CLASSES:
                cls = getattr(module, cls_name)
                original = cls.__init__

                def init(self, *args, __original=original, __cls=cls_name, **kwargs):
                    if not getattr(self, "_captured", False):
                        self._captured = True
                        frame = sys._getframe(1)
                        calls.append((self, __cls, frame.f_code.co_filename, frame.f_lineno))
                    __original(self, *args, **kwargs)

                cls.__init__ = init

        spec.loader.exec_module = patched
        return spec


sys.meta_path.insert(0, Hook())
import h_transport_materials as htm

index = {id(p): i for i, p in enumerate(htm.database)}
out = []
for prop, cls, filename, lineno in calls:
    law = getattr(prop, "law", None)
    out.append(dict(
        cls=cls, file=filename, line=lineno, index=index.get(id(prop)),
        material=getattr(prop.material, "name", str(prop.material)),
        isotope=prop.isotope, source=prop.source, note=prop.note, law=law,
        doi=prop.doi,
    ))
print(json.dumps(out))
"""


def capture():
    """Imports the database with the constructors wrapped.

    Returns:
        list: one dict per constructor call (cls, file, line, index in
            htm.database, material, isotope, source, note, law, doi)
    """
    result = subprocess.run(
        [sys.executable, "-W", "ignore", "-c", _CAPTURE % {"classes": CLASSES}],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout.splitlines()[-1])


_trees = {}


def call_node(call):
    """The ast.Call node of a captured constructor call"""
    path = call["file"]
    if path not in _trees:
        source = Path(path).read_text(encoding="utf-8")
        _trees[path] = (source, ast.parse(source))
    source, tree = _trees[path]
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and _name(node.func) == call["cls"]
            and node.lineno <= call["line"] <= node.end_lineno
        ):
            return node, source
    raise LookupError(f"no {call['cls']} call at {path}:{call['line']}")


def _name(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


UNIT_MODULES = {"u", "ureg"}


def _is_unit(node):
    """u.cm, htm.ureg.cm"""
    if not isinstance(node, ast.Attribute):
        return False
    base = node.value
    if isinstance(base, ast.Name):
        return base.id in UNIT_MODULES
    return isinstance(base, ast.Attribute) and base.attr == "ureg"


def _is_k_B(node):
    return (isinstance(node, ast.Name) and node.id == "k_B") or (
        isinstance(node, ast.Attribute) and node.attr == "k_B"
    )


def _is_number(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return True
    return (
        isinstance(node, ast.UnaryOp)
        and isinstance(node.op, ast.USub)
        and _is_number(node.operand)
    )


def _is_np_exp(node):
    return (
        isinstance(node, ast.Call)
        and _name(node.func) == "exp"
        and len(node.args) == 1
        and _is_number(node.args[0])
    )


def _factors(node):
    """Flattens a product a * b / c into [(factor, +1|-1), ...]"""
    if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Mult, ast.Div)):
        left = _factors(node.left)
        right = _factors(node.right)
        if left is None or right is None:
            return None
        sign = 1 if isinstance(node.op, ast.Mult) else -1
        return left + [(f, s * sign) for f, s in right]
    return [(node, 1)]


def _unit_factor(node):
    """u.cm, u.cm**2, u.Pa**-0.5"""
    if _is_unit(node):
        return True
    return (
        isinstance(node, ast.BinOp)
        and isinstance(node.op, ast.Pow)
        and _is_unit(node.left)
        and _is_number(node.right)
    )


def literal_quantity(node):
    """Describes a quantity typed as numbers and units.

    Returns:
        dict or None: {"kind": "plain" | "exp" | "k_B", "number": node,
            "units": [(node, sign)]}; None if it is not a literal quantity
    """
    if isinstance(node, ast.Call) and _name(node.func) == "Quantity":
        if len(node.args) == 2 and _is_number(node.args[0]) and _unit_factor(node.args[1]):
            return {"kind": "plain", "number": node.args[0], "units": [(node.args[1], 1)]}
        return None
    factors = _factors(node)
    if factors is None:
        return None
    numbers = [(f, s) for f, s in factors if _is_number(f) or _is_np_exp(f)]
    k_B = [(f, s) for f, s in factors if _is_k_B(f)]
    units = [(f, s) for f, s in factors if _unit_factor(f)]
    if len(numbers) + len(k_B) + len(units) != len(factors):
        return None  # a variable, a function call, ...
    if len(numbers) != 1 or numbers[0][1] != 1 or len(k_B) > 1:
        return None  # arithmetic on numbers (e.g. 7e-7 / 2**0.5) is computed
    number = numbers[0][0]
    if k_B:
        if _is_np_exp(number) or k_B[0][1] != 1:
            return None
        kind = "k_B"
    else:
        kind = "exp" if _is_np_exp(number) else "plain"
    return {"kind": kind, "number": number, "units": units}


ARRHENIUS_ARGS = {
    "Diffusivity": ("D_0", "E_D"),
    "Solubility": ("S_0", "E_S"),
    "Permeability": ("pre_exp", "act_energy"),
    "RecombinationCoeff": ("pre_exp", "act_energy"),
    "DissociationCoeff": ("pre_exp", "act_energy"),
}
OTHER_ARGS = {"range", "source", "isotope", "note", "law", "author", "year", "material"}


def call_kwargs(call):
    """Keyword arguments of the call, positional ones mapped to their names"""
    node, _ = call_node(call)
    kwargs = {k.arg: k.value for k in node.keywords}
    for name, value in zip(ARRHENIUS_ARGS[call["cls"]], node.args):
        kwargs[name] = value
    if len(node.args) > 2:
        kwargs[None] = node.args[2]  # unexpected
    return kwargs


def _range_values(node):
    """[(number node, unit node), (number node, unit node)] or None

    Accepts (a * u.K, b * u.K), (u.Quantity(a, u.degC), ...) and (a, b) * u.K
    """
    if (
        isinstance(node, ast.BinOp)
        and isinstance(node.op, ast.Mult)
        and isinstance(node.left, ast.Tuple)
        and len(node.left.elts) == 2
        and all(_is_number(e) for e in node.left.elts)
        and _is_unit(node.right)
    ):
        return [(e, node.right) for e in node.left.elts]
    if not (isinstance(node, ast.Tuple) and len(node.elts) == 2):
        return None
    out = []
    for e in node.elts:
        q = literal_quantity(e)
        if q is None or q["kind"] != "plain" or len(q["units"]) != 1 or q["units"][0][1] != 1:
            return None
        out.append((q["number"], q["units"][0][0]))
    return out


class Unsupported(Exception):
    pass


def _is_data_ref(node):
    """data, data[:, 0], data["H"]["x"][:4]: a reference to loaded data, no arithmetic"""
    if isinstance(node, ast.Name):
        return True
    if not isinstance(node, ast.Subscript) or not _is_data_ref(node.value):
        return False
    parts = node.slice.elts if isinstance(node.slice, ast.Tuple) else [node.slice]
    for p in parts:
        if isinstance(p, ast.Slice):
            if not all(b is None or _is_number(b) for b in (p.lower, p.upper, p.step)):
                return False
        elif not (_is_number(p) or (isinstance(p, ast.Constant) and isinstance(p.value, str))):
            return False
    return True


def _is_number_list(node):
    """[1, 2, 3] or np.array([1, 2, 3])"""
    if isinstance(node, ast.Call) and _name(node.func) == "array" and len(node.args) == 1:
        node = node.args[0]
    return isinstance(node, ast.List) and all(_is_number(e) for e in node.elts)


def _column(node):
    """The data factor of an axis: ("ln" | "linear", values node)"""
    if _is_np_exp_of_data(node):
        return "ln", node.args[0]
    if _is_data_ref(node) or _is_number_list(node):
        return "linear", node
    return None


def _is_np_exp_of_data(node):
    return (
        isinstance(node, ast.Call)
        and _name(node.func) == "exp"
        and len(node.args) == 1
        and (_is_data_ref(node.args[0]) or _is_number_list(node.args[0]))
    )


def _axis_parts(node):
    """Splits an axis expression into (column, numbers, units)

    Returns:
        tuple: ((scale, values node, sign), [(number node, sign)], [(unit node, sign)])
    """
    if isinstance(node, ast.Call) and _name(node.func) == "Quantity" and len(node.args) == 2:
        column = _column(node.args[0])
        if column is None or not _unit_factor(node.args[1]):
            raise Unsupported("values not read from data")
        return (*column, 1), [], [(node.args[1], 1)]
    if isinstance(node, ast.Name):
        raise Unsupported(f"values computed in the module ({node.id})")
    factors = _factors(node)
    if factors is None:
        raise Unsupported("values not read from data")
    columns, numbers, units = [], [], []
    for f, sign in factors:
        if _unit_factor(f):
            units.append((f, sign))
        elif _is_number(f):
            numbers.append((f, sign))
        elif _column(f) is not None:
            columns.append((*_column(f), sign))
        else:
            raise Unsupported(f"computed values: {ast.unparse(f)[:40]}")
    if len(columns) != 1:
        raise Unsupported("values not read from a single data column")
    return columns[0], numbers, units


def _net_unit(units):
    """Unit string of a list of unit factors, with each factor's sign applied"""
    return _unit_string(units)


def points_axes(call):
    """Axis descriptions and value nodes of a data point call.

    Returns:
        tuple: (x axis dict, x values node, y axis dict, y values node)

    Raises:
        Unsupported: with the reason, if the call does not fit the patterns
    """
    import h_transport_materials as htm

    kwargs = call_kwargs(call)
    if "data_T" not in kwargs or "data_y" not in kwargs:
        raise Unsupported("data_T or data_y missing")
    (scale_T, values_T, sign_T), numbers_T, units_T = _axis_parts(kwargs["data_T"])
    (scale_y, values_y, sign_y), numbers_y, units_y = _axis_parts(kwargs["data_y"])
    if scale_T != "linear" or sign_y != 1 or numbers_y:
        raise Unsupported("unusual axis")

    factor = 1.0
    for n, sign in numbers_T:
        factor *= _number(n) ** sign
    unit_T = htm.ureg.Unit(_net_unit(units_T)) if units_T else htm.ureg.dimensionless
    if sign_T == -1:  # T = factor / x: the axis is factor / T
        if unit_T != htm.ureg.K:
            raise Unsupported("1/T axis not in kelvin")
        x = {"quantity": "inverse_temperature", "unit": "1/K", "factor": factor}
    else:
        if factor != 1.0 or not unit_T.dimensionality == htm.ureg.K.dimensionality:
            raise Unsupported("temperature axis with a factor")
        x = {"quantity": "temperature", "unit": _unit_name(units_T[0][0])}
    y = {"quantity": "value", "unit": _net_unit(units_y)}
    if scale_y == "ln":
        y["scale"] = "ln"
    return x, values_T, y, values_y


def _module(call):
    import importlib

    dotted = Path(call["file"]).resolve().relative_to(REPO).with_suffix("").as_posix()
    return importlib.import_module(dotted.replace("/", "."))


def _values(node, call):
    """Evaluates a values node (a data reference or a number list) as floats"""
    import numpy as np

    if _is_number_list(node):
        if isinstance(node, ast.Call):
            node = node.args[0]
        values = ast.literal_eval(node)
    else:
        values = eval(compile(ast.Expression(node), "<migrate>", "eval"), vars(_module(call)))
    if hasattr(values, "magnitude"):
        raise Unsupported("values are already a quantity")
    return [float(v) for v in np.asarray(values, dtype=float).ravel()]


def classify(call):
    """Returns ("auto", None) or ("hand", reason)"""
    if call["index"] is None:
        return "hand", "not in htm.database"
    if "property_database" not in Path(call["file"]).parts:
        return "hand", f"computed by HTM code ({Path(call['file']).name}, e.g. D x S)"
    kwargs = call_kwargs(call)
    if None in kwargs:
        return "hand", "unexpected arguments"
    pre_name, energy_name = ARRHENIUS_ARGS[call["cls"]]
    if "data_T" in kwargs or "data_y" in kwargs:
        if {pre_name, energy_name, "range"} & set(kwargs):
            return "hand", "data points with a law or a range"
        try:
            x, values_T, y, values_y = points_axes(call)
            if len(_values(values_T, call)) != len(_values(values_y, call)):
                return "hand", "data points: T and y have different lengths"
        except Unsupported as e:
            return "hand", f"data points: {e}"
        if call["source"].startswith("@") or call["source"] not in _bib_entries():
            return "hand", "source not in references.bib"
        return "auto", None
    unknown = set(kwargs) - {pre_name, energy_name} - OTHER_ARGS
    if unknown:
        return "hand", f"arguments {sorted(unknown)}"
    if pre_name not in kwargs or energy_name not in kwargs:
        return "hand", "missing pre-exponential factor or activation energy"
    for arg in (pre_name, energy_name):
        if literal_quantity(kwargs[arg]) is None:
            return "hand", f"computed {arg}: {ast.unparse(kwargs[arg])[:50]}"
    if literal_quantity(kwargs[energy_name])["kind"] == "exp":
        return "hand", "activation energy in exp()"
    if "range" in kwargs:
        values = _range_values(kwargs["range"])
        if values is None:
            return "hand", f"computed range: {ast.unparse(kwargs['range'])[:50]}"
        if _unit_name(values[0][1]) != _unit_name(values[1][1]):
            return "hand", "range bounds in two different units"
    if call["source"].startswith("@"):
        return "hand", "inline bibtex source"
    if call["source"] not in _bib_entries():
        return "hand", "source not in references.bib"
    return "auto", None


# --- conversion ----------------------------------------------------------------


def _number(node):
    return float(ast.literal_eval(node))


def _unit_name(node):
    """u.cm -> 'cm', htm.ureg.degC -> 'degC'"""
    return node.attr


def _unit_string(units):
    """[(u.cm**2, 1), (u.s, -1)] -> 'cm**2 / s', as typed in the source"""
    out = ""
    for node, sign in units:
        if isinstance(node, ast.BinOp):
            term = f"{_unit_name(node.left)}**{ast.literal_eval(node.right):g}"
        else:
            term = _unit_name(node)
        if not out:
            out = term if sign == 1 else f"1 / {term}"
        else:
            out += f" * {term}" if sign == 1 else f" / {term}"
    return out or "dimensionless"


def reported(call):
    """The reported block of an automatically convertible call"""
    kwargs = call_kwargs(call)
    if "data_T" in kwargs:
        x, values_T, y, values_y = points_axes(call)
        rows = list(zip(_values(values_T, call), _values(values_y, call)))
        return {
            "form": "points",
            "file": None,  # set by run() to <record id>.csv
            "x": {"column": 0, **x},
            "y": {"column": 1, **y},
            "_rows": rows,
        }
    pre_name, energy_name = ARRHENIUS_ARGS[call["cls"]]
    pre = literal_quantity(kwargs[pre_name])
    energy = literal_quantity(kwargs[energy_name])

    if energy["kind"] == "k_B":
        # E = value * K * k_B: the paper gives E / k_B in kelvin
        act_energy = {"value": _number(energy["number"]), "unit": "K"}
    else:
        act_energy = {"value": _number(energy["number"]), "unit": _unit_string(energy["units"])}

    out = {}
    if pre["kind"] == "exp":
        out = {
            "form": "log_linear",
            "base": "e",
            "intercept": _number(pre["number"].args[0]),
            "y_unit": _unit_string(pre["units"]),
        }
        if act_energy["unit"] == "K":
            out["slope"] = {"value": -act_energy["value"], "unit": "K"}
        else:
            out["act_energy"] = act_energy
    else:
        out = {
            "form": "arrhenius",
            "pre_exp": {"value": _number(pre["number"]), "unit": _unit_string(pre["units"])},
            "act_energy": act_energy,
        }
    out["range"] = None
    if "range" in kwargs:
        (a, unit_a), (b, unit_b) = _range_values(kwargs["range"])
        if _unit_name(unit_a) != _unit_name(unit_b):
            raise ValueError(f"range with two units at {call['file']}:{call['line']}")
        out["range"] = {"value": [_number(a), _number(b)], "unit": _unit_name(unit_a)}
    return out


_bib = {}


def _bib_entries():
    if not _bib:
        from pybtex.database import parse_file

        _bib.update(parse_file(str(REPO / "h_transport_materials" / "references.bib")).entries)
    return _bib


# --- writing records -------------------------------------------------------------

PROPERTY_NAMES = {
    "Diffusivity": "diffusivity",
    "Solubility": "solubility",
    "Permeability": "permeability",
    "RecombinationCoeff": "recombination_coeff",
    "DissociationCoeff": "dissociation_coeff",
}
LAWS = {"sievert": "sieverts", "henry": "henry", None: None}

# codes used in record ids for materials without an element symbol
MATERIAL_CODES = {
    "alumina": "Al2O3", "apmt": "APMT", "cucrzr": "CuCrZr", "eurofer_97": "EUROFER97",
    "fe22cr5al": "Fe22Cr5Al", "flinak": "FLiNaK", "hastelloy_n": "HastelloyN",
    "hastelloy_x": "HastelloyX", "incoloy_800": "Incoloy800", "inconel_600": "Inconel600",
    "inconel_625": "Inconel625", "inconel_750": "Inconel750", "nimonic_80a": "Nimonic80A",
    "oxidized_1605": "Oxidized1605", "pd52cu": "Pd52Cu", "60pd40cu": "Pd60Cu40",
    "pdag": "PdAg", "304_steel": "SS304", "316l_steel": "SS316L", "rafm_steel": "RAFM",
    "series_300_steel": "SS300", "t35y": "T35Y", "t54y": "T54Y", "thermacore": "Thermacore",
    "thermacore_oxidized": "ThermacoreOx", "tzm": "TZM", "v4cr4ti": "V4Cr4Ti",
}

FLAG = "migrated automatically: check the values, method and location against the paper"


def _yaml():
    import yaml

    return yaml


def _read_yaml(path):
    with open(path, encoding="utf-8") as f:
        return _yaml().safe_load(f)


def _write_yaml(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        _yaml().safe_dump(content, f, sort_keys=False, allow_unicode=True, width=100)


def _material_entry(attr, material):
    """A registry entry generated from an htm material object"""
    families = [p.family for p in material.parents if p.family != "material"]
    families = list(dict.fromkeys(families))  # duplicates in the class hierarchy
    if "compound" in families:  # Compound subclasses Metal in the current API
        families = ["ceramic" if f == "metal" else f for f in families]
    symbol = getattr(material, "symbol", None)
    entry = {
        "id": material.name,
        "code": symbol or MATERIAL_CODES[material.name],
        "name": material.name,
        "families": families,
    }
    if symbol:
        entry["symbol"] = symbol
        entry["composition"] = {symbol: 100}
    entry["htm_legacy"] = attr
    return entry


def _material_ids(data_dir):
    """legacy material name -> registry id, creating missing registry entries"""
    import h_transport_materials as htm

    legacy = {
        getattr(htm, a).name: (a, getattr(htm, a))
        for a in dir(htm)
        if isinstance(getattr(htm, a), htm.Material)
    }
    mapping = {}
    for path in sorted((data_dir / "materials").glob("*.yaml")):
        m = _read_yaml(path)
        if m.get("htm_legacy"):
            name = getattr(htm, m["htm_legacy"]).name
            if name not in mapping or m["id"] == name:
                mapping[name] = m["id"]
    created = []
    for name, (attr, material) in sorted(legacy.items()):
        if name not in mapping:
            entry = _material_entry(attr, material)
            _write_yaml(data_dir / "materials" / f"{entry['id']}.yaml", entry)
            mapping[name] = entry["id"]
            created.append(entry["id"])
    return mapping, created


def _source_ref(call, sources_dir, fetch, cache):
    """{doi: ...} or {key: ...} for the call's source, creating the source file"""
    from . import sources

    if call["doi"]:
        doi = sources.strip_doi(call["doi"])
        if doi not in cache:
            cache[doi] = sources.add_doi(doi, sources_dir, fetch=fetch)[0].key
        return {"doi": doi}, cache[doi]
    bib_key = call["source"]
    if bib_key not in cache:
        from pybtex.database import BibliographyData

        text = BibliographyData({bib_key: _bib_entries()[bib_key]}).to_string("bibtex")
        existing = sources.existing_sources(sources_dir)
        (candidate,) = sources.bibtex_to_sources(text, taken=existing)
        same = [
            s for s in existing.values()
            if not s.doi and s.year == candidate.year and s.title.lower() == candidate.title.lower()
        ]
        cache[bib_key] = same[0].key if same else sources.write_source(candidate, sources_dir).stem
    return {"key": cache[bib_key]}, cache[bib_key]


def _relative(path):
    return Path(path).resolve().relative_to(REPO).as_posix()


def _match_existing(data_dir, manifest, calls):
    """Adds manifest entries for records written by hand.

    A record with ``curation.migrated_from`` is matched to the property
    created at that location; older ones are matched by class, source,
    isotope and sample form.
    """
    import h_transport_materials as htm

    from . import build, compat

    by_location = {
        f"{_relative(c['file'])}:{c['line']}": c
        for c in calls
        if c["index"] is not None and "property_database" in Path(c["file"]).parts
    }
    db = build.build(data_dir)
    materials = {m["id"]: m for m in db["materials"]}
    srcs = {s["key"]: s for s in db["sources"]}
    for record in db["records"]:
        if record["id"] in manifest:
            continue
        location = record["curation"].get("migrated_from")
        if location in by_location:
            call = by_location[location]
            manifest[record["id"]] = {"index": call["index"], "class": call["cls"]}
            continue
        new = compat.to_property(record, materials, srcs)
        matches = [
            i for i, p in enumerate(htm.database)
            if type(p) is type(new) and p.source == new.source
            and (p.isotope or "").upper() == new.isotope
        ]
        form = (record.get("sample") or {}).get("form")
        if len(matches) > 1 and form:
            matches = [i for i in matches if htm.database[i].note and form in htm.database[i].note]
        if len(matches) == 1:
            manifest[record["id"]] = {"index": matches[0], "class": type(new).__name__}


def run(data_dir=None, fetch=None):
    """Converts every automatically convertible property and lists the rest.

    Writes data/records/*.yaml, missing data/materials and data/sources files,
    data/migration/legacy.yaml (record id -> index in htm.database, for the
    equivalence test) and data/migration/todo.md (what needs a human).

    Returns:
        dict: counts of written records, records in the manifest, properties
            left for hand transcription, and materials created
    """
    from . import build, sources
    from .models import PROPERTY_CODES, Record

    data_dir = Path(data_dir or build.DATA_DIR)
    fetch = fetch or sources.fetch_csl
    manifest_path = data_dir / "migration" / "legacy.yaml"
    manifest = (_read_yaml(manifest_path) if manifest_path.exists() else None) or {}
    calls = capture()
    _match_existing(data_dir, manifest, calls)
    done = {v["index"] for v in manifest.values()}

    material_ids, created_materials = _material_ids(data_dir)
    codes = {m["id"]: m["code"] for m in map(_read_yaml, (data_dir / "materials").glob("*.yaml"))}
    taken = {p.stem for p in (data_dir / "records").glob("*.yaml")}
    cache, todo, written = {}, [], 0

    for call in calls:
        if call["index"] in done:
            continue
        kind, reason = classify(call)
        if kind == "hand":
            if call["index"] is not None:
                todo.append((call, reason))
            continue
        material = material_ids[call["material"]]
        isotope = call["isotope"].upper()
        try:
            source, key = _source_ref(call, data_dir / "sources", fetch, cache)
        except Exception as e:
            todo.append((call, f"source file: {str(e).splitlines()[0][:80]}"))
            continue
        base = f"{codes[material]}-{PROPERTY_CODES[PROPERTY_NAMES[call['cls']]]}-{isotope}-{key}"
        record_id, suffix = base, ord("b")
        while record_id in taken:
            record_id, suffix = f"{base}-{chr(suffix)}", suffix + 1
        try:
            rep = reported(call)
        except Unsupported as e:
            todo.append((call, f"data points: {e}"))
            continue
        rows = rep.pop("_rows", None)
        if rows is not None:
            rep["file"] = f"{record_id}.csv"
        content = {
            "id": f"htm:{record_id}",
            "property": PROPERTY_NAMES[call["cls"]],
            "law": LAWS[call["law"]],
            "material": material,
            "isotope": isotope,
            "method": "unknown",
            "source": {**source, "location": None},
            "reported": rep,
            "note": call["note"],
            "curation": {
                "status": "draft",
                "flags": [FLAG],
                "migrated_from": f"{_relative(call['file'])}:{call['line']}",
            },
        }
        content = {k: v for k, v in content.items() if v is not None}
        try:
            Record(**content)
        except Exception as e:
            todo.append((call, f"validation: {str(e).splitlines()[0][:80]}"))
            continue
        _write_yaml(data_dir / "records" / f"{record_id}.yaml", content)
        if rows is not None:
            (data_dir / "records" / rep["file"]).write_text(
                "".join(f"{x!r},{y!r}\n" for x, y in rows), encoding="utf-8"
            )
        taken.add(record_id)
        manifest[content["id"]] = {"index": call["index"], "class": call["cls"]}
        written += 1

    _write_yaml(manifest_path, dict(sorted(manifest.items())))
    _write_todo(data_dir / "migration" / "todo.md", todo)
    return {
        "written": written,
        "records": len(manifest),
        "hand": len(todo),
        "materials_created": created_materials,
    }


def _write_todo(path, todo):
    lines = [
        "# Properties to transcribe by hand",
        "",
        "Generated by `htm migrate`. These property_database entries use",
        "computed values, data points or other patterns the migration tool does",
        "not convert automatically.",
        "",
        "| Location | Property | Isotope | Material | Reason |",
        "|---|---|---|---|---|",
    ]
    for call, reason in sorted(todo, key=lambda t: (t[0]["file"], t[0]["line"])):
        reason = reason.replace("|", "/")
        lines.append(
            f"| `{_relative(call['file'])}:{call['line']}` | {call['cls']}"
            f" | {call['isotope']} | {call['material']} | {reason} |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
