Язык: [English](./cline-contract.md) | **Русский**

# Контракт Cline

Как фреймворк Hypothesis Stress Test соотносится с компонентами Cline.

## Соответствие

| Концепция фреймворка | Имплементация в Cline |
|----------------------|----------------------|
| Инварианты слоёв | `.clinerules/*.md` |
| Выполнение слоя | `.cline/skills/*/SKILL.md` |
| End-to-end прогон | `.clinerules/workflows/run-hypothesis.md` |
| Local knowledge (Market) | Confluence MCP |
| Артефакты | Файлы в `RUN_DIR/outputs/` |

## Компоненты

### Rules (всегда активны)

Расположение: `.clinerules/`

| Файл | Назначение |
|------|------------|
| `00-hypothesis-framework.md` | Обзор фреймворка, порядок слоёв |
| `10-artifact-contracts.md` | Структура RUN_DIR, именование, markers |
| `20-evidence-rules.md` | Confluence-first, типы сигналов |

### Skills (по запросу)

Расположение: `.cline/skills/`

| Skill | Когда |
|-------|-------|
| `hypothesis-input-validation` | Перед любым слоем |
| `hypothesis-roles-layer` | Roles Layer |
| `hypothesis-market-layer` | Market Layer + Confluence MCP |
| `hypothesis-synthesis-layer` | Synthesis Layer |

### Workflows (slash-команды)

Расположение: `.clinerules/workflows/`

| Workflow | Команда |
|----------|---------|
| `validate-hypothesis-input.md` | `/validate-hypothesis-input.md` |
| `run-hypothesis.md` | `/run-hypothesis.md` |
| `run-market-layer.md` | `/run-market-layer.md` |
| `run-synthesis.md` | `/run-synthesis.md` |

## Поток выполнения

```text
Пользователь указывает RUN_DIR
  → валидация входа (skill или workflow)
  → Roles Layer (skill) → role_outputs + summary + marker
  → Market Layer (skill + Confluence MCP) → market_analysis + marker
  → Synthesis Layer (skill) → hypothesis_map + digest + marker
```

## Требования

1. Установлено [расширение Cline](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev)
2. Проект открыт в VS Code (rules и skills подхватываются автоматически)
3. Настроен Confluence MCP (рекомендуется для Market Layer) — [confluence-mcp.ru.md](./confluence-mcp.ru.md)

## Fallback: ручной режим

Без Cline: скопируйте шаблоны из `templates/` и запускайте слои вручную в любом LLM. См. [playbooks/run-hypothesis.ru.md](../playbooks/run-hypothesis.ru.md).
