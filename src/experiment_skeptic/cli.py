
from __future__ import annotations
import argparse
import json
from pathlib import Path

from .pipeline import critique_readout
from .utils import load_json

def main() -> None:
    parser = argparse.ArgumentParser(description="Critique an experiment readout.")
    parser.add_argument("readout_path", help="Path to readout JSON file")
    args = parser.parse_args()

    readout = load_json(Path(args.readout_path))
    critique = critique_readout(readout)
    print(json.dumps(critique, indent=2))

if __name__ == "__main__":
    main()
