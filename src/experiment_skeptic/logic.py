
from __future__ import annotations
from typing import Any

def detect_missing_evidence(readout: dict[str, Any]) -> list[str]:
    missing = []
    if not readout.get("primary_metric_definition", "").strip():
        missing.append("Primary metric definition missing")
    if not readout.get("sample_size_note", "").strip():
        missing.append("Sample size or power note missing")
    if not readout.get("segment_notes", "").strip():
        missing.append("Segment review notes missing")
    return missing

def should_abstain(readout: dict[str, Any], missing: list[str]) -> tuple[bool, list[str]]:
    reasons = []
    if "Primary metric definition missing" in missing:
        reasons.append("Cannot critique rollout quality without primary metric definition")
    if len(readout.get("summary", "").strip()) < 25:
        reasons.append("Experiment summary too sparse to critique reliably")
    return bool(reasons), reasons

def detect_issues(readout: dict[str, Any]) -> list[str]:
    summary = readout.get("summary", "").lower()
    sample_note = readout.get("sample_size_note", "").lower()
    segment_notes = readout.get("segment_notes", "").lower()
    secondary = readout.get("secondary_metric_notes", "").lower()
    rollout = readout.get("rollout_recommendation", "").lower()

    issues = []

    if "small sample" in sample_note or "2 days" in summary or "2 days" in sample_note or "underpowered" in sample_note:
        issues.append("low_power_risk")
    if "not reviewed" in segment_notes or "desktop only" in segment_notes or not segment_notes.strip():
        issues.append("missing_segment_analysis")
    if ("100%" in rollout or "full rollout" in rollout or "ship broadly" in rollout or "all users" in rollout) and (
        "missing_segment_analysis" in issues or "low_power_risk" in issues or "declined" in secondary or "down" in secondary
    ):
        issues.append("rollout_overreach")
    if "declined" in secondary or "down" in secondary or "unchanged" in secondary and "improved" in summary:
        issues.append("conflicting_metric_signal")
    if not issues:
        issues.append("mixed_or_unclear")
    return list(dict.fromkeys(issues))

def severity_band(issues: list[str]) -> str:
    if "rollout_overreach" in issues and ("low_power_risk" in issues or "conflicting_metric_signal" in issues):
        return "high"
    if "rollout_overreach" in issues or "low_power_risk" in issues:
        return "medium"
    return "low"

def safer_recommendation_frame(issues: list[str]) -> str:
    if "rollout_overreach" in issues and "missing_segment_analysis" in issues:
        return "Promising signal, but do not recommend full rollout until missing segments are reviewed."
    if "low_power_risk" in issues:
        return "Treat this as directional only. Gather more evidence before broad rollout."
    if "conflicting_metric_signal" in issues:
        return "Do not ship broadly until the tradeoff between primary and secondary metrics is resolved."
    return "Recommendation should remain limited until evidence quality improves."

def questions_to_answer(issues: list[str]) -> list[str]:
    qs = []
    if "missing_segment_analysis" in issues:
        qs.append("Which unreviewed segments could change the decision?")
    if "low_power_risk" in issues:
        qs.append("What additional sample size or duration is needed before rollout?")
    if "rollout_overreach" in issues:
        qs.append("Why is full rollout justified instead of phased rollout?")
    if "conflicting_metric_signal" in issues:
        qs.append("Which metric governs the final decision when primary and secondary outcomes conflict?")
    if not qs:
        qs.append("What evidence would meaningfully change this recommendation?")
    return qs[:5]
