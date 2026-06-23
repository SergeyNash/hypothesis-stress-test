<p align="right">
  <sub>
    🌐 <b>Язык:</b>
    <a href="./README.md">🇬🇧 English</a> ·
    <b>🇷🇺 Русский</b> ·
    <a href="./implementations/quick-start.ru.md">Быстрый старт</a>
  </sub>
</p>

# 🧠 Hypothesis Stress Test

<p align="center">
  <sub>Версия фреймворка <b>2.0.0</b> · <a href="./CHANGELOG.ru.md">Changelog</a></sub>
</p>

<p align="center">
  <b>Проверяйте продуктовые гипотезы до того, как начнёте их реализовывать.</b>
</p>

<p align="center">
  Слоистый фреймворк для продуктовых решений — запуск в VS Code через <a href="https://cline.bot/">Cline</a>, skills и Confluence MCP.
</p>

<p align="center">
  <a href="./implementations/quick-start.ru.md"><b>Быстрый старт</b></a>
  ·
  <a href="./playbooks/run-hypothesis.ru.md"><b>Playbook</b></a>
  ·
  <a href="./implementations/README.ru.md"><b>Документация</b></a>
  ·
  <a href="./examples/example-001/"><b>Пример</b></a>
  ·
  <a href="./architecture/overview.ru.md"><b>Архитектура</b></a>
  ·
  <a href="./roadmap/README.md"><b>Roadmap</b></a>
  ·
  <a href="./CHANGELOG.ru.md"><b>Changelog</b></a>
</p>

<p align="center">
  <img src="./assets/architecture-overview.svg" width="760"/>
</p>

<p align="center">
  <a href="./assets/architecture-overview.svg">Открыть диаграмму</a>
</p>

---

## Зачем это нужно

Большинство продуктовых команд терпят неудачу не из-за отсутствия идей.

А потому что они:

* проверяют гипотезы слишком поздно
* полагаются на интуицию
* смешивают предположения с реальностью
* избегают противоречий

Этот фреймворк помогает ответить на один вопрос:

> **Стоит ли вообще реализовывать эту идею?**

---

## Ключевая идея

Не используйте LLM для генерации ещё большего количества идей.

Используйте его, чтобы **нагружать и проверять** уже существующие.

```text
идея → стресс-тест → решение
```

---

## Как это работает

Три слоя анализа, Customer Discovery Planning, обязательный Decision Review и финальное решение человека:

| Фаза | Skill | Результат |
|------|-------|-----------|
| **Validate** | `hypothesis-input-validation` | готовый `input/hypothesis.md` |
| **Facilitator** (Roles / stress test) | `hypothesis-facilitator` | `role_outputs/*`, `hypothesis_summary.md`, `validation_questions.md` |
| **Market** (market reality check) | `hypothesis-market-layer` | `market_analysis.md` |
| **Synthesis** (столкновение сигналов) | `hypothesis-synthesis` | `hypothesis_map.md`, `hypothesis_digest.txt` |
| **Customer Discovery Planning** | `customer-discovery-planning` | `customer_discovery_plan.md` |
| **Decision Review** | `hypothesis-decision-review` | `decision_review.md` |
| **Backlog Decision** (человек) | — | proceed / validate / research / reject |

Полный прогон: `/run-hypothesis.md`

По фазам:

```text
/validate-hypothesis-input.md
/run-facilitator.md
/run-market-layer.md
/run-synthesis.md
/run-customer-discovery-planning.md
/run-decision-review.md
```

Указывайте `RUN_DIR` в сообщении Cline, например: `RUN_DIR: runs/HYP-2026-06-22-001`

---

## Реализация на Cline

<p align="center">
  <img src="./assets/cline-workflow.svg" width="800"/>
</p>

| Компонент | Расположение | Назначение |
|-----------|--------------|------------|
| **Rules** | `.clinerules/` | Постоянные инварианты фреймворка |
| **Skills** | `.cline/skills/` | Выполнение фаз по запросу |
| **Workflows** | `.clinerules/workflows/` | Slash-команды |
| **Confluence MCP** | MCP config | Основной источник local signals |

Настройка: [implementations/cline-setup.ru.md](./implementations/cline-setup.ru.md)

Confluence MCP: [implementations/confluence-mcp.ru.md](./implementations/confluence-mcp.ru.md)

Контракт: [implementations/cline-contract.ru.md](./implementations/cline-contract.ru.md)

---

## Модель принятия решений

<p align="center">
  <img src="./assets/signal-model.svg" width="660"/>
</p>

Synthesis (`hypothesis-synthesis`) классифицирует столкновение сигналов:

* **Validated Opportunity** — внутренние и внешние сигналы совпадают
* **Internal Illusion** — внутри всё выглядит логично, но рынок не подтверждает
* **Blind Spot** — рынок показывает возможность, но внутри её не видят
* **Weak Signal** — слабые сигналы со всех сторон
* **Local Optimization Trap** — боль подтверждена, но стратегической ценности нет

---

## Поток артефактов

<p align="center">
  <img src="./assets/artifact-flow.svg" width="820"/>
</p>

Каждый запуск создаёт трассируемую цепочку:

```text
RUN_DIR/
  input/
    hypothesis.md
    attachments/
  run.md
  outputs/
    role_outputs/*
    hypothesis_summary.md
    validation_questions.md
    market_analysis.md
    hypothesis_map.md
    hypothesis_digest.txt
    customer_discovery_plan.md
    decision_review.md
    *.marker
```

Язык артефактов совпадает с языком `input/hypothesis.md`.

---

## Быстрый старт (Cline)

Полный гайд: **[implementations/quick-start.ru.md](./implementations/quick-start.ru.md)**

Кратко:

1. Установите [Cline](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev) в VS Code
2. Откройте **свою базу знаний** и добавьте папку `hypothesis-stress-test/` (clone или submodule)
3. Symlink `.clinerules/` и `.cline/` в корень KB — см. [quick start](./implementations/quick-start.ru.md)
4. Настройте [Confluence MCP](./implementations/confluence-mcp.ru.md)
5. Создайте `runs/HYP-YYYY-MM-DD-NNN/input/hypothesis.md` — см. [templates/input-schema.md](./templates/input-schema.md)
6. В чате Cline: `RUN_DIR: runs/HYP-YYYY-MM-DD-NNN` + `/run-hypothesis.md`

Операционная документация: [implementations/README.ru.md](./implementations/README.ru.md)

Ручной режим: [playbooks/run-hypothesis.ru.md](./playbooks/run-hypothesis.ru.md)

---

## Пример

```text
examples/example-001/
```

B2B-гипотеза в AppSec: synthesis переформулирует гипотезу из «снизить риски в проде» в «повысить операционную эффективность»; `decision_review.md` рекомендует **Proceed with Validation**.

---

## Фреймворк vs Инструменты

```text
Фреймворк  → как думать (слои, контракты, модель решений)
Cline      → как запускать (rules, skills, workflows, MCP)
```

Фреймворк не привязан к инструменту. Cline — основная поддерживаемая реализация. Возможны ручной режим и API (см. [architecture/implementations.ru.md](./architecture/implementations.ru.md)).

---

## Структура репозитория

```text
.clinerules/       правила и workflows Cline
.cline/skills/     skills по фазам
layers/            логика анализа
templates/         шаблоны для ручного режима
playbooks/         сценарии
examples/          примеры
runs/              прогоны гипотез (в KB workspace)
knowledge-base/    гайд по Confluence / local signals
architecture/      устройство системы
implementations/   настройка Cline, Confluence MCP
roadmap/           дорожная карта (RU)
assets/            диаграммы
CHANGELOG.ru.md    история версий фреймворка
VERSION            текущая версия фреймворка
```

---

## Принципы

* разделяй внутренние и внешние сигналы
* сначала local evidence inventory, затем Confluence как внутренний wiki-канал
* нет данных → нет утверждения
* противоречия важнее согласия
* оспаривай выводы перед backlog
* решение принимает человек
* плохие идеи должны умирать рано

---

## Чем это не является

* генератором идей
* заменой реальным пользователям и интервью
* substitute для полноценного market research
* автономным decision-maker

---

<p align="center">
  <b>Проверьте идею до того, как начнёте её делать.</b>
</p>
