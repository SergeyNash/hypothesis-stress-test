Language: **English** | [Русский](./implementations.ru.md)

# Implementations

This framework is tool-agnostic at its core. The **primary supported implementation** is **Cline in VS Code**.

---

## Framework vs Tooling

```text
Framework  = how to think (layers, contracts, decision model)
Cline impl = how to run it (rules, skills, workflows, MCP)
```

The framework defines layers and reasoning contracts. Cline provides execution, file artifacts, and Confluence integration.

---

## Primary: Cline (VS Code)

### Components

| Piece | Location |
|-------|----------|
| Rules | `.clinerules/` |
| Skills | `.cline/skills/` |
| Workflows | `.clinerules/workflows/` |
| Setup guide | [implementations/cline-setup.md](../implementations/cline-setup.md) |
| Contract | [implementations/cline-contract.md](../implementations/cline-contract.md) |

### Quick start

1. Install Cline extension in VS Code
2. Open this repository
3. Configure [Confluence MCP](../implementations/confluence-mcp.md)
4. Create `RUN_DIR/hypothesis.md`
5. Run `/run-hypothesis.md` in Cline chat

### Mapping

```text
Template (templates/*.md)  → Cline skill (SKILL.md)
Playbook step              → Cline workflow (slash command)
RUN_DIR                    → local filesystem workspace
Layer output               → markdown artifact in outputs/
Confluence pages           → local signals in market_analysis.md
```

---

## Confluence MCP (required for full Market Layer)

Confluence is the **primary MCP source** for local signals.

- Search internal wiki for discovery notes, past decisions, research
- Cite pages in `market_analysis.md`
- Without MCP: document `missing local evidence`

See [implementations/confluence-mcp.md](../implementations/confluence-mcp.md).

---

## Manual implementation

Copy templates from `templates/`, fill in hypothesis and context, run in any LLM interface, save artifacts manually.

Best for: first experiments, environments without Cline.

Steps:

1. Copy template for a layer
2. Insert hypothesis and context
3. Run in LLM interface
4. Save output to `RUN_DIR/outputs/`
5. Move to next layer

---

## API-based implementation (future)

Programmatic execution via LLM API calls:

```text
hypothesis → roles call → market call → synthesis call → artifacts
```

Useful for high-frequency or CI-integrated analysis. Not included in v1.

---

## Implementation maturity

| Level | Method | Best for |
|-------|--------|----------|
| 1 — Manual | Copy templates | Individual experiments |
| 2 — Cline assisted | Rules + skills + workflows | Regular use, small teams |
| 3 — Automated | API pipeline | High-frequency, platforms |

---

## Legacy: RooCode

Previous versions targeted RooCode. RooCode is no longer supported. Legacy screenshots are in `assets/legacy/`. Use Cline as the supported IDE adapter.

---

## Key principle

Implementation should not change the reasoning model. Tools may vary. The layers stay the same.
