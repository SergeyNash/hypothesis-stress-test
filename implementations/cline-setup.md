Language: **English** | [Русский](./cline-setup.ru.md)

# Cline Setup

Step-by-step guide to run Hypothesis Stress Test with Cline in VS Code.

## 1. Install Cline

1. Open VS Code.
2. Go to Extensions → search **Cline**.
3. Install [Cline](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev).
4. Configure your LLM provider in Cline settings (API key or local model).

## 2. Open your project

### Recommended: KB + `hypothesis-stress-test/` folder

Open **your knowledge base** and add the full framework repository inside it:

```text
my-knowledge-base/
  discovery/                 ← your KB
  runs/                      ← hypothesis runs
  hypothesis-stress-test/      ← clone or git submodule
    .clinerules/
    .cline/skills/
    templates/
    implementations/
    ...
```

Cline looks for `.clinerules/` and `.cline/` at the **workspace root**. After adding the nested folder, create a symlink or copy at KB root — see [quick-start.md](./quick-start.md#knowledge-base-and-workspace).

### Alternative: framework only

```text
git clone <repo-url>
code hypothesis-stress-test
```

Cline auto-discovers from root:

- Rules from `.clinerules/` (including `workflows/`)
- Skills from `.cline/skills/`

Verify in Cline panel:

- **Rules** (scale icon) — framework rules should be listed and enabled
- Skills — `hypothesis-*` skills should appear when relevant

## 3. Configure Confluence MCP (recommended)

See [confluence-mcp.md](./confluence-mcp.md).

Without Confluence, Market Layer will mark `missing local evidence`.

## 4. Run a hypothesis

### Chat-first (recommended)

In Cline chat:

```text
/run-hypothesis-conversational.md

Describe your hypothesis in natural language.
```

Use `#context` for dirty discovery notes. Use `#new-run` when a previous run exists the same day.  
`runs/` is created only after **two** confirms: draft + proposed RUN_DIR. See [examples/chat-first-run.md](../examples/chat-first-run.md).

### File-first (fallback)

Create a run directory:

```text
runs/HYP-2026-06-22-001/
  input/
    hypothesis.md
```

Use `templates/input-schema.md` as reference for `input/hypothesis.md` format.

Or copy the example:

```text
examples/example-001/
```

## 5. Run a hypothesis (file-first)

In Cline chat, type:

```text
/run-hypothesis.md
```

Or step by step:

```text
/validate-hypothesis-input.md
```

Then ask Cline to run each layer, or use individual workflows:

```text
/run-facilitator.md
/run-market-layer.md
/run-synthesis.md
/run-customer-discovery-planning.md
/run-decision-review.md
/run-human-report-export.md
```

Specify `RUN_DIR` in your message, e.g.:

```text
RUN_DIR: runs/HYP-2026-06-22-001
/run-hypothesis.md
```

## 6. Review outputs

Check `RUN_DIR/outputs/`:

```text
outputs/
  role_outputs/*
  hypothesis_summary.md
  validation_questions.md
  discovery_preview.md
  evidence_inventory.md
  market_analysis.md
  hypothesis_map.md
  hypothesis_digest.txt
  customer_discovery_plan.md
  decision_review.md
  human_report.html
```

Open **`human_report.html`** in a browser for the decision-facing summary. For evidence traceability, inspect `discovery_preview.md` and `evidence_inventory.md` before reading `market_analysis.md`.

## Plan vs Act mode

- Use **Plan** mode to review the approach before file writes.
- Use **Act** mode to execute layers and write artifacts.
- Approve MCP tool calls (especially Confluence searches) when prompted.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Rules not visible | Reload VS Code window; check `.clinerules/` exists |
| Skills not triggering | Mention "hypothesis stress test" or use slash workflows |
| Confluence MCP fails | See [confluence-mcp.md](./confluence-mcp.md) troubleshooting |
| Missing outputs | Check which layer marker files are absent |

## Manual fallback

Copy templates from `templates/` and run in any LLM chat. See `playbooks/run-hypothesis.md`.
