# Дорожная карта

План развития фреймворка Hypothesis Stress Test.  
Документ только на русском языке.

## Обзор

> Сроки на диаграмме **ориентировочные** — для навигации по приоритетам и зависимостям. Детали — в разделах ниже.

```mermaid
gantt
    title Roadmap — задачи по приоритетам
    dateFormat YYYY-MM-DD
    axisFormat %b %Y
    todayMarker on

    section P0 — критично
    Conversational Run (chat-first)           :done, p0conv, 2026-06-01, 3w
    Неструктурированная KB                  :crit, p0kb, 2026-07-01, 8w
    Business Context & Value Check            :crit, p0biz, after p0kb, 6w

    section P1 — важно
    Onboarding (2 сценария)                   :p1on, 2026-07-15, 5w
    Human output HTML report фаза 1             :p1html, 2026-08-01, 5w
    Windows-safe rules/skills                 :p1win, after p1on, 3w
    Режим артефактов full/minimal фаза 2      :p1modes, after p1on, 4w

    section P2 — расширения
    Доп. источники local signals              :p2sig, 2026-10-01, 8w
```

| Задача | Приоритет | Статус | Зависимости |
| ------ | --------- | ------ | ----------- |
| [Неструктурированная KB](#p0--поддержка-неструктурированной-базы-знаний) | P0 #1 | запланировано | — |
| [Conversational Run (chat-first)](#p0--conversational-run-chat-first-запуск-из-чата) | P0 #2 | **реализовано** | — |
| [Business Context & Value Check](#p0--business-context--value-check-проверка-бизнес-контекста-и-ценности) | P0 #3 | запланировано | P0 #1 (частично; при структурированной KB — можно раньше) |
| [Onboarding (2 сценария)](#p1--упрощение-onboarding-два-пользовательских-сценария) | P1 | запланировано | — |
| [Human output и режим артефактов](#p1--human-output-и-режим-артефактов) | P1 | запланировано (фаза 1 — MVP) | Decision Review (текущий пайплайн) |
| [Windows-safe rules/skills](#p1--windows-safe-подключение-rulesskills) | P1 | запланировано | Onboarding |
| [Доп. источники local signals](#p2--дополнительные-источники-local-signals) | P2 | идея | P0 #1 (желательно) |

Приоритеты:

| Уровень | Значение |
| ------- | -------- |
| **P0** | Критично для практического использования |
| **P1** | Важно, но не блокирует текущий прогон |
| **P2** | Улучшения и расширения |

---

## P0 — Поддержка неструктурированной базы знаний

**Статус:** запланировано  
**Приоритет:** первый пункт roadmap

### Зачем

Сейчас фреймворк хорошо работает со структурированными артефактами:

- `RUN_DIR/input/hypothesis.md`
- `knowledge-base/personas/`, `interviews/`, `persona-builds/`
- Confluence через MCP

В реальности база знаний часто **неструктурирована**:

- свободные заметки без единой схемы
- скриншоты, диаграммы, фото whiteboard
- аудиозаписи интервью (с транскриптом или без)
- смешанные папки без фиксированной таксономии
- черновики в разных форматах и с разной степенью готовности

Без поддержки таких источников Market Layer и Customer Discovery Planning теряют local evidence и опираются в основном на Confluence или внешние источники.

### Цель

Научить фреймворк находить, интерпретировать и цитировать evidence из неструктурированной KB, сохраняя правила качества доказательств (`local` / `external` / `inferred`, no evidence → no claim).

### Область работ

- Поддержка гетерогенных локальных источников:
  - markdown и plain text
  - изображения (png, jpg, webp, скриншоты)
  - аудио (метаданные, транскрипты, ссылки на файлы)
- Стратегия discovery по «грязным» папкам KB без обязательной схемы именования
- Извлечение сигналов с привязкой к конкретному файлу/фрагменту
- Маппинг в существующую модель сигналов Market Layer
- Обратная совместимость с текущими контрактами `RUN_DIR`

### Вне scope (на этом этапе)

- Полная замена Confluence-first поведения
- Считать вывод модели доказательством без ссылки на источник
- Принудительная жёсткая схема KB для пользователя

### Ожидаемые результаты

- Спецификация discovery для неструктурированных источников
- Правила извлечения evidence из заметок, изображений и аудио
- Обновление Market Layer, evidence rules и связанной документации
- Пример прогона с mixed-source local evidence

### Фазы реализации

**Фаза A (завершено): дизайн**

- design-doc: [`architecture/local-knowledge-retrieval.md`](../architecture/local-knowledge-retrieval.md)
- формализация `discovery_preview.md` и `evidence_inventory.md`
- контракт evidence (`evidence_type`, `relevance_reason`, `extraction_note`, атомарность)
- пример workflow на уровне спецификации (без кода)

**Фаза B (в работе): реализация**

- новый skill/workflow для Local Evidence Discovery
- интеграция с Market Layer и контрактами артефактов
- обновление playbooks/docs/examples

Фаза B реализуется после review design-doc и уточняет контракты, workflow и документацию.

### Критерии готовности

- Прогон даёт полезные local signals даже при «грязной» KB
- `market_analysis.md` содержит findings со ссылками на конкретные источники (файл, страница, фрагмент)
- Структурированные workflow (`RUN_DIR`, personas, interviews) продолжают работать без изменений для пользователя

### Затрагиваемые компоненты (план)

- **Фаза A (дизайн):**
  - `architecture/local-knowledge-retrieval.md`
  - `roadmap/README.md` (этот раздел)
- **Фаза B (реализация, позже):**
  - `hypothesis-market-layer` — расширение local signal retrieval
  - `.clinerules/20-evidence-rules.md` — правила для mixed-format sources
  - `knowledge-base/` — документация по неструктурированным материалам
  - `implementations/quick-start.ru.md` — сценарии «есть своя KB»

---

## P0 — Conversational Run (chat-first запуск из чата)

**Статус:** реализовано  
**Приоритет:** второй пункт roadmap (P0 #2)

### Зачем

Ручной UX (`создать RUN_DIR` → заполнить `input/hypothesis.md` → `RUN_DIR: …` + `/run-hypothesis.md`) создаёт высокий порог входа. Пользователь должен уметь запускать stress test прямо из диалога в Cline.

### Цель

Основной сценарий запуска через чат: агент собирает карточку гипотезы, пользователь подтверждает, система автоматически создаёт `RUN_DIR` и запускает полный pipeline.

### Реализованные компоненты

- Skill: `conversational-hypothesis-intake` — guided Q&A, draft preview, confirm/revise/cancel
- Workflow: `/run-hypothesis-conversational.md` — bootstrap `RUN_DIR`, validation, handoff в `/run-hypothesis.md`
- Документация: chat-first как recommended path в quick-start, README, playbooks
- Пример: [examples/chat-first-run.md](../examples/chat-first-run.md)

### Критерии готовности (выполнены)

- Запуск новой гипотезы без ручного создания `RUN_DIR` и без редактирования `input/hypothesis.md`
- Обязательный confirm-step перед bootstrap
- Созданный файл соответствует `templates/input-schema.md` и проходит validation
- File-first путь сохранён как fallback

### Затрагиваемые файлы

- `.cline/skills/conversational-hypothesis-intake/SKILL.md`
- `.clinerules/workflows/run-hypothesis-conversational.md`
- `.clinerules/10-artifact-contracts.md` — правила auto ID assignment
- `implementations/quick-start.md`, `README.md`, playbooks, examples

---

## Зависимости между P0

Три приоритетных пункта P0 связаны так:

1. **P0 #1 — неструктурированная KB** даёт доступ к материалам стратегии в «грязной» базе знаний (`strategy/*`, `okr/*`, `business-model/*` и эквиваленты).
2. **P0 #2 — Conversational Run** снижает порог входа; **не зависит** от P0 #1 и P0 #3, работает с текущим контрактом `input/hypothesis.md`.
3. **P0 #3 — Business Context & Value Check** использует материалы стратегии для проверки бизнес-механизма ценности.

```text
P0 #2 (Conversational Run)     ← независим, реализован
P0 #1 (Unstructured KB)
  → находит strategy/okr/business-model в KB
P0 #3 (Business Context & Value Check)
  → строит карту ценности и strategic fit
  → передаёт сигнал в Market / Synthesis
```

Без P0 #1 слой P0 #3 может работать только при уже структурированной KB.  
Без материалов стратегии в KB P0 #3 не анализирует гипотезу, а фиксирует gap (`missing_business_context.md`).

---

## P0 — Business Context & Value Check (проверка бизнес-контекста и ценности)

**Статус:** запланировано  
**Приоритет:** третий пункт roadmap (зависит от P0 #1 и от наличия стратегии в KB)

### Проблема

Сейчас фреймворк отвечает на вопросы:

- есть ли боль?
- есть ли рынок?
- есть ли подтверждение?
- есть ли противоречия?
- что исследовать дальше?

Но нигде не задаётся ключевой B2B-вопрос:

> Если всё это правда, почему компания должна этим заниматься?

Большинство продуктовых гипотез погибают не потому, что проблема не существует.  
Они погибают потому, что проблема существует **не у того человека** — или не создаёт бизнес-ценность для компании.

Типичный провал:

| Сигнал | Статус |
| ------ | ------ |
| Problem Exists | да |
| Market Confirms | да |
| Users Want It | да |
| Revenue / Strategic Impact | неизвестно |

Текущий фреймворк может ошибочно считать такую ситуацию успешной, хотя в реальности это плохая инвестиция.

### Reference case (B2B AppSec)

- Developer: «мне неудобно работать»
- AppSec Engineer: «да, это неудобно»
- Интервью и рынок подтверждают проблему
- Но CISO не принимает решение о покупке на основании этой возможности
- Или фича не помогает выигрывать тендеры
- Или клиенты готовы жить без неё ещё 5 лет

### Какой вопрос решает слой

Не:

> Сколько денег принесёт?

На это почти никогда нет данных на ранней стадии.

А:

> Через какой механизм эта гипотеза может создать ценность для бизнеса?

Слой строит **карту движения ценности**:

```text
Проблема
  ↓
Получатель пользы
  ↓
Изменение поведения
  ↓
Бизнес-эффект
```

Для каждой гипотезы нужно понять:

- кто получает пользу?
- кто принимает решение?
- кто платит?
- кто внедряет?
- кто сопротивляется?

Очень часто это разные люди. Роли анализируются независимо в Stress Test, но никто не отвечает: **кто вообще готов за это платить?**

### Ключевая идея

Слой **не** отвечает: делать или не делать?

Слой отвечает:

> Если гипотеза подтвердится, как именно она создаст ценность для бизнеса?

И имеет право зафиксировать:

> Проблема реальна, но бизнес-кейс пока не доказан.

Для сложных B2B-продуктов это зачастую важнее любого анализа ролей или рынка.

### Поведение skill (план)

**Шаг 1 — Проверка бизнес-контекста**

Искать в KB (после P0 #1 или в структурированных папках):

- `strategy/*`
- `okr/*`
- `business-model/*`
- сегментация, GTM, positioning (эквиваленты)

Если данных нет:

- **не анализировать**
- создать `missing_business_context.md` со списком отсутствующих источников

**Шаг 2 — Карта заинтересованных сторон**

Построить цепочку, например:

```text
Developer          → получает пользу
AppSec Lead        → использует результат
CISO               → принимает решение
Budget Owner       → финансирует
```

**Шаг 3 — Механизм создания ценности**

Классифицировать тип бизнес-эффекта (не деньги, а механизм):

- Revenue Driver
- Retention Driver
- Competitive Driver
- Adoption Driver
- Operational Driver

**Шаг 4 — Проверка связи со стратегией**

Пример:

- Стратегия: «отобрать долю у Appscreener»
- Вопрос: «эта гипотеза помогает выиграть тендер?»
- Если нет: `Strategic Fit = Low`

### Артефакты (целевой контракт)

**`business_context_analysis.md`** — полный анализ:

```markdown
# Business Context Analysis

## Доступный контекст
...

## Недостающий контекст
...

## Карта заинтересованных сторон
...

## Поток создания ценности
...

## Тип бизнес-эффекта
- Revenue Driver
- Retention Driver
- Competitive Driver
- Adoption Driver
- Operational Driver

## Связь со стратегией
...

## Основные риски
...

## Основные возможности
...
```

**`missing_business_context.md`** — только если не хватает данных для анализа.

**`business_context_complete.marker`** — сигнал готовности для следующих слоёв (будущая интеграция).

### Место в пайплайне (целевое)

```text
Hypothesis
  ↓
Hypothesis Stress Test (Roles)
  ↓
Business Context & Value Check   ← новый слой
  ↓
Market Reality Check
  ↓
Hypothesis Synthesis
  ↓
Customer Discovery Planning
  ↓
Decision Review
```

### Критерии готовности

- Слой отделяет «problem exists» от «business case plausible»
- При отсутствии стратегии в KB создаётся явный gap-артефакт, а не «успешный» вывод
- Synthesis получает сигнал о strategic fit и value mechanism
- Reference case AppSec (Developer/AppSec vs CISO/budget) воспроизводим в примере

### Затрагиваемые компоненты (будущая реализация)

- новый skill: `business-context-value-check` (рабочее имя)
- workflow: `/run-business-context-value-check.md`
- layer doc + manual template
- обновление `.clinerules/00-hypothesis-framework.md`, `10-artifact-contracts.md`, playbooks, diagrams — после утверждения roadmap

---

## P1 — Упрощение onboarding (два пользовательских сценария)

**Статус:** запланировано

Явно описать и упростить два пути:

1. **Нет своей базы знаний** — работа из корня `hypothesis-stress-test`, без bridge-папок
2. **Есть своя база знаний** — `hypothesis-stress-test/` внутри KB + `.clinerules`/`.cline` в корне workspace (копия или junction)

Для сценария «есть KB» рекомендуется хранить материалы стратегии — это prerequisite для P0 #3:

- `strategy/` — стратегия, positioning, GTM
- `okr/` — цели и приоритеты
- `business-model/` — сегментация, монетизация, unit economics (если есть)

Без этих материалов Business Context & Value Check создаст `missing_business_context.md` вместо анализа.

В **фазе 2** [Human output](#p1--human-output-и-режим-артефактов) onboarding должен спрашивать предпочтение режима артефактов: `full` (все `.md` на виду) или `minimal` (только финальный HTML-отчёт).

Включить Windows-safe инструкции (копирование по умолчанию, junction как advanced).

---

## P1 — Windows-safe подключение rules/skills

**Статус:** запланировано

- Документировать `robocopy` как дефолт для синхронизации `.clinerules` и `.cline`
- Junction (`mklink /J`) — как продвинутый вариант
- Убрать из quick-start неоднозначные команды (`&&` в PowerShell 5.1, `mklink` без `cmd /c`)

---

## P1 — Human output и режим артефактов

**Статус:** запланировано (фаза 1 — первая реализация)  
**Приоритет:** P1 — важно для adoption, не блокирует текущий прогон

### Проблема

Полный прогон создаёт **слишком много текста** для ручного чтения:

| Слой | Артефакты |
| ---- | --------- |
| Facilitator | `role_outputs/*.md`, `hypothesis_summary.md`, `validation_questions.md` |
| Market | `market_analysis.md` |
| Synthesis | `hypothesis_map.md`, `hypothesis_digest.txt` |
| CustDev | `customer_discovery_plan.md` |
| Decision | `decision_review.md` |
| Служебные | 5× `*.marker` |

Уже есть попытка сжать вывод (`hypothesis_digest.txt`, Executive Summary в `decision_review.md`), но workflow и документация по-прежнему ориентируют человека на чтение цепочки Markdown.

Человеку нужен **один финальный срез**, а не 10+ файлов.  
Агентам нужны детальные артефакты — но это не обязательно human-facing формат.

### Целевая модель

Два класса артефактов:

```text
Machine-facing (между слоями)     Human-facing (для человека)
─────────────────────────────     ────────────────────────────
role_outputs/*.md                   human_report.html
market_analysis.md                  (открыть в браузере)
hypothesis_map.md
*.marker
```

- **Промежуточные** — контракт между слоями/skills (сегодня Markdown; в будущем — JSON).
- **Human-facing** — один удобный отчёт (фаза 1: HTML).

### Фазы

| Фаза | Scope | Статус |
| ---- | ----- | ------ |
| **1** | HTML-экспорт финала после Decision Review | первая реализация (MVP) |
| **2** | Настраиваемый режим при старте прогона (`full` / `minimal`) | запланировано |
| **3** | Machine-readable JSON между агентами в режиме `minimal` | идея / после фазы 2 |

#### Фаза 1 — HTML final report (MVP)

**Триггер:** после `decision_review_complete.marker`.

**Новый артефакт:** `outputs/human_report.html`

**Содержимое** (human slice, без дублирования всего pipeline):

- метаданные и statement из `input/hypothesis.md`
- `hypothesis_digest.txt`
- Executive Summary + Recommendation + Confidence из `decision_review.md`
- краткий блок «что делать дальше» из `customer_discovery_plan.md` (top priorities)
- опционально: ссылки «подробнее» на исходные `.md` (drill-down), без встраивания всего `hypothesis_map.md`

**Ограничения MVP:**

- статический HTML + inline CSS
- без сборщика, открывается локально в браузере
- все `.md` остаются источником истины (обратная совместимость)

#### Фаза 2 — настройка при старте (запланировано)

Вопрос пользователю в начале прогона (связь с [P1 onboarding](#p1--упрощение-onboarding-два-пользовательских-сценария)):

| Режим | Поведение |
| ----- | --------- |
| `full` (по умолчанию сейчас) | все `.md` как сейчас + HTML в конце |
| `minimal` | человеку — только `human_report.html`; промежуточные файлы не акцентируются в workflow |

Где хранить настройку — открытый вопрос: поле в `input/hypothesis.md` (Metadata) или отдельный `run_config`.

#### Фаза 3 — JSON между агентами (идея)

- В режиме `minimal` слои обмениваются структурированными snapshot (JSON schema TBD)
- Markdown остаётся для режима `full` и для отладки
- **Вне scope фазы 1**

### Критерии готовности (фаза 1)

- После полного прогона в `RUN_DIR/outputs/` есть открываемый `human_report.html`
- Человек получает verdict (confidence + recommendation) и next steps **без обязательного чтения** `hypothesis_map.md` / `role_outputs/*`
- Промежуточные `.md` по-прежнему создаются
- Целевой пример: `examples/example-001/outputs/human_report.html` (при будущей реализации)

### Затрагиваемые компоненты (будущая реализация)

- новый skill или post-step: `human-report-export` (рабочее имя)
- workflow: `/run-human-report-export.md` или шаг в `run-decision-review`
- template HTML + mapping из существующих артефактов
- `.clinerules/10-artifact-contracts.md`, playbooks, `run-hypothesis.md` — после roadmap
- P1 onboarding — вопрос о режиме `full` / `minimal` (фаза 2)

---

## P2 — Дополнительные источники local signals

**Статус:** идея

- Jira / Linear
- Slack
- Веб-поиск для external signals (с явным approval)

См. также внутренний список задач: [architecture/todo.md](../architecture/todo.md).
