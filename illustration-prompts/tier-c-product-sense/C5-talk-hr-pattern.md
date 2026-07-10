# C5 Talk — HR Tech pattern (before / after)

## Meta

| Поле | Значение |
|------|----------|
| Target output RU | `product-sense/assets/ru/talk-hr-pattern.svg` |
| Canvas | 1920×1080 |
| Tier | C |
| Talk section | §4 Демо HR Tech (7 min) |
| Source | `product-sense/examples/non-appsec-story.md` |

## Purpose

Один слайд «было → стало» для HR кейса без security jargon.

## Composition

Two columns with arrow between:

**Было:** ИИ auto-ranking · −30% time-to-hire · buyer = recruiter (wrong)

**Стало:** Governed recruiter assist · audit trail · buyer = CHRO · metric = screening hours saved

Verdict badge bottom: **Продолжить с валидацией**

## Generation prompt (copy-paste)

```
1920x1080 before/after slide RU, flat minimal.

Title: "HR Tech: что изменилось после стресс-теста"

LEFT column header "Было" gray box:
- "ИИ auto-ranking кандидатов"
- "−30% time-to-hire"
- small red note "Покупатель: рекрутер"

Center large arrow

RIGHT column header "Стало" green tint box:
- "Governed recruiter assist"
- "Audit trail · compliance"
- "Покупатель: CHRO"
- "Метрика: часы screening"

Bottom center badge rose outline: "Продолжить с валидацией"

No AppSec terms. Sans-serif. Conference colors.
```

## Post-generation checklist

- [ ] −30% shown as illusion in "Было"
- [ ] CHRO visible in "Стало"
