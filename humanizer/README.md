# Writing skills — понятный русский

В этом репозитории редактура русского текста идёт через skill **`russian-humanizer`**
и project voice adapters.

## Канонический skill

Self-contained skill с bundled references:

```text
.cline/skills/russian-humanizer/
  SKILL.md
  references/
    HUMANIZER_CORE.md
    MODES.md
    VOICE_ADAPTERS.md
  agents/openai.yaml
```

Upstream: [thinking-lab/skills/russian-humanizer](https://github.com/SergeyNash/thinking-lab/tree/main/skills/russian-humanizer)

Обновление core из upstream:

```powershell
git clone --depth 1 https://github.com/SergeyNash/thinking-lab.git $env:TEMP\thinking-lab-sync
Copy-Item -Recurse "$env:TEMP\thinking-lab-sync\skills\russian-humanizer\*" ".cline\skills\russian-humanizer\" -Force
# затем снова применить секцию Project adapters в SKILL.md
```

## Project adapters

Голоса проекта лежат отдельно — не в bundled references:

| Adapter | Когда |
|---------|--------|
| [`adapters/PUBLIC_EXPLAINER_VOICE.md`](adapters/PUBLIC_EXPLAINER_VOICE.md) | Публичные объяснения, притчи «для улицы» |

Подробнее: [`USAGE.md`](USAGE.md)

## Как вызвать

```
Используй russian-humanizer.
Mode: general.

Сохрани смысл. Без новых фактов.
Отредактируй:
<фрагмент>
```

## Что humanizer делает

- убирает AI-ритм, канцелярит, механические двоеточия;
- делает текст конкретнее и живее;
- сохраняет смысл, факты и авторский голос.

## Что humanizer не делает

- не придумывает аргументы и факты;
- не запускает Thinking Lab research;
- не humanize framework contracts и run outputs.
