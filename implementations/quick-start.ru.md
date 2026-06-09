Язык: [English](./README.md) | **Русский**

# Быстрый старт

Короткий путь: от установки Cline до первого прогона гипотезы за 10–15 минут.

Полная документация: [README.ru.md](./README.ru.md)

---

## Что понадобится

- VS Code
- [Cline](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev)
- API-ключ LLM-провайдера (или локальная модель)
- Confluence MCP (рекомендуется) — [confluence-mcp.ru.md](./confluence-mcp.ru.md)

---

## Шаг 1. Установить Cline

1. Откройте VS Code → Extensions → найдите **Cline** → Install.
2. В настройках Cline укажите провайдера LLM и API-ключ.

---

## Шаг 2. Открыть репозиторий

```text
git clone <repo-url>
code hypothesis-stress-test
```

Cline автоматически подхватит:

- Rules из `.clinerules/`
- Skills из `.cline/skills/`
- Workflows из `.clinerules/workflows/`

Проверьте в панели Cline: иконка Rules (весы) — правила фреймворка должны быть включены.

---

## Шаг 3. Настроить Confluence MCP

Market Layer ищет **local signals** сначала в Confluence.

Минимальная настройка — см. [confluence-mcp.ru.md](./confluence-mcp.ru.md).

Без Confluence Market Layer пометит `missing local evidence` — прогон возможен, но без внутренних данных.

---

## Шаг 4. Создать RUN_DIR

```text
runs/my-hypothesis/
  hypothesis.md
```

Минимальный пример `hypothesis.md`:

```markdown
# Hypothesis

## Statement

Если [действие], то [ожидаемый результат для конкретной аудитории].

## Relevant Roles

* Роль 1
* Роль 2

## Research Context

* Domain: [домен]
* Target audience: [аудитория]
* Scenario: [сценарий]
```

Полная схема: [templates/input-schema.md](../templates/input-schema.md)

Или скопируйте пример: [examples/example-001/hypothesis.md](../examples/example-001/hypothesis.md)

---

## Шаг 5. Запустить прогон

В чате Cline:

```text
RUN_DIR: runs/my-hypothesis
/run-hypothesis.md
```

Cline выполнит:

1. Валидацию входа
2. Roles Layer
3. Market Layer (с поиском в Confluence)
4. Synthesis Layer

Подтверждайте запись файлов и вызовы MCP по запросу.

---

## Шаг 6. Прочитать результат

Сначала откройте:

```text
runs/my-hypothesis/outputs/hypothesis_digest.txt
```

Полный анализ:

```text
outputs/
  role_outputs/*
  hypothesis_summary.md
  market_analysis.md
  hypothesis_map.md
  hypothesis_digest.txt
```

| Артефакт | Что внутри |
|----------|------------|
| `hypothesis_digest.txt` | Краткий итог: классификация, конфликт, следующий шаг |
| `hypothesis_map.md` | Полный синтез: противоречия и границы решения |
| `market_analysis.md` | Внешние и внутренние сигналы с источниками |

---

## Если что-то пошло не так

| Проблема | Решение |
|----------|---------|
| Rules не видны | Перезагрузите окно VS Code; проверьте `.clinerules/` |
| Workflow не запускается | Укажите `RUN_DIR:` явно в сообщении |
| Confluence MCP не работает | [confluence-mcp.ru.md](./confluence-mcp.ru.md) |
| Нет outputs | Проверьте, какой слой не завершился (marker-файлы в `outputs/`) |

---

## Куда идти дальше

- [cline-setup.ru.md](./cline-setup.ru.md) — полная настройка Cline
- [playbooks/run-hypothesis.ru.md](../playbooks/run-hypothesis.ru.md) — детальный сценарий прогона
- [examples/example-001/](../examples/example-001/) — эталонный пример с артефактами
