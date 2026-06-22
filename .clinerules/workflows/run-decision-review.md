# Run Decision Review

Execute Decision Review for an existing `RUN_DIR` after Customer Discovery Planning completes.

## Prerequisites

Confirm these files exist:

- `RUN_DIR/input/hypothesis.md`
- `RUN_DIR/outputs/hypothesis_summary.md`
- `RUN_DIR/outputs/market_analysis.md`
- `RUN_DIR/outputs/hypothesis_map.md`
- `RUN_DIR/outputs/customer_discovery_plan.md` (recommended)
- `RUN_DIR/outputs/hypothesis_digest.txt` (recommended)
- `RUN_DIR/outputs/synthesis_complete.marker` (recommended)
- `RUN_DIR/outputs/customer_discovery_planning_complete.marker` (recommended)

If missing, tell the user to run Customer Discovery Planning first.

## Steps

1. Activate skill `hypothesis-decision-review`.
2. Read all required synthesis, customer discovery, and prior layer outputs.
3. Challenge conclusions — do not repeat or summarize synthesis.
4. Write `RUN_DIR/outputs/decision_review.md`.
5. Write `RUN_DIR/outputs/decision_review_complete.marker`.
6. Display executive summary (confidence + recommendation) to the user.
7. Remind: human makes the final backlog decision.
