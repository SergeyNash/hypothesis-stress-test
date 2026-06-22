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

[2.0.0]: https://github.com/SergeyNash/hypothesis-stress-test/compare/v1.3.0...v2.0.0
[1.3.0]: https://github.com/SergeyNash/hypothesis-stress-test/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/SergeyNash/hypothesis-stress-test/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/SergeyNash/hypothesis-stress-test/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/SergeyNash/hypothesis-stress-test/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/SergeyNash/hypothesis-stress-test/releases/tag/v0.1.0
