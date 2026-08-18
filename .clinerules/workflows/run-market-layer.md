# Run Market Layer

Execute Market Layer only for an existing `RUN_DIR` after Business Context.

## Prerequisites

Confirm these exist:

- `RUN_DIR/input/hypothesis.md`
- `RUN_DIR/outputs/business_context_complete.marker` with canonical JSON
  `status: completed` or `status: skipped_missing_context`
- `RUN_DIR/outputs/business_context_analysis.md` or
  `RUN_DIR/outputs/missing_business_context.md`

Recommended:

- `RUN_DIR/outputs/evidence_inventory.md`
- `RUN_DIR/outputs/knowledge_retrieval_complete.marker` with `status: completed`

If the Business Context marker or gap/analysis artifact is missing, stop and
ask the user to run `/run-business-context-value-check.md` first. Do not start
Market Layer.

## Steps

1. Confirm `RUN_DIR/input/hypothesis.md` exists.
2. Verify the Business Context gate above.
3. Activate skill `hypothesis-market-layer`.
4. Read `RUN_DIR/outputs/evidence_inventory.md` if available and map findings to local KB signals.
5. Search Confluence MCP for additional local/internal signals.
6. If Confluence MCP unavailable — document MCP status and continue with KB inventory + explicit gaps.
7. Use external sources only after an explicit user approval; default is skip.
8. Write `RUN_DIR/outputs/market_analysis.md`.
9. Write `RUN_DIR/outputs/market_analysis_complete.marker` as the canonical JSON body from `.clinerules/10-artifact-contracts.md`.
10. Summarize signal strength and missing evidence to the user.

## Reference

See `implementations/confluence-mcp.md` for MCP setup.
