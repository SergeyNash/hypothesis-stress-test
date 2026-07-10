# B2 Business value flow

## Meta

| Поле | Значение |
|------|----------|
| Target output EN | `assets/en/business-value-flow.svg` |
| Target output RU | `assets/ru/business-value-flow.svg` |
| Canvas | 1100×500 |
| Tier | B |

## Purpose

Слой Business Context: разделить user pain, buyer value и strategic fit.

## Audience and context

- `layers/business-context-layer.md`
- README (optional deep link)

## Composition

Horizontal flow with **three gates**:

1. **User pain** (blue) — operator feels the problem
2. **Buyer value** (pink) — who pays and why
3. **Strategic fit** (purple tint) — aligns with company strategy

Red X overlay path: "Pain without buyer" dashed failure path below main flow

## Labels EN

User pain · Buyer value · Strategic fit · Pain ≠ revenue

## Labels RU

Боль пользователя · Ценность для покупателя · Strategic fit · Боль ≠ выручка

## Generation prompt (copy-paste)

```
Horizontal 3-block diagram "Business value flow", 1100x500, flat minimal.

Title: "Business Context & Value Check"

Three large blocks left to right with arrows:
1 #DBEAFE "User pain" — "Problem exists for operator?"
2 #FCE7F3 "Buyer value" — "Who pays and for what?"
3 #EDE9FE "Strategic fit" — "Why now for the business?"

Below main arrow dashed red path skipping from block 1 to X icon: "Pain without buyer — weak case"

Subtitle: "Problem exists ≠ business case". Colors semantic. No gradients.
```

### Russian variant note

```
Title "Бизнес-контекст и ценность". Blocks: Боль пользователя | Ценность для покупателя | Strategic fit (можно оставить EN термин). Dashed: "Боль без покупателя — слабый кейс". Subtitle: "Проблема есть ≠ бизнес-кейс".
```

## Post-generation checklist

- [ ] Three distinct blocks, not one generic "business"
