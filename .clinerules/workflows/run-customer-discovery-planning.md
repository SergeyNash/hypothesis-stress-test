# Run Customer Discovery Planning

Execute Customer Discovery Planning for an existing `RUN_DIR` after Synthesis completes.

## Prerequisites

Confirm these files exist:

- `RUN_DIR/input/hypothesis.md`
- `RUN_DIR/outputs/hypothesis_summary.md`
- `RUN_DIR/outputs/market_analysis.md`
- `RUN_DIR/outputs/hypothesis_map.md`
- `RUN_DIR/outputs/synthesis_complete.marker` with canonical JSON
  `status: completed`

Optional context:

- `RUN_DIR/outputs/validation_questions.md`
- `RUN_DIR/outputs/role_outputs/*`
- `RUN_DIR/outputs/evidence_inventory.md`
- `RUN_DIR/outputs/business_context_analysis.md` or
  `RUN_DIR/outputs/missing_business_context.md`

Do not read `decision_review.md` — that artifact is produced after this phase.

If Synthesis outputs or marker are missing, tell the user to run Synthesis first.

## Steps

1. Activate skill `customer-discovery-planning`.
2. Read required synthesis and prior layer outputs, including Business Context or its gap.
3. Extend `validation_questions.md`; do not duplicate it.
4. Extract unknowns, classify risks, and define research goals. Bind unknowns to `EVID-*` when possible.
5. Write `RUN_DIR/outputs/customer_discovery_plan.md`.
6. Write `RUN_DIR/outputs/customer_discovery_planning_complete.marker` as the canonical JSON body from `.clinerules/10-artifact-contracts.md`.
7. Display top unknowns and high-priority interview roles to the user.

## What this phase does NOT do

- Does not validate hypotheses
- Does not make product or backlog decisions
- Does not recommend implementation
- Does not invent missing business context
