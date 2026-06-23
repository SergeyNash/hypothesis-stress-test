---
name: conversational-hypothesis-intake
description: Collect a product hypothesis through guided chat dialogue, draft input/hypothesis.md, propose a new RUN_DIR in dialog, and obtain user confirmation before bootstrap. Supports trigger tags (#hypothesis, #context, #new-run). Use when starting a new stress test without manually creating RUN_DIR.
---

# Conversational Hypothesis Intake

Collect hypothesis input through chat, produce a canonical `input/hypothesis.md` draft, propose a **new** `runs/HYP-*-NNN/` in dialog, and obtain explicit user confirmation before any file writes or pipeline execution.

## When to use

- User describes a hypothesis in natural language
- User invokes `/run-hypothesis-conversational.md` **without** `RUN_DIR:` (new hypothesis)
- User pastes dirty discovery notes, Q&A tables, or CustDev context
- User wants to avoid manual `RUN_DIR` setup and file editing
- Validation failed and targeted repair is needed for specific sections

## When NOT to use

- User provided `RUN_DIR: runs/HYP-...` in the same message — use **continue existing run** path in workflow (validate + pipeline), not new intake
- User already has a valid `input/hypothesis.md` and only wants to re-run layers — use `/run-hypothesis.md`
- User explicitly wants file-first workflow

## Core rules

### New run isolation

- `/run-hypothesis-conversational` **without** `RUN_DIR:` = always a **new** hypothesis archive
- Auto-apply `#new-run` semantics even if the tag is omitted
- Do NOT write to an existing `runs/HYP-*` folder unless the user explicitly provided `RUN_DIR:` to continue that run
- Open files or tabs from a previous run are **read-only context** — never the write target for a new hypothesis
- If `runs/HYP-YYYY-MM-DD-001` exists and the user starts a new hypothesis the same day, propose `002` (next free suffix) — do not reuse `001`

### Two-step confirm

1. **Step 4a** — confirm hypothesis draft card
2. **Step 4b** — confirm proposed new `RUN_DIR` (dialog)

Do NOT create `RUN_DIR` or write any files until **both** steps pass.

### Other rules

- Do NOT invoke `/run-hypothesis.md` until bootstrap is complete and validation passes
- Draft markdown MUST follow `templates/input-schema.md` and `.clinerules/10-artifact-contracts.md`
- Use English section headings (`## Metadata`, `## Statement`, etc.) even when body text is Russian
- Metadata IDs are placeholders until bootstrap assigns final values after Step 4b
- Always show intake status before each confirm step (see **Status messages**)

### Artifact allowlist

During conversational intake and bootstrap, write **only** files defined in `.clinerules/10-artifact-contracts.md`.

Forbidden examples: `product_specification.md`, `implementation_plan.md`, or any ad-hoc analysis doc under `runs/`.

Do NOT run ad-hoc multi-step analysis plans instead of the intake flow.

## Intake modes and trigger tags

Detect mode from explicit tags in the user message, or auto-detect from input shape.

### Trigger tags (user places at start of message)

| Tag | Aliases | Mode / intent | Behavior |
| --- | ------- | ------------- | -------- |
| `#hypothesis` | `#гипотеза`, `#if-then` | **ready** | User already has a testable statement; minimize questions |
| `#context` | `#контекст`, `#discovery`, `#custdev` | **dirty** | Extract fields from notes, tables, Q&A; validate mapping with user first |
| `#roles` | `#роли` | **roles-only** | User provided roles; collect statement and research context |
| `#new-run` | `#новая`, `#новый-прогон` | **new archive** | Explicit: do not reuse any existing `RUN_DIR` |

`#new-run` is implied when `/run-hypothesis-conversational` is invoked without `RUN_DIR:`.

Tags are optional except new-run semantics (always on for new hypothesis).

### Auto-detect (no tag)

| Input shape | Mode |
| ----------- | ---- |
| Clear `If … then …` (or `Если … то …`) statement | **ready** |
| Q&A table, discovery notes, bullet pain points, long narrative without testable statement | **dirty** |
| Only role names listed | **roles-only** |
| Ambiguous | Ask once: «Это `#гипотеза` (готовая формулировка) или `#контекст` (сырые заметки)?» |

Announce detected mode in chat:

```text
Режим intake: #контекст (dirty discovery), новый прогон (#new-run)
Mode: #context (dirty discovery), new run (#new-run)
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

1. If message contains `RUN_DIR: runs/HYP-...` → stop intake; hand off to workflow **continue existing run**
2. Check for trigger tags (`#hypothesis`, `#context`, `#roles`, `#new-run` and aliases)
3. If no intake tag, auto-detect mode
4. Extract what is already present: statement, roles, domain, audience, scenario

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
- New run (`#new-run` implied)
- Statement (one line)
- Roles
- Domain / audience / scenario

### Step 4a — Confirm hypothesis draft

Show status message (mandatory):

```text
Статус: draft готов. runs/ ещё НЕ создан.
Status: draft ready. runs/ NOT created yet.

Подтвердить карточку / Исправить / Отменить
Confirm draft / Revise / Cancel
```

Match the user's language.

| Response | Action |
| -------- | ------ |
| Confirm draft | Proceed to Step 4b (RUN_DIR dialog) |
| Revise | Ask what to change; update draft; show preview again; repeat Step 4a |
| Cancel | Stop; do not propose RUN_DIR or bootstrap |

Do NOT treat silence, «ок», or continuing the conversation as confirm.

### Step 4b — RUN_DIR dialog (new archive)

After Step 4a confirm only:

1. Scan `runs/` for directories matching `HYP-YYYY-MM-DD-*` (today's date)
2. List existing runs for transparency (read-only)
3. Propose the **next available** suffix `NNN` (e.g. `002` if `001` exists)
4. Show dialog:

```text
Создам новый прогон:
  RUN_DIR: runs/HYP-2026-06-23-002

Сегодня уже есть:
  - runs/HYP-2026-06-23-001 (не трогаю)

Подтвердить создание 002 / Указать другой ID / Отмена
Confirm create 002 / Specify other ID / Cancel
```

Rules:

- Never propose reusing an existing folder for a new hypothesis
- User may override: «используй 003» — verify suffix is free, then confirm
- If proposed path already exists, pick next free suffix and explain

### RUN_DIR confirm triggers (bootstrap only after these)

- `Подтвердить создание`, `да, создай`, `создай 002`
- `Confirm create`, `yes, create`, `create 002`
- Tag `#запуск` / `#confirm` after reviewing proposed `RUN_DIR`

| Response | Action |
| -------- | ------ |
| Confirm RUN_DIR | Return confirmed draft + `proposed_rundir` to workflow for bootstrap |
| Specify other ID | Validate free suffix; re-show dialog; repeat Step 4b |
| Cancel | Stop; do not bootstrap or run |

Do NOT write any files in this skill — workflow executes bootstrap after Step 4b.

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
4. Return to Step 4a (confirm draft), then Step 4b if RUN_DIR not yet confirmed

## Output to workflow

After Step 4b confirm, provide:

- `confirmed: true`
- `draft_confirmed: true`
- `rundir_confirmed: true`
- `proposed_rundir`: `runs/HYP-YYYY-MM-DD-NNN`
- `intake_mode`: `ready` | `dirty` | `roles-only` | `auto`
- `draft_hypothesis_md` — full markdown body (Metadata placeholders filled at bootstrap)
- `summary` — one-line statement, roles, context

The workflow `run-hypothesis-conversational.md` creates files only after receiving `rundir_confirmed`.

## Reference

- `templates/input-schema.md` — canonical input schema
- `.cline/skills/hypothesis-input-validation/SKILL.md` — validation gate
- `.clinerules/workflows/run-hypothesis-conversational.md` — bootstrap and run orchestration
- `examples/chat-first-run.md` — ready, dirty, and second-run-same-day examples
