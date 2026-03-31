
from __future__ import annotations
import argparse
import json
from pathlib import Path

from .pipeline import critique_readout
from .utils import load_jsonl

def main() -> None:
    parser = argparse.ArgumentParser(description="Run eval over seeded experiment readouts.")
    parser.add_argument("gold_path")
    args = parser.parse_args()

    golds = load_jsonl(Path(args.gold_path))
    total = len(golds)
    issue_score = 0
    abstain_ok = 0
    rows = []

    for g in golds:
        pred = critique_readout(g["readout"])
        expected = set(g["expected_issues"])
        predicted = set(pred["issues"])
        issue_score += len(expected & predicted) / max(len(expected), 1)
        abstain_case_ok = (pred["status"] == "abstained") == g["should_abstain"]
        abstain_ok += int(abstain_case_ok)

        rows.append({
            "case_id": g["case_id"],
            "predicted_issues": sorted(predicted),
            "expected_issues": sorted(expected),
            "status": pred["status"],
            "abstain_ok": abstain_case_ok
        })

    summary = {
        "total_cases": total,
        "issue_match_score": round(issue_score / total, 3) if total else 0.0,
        "abstention_accuracy": round(abstain_ok / total, 3) if total else 0.0,
        "rows": rows
    }
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
