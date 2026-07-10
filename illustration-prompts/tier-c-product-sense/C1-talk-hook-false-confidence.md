# C1 Talk hook — false confidence

## Meta

| Поле | Значение |
|------|----------|
| Target output RU | `product-sense/assets/ru/talk-hook-false-confidence.svg` |
| Target output EN | `product-sense/assets/en/talk-hook-false-confidence.svg` |
| Canvas | 1920×1080 |
| Tier | C |
| Talk section | §0 Зацепка (3 min) |

## Purpose

Визуализировать проблему: много информации (RAG, KB, CustDev), но решения всё равно ошибочные — из-за ложной уверенности.

## Composition

Split screen 50/50:

**Left (cluttered but organized):** icons-as-boxes labeled RAG, KB, CustDev, Docs — many checkmarks, green tint — caption "We have information"

**Right (single wrong arrow):** large arrow to "Wrong product in backlog" in red — caption "False confidence"

Center vertical divider. Question at top: "Why do we still build the wrong thing?"

## Labels RU

Есть RAG · Есть база знаний · Есть CustDev · Ложная уверенность · Не то в backlog

## Generation prompt (copy-paste)

```
Conference slide 1920x1080, flat minimal, high contrast.

Top question large bold RU: "Почему мы всё равно строим не то?"

Split screen:

LEFT half light green gray #F0FDF4: stacked boxes "RAG" "База знаний" "CustDev" with checkmarks, caption bottom "Информации достаточно"

RIGHT half white with bold red arrow pointing to red outline box "Не то в backlog", caption "Ложная уверенность"

Vertical divider #CBD5E1. No photos. Bold sans-serif for projector. Russian text only for RU version.
```

### English variant

```
Question: "Why do we still build the wrong thing?" LEFT "We have information" boxes RAG, Knowledge base, CustDev. RIGHT "False confidence" → "Wrong item in backlog".
```

## Post-generation checklist

- [ ] Not blaming tools — blaming decision process
- [ ] Readable in 3 seconds from back row
