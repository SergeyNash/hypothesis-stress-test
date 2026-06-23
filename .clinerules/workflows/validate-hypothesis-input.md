# Validate Hypothesis Input

Use the **hypothesis-input-validation** skill to check `RUN_DIR/input/hypothesis.md`.

## Steps

1. Ask the user for `RUN_DIR` if not provided.
2. Activate skill `hypothesis-input-validation`.
3. Read `RUN_DIR/input/hypothesis.md`.
4. Run all validation checks (metadata, statement, roles, research context).
5. If invalid — ask clarifying questions and stop.
   - In conversational flow (`/run-hypothesis-conversational.md`): return to skill `conversational-hypothesis-intake` for targeted repair, then re-validate.
6. If valid — confirm readiness and suggest `/run-hypothesis.md`, `/run-hypothesis-conversational.md` (for a new run), or individual layer workflows.

## Do not

- Run any layer on invalid input
- Skip role or context checks
