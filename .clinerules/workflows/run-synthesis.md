# Run Synthesis Layer

Execute Synthesis Layer for an existing `RUN_DIR`.

## Prerequisites

Confirm these files exist:

- `RUN_DIR/outputs/role_outputs/*`
- `RUN_DIR/outputs/hypothesis_summary.md`
- `RUN_DIR/outputs/market_analysis.md`

If missing, tell the user which layer to run first.

## Steps

1. Activate skill `hypothesis-synthesis-layer`.
2. Read all prior layer outputs.
3. Compare internal vs external signals.
4. Classify hypothesis (Validated Opportunity / Internal Illusion / Blind Spot / Weak Signal).
5. Write `RUN_DIR/outputs/hypothesis_map.md`.
6. Write `RUN_DIR/outputs/hypothesis_digest.txt`.
7. Write `RUN_DIR/outputs/synthesis_complete.marker`.
8. Display digest to the user.
