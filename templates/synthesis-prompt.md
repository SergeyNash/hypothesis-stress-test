# Synthesis Prompt
This is an execution template, not a system prompt.

RUN_DIR: [set your run directory]

---

## Instructions

Read all outputs from previous steps:

* role_outputs/*
* hypothesis_summary.md
* market_analysis.md

---

## Task

Compare internal and external signals.

Do NOT generate new ideas.

Do NOT add external assumptions.

---

## Classification Model

Classify the hypothesis into one or more categories:

1. Validated Opportunity
2. Internal Illusion
3. Blind Spot
4. Weak Signal

---

## Analysis Requirements

* identify where signals align
* identify contradictions
* identify missing perspectives
* explain reasoning clearly

---

## Output Requirements

Generate:

1. Full analysis:
   RUN_DIR/outputs/hypothesis_map.md

2. Short digest:
   RUN_DIR/outputs/hypothesis_digest.txt

3. Completion marker:
   RUN_DIR/outputs/synthesis_complete.marker

---

## Important

* focus on conflicts, not summaries
* avoid smoothing contradictions
* uncertainty is allowed and expected
