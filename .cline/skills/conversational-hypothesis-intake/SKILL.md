---
name: conversational-hypothesis-intake
description: Collect a product hypothesis through guided chat dialogue, draft input/hypothesis.md, and obtain user confirmation before run bootstrap. Supports trigger tags for ready hypotheses (#hypothesis) and dirty discovery context (#context). Use when the user wants to start a stress test without manually creating RUN_DIR or editing hypothesis files.
---

# Conversational Hypothesis Intake

Collect hypothesis input through chat, produce a canonical `input/hypothesis.md` draft, and obtain explicit user confirmation before any run bootstrap or pipeline execution.

## When to use

- User describes a hypothesis in natural language
- User invokes `/run-hypothesis-conversational.md`
- User pastes dirty discovery notes, Q&A tables, or CustDev context
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
- Always show intake status before confirm (see **Status messages**)

## Intake modes and trigger tags

Detect mode from explicit tags in the user message, or auto-detect from input shape.

### Trigger tags (user places at start of message)

| Tag | Aliases | Mode | Behavior |
| --- | ------- | ---- | -------- |
| `#hypothesis` | `#гипотеза`, `#if-then` | **ready** | User already has a testable statement; minimize questions |
| `#context` | `#контекст`, `#discovery`, `#custdev` | **dirty** | Extract fields from notes, tables, Q&A; validate mapping with user first |
| `#roles` | `#роли` | **roles-only** | User provided roles; collect statement and research context |

Tags are optional. If absent, auto-detect (see below).

### Auto-detect (no tag)

| Input shape | Mode |
| ----------- | ---- |
| Clear `If … then …` (or `Если … то …`) statement | **ready** |
| Q&A table, discovery notes, bullet pain points, long narrative without testable statement | **dirty** |
| Only role names listed | **roles-only** |
| Ambiguous | Ask once: «Это `#гипотеза` (готовая формулировка) или `#контекст` (сырые заметки)?» |

Announce detected mode in chat:

```text
Режим intake: #контекст (dirty discovery)
Mode: #context (dirty discovery)
```

## Dirty input handling (`#context` mode)

Use when input is discovery/CustDev material, not a canonical hypothesis card.

### Detect dirty input

Any of:

- Tab-separated or multi-line Q&A (`Вопрос → Ответ`)
- Sections like «Какую задачу хочет решить клиент?», «Как решает сейчас?», «Чего не хватает?»
- Unstructured narrative without `If … then …`
- Pasted interview or sales notes

### Extraction mapping (dirty → card fields)

| Source pattern (RU / EN) | Target field |
| ------------------------ | ------------ |
| «Какую задачу хочет решить клиент?» / desired outcome / job to be done | Draft `## Statement` (rewrite as If … then …) |
| «Как клиент решает сейчас?» / current workaround | `Known assumptions` or `Scenario` context |
| «Какой функциональности не хватает?» / gap | Refine `## Statement` |
| «Предложения и видение» / proposed solution | `Constraints` or statement refinement |
| «Альтернативы» / alternatives | `Known assumptions` (optional) |
| Named roles in opening line (AppSec, Developer, CISO, …) | `## Relevant Roles` |
| Product domain (SAST, AppSec, …) | `Domain`, `Target audience`, `Scenario` |

### Step 2a — Validate extraction with user (dirty mode only)

Before full draft card, show a short mapping summary:

```text
Я извлёк из контекста:

Statement (черновик):
If [change], then [expected outcome].

Roles: ...
Domain: ...
Target audience: ...
Scenario: ...

Верно? (да / исправить / отмена)
Yes? (yes / revise / cancel)
```

- **да / yes** → proceed to Step 3 (full draft card preview)
- **исправить / revise** → ask what to change; update mapping; repeat Step 2a
- **отмена / cancel** → stop

Do NOT skip this step for dirty input unless the user used `#hypothesis` explicitly.

## Intake flow

### Step 1 — Capture initial intent

Accept the user's first message as the starting point.

1. Check for trigger tags (`#hypothesis`, `#context`, `#roles` and aliases)
2. If no tag, auto-detect mode
3. Extract what is already present: statement, roles, domain, audience, scenario

If mode is **ready** and fields are complete, skip redundant questions.

If mode is **dirty**, run **Step 2a** (validate extraction) before Step 3.

### Step 2 — Guided questions (only for gaps)

Ask short, targeted questions. Maximum one round of 3–5 questions unless validation repair requires more.

Skip fields already extracted in dirty mode after user confirmed mapping.

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

- Intake mode used (`#hypothesis` / `#context` / auto)
- Statement (one line)
- Roles
- Domain / audience / scenario

### Step 4 — Confirm, revise, or cancel

Show status message (mandatory):

```text
Статус: draft готов. runs/ ещё НЕ создан.
Status: draft ready. runs/ NOT created yet.

Подтвердить и запустить / Исправить / Отменить
Confirm and run / Revise / Cancel
```

Match the user's language.

### Confirm triggers (bootstrap only after these)

Treat as explicit confirm:

- `Подтвердить и запустить`, `подтвердить`, `да, запускай`, `запускай`
- `Confirm and run`, `confirm`, `yes, run`, `run it`
- Tag `#confirm` / `#запуск` when user adds it after reviewing draft

Do NOT treat silence, «ок», or continuing the conversation as confirm.

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
- `intake_mode`: `ready` | `dirty` | `roles-only` | `auto`
- `draft_hypothesis_md` — full markdown body (Metadata may still have placeholders)
- `summary` — one-line statement, roles, context

The workflow `run-hypothesis-conversational.md` handles ID assignment, `RUN_DIR` creation, file writes, validation, and pipeline handoff.

## Reference

- `templates/input-schema.md` — canonical input schema
- `.cline/skills/hypothesis-input-validation/SKILL.md` — validation gate
- `.clinerules/workflows/run-hypothesis-conversational.md` — bootstrap and run orchestration
- `examples/chat-first-run.md` — ready and dirty input examples
