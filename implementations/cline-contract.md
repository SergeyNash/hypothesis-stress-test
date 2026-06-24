Language: **English** | [Русский](./cline-contract.ru.md)

# Cline Contract

This document defines how the Hypothesis Stress Test framework maps to Cline.

## Mapping

| Framework concept | Cline implementation |
|-----------------|---------------------|
| Layer invariants | `.clinerules/*.md` |
| Layer execution | `.cline/skills/*/SKILL.md` |
| End-to-end run | `.clinerules/workflows/run-hypothesis.md` |
| Local evidence retrieval | `local-knowledge-retrieval` skill + KB files |
| Artifacts | Files under `RUN_DIR/outputs/` |

## Components

### Rules (always active)

Located in `.clinerules/`:

| File | Purpose |
|------|---------|
| `00-hypothesis-framework.md` | Framework overview, layer order |
| `10-artifact-contracts.md` | RUN_DIR structure, naming, markers |
| `20-evidence-rules.md` | KB evidence + Confluence + external/inferred channel rules |

### Skills (on-demand)

Located in `.cline/skills/`:

| Skill | Trigger |
|-------|---------|
| `conversational-hypothesis-intake` | Chat-first hypothesis collection before bootstrap |
| `hypothesis-input-validation` | Before any layer run |
| `hypothesis-facilitator` | Facilitator (Roles Layer / stress test) |
| `local-knowledge-retrieval` | Local Evidence Discovery (preview + inventory) |
| `hypothesis-market-layer` | Market Layer with KB inventory + Confluence MCP |
| `hypothesis-synthesis` | Synthesis Layer (signal collision) |
| `customer-discovery-planning` | Customer Discovery Planning (interview-ready research plan) |
| `hypothesis-decision-review` | Decision Review (mandatory gate) |
| `human-report-export` | Human Decision Report Export (`human_report.html`) |

### Workflows (slash commands)

Located in `.clinerules/workflows/`:

| Workflow | Command |
|----------|---------|
| `run-hypothesis-conversational.md` | `/run-hypothesis-conversational.md` |
| `validate-hypothesis-input.md` | `/validate-hypothesis-input.md` |
| `run-facilitator.md` | `/run-facilitator.md` |
| `run-knowledge-retrieval.md` | `/run-knowledge-retrieval.md` |
| `run-hypothesis.md` | `/run-hypothesis.md` |
| `run-market-layer.md` | `/run-market-layer.md` |
| `run-synthesis.md` | `/run-synthesis.md` |
| `run-customer-discovery-planning.md` | `/run-customer-discovery-planning.md` |
| `run-decision-review.md` | `/run-decision-review.md` |
| `run-human-report-export.md` | `/run-human-report-export.md` |

## Execution flow

### Chat-first (recommended)

```text
User describes hypothesis in chat
  → conversational intake (skill) → draft card → user confirms
  → bootstrap RUN_DIR + input/hypothesis.md
  → validate input (skill or workflow)
  → full pipeline via /run-hypothesis.md
  → Human backlog decision
```

### File-first (fallback)

```text
User provides RUN_DIR
  → validate input (skill or workflow)
  → Facilitator (skill) → role_outputs + summary + validation_questions + marker
  → Local Evidence Discovery (skill) → discovery_preview + evidence_inventory + marker
  → Market Layer (skill + inventory + Confluence MCP) → market_analysis + marker
  → Synthesis (hypothesis-synthesis) → hypothesis_map + digest + marker
  → Customer Discovery Planning (skill) → customer_discovery_plan + marker
  → Decision Review (skill) → decision_review + marker
  → Human Decision Report Export (skill) → human_report.html + marker
  → Human backlog decision
```

## Prerequisites

1. [Cline VS Code extension](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev) installed
2. Project opened in VS Code (rules and skills auto-discovered)
3. Confluence MCP configured (recommended for Market Layer) — see [confluence-mcp.md](./confluence-mcp.md)

## Fallback: manual mode

Without Cline, copy templates from `templates/` and run layers manually in any LLM interface. See [playbooks/run-hypothesis.md](../playbooks/run-hypothesis.md).
