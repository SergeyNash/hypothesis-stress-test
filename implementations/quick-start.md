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

## Step 2. Open your project

**Recommended:** open **your knowledge base** as the main project and add a `hypothesis-stress-test/` folder with the full framework repo. Details — [Knowledge base and workspace](#knowledge-base-and-workspace).

**Alternative:** open only the framework repository:

```text
git clone <repo-url>
code hypothesis-stress-test
```

Cline auto-discovers from the **workspace root**:

- Rules from `.clinerules/` (including `workflows/` — slash commands)
- Skills from `.cline/skills/`

Check the Cline panel: Rules icon (scales) — framework rules should be listed and enabled.

---

## Knowledge base and workspace

Your knowledge base and the framework wrapper are **different things**. You do **not** need two separate VS Code windows.

| What | Source | Depends on open project? |
| ------ | -------- | -------------------------- |
| Wrapper (rules, skills, workflows) | `.clinerules/`, `.cline/skills/` | **Yes** — from open workspace root only |
| Confluence (wiki) | Confluence MCP in Cline | **No** — configured once, works in any workspace |
| Local KB files | Markdown notes in a repo | **Yes** — Cline reads files in the open project |
| Run artifacts | `RUN_DIR/outputs/` | Any folder **inside** the open workspace |

The `knowledge-base/` folder in this repo is **documentation** about Confluence search — not your personal knowledge base.

### Option A (recommended): KB as main project + `hypothesis-stress-test/` folder

You already have a project open — **your knowledge base**. Add a folder with the full framework repository:

```text
my-knowledge-base/                    ← open in VS Code
  discovery/                          ← your KB: notes, interviews, research
  knowledge-base/
    interviews/                        ← raw CustDev notes and interview summaries
    persona-builds/                    ← logs of persona rebuilds from evidence
    personas/                          ← reusable role profiles
  research/
  adr/
  runs/                               ← RUN_DIR for hypotheses (next to KB)
    HYP-2026-06-22-001/
      input/
        hypothesis.md
      outputs/
  hypothesis-stress-test/               ← full framework repository
    .clinerules/                      ← rules + workflows (/run-hypothesis.md)
    .cline/skills/                    ← per-layer skills
    templates/                        ← manual mode templates
    playbooks/
    examples/
    implementations/                  ← docs (quick start, MCP, setup)
    ...
```

Add the folder:

```bash
cd my-knowledge-base
git submodule add https://github.com/SergeyNash/hypothesis-stress-test.git hypothesis-stress-test
# or: git clone <repo-url> hypothesis-stress-test
```

**Important for Cline:** rules and skills are discovered at the **workspace root**, not inside a nested folder. After adding `hypothesis-stress-test/`, do one of the following:

**A1 — symlinks at KB root (good for submodules):**

```bash
# Windows (cmd as admin) or mklink in PowerShell
mklink /D .clinerules hypothesis-stress-test\.clinerules
mklink /D .cline hypothesis-stress-test\.cline
```

**A2 — copy dot-folders to KB root** (if symlinks are not an option):

```bash
cp -r hypothesis-stress-test/.clinerules .
cp -r hypothesis-stress-test/.cline .
```

Benefits: one window; KB and framework side by side; `runs/` lives in your project; docs always at `hypothesis-stress-test/implementations/`.

### Option B: multi-root workspace

Two repos, one VS Code window. Create `my-work.code-workspace`:

```json
{
  "folders": [
    { "path": "my-knowledge-base", "name": "KB" },
    { "path": "hypothesis-stress-test", "name": "Framework" }
  ]
}
```

Cline picks up rules/skills from the `hypothesis-stress-test` root. `RUN_DIR` — in KB: `runs/HYP-2026-06-22-001/`. Context via `@discovery/...`.

### Option C: hypothesis-stress-test only

Open the framework repo as workspace. Best when KB is mainly in **Confluence**, not local files.

### How to connect knowledge sources

**Confluence (primary path):**

1. Configure Confluence MCP — [confluence-mcp.md](./confluence-mcp.md).
2. Market Layer searches Confluence during `/run-market-layer.md` or a full run.
3. Results go to `market_analysis.md` as **Local Signals (Confluence)**.

**Local files:**

- Open the repository containing your notes (option A or B).
- Cline reads them during Market Layer via file tools.
- Label such findings as **local** in `market_analysis.md` (source: file path).

**Personas and interviews:**

- Store raw CustDev materials in `knowledge-base/interviews/`.
- Store current reusable role profiles in `knowledge-base/personas/`.
- Store rebuild logs in `knowledge-base/persona-builds/`.
- Roles Layer can use matching personas as supporting context.
- A persona without linked `source_interviews` is a weak local signal, not primary evidence.

Without Confluence and without local files in the workspace, Market Layer will record `missing local evidence`.

---

## Step 3. Configure Confluence MCP

Market Layer searches **local signals** in Confluence first.

Minimal setup: [confluence-mcp.md](./confluence-mcp.md).

Without Confluence, Market Layer marks `missing local evidence` — the run still works, but without internal data.

---

## Step 4. Create RUN_DIR

```text
runs/HYP-2026-06-22-001/
  input/
    hypothesis.md
    attachments/
```

Minimal `input/hypothesis.md` example:

```markdown
# Hypothesis

## Metadata

- Hypothesis ID: HYP-2026-06-22-001
- Created at: 2026-06-22
- Run ID: RUN-2026-06-22-001
- Status: draft

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

Full schema: `hypothesis-stress-test/templates/input-schema.md` (or [templates/input-schema.md](../templates/input-schema.md) if workspace = framework).

Example: `hypothesis-stress-test/examples/example-001/input/hypothesis.md`

If `knowledge-base/personas/` contains matching role profiles, the Roles Layer can use them as supporting context. The role list in `input/hypothesis.md` still defines the scope for the current run.

---

## Step 5. Run

In Cline chat:

```text
RUN_DIR: runs/HYP-2026-06-22-001
/run-hypothesis.md
```

Cline will:

1. Validate input
2. Run Facilitator (Roles Layer)
3. Run Market Layer (with Confluence search)
4. Run Synthesis Layer
5. Run Customer Discovery Planning
6. Run Decision Review

Approve file writes and MCP tool calls when prompted.

---

## Step 6. Read the result

Start with:

```text
runs/HYP-2026-06-22-001/outputs/hypothesis_digest.txt
```

Full analysis:

```text
outputs/
  role_outputs/*
  hypothesis_summary.md
  validation_questions.md
  market_analysis.md
  hypothesis_map.md
  hypothesis_digest.txt
  customer_discovery_plan.md
  decision_review.md
```

| Artifact | Contents |
| ---------- | ---------- |
| `hypothesis_digest.txt` | Short digest (max 150 words): viability, conflict, illusion, blind spot, next step |
| `hypothesis_map.md` | Signal collision: divergences, blind spots, new information, applicability, reframe impact |
| `customer_discovery_plan.md` | Interview-ready CustDev plan: unknowns, priorities, target roles, interview guide |
| `decision_review.md` | Adversarial review: confidence, risks, validation plan |
| `market_analysis.md` | Internal and external signals with sources |

---

## Troubleshooting

| Issue | Fix |
| ------- | ----- |
| Rules not visible | Check `.clinerules/` at **workspace root** (symlink from `hypothesis-stress-test/`); reload VS Code |
| Workflow does not start | Specify `RUN_DIR:` explicitly in your message |
| Confluence MCP fails | [confluence-mcp.md](./confluence-mcp.md) |
| Missing outputs | Check which layer did not finish (marker files in `outputs/`) |

---

## Next steps

- [cline-setup.md](./cline-setup.md) — full Cline setup
- [playbooks/run-hypothesis.md](../playbooks/run-hypothesis.md) — detailed run playbook
- [examples/example-001/](../examples/example-001/) — canonical example with artifacts
