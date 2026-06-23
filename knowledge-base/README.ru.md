Язык: [English](./README.md) | **Русский**

# База знаний

Ваша личная база знаний — это **отдельный проект** (заметки, discovery, research). Фреймворк добавляется папкой `hypothesis-stress-test/` внутри него. См. [quick-start.ru.md](../implementations/quick-start.ru.md#база-знаний-и-workspace).

Фреймворк теперь явно разделяет retrieval и анализ:

- **Local Evidence Discovery** собирает file-based evidence в `discovery_preview.md` и `evidence_inventory.md`.
- **Market Layer** интерпретирует inventory + Confluence + external сигналы.

## Основной источник: Confluence

Настройте Confluence MCP перед запуском Market Layer. См.:

```text
implementations/confluence-mcp.ru.md
```

## Что искать в Confluence

При стресс-тесте гипотезы ищите:

- Заметки customer discovery и саммари интервью
- Исходные материалы для персон и исследования ролей
- Обсуждения продуктовых требований
- Architecture decision records
- Прошлые оценки гипотез и инициатив
- Отчёты об операционных проблемах
- Внутренний competitive analysis

## Локальная модель персон

Репозиторий может хранить знания о ролях в три слоя:

```text
knowledge-base/
  interviews/      сырые CustDev-заметки и саммари интервью
  persona-builds/  журналы пересборки персон
  personas/        текущие переиспользуемые профили ролей
```

`personas/` — это синтезированные артефакты. Их не следует считать первичным evidence.

Если у persona нет связанных `source_interviews`, считайте её слабым локальным сигналом. Если persona пересобрана из интервью, при использовании в качестве local evidence ссылайтесь на исходные интервью или persona build.

## Маркировка сигналов

В `market_analysis.md` каналы должны быть разделены:

- `Local Signals from Knowledge Base`
- `Confluence Signals`
- `External Market Signals`
- `Inferred Signals`

Все findings из Confluence попадают в раздел **Confluence Signals** с указанием:

- Силы сигнала: strong / weak / none
- Цитаты источника (название страницы + URL)

## Без Confluence

Если MCP не настроен:

- локальный inventory из KB всё равно может дать local evidence
- канал Confluence помечается как отсутствующий
- external sources остаются вторичными и требуют явного одобрения пользователя

## Будущие расширения

Опциональные вторичные источники (не обязательны для v1):

- Jira work items
- Внутренние wiki помимо Confluence
- Локальные research-репозитории в этом репо
