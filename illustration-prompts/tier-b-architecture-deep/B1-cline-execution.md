# B1 Cline execution model

## Meta

| Поле | Значение |
|------|----------|
| Target output EN | `assets/en/cline-execution.svg` |
| Target output RU | `assets/ru/cline-execution.svg` |
| Canvas | 1200×650 |
| Tier | B |
| Replaces | `assets/cline-workflow.svg` |

## Purpose

Как Cline запускает фреймворк: Rules, Skills, Workflows, MCP — без детализации каждого skill.

## Audience and context

- README Cline section
- `implementations/cline-contract.md`

## Composition

Center: **Hypothesis run** box. Around it four quadrants or orbit:

- `.clinerules/` — Rules (always on)
- `.cline/skills/` — Skills (on demand per phase)
- `workflows/` — Slash commands (`/run-hypothesis.md`)
- MCP — Confluence (optional local signals)

Arrows: User → Workflow → Skills → Artifacts in RUN_DIR

## Labels EN

Rules · Skills · Workflows · MCP · RUN_DIR outputs

## Labels RU

Правила · Skills · Workflows · MCP · Артефакты RUN_DIR

## Generation prompt (copy-paste)

```
Technical architecture diagram "Cline execution", 1200x650, flat minimal white background.

Center large rounded rect #F8FAFC stroke #64748B: "Hypothesis run" with small "RUN_DIR/outputs/"

Four satellite boxes connected to center with arrows:
TOP-LEFT #F1F5F9 ".clinerules/" label "Rules" subtitle "always active"
TOP-RIGHT #DBEAFE ".cline/skills/" "Skills" "on demand"
BOTTOM-LEFT #EDE9FE "workflows/" "Slash commands"
BOTTOM-RIGHT #DCFCE7 "MCP" "Confluence · optional"

User icon simplified as box left: "Product manager" arrow to Workflows.

Title: "Cline adapter". No gradients. Sans-serif.
```

### Russian variant note

```
Title "Адаптер Cline". Labels: Правила | Skills | Workflows | MCP | Артефакты. User: "Продакт-менеджер".
```

## Post-generation checklist

- [ ] Framework vs Cline boundary clear (center = run, satellites = adapter)
