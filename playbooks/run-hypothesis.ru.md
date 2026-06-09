Язык: [English](./run-hypothesis.md) | **Русский**

# Прогон гипотезы

Playbook описывает, как проверить продуктовую гипотезу через фреймворк.

**Основной метод:** Cline в VS Code со skills и workflows.
**Fallback:** ручной запуск шаблонов в любом LLM.

---

## Быстрый путь через Cline

1. Установить Cline — [implementations/cline-setup.ru.md](../implementations/cline-setup.ru.md)
2. Настроить Confluence MCP — [implementations/confluence-mcp.ru.md](../implementations/confluence-mcp.ru.md)
3. Создать `RUN_DIR/hypothesis.md`
4. В чате Cline:

```text
RUN_DIR: runs/my-hypothesis
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

Напишите чёткое, проверяемое утверждение в `RUN_DIR/hypothesis.md`.

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

## Шаг 1 — Roles Layer

**Cline:** skill `hypothesis-roles-layer` или в составе `/run-hypothesis.md`

**Ручной режим:** [templates/facilitator-prompt.md](../templates/facilitator-prompt.md)

Вход:

* гипотеза
* выбранные роли

Выход:

* `role_outputs/*`
* `hypothesis_summary.md`
* `ready_for_synthesis.marker`

Цель:

* выявить скрытые допущения
* понять границы внутренней ценности
* обнаружить friction и условия отказа

---

## Шаг 2 — Market Layer

**Cline:** skill `hypothesis-market-layer` или `/run-market-layer.md`

**Ручной режим:** [templates/market-prompt.md](../templates/market-prompt.md)

**Confluence first:** сначала поиск local signals в Confluence MCP.

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
* тип сигнала: local / external / inferred

---

## Шаг 3 — Synthesis Layer

**Cline:** skill `hypothesis-synthesis-layer` или `/run-synthesis.md`

**Ручной режим:** [templates/synthesis-prompt.md](../templates/synthesis-prompt.md)

Вход:

* outputs предыдущих шагов

Выход:

* `hypothesis_map.md`
* `hypothesis_digest.txt`
* `synthesis_complete.marker`

Цель:

* сравнить внутренние и внешние сигналы
* выявить противоречия
* классифицировать гипотезу

---

## Шаг 4 — Decision Review

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

## Шаг 5 — Backlog Decision (человек)

Изучите `decision_review.md` и примите финальное решение:

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

---

## Структура output

```text
RUN_DIR/
  hypothesis.md
  outputs/
    role_outputs/
    hypothesis_summary.md
    market_analysis.md
    hypothesis_map.md
    hypothesis_digest.txt
    decision_review.md
```

---

## Ожидаемое время

5–15 минут на гипотезу (с Cline).

---

## Советы

* формулируйте гипотезы узко
* явно определяйте роли
* настройте Confluence MCP для лучших local signals
* не пропускайте synthesis и decision review

---

## Принцип

Речь не о генерации идей.

Речь о решении:

> стоит ли этой идее вообще существовать
