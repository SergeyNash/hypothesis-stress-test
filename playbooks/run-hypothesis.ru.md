Язык: [English](./run-hypothesis.md) | **Русский**

# Прогон гипотезы

Playbook описывает, как проверить продуктовую гипотезу через фреймворк.

**Основной метод:** Cline в VS Code со skills и workflows.
**Fallback:** ручной запуск шаблонов в любом LLM.

---

## Быстрый путь через Cline

### Chat-first (рекомендуется)

1. Установить Cline — [implementations/cline-setup.ru.md](../implementations/cline-setup.ru.md)
2. Настроить Confluence MCP — [implementations/confluence-mcp.ru.md](../implementations/confluence-mcp.ru.md)
3. В чате Cline:

```text
/run-hypothesis-conversational.md

Опишите гипотезу естественным языком.
```

**Теги intake:** `#гипотеза`, `#контекст`, `#роли`, `#новая`.  
**Двойной confirm:** draft карточки → предложенный `RUN_DIR` (напр. `002`, если `001` есть). См. [examples/chat-first-run.ru.md](../examples/chat-first-run.ru.md).

Агент собирает вход, показывает draft, предлагает новый `RUN_DIR` в диалоге, создаёт папку только после подтверждения, валидирует и запускает pipeline.

### File-first (fallback)

1. Создать `RUN_DIR/input/hypothesis.md` — см. [templates/input-schema.md](../templates/input-schema.md)
2. В чате Cline:

```text
RUN_DIR: runs/HYP-2026-06-22-001
/run-hypothesis.md
```

Или по шагам:

```text
/validate-hypothesis-input.md
```

Затем отдельные workflow по слоям.

---

## Цель

Определить, создаёт ли гипотеза:

* реальную ценность
* выдерживает ли внешнюю проверку
* или должна быть отброшена на раннем этапе

---

## Шаг 0 — Сформулировать гипотезу

Напишите чёткое, проверяемое утверждение в `RUN_DIR/input/hypothesis.md`.

Дополнительно определите:

1. **Relevant roles** (для внутреннего анализа)
2. **Research context** (для market validation)

См. [templates/input-schema.md](../templates/input-schema.md).

### Гипотеза

Хорошо:

> Users need a way to prioritize notifications based on context

Плохо:

> Improve user experience

### Relevant Roles

Выбирайте только роли, которые напрямую затронуты.

### Research Context

* domain / тип продукта
* target audience
* сценарий использования
* constraints (опционально)

Валидируйте вход перед запуском — skill `hypothesis-input-validation` или `/validate-hypothesis-input.md`.

---

## Шаг 1 — Facilitator (Roles Layer / Hypothesis Stress Test)

**Cline:** skill `hypothesis-facilitator` или `/run-facilitator.md` или в составе `/run-hypothesis.md`

**Ручной режим:** [templates/facilitator-prompt.md](../templates/facilitator-prompt.md)

Эта фаза **не**: принимает решения, исследует рынок, синтезирует выводы, проектирует эксперименты.

Вход:

* гипотеза
* выбранные роли

Выход:

* `role_outputs/*`
* `hypothesis_summary.md`
* `validation_questions.md`
* `ready_for_synthesis.marker`

Цель:

* вскрыть скрытые допущения и границы применимости
* показать конфликты ролей
* сгенерировать behavior-based вопросы для интервью
* найти, где гипотеза ломается

Язык outputs = язык `input/hypothesis.md`.

---

## Шаг 2 — Local Evidence Discovery

**Cline:** skill `local-knowledge-retrieval` или `/run-knowledge-retrieval.md`

**Ручной режим:** [templates/knowledge-retrieval-prompt.md](../templates/knowledge-retrieval-prompt.md)

Выход:

* `discovery_preview.md`
* `evidence_inventory.md`
* `knowledge_retrieval_complete.marker`

Правила:

* один evidence item = один атомарный сигнал
* без синтеза в retrieval-шаге
* preview всегда создаётся; в V1 извлечение продолжается автоматически

---

## Шаг 3 — Market Layer (Market Reality Check)

**Cline:** skill `hypothesis-market-layer` или `/run-market-layer.md`

**Ручной режим:** [templates/market-prompt.md](../templates/market-prompt.md)

**Inventory first:** сначала используйте `evidence_inventory.md`, затем Confluence MCP для дополнительных внутренних сигналов.

Вход:

* гипотеза
* research context

Выход:

* `market_analysis.md`
* `market_analysis_complete.marker`

Правила:

* нет evidence → нет утверждения
* источники должны быть явными
* разделяйте факты и допущения
* держите каналы раздельно: KB / Confluence / external / inferred

---

## Шаг 4 — Synthesis Layer

**Cline:** skill `hypothesis-synthesis` или `/run-synthesis.md`

**Ручной режим:** [templates/synthesis-prompt.md](../templates/synthesis-prompt.md)

Эта фаза **не**: пересказывает без сравнения, добавляет сигналы, принимает финальные решения.

Prerequisites: `ready_for_synthesis.marker` + `market_analysis_complete.marker`

Вход:

* `role_outputs/*`, `hypothesis_summary.md`, `market_analysis.md`
* опционально: `validation_questions.md`

Выход:

* `hypothesis_map.md`
* `hypothesis_digest.txt` (макс. 150 слов)
* `synthesis_complete.marker`

Цель:

* столкнуть внутренние и внешние сигналы
* выявить противоречия, слепые зоны, ловушки локальной оптимизации
* показать новую информацию, видимую только после сравнения
* определить влияние на исходную формулировку гипотезы

---

## Шаг 5 — Customer Discovery Planning

**Cline:** skill `customer-discovery-planning` или `/run-customer-discovery-planning.md`

**Ручной режим:** [templates/customer-discovery-planning-prompt.md](../templates/customer-discovery-planning-prompt.md)

Эта фаза **не**: валидирует гипотезу, принимает продуктовые решения, рекомендует имплементацию.

Вход:

* артефакты synthesis и предыдущих слоёв

Выход:

* `customer_discovery_plan.md`
* `customer_discovery_planning_complete.marker`

Цель:

* выделить критические неизвестные и непроверенные допущения
* определить отсутствующие evidence и нужные customer conversations
* собрать практичный план интервью и ролей

---

## Шаг 6 — Decision Review

**Cline:** skill `hypothesis-decision-review` или `/run-decision-review.md`

**Ручной режим:** [templates/decision-review-prompt.md](../templates/decision-review-prompt.md)

Вход:

* артефакты synthesis и предыдущих слоёв

Выход:

* `decision_review.md`
* `decision_review_complete.marker`

Цель:

* оспорить выводы synthesis
* выявить слабые доказательства и скрытые допущения
* предложить самый дешёвый путь валидации

Не пропускайте этот шаг. Decision Review не пересказывает synthesis — добавляет adversarial critique.

---

## Шаг 7 — Human Decision Report Export

**Cline:** skill `human-report-export` или `/run-human-report-export.md`

**Шаблон:** [templates/human-report-template.html](../templates/human-report-template.html)

Вход:

* завершённый decision review и предыдущие артефакты

Выход:

* `human_report.html`
* `human_report_complete.marker`

Цель:

* собрать decision-facing HTML-отчёт для человека
* показать confidence, recommendation, decision readiness, what changed, validation priorities
* дать сгруппированные ссылки на детальные Markdown-артефакты

Откройте `outputs/human_report.html` в браузере. Markdown остаётся источником истины.

---

## Шаг 8 — Backlog Decision (человек)

Изучите `human_report.html` (или `decision_review.md`) и примите финальное решение:

* Proceed
* Proceed with Validation
* Additional Research Required
* Reject

---

## Модель интерпретации

### Validated Opportunity

Внутренние и внешние сигналы совпадают. → Продолжать разработку

### Internal Illusion

Внутренняя логика поддерживает, рынок — нет. → НЕ строить

### Blind Spot

Рынок показывает сигнал, внутренняя модель — нет. → Исследовать глубже

### Weak Signal

Нет сильных доказательств нигде. → Низкий приоритет

### Local Optimization Trap

Роли и рынок подтверждают боль, но решение не создаёт стратегической ценности. → Переформулировать или сузить scope

---

## Структура output

```text
RUN_DIR/
  input/
    hypothesis.md
  outputs/
    role_outputs/
    hypothesis_summary.md
    validation_questions.md
    market_analysis.md
    hypothesis_map.md
    hypothesis_digest.txt
    customer_discovery_plan.md
    decision_review.md
    human_report.html
```

---

## Ожидаемое время

5–15 минут на гипотезу (с Cline).

---

## Советы

* формулируйте гипотезы узко
* явно определяйте роли
* настройте Confluence MCP для лучших local signals
* не пропускайте customer discovery planning и decision review

---

## Принцип

Речь не о генерации идей.

Речь о решении:

> стоит ли этой идее вообще существовать
