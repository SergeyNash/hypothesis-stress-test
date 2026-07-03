# Анализ бизнес-контекста

## Доступный контекст

- `kb-samples/strategy/product-strategy-2026.md` — CHRO-led GTM, compliance-first AI positioning
- Role outputs и EVID-001 — EVID-004

## Недостающий контекст

- Win/loss data по AI screening features
- Влияние legal review cycle на revenue
- Baseline time-to-hire в target segment

## Карта заинтересованных сторон

| Роль | Связь |
|------|-------|
| Recruiter | Испытывает боль, daily user |
| Hiring Manager | Потребляет output, влияет на adoption |
| CHRO / Head of Talent | Экономический покупатель, compliance owner |
| Legal / DEI | Blocker или approver в enterprise |

## Поток создания ценности

```text
Перегрузка откликов (проблема)
  ↓ ИИ ранжирует / assist triage (изменение поведения)
  ↓ Рекрутер быстрее отдаёт shortlist (user outcome)
  ↓ −30% time-to-hire (заявленный эффект — не доказан)
  ↓ ??? → CHRO покупает compliance-ready efficiency (другой механизм)
```

## Тип бизнес-эффекта

- **Operational Driver** — сильный для recruiter workflow (EVID-001, EVID-002)
- **Adoption Driver** — средний при росте engagement ATS
- **Revenue Driver** — средний через AI module upsell **только если** compliance packaging удовлетворяет CHRO (EVID-003)
- **Competitive Driver** — сильное соответствие стратегии vs Greenhouse/Lever на governed AI

Первичный: **Operational Driver** для users; **Revenue Driver** для бизнеса — через compliance-ready positioning.

## Связь со стратегией

**Low** для гипотезы как заявлено («−30% time-to-hire через ИИ-ранжирование»).

**High** для reframe **governed recruiter assist с audit trail** — приоритеты #2, #3 и H1 OKR.

Источники: `product-strategy-2026.md`.

## Ключевые риски

- Marketing speed без compliance → legal blocks enterprise rollout
- User vs buyer value gap
- Black-box ranking повторяет failed pilot (EVID-004)

## Ключевые возможности

- Reframe explainable assist + audit log → AI module upsell
- Метрика recruiter hours saved, не time-to-hire — OKR alignment

## Резюме для downstream-слоёв

Screening pain validated. Business case для «−30% faster hiring» **не доказан** и **misaligned с покупателем**. Strategic fit high только после reframe. Ожидать Internal Illusion на speed metrics и Local Optimization Trap.
