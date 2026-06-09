Язык: [English](./overview.md) | **Русский**

# Обзор архитектуры

Hypothesis Stress Test — **слоистый фреймворк рассуждений** с **адаптером имплементации на Cline**.

## Слои (ядро фреймворка)

Три независимых слоя анализа производят структурированные сигналы:

| Слой | Вопрос | Output |
|------|--------|--------|
| **Roles** | Как гипотеза ведёт себя с разных перспектив? | `role_outputs/*`, `hypothesis_summary.md` |
| **Market** | Существует ли проблема в реальности? | `market_analysis.md` |
| **Synthesis** | Что выживает при столкновении сигналов? | `hypothesis_map.md`, `hypothesis_digest.txt` |

Слои не смешивают сигналы преждевременно. Synthesis сравнивает только артефакты предыдущих слоёв.

После Synthesis — обязательный **Decision Review**: adversarial review выводов перед backlog. Новых сигналов не добавляет.

## Адаптер Cline

Фреймворк запускается в VS Code через [Cline](https://cline.bot/):

| Компонент | Расположение | Роль |
|-----------|--------------|------|
| Rules | `.clinerules/` | Постоянные инварианты |
| Skills | `.cline/skills/` | Выполнение слоёв по запросу |
| Workflows | `.clinerules/workflows/` | Оркестрация через slash-команды |
| MCP | Confluence (primary) | Получение local signals |

Полное соответствие: [implementations/cline-contract.ru.md](../implementations/cline-contract.ru.md)

## Поток данных

```text
hypothesis.md
  → Input Validation
  → Roles Layer (skill)
  → Market Layer (skill + Confluence MCP)
  → Synthesis Layer (skill)
  → hypothesis_map.md + hypothesis_digest.txt
  → Decision Review (skill)
  → decision_review.md
  → Решение человека (backlog)
```

## Контракт артефактов

Каждый прогон использует изолированный `RUN_DIR`. См. [run-structure.ru.md](./run-structure.ru.md) и `.clinerules/10-artifact-contracts.md`.

## Модель решений

Synthesis Layer классифицирует гипотезы по четырём паттернам:

- **Validated Opportunity** — внутренние и внешние сигналы совпадают
- **Internal Illusion** — внутренняя логика сильная, рынок слабый
- **Blind Spot** — рыночный сигнал есть, внутренняя модель его не видит
- **Weak Signal** — нет сильных доказательств

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
| Настройка Cline | [implementations/cline-setup.ru.md](../implementations/cline-setup.ru.md) |
| Confluence MCP | [implementations/confluence-mcp.ru.md](../implementations/confluence-mcp.ru.md) |
| Контракт Cline | [implementations/cline-contract.ru.md](../implementations/cline-contract.ru.md) |
| Playbook | [playbooks/run-hypothesis.ru.md](../playbooks/run-hypothesis.ru.md) |
| Пример | [examples/example-001/](../examples/example-001/) |
