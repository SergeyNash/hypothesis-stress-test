Language: **English** | [Русский](./chat-first-run.ru.md)

# Chat-First Run Example

This document walks through the **conversational (chat-first)** entry path: start a full hypothesis stress test from Cline chat without manually creating `RUN_DIR` or editing `input/hypothesis.md`.

File-first fallback: [run.md](./run.md) and [example-001/](./example-001/).

---

## Intake trigger tags

Place a tag at the start of your message (after the slash command) to control how the agent parses input:

| Tag | When to use |
| --- | ----------- |
| `#hypothesis` | You already have a clear If…then statement |
| `#context` | Dirty discovery notes, Q&A tables, CustDev paste |
| `#roles` | You listed roles; need help with statement and context |
| `#new-run` | Explicit new archive (implied when no `RUN_DIR:`) |

Aliases: `#гипотеза`, `#контекст`, `#discovery`, `#custdev`, `#роли`, `#новая`, `#новый-прогон`.

**Important:** `runs/` is created only after **two** confirms: (1) draft card (2) proposed `RUN_DIR`. Until then: `runs/ NOT created yet`. Agent must not write to an existing run when starting a new hypothesis.

---

## Prerequisites

1. Cline extension installed — [implementations/cline-setup.md](../implementations/cline-setup.md)
2. `.clinerules/` and `.cline/` at workspace root — [implementations/quick-start.md](../implementations/quick-start.md)
3. Confluence MCP configured (recommended) — [implementations/confluence-mcp.md](../implementations/confluence-mcp.md)

---

## Step 1 — Start in chat

In Cline chat (Example A — ready hypothesis):

```text
/run-hypothesis-conversational.md

If Application Security engineers can manually prioritize projects in the SAST scanning queue, then business-critical applications will be scanned first, reducing time to detect high-risk vulnerabilities.
```

The agent activates skill `conversational-hypothesis-intake`.

---

## Step 2 — Guided questions (if needed)

If the initial message is incomplete, the agent asks short questions, for example:

| Question | Example answer |
| -------- | -------------- |
| Who is directly affected? | AppSec Engineer, CISO |
| Domain? | Application Security |
| Target audience? | Security teams in mid-to-large enterprises |
| Scenario? | Queue-based SAST scan execution with competing project priorities |
| Constraints? (optional) | Must coexist with existing CI/CD pipelines |

Skip questions the user already answered in the first message.

---

## Step 3 — Draft card preview

The agent shows a canonical draft matching [templates/input-schema.md](../templates/input-schema.md):

```markdown
# Hypothesis

## Metadata

- Hypothesis ID: (assigned at bootstrap)
- Created at: (assigned at bootstrap)
- Run ID: (assigned at bootstrap)
- Status: draft

## Statement

If Application Security engineers can manually prioritize projects in the SAST scanning queue, then business-critical applications will be scanned first, reducing time to detect high-risk vulnerabilities.

## Relevant Roles

- AppSec Engineer
- CISO

## Research Context

- Domain: Application Security
- Target audience: Security teams in mid-to-large enterprises
- Scenario: Queue-based SAST scan execution with competing project priorities
- Constraints: Must coexist with existing CI/CD pipelines
```

---

## Step 4a — Confirm draft

The agent asks:

```text
Status: draft ready. runs/ NOT created yet.
Confirm draft / Revise / Cancel
```

User responds: **Confirm draft**

## Step 4b — RUN_DIR dialog

```text
Will create new run:
  RUN_DIR: runs/HYP-2026-06-23-001

Confirm create 001 / Specify other ID / Cancel
```

If `001` already exists from an earlier hypothesis today, agent proposes `002` and lists `001` as «will not modify».

User responds: **Confirm create**

No files are written until Step 4b completes.

---

## Step 5 — Automatic bootstrap

After RUN_DIR confirm, workflow creates the confirmed path, e.g.:

```text
runs/HYP-2026-06-23-001/
  input/
    hypothesis.md
    attachments/
  run.md
  outputs/
```

Metadata is assigned automatically:

- `Hypothesis ID`: `HYP-2026-06-23-001`
- `Run ID`: `RUN-2026-06-23-001`
- `Created at`: today's date
- `Status`: `draft` → `running` when pipeline starts

The agent tells the user which `RUN_DIR` was created.

---

## Step 6 — Validation

Skill `hypothesis-input-validation` checks `input/hypothesis.md`.

If validation fails, the agent returns to intake repair mode (targeted questions only), updates the file, and re-validates.

---

## Step 7 — Full pipeline

On validation pass, workflow invokes `/run-hypothesis.md` with the bootstrapped `RUN_DIR`:

1. Facilitator (Roles Layer)
2. Local Evidence Discovery
3. Market Layer
4. Synthesis Layer
5. Customer Discovery Planning
6. Decision Review

Same artifacts as file-first runs — see [run.md](./run.md).

---

## Step 8 — Read the result

Start with:

```text
runs/HYP-2026-06-23-001/outputs/hypothesis_digest.txt
```

Full outputs under `outputs/` — same structure as [example-001/outputs/](./example-001/outputs/).

---

## Revise or cancel

| User says | Behavior |
| --------- | -------- |
| Revise | Agent asks what to change; shows updated draft; waits for confirm again |
| Cancel | No `RUN_DIR` created; no pipeline started |

---

## Comparison with file-first

| | Chat-first | File-first |
| - | ---------- | ---------- |
| Entry | `/run-hypothesis-conversational.md` | Manual `input/hypothesis.md` + `/run-hypothesis.md` |
| RUN_DIR | Dialog-confirmed new archive | User-created |
| Confirm step | Draft + proposed RUN_DIR (two steps) | Implicit (user wrote the file) |
| Pipeline | Same `/run-hypothesis.md` after validation | Direct |

---

## Reference

- Skill: `.cline/skills/conversational-hypothesis-intake/SKILL.md`
- Workflow: `.clinerules/workflows/run-hypothesis-conversational.md`
- Schema: `templates/input-schema.md`
- Canonical completed example artifacts: `examples/example-001/`

---

## Example B — Dirty discovery context (`#context`)

Use when you have CustDev or sales notes, not a polished If…then statement.

### Step 1 — Start with tag

```text
/run-hypothesis-conversational.md
#context

Hypothesis for AppSec engineers, developers, and CISO:

What job does the client want to solve? Group scan projects with shared parameters (API + UI).
Additionally: individually configurable RBAC.
How do they solve it today? Manual per-project switching only.
What is missing? Project grouping + shared scan params + configurable role model.
Proposed implementation: UI and API changes.
```

### Step 2 — Extraction validation

Agent announces mode and shows mapping:

```text
Mode: #context (dirty discovery)

Extracted draft:

Statement:
If we add project grouping with shared scan parameters (API + UI) and configurable RBAC,
then AppSec engineers and developers can manage scan scope faster without manual per-project switching,
and the CISO gets more predictable governance.

Roles: AppSec Engineer, Developer, CISO
Domain: Application Security (SAST)
Scenario: Many scan projects without grouping or shared parameters

Correct? (yes / revise / cancel)
```

User: **yes**

### Step 3 — Draft card → two-step confirm → bootstrap

Same flow as Example A (Steps 3–8), with **two** confirm steps:

**4a — Draft:**

```text
Status: draft ready. runs/ NOT created yet.
Confirm draft / Revise / Cancel
```

User: **Confirm draft**

**4b — RUN_DIR dialog:**

```text
Will create new run:
  RUN_DIR: runs/HYP-2026-06-23-002

Already exists today:
  - runs/HYP-2026-06-23-001 (will not modify)

Confirm create 002 / Specify other ID / Cancel
```

User: **Confirm create 002** → `runs/HYP-2026-06-23-002/` is created.

---

## Example C — Second hypothesis same day (`#new-run`)

`runs/HYP-2026-06-23-001/` already has outputs from a previous hypothesis.  
You start a **new** hypothesis — agent must propose `002`, not write into `001`.

### Trigger

```text
/run-hypothesis-conversational.md
#контекст #новая

[new discovery context — unrelated to 001]
```

### Expected behavior

1. Agent does **not** read/write `001/outputs/` as the target for this hypothesis
2. After draft confirm, proposes `runs/HYP-2026-06-23-002`
3. Lists `001` as existing — «will not modify»
4. Creates `002/` only after **Confirm create 002**
5. Does **not** create `product_specification.md` or other non-contract files

### Wrong behavior (guardrails prevent)

- Writing analysis into `runs/HYP-2026-06-23-001/`
- Skipping RUN_DIR dialog and reusing open tabs
- Creating files before user confirms proposed `RUN_DIR`
