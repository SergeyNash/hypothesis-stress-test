# Run Hypothesis (Conversational / Chat-First)

Start a full hypothesis stress test from chat dialogue. The user does not need to create `RUN_DIR` or edit `input/hypothesis.md` manually.

**Primary entry point for new hypotheses.** File-first workflow remains available via `/run-hypothesis.md`.

## Steps

### 0. Detect intake mode (optional tags)

Before collecting input, check the user message for trigger tags:

| Tag | Mode |
| --- | ---- |
| `#hypothesis`, `#гипотеза`, `#if-then` | Ready statement — fast path |
| `#context`, `#контекст`, `#discovery`, `#custdev` | Dirty discovery notes — extract + validate mapping |
| `#roles`, `#роли` | Roles provided — collect statement and context |

If no tag and input looks like Q&A table or discovery notes without `If … then …`, treat as **dirty** mode.

If ambiguous, ask once: «`#гипотеза` (готовая формулировка) или `#контекст` (сырые заметки)?»

Announce mode to the user before intake continues.

### 1. Conversational intake

Activate skill `conversational-hypothesis-intake`.

- Accept the user's hypothesis in natural language (or continue from an in-progress intake)
- Apply intake mode (ready / dirty / roles-only)
- For **dirty** input: extract fields, validate mapping with user, then build draft
- Collect missing fields through guided questions (only gaps)
- Show draft `input/hypothesis.md` preview
- Show status: `runs/ NOT created yet`
- Wait for explicit user confirmation (`Confirm and run` / `Подтвердить и запустить` / `#запуск`)

Stop if the user cancels.

### 2. Bootstrap RUN_DIR

After confirmation, create the run archive automatically.

#### ID generation

1. Use today's date: `YYYY-MM-DD` (workspace local date)
2. List existing directories under `runs/` matching `HYP-YYYY-MM-DD-*`
3. Pick the next available suffix `NNN` (001, 002, …) for today
4. Assign:
   - `Hypothesis ID`: `HYP-YYYY-MM-DD-NNN`
   - `Run ID`: `RUN-YYYY-MM-DD-NNN`
   - `Created at`: `YYYY-MM-DD`
   - `Status`: `draft` (update to `running` when pipeline starts)

#### Directory creation

```text
runs/HYP-YYYY-MM-DD-NNN/
  input/
    hypothesis.md
    attachments/
  run.md
  outputs/
```

Write `input/hypothesis.md` using the confirmed draft with final Metadata values filled in.

Folder name MUST match `Hypothesis ID` in metadata.

#### run.md stub

Write a minimal `run.md` log:

```markdown
# Run

## Execution Mode

**Primary:** Conversational (chat-first) via `/run-hypothesis-conversational.md`

## Input

Created from conversational intake on [date].
Intake mode: [ready | dirty | roles-only | auto]

## Pipeline

Started automatically after intake confirmation and input validation.
```

Set `RUN_DIR` to `runs/HYP-YYYY-MM-DD-NNN` for all subsequent steps.

Tell the user which `RUN_DIR` was created.

### 3. Validate input

Invoke `/validate-hypothesis-input.md` or skill `hypothesis-input-validation` against the new `RUN_DIR`.

If validation fails:

- Activate skill `conversational-hypothesis-intake` in repair mode
- Update `input/hypothesis.md` after user confirms revised draft
- Re-run validation
- Repeat until validation passes or user cancels

Do NOT start the pipeline on invalid input.

### 4. Run full pipeline

When validation passes:

1. Update `Status` in `input/hypothesis.md` to `running` if still `draft`
2. Invoke `/run-hypothesis.md` with the bootstrapped `RUN_DIR`

The conversational workflow does not duplicate layer logic — it delegates to the existing end-to-end workflow.

### 5. Report

After pipeline completes, display:

- `RUN_DIR` path
- `outputs/hypothesis_digest.txt`
- Key verdict from `outputs/decision_review.md`
- Reminder: human makes the final backlog decision

## User trigger examples

**Ready hypothesis (`#hypothesis` optional):**

```text
/run-hypothesis-conversational.md

If AppSec engineers can manually prioritize SAST queue items, critical apps get scanned first.
```

**Dirty discovery context:**

```text
/run-hypothesis-conversational.md
#контекст

Моя гипотеза для AppSec инженеров, разработчиков и CISO:
Какую задачу хочет решить клиент? Группировка проектов сканирования с общими параметрами (API + UI).
Как клиент решает сейчас? Вручную переключает проекты.
Чего не хватает? Группировка + настраиваемая ролевая модель.
```

Agent extracts fields, shows mapping for confirmation, then draft card, then waits for `Подтвердить и запустить`.

**Minimal start:**

```text
/run-hypothesis-conversational.md
```

(Then answer guided questions or use `#контекст` + paste notes.)

## Fallback

Users who prefer file-first workflow:

```text
RUN_DIR: runs/HYP-2026-06-22-001
/run-hypothesis.md
```

## Do not

- Skip the confirmation step before bootstrap
- Create `runs/` before user confirms draft
- Treat «ок» or continued chat as confirmation
- Start pipeline before validation passes
- Change downstream artifact contracts or layer skills

## Reference

- Skill: `conversational-hypothesis-intake`
- Schema: `templates/input-schema.md`
- Examples: `examples/chat-first-run.md`
- Full pipeline: `run-hypothesis.md`
- Playbook: `playbooks/run-hypothesis.md`
