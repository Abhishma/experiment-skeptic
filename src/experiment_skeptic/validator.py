
from __future__ import annotations
from pathlib import Path
from jsonschema import validate

from .utils import load_json

ROOT = Path(__file__).resolve().parents[2]

def validate_readout(readout: dict) -> None:
    schema = load_json(ROOT / "schemas" / "readout_input.schema.json")
    validate(instance=readout, schema=schema)

def validate_critique(critique: dict) -> None:
    schema = load_json(ROOT / "schemas" / "critique_output.schema.json")
    validate(instance=critique, schema=schema)
