<p align="right">
  <sub>
    🌐 <b>Язык:</b>
    <a href="./README.md">🇬🇧 English</a> ·
    <b>🇷🇺 Русский</b>
  </sub>
</p>

# 🧠 Hypothesis Stress Test

<p align="center">
  <b>Проверяйте продуктовые гипотезы до того, как начнёте их реализовывать.</b>
</p>

<p align="center">
  Слоистый фреймворк для продуктовых решений — запуск в VS Code через <a href="https://cline.bot/">Cline</a>, skills и Confluence MCP.
</p>

<p align="center">
  <a href="./implementations/quick-start.ru.md"><b>Быстрый старт</b></a>
  ·
  <a href="./implementations/README.ru.md"><b>Документация</b></a>
  ·
  <a href="./examples/example-001/"><b>Пример</b></a>
  ·
  <a href="./architecture/overview.ru.md"><b>Архитектура</b></a>
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

Фреймворк разделяет анализ на три слоя:

| Слой                | Задача                 | Результат                  |
| ------------------- | ---------------------- | -------------------------- |
| **Roles Layer**     | Внутренняя перспектива | ограничения и логика ролей |
| **Market Layer**    | Внешняя реальность     | сигналы и доказательства   |
| **Synthesis Layer** | Конфликт               | границы решения            |

Полный запуск в Cline: `/run-hypothesis.md` или по слоям через skills и workflows.

---

## Реализация на Cline

<p align="center">
  <img src="./assets/cline-workflow.svg" width="800"/>
</p>

| Компонент | Расположение | Назначение |
|-----------|--------------|------------|
| **Rules** | `.clinerules/` | Постоянные инварианты фреймворка |
| **Skills** | `.cline/skills/` | Выполнение слоёв по запросу |
| **Workflows** | `.clinerules/workflows/` | Slash-команды (`/run-hypothesis.md`) |
| **Confluence MCP** | MCP config | Основной источник local signals |

Настройка: [implementations/cline-setup.ru.md](./implementations/cline-setup.ru.md)

Confluence MCP: [implementations/confluence-mcp.ru.md](./implementations/confluence-mcp.ru.md)

---

## Модель принятия решений

<p align="center">
  <img src="./assets/signal-model.svg" width="660"/>
</p>

Система классифицирует гипотезу:

* **Validated Opportunity** — внутренние и внешние сигналы совпадают
* **Internal Illusion** — внутри всё выглядит логично, но рынок не подтверждает
* **Blind Spot** — рынок показывает возможность, но внутри её не видят
* **Weak Signal** — слабые сигналы со всех сторон

---

## Поток артефактов

<p align="center">
  <img src="./assets/artifact-flow.svg" width="820"/>
</p>

Каждый запуск создаёт трассируемую цепочку:

```text
RUN_DIR/
  hypothesis.md
  outputs/
    role_outputs/*
    hypothesis_summary.md
    market_analysis.md
    hypothesis_map.md
    hypothesis_digest.txt
```

---

## Быстрый старт (Cline)

Полный гайд: **[implementations/quick-start.ru.md](./implementations/quick-start.ru.md)**

Кратко:

1. Установите [Cline](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev) в VS Code
2. Откройте **свою базу знаний** и добавьте папку `hypothesis-stress-test/` (clone или submodule)
3. Symlink `.clinerules/` и `.cline/` в корень KB — см. quick start
4. Настройте [Confluence MCP](./implementations/confluence-mcp.ru.md)
5. Создайте `runs/my-hypothesis/hypothesis.md`
6. В чате Cline: `RUN_DIR: runs/my-hypothesis` + `/run-hypothesis.md`

Вся операционная документация на русском: [implementations/README.ru.md](./implementations/README.ru.md)

Ручной режим: [playbooks/run-hypothesis.ru.md](./playbooks/run-hypothesis.ru.md)

---

## Пример

```text
examples/example-001/
```

B2B-гипотеза в AppSec: переформулировка из «снизить риски в проде» в «повысить операционную эффективность».

---

## Фреймворк vs Инструменты

```text
Фреймворк  → как думать (слои, контракты, модель решений)
Cline      → как запускать (rules, skills, workflows, MCP)
```

Фреймворк не привязан к инструменту. Cline — основная поддерживаемая реализация.

---

## Структура репозитория

```text
.clinerules/       правила и workflows Cline
.cline/skills/     skills по слоям
layers/            логика анализа
templates/         шаблоны для ручного режима
playbooks/         сценарии
examples/          примеры
architecture/      устройство системы
implementations/   настройка Cline, Confluence MCP
assets/            диаграммы
```

---

## Принципы

* разделяй внутренние и внешние сигналы
* Confluence первым для local evidence
* нет данных → нет утверждения
* противоречия важнее согласия
* решение принимает человек
* плохие идеи должны умирать рано

---

<p align="center">
  <b>Проверьте идею до того, как начнёте её делать.</b>
</p>
