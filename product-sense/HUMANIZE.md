# Humanize — Product Sense

Перед выступлением прогоните правки через [russian-humanizer](../.cline/skills/russian-humanizer/SKILL.md): после изменений в outline, перед финальной репетицией, когда текст снова звучит как AI-конспект.

## Когда применять

- после правок в `talk-outline.md` или `demo-script.md`
- перед репетицией, если реплики читаются «с листа»
- **не** применять к `examples/*/outputs/`, `layers/`, `.clinerules/` и core skills (кроме самого russian-humanizer)

## Как вызывать

```
Используй russian-humanizer.
Mode: business.
Voice adapter: humanizer/PRODUCT_SENSE_VOICE.md.

Сохрани смысл, факты, структуру и ограничения voice adapter.
Не добавляй аргументов, цифр и кейсов.
Не humanize таблицы и тайминги — только прозу и реплики.

Отредактируй:
<фрагмент>
```

Для [framework-laws.md](./framework-laws.md) — `Mode: essay`.

Правила ядра: [humanizer/HUMANIZER_CORE.md](../humanizer/HUMANIZER_CORE.md). Голос доклада: [humanizer/PRODUCT_SENSE_VOICE.md](../humanizer/PRODUCT_SENSE_VOICE.md).

## Чеклист после humanize

- 4 этапа конвейера на месте
- 3 ошибки LLM
- HR Tech первый, AppSec — производственный кейс
- «Продолжить с валидацией» не превратилось в «строить MVP»
- CHRO, compliance, governance, backlog на месте
- таблицы и минуты в outline не сломаны
