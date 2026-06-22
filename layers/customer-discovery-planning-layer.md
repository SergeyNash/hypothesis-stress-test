# Customer Discovery Planning Layer

Customer Discovery Planning is the **research planning layer** after Synthesis and before Decision Review.

It turns unresolved uncertainty into an actionable customer interview plan.

---

## Purpose

This layer answers:

> What do we still need to learn before deciding?

It does not validate hypotheses.

It does not make product or backlog decisions.

---

## Inputs

Required:

- `hypothesis_summary.md`
- `market_analysis.md`
- `hypothesis_map.md`

Optional:

- `validation_questions.md`
- `role_outputs/*`
- `decision_review.md`

Start condition:

- `synthesis_complete.marker`

---

## What this layer produces

| Artifact | Purpose |
|----------|---------|
| `customer_discovery_plan.md` | Practical interview-ready research plan |
| `customer_discovery_planning_complete.marker` | Signals readiness for Decision Review |

---

## Core process

1. Extract critical unknowns from assumptions, weak signals, contradictions, and missing evidence.
2. Classify uncertainty by risk type:
   - Problem Risk
   - Frequency Risk
   - Severity Risk
   - Buyer Risk
   - Adoption Risk
   - Workflow Risk
   - Business Value Risk
   - Strategic Fit Risk
3. Convert unknowns into research objectives.
4. Select interview roles that can provide direct evidence.
5. Build behavior-based interview guide.
6. Prioritize unknowns by decision impact (HIGH / MEDIUM / LOW).
7. Define expected learning outcomes.

---

## Interview rule

Avoid opinion questions such as:

- Would you use this?
- Would you buy this?
- Do you need this feature?

Focus on behavior, workflows, recent events, constraints, and real decisions.

---

## Relationship with other phases

- Facilitator (Roles Layer) -> internal pressure test and interview question seeds
- Market Layer -> external evidence
- Synthesis -> contradiction map and unknowns
- **Customer Discovery Planning** -> customer research plan
- Decision Review -> adversarial critique and recommendation quality gate
- Human -> final backlog decision

