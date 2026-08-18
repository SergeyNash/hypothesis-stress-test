# Business Context & Value Check — Manual Prompt

Use after Roles Layer and Local Evidence Discovery, before Market Layer.

## Input

- `RUN_DIR/input/hypothesis.md`
- `RUN_DIR/outputs/hypothesis_summary.md`
- `RUN_DIR/outputs/role_outputs/*`
- KB: `strategy/`, `okr/`, `business-model/` (or equivalents)

## Task

1. Check whether strategy materials exist in KB.
2. If missing → write `missing_business_context.md` only.
3. If present → write `business_context_analysis.md` with:
   - stakeholder map (pain / value / decide / pay / block)
   - value flow: Problem → Beneficiary → Behavior change → Business effect
   - business effect type(s)
   - strategic fit (High / Medium / Low) with citations
   - key risks and opportunities
4. Write `business_context_complete.marker` as canonical JSON
   (`status: completed` or `skipped_missing_context`).

## Rules

- No evidence → no claim
- Do not invent OKR alignment
- Language matches `input/hypothesis.md`

## Output paths

- `RUN_DIR/outputs/business_context_analysis.md`
- `RUN_DIR/outputs/missing_business_context.md` (if gap)
- `RUN_DIR/outputs/business_context_complete.marker`
