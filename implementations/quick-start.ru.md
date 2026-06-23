Язык: [English](./quick-start.md) | **Русский**

# Быстрый старт

Короткий путь: от установки Cline до первого прогона гипотезы за 10–15 минут.

Полная документация: [README.ru.md](./README.ru.md)

---

## Что понадобится

- VS Code
- [Cline](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev)
- API-ключ LLM-провайдера (или локальная модель)
- Confluence MCP (рекомендуется) — [confluence-mcp.ru.md](./confluence-mcp.ru.md)

---

## Шаг 1. Установить Cline

1. Откройте VS Code → Extensions → найдите **Cline** → Install.
2. В настройках Cline укажите провайдера LLM и API-ключ.

---

## Шаг 2. Открыть проект

**Рекомендуется:** откройте **свою базу знаний** как главный проект и добавьте в неё папку `hypothesis-stress-test/` с полным репозиторием фреймворка. Подробности — в разделе [База знаний и workspace](#база-знаний-и-workspace).

**Альтернатива:** откройте только репозиторий фреймворка:

```text
git clone <repo-url>
code hypothesis-stress-test
```

Cline автоматически подхватит из **корня workspace**:

- Rules из `.clinerules/` (включая `workflows/` — slash-команды)
- Skills из `.cline/skills/`

Проверьте в панели Cline: иконка Rules (весы) — правила фреймворка должны быть включены.

---

## База знаний и workspace

База знаний и обвязка фреймворка — **разные вещи**. Открывать оба проекта одновременно **не обязательно**.

| Что | Откуда | Зависит от открытого проекта? |
| ----- | -------- | ------------------------------- |
| Обвязка (rules, skills, workflows) | `.clinerules/`, `.cline/skills/` | **Да** — только из корня открытого workspace |
| Confluence (wiki) | Confluence MCP в Cline | **Нет** — настраивается один раз, работает из любого workspace |
| Локальные файлы KB | Markdown и заметки в репозитории | **Да** — Cline читает файлы открытого проекта |
| Артефакты прогона | `RUN_DIR/outputs/` | Любая папка **внутри** открытого workspace |

Папка `knowledge-base/` в этом репозитории — **документация** о поиске в Confluence, а не ваша личная база знаний.

### Вариант A (рекомендуется): KB — главный проект + папка `hypothesis-stress-test/`

У вас уже есть открытый проект — **ваша база знаний**. Добавьте в него папку с полным репозиторием фреймворка:

```text
my-knowledge-base/                    ← открыт в VS Code
  discovery/                          ← ваша KB: заметки, интервью, research
  knowledge-base/
    interviews/                        ← сырые CustDev-заметки и саммари интервью
    persona-builds/                    ← логи пересборки персон из evidence
    personas/                          ← переиспользуемые профили ролей
  research/
  adr/
  runs/                               ← RUN_DIR для гипотез (рядом с KB)
    HYP-2026-06-22-001/
      input/
        hypothesis.md
      outputs/
  hypothesis-stress-test/               ← весь репозиторий фреймворка
    .clinerules/                      ← rules + workflows (/run-hypothesis.md)
    .cline/skills/                    ← skills по слоям
    templates/                        ← шаблоны для ручного режима
    playbooks/
    examples/
    implementations/                  ← документация (quick start, MCP, setup)
    ...
```

Добавить папку:

```bash
cd my-knowledge-base
git submodule add https://github.com/SergeyNash/hypothesis-stress-test.git hypothesis-stress-test
# или: git clone <repo-url> hypothesis-stress-test
```

**Важно про Cline:** rules и skills ищутся в **корне workspace**, а не внутри вложенной папки. После добавления `hypothesis-stress-test/` сделайте одно из двух:

**A1 — symlink в корне KB (удобно для submodule):**

```bash
# Windows (cmd as admin) или mklink в PowerShell
mklink /D .clinerules hypothesis-stress-test\.clinerules
mklink /D .cline hypothesis-stress-test\.cline
```

**A2 — скопировать dot-папки в корень KB** (если symlink не подходит):

```bash
cp -r hypothesis-stress-test/.clinerules .
cp -r hypothesis-stress-test/.cline .
```

Плюсы: одно окно; KB и фреймворк рядом; `runs/` живёт в вашем проекте; документация всегда под рукой в `hypothesis-stress-test/implementations/`.

### Вариант B: multi-root workspace

Два репозитория рядом, одно окно VS Code. Файл `my-work.code-workspace`:

```json
{
  "folders": [
    { "path": "my-knowledge-base", "name": "KB" },
    { "path": "hypothesis-stress-test", "name": "Framework" }
  ]
}
```

Cline подхватит rules/skills из корня `hypothesis-stress-test`. `RUN_DIR` — в KB: `runs/HYP-2026-06-22-001/`. Контекст — через `@discovery/...`.

### Вариант C: только hypothesis-stress-test

Открываете репозиторий фреймворка как workspace. Подходит, если KB в основном в **Confluence**, а не в локальных файлах.

### Как подключить источники знаний

**Confluence (основной путь):**

1. Настройте Confluence MCP — [confluence-mcp.ru.md](./confluence-mcp.ru.md).
2. Запустите Local Evidence Discovery (`/run-knowledge-retrieval.md`) для inventory локальных файлов.
3. Market Layer читает inventory и затем ищет сигналы в Confluence.
4. Результаты пишутся в `market_analysis.md` с раздельными каналами: KB / Confluence / External / Inferred.

**Локальные файлы:**

- Откройте репозиторий, где лежат заметки (вариант A или B).
- Cline читает их на шаге Local Evidence Discovery.
- File-based findings сначала попадают в `outputs/evidence_inventory.md`, затем интерпретируются в Market Layer.

**Personas и интервью:**

- Сырые CustDev-материалы храните в `knowledge-base/interviews/`.
- Текущие переиспользуемые профили ролей храните в `knowledge-base/personas/`.
- Логи пересборки персон храните в `knowledge-base/persona-builds/`.
- Roles Layer может использовать совпадающие personas как supporting context.
- Persona без связанных `source_interviews` — слабый локальный сигнал, а не первичное evidence.

Без Confluence и без локальных файлов retrieval + market зафиксируют gap по local evidence.

---

## Шаг 3. Настроить Confluence MCP

Market Layer сначала использует `evidence_inventory.md`, затем Confluence MCP.

Минимальная настройка — см. [confluence-mcp.ru.md](./confluence-mcp.ru.md).

Без Confluence Market Layer пометит `missing local evidence` — прогон возможен, но без внутренних данных.

---

## Шаг 4. Создать RUN_DIR

```text
runs/HYP-2026-06-22-001/
  input/
    hypothesis.md
    attachments/
```

Минимальный пример `input/hypothesis.md`:

```markdown
# Hypothesis

## Metadata

- Hypothesis ID: HYP-2026-06-22-001
- Created at: 2026-06-22
- Run ID: RUN-2026-06-22-001
- Status: draft

## Statement

Если [действие], то [ожидаемый результат для конкретной аудитории].

## Relevant Roles

* Роль 1
* Роль 2

## Research Context

* Domain: [домен]
* Target audience: [аудитория]
* Scenario: [сценарий]
```

Полная схема: `hypothesis-stress-test/templates/input-schema.md` (или [templates/input-schema.md](../templates/input-schema.md) если workspace = фреймворк).

Пример: `hypothesis-stress-test/examples/example-001/input/hypothesis.md`

Если в `knowledge-base/personas/` есть совпадающие профили ролей, Roles Layer может использовать их как supporting context. Список ролей в `input/hypothesis.md` всё равно задаёт scope конкретного прогона.

---

## Шаг 5. Запустить прогон

В чате Cline:

```text
RUN_DIR: runs/HYP-2026-06-22-001
/run-hypothesis.md
```

Cline выполнит:

1. Валидацию входа
2. Facilitator (Roles Layer)
3. Local Evidence Discovery (preview + inventory)
4. Market Layer (inventory + поиск в Confluence)
5. Synthesis Layer
6. Customer Discovery Planning
7. Decision Review

Подтверждайте запись файлов и вызовы MCP по запросу.

---

## Шаг 6. Прочитать результат

Сначала откройте:

```text
runs/HYP-2026-06-22-001/outputs/hypothesis_digest.txt
```

Полный анализ:

```text
outputs/
  role_outputs/*
  hypothesis_summary.md
  validation_questions.md
  discovery_preview.md
  evidence_inventory.md
  market_analysis.md
  hypothesis_map.md
  hypothesis_digest.txt
  customer_discovery_plan.md
  decision_review.md
```

| Артефакт | Что внутри |
| ---------- | ------------ |
| `hypothesis_digest.txt` | Краткий digest (макс. 150 слов): жизнеспособность, конфликт, иллюзия, слепая зона, следующий шаг |
| `hypothesis_map.md` | Столкновение сигналов: дивергенции, слепые зоны, новая информация, границы, влияние на гипотезу |
| `customer_discovery_plan.md` | Практичный CustDev-план: неизвестные, приоритеты, роли, гайд интервью |
| `decision_review.md` | Adversarial review: уверенность, риски, план валидации |
| `market_analysis.md` | Раздельные каналы KB + Confluence + external + inferred с источниками |

---

## Если что-то пошло не так

| Проблема | Решение |
| ---------- | --------- |
| Rules не видны | Проверьте `.clinerules/` в **корне** workspace (symlink из `hypothesis-stress-test/`); перезагрузите VS Code |
| Workflow не запускается | Укажите `RUN_DIR:` явно в сообщении |
| Confluence MCP не работает | [confluence-mcp.ru.md](./confluence-mcp.ru.md) |
| Нет outputs | Проверьте, какой слой не завершился (marker-файлы в `outputs/`) |

---

## Куда идти дальше

- [cline-setup.ru.md](./cline-setup.ru.md) — полная настройка Cline
- [playbooks/run-hypothesis.ru.md](../playbooks/run-hypothesis.ru.md) — детальный сценарий прогона
- [examples/example-001/](../examples/example-001/) — эталонный пример с артефактами
