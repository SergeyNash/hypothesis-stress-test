Язык: [English](./cline-contract.md) | **Русский**

# Контракт Cline

Как фреймворк Hypothesis Stress Test соотносится с компонентами Cline.

## Соответствие

| Концепция фреймворка | Имплементация в Cline |
|----------------------|----------------------|
| Инварианты слоёв | `.clinerules/*.md` |
| Выполнение слоя | `.cline/skills/*/SKILL.md` |
| End-to-end прогон | `.clinerules/workflows/run-hypothesis.md` |
| Local evidence retrieval | skill `local-knowledge-retrieval` + KB files |
| Артефакты | Файлы в `RUN_DIR/outputs/` |

## Компоненты

### Rules (всегда активны)

Расположение: `.clinerules/`

| Файл | Назначение |
|------|------------|
| `00-hypothesis-framework.md` | Обзор фреймворка, порядок слоёв |
| `10-artifact-contracts.md` | Структура RUN_DIR, именование, markers |
| `20-evidence-rules.md` | правила каналов KB evidence + Confluence + external/inferred |

### Skills (по запросу)

Расположение: `.cline/skills/`

| Skill | Когда |
|-------|-------|
| `hypothesis-input-validation` | Перед любым слоем |
| `hypothesis-facilitator` | Facilitator (Roles Layer / stress test) |
| `local-knowledge-retrieval` | Local Evidence Discovery (preview + inventory) |
| `hypothesis-market-layer` | Market Layer + KB inventory + Confluence MCP |
| `hypothesis-synthesis` | Synthesis Layer (signal collision) |
| `customer-discovery-planning` | Customer Discovery Planning (практичный план интервью) |
| `hypothesis-decision-review` | Decision Review (обязательный gate) |

### Workflows (slash-команды)

Расположение: `.clinerules/workflows/`

| Workflow | Команда |
|----------|---------|
| `validate-hypothesis-input.md` | `/validate-hypothesis-input.md` |
| `run-facilitator.md` | `/run-facilitator.md` |
| `run-knowledge-retrieval.md` | `/run-knowledge-retrieval.md` |
| `run-hypothesis.md` | `/run-hypothesis.md` |
| `run-market-layer.md` | `/run-market-layer.md` |
| `run-synthesis.md` | `/run-synthesis.md` |
| `run-customer-discovery-planning.md` | `/run-customer-discovery-planning.md` |
| `run-decision-review.md` | `/run-decision-review.md` |

## Поток выполнения

```text
Пользователь указывает RUN_DIR
  → валидация входа (skill или workflow)
  → Facilitator (skill) → role_outputs + summary + validation_questions + marker
  → Local Evidence Discovery (skill) → discovery_preview + evidence_inventory + marker
  → Market Layer (skill + inventory + Confluence MCP) → market_analysis + marker
  → Synthesis (hypothesis-synthesis) → hypothesis_map + digest + marker
  → Customer Discovery Planning (skill) → customer_discovery_plan + marker
  → Decision Review (skill) → decision_review + marker
  → Решение человека (backlog)
```

## Требования

1. Установлено [расширение Cline](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev)
2. Проект открыт в VS Code (rules и skills подхватываются автоматически)
3. Настроен Confluence MCP (рекомендуется для Market Layer) — [confluence-mcp.ru.md](./confluence-mcp.ru.md)

## Fallback: ручной режим

Без Cline: скопируйте шаблоны из `templates/` и запускайте слои вручную в любом LLM. См. [playbooks/run-hypothesis.ru.md](../playbooks/run-hypothesis.ru.md).
