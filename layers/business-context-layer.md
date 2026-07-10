# Business Context & Value Check Layer

This layer answers:

> If the hypothesis is true, how does it create value for the business?

It separates **problem exists** from **business case plausible**.

---

## What this layer does NOT do

- Does not perform market research
- Does not synthesize role and market signals
- Does not make final product decisions
- Does not estimate revenue without evidence

---

## Purpose

Most B2B hypotheses fail not because pain is fake, but because:

- the buyer is not the user
- value does not connect to strategy
- the mechanism from pain to business effect is unclear

This layer builds a **value flow map** before external validation.

<p align="center">
  <img src="../assets/ru/business-value-flow.png" width="760"/>
</p>

---

## Inputs

Required:

- `input/hypothesis.md`
- Roles Layer outputs (`role_outputs/*`, `hypothesis_summary.md`)

Optional:

- `evidence_inventory.md`
- KB strategy materials (`strategy/`, `okr/`, `business-model/`)

## Start conditions

- `ready_for_synthesis.marker`

---

## Business effect types

| Type | Question |
|------|----------|
| **Revenue Driver** | Does this help win or expand revenue? |
| **Retention Driver** | Does this protect or grow existing customers? |
| **Competitive Driver** | Does this differentiate vs named competitors? |
| **Adoption Driver** | Does this increase usage or seat expansion? |
| **Operational Driver** | Does this improve internal efficiency? |

---

## Outputs

| Artifact | Purpose |
|----------|---------|
| `business_context_analysis.md` | Full value map and strategic fit |
| `missing_business_context.md` | Explicit gap when strategy KB is absent |
| `business_context_complete.marker` | Gate for Market Layer |

---

## Place in pipeline

```text
Roles Layer
  ↓
Local Evidence Discovery
  ↓
Business Context & Value Check   ← this layer
  ↓
Market Layer
  ↓
Synthesis
```

Synthesis and Decision Review consume business context to detect **Local Optimization Trap** and **Needs business context** readiness.

---

## Review rules

- No strategy data → `missing_business_context.md`, not fabricated analysis
- User pain ≠ buyer value
- Strategic fit must cite sources

---

## Next

- `templates/business-context-prompt.md` — manual execution
- `.cline/skills/business-context-value-check/SKILL.md` — Cline execution
