Language: **English** | [Русский](./quick-start.ru.md)

# Quick Start

Short path from Cline installation to your first hypothesis run in 10–15 minutes.

Full documentation: [README.md](../README.md)

---

## Prerequisites

- VS Code
- [Cline](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev)
- LLM provider API key (or local model)
- Confluence MCP (recommended) — [confluence-mcp.md](./confluence-mcp.md)

---

## Step 1. Install Cline

1. Open VS Code → Extensions → search **Cline** → Install.
2. Configure your LLM provider and API key in Cline settings.

---

## Step 2. Open the repository

```text
git clone <repo-url>
code hypothesis-stress-test
```

Cline auto-discovers:

- Rules from `.clinerules/`
- Skills from `.cline/skills/`
- Workflows from `.clinerules/workflows/`

Check the Cline panel: Rules icon (scales) — framework rules should be listed and enabled.

> You do **not** have to keep `hypothesis-stress-test` as your only open project. See [Knowledge base and workspace](#knowledge-base-and-workspace) below.

---

## Knowledge base and workspace

Your knowledge base and the framework wrapper are **different things**. You do **not** need two separate VS Code windows.

| What | Source | Depends on open project? |
|------|--------|--------------------------|
| Wrapper (rules, skills, workflows) | `.clinerules/`, `.cline/skills/` | **Yes** — from open workspace root only |
| Confluence (wiki) | Confluence MCP in Cline | **No** — configured once, works in any workspace |
| Local KB files | Markdown notes in a repo | **Yes** — Cline reads files in the open project |
| Run artifacts | `RUN_DIR/outputs/` | Any folder **inside** the open workspace |

The `knowledge-base/` folder in this repo is **documentation** about Confluence search — not your personal knowledge base.

### Option A (recommended): your KB as the main project

If your knowledge lives in a separate repository, make it the primary workspace and add the framework:

```text
my-knowledge-base/
  .clinerules/          ← copy or git submodule from hypothesis-stress-test
  .cline/skills/
  discovery/            ← your notes, interviews, research
  research/
  adr/
  runs/                 ← RUN_DIR for hypotheses
    my-hypothesis-001/
      hypothesis.md
      outputs/
```

Benefits: one VS Code window; Cline sees both KB and rules/skills; Market Layer reads **local files** and **Confluence via MCP**.

### Option B: multi-root workspace (two repos)

Create `my-work.code-workspace`:

```json
{
  "folders": [
    { "path": "../my-knowledge-base" },
    { "path": "../hypothesis-stress-test" }
  ]
}
```

Open the `.code-workspace` file — both projects in one window. `RUN_DIR` can live in `hypothesis-stress-test/runs/` while context comes from `@my-knowledge-base/discovery/...`.

### Option C: hypothesis-stress-test only

As in the steps below. Best when internal knowledge is mainly in **Confluence**, not local files.

### How to connect knowledge sources

**Confluence (primary path):**

1. Configure Confluence MCP — [confluence-mcp.md](./confluence-mcp.md).
2. Market Layer searches Confluence during `/run-market-layer.md` or a full run.
3. Results go to `market_analysis.md` as **Local Signals (Confluence)**.

**Local files:**

- Open the repository containing your notes (option A or B).
- Cline reads them during Market Layer via file tools.
- Label such findings as **local** in `market_analysis.md` (source: file path).

Without Confluence and without local files in the workspace, Market Layer will record `missing local evidence`.

---

## Step 3. Configure Confluence MCP

Market Layer searches **local signals** in Confluence first.

Minimal setup: [confluence-mcp.md](./confluence-mcp.md).

Without Confluence, Market Layer marks `missing local evidence` — the run still works, but without internal data.

---

## Step 4. Create RUN_DIR

```text
runs/my-hypothesis/
  hypothesis.md
```

Minimal `hypothesis.md` example:

```markdown
# Hypothesis

## Statement

If [action], then [expected outcome for a specific audience].

## Relevant Roles

* Role 1
* Role 2

## Research Context

* Domain: [domain]
* Target audience: [audience]
* Scenario: [scenario]
```

Full schema: [templates/input-schema.md](../templates/input-schema.md)

Or copy the example: [examples/example-001/hypothesis.md](../examples/example-001/hypothesis.md)

---

## Step 5. Run

In Cline chat:

```text
RUN_DIR: runs/my-hypothesis
/run-hypothesis.md
```

Cline will:

1. Validate input
2. Run Roles Layer
3. Run Market Layer (with Confluence search)
4. Run Synthesis Layer

Approve file writes and MCP tool calls when prompted.

---

## Step 6. Read the result

Start with:

```text
runs/my-hypothesis/outputs/hypothesis_digest.txt
```

Full analysis:

```text
outputs/
  role_outputs/*
  hypothesis_summary.md
  market_analysis.md
  hypothesis_map.md
  hypothesis_digest.txt
```

| Artifact | Contents |
|----------|----------|
| `hypothesis_digest.txt` | Short summary: classification, conflict, next step |
| `hypothesis_map.md` | Full synthesis: contradictions and decision boundaries |
| `market_analysis.md` | Internal and external signals with sources |

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Rules not visible | Reload VS Code window; check `.clinerules/` exists |
| Workflow does not start | Specify `RUN_DIR:` explicitly in your message |
| Confluence MCP fails | [confluence-mcp.md](./confluence-mcp.md) |
| Missing outputs | Check which layer did not finish (marker files in `outputs/`) |

---

## Next steps

- [cline-setup.md](./cline-setup.md) — full Cline setup
- [playbooks/run-hypothesis.md](../playbooks/run-hypothesis.md) — detailed run playbook
- [examples/example-001/](../examples/example-001/) — canonical example with artifacts
