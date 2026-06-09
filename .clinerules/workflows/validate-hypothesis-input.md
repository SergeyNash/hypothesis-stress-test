# Validate Hypothesis Input

Use the **hypothesis-input-validation** skill to check `RUN_DIR/hypothesis.md`.

## Steps

1. Ask the user for `RUN_DIR` if not provided.
2. Activate skill `hypothesis-input-validation`.
3. Read `RUN_DIR/hypothesis.md`.
4. Run all validation checks (statement, roles, research context).
5. If invalid — ask clarifying questions and stop.
6. If valid — confirm readiness and suggest `/run-hypothesis.md` or individual layer workflows.

## Do not

- Run any layer on invalid input
- Skip role or context checks
