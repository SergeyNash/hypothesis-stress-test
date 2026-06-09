# Decision Review Prompt

This is an execution template, not a system prompt.

RUN_DIR: [set your run directory]

---

## Prerequisites

Synthesis must be complete. Read:

- `hypothesis.md`
- `outputs/hypothesis_summary.md`
- `outputs/market_analysis.md`
- `outputs/hypothesis_map.md`
- `outputs/hypothesis_digest.txt` (optional)
- `outputs/role_outputs/*` (optional)

---

## Core principle

Assume the current conclusion may be wrong.

Do not support the recommendation. Identify why it may fail.

Do NOT repeat or summarize synthesis outputs. Add new critical thinking only.

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

Create `RUN_DIR/outputs/decision_review_complete.marker` when done.

---

## Review rules

- Never repeat the synthesis
- Never summarize existing outputs
- Always look for weaknesses
- If no weaknesses are found, explain why confidence is high
