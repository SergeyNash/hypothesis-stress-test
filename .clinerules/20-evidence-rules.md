# Evidence Rules

These rules apply to **Market Layer** and any MCP-backed research.

## Signal types

Every finding in `market_analysis.md` must be labeled:

| Type | Source | Trust |
|------|--------|-------|
| **local** | Confluence (primary), internal docs | Highest |
| **external** | Public sources, articles, vendor docs | Medium — cite URL |
| **inferred** | Logical conclusion from available data | Lowest — mark explicitly |

## Confluence-first (MCP)

For Market Layer:

1. **First** search Confluence via MCP for local signals related to the hypothesis.
2. Cite each Confluence page: title, space, URL or page ID.
3. If Confluence returns no relevant results, state `missing local evidence` explicitly.
4. Only then use external sources or mark gaps.

## Core rules

- **No evidence → no claim**
- Distinguish facts from assumptions
- Prefer uncertainty over hallucination
- Do not invent market demand
- Do not generalize without support

## market_analysis.md structure

```markdown
# Market Analysis

## Local Signals (Confluence)
- [finding] — signal: strong|weak|none — source: [page title](url)

## External Signals
- [finding] — signal: strong|weak|none — source: [reference]

## Inferred Signals
- [finding] — signal: strong|weak|none — basis: [what it was inferred from]

## Signal Summary
- Overall local signal: strong|weak|none
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
- Mark all local signals as `missing local evidence`
- Proceed with external research only if the user explicitly requests it
- Do not fabricate internal knowledge

## Decision Review

Decision Review applies to **Synthesis outputs only**:

- Do not generate new market or role signals
- Do not cite sources not already present in prior artifacts
- Challenge evidence quality, assumptions, and conclusions — do not repeat synthesis
- Propose validation activities; do not treat them as completed evidence
