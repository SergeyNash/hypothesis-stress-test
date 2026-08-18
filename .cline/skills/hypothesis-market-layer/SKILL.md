---
name: hypothesis-market-layer
description: Execute Market Layer with explicit signal channels (KB inventory, Confluence, external, inferred). Validate external reality for a hypothesis and produce market_analysis.md.
---

# Market Layer (Evidence-channel separation)

Validate whether the problem exists in reality using evidence-based analysis.

## Prerequisites

Required:

- `RUN_DIR/input/hypothesis.md`
- `RUN_DIR/outputs/business_context_complete.marker` with canonical JSON
  `status: completed` or `status: skipped_missing_context`
- `RUN_DIR/outputs/business_context_analysis.md` **or**
  `RUN_DIR/outputs/missing_business_context.md`

Recommended:

- `RUN_DIR/outputs/evidence_inventory.md`
- `RUN_DIR/outputs/hypothesis_summary.md`

If the Business Context gate is missing, stop. Do not start Market Layer.

Use Business Context only to frame buyer, value, and strategic-fit interpretation.
If the gap artifact exists, preserve it: market evidence must not fabricate
internal strategic fit.

## Step 0 — Local KB inventory (if present)

If `RUN_DIR/outputs/evidence_inventory.md` exists:

- Read local evidence items (`EVID-NNN`)
- Keep evidence atomic (do not rewrite as synthesis)
- Preserve `evidence_type` and `relevance_reason`
- If item is `metadata_only`, do not promote it to factual claim

If inventory is missing:

- Add explicit gap note in Local KB section: `missing local file evidence`

## Step 1 — Confluence MCP

Search Confluence for local signals related to the hypothesis:

- Similar problems discussed internally
- Past decisions or research notes
- Customer feedback or discovery artifacts
- Architectural constraints
- Historical hypotheses on the same topic

For each finding, record:

- Signal type: **local (confluence)**
- Signal strength: strong / weak / none
- Source: page title, space, URL or page ID

If Confluence MCP is not available, add:

```markdown
## MCP Status
Confluence MCP: not configured
```

Do not fabricate internal knowledge.

## Step 2 — External signals (secondary, default skip)

Do **not** search external sources unless the user explicitly approves.

Default: skip external research and record:

```markdown
## External Market Signals
- skipped — user did not approve external research
```

If the user approves, cite URLs for every external claim and label type **external**.

## Step 3 — Inferred signals (last resort)

Logical conclusions from available data only. Label as **inferred** with explicit `basis:`.

## Evidence rules

- No evidence → no claim
- Distinguish facts from assumptions
- Prefer uncertainty over hallucination
- Do not invent market demand
- Keep channels separate (KB / Confluence / External / Inferred)

## Output

Write `RUN_DIR/outputs/market_analysis.md` with sections:

```markdown
# Market Analysis

## MCP Status
Confluence MCP: configured | not configured

## Local Signals from Knowledge Base
- [finding] — signal: strong|weak|none — evidence_id: EVID-NNN — evidence_type: ... — source: [path]

## Confluence Signals
- [finding] — signal: strong|weak|none — source: [page title](url)

## External Market Signals
- [finding] — signal: strong|weak|none — source: [reference]
  or: skipped — user did not approve external research

## Inferred Signals
- [finding] — signal: strong|weak|none — basis: [what it was inferred from]

## Signal Summary
- Overall local KB signal: strong|weak|none
- Overall confluence signal: strong|weak|none
- Overall external signal: strong|weak|none
- Missing evidence: [list gaps]
```

Write `RUN_DIR/outputs/market_analysis_complete.marker`:

```json
{
  "status": "completed",
  "completed_phase": "market",
  "next_phase": "synthesis",
  "inputs": [
    "outputs/market_analysis.md"
  ]
}
```

Match heading language to `input/hypothesis.md`.

## Reference

Based on `templates/market-prompt.md`, `layers/market-layer.md`, and `.clinerules/20-evidence-rules.md`.
