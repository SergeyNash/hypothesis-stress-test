# A2 Pipeline — 4 stages (talk / PM view)

## Meta

| Поле | Значение |
|------|----------|
| Target output EN | `assets/en/pipeline-4-stages.svg` |
| Target output RU | `assets/ru/pipeline-4-stages.svg` |
| Format | Vector diagram (SVG) |
| Canvas | 1920×1080 (deck) or 1480×400 (README embed) |
| Style reference | [STYLE.md](../STYLE.md) |
| Tier | A |
| Also for deck | `product-sense/assets/ru/pipeline-4-stages.svg` |

## Purpose

Упрощённая схема для Product Sense и продуктовой аудитории: 4 смысловых этапа вместо 8+ технических слоёв.

## Audience and context

- `product-sense/talk-outline.md` — §3 Конвейер (главная схема доклада)
- `architecture/overview.md` — секция «для продуктовой аудитории»

## Composition

### Layout

Single horizontal row — **exactly 4 large blocks**, centered on slide. Large arrows between. Optional subtitle under each block (one line max).

### Blocks

1. **Divide perspectives** — blue family — Roles, user vs buyer tensions
2. **Find evidence** — sky + green accent — Facts, KB, business context, market
3. **Collide signals** — purple — Contradictions, 5 patterns, reframe
4. **Next step** — yellow + rose — CustDev plan, review, cheap validation — NOT backlog

### Title

- EN: **Four stages of hypothesis stress test**
- RU: **Четыре этапа стресс-теста гипотезы**

### Footer (small)

- EN: Full pipeline has more layers in repo — this is the stage view for decisions
- RU: Полный pipeline шире — это схема для принятия решений

## Labels EN

1. **1. Divide perspectives** — Stakeholder conflicts
2. **2. Find evidence** — Facts, not opinions
3. **3. Collide signals** — No smoothing
4. **4. Shape next step** — Not backlog yet

## Labels RU

1. **1. Разделить точки зрения** — Конфликты стейкхолдеров
2. **2. Найти evidence** — Факты, не мнения
3. **3. Столкнуть сигналы** — Без сглаживания
4. **4. Сформировать следующий шаг** — Не backlog

## Do NOT include

- 8 technical layer names
- Cline, MCP, skill names
- AppSec terminology

## Generation prompt (copy-paste)

```
Create a bold conference slide diagram, 1920x1080, white background, flat minimal style.

Title centered top: "Four stages of hypothesis stress test" (28px bold).

Four extra-large rounded rectangles in one horizontal row, centered vertically, each ~380px wide x 200px tall, 40px gaps, thick 2px arrows between:

Block 1 — fill #DBEAFE stroke #2563EB — main "1. Divide perspectives" subtitle "Stakeholder conflicts"
Block 2 — fill #E0F2FE stroke #0284C7 — "2. Find evidence" / "Facts, not opinions"  
Block 3 — fill #EDE9FE stroke #7C3AED — "3. Collide signals" / "No smoothing"
Block 4 — fill #FEF9C3 stroke #CA8A04 with small rose accent corner — "4. Shape next step" / "Not backlog yet"

Typography: sans-serif, main labels 20px bold, subtitles 14px #475569.

No gradients, no icons, no more than 4 blocks. Footer small gray 12px: "Full pipeline has more layers in repo — stage view for product decisions".

High contrast for projector. Semantic colors from hypothesis stress test style guide.
```

### Russian variant note

```
Title: "Четыре этапа стресс-теста гипотезы". Blocks: "1. Разделить точки зрения" / "Конфликты стейкхолдеров" | "2. Найти evidence" / "Факты, не мнения" | "3. Столкнуть сигналы" / "Без сглаживания" | "4. Сформировать следующий шаг" / "Не backlog". Footer: "Полный pipeline шире — схема для продуктовых решений".
```

## Post-generation checklist

- [ ] Exactly 4 blocks, not 5+
- [ ] Block 4 does NOT say "build" or "MVP"
- [ ] EN + RU for talk (RU primary)
