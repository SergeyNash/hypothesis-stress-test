# C3 Talk — three LLM mistakes

## Meta

| Поле | Значение |
|------|----------|
| Target output RU | `product-sense/assets/ru/talk-llm-mistakes.svg` |
| Canvas | 1920×1080 |
| Tier | C |
| Talk section | §6 Типичные ошибки LLM (3 min) |
| Source | `product-sense/llm-mistakes.md` |

## Purpose

Три карточки контраста: обычный LLM vs стресс-тест — для трёх слайдов или одного summary slide.

## Composition

Three horizontal rows (or 3 columns). Each row:

- Left small gray: "Один промпт" + mistake
- Arrow
- Right colored: "Стресс-тест" + correction

Rows:
1. Logic = proof → Internal illusion flagged
2. Smooth contradictions → Divergences HIGH required
3. Build MVP → Proceed with validation

## Labels RU

См. llm-mistakes.md — три пары

## Generation prompt (copy-paste)

```
1920x1080 slide "Три ошибки обычного LLM", three horizontal comparison rows, flat minimal.

Title top: "Три ошибки обычного LLM"

Row 1: gray box "Звучит логично ✓" → purple box "Внутренняя иллюзия ✗"
Row 2: gray "Риски, но перспективно" → purple "Противоречия HIGH обязательны"  
Row 3: gray "Roadmap · MVP" → yellow-rose "Продолжить с валидацией"

Left column header small "Один промпт", right "Стресс-тест". 2px arrows between. Semantic colors from style guide. Russian text. Bold readable.
```

### Optional: 3 separate slides

Use same row design one per slide 1920x1080 with larger text.

## Post-generation checklist

- [ ] Exactly 3 mistakes, not more
- [ ] Row 3 does not say "build"
