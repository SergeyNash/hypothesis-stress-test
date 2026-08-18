# Обзор архитектуры

Hypothesis Stress Test — **слоистый фреймворк рассуждений** с **адаптером имплементации на Cline**.

## Слои (ядро фреймворка)

Независимые слои анализа производят структурированные сигналы:

| Слой | Вопрос | Output |
|------|--------|--------|
| **Roles** (facilitator / stress test) | Как гипотеза ведёт себя с разных перспектив? | `role_outputs/*`, `hypothesis_summary.md`, `validation_questions.md` |
| **Local Evidence Discovery** | Какие локальные доказательства есть до интерпретации рынка? | `discovery_preview.md`, `evidence_inventory.md` |
| **Business Context** (ценность и стратегия) | Как гипотеза создаёт бизнес-ценность? | `business_context_analysis.md` или `missing_business_context.md` |
| **Market** (market reality check) | Существует ли проблема в реальности? | `market_analysis.md` |
| **Synthesis** (`hypothesis-synthesis`) | Что становится видно только при столкновении сигналов? | `hypothesis_map.md`, `hypothesis_digest.txt` |

Слои не смешивают сигналы преждевременно. Synthesis сталкивает уже существующие артефакты — не переанализирует их и не добавляет новые данные.

После Synthesis — **Customer Discovery Planning**, который переводит неопределённость в практичный CustDev-план интервью. Эта фаза не валидирует гипотезу и не принимает решения.

После Customer Discovery Planning — обязательный **Decision Review**: adversarial review выводов перед backlog. Новых сигналов не добавляет.

## Адаптер Cline

Фреймворк запускается в VS Code через [Cline](https://cline.bot/):

| Компонент | Расположение | Роль |
|-----------|--------------|------|
| Rules | `.clinerules/` | Постоянные инварианты |
| Skills | `.cline/skills/` | Выполнение слоёв по запросу |
| Workflows | `.clinerules/workflows/` | Оркестрация через slash-команды |
| MCP | Confluence (primary) | Получение local signals |

Полное соответствие: [implementations/cline-contract.md](../implementations/cline-contract.md)

## Поток данных

```text
input/hypothesis.md
  → Input Validation
  → Roles Layer (skill)
  → Local Evidence Discovery (skill)
  → discovery_preview.md + evidence_inventory.md
  → Business Context & Value Check (skill)
  → business_context_analysis.md or missing_business_context.md
  → Market Layer (skill + inventory + Confluence MCP)
  → Synthesis Layer (skill)
  → hypothesis_map.md + hypothesis_digest.txt
  → Customer Discovery Planning (skill)
  → customer_discovery_plan.md
  → Decision Review (skill)
  → decision_review.md
  → Решение человека (backlog)
```

## Контракт артефактов

Каждый прогон использует изолированный `RUN_DIR`. См. [run-structure.md](./run-structure.md) и `.clinerules/10-artifact-contracts.md`.

## Модель решений

Synthesis Layer классифицирует гипотезы по пяти паттернам:

- **Validated Opportunity** — внутренние и внешние сигналы совпадают
- **Internal Illusion** — внутренняя логика сильная, рынок слабый
- **Blind Spot** — рыночный сигнал есть, внутренняя модель его не видит
- **Weak Signal** — нет сильных доказательств
- **Local Optimization Trap** — боль подтверждена, стратегической ценности нет

Диаграмма: [signal model](../assets/signal-model.svg)

## Фреймворк vs имплементация

```text
Фреймворк  → слои, контракты, модель рассуждений (tool-agnostic)
Cline impl → rules, skills, workflows, Confluence MCP
```

Фреймворк можно запускать вручную через `templates/` без Cline.

## Карта документации

| Тема | Файл |
|------|------|
| Настройка Cline | [implementations/cline-setup.md](../implementations/cline-setup.md) |
| Confluence MCP | [implementations/confluence-mcp.md](../implementations/confluence-mcp.md) |
| Контракт Cline | [implementations/cline-contract.md](../implementations/cline-contract.md) |
| Playbook | [playbooks/run-hypothesis.md](../playbooks/run-hypothesis.md) |
| Chat-first прогон | [examples/chat-first-run.md](../examples/chat-first-run.md) |
| Пример | [examples/example-001/](../examples/example-001/) |
