Язык: [English](./chat-first-run.md) | **Русский**

# Пример chat-first прогона

Этот документ описывает **conversational (chat-first)** сценарий: полный stress test из чата Cline без ручного создания `RUN_DIR` и редактирования `input/hypothesis.md`.

File-first fallback: [run.ru.md](./run.ru.md) и [example-001/](./example-001/).

---

## Trigger-теги intake

Добавьте тег в начало сообщения (после slash-команды), чтобы задать режим разбора:

| Тег | Когда использовать |
| --- | ------------------ |
| `#гипотеза` / `#hypothesis` | Уже есть чёткая формулировка If…then / Если…то |
| `#контекст` / `#context` | Сырые заметки, таблица Q&A, CustDev |
| `#роли` / `#roles` | Перечислены роли; нужно дособрать statement и context |

Алиасы: `#discovery`, `#custdev`.

**Важно:** `runs/` создаётся только после явного подтверждения draft (`Подтвердить и запустить`). До этого агент показывает: `runs/ ещё НЕ создан`.

---

## Предварительные требования

1. Установлено расширение Cline — [implementations/cline-setup.ru.md](../implementations/cline-setup.ru.md)
2. `.clinerules/` и `.cline/` в корне workspace — [implementations/quick-start.ru.md](../implementations/quick-start.ru.md)
3. Настроен Confluence MCP (рекомендуется) — [implementations/confluence-mcp.ru.md](../implementations/confluence-mcp.ru.md)

---

## Шаг 1 — Старт в чате (пример A — готовая гипотеза)

В чате Cline:

```text
/run-hypothesis-conversational.md

If Application Security engineers can manually prioritize projects in the SAST scanning queue, then business-critical applications will be scanned first, reducing time to detect high-risk vulnerabilities.
```

Агент активирует skill `conversational-hypothesis-intake`.

---

## Шаг 2 — Уточняющие вопросы (при необходимости)

Если первое сообщение неполное, агент задаёт короткие вопросы, например:

| Вопрос | Пример ответа |
| ------ | ------------- |
| Кого это напрямую затрагивает? | AppSec Engineer, CISO |
| Домен? | Application Security |
| Целевая аудитория? | Security teams in mid-to-large enterprises |
| Сценарий? | Queue-based SAST scan execution with competing project priorities |
| Ограничения? (опционально) | Must coexist with existing CI/CD pipelines |

Пропускайте вопросы, на которые пользователь уже ответил в первом сообщении.

---

## Шаг 3 — Preview карточки

Агент показывает canonical draft по [templates/input-schema.md](../templates/input-schema.md):

```markdown
# Hypothesis

## Metadata

- Hypothesis ID: (assigned at bootstrap)
- Created at: (assigned at bootstrap)
- Run ID: (assigned at bootstrap)
- Status: draft

## Statement

If Application Security engineers can manually prioritize projects in the SAST scanning queue, then business-critical applications will be scanned first, reducing time to detect high-risk vulnerabilities.

## Relevant Roles

- AppSec Engineer
- CISO

## Research Context

- Domain: Application Security
- Target audience: Security teams in mid-to-large enterprises
- Scenario: Queue-based SAST scan execution with competing project priorities
- Constraints: Must coexist with existing CI/CD pipelines
```

---

## Шаг 4 — Подтверждение

Агент спрашивает:

```text
Подтвердить и запустить / Исправить / Отменить
```

Пользователь отвечает: **Подтвердить и запустить**

До этого шага файлы не создаются.

---

## Шаг 5 — Автоматический bootstrap

Workflow `run-hypothesis-conversational.md` создаёт:

```text
runs/HYP-2026-06-23-001/
  input/
    hypothesis.md
    attachments/
  run.md
  outputs/
```

Metadata назначается автоматически:

- `Hypothesis ID`: `HYP-2026-06-23-001`
- `Run ID`: `RUN-2026-06-23-001`
- `Created at`: сегодняшняя дата
- `Status`: `draft` → `running` при старте pipeline

Агент сообщает, какой `RUN_DIR` создан.

---

## Шаг 6 — Валидация

Skill `hypothesis-input-validation` проверяет `input/hypothesis.md`.

При failed validation агент возвращается в repair mode (точечные вопросы), обновляет файл и повторяет валидацию.

---

## Шаг 7 — Полный pipeline

После pass validation workflow вызывает `/run-hypothesis.md` с bootstrapped `RUN_DIR`:

1. Facilitator (Roles Layer)
2. Local Evidence Discovery
3. Market Layer
4. Synthesis Layer
5. Customer Discovery Planning
6. Decision Review

Те же артефакты, что и при file-first — см. [run.ru.md](./run.ru.md).

---

## Шаг 8 — Прочитать результат

Начните с:

```text
runs/HYP-2026-06-23-001/outputs/hypothesis_digest.txt
```

Полные outputs в `outputs/` — та же структура, что в [example-001/outputs/](./example-001/outputs/).

---

## Исправить или отменить

| Пользователь говорит | Поведение |
| -------------------- | --------- |
| Исправить | Агент спрашивает, что изменить; показывает обновлённый draft; ждёт подтверждения снова |
| Отменить | `RUN_DIR` не создаётся; pipeline не запускается |

---

## Сравнение с file-first

| | Chat-first | File-first |
| - | ---------- | ---------- |
| Вход | `/run-hypothesis-conversational.md` | Ручной `input/hypothesis.md` + `/run-hypothesis.md` |
| RUN_DIR | Создаётся автоматически | Создаёт пользователь |
| Подтверждение | Обязательно до bootstrap | Неявное (пользователь сам написал файл) |
| Pipeline | Тот же `/run-hypothesis.md` после validation | Напрямую |

---

## Ссылки

- Skill: `.cline/skills/conversational-hypothesis-intake/SKILL.md`
- Workflow: `.clinerules/workflows/run-hypothesis-conversational.md`
- Schema: `templates/input-schema.md`
- Эталонные артефакты завершённого прогона: `examples/example-001/`

---

## Пример B — «Грязный» discovery-контекст (`#контекст`)

Когда есть CustDev/sales заметки, а не готовая If…then формулировка.

### Шаг 1 — Старт с тегом

```text
/run-hypothesis-conversational.md
#контекст

Моя гипотеза для AppSec инженеров, разработчиков и CISO:

Какую задачу хочет решить клиент? Группировка проектов сканирования с общими параметрами (API + UI).
Дополнительно: индивидуально настраиваемая ролевая модель.
Как клиент решает сейчас? Вручную переключает проекты.
Какой функциональности не хватает? Группировка + общие параметры сканирования + RBAC.
Предложения: доработка UI и API.
```

### Шаг 2 — Валидация извлечения

Агент объявляет режим и показывает mapping:

```text
Режим: #контекст (dirty discovery)

Извлёк черновик:

Statement:
If we add project grouping with shared scan parameters (API + UI) and configurable RBAC,
then AppSec engineers and developers can manage scan scope faster without manual per-project switching,
and the CISO gets more predictable governance.

Roles: AppSec Engineer, Developer, CISO
Domain: Application Security (SAST)
Scenario: Many scan projects without grouping or shared parameters

Верно? (да / исправить / отмена)
```

Пользователь: **да**

### Шаг 3 — Draft карточки → confirm → bootstrap

Тот же flow, что в примере A (шаги 3–8). Агент показывает полный preview `input/hypothesis.md`, затем:

```text
Статус: draft готов. runs/ ещё НЕ создан.
Подтвердить и запустить / Исправить / Отменить
```

Пользователь: **Подтвердить и запустить** → создаётся `runs/HYP-YYYY-MM-DD-NNN/`.
