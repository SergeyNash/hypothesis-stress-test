---
name: hypothesis-market-layer
description: Execute the Market Layer with Confluence-first local signal retrieval. Validate external reality for a hypothesis and produce market_analysis.md. Use after Roles Layer or when external validation is needed.
---

# Market Layer (Confluence-first)

Validate whether the problem exists in reality using evidence-based analysis.

## Prerequisites

- `RUN_DIR/input/hypothesis.md` exists
- Roles Layer outputs are optional but recommended

## Step 1 — Confluence MCP (required first)

Search Confluence for local signals related to the hypothesis:

- Similar problems discussed internally
- Past decisions or research notes
- Customer feedback or discovery artifacts
- Architectural constraints
- Historical hypotheses on the same topic

For each finding, record:

- Signal type: **local**
- Signal strength: strong / weak / none
- Source: page title, space, URL or page ID

If Confluence MCP is not available, add:

```markdown
## MCP Status
Confluence MCP: not configured
```

Mark local signals as `missing local evidence`. Do not fabricate internal knowledge.

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

## Output

Write `RUN_DIR/outputs/market_analysis.md` with sections:

```markdown
# Market Analysis

## MCP Status
Confluence MCP: configured | not configured

## Local Signals (Confluence)
...

## External Signals
...

## Inferred Signals
...

## Signal Summary
- Overall local signal: strong|weak|none
- Overall external signal: strong|weak|none
- Missing evidence: ...
```

Write `RUN_DIR/outputs/market_analysis_complete.marker`.

## Reference

Based on `templates/market-prompt.md`, `layers/market-layer.md`, and `.clinerules/20-evidence-rules.md`.
