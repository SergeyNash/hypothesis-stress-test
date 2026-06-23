Язык: [English](./implementations.md) | **Русский**

# Имплементации

Ядро фреймворка tool-agnostic. **Основная поддерживаемая имплементация** — **Cline в VS Code**.

---

## Фреймворк vs инструменты

```text
Фреймворк  = как думать (слои, контракты, модель решений)
Cline impl = как запускать (rules, skills, workflows, MCP)
```

Фреймворк определяет слои и контракты рассуждений. Cline обеспечивает выполнение, файловые артефакты и интеграцию с Confluence.

---

## Основная: Cline (VS Code)

### Компоненты

| Элемент | Расположение |
|---------|--------------|
| Rules | `.clinerules/` |
| Skills | `.cline/skills/` |
| Workflows | `.clinerules/workflows/` |
| Гайд по настройке | [implementations/cline-setup.ru.md](../implementations/cline-setup.ru.md) |
| Контракт | [implementations/cline-contract.ru.md](../implementations/cline-contract.ru.md) |

### Быстрый старт

1. Установить расширение Cline в VS Code
2. Открыть репозиторий
3. Настроить [Confluence MCP](../implementations/confluence-mcp.ru.md)
4. **Chat-first:** вызвать `/run-hypothesis-conversational.md` в чате Cline — см. [examples/chat-first-run.ru.md](../examples/chat-first-run.ru.md)
5. **File-first:** создать `RUN_DIR/input/hypothesis.md`, затем `/run-hypothesis.md`

Подробнее: [implementations/quick-start.ru.md](../implementations/quick-start.ru.md)

### Соответствие

```text
Template (templates/*.md)  → Cline skill (SKILL.md)
Шаг playbook             → Cline workflow (slash command)
RUN_DIR                    → локальная рабочая директория
Output слоя                → markdown-артефакт в outputs/
Страницы Confluence        → local signals в market_analysis.md
```

---

## Confluence MCP (для полноценного Market Layer)

Confluence — **основной MCP-источник** local signals.

- Поиск во внутренней wiki: discovery, прошлые решения, research
- Цитирование страниц в `market_analysis.md`
- Без MCP: фиксировать `missing local evidence`

См. [implementations/confluence-mcp.ru.md](../implementations/confluence-mcp.ru.md).

---

## Ручная имплементация

Скопируйте шаблоны из `templates/`, заполните гипотезу и контекст, запускайте в любом LLM-интерфейсе, сохраняйте артефакты вручную.

Подходит для: первых экспериментов, сред без Cline.

Шаги:

1. Скопировать шаблон слоя
2. Вставить гипотезу и контекст
3. Запустить в LLM
4. Сохранить output в `RUN_DIR/outputs/`
5. Перейти к следующему слою

---

## API-имплементация (будущее)

Программное выполнение через вызовы LLM API:

```text
hypothesis → roles call → market call → synthesis call → decision review call → artifacts
```

Для высокочастотного или CI-интегрированного анализа. Не входит в v1.

---

## Зрелость имплементации

| Уровень | Метод | Для кого |
|---------|-------|----------|
| 1 — Manual | Копирование templates | Индивидуальные эксперименты |
| 2 — Cline assisted | Rules + skills + workflows | Регулярное использование, малые команды |
| 3 — Automated | API pipeline | Высокая частота, платформы |

---

## Legacy: RooCode

Ранние версии ориентировались на RooCode. RooCode больше не поддерживается. Скриншоты в `assets/legacy/`. Используйте Cline как поддерживаемый IDE-адаптер.

---

## Ключевой принцип

Имплементация не должна менять модель рассуждений. Инструменты могут отличаться. Слои остаются теми же.
