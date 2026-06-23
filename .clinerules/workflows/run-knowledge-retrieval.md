# Run Local Evidence Discovery

Execute Local Evidence Discovery for an existing `RUN_DIR`.

## Prerequisites

Confirm these files exist:

- `RUN_DIR/input/hypothesis.md`
- `RUN_DIR/outputs/hypothesis_summary.md` (recommended)

If `hypothesis_summary.md` is missing, continue with hypothesis-only relevance matching.

## Steps

1. Confirm `RUN_DIR/input/hypothesis.md` exists.
2. Activate skill `local-knowledge-retrieval`.
3. Generate `RUN_DIR/outputs/discovery_preview.md`.
4. Continue automatically to generate `RUN_DIR/outputs/evidence_inventory.md`.
5. Generate `RUN_DIR/outputs/knowledge_retrieval_complete.marker`.
6. Show the user brief retrieval summary:
   - scanned files
   - skipped files
   - evidence items written
   - top missing evidence gaps

## Rules

- Do not interpret market meaning in this workflow.
- Keep evidence items atomic and source-linked.
- Do not block on manual confirmation after preview (V1).

## Reference

See:

- `architecture/local-knowledge-retrieval.md`
- `.cline/skills/local-knowledge-retrieval/SKILL.md`
