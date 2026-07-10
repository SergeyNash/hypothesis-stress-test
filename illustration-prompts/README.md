# Illustration prompts

Промпты для генерации иллюстраций Hypothesis Stress Test. **Готовые SVG/PNG здесь не хранятся** — только брифы.

## Зачем

- Единый **conference-minimal** стиль ([STYLE.md](./STYLE.md))
- Парные **EN / RU** версии
- Покрытие README, architecture и Product Sense deck
- Закрытие пробелов текущих диаграмм (Business Context, Human Report, 4 этапа для зала)

## Как использовать

1. Откройте нужный промпт в `tier-a-*`, `tier-b-*` или `tier-c-*`
2. Скопируйте секцию **Generation prompt (copy-paste)**
3. Сгенерируйте SVG (LLM, Figma, Recraft, дизайнер)
4. Сохраните по путям из Meta (см. [INDEX.md](./INDEX.md))
5. Проверьте **Post-generation checklist** в промпте

## Структура

```text
illustration-prompts/
  STYLE.md
  _TEMPLATE.md
  INDEX.md
  tier-a-readme-architecture/    # README + architecture (5)
  tier-b-architecture-deep/      # deep-dive (3)
  tier-c-product-sense/          # talk slides (6)
```

## Приоритет генерации

1. **A2** pipeline-4-stages — эталон стиля + главный слайд доклада
2. **A1** architecture-overview — hero README
3. **C2, C3** — блоки 1 и 6 доклада
4. Остальные по INDEX

## После генерации

Обновить `<img src>` в:

- `README.md` / `README.ru.md`
- `architecture/diagram.md` / `diagram.ru.md`

До появления файлов README продолжает ссылаться на legacy `assets/*.svg`.
