# TODO

## Cline Implementation

- [x] Create `.clinerules/` with framework rules
- [x] Create `.cline/skills/` for each layer
- [x] Create workflows in `.clinerules/workflows/`
- [x] Document Cline setup and contract
- [x] Document Confluence-first MCP model
- [x] Update README and playbooks for Cline-first path
- [x] Archive RooCode assets to `assets/legacy/`

## Market Layer Improvements

- [ ] Add structured research context to input
- [ ] Improve source attribution rules
- [ ] Separate local vs external signals in validation
- [ ] Introduce signal strength classification automation

## Roles Layer Improvements

- [x] Add `hypothesis-facilitator` skill with 6-step stress-test process
- [x] Add `validation_questions.md` artifact
- [ ] Improve role selection strategy
- [ ] Add reusable role profile templates in `/roles`

## Experiment Design (future)

- [ ] Add experiment design phase after Decision Review

## Synthesis Layer

- [x] Add `hypothesis-synthesis` skill with 7-step collision process and 5 signal categories
- [ ] Improve conflict classification automation
- [ ] Add confidence scoring automation

## Decision Review

- [x] Add `hypothesis-decision-review` skill and workflow
- [x] Add `decision_review.md` artifact contract
- [x] Add worked example with full decision review in `examples/`

## System

- [x] Define minimal viable input format (`templates/input-schema.md`)
- [x] Standardize RUN_DIR structure (`architecture/run-structure.md`)

## Input / Prompt Validation

- [x] Add validation skill before Roles Layer
- [ ] Detect missing roles automatically in workflow
- [ ] Detect missing research context automatically

## Local Evidence Discovery — P0 #1

См. [roadmap/README.md](../roadmap/README.md#p0--поддержка-неструктурированной-базы-знаний). Релиз: **v2.3.0**.

- [x] Design-doc: `architecture/local-knowledge-retrieval.md`
- [x] Skill `local-knowledge-retrieval` — preview, guardrails, atomic evidence extraction
- [x] Workflow `/run-knowledge-retrieval.md`
- [x] Layer doc + manual template (`layers/local-evidence-discovery-layer.md`, `templates/knowledge-retrieval-prompt.md`)
- [x] Интеграция в `/run-hypothesis.md` (шаг 3) и Market Layer (inventory-first)
- [x] Артефакты: `discovery_preview.md`, `evidence_inventory.md`, `knowledge_retrieval_complete.marker`
- [x] Контракты: `10-artifact-contracts.md`, `20-evidence-rules.md`
- [x] Документация, playbooks, SVG diagrams
- [x] Пример mixed-source: `examples/example-001/kb-samples/` + discovery outputs
- [ ] Поддержка `.pdf` / `.docx` / `.html` (V2)
- [ ] E2E на реальном Obsidian vault в `runs/HYP-*`

---

## Conversational Run (chat-first) — P0 #2

См. [roadmap/README.md](../roadmap/README.md#p0--conversational-run-chat-first-запуск-из-чата). Релизы: **v2.2.0** (базовый flow), **v2.2.1** (dirty input + trigger-теги), **v2.2.2** (dialog RUN_DIR + isolation).

- [x] Skill `conversational-hypothesis-intake` — guided Q&A, draft preview, confirm/revise/cancel
- [x] Workflow `/run-hypothesis-conversational.md` — intake → dialog-confirmed `RUN_DIR` bootstrap → validate → pipeline
- [x] Auto ID assignment (`HYP-*`, `RUN-*`) и правила в `10-artifact-contracts.md`
- [x] Chat-first как recommended path в quick-start, README, playbooks (EN/RU)
- [x] Примеры `examples/chat-first-run.md` / `.ru.md`
- [x] Trigger-теги intake: `#гипотеза` / `#hypothesis`, `#контекст` / `#context`, `#роли` / `#roles`
- [x] Dirty input mode: извлечение из Q&A / CustDev + валидация mapping с пользователем
- [x] Статус до confirm RUN_DIR: `runs/ ещё НЕ создан`
- [x] Двойной confirm: draft гипотезы + предложенный `RUN_DIR` (Step 4a/4b)
- [x] New run isolation: без `RUN_DIR:` — новый archive; не reuse открытых табов
- [x] Trigger `#новая` / `#new-run`; continue-existing только с явным `RUN_DIR:`
- [x] Artifact allowlist в conversational flow (без несуществующих артефактов)
- [x] Пример C: вторая гипотеза в тот же день (`002` vs `001`)
- [ ] E2E-пример: реальный `runs/HYP-*` с артефактами после chat-first прогона (не только walkthrough-doc)
- [ ] Доп. input patterns: FR/требования, Jira/Linear paste, многоязычные заголовки в `input/hypothesis.md`
- [ ] Шаблоны быстрых тегов в onboarding (P1): подсказка тегов при первом запуске

---

## Documentation

- [x] Add Cline as primary implementation
- [x] Emphasize inventory-first local evidence, then Confluence MCP
- [x] Add product manager as primary user in README
- [ ] Add examples of role profiles

## Secondary MCP (future)

- [ ] Jira / Linear integration
- [ ] Slack integration
- [ ] Web search for external signals
