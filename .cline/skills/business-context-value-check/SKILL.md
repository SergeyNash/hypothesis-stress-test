---
name: business-context-value-check
description: Map stakeholder value flow, business effect type, and strategic fit from KB strategy materials. Separate problem existence from business case plausibility. Supports digital_product and service_business decisions.
---

## Application profile (resolve before this skill)

Read `Application Profile / Профиль применения` from input Metadata; during intake infer a proposed profile from the requested decision and confirm it in the draft. Missing field means `digital_product`.

For `service_business`, read [service-business profile](../../../profiles/service-business.md), especially **Business context**, and apply its profile-specific rules before the default instructions below. Service-specific fields and criteria override product-only wording; the existing phase order, output paths and markers remain unchanged. Unknown profile is a validation error, not a reason to guess.


# Business Context & Value Check

## Purpose

Answer:

> If this hypothesis is true, how would it create value for the business?

This skill does **not** decide whether to build. It maps the **value mechanism** and **strategic fit** before market and synthesis layers interpret signals.

## What this skill does NOT do

- Does not decide market viability; commissions public evidence collection through `external-business-research` before assessing the value mechanism.
- Does not re-run role analysis
- Does not make final product decisions
- Does not estimate revenue without evidence

## Prerequisites

Required:

- `RUN_DIR/input/hypothesis.md`
- `RUN_DIR/outputs/ready_for_synthesis.marker` with canonical JSON
  `status: completed`
- `RUN_DIR/outputs/knowledge_retrieval_complete.marker` with canonical JSON
  `status: completed`

Recommended:

- `RUN_DIR/outputs/hypothesis_summary.md`
- `RUN_DIR/outputs/role_outputs/*`
- `RUN_DIR/outputs/evidence_inventory.md`

If Local Evidence is missing, stop and ask the user to run
`/run-knowledge-retrieval.md` first.

## KB search paths

Search workspace knowledge base for strategy materials:

- `strategy/`, `okr/`, `business-model/`
- `knowledge-base/strategy/`, `knowledge-base/okr/`, `knowledge-base/business-model/`
- Run-local samples: `kb-samples/strategy/`, `kb-samples/okr/`, `kb-samples/business-model/`

Also scan `evidence_inventory.md` for strategy-related `EVID-NNN` items.

## Step 0 — External evidence brief and collection

Activate `external-business-research` after local-source completeness review, including when internal strategy is missing. Write `outputs/external_research.md` with actual search/read log, source ledger, contradictions and gaps. Passive public research is part of the requested full run unless explicitly excluded; distinguish host approval pending, actual refusal, unavailable tools and no results. Record them in the progress journal and show the user. Preserve internal strategic-fit gaps; external facts cannot fill them.

Search existing workspace folder names in the discovery catalog too; the English KB paths below are examples, not a whitelist. Strategy/development/growth and Russian equivalents can be anywhere.

## Step 1 — Context availability check

For **digital_product**, if strategy, GTM, OKR, or business-model materials are **not found** (service_business uses the profile-specific availability rule):

1. Write `RUN_DIR/outputs/missing_business_context.md` using the gap template below.
2. Write `RUN_DIR/outputs/business_context_complete.marker` with
   `status: skipped_missing_context`.
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

### `missing_business_context.md`

Required sections (EN or RU to match input language):

```markdown
# Missing Business Context

## Missing Source Types
- strategy
- okr
- business-model / GTM

## Searched Paths
- ...

## Impact on Downstream Layers
- Market: proceed with explicit gap; do not infer strategic fit
- Synthesis: Local Optimization Trap / buyer-value analysis unavailable
- Decision Review / Human Report: Decision Readiness may be Needs business context

## What To Add To KB
- ...
```

### `business_context_complete.marker`

Completed analysis:

```json
{
  "status": "completed",
  "completed_phase": "business_context",
  "next_phase": "market",
  "inputs": [
    "outputs/business_context_analysis.md"
  ]
}
```

Gap path:

```json
{
  "status": "skipped_missing_context",
  "completed_phase": "business_context",
  "next_phase": "market",
  "inputs": [
    "outputs/missing_business_context.md"
  ]
}
```

## Review rules

- No evidence → no claim
- Do not invent strategy alignment
- Distinguish user pain from buyer value
- Language matches `input/hypothesis.md`

## Next step

After completion, run skill `hypothesis-market-layer` or workflow `/run-market-layer.md`.

## Service profile context availability

For `service_business`, strategy-document absence alone does not trigger the default stop. Assess usable operational/commercial context as required by the service profile, set Strategic Fit to Unknown when strategy is absent, and write available checks. Use the gap path only when no usable business context exists. Keep customer outcome and provider economics separate. Write the four canonical status fields specified in the artifact contract.

## Evidence quality gate

Read `FRAMEWORK_DIR/implementations/run-quality.md`. Maintain the claim ledger for new protocol-2 runs; preserve source lineage, numerical scope and original intent. Correct upstream errors rather than copying them. Before completion, reconcile claims in this output against actual source anchors. Human Report completion requires `run_control.py finish --run-dir <RUN_DIR>`; PASS from repository examples is not a run check.
