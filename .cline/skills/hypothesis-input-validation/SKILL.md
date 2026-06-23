---
name: hypothesis-input-validation
description: Validate hypothesis input before running the stress-test framework. Use when starting a new hypothesis run, before Roles or Market layers, or when input quality is uncertain.
---

# Hypothesis Input Validation

Validate `RUN_DIR/input/hypothesis.md` before any layer executes.

## Read input

1. Locate `RUN_DIR` (ask user if not specified).
2. Read `RUN_DIR/input/hypothesis.md`.

## Required checks

### Metadata

- Hypothesis ID present and matches `HYP-YYYY-MM-DD-NNN` format?
- Created at date present?
- Run ID present?
- Status defined (`draft` | `running` | `completed` | `archived`)?
- If `RUN_DIR` folder name includes a hypothesis ID, it should match `Hypothesis ID` in metadata.

### Hypothesis statement

- Is it specific and testable?
- Does it describe a change and expected outcome?
- Reject vague statements like "improve user experience".

### Relevant roles

- Are roles defined?
- Are they real perspectives (not generic placeholders)?
- Are they directly impacted by the hypothesis?
- Flag if more than 5 roles (noise risk).

### Research context

- Domain defined?
- Target audience defined?
- Scenario concrete enough for market validation?

## If validation fails

Do NOT run any layer. Ask clarifying questions:

- "Who is affected by this?"
- "In what context does this happen?"
- "What exactly changes?"

## If validation passes

Confirm readiness and list:

- Hypothesis ID and Run ID
- Hypothesis statement (one line)
- Roles selected
- Research context summary

Suggest next step: invoke `/run-hypothesis.md` workflow, or `/run-hypothesis-conversational.md` for a new chat-first run.

## Reference

See `templates/input-schema.md` and `playbooks/validate-input.md`.
