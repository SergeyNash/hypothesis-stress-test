# Run Synthesis Layer

Execute Synthesis for an existing `RUN_DIR` after Facilitator and Market layers complete.

## Prerequisites

Confirm these exist:

- `RUN_DIR/outputs/ready_for_synthesis.marker`
- `RUN_DIR/outputs/market_analysis_complete.marker`
- `RUN_DIR/outputs/role_outputs/*`
- `RUN_DIR/outputs/hypothesis_summary.md`
- `RUN_DIR/outputs/market_analysis.md`

If missing, stop and tell the user which layer to run first.

## Steps

1. Activate skill `hypothesis-synthesis`.
2. Read all prior layer outputs (do not re-analyze roles or market).
3. Execute 7-step cross-signal analysis.
4. Write `RUN_DIR/outputs/hypothesis_map.md`.
5. Write `RUN_DIR/outputs/hypothesis_digest.txt` (max 150 words).
6. Write `RUN_DIR/outputs/synthesis_complete.marker`.
7. Display digest to the user.

## What this phase does NOT do

- Does not summarize without comparison
- Does not add new market or role signals
- Does not make final backlog decisions
