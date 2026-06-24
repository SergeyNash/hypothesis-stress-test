Язык: [English](./CHANGELOG.md) | **Русский**

# Changelog

В этом файле фиксируются все значимые изменения фреймворка **Hypothesis Stress Test**.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/),
версионирование следует [Semantic Versioning](https://semver.org/lang/ru/).

Текущая версия: см. [VERSION](./VERSION).

## Политика версий

| Уровень | Когда повышать |
| ------- | -------------- |
| **MAJOR** | Breaking changes в структуре прогона, контрактах артефактов или обязательном входе |
| **MINOR** | Новые слои, skills, workflows или опциональные возможности |
| **PATCH** | Документация, уточнения, некритичные правки skills и rules |

Версия фреймворка не совпадает с ID отдельных прогонов гипотез (`HYP-YYYY-MM-DD-NNN`).

---

## [Unreleased]

### Добавлено

- **Human Decision Report MVP** — decision-facing `human_report.html` после Decision Review.
- Skill: `human-report-export` — компиляция verdict, readiness, reframing, validation priorities из существующих артефактов.
- Workflow: `/run-human-report-export.md`.
- Template: `templates/human-report-template.html`.
- Секции отчёта: What changed?, Decision Readiness, сгруппированные Detailed Artifacts с relative links.
- Marker: `human_report_complete.marker`.
- Пример: `examples/example-001/outputs/human_report.html`.

### Изменено

- `/run-hypothesis.md` — Human Decision Report Export как шаг 8 (после Decision Review).
- `.clinerules/10-artifact-contracts.md` — контракт `human_report.html`, mapping readiness, правила relative links.
- Playbooks, examples, architecture run-structure, cline-contract — human report как основной human-facing output.
- `roadmap/README.md` — P1 фаза 1 отмечена как реализована.

---

## [2.3.0] - 2026-06-23

### Добавлено

- **Local Evidence Discovery** — шаг до Market Layer для сбора трассируемых evidence из неструктурированной локальной KB (не «поиск по документам»).
- Skill: `local-knowledge-retrieval` (preview, guardrails, атомарные `EVID-NNN`).
- Workflow: `/run-knowledge-retrieval.md`.
- Layer doc: `layers/local-evidence-discovery-layer.md`.
- Manual template: `templates/knowledge-retrieval-prompt.md`.
- Design reference: `architecture/local-knowledge-retrieval.md`.
- Артефакты: `discovery_preview.md`, `evidence_inventory.md`, `knowledge_retrieval_complete.marker`.
- Контракт evidence: `evidence_type`, `relevance_reason`, `extraction_note`; правила атомарности.
- Пример mixed-source KB: `examples/example-001/kb-samples/` + discovery outputs.

### Изменено

- `/run-hypothesis.md` — Local Evidence Discovery как шаг 3 (между Facilitator и Market).
- Skill `hypothesis-market-layer` — inventory-first, затем Confluence MCP; четыре канала сигналов в output.
- `/run-market-layer.md` — читать `evidence_inventory.md` до Confluence search.
- `.clinerules/10-artifact-contracts.md`, `20-evidence-rules.md` — артефакты discovery и разделение каналов.
- Структура Market output: Local KB / Confluence / External / Inferred.
- Playbooks, quick-start, cline-setup, architecture docs, SVG diagrams — inventory-first flow.
- `examples/example-001/outputs/market_analysis.md` — local signals со ссылками на `EVID-*`.
- `roadmap/README.md` — P0 #1 отмечен как реализовано; `architecture/todo.md` — чеклист P0 #1.

---

## [2.2.2] - 2026-06-23

### Добавлено

- **Двойной confirm** для conversational run: (1) draft гипотезы (2) предложенный `RUN_DIR` (`HYP-YYYY-MM-DD-NNN`).
- **Диалог RUN_DIR** (Step 4b): сканирование прогонов за день, предложение следующего suffix, список существующих — «не трогаю».
- **New run isolation**: без явного `RUN_DIR:` в сообщении — всегда новый archive, без reuse открытых табов.
- **Trigger-тег** `#new-run` / `#новая` / `#новый-прогон` для явного указания нового прогона.
- **Artifact allowlist**: запрет несуществующих в контракте файлов (например `product_specification.md`) в conversational flow.
- Пример C (вторая гипотеза в тот же день → `002` vs `001`) в `examples/chat-first-run.md` и `.ru.md`.

### Изменено

- Skill `conversational-hypothesis-intake`: разделение Step 4a/4b, правила isolation, continue-existing только с `RUN_DIR:`.
- Workflow `run-hypothesis-conversational.md`: диалог RUN_DIR между confirm draft и bootstrap; do-not rules.
- `.clinerules/10-artifact-contracts.md` — dialog-confirmed bootstrap вместо автоматического.
- `.clinerules/00-hypothesis-framework.md` — режимы входа: новая гипотеза = новый `HYP-*-NNN` через диалог.
- Quick start, playbooks, cline-setup (EN/RU) — двойной confirm и guidance по `#новая`.

---

## [2.2.1] - 2026-06-23

### Добавлено

- **Trigger-теги intake** для conversational run: `#hypothesis`, `#context`, `#roles` (и RU-алиасы `#гипотеза`, `#контекст`, `#роли`).
- **Режим dirty input** (`#контекст`): извлечение полей гипотезы из таблиц Q&A, CustDev-заметок и неструктурированного discovery.
- **Шаг валидации извлечения**: агент показывает mapping Statement/Roles/Context и спрашивает подтверждение до draft карточки.
- **Статус-сообщения** до bootstrap: `runs/ ещё НЕ создан` до явного confirm.
- Пример B (dirty `#контекст`) в `examples/chat-first-run.md` и `.ru.md`.

### Изменено

- Skill `conversational-hypothesis-intake`: режимы intake (ready / dirty / roles-only), auto-detect, триггеры confirm.
- Workflow `run-hypothesis-conversational.md`: Step 0 определение режима; пример dirty input.
- Quick start, playbooks, cline-setup, README (EN/RU) — теги и guidance для грязных входов.
- `roadmap/README.md` — таблица релизов P0 #2 (2.2.0 / 2.2.1), follow-up бэклог.
- `architecture/todo.md` — секция Conversational Run (P0 #2): выполненное и открытые пункты.

---

## [2.2.0] - 2026-06-23

### Добавлено

- **Conversational Run (chat-first)** — основной сценарий запуска новой гипотезы из чата Cline.
- Новый skill: `conversational-hypothesis-intake` (guided Q&A, preview карточки, подтвердить/исправить/отменить).
- Новый workflow: `/run-hypothesis-conversational.md` (intake → auto bootstrap `RUN_DIR` → validate → полный pipeline).
- Автоматическое создание run archive в `runs/HYP-YYYY-MM-DD-NNN/` с `input/hypothesis.md` и `run.md`.
- Автоназначение metadata: `Hypothesis ID`, `Run ID`, `Created at`, `Status`.
- Repair-loop при failed validation: возврат в conversational intake перед повторной валидацией.
- Пошаговый пример: `examples/chat-first-run.md` (EN) и `examples/chat-first-run.ru.md` (RU).

### Изменено

- Chat-first задокументирован как **рекомендуемый** путь входа; file-first (`RUN_DIR` + `/run-hypothesis.md`) сохранён как fallback.
- `.clinerules/10-artifact-contracts.md` — правила bootstrap `RUN_DIR` и назначения ID в conversational flow.
- `.clinerules/00-hypothesis-framework.md` — таблица режимов входа (chat-first vs file-first).
- `roadmap/README.md` — Conversational Run отмечен как **P0 #2 реализовано**; Business Context перенумерован в P0 #3.
- Синхронизирована EN/RU документация: README, quick-start, cline-setup, cline-contract, playbooks, validate-input, templates/readme, architecture/implementations, architecture/overview, implementations/README.

---

## [2.1.0] - 2026-06-23

### Добавлено

- Новый этап **Customer Discovery Planning** между Synthesis и Decision Review.
- Новый skill: `customer-discovery-planning`.
- Новый workflow: `/run-customer-discovery-planning.md`.
- Новый manual template: `templates/customer-discovery-planning-prompt.md`.
- Новый layer doc: `layers/customer-discovery-planning-layer.md`.
- Новые артефакты: `customer_discovery_plan.md` и `customer_discovery_planning_complete.marker`.
- Добавлены примерные артефакты для `examples/example-001`:
  - `outputs/customer_discovery_plan.md`
  - `outputs/customer_discovery_planning_complete.marker`
- Новый skill: `local-knowledge-retrieval` (**Local Evidence Discovery**).
- Новый workflow: `/run-knowledge-retrieval.md`.
- Новый manual template: `templates/knowledge-retrieval-prompt.md`.
- Новый layer doc: `layers/local-evidence-discovery-layer.md`.
- Новые retrieval-артефакты: `discovery_preview.md`, `evidence_inventory.md`, `knowledge_retrieval_complete.marker`.

### Изменено

- Порядок полного пайплайна обновлён:
  - Validate -> Facilitator -> Market -> Synthesis -> Customer Discovery Planning -> Decision Review -> Human backlog decision.
- Prerequisites для Decision Review теперь учитывают outputs Customer Discovery Planning.
- В Synthesis следующий шаг теперь ведёт сначала в Customer Discovery Planning, затем в Decision Review.
- Контракты артефактов, workflows и документация синхронизированы в EN/RU:
  - README, playbooks, quick start, architecture docs, Cline contract/setup docs.
- Обновлены диаграммы пайплайна:
  - `assets/architecture-overview.svg`
  - `assets/artifact-flow.svg`
  - `assets/cline-workflow.svg`
- Полный пайплайн теперь включает Local Evidence Discovery перед Market:
  - Validate -> Facilitator -> Local Evidence Discovery -> Market -> Synthesis -> Customer Discovery Planning -> Decision Review -> Human backlog decision.
- В Market Layer добавлено раздельное представление каналов:
  - `Local Signals from Knowledge Base`
  - `Confluence Signals`
  - `External Market Signals`
  - `Inferred Signals`
- Market Layer теперь сначала использует `evidence_inventory.md`, затем Confluence, затем external/inferred.
- Обновлены контракты артефактов и evidence-rules для атомарных evidence items (`evidence_type`, `relevance_reason`, `extraction_note`) и retrieval preview.
- Синхронизирована EN/RU документация: architecture, playbooks, quick-start, Cline contract/setup, knowledge-base docs, templates.
- Дополнительно обновлены диаграммы и reference-output под новый поток:
  - `assets/cline-mcp-confluence.svg`
  - `assets/artifact-flow-clean.svg`
  - `examples/example-001/outputs/market_analysis.md`

---

## [2.0.0] - 2026-06-22

### Изменено

- **Контракт run archive (breaking):** вход гипотезы перенесён в `RUN_DIR/input/hypothesis.md`; outputs остаются в `RUN_DIR/outputs/`.
- Шаблон имени `RUN_DIR`: `runs/HYP-YYYY-MM-DD-NNN/`.
- Обязательный блок **Metadata** во входе: Hypothesis ID, Created at, Run ID, Status.
- Все skills, workflows, templates и документация обновлены под новые пути.
- `examples/example-001` переведён на layout архива (`input/`, `outputs/`, `run.md`).

### Добавлено

- Опциональная папка `input/attachments/` для вспомогательных файлов прогона.
- Migration note в `.clinerules/10-artifact-contracts.md` для пользователей старого layout.

---

## [1.3.0] - 2026-06-19

### Добавлено

- **Модель персон:** `knowledge-base/personas/`, `knowledge-base/interviews/`, `knowledge-base/persona-builds/`.
- Пять начальных AppSec personas (initial profiles, `confidence: low` до привязки CustDev).
- Правила persona evidence в `.clinerules/20-evidence-rules.md`.
- Поддержка matching personas в Roles Layer (`hypothesis-facilitator` skill).

---

## [1.2.0] - 2026-06-09

### Добавлено

- Паттерн **Local Optimization Trap** в Synthesis Layer.
- `validation_questions.md` как output Facilitator (behavior-based вопросы для интервью).

### Изменено

- Roles Layer в документации переименован в **Facilitator**.
- Расширены signal model и synthesis skill.

---

## [1.1.0] - 2026-06-09

### Добавлено

- **Decision Review** как обязательный gate после Synthesis.
- Skill `hypothesis-decision-review` и workflow `/run-decision-review.md`.
- Артефакты `decision_review.md` и `decision_review_complete.marker`.

---

## [1.0.0] - 2026-06-09

### Добавлено

- Tool-agnostic слоистый фреймворк: Roles, Market, Synthesis.
- **Cline adapter:** `.clinerules/`, `.cline/skills/`, slash-command workflows.
- Контракты артефактов, completion markers, изоляция `RUN_DIR`.
- Market Layer с Confluence-first и evidence rules (`local` / `external` / `inferred`).
- Quick Start, playbooks, architecture docs, `examples/example-001`.
- Двуязычная документация (EN / RU).

---

## [0.1.0] - 2026-06-08

### Добавлено

- Начальная концепция: стресс-тест существующих идей, а не генерация новых.
- Manual templates в `templates/`.
- Модель слоёв в `layers/`.

[2.2.2]: https://github.com/SergeyNash/hypothesis-stress-test/compare/v2.2.1...v2.2.2
[2.2.1]: https://github.com/SergeyNash/hypothesis-stress-test/compare/v2.2.0...v2.2.1
[2.2.0]: https://github.com/SergeyNash/hypothesis-stress-test/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/SergeyNash/hypothesis-stress-test/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/SergeyNash/hypothesis-stress-test/compare/v1.3.0...v2.0.0
[1.3.0]: https://github.com/SergeyNash/hypothesis-stress-test/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/SergeyNash/hypothesis-stress-test/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/SergeyNash/hypothesis-stress-test/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/SergeyNash/hypothesis-stress-test/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/SergeyNash/hypothesis-stress-test/releases/tag/v0.1.0
