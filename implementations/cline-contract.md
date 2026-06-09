Language: **English** | [Русский](./cline-contract.ru.md)

# Cline Contract

This document defines how the Hypothesis Stress Test framework maps to Cline.

## Mapping

| Framework concept | Cline implementation |
|-----------------|---------------------|
| Layer invariants | `.clinerules/*.md` |
| Layer execution | `.cline/skills/*/SKILL.md` |
| End-to-end run | `.clinerules/workflows/run-hypothesis.md` |
| Local knowledge (Market) | Confluence MCP |
| Artifacts | Files under `RUN_DIR/outputs/` |

## Components

### Rules (always active)

Located in `.clinerules/`:

| File | Purpose |
|------|---------|
| `00-hypothesis-framework.md` | Framework overview, layer order |
| `10-artifact-contracts.md` | RUN_DIR structure, naming, markers |
| `20-evidence-rules.md` | Confluence-first evidence, signal types |

### Skills (on-demand)

Located in `.cline/skills/`:

| Skill | Trigger |
|-------|---------|
| `hypothesis-input-validation` | Before any layer run |
| `hypothesis-roles-layer` | Roles Layer execution |
| `hypothesis-market-layer` | Market Layer with Confluence MCP |
| `hypothesis-synthesis-layer` | Synthesis Layer |

### Workflows (slash commands)

Located in `.clinerules/workflows/`:

| Workflow | Command |
|----------|---------|
| `validate-hypothesis-input.md` | `/validate-hypothesis-input.md` |
| `run-hypothesis.md` | `/run-hypothesis.md` |
| `run-market-layer.md` | `/run-market-layer.md` |
| `run-synthesis.md` | `/run-synthesis.md` |

## Execution flow

```text
User provides RUN_DIR
  → validate input (skill or workflow)
  → Roles Layer (skill) → role_outputs + summary + marker
  → Market Layer (skill + Confluence MCP) → market_analysis + marker
  → Synthesis Layer (skill) → hypothesis_map + digest + marker
```

## Prerequisites

1. [Cline VS Code extension](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev) installed
2. Project opened in VS Code (rules and skills auto-discovered)
3. Confluence MCP configured (recommended for Market Layer) — see [confluence-mcp.md](./confluence-mcp.md)

## Fallback: manual mode

Without Cline, copy templates from `templates/` and run layers manually in any LLM interface. See [playbooks/run-hypothesis.md](../playbooks/run-hypothesis.md).
