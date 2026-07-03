# Анализ бизнес-контекста

## Доступный контекст

- `kb-samples/strategy/product-strategy-2025.md` — продуктовая стратегия, GTM, OKR, определение покупателя
- Выходы Roles Layer и evidence inventory (EVID-001 — EVID-004)

## Недостающий контекст

- Формальная unit economics и влияние на pricing
- Win/loss data по приоритизации очереди в конкурентных сделках
- Критерии закупки CISO в недавних enterprise deals

## Карта заинтересованных сторон

| Роль | Связь | Заметки |
|------|-------|---------|
| AppSec Engineer | Испытывает боль, ежедневный пользователь | Хочет ручной контроль очереди |
| Enterprise Developer | Косвенный стейкхолдер | Задержки сканов и переприоритизация |
| CISO | Экономический покупатель, decision maker | Policy consistency и auditability |
| Platform / DevOps | Внедренец | Ограничения CI/CD |
| Finance / Procurement | Budget gate (не в гипотезе) | Нужны ROI-доказательства на scale |

## Поток создания ценности

```text
Перегрузка очереди сканов (проблема)
  ↓ AppSec приоритизирует критичные приложения (beneficiary / изменение поведения)
  ↓ Быстрее time-to-action по критичным findings (операционный outcome)
  ↓ ??? → Снижение production risk (заявленный бизнес-эффект — слабо подтверждён)
```

**Gap:** исходная гипотеза перескакивает от операционного поведения к production risk reduction без документированного buyer-visible эффекта.

## Тип бизнес-эффекта

- **Operational Driver** — сильный (боль в очереди, workflow efficiency) — роли + local evidence
- **Adoption Driver** — средний (удовлетворённость AppSec, использование инструмента)
- **Competitive Driver** — слабый (стратегия называет workflow differentiation, но queue prioritization не ключевая win-тема)
- **Revenue Driver** — неизвестно (нет evidence, что покупают ради приоритизации очереди)

Первичная классификация: **Operational Driver**, не доказанные **Revenue Driver** или risk-reduction outcome.

## Связь со стратегией

**Medium-Low** для текущего framing («снизить production risk»).

**Medium** при reframe на enterprise workflow efficiency с governance и audit trail — соответствует приоритету #1 (win enterprise AppSec workflows) и OKR по time-to-value.

Стратегия предупреждает: фичи, помогающие только операторам без CISO-visible value — риск upsell, не core driver.

Источники: `product-strategy-2025.md` — GTM, OKR, buyer definition.

## Ключевые риски

- **Buyer vs user gap:** AppSec хочет контроль; CISO — централизованную policy
- **Стратегическое несоответствие:** risk-reduction narrative не в H1 OKR; ближе workflow efficiency
- **Локальная оптимизация:** фича для оператора без движения buyer metrics
- **Standalone feature risk:** стратегия — не позиционироваться как узкая scanner utility

## Ключевые возможности

- Reframe как **governed workflow automation** (policy + manual exceptions)
- Audit trail для решений о приоритизации — связь operator pain с CISO buyer value
- Пилот в mature accounts (10–50 проектов) с метрикой time-to-action — OKR time-to-value

## Резюме для downstream-слоёв

Существование проблемы правдоподобно на операционном уровне. Business case для «снизить production risk» **не доказан**. Strategic fit улучшается при reframe на **workflow efficiency + governance** с buyer-visible outcomes. Ожидать Local Optimization Trap, если строить operator-only queue tool без CISO value chain.
