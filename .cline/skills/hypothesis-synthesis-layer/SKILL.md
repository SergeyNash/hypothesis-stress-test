---
name: hypothesis-synthesis-layer
description: Execute the Synthesis Layer. Compare internal and external signals, classify the hypothesis, and produce hypothesis_map and digest. Use after Roles and Market layers complete.
---

# Synthesis Layer

Compare internal and external signals. Expose contradictions — do not smooth them.

## Prerequisites

Read all prior outputs:

- `RUN_DIR/outputs/role_outputs/*`
- `RUN_DIR/outputs/hypothesis_summary.md`
- `RUN_DIR/outputs/market_analysis.md`

Do not run if Market or Roles outputs are missing. Ask user to complete prior layers.

## Task

Compare internal vs external signals. Do NOT:

- Generate new ideas
- Add external assumptions
- Smooth contradictions
- Merge perspectives into false consensus

## Classification model

Classify into one or more categories:

| Category | Meaning | Action |
|----------|---------|--------|
| **Validated Opportunity** | Internal + external align | Proceed |
| **Internal Illusion** | Internal strong, market weak | Do NOT build |
| **Blind Spot** | Market strong, internal misses it | Investigate |
| **Weak Signal** | No strong evidence | Low priority |

## Analysis requirements

- Where signals align
- Contradictions (most important)
- Missing perspectives
- Confidence level per conclusion: High / Medium / Low

## Outputs

### Full analysis

`RUN_DIR/outputs/hypothesis_map.md`

### Short digest

`RUN_DIR/outputs/hypothesis_digest.txt` — 5–10 lines:

- Classification
- Key conflict
- Primary risk
- Recommended next step

### Completion marker

`RUN_DIR/outputs/synthesis_complete.marker`

## Reference

Based on `templates/synthesis-prompt.md` and `layers/synthesis-layer.md`.
