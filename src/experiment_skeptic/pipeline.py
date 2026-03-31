
from __future__ import annotations
from typing import Any

from .logic import detect_missing_evidence, should_abstain, detect_issues, severity_band, safer_recommendation_frame, questions_to_answer
from .validator import validate_readout, validate_critique

def critique_readout(readout: dict[str, Any]) -> dict[str, Any]:
    validate_readout(readout)

    missing = detect_missing_evidence(readout)
    abstain, reasons = should_abstain(readout, missing)
    if abstain:
        critique = {
            "readout_id": readout["readout_id"],
            "status": "abstained",
            "issues": ["mixed_or_unclear"],
            "severity_band": "low",
            "missing_evidence": list(dict.fromkeys(missing + reasons)),
            "safer_recommendation_frame": "Do not make a rollout recommendation until the experiment evidence is more complete.",
            "questions_to_answer": [
                "What is the primary metric definition?",
                "What supporting evidence is needed to critique this readout safely?"
            ]
        }
        validate_critique(critique)
        return critique

    issues = detect_issues(readout)
    critique = {
        "readout_id": readout["readout_id"],
        "status": "critique_ready",
        "issues": issues,
        "severity_band": severity_band(issues),
        "missing_evidence": missing,
        "safer_recommendation_frame": safer_recommendation_frame(issues),
        "questions_to_answer": questions_to_answer(issues)
    }
    validate_critique(critique)
    return critique
