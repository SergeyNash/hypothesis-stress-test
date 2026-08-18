# Decision Review Prompt

This is an execution template, not a system prompt.

RUN_DIR: [set your run directory]

---

## Prerequisites

Customer Discovery Planning must be complete. Read:

- `input/hypothesis.md`
- `outputs/hypothesis_summary.md`
- `outputs/evidence_inventory.md`
- `outputs/business_context_analysis.md` or `outputs/missing_business_context.md`
- `outputs/market_analysis.md`
- `outputs/hypothesis_map.md`
- `outputs/hypothesis_digest.txt` (optional)
- `outputs/customer_discovery_plan.md`
- `outputs/role_outputs/*` (optional)

---

## Core principle

Assume the current conclusion may be wrong.

Do not support the recommendation. Identify why it may fail.

Do NOT repeat or summarize synthesis outputs. Add new critical thinking only.

You may reference existing Roles, Local Evidence, Business Context, Market, Synthesis, and Customer Discovery Planning artifacts. Do NOT perform new retrieval, Confluence/external research, market research, or role analysis. Do NOT introduce uncited signals. Every factual challenge must be traceable to an existing artifact and its cited evidence; report missing context as a gap for validation.

---

## Task

Execute the 7-step review process:

1. Evaluate evidence quality (Strong / Moderate / Weak / Unsupported per conclusion)
2. Identify hidden assumptions
3. Search for missing perspectives
4. Evaluate scalability (10 / 50 / 100 / enterprise)
5. Evaluate business risk (false positive / false negative)
6. Challenge the recommendation
7. Design the cheapest validation for each major uncertainty

---

## Output

Write `RUN_DIR/outputs/decision_review.md` using this structure:

```markdown
# Decision Review

## Executive Summary

Confidence: High | Medium | Low

Recommendation: Proceed | Proceed with Validation | Additional Research Required | Reject

## Evidence Quality Review

| Conclusion | Evidence Strength | Notes |
|------------|------------------|-------|

## Hidden Assumptions

| Assumption | Risk | Impact |
|------------|------|--------|

## Missing Perspectives

## Scalability Risks

## Business Risks

### False Positive Risk

### False Negative Risk

## Validation Plan

For each item: objective, expected learning, estimated effort

## Final Recommendation
```

Create `RUN_DIR/outputs/decision_review_complete.marker` as valid JSON per `.clinerules/10-artifact-contracts.md` when done.

---

## Review rules

- Never repeat the synthesis
- Never summarize existing outputs
- Never perform new retrieval/research or introduce uncited signals
- Treat missing Business Context as a gap, not inferred strategic fit
- Always look for weaknesses
- If no weaknesses are found, explain why confidence is high
