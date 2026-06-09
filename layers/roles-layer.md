# Roles Layer (Facilitator / Hypothesis Stress Test)

The Roles Layer provides an **internal stress-test** of a hypothesis through role-based analysis.

Also known as the **facilitator phase** or **Hypothesis Stress Test** in the pipeline.

---

## What this layer does NOT do

- Does not make decisions
- Does not research the market
- Does not synthesize conclusions
- Does not design experiments

---

## Purpose

The goal is not to validate the hypothesis.

The goal is to:

- expose the hypothesis
- find weak points
- surface hidden assumptions
- show role conflicts
- define applicability boundaries

> Where this hypothesis creates value — and where it breaks.

---

## Persona

An experienced B2B product facilitator acting as an intellectual opponent — not supporting ideas, but expanding the author's perspective before development.

---

## What it does

The layer analyzes the hypothesis through **relevant roles** from `hypothesis.md`.

Each role represents a real perspective (user, developer, security, operations, etc.).

---

## Analysis process

1. **Extract hidden assumptions** — before role analysis
2. **Define applicability boundaries** — value / no value / harmful / alternatives
3. **Role analysis** — pain, new problems, alternatives, failure context per role
4. **Conflict detection** — agreement, tension, conflict zones, blind spots
5. **Validation questions** — behavior-based interview questions (no leading questions)
6. **Hypothesis assessment** — promising / uncertain / risky — no implementation recommendation

---

## Core questions per role

### Pain

Priority: CRITICAL / SECONDARY / DOES NOT ADDRESS PAIN

### New problems

Operational friction, governance, maintenance, adoption friction

### Alternatives

Including doing nothing

### Failure context

When useless, harmful, or irrelevant

### Applicability boundaries

Works when / does not work when / harms when

---

## Validation questions rules

**Allowed:** behavior-based (how you currently solve, walk me through the last time…)

**Forbidden:** Would you use this? / Do you need this? / Would you buy it?

---

## Output language

Artifacts match the language of `hypothesis.md`.

---

## Output

| Artifact | Purpose |
|----------|---------|
| `role_outputs/{role_slug}.md` | Per-role analysis |
| `hypothesis_summary.md` | Assumptions, boundaries, conflicts, assessment |
| `validation_questions.md` | Interview questions per role |
| `ready_for_synthesis.marker` | Phase complete, ready for Market Layer |

---

## What it does NOT do (constraints)

* does not confirm the hypothesis
* does not consider market reality
* does not generate solutions
* does not replace user research

---

## Relationship with other layers

* Market Layer (Market Reality Check) → validates external reality
* Synthesis Layer → compares signals
* Decision Review → challenges synthesis conclusions

Roles Layer alone is insufficient.

---

## Key principle

> Internal logic is not reality.

The Roles Layer defines how the hypothesis *should* work — not whether it actually does.

---

## Next

* `market-layer.md`
* `synthesis-layer.md`
* `templates/facilitator-prompt.md` — manual execution
* `.cline/skills/hypothesis-facilitator/SKILL.md` — Cline execution
