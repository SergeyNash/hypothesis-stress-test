# Схема входных данных / Input Schema

Минимальный вход гипотезы может быть оформлен на русском или английском. Парсер
обязан принимать перечисленные ниже алиасы независимо от языка основного текста.
Не смешивайте языки без необходимости: выбранный пользователем язык заголовков и
тела сохраняется в draft и downstream outputs.

## Required

### Metadata / Метаданные

- **Hypothesis ID / ID гипотезы** — стабильный идентификатор `HYP-YYYY-MM-DD-NNN`
- **Created at / Дата создания** — дата создания архива (`YYYY-MM-DD`)
- **Run ID / ID прогона** — идентификатор выполнения `RUN-YYYY-MM-DD-NNN`
- **Status / Статус** — хранится как `draft` | `running` | `completed` | `archived`

---

### Statement / Формулировка

Конкретная проверяемая формулировка: предлагаемое изменение, ожидаемый результат
и наблюдаемый способ понять, что результат достигнут.

---

### Relevant Roles / Релевантные роли

Только роли, которых гипотеза затрагивает напрямую. Требуется минимум одна роль,
рекомендуется 2–4, более 5 не допускается без уточнения scope.

---

### Research Context / Контекст исследования

- **Domain / Домен**
- **Target audience / Целевая аудитория**
- **Scenario / Сценарий**

---

## Optional

- **Constraints / Ограничения**
- Known assumptions
- Owner

## Правила алиасов и нормализации

- Канонические разделы распознаются по любой паре: `Metadata` / `Метаданные`,
  `Statement` / `Формулировка`, `Relevant Roles` / `Релевантные роли` /
  `Затронутые роли`, `Research Context` / `Контекст исследования`.
- Поля контекста распознаются как `Domain` / `Домен`, `Target audience` /
  `Целевая аудитория`, `Scenario` / `Сценарий`, `Constraints` / `Ограничения`.
- Один конкретный язык заголовков не обязателен. Регистр и окружающий Markdown
  не меняют смысл, но один канонический раздел не должен встречаться дважды под
  разными алиасами.
- Значение `Status` хранится как английский токен. Парсер может распознать
  локализованные значения `черновик` → `draft`, `выполняется` / `в работе` →
  `running`, `завершён` / `завершено` → `completed`, `архив` / `архивирован` →
  `archived`, но validation должен предложить нормализовать файл и не выполнять
  эту запись без подтверждения пользователя.

---

## Пример на русском

```markdown
# Гипотеза

## Метаданные

- ID гипотезы: HYP-2026-06-22-001
- Дата создания: 2026-06-22
- ID прогона: RUN-2026-06-22-001
- Статус: draft

## Формулировка

Если AppSec-инженеры смогут вручную приоритизировать проекты в очереди SAST, то критичные приложения будут сканироваться раньше, что сократит время обнаружения уязвимостей высокого риска.

## Релевантные роли

- AppSec-инженер
- CISO

## Контекст исследования

- Домен: Application Security
- Целевая аудитория: команды безопасности средних и крупных компаний
- Сценарий: очередь SAST с конкурирующими приоритетами проектов
```

## Example in English

```markdown
# Hypothesis

## Metadata

- Hypothesis ID: HYP-2026-06-22-001
- Created at: 2026-06-22
- Run ID: RUN-2026-06-22-001
- Status: draft

## Statement

If Application Security engineers are able to manually prioritize projects in the SAST scanning queue, then business-critical applications will be scanned first, reducing the time required to detect high-risk vulnerabilities.

## Relevant Roles

* AppSec Engineer
* CISO

## Research Context

* Domain: Application Security
* Target audience: Security teams in mid-to-large enterprises
* Scenario: Queue-based SAST scan execution with competing project priorities
```

---

## Archive location

Store the input file at:

```text
RUN_DIR/input/hypothesis.md
```

Where `RUN_DIR` is the hypothesis run archive, e.g. `runs/HYP-2026-06-22-001/`.

**Chat-first:** use `/run-hypothesis-conversational.md` — the workflow creates `RUN_DIR` and writes this file after user confirms the draft. Use `#hypothesis` for ready If…then statements or `#context` for dirty discovery notes. See [examples/chat-first-run.md](../examples/chat-first-run.md).

**File-first:** create `RUN_DIR` and `input/hypothesis.md` manually before `/run-hypothesis.md`.

---

## Principle

Weak input → weak output
