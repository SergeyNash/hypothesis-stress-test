---
name: business-context-value-check
description: Map stakeholder value flow, business effect type, and strategic fit from KB strategy materials. Separate problem existence from business case plausibility.
---

# Business Context & Value Check

## Purpose

Answer:

> If this hypothesis is true, how would it create value for the business?

This skill does **not** decide whether to build. It maps the **value mechanism** and **strategic fit** before market and synthesis layers interpret signals.

## What this skill does NOT do

- Does not perform market research
- Does not re-run role analysis
- Does not make final product decisions
- Does not estimate revenue without evidence

## Prerequisites

Required:

- `RUN_DIR/input/hypothesis.md`
- `RUN_DIR/outputs/ready_for_synthesis.marker` (Roles Layer complete)

Recommended:

- `RUN_DIR/outputs/hypothesis_summary.md`
- `RUN_DIR/outputs/role_outputs/*`
- `RUN_DIR/outputs/evidence_inventory.md`

## KB search paths

Search workspace knowledge base for strategy materials:

- `strategy/`, `okr/`, `business-model/`
- `knowledge-base/strategy/`, `knowledge-base/okr/`, `knowledge-base/business-model/`
- Run-local samples: `kb-samples/strategy/`, `kb-samples/okr/`, `kb-samples/business-model/`

Also scan `evidence_inventory.md` for strategy-related `EVID-NNN` items.

## Step 1 — Context availability check

If strategy, GTM, OKR, or business-model materials are **not found**:

1. Write `RUN_DIR/outputs/missing_business_context.md` listing missing sources and what to add.
2. Write `RUN_DIR/outputs/business_context_complete.marker` with note `analysis_skipped_missing_context`.
3. **Stop** — do not invent business context.

If materials exist, proceed to Step 2.

## Step 2 — Stakeholder map

Build value-chain roles from hypothesis roles + KB strategy:

```text
Problem → Beneficiary → Behavior change → Business effect
```

For each link identify:

- Who experiences pain?
- Who receives value?
- Who decides?
- Who pays?
- Who implements?
- Who may block?

## Step 3 — Value mechanism

Classify primary business effect type (one or more):

- **Revenue Driver** — wins deals, expands ARR
- **Retention Driver** — reduces churn, increases renewal
- **Competitive Driver** — differentiation vs named competitors
- **Adoption Driver** — increases usage, activation, seat expansion
- **Operational Driver** — internal efficiency, cost reduction

State mechanism in plain language. No revenue numbers without evidence.

## Step 4 — Strategic fit

Compare hypothesis to available strategy/OKR/GTM:

- Does this advance stated priorities?
- Does it help win target segment?
- Strategic fit: High / Medium / Low / Unknown

Cite sources (file paths or EVID-NNN).

## Step 5 — Risks and opportunities

Document:

- buyer vs user gap
- value mechanism gaps
- strategic misalignment risks
- opportunities if reframed

## Output artifacts

### `business_context_analysis.md`

Required sections:

```markdown
# Business Context Analysis

## Available Context
...

## Missing Context
...

## Stakeholder Map
...

## Value Flow
Problem → Beneficiary → Behavior change → Business effect

## Business Effect Type
- [type] — rationale

## Strategic Fit
...

## Key Risks
...

## Key Opportunities
...

## Summary for Downstream Layers
...
```

### `business_context_complete.marker`

```text
Business context analysis completed.
Ready for Market Layer.
```

Or if skipped:

```text
Business context analysis skipped.
missing_business_context.md created.
Ready for Market Layer with explicit gap.
```

## Review rules

- No evidence → no claim
- Do not invent strategy alignment
- Distinguish user pain from buyer value
- Language matches `input/hypothesis.md`

## Next step

After completion, run skill `hypothesis-market-layer` or workflow `/run-market-layer.md`.
