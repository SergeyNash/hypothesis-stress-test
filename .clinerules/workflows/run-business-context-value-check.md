# Run Business Context & Value Check

Map business value mechanism and strategic fit before Market Layer.

## Prerequisites

Confirm these exist:

- `RUN_DIR/input/hypothesis.md`
- `RUN_DIR/outputs/ready_for_synthesis.marker` with canonical JSON
  `status: completed`
- `RUN_DIR/outputs/knowledge_retrieval_complete.marker` with canonical JSON
  `status: completed`

Recommended:

- `RUN_DIR/outputs/hypothesis_summary.md`
- `RUN_DIR/outputs/evidence_inventory.md`

If the Local Evidence marker is missing, stop and ask the user to run
`/run-knowledge-retrieval.md` first.

## Steps

1. Confirm the gates above.
2. Activate skill `business-context-value-check`.
3. Search KB for strategy, OKR, business-model materials.
4. If context missing:
   - Produce `missing_business_context.md`.
   - Produce `business_context_complete.marker` with
     `status: skipped_missing_context`.
   - Show user what to add to KB.
5. If context found:
   - Produce `business_context_analysis.md`.
   - Produce `business_context_complete.marker` with `status: completed`.
   - Show stakeholder map and strategic fit summary.
6. Continue to Market Layer (`/run-market-layer.md` or full pipeline).

Marker bodies MUST match `.clinerules/10-artifact-contracts.md`.

## Reference

- Skill: `.cline/skills/business-context-value-check/SKILL.md`
- Layer doc: `layers/business-context-layer.md`
- Contract: `.clinerules/10-artifact-contracts.md`
