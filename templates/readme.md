# Шаблоны

В этой папке лежат шаблоны выполнения для ручного запуска фреймворка.

Шаблоны задают **как вызывается каждый слой**, а не как конфигурируется модель.

Для **запуска в Cline** используйте skills в `.cline/skills/` — эти шаблоны являются исходным материалом для тех skills.

---

## Что такое шаблоны?

Шаблоны — структурированные промпты для выполнения каждого слоя:

* Roles Layer
* Local Evidence Discovery
* Business Context & Value Check
* Market Layer
* Synthesis Layer
* Customer Discovery Planning
* Decision Review
* Human Decision Report Export

Они работают как **интерфейс между пользователем и системой**.

---

## Это не системные промпты

Шаблоны НЕ являются полными системными промптами.

Они задают:

* структуру входа
* определение задачи
* ожидаемые outputs

---

## Как использовать

### 1. Cline (рекомендуется)

**Chat-first (новая гипотеза):**

```text
/run-hypothesis-conversational.md
```

**File-first (существующий RUN_DIR):**

```text
/run-hypothesis.md
```

Соответствие шаблонов и skills:

| Шаблон | Skill |
|----------|-------|
| `facilitator-prompt.md` | `hypothesis-facilitator` |
| `knowledge-retrieval-prompt.md` | `local-knowledge-retrieval` |
| `business-context-prompt.md` | `business-context-value-check` |
| `market-prompt.md` | `hypothesis-market-layer` |
| `synthesis-prompt.md` | `hypothesis-synthesis` |
| `customer-discovery-planning-prompt.md` | `customer-discovery-planning` |
| `decision-review-prompt.md` | `hypothesis-decision-review` |
| `human-report-template.html` | `human-report-export` |
| `input-schema.md` | `hypothesis-input-validation` |
| `input-schema.md` | `conversational-hypothesis-intake` (генерация draft) |

### 2. Прямое использование (вручную)

Скопируйте шаблон, заполните гипотезу, роли и контекст. Запустите как обычный промпт в любой LLM.

### 3. Внутренний workflow

Следуйте шагам вручную без автоматизации.

---

## Что входит в каждый шаблон

* обязательные входы
* описание задачи
* ожидания по output

---

## Связь с другими частями

* Playbook → описывает процесс
* Шаблоны → ручной запуск
* Skills → автоматизированный запуск в Cline
* Слои → задают логику рассуждения

---

## Важно

Шаблоны предполагают:

* ясную гипотезу
* определённые роли
* базовый research-контекст

Если вход слабый → выход будет слабым.

---

## Дальше

См.:

* `facilitator-prompt.md`
* `knowledge-retrieval-prompt.md`
* `business-context-prompt.md`
* `market-prompt.md`
* `synthesis-prompt.md`
* `customer-discovery-planning-prompt.md`
* `decision-review-prompt.md`
* `human-report-template.html`
