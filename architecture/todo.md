# TODO

## Имплементация Cline

- [x] Создать `.clinerules/` с правилами фреймворка
- [x] Создать `.cline/skills/` для каждого слоя
- [x] Создать workflows в `.clinerules/workflows/`
- [x] Задокументировать setup и контракт Cline
- [x] Задокументировать Confluence-first модель MCP
- [x] Обновить README и playbooks под Cline-first путь
- [x] Перенести ассеты RooCode в `assets/legacy/`

## Улучшения Market Layer

- [ ] Добавить структурированный research-контекст во вход
- [ ] Улучшить правила атрибуции источников
- [ ] Разделять local vs external сигналы в валидации
- [ ] Ввести автоматизацию классификации силы сигнала

## Улучшения Roles Layer

- [x] Добавить skill `hypothesis-facilitator` с 6-шаговым процессом stress-test
- [x] Добавить артефакт `validation_questions.md`
- [ ] Улучшить стратегию выбора ролей
- [ ] Добавить переиспользуемые шаблоны профилей ролей в `/roles`

## Experiment Design (будущее)

- [ ] Добавить фазу experiment design после Decision Review

## Synthesis Layer

- [x] Добавить skill `hypothesis-synthesis` с 7-шаговым collision-процессом и 5 категориями сигналов
- [ ] Улучшить автоматизацию классификации конфликтов
- [ ] Добавить автоматизацию scoring уверенности

## Decision Review

- [x] Добавить skill `hypothesis-decision-review` и workflow
- [x] Добавить контракт артефакта `decision_review.md`
- [x] Добавить разобранный пример с полным decision review в `examples/`

## Система

- [x] Задать минимальный жизнеспособный формат входа (`templates/input-schema.md`)
- [x] Стандартизировать структуру RUN_DIR (`architecture/run-structure.md`)

## Валидация входа / промпта

- [x] Добавить skill валидации до Roles Layer
- [ ] Автоматически детектировать отсутствующие роли в workflow
- [ ] Автоматически детектировать отсутствующий research-контекст

## Local Evidence Discovery — P0 #1

См. [roadmap/README.md](../roadmap/README.md#p0--поддержка-неструктурированной-базы-знаний). Релиз: **v2.3.0**.

- [x] Design-doc: `architecture/local-knowledge-retrieval.md`
- [x] Skill `local-knowledge-retrieval` — preview, guardrails, извлечение атомарных evidence
- [x] Workflow `/run-knowledge-retrieval.md`
- [x] Документация слоя + ручной шаблон (`layers/local-evidence-discovery-layer.md`, `templates/knowledge-retrieval-prompt.md`)
- [x] Интеграция в `/run-hypothesis.md` (шаг 3) и Market Layer (inventory-first)
- [x] Артефакты: `discovery_preview.md`, `evidence_inventory.md`, `knowledge_retrieval_complete.marker`
- [x] Контракты: `10-artifact-contracts.md`, `20-evidence-rules.md`
- [x] Документация, playbooks, SVG-диаграммы
- [x] Пример mixed-source: `examples/example-001/kb-samples/` + outputs discovery
- [ ] Поддержка `.pdf` / `.docx` / `.html` (V2)
- [ ] E2E на реальном Obsidian vault в `runs/HYP-*`

---

## Conversational Run (chat-first) — P0 #2

См. [roadmap/README.md](../roadmap/README.md#p0--conversational-run-chat-first-запуск-из-чата). Релизы: **v2.2.0** (базовый flow), **v2.2.1** (dirty input + trigger-теги), **v2.2.2** (dialog RUN_DIR + isolation).

- [x] Skill `conversational-hypothesis-intake` — guided Q&A, preview draft, confirm/revise/cancel
- [x] Workflow `/run-hypothesis-conversational.md` — intake → dialog-confirmed bootstrap `RUN_DIR` → validate → pipeline
- [x] Автоназначение ID (`HYP-*`, `RUN-*`) и правила в `10-artifact-contracts.md`
- [x] Chat-first как рекомендуемый путь в quick-start, README, playbooks (EN/RU)
- [x] Примеры `examples/chat-first-run.md`
- [x] Trigger-теги intake: `#гипотеза` / `#hypothesis`, `#контекст` / `#context`, `#роли` / `#roles`
- [x] Dirty input mode: извлечение из Q&A / CustDev + валидация mapping с пользователем
- [x] Статус до confirm RUN_DIR: `runs/ ещё НЕ создан`
- [x] Двойной confirm: draft гипотезы + предложенный `RUN_DIR` (Step 4a/4b)
- [x] Изоляция нового прогона: без `RUN_DIR:` — новый archive; не reuse открытых табов
- [x] Trigger `#новая` / `#new-run`; continue-existing только с явным `RUN_DIR:`
- [x] Artifact allowlist в conversational flow (без несуществующих артефактов)
- [x] Пример C: вторая гипотеза в тот же день (`002` vs `001`)
- [ ] E2E-пример: реальный `runs/HYP-*` с артефактами после chat-first прогона (не только walkthrough-doc)
- [ ] Доп. input patterns: FR/требования, Jira/Linear paste, многоязычные заголовки в `input/hypothesis.md`
- [ ] Шаблоны быстрых тегов в onboarding (P1): подсказка тегов при первом запуске

---

## Human Decision Report — P1 Phase 1

См. [roadmap/README.md](../roadmap/README.md#p1--human-output-и-режим-артефактов).

- [x] Skill `human-report-export` — собирать `human_report.html` из существующих артефактов
- [x] Workflow `/run-human-report-export.md`
- [x] Шаблон `templates/human-report-template.html`
- [x] Контракт в `10-artifact-contracts.md` — What changed?, Decision Readiness, grouped links
- [x] Интеграция в `/run-hypothesis.md`
- [x] Пример `examples/example-001/outputs/human_report.html`
- [x] Обновление executive report — business value, contradictions, cheapest validation (v2.4.0)
- [ ] Phase 2: режим артефактов `full` / `minimal` в начале прогона
- [ ] В будущем: полный экспорт прогона `run_report.html`

---

## Business Context & Value Check — P0 #3

См. [roadmap/README.md](../roadmap/README.md#p0--business-context--value-check-проверка-бизнес-контекста-и-ценности). Релиз: **v2.4.0**.

- [x] Skill `business-context-value-check`
- [x] Workflow `/run-business-context-value-check.md`
- [x] Документация слоя + ручной шаблон
- [x] Артефакты и контракты в `10-artifact-contracts.md`
- [x] Интеграция в `/run-hypothesis.md` и playbooks
- [x] Примеры example-001 и example-002

---

## Документация

- [x] Добавить Cline как основную имплементацию
- [x] Подчеркнуть inventory-first local evidence, затем Confluence MCP
- [x] Указать product manager как основного пользователя в README
- [ ] Добавить примеры профилей ролей

## Вторичный MCP (будущее)

- [ ] Интеграция Jira / Linear
- [ ] Интеграция Slack
- [ ] Web search для external signals
