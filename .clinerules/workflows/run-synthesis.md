# Run Synthesis Layer

Execute Synthesis for an existing `RUN_DIR` after Market Layer completes.

## Prerequisites

Confirm these exist:

- `RUN_DIR/outputs/ready_for_synthesis.marker` with `status: completed`
- `RUN_DIR/outputs/knowledge_retrieval_complete.marker` with `status: completed`
- `RUN_DIR/outputs/business_context_complete.marker` with `status: completed`
  or `skipped_missing_context`
- `RUN_DIR/outputs/market_analysis_complete.marker` with `status: completed`
- `RUN_DIR/outputs/role_outputs/*`
- `RUN_DIR/outputs/hypothesis_summary.md`
- `RUN_DIR/outputs/market_analysis.md`
- `RUN_DIR/outputs/business_context_analysis.md` or
  `RUN_DIR/outputs/missing_business_context.md`

If missing, stop and tell the user which layer to run first.

## Steps

1. Activate skill `hypothesis-synthesis`.
2. Read all prior layer outputs (do not re-analyze roles, retrieval, or market).
3. Consume Business Context or preserve the explicit gap.
4. Execute 7-step cross-signal analysis.
5. Write `RUN_DIR/outputs/hypothesis_map.md`.
6. Write `RUN_DIR/outputs/hypothesis_digest.txt` (max 150 words).
7. Write `RUN_DIR/outputs/synthesis_complete.marker` as the canonical JSON body from `.clinerules/10-artifact-contracts.md`.
8. Display digest to the user and recommend running `/run-customer-discovery-planning.md`.

## What this phase does NOT do

- Does not summarize without comparison
- Does not add new market or role signals
- Does not infer strategic fit when Business Context is a gap
- Does not make final backlog decisions
