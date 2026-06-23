Language: **English** | [Русский](./README.ru.md)

# Knowledge Base

Your personal knowledge base is a **separate project** (notes, discovery, research). Add the framework as a `hypothesis-stress-test/` folder inside it. See [quick-start.md](../implementations/quick-start.md#knowledge-base-and-workspace).

The framework now separates local retrieval and analysis:

- **Local Evidence Discovery** collects file-based local evidence into `discovery_preview.md` and `evidence_inventory.md`.
- **Market Layer** interprets inventory + Confluence + external signals.

## Primary source: Confluence

Configure Confluence MCP before running Market Layer. See:

```text
implementations/confluence-mcp.md
```

## What to search in Confluence

When stress-testing a hypothesis, search for:

- Customer discovery notes and interview summaries
- Persona source materials and role research
- Product requirement discussions
- Architecture decision records
- Past hypothesis or initiative evaluations
- Support or operational pain reports
- Competitive analysis stored internally

## Local persona model

The repository can store local role knowledge in three layers:

```text
knowledge-base/
  interviews/      raw CustDev notes and interview summaries
  persona-builds/  rebuild logs explaining how personas changed
  personas/        current reusable role profiles
```

`personas/` are synthesized artifacts. They should not be treated as raw evidence.

If a persona has no linked `source_interviews`, treat it as a weak local signal. If a persona is rebuilt from interviews, cite the underlying interviews or persona build when using it as local evidence.

## Signal labeling

Market findings should keep channels separated:

- `Local Signals from Knowledge Base`
- `Confluence Signals`
- `External Market Signals`
- `Inferred Signals`

All Confluence findings go into `market_analysis.md` under **Confluence Signals** with:

- Signal strength: strong / weak / none
- Source citation (page title + URL)

## Without Confluence

If MCP is not configured:

- Local KB inventory can still provide local file evidence
- Market Layer should mark Confluence channel as missing
- External sources remain secondary and require explicit user approval

## Future extensions

Optional secondary sources (not required for v1):

- Jira work items
- Internal wikis beyond Confluence
- Local research repositories in this repo
