Язык: [English](./run.md) | **Русский**

# Прогон

Этот файл описывает, как гипотеза была обработана через фреймворк.

---

## Вход

Файл гипотезы:

```text
examples/example-001/hypothesis.md
```

---

## Режим выполнения

**Основной:** Cline в VS Code с project rules, skills и workflows.

```text
RUN_DIR: examples/example-001
/run-hypothesis.md
```

**Fallback:** ручной запуск через шаблоны в любом LLM-интерфейсе.

---

## Предварительные требования

1. Установлено расширение Cline — [implementations/cline-setup.ru.md](../implementations/cline-setup.ru.md)
2. Настроен Confluence MCP (рекомендуется) — [implementations/confluence-mcp.ru.md](../implementations/confluence-mcp.ru.md)
3. Вход провалидирован — `/validate-hypothesis-input.md`

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

## Шаг 2 — Market Layer

**Cline skill:** `hypothesis-market-layer`

**Ручной шаблон:** `templates/market-prompt.md`

**Confluence first:** сначала поиск local signals в Confluence MCP.

Вход:

* формулировка гипотезы
* research context
* domain и тип продукта

Ожидаемый output:

```text
outputs/market_analysis.md
outputs/market_analysis_complete.marker
```

Цель:

* проверить, существует ли проблема вовне
* получить local signals из Confluence
* выявить текущие паттерны решений
* классифицировать силу сигналов

---

## Шаг 3 — Synthesis Layer

**Cline skill:** `hypothesis-synthesis`

**Ручной шаблон:** `templates/synthesis-prompt.md`

Вход:

* role outputs
* hypothesis summary
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

## Шаг 4 — Decision Review

**Cline skill:** `hypothesis-decision-review`

**Ручной шаблон:** `templates/decision-review-prompt.md`

Вход:

* артефакты synthesis и предыдущих слоёв

Ожидаемый output:

```text
outputs/decision_review.md
outputs/decision_review_complete.marker
```

Цель:

* оспорить выводы synthesis
* выявить слабые доказательства и скрытые допущения
* предложить самый дешёвый путь валидации

---

## Ожидаемый результат

```text
examples/example-001/
  hypothesis.md
  run.md
  outputs/
    role_outputs/
    hypothesis_summary.md
    validation_questions.md
    market_analysis.md
    hypothesis_map.md
    hypothesis_digest.txt
    decision_review.md
    *.marker
```

---

## Примечания

Пример использует доменно-специфичную B2B AppSec гипотезу.

Сам фреймворк domain-agnostic.

Эталонные outputs в `examples/example-001/outputs/` служат референсными артефактами.
