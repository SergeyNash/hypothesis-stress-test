Language: **English** | [Русский](./README.ru.md)

# Knowledge Base

The Market Layer retrieves **local signals** primarily from **Confluence** via MCP.

## Primary source: Confluence

Configure Confluence MCP before running Market Layer. See:

```text
implementations/confluence-mcp.md
```

## What to search in Confluence

When stress-testing a hypothesis, search for:

- Customer discovery notes and interview summaries
- Product requirement discussions
- Architecture decision records
- Past hypothesis or initiative evaluations
- Support or operational pain reports
- Competitive analysis stored internally

## Signal labeling

All Confluence findings go into `market_analysis.md` under **Local Signals (Confluence)** with:

- Signal strength: strong / weak / none
- Source citation (page title + URL)

## Without Confluence

If MCP is not configured, Market Layer documents `missing local evidence`. External sources are secondary and require explicit user approval.

## Future extensions

Optional secondary sources (not required for v1):

- Jira work items
- Internal wikis beyond Confluence
- Local research repositories in this repo
