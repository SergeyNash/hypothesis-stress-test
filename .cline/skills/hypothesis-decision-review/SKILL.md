---
name: hypothesis-decision-review
description: Critically review synthesized hypothesis conclusions, identify weak signals, hidden assumptions, uncertainty, and propose the lowest-cost validation strategy.
---

# Hypothesis Decision Review

## Purpose

The purpose of this skill is not to re-analyze the hypothesis.

The purpose is to challenge the conclusions already produced by the framework.

This skill acts as an independent reviewer and attempts to identify:

- weak evidence
- overconfidence
- unsupported conclusions
- hidden assumptions
- reasoning gaps
- confirmation bias
- missing validation
- overlooked risks

The goal is to improve decision quality before a hypothesis enters backlog planning or implementation.

## Prerequisites

Required canonical JSON markers:

- `RUN_DIR/outputs/synthesis_complete.marker` with `status: completed`
- `RUN_DIR/outputs/customer_discovery_planning_complete.marker` with
  `status: completed`

Required artifacts:

- `RUN_DIR/outputs/hypothesis_map.md`
- `RUN_DIR/outputs/hypothesis_digest.txt`
- `RUN_DIR/outputs/customer_discovery_plan.md`
- `RUN_DIR/outputs/business_context_analysis.md` **or**
  `RUN_DIR/outputs/missing_business_context.md`

Do not run if Synthesis or Customer Discovery Planning is incomplete.

## Inputs

Required:

- `RUN_DIR/input/hypothesis.md`
- `RUN_DIR/outputs/hypothesis_summary.md`
- `RUN_DIR/outputs/market_analysis.md`
- `RUN_DIR/outputs/hypothesis_map.md`
- `RUN_DIR/outputs/customer_discovery_plan.md`
- `RUN_DIR/outputs/business_context_analysis.md` **or**
  `RUN_DIR/outputs/missing_business_context.md`

Optional:

- `RUN_DIR/outputs/role_outputs/*`
- `RUN_DIR/outputs/hypothesis_digest.txt`
- `RUN_DIR/outputs/evidence_inventory.md`

Do not ingest additional market research or interview notes that are not already in this `RUN_DIR`.

## Core Principle

Assume that the current conclusion may be wrong.

Your task is not to support the recommendation.

Your task is to identify why the recommendation may fail.

Always challenge:

- assumptions
- evidence quality
- applicability
- scalability
- business impact

## Review Process

### Step 1 — Evaluate Evidence Quality

Review all supporting signals.

For every major conclusion determine:

- Is it supported by direct evidence?
- Is it supported by indirect evidence?
- Is it supported only by assumptions?
- Is it supported only by model reasoning?

Classify each signal:

- Strong
- Moderate
- Weak
- Unsupported

### Step 2 — Identify Hidden Assumptions

Find assumptions that must be true for the hypothesis to work.

Examples:

- users have required context
- required data is available
- process maturity exists
- teams behave rationally
- adoption will occur naturally

For each assumption:

- describe it
- explain why it matters
- estimate impact if assumption is false

### Step 3 — Search for Missing Perspectives

Determine:

- which stakeholder groups were not represented
- which business concerns were ignored
- which operational realities were not considered

Examples:

- finance
- procurement
- compliance
- support
- operations
- platform teams

### Step 4 — Evaluate Scalability

Determine whether conclusions remain valid:

- at 10 projects
- at 50 projects
- at 100 projects
- at enterprise scale

Identify:

- operational bottlenecks
- governance risks
- maintenance costs
- coordination overhead

### Step 5 — Evaluate Business Risk

Review:

- revenue impact
- adoption risk
- implementation cost
- opportunity cost

Determine:

- what happens if hypothesis is accepted incorrectly
- what happens if hypothesis is rejected incorrectly

Estimate:

- False Positive Risk
- False Negative Risk

### Step 6 — Challenge the Recommendation

Actively attempt to disprove the current recommendation.

Ask:

- Why might this be wrong?
- What would invalidate this conclusion?
- What evidence would reverse the decision?
- What market condition would make this obsolete?

### Step 7 — Design the Cheapest Validation

For every major uncertainty propose:

- the smallest experiment
- the fastest validation method
- the lowest-cost learning activity

Examples:

- interview
- survey
- telemetry analysis
- prototype
- pilot
- A/B test
- customer workshop

Focus on:

Maximum learning per unit of effort.

## Outputs

### Full review

`RUN_DIR/outputs/decision_review.md`

Language matches `input/hypothesis.md`. Use the English or Russian section set below, not a mix.

### Completion marker

```json
{
  "status": "completed",
  "completed_phase": "decision_review",
  "next_phase": "human_report",
  "inputs": [
    "outputs/decision_review.md"
  ]
}
```

## Recommendation tokens

Store one canonical token and a localized label:

| Token | EN label | RU label |
| ----- | -------- | -------- |
| `proceed` | Proceed | Продолжить |
| `proceed_with_validation` | Proceed with Validation | Продолжить с валидацией |
| `additional_research` | Additional Research Required | Нужно дополнительное исследование |
| `reject` | Reject | Отклонить |

## Output Structure (English)

```markdown
# Decision Review

## Executive Summary

Confidence: High | Medium | Low
Recommendation token: proceed | proceed_with_validation | additional_research | reject
Recommendation: [localized label]

## Evidence Quality Review

| Conclusion | Evidence Strength | Source artifact | Notes |
|------------|------------------|-----------------|-------|

## Hidden Assumptions

| Assumption | Risk | Impact | Source artifact |
|------------|------|--------|-----------------|

## Missing Perspectives
...

## Scalability Risks
...

## Business Risks

### False Positive Risk
...

### False Negative Risk
...

## Validation Plan

- objective
- expected learning
- estimated effort (Low | Medium | High)

## Final Recommendation
...
```

## Структура output (русский)

```markdown
# Decision Review

## Краткое резюме

Уверенность: Высокая | Средняя | Низкая
Токен рекомендации: proceed | proceed_with_validation | additional_research | reject
Рекомендация: Продолжить | Продолжить с валидацией | Нужно дополнительное исследование | Отклонить
```

Remaining Russian sections mirror the English structure: качество evidence, скрытые допущения, отсутствующие перспективы, риски масштабирования, бизнес-риски, план валидации, итоговая рекомендация.

## Review Rules

- Never repeat the synthesis
- Never summarize existing outputs
- Always add new critical thinking
- Always look for weaknesses
- Always assume uncertainty exists
- If no weaknesses are found, explicitly explain why confidence is high
- Do not perform new retrieval, Confluence/external research, market research, or role analysis
- Do not generate new signals or introduce facts not already cited in prior artifacts
- Every factual challenge must remain traceable to an existing artifact and its cited evidence
- Missing evidence is a gap to report, not permission to fill it

## Reference

Based on `templates/decision-review-prompt.md`, `layers/decision-review-layer.md`, and `.clinerules/20-evidence-rules.md`.
