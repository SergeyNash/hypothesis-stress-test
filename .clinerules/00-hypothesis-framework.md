# Hypothesis Stress Test Framework

**Framework version:** 2.0.0 — see [CHANGELOG.md](../CHANGELOG.md) and [VERSION](../VERSION).

This project implements a **tool-agnostic hypothesis stress-test framework** with a **Cline adapter**.

## Core principle

Do not ask the LLM to generate more ideas. Use it to apply pressure to ideas you already have.

```text
idea → stress test → decision
```

## Three analysis layers (never mix prematurely)

| Layer | Purpose | Output |
|-------|---------|--------|
| **Roles** (facilitator / stress test) | Internal perspectives, assumptions, conflicts | role_outputs/*, hypothesis_summary.md, validation_questions.md |
| **Market** | External reality | market_analysis.md |
| **Synthesis** | Signal collision | hypothesis_map.md, hypothesis_digest.txt |

## Decision Review (mandatory gate)

After Synthesis, run **Decision Review** — an adversarial critique of conclusions. It does not add new signals; it challenges existing ones.

| Phase | Purpose | Output |
|-------|---------|--------|
| **Decision Review** | Challenge conclusions, propose cheap validation | decision_review.md |

## Execution order

1. Validate input (hypothesis, roles, research context)
2. Run Facilitator (Roles Layer) — skill `hypothesis-facilitator`
3. Run Market Layer (Confluence MCP first for local signals)
4. Run Synthesis Layer
5. Run Decision Review
6. Human backlog decision

Analysis layers are **sequential** and **independent**. Synthesis consumes artifacts only — it does not add new data. Decision Review critiques artifacts only — it does not add new data.

## Human-in-the-loop

- The human makes the final decision.
- Cline proposes analysis; the user approves file writes and MCP tool calls.
- Bad ideas should die early.

## What this is NOT

- Not an idea generator
- Not a replacement for real users
- Not an autonomous decision-maker

## Skills and workflows

Use project skills from `.cline/skills/` or invoke workflows:

- `/validate-hypothesis-input.md` — check input before running
- `/run-facilitator.md` — Facilitator (Roles Layer) only
- `/run-hypothesis.md` — full end-to-end run
- `/run-market-layer.md` — Market Layer only
- `/run-synthesis.md` — Synthesis Layer only
- `/run-decision-review.md` — Decision Review only
