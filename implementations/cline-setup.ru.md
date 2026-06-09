Язык: [English](./cline-setup.md) | **Русский**

# Настройка Cline

Пошаговый гайд по запуску Hypothesis Stress Test через Cline в VS Code.

## 1. Установить Cline

1. Откройте VS Code.
2. Extensions → найдите **Cline**.
3. Установите [Cline](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev).
4. В настройках Cline укажите LLM-провайдера (API-ключ или локальная модель).

## 2. Открыть проект

### Рекомендуется: KB + папка `hypothesis-stress-test/`

Откройте **свою базу знаний** и добавьте в неё полный репозиторий фреймворка:

```text
my-knowledge-base/
  discovery/                 ← ваша KB
  runs/                      ← прогоны гипотез
  hypothesis-stress-test/      ← clone или git submodule
    .clinerules/
    .cline/skills/
    templates/
    implementations/
    ...
```

Cline ищет `.clinerules/` и `.cline/` в **корне workspace**. После добавления вложенной папки создайте symlink или копию в корне KB — см. [quick-start.ru.md](./quick-start.ru.md#база-знаний-и-workspace).

### Альтернатива: только фреймворк

```text
git clone <repo-url>
code hypothesis-stress-test
```

Cline автоматически обнаружит из корня:

- Rules из `.clinerules/` (включая `workflows/`)
- Skills из `.cline/skills/`

Проверьте в панели Cline:

- **Rules** (иконка весов) — правила фреймворка должны быть в списке и включены
- Skills — `hypothesis-*` skills появятся при релевантном запросе

## 3. Настроить Confluence MCP (рекомендуется)

См. [confluence-mcp.ru.md](./confluence-mcp.ru.md).

Без Confluence Market Layer пометит `missing local evidence`.

## 4. Создать директорию прогона

```text
runs/my-hypothesis/
  hypothesis.md
```

Формат входа: [templates/input-schema.md](../templates/input-schema.md)

Или скопируйте пример:

```text
examples/example-001/
```

## 5. Запустить гипотезу

В чате Cline:

```text
/run-hypothesis.md
```

Или по шагам:

```text
/validate-hypothesis-input.md
```

Затем отдельные workflow по слоям:

```text
/run-market-layer.md
/run-synthesis.md
/run-decision-review.md
```

Укажите `RUN_DIR` в сообщении:

```text
RUN_DIR: runs/my-hypothesis
/run-hypothesis.md
```

## 6. Проверить outputs

```text
outputs/
  role_outputs/*
  hypothesis_summary.md
  market_analysis.md
  hypothesis_map.md
  hypothesis_digest.txt
  decision_review.md
```

Сначала `hypothesis_digest.txt`, затем `decision_review.md` — уверенность и рекомендация перед backlog decision.

## Plan vs Act mode

- **Plan** — просмотрите план до записи файлов.
- **Act** — выполнение слоёв и запись артефактов.
- Подтверждайте вызовы MCP (особенно поиск в Confluence).

## Troubleshooting

| Проблема | Решение |
|----------|---------|
| Rules не видны | Перезагрузите VS Code; проверьте `.clinerules/` |
| Skills не срабатывают | Упомяните «hypothesis stress test» или используйте slash workflows |
| Confluence MCP не работает | [confluence-mcp.ru.md](./confluence-mcp.ru.md) |
| Нет outputs | Проверьте отсутствующие marker-файлы в `outputs/` |

## Ручной режим (fallback)

Скопируйте шаблоны из `templates/` и запускайте в любом LLM-чате. См. [playbooks/run-hypothesis.ru.md](../playbooks/run-hypothesis.ru.md).
