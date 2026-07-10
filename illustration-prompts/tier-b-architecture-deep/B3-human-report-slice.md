# B3 Human report slice (wireframe)

## Meta

| Поле | Значение |
|------|----------|
| Target output EN | `assets/en/human-report-slice.svg` |
| Target output RU | `assets/ru/human-report-slice.svg` |
| Canvas | 1200×700 |
| Tier | B |

## Purpose

Wireframe секций `human_report.html` для README и подготовки live demo — не скриншот, схема блоков.

## Audience and context

- README
- `product-sense/demo-script.md`

## Composition

Browser-frame mock (simple rectangle, no chrome detail). Stacked sections top to bottom:

1. Overview / hypothesis
2. Verdict + confidence
3. Business value & strategic fit
4. What changed? (before / after)
5. Top contradictions (HIGH)
6. Cheapest validation
7. Links to detailed artifacts (collapsed)

Highlight boxes 3, 4, 5, 6 as **demo focus** with subtle rose border

## Labels EN

Overview · Verdict · Business value · What changed? · Contradictions · Cheap validation · Artifacts

## Labels RU

Обзор · Вердикт · Бизнес-ценность · Что изменилось? · Противоречия · Дешёвая валидация · Артефакты

## Generation prompt (copy-paste)

```
UI wireframe diagram "Human Decision Report", 1200x700, flat grayscale + semantic accent, not a photo screenshot.

Simple browser window outline. Inside vertical stack of 7 section blocks with labels:

1 Overview
2 Verdict + confidence badge
3 Business value & strategic fit  [HIGHLIGHT rose border]
4 What changed? before|after columns  [HIGHLIGHT]
5 Top contradictions HIGH  [HIGHLIGHT]
6 Cheapest validation  [HIGHLIGHT]
7 Detailed artifacts (links)

Title outside: "Executive report — decision slice". Minimal lines, sans-serif, conference-minimal. No lorem ipsum paragraphs — only section titles.
```

### Russian variant note

```
Russian section titles per Labels RU. Title: "Executive-отчёт — срез для решения".
```

## Post-generation checklist

- [ ] Demo sections 3-6 visually marked
- [ ] Does not look like real confidential data
