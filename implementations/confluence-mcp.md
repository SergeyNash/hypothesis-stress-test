Language: **English** | [Русский](./confluence-mcp.ru.md)

# Confluence MCP Setup

Confluence is the **primary MCP source** for local signals in the Market Layer.

## Why Confluence first

Internal Confluence often contains:

- Real user problems and discovery notes
- Past product decisions
- Architectural constraints
- Customer research artifacts
- Historical hypothesis discussions

This is more reliable than generic external sources for **local signals**.

## Recommended: Atlassian Rovo MCP Server (official)

For **Confluence Cloud** with OAuth 2.1:

### Prerequisites

- Atlassian Cloud site with Confluence
- Node.js 18+ (for `mcp-remote` proxy)
- Cline VS Code extension

### Cline configuration

1. Open Cline panel → **MCP Servers** icon (stacked servers in toolbar).
2. Open **Configure** tab → **Configure MCP Servers**.
3. Add the Atlassian remote server:

```json
{
  "mcpServers": {
    "atlassian": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote@latest",
        "https://mcp.atlassian.com/v1/mcp/authv2"
      ],
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

4. Restart the MCP server and complete OAuth in the browser when prompted.
5. Verify Confluence search/read tools appear in the tool list.

> **Note:** Use endpoint `https://mcp.atlassian.com/v1/mcp/authv2` (not the legacy `/sse` endpoint).

Docs: [Atlassian Rovo MCP Server](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/)

## Alternative: Community Confluence MCP (API token)

For environments where OAuth is not available, use a community server with API token auth.

### Example: mcp-atlassian

```json
{
  "mcpServers": {
    "mcp-atlassian": {
      "command": "uvx",
      "args": ["mcp-atlassian"],
      "env": {
        "CONFLUENCE_URL": "https://your-company.atlassian.net/wiki",
        "CONFLUENCE_USERNAME": "your.email@company.com",
        "CONFLUENCE_API_TOKEN": "your_api_token"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

Generate API token: Atlassian Account Settings → Security → API tokens.

Docs: [mcp-atlassian](https://github.com/sooperset/mcp-atlassian)

### Server / Data Center

Use Personal Access Token (PAT) instead of username + API token. See your server's MCP documentation.

## How Market Layer uses Confluence

When running Market Layer (`hypothesis-market-layer` skill or `/run-market-layer.md`):

1. Search Confluence for pages related to:
   - The hypothesis domain and scenario
   - Similar problems or past initiatives
   - User research and customer feedback
   - Architectural or process constraints

2. For each relevant finding, record in `market_analysis.md`:

```markdown
## Local Signals (Confluence)

- [finding description]
  - signal: strong | weak | none
  - type: local
  - source: [Page Title](https://your-site.atlassian.net/wiki/spaces/...)
```

3. If no relevant pages found — state explicitly:

```markdown
## Local Signals (Confluence)

No relevant local evidence found.

- signal: none
- note: Confluence search returned no matches for [query terms]
```

## Without Confluence MCP

Market Layer can still run, but must document:

```markdown
## MCP Status
Confluence MCP: not configured

## Local Signals (Confluence)
missing local evidence — MCP not available
```

Do not fabricate internal knowledge. External signals may be used if the user approves.

## Security

| Rule | Detail |
|------|--------|
| Credentials | Environment variables or Cline MCP config only — never commit to repo |
| autoApprove | Limit to read-only search/get operations |
| Permissions | MCP respects user's existing Confluence access |
| Write tools | Disable or do not auto-approve Confluence write operations for analysis runs |

## Secondary MCP sources (future)

These are optional extensions, not required for v1:

- Jira / Linear — linked work items
- Slack — informal discussions
- Web search — external market signals
- Filesystem — local repo artifacts

Confluence remains the primary local signal source.
