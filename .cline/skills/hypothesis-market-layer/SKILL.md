---
name: hypothesis-market-layer
description: Execute Market Layer with explicit signal channels (KB inventory, Confluence, external, inferred). Validate external reality for a hypothesis and produce market_analysis.md.
---

# Market Layer (Evidence-channel separation)

Validate whether the problem exists in reality using evidence-based analysis.

## Prerequisites

- `RUN_DIR/input/hypothesis.md` exists
- Roles Layer outputs are optional but recommended
- `RUN_DIR/outputs/evidence_inventory.md` is optional but recommended

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

## Step 2 — External signals (secondary)

Only after Confluence search, if gaps remain:

- Search external sources if user approves
- Cite URLs for every external claim
- Label signal type: **external**

## Step 3 — Inferred signals (last resort)

Logical conclusions from available data only. Label as **inferred** with explicit basis.

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
...

## External Market Signals
...

## Inferred Signals
...

## Signal Summary
- Overall local KB signal: strong|weak|none
- Overall confluence signal: strong|weak|none
- Overall external signal: strong|weak|none
- Missing evidence: ...
```

Write `RUN_DIR/outputs/market_analysis_complete.marker`.

## Reference

Based on `templates/market-prompt.md`, `layers/market-layer.md`, and `.clinerules/20-evidence-rules.md`.
