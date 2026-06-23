<p align="right">
  <sub>
    🌐 <b>Language:</b>
    <b>🇬🇧 English</b> ·
    <a href="./README.ru.md">🇷🇺 Русский</a> ·
    <a href="./implementations/quick-start.md">Quick Start</a> ·
    <a href="./implementations/quick-start.ru.md">Быстрый старт</a>
  </sub>
</p>

# 🧠 Hypothesis Stress Test

<p align="center">
  <sub>Framework version <b>2.2.1</b> · <a href="./CHANGELOG.md">Changelog</a></sub>
</p>

<p align="center">
  <b>Challenge product hypotheses before you waste time building them.</b>
</p>

<p align="center">
  A layered framework for product decision-making — run in VS Code with <a href="https://cline.bot/">Cline</a>, skills, and Confluence MCP.
</p>

<p align="center">
  <a href="./implementations/quick-start.md"><b>Quick Start</b></a>
  ·
  <a href="./playbooks/run-hypothesis.md"><b>Playbook</b></a>
  ·
  <a href="./implementations/README.md"><b>Docs</b></a>
  ·
  <a href="./examples/example-001/"><b>Example</b></a>
  ·
  <a href="./architecture/overview.md"><b>Architecture</b></a>
  ·
  <a href="./CHANGELOG.md"><b>Changelog</b></a>
  ·
  <a href="./implementations/README.ru.md"><b>Документация (RU)</b></a>
</p>

<p align="center">
  <img src="./assets/architecture-overview.svg" width="760"/>
</p>

<p align="center">
  <a href="./assets/architecture-overview.svg">Open architecture diagram</a>
</p>

---

## Why this exists

Most product teams don't fail because they lack ideas.

They fail because they:

* validate ideas too late
* rely on intuition
* mix assumptions with reality
* avoid confronting contradictions

This framework helps answer one question early:

> **Should this idea exist at all?**

---

## The core idea

Do not ask an LLM to generate more ideas.

Use it to apply pressure to the ideas you already have.

```text
idea → stress test → decision
```

---

## How it works

Three analysis layers, Customer Discovery Planning, mandatory Decision Review, then human backlog decision:

| Phase | Skill | Output |
|-------|-------|--------|
| **Validate** | `hypothesis-input-validation` | ready `input/hypothesis.md` |
| **Facilitator** (Roles / stress test) | `hypothesis-facilitator` | `role_outputs/*`, `hypothesis_summary.md`, `validation_questions.md` |
| **Market** (market reality check) | `hypothesis-market-layer` | `market_analysis.md` |
| **Synthesis** (signal collision) | `hypothesis-synthesis` | `hypothesis_map.md`, `hypothesis_digest.txt` |
| **Customer Discovery Planning** | `customer-discovery-planning` | `customer_discovery_plan.md` |
| **Decision Review** | `hypothesis-decision-review` | `decision_review.md` |
| **Backlog Decision** (human) | — | proceed / validate / research / reject |

Full run (chat-first): `/run-hypothesis-conversational.md`

Full run (file-first): `/run-hypothesis.md`

Phase by phase:

```text
/validate-hypothesis-input.md
/run-facilitator.md
/run-market-layer.md
/run-synthesis.md
/run-customer-discovery-planning.md
/run-decision-review.md
```

Specify `RUN_DIR` in your Cline message, e.g. `RUN_DIR: runs/HYP-2026-06-22-001`

---

## Cline implementation

<p align="center">
  <img src="./assets/cline-workflow.svg" width="800"/>
</p>

| Component | Location | Purpose |
|-----------|----------|---------|
| **Rules** | `.clinerules/` | Persistent framework invariants |
| **Skills** | `.cline/skills/` | On-demand phase execution |
| **Workflows** | `.clinerules/workflows/` | Slash commands |
| **Confluence MCP** | MCP config | Primary local signal source |

Setup: [implementations/cline-setup.md](./implementations/cline-setup.md)

Confluence MCP: [implementations/confluence-mcp.md](./implementations/confluence-mcp.md)

Contract: [implementations/cline-contract.md](./implementations/cline-contract.md)

---

## Decision model

<p align="center">
  <img src="./assets/signal-model.svg" width="660"/>
</p>

The Synthesis layer (`hypothesis-synthesis`) classifies signal collisions into five patterns:

* **Validated Opportunity** — internal and external signals align
* **Internal Illusion** — internal logic looks strong, market does not confirm
* **Blind Spot** — market signal exists, internal model misses it
* **Weak Signal** — no strong evidence from either side
* **Local Optimization Trap** — pain confirmed, but no strategic business value

---

## Artifact flow

<p align="center">
  <img src="./assets/artifact-flow.svg" width="820"/>
</p>

Every run creates a traceable decision trail:

```text
RUN_DIR/
  input/
    hypothesis.md
    attachments/
  run.md
  outputs/
    role_outputs/*
    hypothesis_summary.md
    validation_questions.md
    market_analysis.md
    hypothesis_map.md
    hypothesis_digest.txt
    customer_discovery_plan.md
    decision_review.md
    *.marker
```

Output language matches `input/hypothesis.md`.

---

## Quick start (Cline)

Full guide: **[implementations/quick-start.md](./implementations/quick-start.md)**

In short:

1. Install [Cline](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev) in VS Code
2. Open **your knowledge base** and add the `hypothesis-stress-test/` folder (clone or submodule)
3. Symlink `.clinerules/` and `.cline/` to the KB root — see [quick start](./implementations/quick-start.md)
4. Configure [Confluence MCP](./implementations/confluence-mcp.md)
5. **Chat-first (recommended):** in Cline chat, invoke `/run-hypothesis-conversational.md` — use `#hypothesis` for ready statements or `#context` for dirty discovery notes; confirm draft before `runs/` is created
6. **File-first (fallback):** create `runs/HYP-YYYY-MM-DD-NNN/input/hypothesis.md` — see [templates/input-schema.md](./templates/input-schema.md), then `RUN_DIR: runs/HYP-YYYY-MM-DD-NNN` + `/run-hypothesis.md`

Operational docs: [implementations/README.md](./implementations/README.md)

Manual fallback: [playbooks/run-hypothesis.md](./playbooks/run-hypothesis.md)

---

## Example

```text
examples/example-001/
```

Chat-first walkthrough: [examples/chat-first-run.md](./examples/chat-first-run.md)

A B2B AppSec hypothesis: synthesis reframes from "reduce production risk" to "improve operational efficiency"; `decision_review.md` recommends **Proceed with Validation**.

---

## Framework vs tooling

```text
Framework  → how to think (layers, contracts, decision model)
Cline      → how to run it (rules, skills, workflows, MCP)
```

The framework is tool-agnostic. Cline is the primary supported implementation. Manual and API modes are also possible — see [architecture/implementations.md](./architecture/implementations.md).

---

## Repository structure

```text
.clinerules/       Cline rules and workflows
.cline/skills/     Cline skills per phase
layers/            reasoning model
templates/         manual execution templates
playbooks/         usage workflows
examples/          worked examples
runs/              hypothesis runs (in KB workspace)
knowledge-base/    Confluence / local signals guide
architecture/      system design
implementations/   Cline setup, Confluence MCP, contract
assets/            diagrams
CHANGELOG.md       framework version history
VERSION            current framework version
```

---

## Principles

* Separate internal and external signals
* Local evidence inventory first, then Confluence for internal wiki signals
* No evidence → no claim
* Contradictions matter more than consensus
* Challenge conclusions before backlog planning
* Human makes the backlog decision
* Bad ideas should die early

---

## What this is not

* an idea generator
* a replacement for real users and interviews
* a substitute for full market research
* an autonomous decision-maker

---

<p align="center">
  <b>Stress-test the idea before you build it.</b>
</p>
