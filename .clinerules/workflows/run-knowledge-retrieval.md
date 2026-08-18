# Run Local Evidence Discovery

Execute Local Evidence Discovery for an existing `RUN_DIR` after Facilitator.

## Prerequisites

Confirm these files exist:

- `RUN_DIR/input/hypothesis.md`
- `RUN_DIR/outputs/ready_for_synthesis.marker` with canonical JSON
  `status: completed`

Recommended:

- `RUN_DIR/outputs/hypothesis_summary.md`

If the Facilitator marker is missing, stop and ask the user to run
`/run-facilitator.md` first. If `hypothesis_summary.md` is missing after a
canonical marker, continue with hypothesis-only relevance matching.

## Steps

1. Confirm `RUN_DIR/input/hypothesis.md` exists.
2. Verify the Facilitator gate above.
3. Activate skill `local-knowledge-retrieval`.
4. Generate `RUN_DIR/outputs/discovery_preview.md`.
5. Continue automatically to generate `RUN_DIR/outputs/evidence_inventory.md`.
6. Generate `RUN_DIR/outputs/knowledge_retrieval_complete.marker` as the canonical JSON body from `.clinerules/10-artifact-contracts.md`.
7. Show the user brief retrieval summary:
   - scanned files
   - skipped files
   - evidence items written
   - `limit_reached` if scan or extraction hit a V1 cap
   - top missing evidence gaps

## Rules

- Do not interpret market meaning in this workflow.
- Keep evidence items atomic and source-linked.
- Do not block on manual confirmation after preview (V1).
- Next phase is Business Context, not Market.

## Reference

See:

- `architecture/local-knowledge-retrieval.md`
- `.cline/skills/local-knowledge-retrieval/SKILL.md`
