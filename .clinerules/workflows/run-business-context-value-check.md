# Run Business Context & Value Check

Map business value mechanism and strategic fit before Market Layer.

## Steps

1. Confirm `RUN_DIR/input/hypothesis.md` and Roles Layer outputs exist (`ready_for_synthesis.marker`).
2. Activate skill `business-context-value-check`.
3. Search KB for strategy, OKR, business-model materials.
4. If context missing:
   - Produce `missing_business_context.md`, `business_context_complete.marker`.
   - Show user what to add to KB.
5. If context found:
   - Produce `business_context_analysis.md`, `business_context_complete.marker`.
   - Show stakeholder map and strategic fit summary.
6. Continue to Market Layer (`/run-market-layer.md` or full pipeline).

## Reference

- Skill: `.cline/skills/business-context-value-check/SKILL.md`
- Layer doc: `layers/business-context-layer.md`
- Contract: `.clinerules/10-artifact-contracts.md`
