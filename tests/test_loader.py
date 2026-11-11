"""Tests for reading the compiled record database (h_transport_materials.records.loader)."""

import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

import h_transport_materials as htm
from h_transport_materials import records
from h_transport_materials.records import loader

REPO = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def compiled(tmp_path_factory):
    pytest.importorskip("pydantic")
    from h_transport_materials.records import build

    path = tmp_path_factory.mktemp("compiled") / "htm-data.json"
    path.write_text(json.dumps(build.build()), encoding="utf-8")
    return path


def test_load_and_get(compiled):
    group = htm.load(compiled)
    assert isinstance(group, htm.PropertiesGroup)
    assert len(group) == len(json.loads(compiled.read_text(encoding="utf-8"))["records"])

    D = htm.get("htm:W-D-H-frauenfelder1969", compiled)
    assert isinstance(D, htm.Diffusivity)
    assert D.record["reported"]["pre_exp"] == {"value": 4.1e-3, "unit": "cm^2/s", "unit_as_printed": None}
    assert D.material == htm.TUNGSTEN


def test_unknown_id(compiled):
    with pytest.raises(KeyError, match="no record"):
        htm.get("htm:W-D-H-nobody2000", compiled)


def test_missing_file():
    with pytest.raises(FileNotFoundError):
        htm.load("does/not/exist.json")


def test_builds_and_caches_when_not_compiled(tmp_path, monkeypatch):
    """git checkout or editable install: built from data/ on first use, then cached"""
    pytest.importorskip("pydantic")
    target = tmp_path / "_data" / "htm-data.json"
    monkeypatch.setattr(loader, "COMPILED", target)
    monkeypatch.setattr(loader, "_cache", {})

    db = loader.load()
    assert target.exists()
    assert len(db["records"]) > 0


def test_rebuilds_when_data_changed(tmp_path, monkeypatch):
    """In a source checkout, editing data/ invalidates the cached build"""
    pytest.importorskip("pydantic")
    target = tmp_path / "_data" / "htm-data.json"
    monkeypatch.setattr(loader, "COMPILED", target)
    monkeypatch.setattr(loader, "_cache", {})
    loader.load()

    os.utime(target, (0, 0))  # pretend it was built before the data files
    assert loader._is_stale(target)
    monkeypatch.setattr(loader, "_cache", {})
    loader.load()
    assert not loader._is_stale(target)


def test_clear_message_without_build_extra(tmp_path, monkeypatch):
    monkeypatch.setattr(loader, "COMPILED", tmp_path / "missing.json")
    monkeypatch.setattr(loader, "_cache", {})
    if hasattr(records, "build"):
        monkeypatch.delattr(records, "build")
    monkeypatch.setitem(sys.modules, "h_transport_materials.records.build", None)

    with pytest.raises(loader.MissingDatabaseError, match=r"h_transport_materials\[build\]"):
        loader.load()


def test_reading_needs_no_build_extra(compiled):
    """Reading the compiled database works with pydantic and pyyaml unavailable"""
    code = textwrap.dedent(
        f"""
        import sys

        class Block:
            def find_spec(self, name, path=None, target=None):
                if name.split(".")[0] in ("pydantic", "yaml"):
                    raise ImportError(f"blocked {{name}}")

        sys.meta_path.insert(0, Block())

        import h_transport_materials as htm
        D = htm.get("htm:W-D-H-frauenfelder1969", {str(compiled)!r})
        assert D.record_id == "htm:W-D-H-frauenfelder1969"
        print("ok")
        """
    )
    result = subprocess.run(
        [sys.executable, "-W", "ignore", "-c", code],
        cwd=REPO,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": str(REPO)},
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "ok"
