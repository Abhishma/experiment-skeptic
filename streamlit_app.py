
from __future__ import annotations
from pathlib import Path
import streamlit as st

from experiment_skeptic.pipeline import critique_readout
from experiment_skeptic.utils import load_json, load_jsonl

ROOT = Path(__file__).resolve().parent
EXAMPLES = ROOT / "examples"
GOLDS = ROOT / "eval" / "goldens" / "readout_cases.jsonl"

st.set_page_config(page_title="Experiment Skeptic", layout="wide")
st.title("Experiment Skeptic")
st.caption("AI-assisted critique for A/B test readouts, rollout logic, and decision quality.")

example = st.sidebar.selectbox("Example readout", ["readout_01.json", "readout_02.json", "readout_03.json", "readout_04.json"])
readout = load_json(EXAMPLES / example)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Readout input")
    st.json(readout)

with col2:
    st.subheader("Critique output")
    critique = critique_readout(readout)
    st.json(critique)
    if critique["status"] == "abstained":
        st.warning("System abstained due to weak or incomplete evidence.")
    else:
        st.success(f"Critique ready with {len(critique['issues'])} issue(s).")

st.markdown("---")
st.subheader("Quick evaluation snapshot")
if st.button("Run eval on gold readouts"):
    golds = load_jsonl(GOLDS)
    total = len(golds)
    issue_score = 0
    abstain_ok = 0
    rows = []
    for g in golds:
        pred = critique_readout(g["readout"])
        expected = set(g["expected_issues"])
        predicted = set(pred["issues"])
        issue_score += len(expected & predicted) / max(len(expected), 1)
        ok = (pred["status"] == "abstained") == g["should_abstain"]
        abstain_ok += int(ok)
        rows.append({
            "case_id": g["case_id"],
            "predicted": sorted(predicted),
            "expected": sorted(expected),
            "status": pred["status"],
            "abstain_ok": ok
        })
    c1, c2 = st.columns(2)
    c1.metric("Issue match score", f"{issue_score/total:.0%}")
    c2.metric("Abstention accuracy", f"{abstain_ok/total:.0%}")
    st.dataframe(rows, use_container_width=True)

st.markdown("---")
st.subheader("Portfolio interpretation")
if critique["status"] == "abstained":
    st.write("This refusal is a feature. The system avoids acting confident when the readout is too thin.")
else:
    st.write("This repo critiques rollout reasoning instead of pretending to automate experiment judgment.")
