# A1 Architecture overview (full pipeline v2.4)

## Meta

| Поле | Значение |
|------|----------|
| Target output EN | `assets/en/architecture-overview.svg` |
| Target output RU | `assets/ru/architecture-overview.svg` |
| Format | Vector diagram (SVG) |
| Canvas | 1480×720 |
| Style reference | [STYLE.md](../STYLE.md) |
| Tier | A |
| Replaces | `assets/architecture-overview.svg` |

## Purpose

Показать полный end-to-end pipeline Hypothesis Stress Test v2.4 — от гипотезы до human backlog decision, включая Business Context и Human Report.

## Audience and context

- `README.md` — hero diagram
- `architecture/diagram.md` — System view
- `architecture/overview.md`

## Composition

### Layout

Horizontal main pipeline (top row, left to right). Below: compact artifact strip. Bottom: thin Cline adapter bar.

### Blocks (top row, 10 main blocks)

1. **INPUT** — amber — Hypothesis statement + roles
2. **ROLES** — blue — Facilitator / internal perspectives
3. **EVIDENCE** — sky — Local Evidence Discovery (preview + inventory)
4. **BUSINESS** — pink — Business Context & Value Check
5. **MARKET** — green — Market reality (inventory + channels)
6. **SYNTHESIS** — purple — Signal collision
7. **DISCOVERY** — yellow — Customer Discovery Planning
8. **REVIEW** — rose — Decision Review (gate)
9. **REPORT** — light rose — Human Report export (`human_report.html`)
10. **HUMAN** — red tint — Backlog decision (proceed / validate / research / reject)

Note: VALIDATE input may appear as a small pill before INPUT or as a subtitle under INPUT — optional, not an 11th main block.

### Artifact strip (bottom)

Pills left to right: `role_outputs/*` → `business_context_analysis.md` → `market_analysis.md` → `hypothesis_map.md` → `customer_discovery_plan.md` → `decision_review.md` → `human_report.html`

### Title

- EN: **Hypothesis Stress Test**
- RU: **Стресс-тест продуктовых гипотез**

### Subtitle

- EN: Sequential layers · traceable artifacts · human decision
- RU: Последовательные слои · трассируемые артефакты · решение человека

## Labels EN

- INPUT: Hypothesis
- ROLES: Roles / stress test
- EVIDENCE: Local evidence
- BUSINESS: Business value
- MARKET: Market check
- SYNTHESIS: Signal collision
- DISCOVERY: CustDev plan
- REVIEW: Decision review
- REPORT: Human report
- HUMAN: Backlog decision

## Labels RU

- INPUT: Гипотеза
- ROLES: Роли / стресс-тест
- EVIDENCE: Локальные доказательства
- BUSINESS: Бизнес-ценность
- MARKET: Проверка рынка
- SYNTHESIS: Столкновение сигналов
- DISCOVERY: План CustDev
- REVIEW: Обзор решения
- REPORT: Отчёт для человека
- HUMAN: Решение по backlog

## Do NOT include

- Gradients, shadows, Cline logo, Confluence logo large
- More than 2 lines of text per block
- "8 layers" label confusion — this IS the full technical view

## Generation prompt (copy-paste)

```
Create a flat minimal technical architecture diagram, SVG-style, canvas 1480x720, white background #F8FAFC.

Title top-left: "Hypothesis Stress Test" (bold 24px). Subtitle: "Sequential layers · traceable artifacts · human decision" (14px gray #475569).

Main horizontal pipeline — 10 rounded rectangles in a row, equal height ~100px, 24px gaps, left to right, connected by 2px gray arrows #64748B:

1. INPUT — fill #FEF3C7 stroke #D97706 — label "Hypothesis"
2. ROLES — fill #DBEAFE stroke #2563EB — "Roles / stress test"
3. EVIDENCE — fill #E0F2FE stroke #0284C7 — "Local evidence"
4. BUSINESS — fill #FCE7F3 stroke #DB2777 — "Business value"
5. MARKET — fill #DCFCE7 stroke #16A34A — "Market check"
6. SYNTHESIS — fill #EDE9FE stroke #7C3AED — "Signal collision"
7. DISCOVERY — fill #FEF9C3 stroke #CA8A04 — "CustDev plan"
8. REVIEW — fill #FFE4E6 stroke #E11D48 — "Decision review"
9. REPORT — fill #FFF1F2 stroke #BE123C — "Human report"
10. HUMAN — fill #FFF1F2 stroke #BE123C — "Backlog decision"

Below pipeline at y~520: light gray container "ARTIFACTS" with small pills showing file names: role_outputs, business_context_analysis.md, market_analysis.md, hypothesis_map.md, customer_discovery_plan.md, decision_review.md, human_report.html — connected by small arrows.

Bottom bar y~660: light indigo strip text "Cline: rules + skills + workflows · inventory-first evidence".

Style: conference-minimal, no gradients, no 3D, sans-serif Inter or Arial, large readable labels, semantic colors exactly as specified.
```

### Russian variant note

```
Identical layout and colors. Title: "Стресс-тест продуктовых гипотез". Subtitle: "Последовательные слои · трассируемые артефакты · решение человека". Block labels: Гипотеза | Роли / стресс-тест | Локальные доказательства | Бизнес-ценность | Проверка рынка | Столкновение сигналов | План CustDev | Обзор решения | Отчёт для человека | Решение по backlog. Bottom: "Cline: rules + skills + workflows · inventory-first evidence" (можно оставить EN или "правила + skills + workflows").
```

## Post-generation checklist

- [ ] Business Context block present (pink)
- [ ] Human Report block before Human decision
- [ ] EN + RU exported
- [ ] Readable when scaled to 760px width in README
