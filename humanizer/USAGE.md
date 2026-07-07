# Russian Humanizer — когда что использовать

Skill: [`.cline/skills/russian-humanizer/SKILL.md`](../.cline/skills/russian-humanizer/SKILL.md)

Core references (bundled in skill): [`.cline/skills/russian-humanizer/references/HUMANIZER_CORE.md`](../.cline/skills/russian-humanizer/references/HUMANIZER_CORE.md), [`MODES.md`](../.cline/skills/russian-humanizer/references/MODES.md), [`VOICE_ADAPTERS.md`](../.cline/skills/russian-humanizer/references/VOICE_ADAPTERS.md)

## Задача → mode → adapter

| Задача | Mode | Adapter | Папка / файлы |
|--------|------|---------|----------------|
| Доклад, demo-script, llm-mistakes | `business` | `humanizer/adapters/PRODUCT_SENSE_VOICE.md` | `product-sense/` |
| Законы фреймворка для сцены | `essay` | `humanizer/adapters/PRODUCT_SENSE_VOICE.md` | `product-sense/framework-laws.md` |
| Публичная притча / объяснение «на улице» | `fiction` или `general` | `humanizer/adapters/PUBLIC_EXPLAINER_VOICE.md` | `product-sense/street-parable.md`, посты |
| Нейтральная правка без project voice | `general` | — | черновики |
| Framework contracts, run outputs | — | **не humanize** | `layers/`, `.clinerules/`, `examples/*/outputs/` |

## Промпт-шаблоны

### Product Sense

```
Используй russian-humanizer.
Mode: business.
Voice adapter: humanizer/adapters/PRODUCT_SENSE_VOICE.md.

Сохрани смысл, факты, структуру и ограничения adapter.
Не добавляй аргументов, цифр и кейсов.
Не humanize таблицы и тайминги — только прозу и реплики.

Отредактируй:
<фрагмент>
```

### Public explainer

```
Используй russian-humanizer.
Mode: fiction.
Voice adapter: humanizer/adapters/PUBLIC_EXPLAINER_VOICE.md.

Сохрани смысл и ограничения adapter.
Без product/AI жаргона. Без новых фактов.

Отредактируй:
<фрагмент>
```

## Чеклист после правки

**Product Sense:** 4 этапа, 3 ошибки LLM, HR → AppSec, «продолжить с валидацией».

**Public explainer:** понятно без IT-фона, живая сцена, финал одной фразой.
