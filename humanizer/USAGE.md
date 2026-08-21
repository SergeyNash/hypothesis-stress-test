# Russian Humanizer — когда что использовать

Skill: [`.cline/skills/russian-humanizer/SKILL.md`](../.cline/skills/russian-humanizer/SKILL.md)

Core references (bundled in skill): [`.cline/skills/russian-humanizer/references/HUMANIZER_CORE.md`](../.cline/skills/russian-humanizer/references/HUMANIZER_CORE.md), [`MODES.md`](../.cline/skills/russian-humanizer/references/MODES.md), [`VOICE_ADAPTERS.md`](../.cline/skills/russian-humanizer/references/VOICE_ADAPTERS.md)

## Задача → mode → adapter

| Задача | Mode | Adapter | Папка / файлы |
|--------|------|---------|----------------|
| Публичное объяснение «на улице» | `fiction` или `general` | `humanizer/adapters/PUBLIC_EXPLAINER_VOICE.md` | посты, короткие объяснения |
| Нейтральная правка без project voice | `general` | — | черновики |
| Framework contracts, run outputs | — | **не humanize** | `layers/`, `.clinerules/`, `examples/*/outputs/` |

## Промпт-шаблоны

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

**Public explainer:** понятно без IT-фона, живая сцена, финал одной фразой.
