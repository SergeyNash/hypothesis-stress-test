# Run Decision Review

Execute Decision Review for an existing `RUN_DIR` after Customer Discovery Planning completes.

## Prerequisites

Confirm these files exist:

- `RUN_DIR/input/hypothesis.md`
- `RUN_DIR/outputs/hypothesis_map.md`
- `RUN_DIR/outputs/customer_discovery_plan.md`
- `RUN_DIR/outputs/synthesis_complete.marker` with `status: completed`
- `RUN_DIR/outputs/customer_discovery_planning_complete.marker` with
  `status: completed`

Also read when present:

- `RUN_DIR/outputs/hypothesis_summary.md`
- `RUN_DIR/outputs/evidence_inventory.md`
- `RUN_DIR/outputs/business_context_analysis.md` or
  `RUN_DIR/outputs/missing_business_context.md`
- `RUN_DIR/outputs/market_analysis.md`
- `RUN_DIR/outputs/hypothesis_digest.txt`
- `RUN_DIR/outputs/role_outputs/*`

If Customer Discovery Planning is missing, tell the user to run it first.

## Steps

1. Activate skill `hypothesis-decision-review`.
2. Read existing synthesis, customer discovery, and prior layer artifacts.
3. Challenge conclusions — do not repeat synthesis and do not add new signals.
4. Write `RUN_DIR/outputs/decision_review.md`.
5. Write `RUN_DIR/outputs/decision_review_complete.marker` as the canonical JSON body from `.clinerules/10-artifact-contracts.md`.
6. Display executive summary (confidence + recommendation token) to the user.
7. Remind: human makes the final backlog decision.

## Scope

Decision Review may reference Roles, Local Evidence, Business Context, Market,
Synthesis, and Customer Discovery Planning artifacts. It must not perform new
retrieval, MCP/external research, or role analysis.
