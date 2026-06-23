# Run Hypothesis (Conversational / Chat-First)

Start a full hypothesis stress test from chat dialogue. The user does not need to create `RUN_DIR` or edit `input/hypothesis.md` manually.

**Primary entry point for new hypotheses.** File-first workflow remains available via `/run-hypothesis.md`.

## Steps

### 1. Conversational intake

Activate skill `conversational-hypothesis-intake`.

- Accept the user's hypothesis in natural language (or continue from an in-progress intake)
- Collect missing fields through guided questions
- Show draft `input/hypothesis.md` preview
- Wait for explicit user confirmation (`Confirm and run` / `Подтвердить и запустить`)

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

```text
/run-hypothesis-conversational.md

I want to test this hypothesis: if AppSec engineers can manually prioritize SAST queue items, critical apps get scanned first.
```

```text
/run-hypothesis-conversational.md
```

(Then answer guided questions in chat.)

## Fallback

Users who prefer file-first workflow:

```text
RUN_DIR: runs/HYP-2026-06-22-001
/run-hypothesis.md
```

## Do not

- Skip the confirmation step before bootstrap
- Start pipeline before validation passes
- Change downstream artifact contracts or layer skills

## Reference

- Skill: `conversational-hypothesis-intake`
- Schema: `templates/input-schema.md`
- Full pipeline: `run-hypothesis.md`
- Playbook: `playbooks/run-hypothesis.md`
