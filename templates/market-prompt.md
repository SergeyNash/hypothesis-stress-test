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

Use evidence channels in this order:

1. Local KB inventory (`outputs/evidence_inventory.md`) if available
2. Confluence MCP
3. External sources (only if gaps remain and user approves)
4. Inferred signals (last resort)

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
* Local Signals from Knowledge Base
* Confluence Signals
* External Market Signals
* Inferred Signals
* Signal Summary

Generate completion marker:

`RUN_DIR/outputs/market_analysis_complete.marker`

---

## Important

* do NOT invent market demand
* do NOT generalize without evidence
* prefer uncertainty over hallucination
