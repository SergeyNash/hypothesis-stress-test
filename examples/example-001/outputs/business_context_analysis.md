# Анализ бизнес-контекста

## Доступный контекст

- `kb-samples/strategy/product-strategy-2025.md` — приоритеты, GTM, OKR H1 2025, покупатель, бизнес-модель
- Roles Layer: `hypothesis_summary.md`, `role_outputs/appsec_engineer.md`, `role_outputs/ciso.md`, `role_outputs/enterprise_developer.md`
- Evidence: EVID-001 — EVID-016

## Недостающий контекст

- Unit economics и влияние queue capability на pricing / scan-capacity SKU
- Win/loss по bake-off: выигрывали ли сделки на queue/workflow, а не на scanner features
- Критерии закупки CISO в живых enterprise deals (budget cycle, RFP language)
- Количественные OKR-метрики time-to-value по конкретным аккаунтам

## Карта заинтересованных сторон

| Вопрос | Кто | Заметки |
|--------|-----|---------|
| Кто испытывает боль? | AppSec Engineer | EVID-001, EVID-003, EVID-006; CRITICAL в ролевом анализе |
| Кто получает операционную ценность? | AppSec Engineer | быстрее findings в важных репозиториях (EVID-009) |
| Кто решает и платит? | CISO / Head of Application Security | EVID-014 |
| Кто внедряет? | Platform / DevOps (вне scope гипотезы) | ограничение: сосуществовать с CI/CD |
| Кто может блокировать? | CISO (policy/audit), Developer (fairness/гейминг очереди) | EVID-007, EVID-008 |
| Кто не primary budget owner? | Individual developers | EVID-014 |

## Поток создания ценности

```text
Проблема: FIFO-очередь SAST одинаково относится к системам разного риска;
          критичные проекты ждут часы; порядок чинят в Slack (EVID-001, EVID-003, EVID-006)
    ↓
Бенефициар (user): AppSec Engineer меняет порядок очереди руками
    ↓
Изменение поведения: critical / tier-1 едет раньше; меньше ожидания «пока кто-то крикнет»
    ↓
Операционный эффект: быстрее time-to-first-finding в важных репозиториях (EVID-009)
    ↓
Заявленный бизнес-эффект: снижение production risk — разрыв цепочки
    ↓
Buyer-visible эффект: не доказан. Стратегия требует CISO-visible value
          (governance, audit trail, workflow win) — EVID-012, EVID-016
```

Разрыв: гипотеза перескакивает от операторского поведения к production risk. Локальный evidence этот прыжок не поддерживает (EVID-009). Buyer-цепочка обрывается, пока нет policy + audit trail (EVID-007, EVID-008).

## Тип бизнес-эффекта

- **Operational Driver** — основной. Боль очереди и Slack-workaround подтверждены EVID-001—EVID-006, EVID-010, EVID-011.
- **Adoption Driver** — средний. Land с queue management назван в GTM (EVID-015); daily users — AppSec.
- **Competitive Driver** — средний при framing «queue/workflow automation vs Appscreener и Checkmarx» (EVID-013). Слабый, если позиционировать как generic risk reduction.
- **Revenue Driver** — неизвестно. Нет evidence, что CISO покупает отдельную кнопку приоритизации очереди.
- **Retention Driver** — неизвестно. Стратегия связывает retention с глубиной CI/CD и governance, не с ручным bump.

Первичная классификация: **Operational Driver**. Не доказаны Revenue Driver и risk-reduction outcome.

## Связь со стратегией

**Medium** для reframe «enterprise workflow + governed queue exceptions».

**Low** для исходного framing «снизить production risk».

Совпадает:

- Приоритет #1: выигрывать enterprise AppSec workflows операционной эффективностью CI/CD, не risk dashboards (EVID-012)
- Дифференциация через queue/workflow automation (EVID-013)
- GTM land: scan pipeline, queue management, policy gates (EVID-015)
- OKR time-to-value для новых AppSec-команд — ближе к working scan workflow, чем к «меньше production risk»

Расходится:

- Экономический покупатель — CISO, не AppSec-оператор (EVID-014)
- Operator-only без CISO-visible value — риск upsell, не core (EVID-016)
- Standalone features без buyer-visible outcomes — не приоритет OKR
- CISO хочет policy, операторы делают Slack exceptions без audit trail (EVID-007, EVID-008)

Источники: `kb-samples/strategy/product-strategy-2025.md`; EVID-012 — EVID-016.

## Ключевые риски

- **Buyer vs user:** боль у AppSec, бюджет у CISO; ручной контроль без audit — блокер покупки
- **Разрыв механизма ценности:** порядок скана ≠ production risk (EVID-009)
- **Локальная оптимизация:** очередь для оператора без движения buyer metrics
- **Standalone feature:** стратегия запрещает узкую scanner utility без workflow/governance
- **Adoption:** разработчики могут геймить «всё критично», если правила непрозрачны

## Ключевые возможности

- Собрать capability как **governed workflow**: policy default + ручные исключения с TTL, владельцем и audit trail
- Сделать queue management land-фичей (EVID-015), а не «ещё один risk dashboard» (EVID-012)
- Пилот в mature accounts (10–50 проектов) с метрикой time-to-first-finding / time-to-action, явно не production risk
- Audit trail на jump очереди закрывает EVID-008 и даёт CISO-visible value

## Резюме для downstream-слоёв

Проблема очереди правдоподобна как operational pain. Business case «снизить production risk» не собран. Strategic fit есть у **queue/workflow automation с governance**, которую стратегия уже называет осью дифференциации. Если строить только ручной bump для AppSec без policy и следа решений — ждать Local Optimization Trap и отказ покупателя. Market и Synthesis не должны выводить risk-reduction или revenue без новых evidence.
