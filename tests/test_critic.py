
from experiment_skeptic.pipeline import critique_readout

def test_abstain_on_missing_metric_definition():
    readout = {
        "readout_id": "T-1",
        "summary": "Variant looks better. Recommend rollout.",
        "primary_metric_definition": "",
        "sample_size_note": "",
        "segment_notes": "",
        "secondary_metric_notes": "",
        "rollout_recommendation": "full rollout"
    }
    critique = critique_readout(readout)
    assert critique["status"] == "abstained"

def test_flags_rollout_overreach():
    readout = {
        "readout_id": "T-2",
        "summary": "Variant improved conversion over 2 days.",
        "primary_metric_definition": "conversion",
        "sample_size_note": "small sample",
        "segment_notes": "mobile not reviewed",
        "secondary_metric_notes": "",
        "rollout_recommendation": "full rollout"
    }
    critique = critique_readout(readout)
    assert "rollout_overreach" in critique["issues"]
