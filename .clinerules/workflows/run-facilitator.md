# Run Facilitator (Roles Layer)

Execute the facilitator stress-test for an existing `RUN_DIR`.

## Prerequisites

- `RUN_DIR/hypothesis.md` exists
- Input passed validation (`hypothesis-input-validation` or `/validate-hypothesis-input.md`)

If validation was skipped, run validation first.

## Steps

1. Activate skill `hypothesis-facilitator`.
2. Read `RUN_DIR/hypothesis.md` and optional context.
3. Execute the 6-step analysis process.
4. Write `RUN_DIR/outputs/role_outputs/{role_slug}.md` for each role.
5. Write `RUN_DIR/outputs/hypothesis_summary.md`.
6. Write `RUN_DIR/outputs/validation_questions.md`.
7. Write `RUN_DIR/outputs/ready_for_synthesis.marker`.
8. Display brief summary: key assumptions, conflicts, and top validation questions.

## What this phase does NOT do

- Does not make decisions
- Does not research the market
- Does not synthesize conclusions
- Does not design experiments
