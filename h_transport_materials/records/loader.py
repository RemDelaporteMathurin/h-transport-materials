"""Loads the compiled database shipped with the package.

Wheels contain ``h_transport_materials/_data/htm-data.json``, built from
``data/`` by the release workflow. This module only needs the standard
library, numpy and pint: pydantic and pyyaml are only needed to build.

From a git checkout or an editable install the file does not exist yet; it
is then built from ``data/`` on first use (with the ``build`` extra),
cached next to the package, and rebuilt whenever ``data/`` changes.
"""

import json
import warnings
from pathlib import Path

COMPILED = Path(__file__).resolve().parents[1] / "_data" / "htm-data.json"
DATA_DIR = Path(__file__).resolve().parents[2] / "data"

_cache = {}


class MissingDatabaseError(RuntimeError):
    pass


def _build_from_source(path):
    """Builds the compiled database from data/ and caches it at path"""
    if not DATA_DIR.is_dir():
        raise MissingDatabaseError(
            f"no compiled database at {path} and no data/ folder to build it from."
            " Reinstall h_transport_materials from PyPI."
        )
    try:
        from . import build
    except ImportError as e:
        raise MissingDatabaseError(
            "This h_transport_materials install has no compiled database (installed"
            " from a git checkout?). Building it from data/ needs the build extra:"
            " pip install h_transport_materials[build], or run"
            f" `htm build --out {path}`."
        ) from e
    db = build.build(DATA_DIR)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(db, ensure_ascii=False), encoding="utf-8")
    except OSError:
        pass  # read-only install: rebuild next time
    return db


def _is_stale(path):
    """In a source checkout, True if data/ changed after path was built"""
    if not DATA_DIR.is_dir():
        return False  # installed from a wheel: the shipped file is the truth
    built = path.stat().st_mtime
    return any(f.stat().st_mtime > built for f in DATA_DIR.rglob("*") if f.is_file())


def _load_compiled(path):
    if path.exists() and not _is_stale(path):
        return json.loads(path.read_text(encoding="utf-8"))
    try:
        return _build_from_source(path)
    except MissingDatabaseError:
        if not path.exists():
            raise
        warnings.warn(
            f"data/ changed since {path} was built but it cannot be rebuilt"
            " without the build extra; using the old file"
        )
        return json.loads(path.read_text(encoding="utf-8"))


def load(path=None):
    """Returns the compiled database as a dict (materials, sources, records)

    Args:
        path (str or Path, optional): a compiled database file, e.g. one
            attached to a GitHub release. Defaults to the one shipped with
            the package.
    """
    path = Path(path) if path is not None else COMPILED
    key = str(path)
    if key not in _cache:
        if path == COMPILED:
            _cache[key] = _load_compiled(path)
        elif path.exists():
            _cache[key] = json.loads(path.read_text(encoding="utf-8"))
        else:
            raise FileNotFoundError(path)
    return _cache[key]


def properties(path=None):
    """Returns the records as an htm.PropertiesGroup of property objects"""
    key = ("group", str(path))
    if key not in _cache:
        from .compat import to_properties_group

        _cache[key] = to_properties_group(load(path))
    return _cache[key]


def get(record_id, path=None):
    """Returns the property with this record id, e.g. 'htm:W-D-H-frauenfelder1969'

    The full record (as published, transformations, curation) is in
    ``prop.record``.
    """
    for prop in properties(path):
        if prop.record_id == record_id:
            return prop
    raise KeyError(f"no record {record_id!r}")
