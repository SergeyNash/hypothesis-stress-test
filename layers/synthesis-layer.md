# Synthesis Layer

Synthesis Layer — слой **столкновения сигналов**.

Сравнивает внутренние (roles), локальные evidence, Business Context и внешние (market) сигналы и показывает то, что видно только после сравнения.

---

## Чего слой не делает

- Не пересказывает role- или market-outputs без сравнения
- Не проводит market research
- Не выполняет новый retrieval и не добавляет evidence
- Не переанализирует роли
- Не принимает финальные продуктовые решения

---

## Назначение

Цель — не суммировать предыдущий анализ.

Цель — обнаружить:

> Что видно только когда внутренняя логика встречается с внешней реальностью?

Истина проявляется из противоречий, а не из согласия.

---

## Входы

Обязательно:

- `hypothesis_summary.md`
- `market_analysis.md`
- `role_outputs/*`
- `evidence_inventory.md`
- `business_context_analysis.md` или `missing_business_context.md`

Опционально:

- `validation_questions.md`

## Условия старта

- `ready_for_synthesis.marker`
- `knowledge_retrieval_complete.marker`
- `business_context_complete.marker` со статусом `completed` или `skipped_missing_context`
- `market_analysis_complete.marker`

---

## Модель сигналов

| Категория | Паттерн | Риск |
|----------|---------|------|
| **Validated Opportunity** | Roles YES + Market YES | Сильный сигнал |
| **Internal Illusion** | Roles YES + Market NO | Локальная проблема может не существовать системно |
| **Blind Spot** | Roles NO + Market YES | Организация пропускает возможность |
| **Weak Signal** | Слабо везде | Решение на допущениях |
| **Local Optimization Trap** | Боль подтверждена, стратегической ценности нет | Эффективность без стратегического эффекта |

---

## Процесс анализа

1. Внутреннее выравнивание (согласие / напряжение / зоны конфликта)
2. Проверка Business Context: stakeholder/value flow, strategic fit или явный gap
3. Рыночная валидация (подтверждено / слабо / не подтверждено)
4. Кросс-анализ сигналов с приоритетом валидации
5. Границы применимости
6. Слепые зоны
7. Новая информация (обязательно — только после сравнения)
8. Влияние на исходную гипотезу

---

## Outputs

| Артефакт | Назначение |
|----------|------------|
| `hypothesis_map.md` | Полный collision-анализ |
| `hypothesis_digest.txt` | Короткий digest (макс. 150 слов) |
| `synthesis_complete.marker` | Готово к Customer Discovery Planning |

### Секции `hypothesis_map.md`

- Единое резюме
- Подтверждённые сигналы, internal illusions, упущенные возможности
- Local optimization traps, ключевые расхождения, слепые зоны
- Новая информация (только после сравнения)
- Границы применимости
- Влияние на исходную гипотезу
- Приоритеты валидации

Язык output совпадает с `input/hypothesis.md`.

---

## Правила ревью

- Не сглаживать противоречия
- Не ставить консенсус выше фактов
- Не выдумывать сигналы
- Не проводить новый retrieval/research; использовать только существующие артефакты и их citations
- Не трактовать отсутствующий Business Context как подтверждение strategic fit
- Не пересказывать без сравнения
- Всегда искать возможность reframe

---

## Связь с другими слоями

- Facilitator (Roles) → внутренние сигналы
- Local Evidence → атомарные локальные сигналы
- Business Context → stakeholder/value flow, strategic fit или явный gap
- Market Layer → внешние сигналы
- **Synthesis** → столкновение сигналов
- Customer Discovery Planning → план интервью
- Decision Review → adversarial критика выводов synthesis

---

## Дальше

- `customer-discovery-planning-layer.md`
- `templates/synthesis-prompt.md` — ручной запуск
- `.cline/skills/hypothesis-synthesis/SKILL.md` — запуск через Cline
