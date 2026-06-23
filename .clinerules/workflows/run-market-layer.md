# Run Market Layer

Execute Market Layer only for an existing `RUN_DIR`.

## Steps

1. Confirm `RUN_DIR/input/hypothesis.md` exists.
2. Activate skill `hypothesis-market-layer`.
3. Read `RUN_DIR/outputs/evidence_inventory.md` if available and map findings to local KB signals.
4. Search Confluence MCP for additional local/internal signals.
5. If Confluence MCP unavailable — document MCP status and continue with KB inventory + explicit gaps.
6. Use external sources only if user approves and gaps remain.
7. Write `RUN_DIR/outputs/market_analysis.md`.
8. Write `RUN_DIR/outputs/market_analysis_complete.marker`.
9. Summarize signal strength and missing evidence to the user.

## Reference

See `implementations/confluence-mcp.md` for MCP setup.
