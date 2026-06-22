# Run Market Layer

Execute Market Layer only for an existing `RUN_DIR`.

## Steps

1. Confirm `RUN_DIR/input/hypothesis.md` exists.
2. Activate skill `hypothesis-market-layer`.
3. **Confluence first**: search Confluence MCP for local signals related to the hypothesis.
4. If Confluence MCP unavailable — document `missing local evidence` in output.
5. Use external sources only if user approves and gaps remain.
6. Write `RUN_DIR/outputs/market_analysis.md`.
7. Write `RUN_DIR/outputs/market_analysis_complete.marker`.
8. Summarize signal strength to the user.

## Reference

See `implementations/confluence-mcp.md` for MCP setup.
