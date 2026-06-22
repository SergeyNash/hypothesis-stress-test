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

Read `RUN_DIR/outputs/synthesis_complete.marker` or confirm synthesis artifacts exist:

- `RUN_DIR/outputs/hypothesis_map.md`
- `RUN_DIR/outputs/hypothesis_digest.txt`

Do not run if Synthesis outputs are missing. Ask user to complete Synthesis first.

## Inputs

Required:

- `RUN_DIR/input/hypothesis.md`
- `RUN_DIR/outputs/hypothesis_summary.md`
- `RUN_DIR/outputs/market_analysis.md`
- `RUN_DIR/outputs/hypothesis_map.md`

Optional:

- `RUN_DIR/outputs/role_outputs/*`
- `RUN_DIR/outputs/hypothesis_digest.txt`
- additional market research
- interview notes

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

### Completion marker

`RUN_DIR/outputs/decision_review_complete.marker`

## Output Structure

```markdown
# Decision Review

## Executive Summary

Short assessment of confidence level.

Confidence:

- High
- Medium
- Low

Recommendation:

- Proceed
- Proceed with Validation
- Additional Research Required
- Reject

## Evidence Quality Review

| Conclusion | Evidence Strength | Notes |
|------------|------------------|-------|

## Hidden Assumptions

| Assumption | Risk | Impact |
|------------|------|--------|

## Missing Perspectives

List stakeholder groups or viewpoints not sufficiently represented.

## Scalability Risks

List scalability concerns and boundary conditions.

## Business Risks

### False Positive Risk

What happens if we implement this and we are wrong?

### False Negative Risk

What happens if we reject this and we are wrong?

## Validation Plan

List the cheapest and fastest ways to reduce uncertainty.

For each item include:

- objective
- expected learning
- estimated effort

## Final Recommendation

Provide a final recommendation.

Always explain:

- why confidence is high or low
- what evidence is still missing
- what should happen next
```

## Review Rules

Never repeat the synthesis.

Never summarize existing outputs.

Always add new critical thinking.

Always look for weaknesses.

Always assume uncertainty exists.

If no weaknesses are found, explicitly explain why confidence is high.

## Reference

Based on `templates/decision-review-prompt.md` and `layers/decision-review-layer.md`.
