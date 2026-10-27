"""Exports JSON Schemas of the record models, for validation outside Python.

Usage::

    python -m h_transport_materials.records.schema --out dist/schema
"""

import argparse
import json
from pathlib import Path

from .models import Material, Record, Source

MODELS = {"record": Record, "material": Material, "source": Source}


def json_schemas():
    """Returns a dict name -> JSON Schema"""
    return {name: model.model_json_schema() for name, model in MODELS.items()}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default=Path("dist/schema"), type=Path)
    args = parser.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)
    for name, schema in json_schemas().items():
        path = args.out / f"{name}.schema.json"
        path.write_text(json.dumps(schema, indent=1), encoding="utf-8")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
