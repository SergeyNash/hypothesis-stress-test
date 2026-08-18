# Прогон

Этот файл описывает, как гипотеза была обработана через фреймворк v2.4.

---

## Вход

Файл гипотезы:

```text
examples/example-001/input/hypothesis.md
```

---

## Режим выполнения

**Primary:** Conversational (chat-first) via `/run-hypothesis-conversational.md` — see [chat-first-run.md](./chat-first-run.md)

**File-first:**

```text
RUN_DIR: examples/example-001
/run-hypothesis.md
```

**Fallback:** ручной запуск через шаблоны в любом LLM-интерфейсе.

---

## Предварительные требования

1. Установлено расширение Cline — [implementations/cline-setup.md](../implementations/cline-setup.md)
2. Настроен Confluence MCP (рекомендуется) — [implementations/confluence-mcp.md](../implementations/confluence-mcp.md)
3. Подготовлен `input/hypothesis.md`

---

## Шаг 0 — Validate

Проверить `input/hypothesis.md` через skill `hypothesis-input-validation` или `/validate-hypothesis-input.md`. Следующий слой запускается только для валидного входа.

---

## Шаг 1 — Facilitator (Roles Layer)

**Cline skill:** `hypothesis-facilitator`

**Ручной шаблон:** `templates/facilitator-prompt.md`

Вход:

* формулировка гипотезы
* релевантные роли
* контекст сценария

Ожидаемый output:

```text
outputs/role_outputs/
outputs/hypothesis_summary.md
outputs/validation_questions.md
outputs/ready_for_synthesis.marker
```

Цель:

* вскрыть скрытые допущения и границы применимости
* показать конфликты ролей
* сгенерировать behavior-based вопросы для интервью

---

## Шаг 2 — Local Evidence Discovery

**Cline skill:** `local-knowledge-retrieval`

**Ручной шаблон:** `templates/knowledge-retrieval-prompt.md`

Вход:

* формулировка гипотезы
* опционально summary из Facilitator

Ожидаемый output:

```text
outputs/discovery_preview.md
outputs/evidence_inventory.md
outputs/knowledge_retrieval_complete.marker
```

Цель:

* собрать source-linked local evidence до анализа рынка
* сохранить атомарность evidence (без синтеза)
* дать audit trail retrieval (scanned/skipped/candidates)

---

## Шаг 3 — Business Context & Value Check

**Cline skill:** `business-context-value-check`

**Ручной шаблон:** `templates/business-context-prompt.md`

Вход:

* формулировка гипотезы и outputs Roles Layer
* `outputs/evidence_inventory.md`
* доступные strategy / OKR / business-model материалы

Ожидаемый output:

```text
outputs/business_context_analysis.md
# или, если контекст отсутствует:
outputs/missing_business_context.md
outputs/business_context_complete.marker
```

Цель:

* проверить business value, stakeholder map и strategic fit
* зафиксировать пробел контекста без выдуманного стратегического соответствия

---

## Шаг 4 — Market Layer

**Cline skill:** `hypothesis-market-layer`

**Ручной шаблон:** `templates/market-prompt.md`

**Inventory first:** сначала читать `outputs/evidence_inventory.md`, затем Confluence MCP для дополнительных внутренних сигналов.

Вход:

* формулировка гипотезы
* research context
* domain и тип продукта
* `outputs/business_context_analysis.md` или `outputs/missing_business_context.md`

Ожидаемый output:

```text
outputs/market_analysis.md
outputs/market_analysis_complete.marker
```

Цель:

* проверить, существует ли проблема вовне
* интерпретировать local signals из KB inventory + Confluence
* выявить текущие паттерны решений
* классифицировать силу сигналов

---

## Шаг 5 — Synthesis Layer

**Cline skill:** `hypothesis-synthesis`

**Ручной шаблон:** `templates/synthesis-prompt.md`

Вход:

* role outputs
* hypothesis summary
* local evidence inventory
* business context analysis или явный gap
* market analysis

Ожидаемый output:

```text
outputs/hypothesis_map.md
outputs/hypothesis_digest.txt
outputs/synthesis_complete.marker
```

Цель:

* столкнуть внутренние и внешние сигналы
* выявить противоречия, слепые зоны, ловушки локальной оптимизации
* показать новую информацию, видимую только после сравнения
* определить влияние на исходную формулировку гипотезы

---

## Шаг 6 — Customer Discovery Planning

**Cline skill:** `customer-discovery-planning`

**Ручной шаблон:** `templates/customer-discovery-planning-prompt.md`

Вход:

* артефакты synthesis и предыдущих слоёв, включая Business Context или явный gap

Ожидаемый output:

```text
outputs/customer_discovery_plan.md
outputs/customer_discovery_planning_complete.marker
```

Цель:

* перевести неопределённость в практичный план CustDev-исследования
* приоритизировать неизвестные по влиянию на решение
* определить роли для интервью и behavior-based гайд

---

## Шаг 7 — Decision Review

**Cline skill:** `hypothesis-decision-review`

**Ручной шаблон:** `templates/decision-review-prompt.md`

Вход:

* существующие артефакты Roles, Local Evidence, Business Context, Market, Synthesis и Customer Discovery Planning

Ожидаемый output:

```text
outputs/decision_review.md
outputs/decision_review_complete.marker
```

Цель:

* оспорить выводы synthesis
* выявить слабые доказательства и скрытые допущения
* предложить самый дешёвый путь валидации
* не проводить новый retrieval/research и не вводить сигналы без ссылок

---

## Шаг 8 — Human Decision Report Export

**Cline skill:** `human-report-export`

**Шаблон:** `templates/human-report-template.html`

Ожидаемый output:

```text
outputs/human_report.html
outputs/human_report_complete.marker
```

Цель:

* собрать decision-facing HTML для человека
* показать confidence, recommendation, decision readiness, what changed
* дать ссылки на детальные Markdown-артефакты

---

## Шаг 9 — Решение человека

Человек изучает `outputs/human_report.html` и исходные Markdown-артефакты, затем принимает решение. Pipeline не принимает это решение автоматически.

---

## Ожидаемый результат

```text
examples/example-001/
  input/
    hypothesis.md
  run.md
  outputs/
    role_outputs/
    hypothesis_summary.md
    validation_questions.md
    discovery_preview.md
    evidence_inventory.md
    business_context_analysis.md
    missing_business_context.md  # только при отсутствии контекста
    market_analysis.md
    hypothesis_map.md
    hypothesis_digest.txt
    customer_discovery_plan.md
    decision_review.md
    human_report.html
    *.marker
```

---

## Примечания

Пример использует доменно-специфичную B2B AppSec гипотезу.

Сам фреймворк domain-agnostic.

Эталонные outputs в `examples/example-001/outputs/` служат референсными артефактами. Ветка без бизнес-контекста — `examples/example-004`. Негативные случаи — `examples/fixtures/`.

Статическая проверка контракта (stdlib, без LLM):

```text
python scripts/validate_runs.py
```
