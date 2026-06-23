# Evidence Rules

These rules apply to **Local Evidence Discovery**, **Market Layer**, and any MCP-backed research.

## Signal types

Every finding in `market_analysis.md` must be labeled:

| Type | Source | Trust |
| ------ | -------- | ------- |
| **local** | KB evidence inventory + Confluence | Highest |
| **external** | Public sources, articles, vendor docs | Medium — cite URL |
| **inferred** | Logical conclusion from available data | Lowest — mark explicitly |

## Local Evidence Discovery (KB files)

Before Market interpretation, retrieval should produce:

- `discovery_preview.md`
- `evidence_inventory.md`

Inventory rules:

- one item = one atomic signal
- no synthesis language in `observation`
- preserve source traceability (`EVID-NNN`, path, anchor)
- keep `evidence_type` and `relevance_reason`
- `metadata_only` is a gap marker, not factual proof

## Confluence (MCP)

For Market Layer:

1. Read `evidence_inventory.md` if available and map KB-local findings.
2. Search Confluence via MCP for additional internal signals.
3. Cite each Confluence page: title, space, URL or page ID.
4. If Confluence returns no relevant results, state it explicitly in Confluence section.
5. Only then use external sources or mark gaps.

## Core rules

- **No evidence → no claim**
- Distinguish facts from assumptions
- Prefer uncertainty over hallucination
- Do not invent market demand
- Do not generalize without support

## Persona evidence

Personas in `knowledge-base/personas/` are synthesized role artifacts.

- If `source_interviews` is empty, treat the persona as a weak local signal
- If a persona cites interviews or persona builds, cite the underlying source when making claims
- Do not treat persona statements as primary evidence unless they are backed by CustDev materials

## market_analysis.md structure

```markdown
# Market Analysis

## Local Signals from Knowledge Base
- [finding] — signal: strong|weak|none — evidence_id: EVID-NNN — evidence_type: ... — source: [path]

## Confluence Signals
- [finding] — signal: strong|weak|none — source: [page title](url)

## External Market Signals
- [finding] — signal: strong|weak|none — source: [reference]

## Inferred Signals
- [finding] — signal: strong|weak|none — basis: [what it was inferred from]

## Signal Summary
- Overall local KB signal: strong|weak|none
- Overall confluence signal: strong|weak|none
- Overall external signal: strong|weak|none
- Missing evidence: [list gaps]
```

## MCP security

- Store credentials in environment variables only — never in repo files.
- Use read-only Confluence tools where possible.
- Limit `autoApprove` to safe read operations.
- Respect existing Confluence permission boundaries.

## Without Confluence MCP

If Confluence MCP is not configured:

- Add a section `## MCP Status` with `Confluence MCP: not configured`
- Keep KB-local signals from inventory (if present)
- Mark Confluence channel as missing (`Confluence local evidence missing`)
- Proceed with external research only if the user explicitly requests it
- Do not fabricate internal knowledge

## Decision Review

Decision Review applies to **Synthesis + Customer Discovery Planning outputs only**:

- Do not generate new market or role signals
- Do not cite sources not already present in prior artifacts
- Challenge evidence quality, assumptions, and conclusions — do not repeat synthesis
- Propose validation activities; do not treat them as completed evidence
