---
name: hypothesis-market-layer
description: Execute Market Layer with explicit signal channels (KB inventory, Confluence, external, inferred). Validate external reality for a hypothesis and produce market_analysis.md. Supports digital_product and service_business decisions.
---

## Application profile (resolve before this skill)

Read `Application Profile / Профиль применения` from input Metadata; during intake infer a proposed profile from the requested decision and confirm it in the draft. Missing field means `digital_product`.

For `service_business`, read [service-business profile](../../../profiles/service-business.md), especially **Market**, and apply its profile-specific rules before the default instructions below. Service-specific fields and criteria override product-only wording; the existing phase order, output paths and markers remain unchanged. Unknown profile is a validation error, not a reason to guess.


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
Confluence MCP: unavailable
Reason: [actual tool availability/configuration issue]
```

An actual 401/403 is auth_error, not “not configured” or no_results. Record the failed operation without credentials; tell the user immediately and offer to restore access or continue without this channel. After one failed authentication attempt do not retry until configuration changes. Journal actual queries, pages found/read and sources used. Never claim a tool call from a planned query.

Do not fabricate internal knowledge.

## Step 2 — External signals

Read `outputs/external_research.md` from Business Context first; preserve EXT-IDs, source dates, URLs and coverage limitations. Search remaining critical gaps with `external-business-research` without repeating completed queries. Full-run public read-only research is enabled unless the user explicitly excludes it. Do not require a second framework approval.

If tools require approval, log waiting_approval and ask through the host mechanism. Silence is not refusal. Record `declined` only for an actual user decision; otherwise distinguish unavailable, error, no_results, partial and completed. Missing internal context or a Confluence error must not disable public research. External facts do not prove our internal strategy or customer willingness to pay.

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
Confluence MCP: completed | no_results | unavailable | auth_error | error | waiting_approval | declined

## Local Signals from Knowledge Base
- [finding] — signal: strong|weak|none — evidence_id: EVID-NNN — evidence_type: ... — source: [path]

## Confluence Signals
- [finding] — signal: strong|weak|none — source: [page title](url)

## External Market Signals
- [finding] — signal: strong|weak|none — source: [reference]
  or: [actual coverage status and specific reason]

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

## Evidence quality gate

Read `FRAMEWORK_DIR/implementations/run-quality.md`. Maintain the claim ledger for new protocol-2 runs; preserve source lineage, numerical scope and original intent. Correct upstream errors rather than copying them. Before completion, reconcile claims in this output against actual source anchors. Human Report completion requires `run_control.py finish --run-dir <RUN_DIR>`; PASS from repository examples is not a run check.
