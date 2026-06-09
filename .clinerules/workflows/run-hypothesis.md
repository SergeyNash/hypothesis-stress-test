# Run Hypothesis (Full)

End-to-end hypothesis stress test for a single `RUN_DIR`.

## Steps

1. **Validate input**
   - Invoke `/validate-hypothesis-input.md` or skill `hypothesis-input-validation`.
   - Stop if validation fails.

2. **Roles Layer**
   - Activate skill `hypothesis-roles-layer`.
   - Produce `role_outputs/*`, `hypothesis_summary.md`, `ready_for_synthesis.marker`.
   - Show user a brief summary before continuing.

3. **Market Layer**
   - Activate skill `hypothesis-market-layer`.
   - Search Confluence MCP first for local signals.
   - Produce `market_analysis.md`, `market_analysis_complete.marker`.
   - Show user signal summary before continuing.

4. **Synthesis Layer**
   - Activate skill `hypothesis-synthesis-layer`.
   - Produce `hypothesis_map.md`, `hypothesis_digest.txt`, `synthesis_complete.marker`.

5. **Report**
   - Display `hypothesis_digest.txt` to the user.
   - Remind: human makes the final decision.

## Expected time

5–15 minutes per hypothesis.

## Reference

See `playbooks/run-hypothesis.md` for interpretation model and tips.
