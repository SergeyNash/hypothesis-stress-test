Language: **English** | [Русский](./overview.ru.md)

# Architecture Overview

Hypothesis Stress Test is a **layered reasoning framework** with a **Cline implementation adapter**.

## Layers (framework core)

Three independent analysis layers produce structured signals:

| Layer | Question | Output |
|-------|----------|--------|
| **Roles** (facilitator / stress test) | How does this behave across perspectives? | `role_outputs/*`, `hypothesis_summary.md`, `validation_questions.md` |
| **Market** (market reality check) | Does this problem exist in reality? | `market_analysis.md` |
| **Synthesis** (`hypothesis-synthesis`) | What becomes visible only when signals collide? | `hypothesis_map.md`, `hypothesis_digest.txt` |

Layers do not mix signals prematurely. Synthesis collides facilitator and market artifacts — it does not re-analyze them.

After Synthesis, **Customer Discovery Planning** converts unresolved uncertainty into a practical interview and research plan. It does not validate hypotheses and does not make decisions.

After Customer Discovery Planning, **Decision Review** (mandatory gate) adversarially challenges conclusions before backlog planning. It does not add new signals.

## Cline adapter

The framework runs in VS Code via [Cline](https://cline.bot/) using:

| Component | Location | Role |
|-----------|----------|------|
| Rules | `.clinerules/` | Persistent invariants |
| Skills | `.cline/skills/` | On-demand layer execution |
| Workflows | `.clinerules/workflows/` | Slash-command orchestration |
| MCP | Confluence (primary) | Local signal retrieval |

See [implementations/cline-contract.md](../implementations/cline-contract.md) for the full mapping.

## Data flow

```text
input/hypothesis.md
  → Input Validation
  → Roles Layer (skill)
  → Local Evidence Discovery (skill)
  → discovery_preview.md + evidence_inventory.md
  → Market Layer (skill + inventory + Confluence MCP)
  → Synthesis Layer (skill)
  → hypothesis_map.md + hypothesis_digest.txt
  → Customer Discovery Planning (skill)
  → customer_discovery_plan.md
  → Decision Review (skill)
  → decision_review.md
  → Human backlog decision
```

## Artifact contract

Each run uses an isolated `RUN_DIR`. See [run-structure.md](./run-structure.md) and `.clinerules/10-artifact-contracts.md`.

## Decision model

The Synthesis Layer classifies signal collisions into five patterns:

- **Validated Opportunity** — internal and external signals align
- **Internal Illusion** — internal logic strong, market weak
- **Blind Spot** — market signal exists, internal model misses it
- **Weak Signal** — no strong evidence
- **Local Optimization Trap** — pain confirmed, no strategic business value

See [signal model diagram](../assets/signal-model.svg).

## Framework vs implementation

```text
Framework  → layers, contracts, reasoning model (tool-agnostic)
Cline impl → rules, skills, workflows, Confluence MCP
```

The framework can also run manually via `templates/` without Cline.

## Documentation map

| Topic | File |
|-------|------|
| Cline setup | [implementations/cline-setup.md](../implementations/cline-setup.md) |
| Confluence MCP | [implementations/confluence-mcp.md](../implementations/confluence-mcp.md) |
| Cline contract | [implementations/cline-contract.md](../implementations/cline-contract.md) |
| Run playbook | [playbooks/run-hypothesis.md](../playbooks/run-hypothesis.md) |
| Example | [examples/example-001/](../examples/example-001/) |
