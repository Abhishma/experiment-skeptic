# Experiment Skeptic

AI-assisted critique for A/B test readouts, decision quality, and rollout reasoning.

## Why this exists

Many bad product decisions do not come from bad experiments.
They come from bad readouts.

Small uplifts become "ship it."
Missing segments are ignored.
Metric definitions drift between slides.
Rollout language outruns the evidence.

This pattern is visible in product environments where experimentation infrastructure improves measurement quality but does not improve decision quality — teams measure more precisely while reasoning less carefully.

**Experiment Skeptic** critiques experiment summaries for:
- weak inference
- missing segment analysis
- rollout overreach
- inconsistent metric framing
- evidence gaps
- abstention when data quality is too weak

This is not a statistics engine.
It is a decision-quality critique layer.

## What it does

Input:
- experiment summary
- primary metric definition
- segment notes
- sample size or power note
- rollout recommendation

Output:
- critique issues
- severity
- questions to answer before rollout
- safer decision framing
- abstention when evidence is too weak

## What it does not do

- It does not replace statistical review
- It does not auto-approve rollouts
- It does not pretend noisy data is conclusive

## Run

```bash
pip install -r requirements.txt
export PYTHONPATH=src
python -m experiment_skeptic.cli examples/readout_01.json
python -m experiment_skeptic.eval_runner eval/goldens/readout_cases.jsonl
streamlit run streamlit_app.py
```

## Design choices

- **Critique, not generation** — this tool flags issues in existing readouts; it does not produce readouts or summaries
- **Bounded issue taxonomy** — critique categories are constrained and auditable. v1 uses heuristic pattern detection against a defined issue taxonomy. This is intentional: a bounded, evaluable heuristic is more trustworthy than a model generating generic analytical commentary.
- **Abstention on weak evidence** — when readout inputs are too thin, the system abstains rather than producing spurious critique
- **Structured outputs over prose blobs** — every issue includes severity and a specific question to resolve before rollout

## Repo structure

- `src/experiment_skeptic/` — core implementation
- `examples/` — sample readout inputs
- `schemas/` — readout input and critique output JSON schemas
- `eval/` — rubric and evaluation harness
- `demo/` — sample outputs

## Portfolio point

This repo is about making decision quality harder to fake. The PM design decision is the issue taxonomy and the abstention conditions — not the critique sophistication.

## Known limitations

- v1 critiques rollout reasoning, not underlying statistical validity in a rigorous sense
- heuristic pattern detection, not semantic inference — intentionally constrained for auditability
- examples are intentionally bounded and should be expanded before broader claims
- next upgrade: richer issue taxonomy, semantic inference layer, expanded gold case set

## Where automation stops

- it does not approve launches
- it does not replace stats review
- it does not infer missing experiment details with confidence
- it abstains when readout evidence is too thin

## Trust boundary

This project is decision support, not automation. It produces structured critique for human review and abstains when readout evidence is insufficient for confident analysis.
