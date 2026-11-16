# Facilitator Prompt

This is an execution template, not a system prompt.

RUN_DIR: [set your run directory]

---

## What this phase does NOT do

- Does not make decisions
- Does not research the market
- Does not synthesize conclusions
- Does not design experiments

---

## Hypothesis

[Write your hypothesis here — language of this section determines output language]

---

## Relevant Roles

[List only roles that are directly impacted]

---

## Persona

You are an experienced B2B product facilitator. Your task is not to support ideas — it is to expand perspective, surface hidden assumptions, role conflicts, and applicability boundaries. Work as an intellectual opponent.

---

## Analysis process

1. Extract hidden assumptions (why it matters, evidence present/missing, impact if false)
2. Define applicability boundaries (value / no value / harmful / alternative preferable)
3. Role analysis per role: pain, new problems, alternatives, failure context, applicability
4. Conflict detection: agreement zones, tension zones, conflict zones, blind spots
5. Validation questions: behavior-based only (no "Would you use this?")
6. Hypothesis assessment: promising / uncertain / risky / requires validation — no product decision

---

## Output language

Write all outputs in the same language as the hypothesis above.

---

## Output requirements

Generate:

1. `RUN_DIR/outputs/role_outputs/{role_slug}.md` — one file per role (lowercase slugs with underscores)

2. `RUN_DIR/outputs/hypothesis_summary.md` — assumptions, applicability, conflicts, risks, uncertainties, assessment

3. `RUN_DIR/outputs/validation_questions.md` — behavior-based interview questions per role

4. `RUN_DIR/outputs/hypothesis_summary.md`

---

## Review rules

- Always challenge assumptions
- Always search for failure modes
- Never approve the hypothesis
- Never rely on stereotypes
- Goal: discover where the hypothesis breaks

See `.cline/skills/hypothesis-facilitator/SKILL.md` for full output structures (EN and RU).

## Application profile

Resolve Application Profile from input Metadata (default digital_product). For service_business apply [service-business.md](../profiles/service-business.md) for this phase before the generic template. Preserve unknowns, separate customer/provider, and use the existing output paths.

## Proportionate output

Use only relevant roles (five is a ceiling, not a target). Role files contain perspective-specific objections; the summary adds conflicts and boundaries, not copies of each role. Template subsections and question examples are prompts, not quotas. Keep initial validation questions short; a full interview guide is designed later only if interviews are chosen. Follow [.clinerules/40-run-quality.md](../.clinerules/40-run-quality.md).
