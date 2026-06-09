Язык: [English](./README.md) | **Русский**

# База знаний

Market Layer получает **local signals** прежде всего из **Confluence** через MCP.

## Основной источник: Confluence

Настройте Confluence MCP перед запуском Market Layer. См.:

```text
implementations/confluence-mcp.ru.md
```

## Что искать в Confluence

При стресс-тесте гипотезы ищите:

- Заметки customer discovery и саммари интервью
- Обсуждения продуктовых требований
- Architecture decision records
- Прошлые оценки гипотез и инициатив
- Отчёты об операционных проблемах
- Внутренний competitive analysis

## Маркировка сигналов

Все findings из Confluence попадают в `market_analysis.md` в раздел **Local Signals (Confluence)** с указанием:

- Силы сигнала: strong / weak / none
- Цитаты источника (название страницы + URL)

## Без Confluence

Если MCP не настроен, Market Layer фиксирует `missing local evidence`. External sources — вторичны и требуют явного одобрения пользователя.

## Будущие расширения

Опциональные вторичные источники (не обязательны для v1):

- Jira work items
- Внутренние wiki помимо Confluence
- Локальные research-репозитории в этом репо
