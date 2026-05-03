# Market Prompt
This is an execution template, not a system prompt.

RUN_DIR: [set your run directory]

---

## Hypothesis

[Same hypothesis as before]

---

## Research Context

Provide minimal but concrete context:

* Domain:
* Target audience:
* Scenario:
* Constraints (optional):

---

## Instructions

Validate whether this problem exists in reality.

You MUST:

* identify if similar problems exist
* identify who experiences them
* identify how they are currently solved
* identify gaps in existing solutions

---

## Evidence Rules

* no evidence → no claim
* distinguish facts from assumptions
* provide references when using external information

---

## Signal Analysis

Classify findings:

* strong signal
* weak signal
* no signal

---

## Output Requirements

Generate:

1. Market analysis file:
   RUN_DIR/outputs/market_analysis.md

2. Completion marker:
   RUN_DIR/outputs/market_analysis_complete.marker

---

## Important

* do NOT invent market demand
* do NOT generalize without evidence
* prefer uncertainty over hallucination
