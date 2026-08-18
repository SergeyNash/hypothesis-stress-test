# Слой Business Context & Value Check

Слой отвечает на вопрос:

> Если гипотеза верна, как она создаёт ценность для бизнеса?

Отделяет **проблема существует** от **бизнес-кейс правдоподобен**.

---

## Чего слой не делает

- Не проводит market research
- Не синтезирует role- и market-сигналы
- Не принимает финальные продуктовые решения
- Не оценивает выручку без evidence

---

## Назначение

Большинство B2B-гипотез проваливается не потому, что боль фейковая, а потому что:

- покупатель — не пользователь
- ценность не связана со стратегией
- механизм от боли к бизнес-эффекту неясен

Слой строит **карту потока ценности** до внешней валидации.

<p align="center">
  <img src="../assets/ru/business-value-flow.png" width="760"/>
</p>

---

## Входы

Обязательно:

- `input/hypothesis.md`
- outputs Roles Layer (`role_outputs/*`, `hypothesis_summary.md`)

Опционально:

- `evidence_inventory.md`
- стратегические материалы KB (`strategy/`, `okr/`, `business-model/`)

## Условия старта

- `ready_for_synthesis.marker`

---

## Типы бизнес-эффекта

| Тип | Вопрос |
|------|----------|
| **Revenue Driver** | Помогает ли выигрывать или расширять выручку? |
| **Retention Driver** | Защищает или растит существующих клиентов? |
| **Competitive Driver** | Дифференцирует ли относительно названных конкурентов? |
| **Adoption Driver** | Увеличивает ли использование или число мест? |
| **Operational Driver** | Улучшает ли внутреннюю эффективность? |

---

## Outputs

| Артефакт | Назначение |
|----------|------------|
| `business_context_analysis.md` | Полная карта ценности и strategic fit |
| `missing_business_context.md` | Явный gap, если стратегической KB нет |
| `business_context_complete.marker` | Gate для Market Layer |

---

## Место в пайплайне

```text
Roles Layer
  ↓
Local Evidence Discovery
  ↓
Business Context & Value Check   ← этот слой
  ↓
Market Layer
  ↓
Synthesis
```

Synthesis и Decision Review используют business context, чтобы ловить **Local Optimization Trap** и readiness **Needs business context**.

---

## Правила ревью

- Нет данных по стратегии → `missing_business_context.md`, а не выдуманный анализ
- Боль пользователя ≠ ценность для покупателя
- Strategic fit должен ссылаться на источники

---

## Дальше

- `templates/business-context-prompt.md` — ручной запуск
- `.cline/skills/business-context-value-check/SKILL.md` — запуск через Cline
