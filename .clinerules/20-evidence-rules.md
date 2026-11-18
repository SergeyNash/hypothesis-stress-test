# Evidence Rules

Apply these rules when collecting evidence and when a decisive claim is carried into synthesis, review or either final report.

## Signal types

Every finding in `market_analysis.md` must be labeled:

| Type | Source | Trust |
| ------ | -------- | ------- |
| **local** | KB evidence inventory + Confluence | Assess directness, provenance, age and relevance |
| **external** | Public sources, articles, vendor docs | Assess primary source and independence — cite URL |
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

When a simulated persona speaks to a decisive unknown, turn its statement into a concrete question for a real participant and include that question in the findings or next check. Even agreement among several roles adds no empirical support. If a profile references interviews, trace the claim to the relevant passage in an underlying interview. Count that interview once across the profile, build notes and direct citation. If the passage is unavailable, leave the claim open.

## Scope of a decisive claim

Match the actor, action and scope of the claim to a short passage (source + location). Record exactly what it supports and what remains unknown. Distinguish conditions for a pilot, a supplier’s sales plan, willingness to pay, approval of funds for a specified purpose and actual payment. Name the open questions that affect the decision. If only part is supported, narrow the claim itself in the synthesis, decision review and both reports. Preserve the original hypothesis as submitted.

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
- Continue public research included in the full-run request unless explicitly excluded; Confluence availability does not control the external channel.
- Do not fabricate internal knowledge

## Decision Review

Decision Review may reference the existing **Roles, Local Evidence, Business Context, Market, Synthesis, and Customer Discovery Planning** artifacts to challenge conclusions and evaluate the quality of the recommendation.

- Do not perform new local retrieval, Confluence searches, external research, market research, or role analysis
- Do not generate new signals or introduce facts not already cited in prior artifacts
- Every factual challenge must remain traceable to an existing artifact and its cited evidence
- Missing evidence or a missing perspective is a gap to report and validate later, not permission to fill it with uncited information
- Challenge evidence quality, assumptions, and conclusions — do not repeat synthesis
- Propose validation activities; do not treat them as completed evidence

## Service evidence and provenance

For service_business use the evidence fields and caveats from profiles/service-business.md. Local storage is not a trust rank: assess source directness, independence, sample, age and relevance. A contract demonstrates an obligation, not actual delivery; time saved is not automatically cash saved. Synthetic fixtures and role simulations cannot validate real demand. Read sources through available client tools. If a format cannot be read, disclose the limitation and ask for an export or another available source. Partial reading and formula text must not become complete numeric evidence.

## Public research and source coverage

Use `external-business-research` for a named external question that can change the decision, during Business Context or Market. Reuse existing sources; do not automatically commission a full market/company study for an internal improvement. A full-run request permits ordinary passive search in the agreed channel; it does not require exhausting every channel or gap. Stop at an answer or an explicit gap with its impact. Do not add a second framework approval gate. Host permissions remain authoritative; waiting approval is not refusal. Record actual queries/read results and references separately from plans, including no_results, unavailable, auth_error and explicit declined. Notify the user of channel failure when it happens. Never log credentials, cookies, headers or access tokens. Public evidence does not substitute for internal strategy or customer validation.
