# Validate Hypothesis Input

Use the **hypothesis-input-validation** skill to check `RUN_DIR/input/hypothesis.md`.

## Steps

1. Ask the user for `RUN_DIR` if not provided.
2. Activate skill `hypothesis-input-validation`.
3. Read `RUN_DIR/input/hypothesis.md`.
4. Resolve RU/EN aliases from `templates/input-schema.md`; the file may use
   either heading language and feedback follows the input language.
5. Run all validation checks (metadata, folder ID match, status enum,
   testability, roles, research context).
6. Return the formal result in chat and to the caller (do not write a marker):

   ```yaml
   validation: pass | fail
   failed_checks:
     - code: MISSING_SECTION | INVALID_HYPOTHESIS_ID | RUN_DIR_ID_MISMATCH | INVALID_STATUS | VAGUE_STATEMENT | MISSING_ROLES | TOO_MANY_ROLES | MISSING_CONTEXT_FIELD
       field: canonical_field
       message: localized explanation
   repair_hints:
     - localized actionable hint
   ```

   On pass, both arrays are empty. On fail, include every detected failure.
7. If invalid — ask targeted clarifying questions and stop.
   - In conversational flow (`/run-hypothesis-conversational.md`): return to skill `conversational-hypothesis-intake` for targeted repair, then re-validate.
8. If valid — confirm readiness and suggest `/run-hypothesis.md`,
   `/run-hypothesis-conversational.md` (for a new run), or individual layer
   workflows.

## Do not

- Run any layer on invalid input
- Skip role or context checks
- Silently normalize localized status values or alter the input file
