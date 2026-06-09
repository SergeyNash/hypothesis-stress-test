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

**Confluence first (if MCP available):** search internal wiki for local signals before external sources.

You MUST:

* search Confluence for related internal evidence (local signals)
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

Generate `RUN_DIR/outputs/market_analysis.md` with sections:

* MCP Status
* Local Signals (Confluence)
* External Signals
* Inferred Signals
* Signal Summary

Generate completion marker:

`RUN_DIR/outputs/market_analysis_complete.marker`

---

## Important

* do NOT invent market demand
* do NOT generalize without evidence
* prefer uncertainty over hallucination
