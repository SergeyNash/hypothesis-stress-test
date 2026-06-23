# Run Hypothesis (Conversational / Chat-First)

Start a full hypothesis stress test from chat dialogue. The user does not need to create `RUN_DIR` or edit `input/hypothesis.md` manually.

**Primary entry point for new hypotheses.** File-first workflow remains available via `/run-hypothesis.md`.

## Steps

### 0. Route: new run vs continue existing

Check the user message first:

| Condition | Path |
| --------- | ---- |
| Message contains `RUN_DIR: runs/HYP-...` | **Continue existing run** — skip intake; validate `input/hypothesis.md`; invoke `/run-hypothesis.md` if valid |
| No `RUN_DIR:` in message | **New hypothesis** — full intake + dialog bootstrap (Steps 0b–5) |

For **new hypothesis**, auto-apply `#new-run` semantics: never reuse an existing archive from open tabs or prior context.

### 0b. Detect intake mode (optional tags)

Before collecting input, check trigger tags:

| Tag | Mode |
| --- | ---- |
| `#hypothesis`, `#гипотеза`, `#if-then` | Ready statement — fast path |
| `#context`, `#контекст`, `#discovery`, `#custdev` | Dirty discovery notes — extract + validate mapping |
| `#roles`, `#роли` | Roles provided — collect statement and context |
| `#new-run`, `#новая`, `#новый-прогон` | Explicit new archive (also implied when no `RUN_DIR:`) |

If no tag and input looks like Q&A table or discovery notes without `If … then …`, treat as **dirty** mode.

Announce mode to the user before intake continues.

### 1. Conversational intake

Activate skill `conversational-hypothesis-intake`.

- Accept the user's hypothesis in natural language (or continue from an in-progress intake)
- Apply intake mode (ready / dirty / roles-only)
- For **dirty** input: extract fields, validate mapping with user, then build draft
- Collect missing fields through guided questions (only gaps)
- Show draft `input/hypothesis.md` preview
- **Step 4a:** wait for hypothesis draft confirm (`Confirm draft` / `Подтвердить карточку`)
- **Step 4b:** propose new `RUN_DIR`, list existing runs today, wait for RUN_DIR confirm (`Confirm create` / `Подтвердить создание`)

Stop if the user cancels at any step.

Do NOT write files until Step 4b completes.

### 2. Bootstrap RUN_DIR

Execute **only after** intake returns `rundir_confirmed: true` and `proposed_rundir`.

Use the user-confirmed path from intake (e.g. `runs/HYP-2026-06-23-002`).

#### ID assignment

Fill Metadata in `input/hypothesis.md` from confirmed `proposed_rundir`:

- `Hypothesis ID` = folder name (e.g. `HYP-2026-06-23-002`)
- `Run ID` = `RUN-YYYY-MM-DD-NNN` (same date and suffix)
- `Created at` = today's date
- `Status` = `draft` (update to `running` when pipeline starts)

#### Directory creation

```text
runs/HYP-YYYY-MM-DD-NNN/
  input/
    hypothesis.md
    attachments/
  run.md
  outputs/
```

Write `input/hypothesis.md` using the confirmed draft with final Metadata values.

Folder name MUST match `Hypothesis ID` in metadata.

#### run.md stub

```markdown
# Run

## Execution Mode

**Primary:** Conversational (chat-first) via `/run-hypothesis-conversational.md`

## Input

Created from conversational intake on [date].
Intake mode: [ready | dirty | roles-only | auto]
RUN_DIR confirmed via dialog: runs/HYP-YYYY-MM-DD-NNN

## Pipeline

Started automatically after RUN_DIR bootstrap and input validation.
```

Set `RUN_DIR` for all subsequent steps. Tell the user which `RUN_DIR` was created.

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

## Continue existing run (when `RUN_DIR:` provided)

If the user message includes `RUN_DIR: runs/HYP-...`:

1. Do NOT run new-hypothesis intake
2. Do NOT create a new folder
3. Validate `RUN_DIR/input/hypothesis.md`
4. If valid, invoke `/run-hypothesis.md` with that `RUN_DIR`

Use this when resuming or re-running an existing archive — not for a new hypothesis.

## User trigger examples

**Ready hypothesis:**

```text
/run-hypothesis-conversational.md

If AppSec engineers can manually prioritize SAST queue items, critical apps get scanned first.
```

**Dirty discovery + new run (second hypothesis same day):**

```text
/run-hypothesis-conversational.md
#контекст #новая

[discovery Q&A table — new hypothesis, not related to 001]
```

Agent flow: extract → mapping confirm → draft confirm → propose `runs/HYP-2026-06-23-002` → RUN_DIR confirm → bootstrap.

**Continue existing run:**

```text
RUN_DIR: runs/HYP-2026-06-23-001
/run-hypothesis-conversational.md
```

Skips new intake; validates and runs pipeline on existing archive.

## Do not

- Reuse or write to an existing `runs/HYP-*` when starting a new hypothesis without `RUN_DIR:`
- Use open-tab `RUN_DIR` as write target for a new hypothesis
- Create non-contract artifacts (e.g. `product_specification.md`)
- Bootstrap before RUN_DIR dialog confirm (Step 4b)
- Skip hypothesis draft confirm (Step 4a)
- Treat «ок» or continued chat as confirmation
- Run ad-hoc analysis plans instead of intake → dialog → bootstrap → pipeline
- Start pipeline before validation passes

## Reference

- Skill: `conversational-hypothesis-intake`
- Schema: `templates/input-schema.md`
- Examples: `examples/chat-first-run.md`
- Full pipeline: `run-hypothesis.md`
- Playbook: `playbooks/run-hypothesis.md`
