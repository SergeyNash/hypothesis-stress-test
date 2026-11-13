---
name: hst-start
description: Start a new Hypothesis Stress Test from a natural-language idea or notes; guide intake, confirm a new isolated run and execute hst-run with live progress. Also route explicit RUN_DIR to safe resume.
---

# Run Hypothesis (Conversational / Chat-First)

After the first visible action below, resolve the application profile from input Metadata (new intake: propose and confirm). No field → digital_product. For service_business load FRAMEWORK_DIR/profiles/service-business.md and apply its phase-specific requirements, including service readiness instead of backlog readiness. Preserve canonical artifact paths and gates.

Start a full hypothesis stress test from chat dialogue. The user does not need to create `RUN_DIR` or edit `input/hypothesis.md` manually.

**Primary entry point for new hypotheses.**

Resolve FRAMEWORK_DIR by its actual directory (nested/renamed is allowed); all templates, profiles and scripts live there. KB_ROOT is the open workspace. Use skills directly; legacy slash workflow examples below are compatibility aliases only. If input has no named run, start intake; do not require tags or a prewritten file. At each pause explain what is needed in plain language; never call a pending confirmation a completed run. File-first workflow remains available via skill `hst-run`.

## First visible action (before profile/intake analysis)

For a new request with no explicit RUN_DIR, resolve only KB_ROOT and FRAMEWORK_DIR (use `.hst/workspace.json` when installed), then make the first operational call:

```text
python <FRAMEWORK_DIR>/scripts/startup_progress.py start --workspace <KB_ROOT> --stage routing --message "Принимаю новую гипотезу; готовлю карточку"
```

Keep returned `session_id` as STARTUP_ID. This creates only workspace runtime state in `.hst`, not RUN_DIR, hypothesis files, evidence or completed phases. Do this BEFORE reading profiles/phase instructions, scanning old runs or composing the full card. A read-only classification of new vs resume and resolving the actual script path are the only prerequisites. Do not inspect old run outputs, role personas, research tools or downstream layer contracts during intake. Load only the intake schema and relevant profile sections.

At material transitions, use `startup_progress.py update --workspace <KB_ROOT> --session <STARTUP_ID> --stage intake|confirmation|bootstrap --state running|waiting_user|error|cancelled --message "<actual short action>"`. Record waiting_user BEFORE asking the confirmation question; running after a clear answer; error/cancelled when applicable. No fabricated calls or periodic fake heartbeats. This status is visible in both terminal viewers before any HYP folder exists; the viewers do not execute the model.

For a complete ready statement, gather no already-supplied fields. Prepare the card and next-free folder in one pass; a directory-name scan of today's runs is sufficient, without reading their content. Show both in ONE confirmation. A clear answer approving that displayed card and folder satisfies Steps 4a and 4b together; ordinary yes/да/ок is sufficient when its referent is unambiguous. A previous explicit authorization for that exact card and directory also applies; never ask again just for a prescribed phrase. Missing essential input or an actual revision still requires clarification. Never skip semantic validation or source selection.

After confirmed bootstrap, BEFORE validation, attach the startup session:

```text
python <FRAMEWORK_DIR>/scripts/startup_progress.py attach --workspace <KB_ROOT> --session <STARTUP_ID> --run-dir <RUN_DIR>
```

The helper archives the real pre-folder timestamps in `outputs/startup_events.jsonl`, records intake completion and validation running, and publishes the active pointer. A failed input check must record validation error/wait, not leave a static running state. Then follow normal prepare after valid input. On explicit resume do not create a startup session; activate the supplied run early and preserve its history.

The initial model reasoning before its first tool call is not measured. Do not promise a fixed startup duration. If the first call fails, explain the actual failure in chat rather than claiming that progress is live.

## Steps

### 0. Route: new run vs continue existing

Check the user message first:

| Condition | Path |
| --------- | ---- |
| Message contains `RUN_DIR: runs/HYP-...` | **Resume existing run** — skip intake and bootstrap; delegate to skill `hst-run` preflight/resume logic |
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
- **Step 4a:** confirm the hypothesis draft; for complete ready input combine with the folder proposal and approval.
- **Step 4b:** propose new `RUN_DIR`, list existing runs today, wait for RUN_DIR confirmation; for complete ready input combine with Step 4a as described above.
- Require an unambiguous response to the displayed card/folder. Accept ordinary affirmative wording when clear; silence or unrelated continuation is not confirmation.

Stop if the user cancels at any step.

Do NOT write RUN_DIR/input/output files until Step 4b (or the combined confirmation) completes. The early `.hst` startup state is the explicit exception.

### 2. Bootstrap RUN_DIR

Execute **only after** intake returns:

```yaml
IntakeResult:
  confirmed: true
  intake_mode: ready | dirty | roles-only | auto
  proposed_run_dir: runs/HYP-YYYY-MM-DD-NNN
  draft_markdown: |
    # confirmed markdown
```

Reject an incomplete or differently shaped handoff. Re-check that
`proposed_run_dir` does not exist immediately before creating it; if it now
exists, return to the RUN_DIR proposal and confirmation step. Use
`draft_markdown` from the confirmed handoff.

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

Set `RUN_DIR` for all subsequent steps. Tell the user where this check and its results will be saved. Initialize live progress per `30-run-observability.md` and record intake completed. Do not initialize run files before the bootstrap confirmation. Attach STARTUP_ID immediately after bootstrap, before validation; no HTTP server is needed for this early terminal progress.

### 3. Validate input

Invoke skill `hypothesis-input-validation` or skill `hypothesis-input-validation` against the new `RUN_DIR`.

If validation fails:

- Activate skill `conversational-hypothesis-intake` in repair mode
- Show the structured `validation`, `failed_checks`, and `repair_hints`
- Update `input/hypothesis.md` only after user explicitly confirms the revised
  draft and the overwrite
- Re-run validation
- Repeat until validation passes or user cancels

Do NOT start the pipeline on invalid input.

### 4. Run full pipeline

When validation passes:

1. Update `Status` in `input/hypothesis.md` to `running` if still `draft`
2. Invoke skill `hst-run` with the bootstrapped `RUN_DIR`; its preflight
   will select the first incomplete phase

The conversational workflow does not duplicate layer logic — it delegates to the existing end-to-end workflow.

### 5. Report

After pipeline completes, display:

- `RUN_DIR` path
- `outputs/hypothesis_digest.txt`
- Key verdict from `outputs/decision_review.md`
- Reminder: human makes the final backlog decision

## Resume existing run (when `RUN_DIR:` provided)

If the user message includes `RUN_DIR: runs/HYP-...`:

1. Do NOT run new-hypothesis intake
2. Do NOT create a new folder
3. Invoke skill `hst-run` with that `RUN_DIR`
4. Let its preflight validate input, read canonical JSON marker bodies, verify
   prerequisite artifacts/status, skip completed phases, and summarize the
   first safe resume point
5. If a marker is malformed or free text, ask whether to verify and migrate it,
   rerun the phase, or cancel. Never trust or overwrite it silently.
6. Require explicit confirmation before rerunning a completed/invalidated phase
   or overwriting existing outputs.

Use this for safe resume. A full rerun is not implied by providing `RUN_DIR`.

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

Skips new intake and bootstrap; reports completed phases and resumes at the
first incomplete/invalid phase after any required confirmation.

## Do not

- Reuse or write to an existing `runs/HYP-*` when starting a new hypothesis without `RUN_DIR:`
- Use open-tab `RUN_DIR` as write target for a new hypothesis
- Create non-contract artifacts (e.g. `product_specification.md`)
- Bootstrap before RUN_DIR dialog confirm (Step 4b)
- Skip hypothesis draft confirm (Step 4a)
- Treat silence, an unrelated reply or an ambiguous answer as confirmation
- Blindly rerun all phases for an existing `RUN_DIR`
- Trust or overwrite malformed/free-text legacy markers
- Run ad-hoc analysis plans instead of intake → dialog → bootstrap → pipeline
- Start pipeline before validation passes

## Reference

- Skill: `conversational-hypothesis-intake`
- Schema: `templates/input-schema.md`
- Examples: `examples/chat-first-run.md`
- Full pipeline: `run-hypothesis.md`
- Playbook: `playbooks/run-hypothesis.md`

## Mandatory post-bootstrap handoff

Once confirmed input passes validation, run `scripts/run_control.py prepare --run-dir <RUN_DIR> --mode full` using the resolved FRAMEWORK_DIR. Show its verified live URL immediately, even while waiting for a later phase choice. For a draft-only choice use mode phase and do not start roles. Follow `.clinerules/40-run-quality.md`; do not wait for the user to request progress.

New `prepare` writes audit_version 2. Before roles run `run_control.py start --run-dir <RUN_DIR> --phase facilitator` and show its verified URL; a failed server must be explained and recorded, never silently ignored. Preserve config/version on resume.

## Terminal progress handoff

If the dedicated HST terminal task is installed, it waits for the active-run pointer and does not need a RUN_DIR typed by the user. Normal `prepare` publishes the pointer before HTTP startup. For an explicit resume/selection, run `run_control.py activate --run-dir <RUN_DIR>` once. Resolve framework paths as usual; for custom layouts pass --workspace <KB_ROOT>. Do not start the viewer as a long foreground command in Cline's execution terminal. In an already-open workspace the task must be launched once via Terminal → Run Task → HST · Прогресс, or on folder reopen after native automatic-task permission. Do not present the task as already visible unless observed.
