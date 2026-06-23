---
name: conversational-hypothesis-intake
description: Collect a product hypothesis through guided chat dialogue, draft input/hypothesis.md, and obtain user confirmation before run bootstrap. Use when the user wants to start a stress test without manually creating RUN_DIR or editing hypothesis files.
---

# Conversational Hypothesis Intake

Collect hypothesis input through chat, produce a canonical `input/hypothesis.md` draft, and obtain explicit user confirmation before any run bootstrap or pipeline execution.

## When to use

- User describes a hypothesis in natural language
- User invokes `/run-hypothesis-conversational.md`
- User wants to avoid manual `RUN_DIR` setup and file editing
- Validation failed and targeted repair is needed for specific sections

## When NOT to use

- User already provided a valid `RUN_DIR` with `input/hypothesis.md` — use `/validate-hypothesis-input.md` or `/run-hypothesis.md` instead
- User explicitly wants file-first workflow

## Core rules

- Do NOT create `RUN_DIR` or write files until the user confirms the draft card
- Do NOT invoke `/run-hypothesis.md` until bootstrap is complete and validation passes
- Draft markdown MUST follow `templates/input-schema.md` and `.clinerules/10-artifact-contracts.md`
- Use English section headings (`## Metadata`, `## Statement`, etc.) even when body text is Russian
- Metadata IDs are placeholders until bootstrap assigns final values

## Intake flow

### Step 1 — Capture initial intent

Accept the user's first message as the starting point. Extract what is already present:

- hypothesis statement (even if rough)
- affected roles
- domain, audience, scenario

If the first message is rich enough, skip redundant questions.

### Step 2 — Guided questions (only for gaps)

Ask short, targeted questions. Maximum one round of 3–5 questions unless validation repair requires more.

| Field | Question prompt (adapt to context) |
| ----- | ---------------------------------- |
| Statement | What change are you proposing, and what outcome do you expect? |
| Relevant Roles | Who is directly affected or involved in the decision? (2–4 roles preferred) |
| Domain | What product/domain area does this belong to? |
| Target audience | Who is the primary audience or customer segment? |
| Scenario | In what situation does this problem or opportunity occur? |
| Constraints (optional) | Any technical, organizational, or timeline constraints? |
| Known assumptions (optional) | What are you assuming to be true? |
| Owner (optional) | Who owns this hypothesis? |

Quality bar (same as `hypothesis-input-validation`):

- Statement must be specific and testable — reject vague goals like "improve UX"
- At least one role, directly impacted
- Scenario must be concrete enough for market validation
- Flag if more than 5 roles (noise risk)

### Step 3 — Draft card preview

Render the full canonical markdown draft in chat. Use this structure:

```markdown
# Hypothesis

## Metadata

- Hypothesis ID: (assigned at bootstrap)
- Created at: (assigned at bootstrap)
- Run ID: (assigned at bootstrap)
- Status: draft

## Statement

[testable statement — prefer "If … then …" form]

## Relevant Roles

- [role 1]
- [role 2]

## Research Context

- Domain: [domain]
- Target audience: [audience]
- Scenario: [scenario]
- Constraints: [optional]
- Known assumptions: [optional]
- Owner: [optional]
```

Omit optional Research Context lines when not provided.

Show a short human summary before the draft:

- Statement (one line)
- Roles
- Domain / audience / scenario

### Step 4 — Confirm, revise, or cancel

Ask explicitly:

```text
Подтвердить и запустить / Исправить / Отменить
Confirm and run / Revise / Cancel
```

Match the user's language.

| Response | Action |
| -------- | ------ |
| Confirm | Return confirmed draft to workflow for bootstrap (do not write files in this skill) |
| Revise | Ask what to change; update draft; show preview again; repeat Step 4 |
| Cancel | Stop; do not bootstrap or run |

Do NOT proceed past this step without explicit confirmation.

## Field mapping (chat → hypothesis.md)

| Chat input | Target section | Required |
| ---------- | -------------- | -------- |
| Hypothesis idea / statement | `## Statement` | yes |
| Roles list | `## Relevant Roles` | yes (≥1) |
| Domain | `Research Context` → `Domain:` | yes |
| Target audience | `Research Context` → `Target audience:` | yes |
| Scenario | `Research Context` → `Scenario:` | yes |
| Constraints | `Research Context` → `Constraints:` | no |
| Assumptions | `Research Context` → `Known assumptions:` | no |
| Owner | `Research Context` → `Owner:` | no |

## Validation repair loop

When invoked after failed validation:

1. Read validation feedback (which sections failed and why)
2. Ask only about failing sections — do not re-ask for valid fields
3. Update draft preview
4. Return to Step 4 (confirm / revise / cancel)

## Output to workflow

On confirmation, provide:

- `confirmed: true`
- `draft_hypothesis_md` — full markdown body (Metadata may still have placeholders)
- `summary` — one-line statement, roles, context

The workflow `run-hypothesis-conversational.md` handles ID assignment, `RUN_DIR` creation, file writes, validation, and pipeline handoff.

## Reference

- `templates/input-schema.md` — canonical input schema
- `.cline/skills/hypothesis-input-validation/SKILL.md` — validation gate
- `.clinerules/workflows/run-hypothesis-conversational.md` — bootstrap and run orchestration
