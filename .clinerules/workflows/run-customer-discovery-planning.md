# Run Customer Discovery Planning

Execute Customer Discovery Planning for an existing `RUN_DIR` after Synthesis completes.

## Prerequisites

Confirm these files exist:

- `RUN_DIR/input/hypothesis.md`
- `RUN_DIR/outputs/hypothesis_summary.md`
- `RUN_DIR/outputs/market_analysis.md`
- `RUN_DIR/outputs/hypothesis_map.md`
- `RUN_DIR/outputs/synthesis_complete.marker` (recommended)

Optional context:

- `RUN_DIR/outputs/validation_questions.md`
- `RUN_DIR/outputs/role_outputs/*`
- `RUN_DIR/outputs/decision_review.md`

If missing, tell the user to run Synthesis first.

## Steps

1. Activate skill `customer-discovery-planning`.
2. Read required synthesis and prior layer outputs.
3. Extract unknowns, classify risks, and define research goals.
4. Write `RUN_DIR/outputs/customer_discovery_plan.md`.
5. Write `RUN_DIR/outputs/customer_discovery_planning_complete.marker`.
6. Display top unknowns and high-priority interview roles to the user.

## What this phase does NOT do

- Does not validate hypotheses
- Does not make product or backlog decisions
- Does not recommend implementation
