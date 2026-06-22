# Customer Discovery Planning Prompt

This is an execution template, not a system prompt.

RUN_DIR: [set your run directory]

---

## Prerequisites

Synthesis must be complete. Read:

- `input/hypothesis.md`
- `outputs/hypothesis_summary.md`
- `outputs/market_analysis.md`
- `outputs/hypothesis_map.md`
- `outputs/validation_questions.md` (optional)
- `outputs/role_outputs/*` (optional)
- `outputs/decision_review.md` (optional)

---

## Core principle

The goal is not:

`What should we build?`

The goal is:

`What do we still need to learn before deciding?`

Do not validate the hypothesis.

Do not make product decisions.

---

## Task

1. Extract unknowns from assumptions without evidence, weak signals, contradictions, and unresolved questions.
2. Classify every unknown by risk type: Problem, Frequency, Severity, Buyer, Adoption, Workflow, Business Value, Strategic Fit.
3. Convert unknowns into research objectives (learning goals, not "validate hypothesis").
4. Recommend interview participant roles and expected evidence from each role.
5. Build behavior-based interview guide sections:
   - Current Workflow
   - Recent Experience
   - Consequences
   - Alternatives
   - Decision-Making Process
6. Prioritize unknowns by decision impact (HIGH / MEDIUM / LOW).
7. Define expected learning outcomes.

Forbidden question types:

- Would you use this?
- Would you buy this?
- Do you need this feature?

---

## Output

Write `RUN_DIR/outputs/customer_discovery_plan.md` using this structure:

```markdown
# Customer Discovery Plan

## Research Objective

---

## What We Already Know

---

## Critical Unknowns

| Unknown | Risk Type | Priority |
|----------|------------|----------|

---

## Recommended Interview Roles

---

## Interview Guide

### Current Workflow

### Recent Experience

### Consequences

### Alternatives

### Decision-Making Process

---

## Research Priorities

### High Priority

### Medium Priority

### Low Priority

---

## Expected Learning Outcomes
```

Create `RUN_DIR/outputs/customer_discovery_planning_complete.marker` when done.

