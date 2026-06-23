# Run Hypothesis (Full)

End-to-end hypothesis stress test for a single `RUN_DIR`.

## Steps

1. **Validate input**
   - Invoke `/validate-hypothesis-input.md` or skill `hypothesis-input-validation`.
   - Stop if validation fails.

2. **Facilitator (Roles Layer)**
   - Activate skill `hypothesis-facilitator`.
   - Produce `role_outputs/*`, `hypothesis_summary.md`, `validation_questions.md`, `ready_for_synthesis.marker`.
   - Show user a brief summary (assumptions, conflicts) before continuing.

3. **Local Evidence Discovery**
   - Activate skill `local-knowledge-retrieval`.
   - Produce `discovery_preview.md`, `evidence_inventory.md`, `knowledge_retrieval_complete.marker`.
   - Show user retrieval summary (scanned/skipped/items) before continuing.

4. **Market Layer**
   - Activate skill `hypothesis-market-layer`.
   - Read `evidence_inventory.md` first for KB-local signals.
   - Then search Confluence MCP for internal wiki signals.
   - Produce `market_analysis.md`, `market_analysis_complete.marker`.
   - Show user signal summary before continuing.

5. **Synthesis Layer**
   - Activate skill `hypothesis-synthesis`.
   - Produce `hypothesis_map.md`, `hypothesis_digest.txt`, `synthesis_complete.marker`.

6. **Customer Discovery Planning**
   - Activate skill `customer-discovery-planning`.
   - Produce `customer_discovery_plan.md`, `customer_discovery_planning_complete.marker`.
   - Show user critical unknowns and high-priority interview targets.

7. **Decision Review**
   - Activate skill `hypothesis-decision-review`.
   - Produce `decision_review.md`, `decision_review_complete.marker`.
   - Show user confidence and recommendation before continuing.

8. **Report**
   - Display `hypothesis_digest.txt` and key verdict from `decision_review.md`.
   - Remind: human makes the final backlog decision.

## Expected time

5–15 minutes per hypothesis.

## Reference

See `playbooks/run-hypothesis.md` for interpretation model and tips.
