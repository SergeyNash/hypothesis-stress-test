# План Customer Discovery

## Цель исследования

Снизить неопределённость перед backlog commitment: подтвердить, что приоритизация очереди сканов — прежде всего проблема операционной эффективности, и проверить governance, adoption и buyer constraints для AppSec-команд.

---

## Что уже известно

- Перегрузка очереди — реальная повторяющаяся операционная боль AppSec.
- Framing гипотезы («снизить production risk») слабо поддержан evidence.
- Signal collision предлагает reframe на efficiency и time-to-action.
- Governance tension: ручной контроль AppSec vs policy consistency CISO.

---

## Критические неизвестные

| Неизвестное | Тип риска | Приоритет |
|-------------|-----------|-----------|
| Есть ли у AppSec engineers надёжный контекст бизнес-критичности для корректной приоритизации? | Workflow Risk | HIGH |
| Существенно ли сокращает queue prioritization time-to-action для critical findings? | Severity Risk | HIGH |
| Принимает ли покупатель (CISO) гибридную manual + policy модель? | Buyer Risk | HIGH |
| Как часто перегрузка очереди блокирует critical findings в target accounts? | Frequency Risk | MEDIUM |
| Приоритизация очереди — standalone purchase driver или часть broader workflow? | Business Value Risk | MEDIUM |
| Масштабируется ли процесс beyond 50 проектов без governance breakdown? | Strategic Fit Risk | MEDIUM |

---

## Рекомендуемые роли для интервью

- **AppSec Engineer** — workflow очереди, доступность контекста, практическое поведение приоритизации.
- **Security Team Lead / AppSec Manager** — operational KPIs, координация, policy exceptions.
- **CISO / Security Director** — governance, auditability, purchasing priorities.
- **Developer / Engineering Manager** — downstream impact (release delays, fairness).
- **Platform / DevOps Engineer** — CI/CD constraints, integration friction, limits at scale.

---

## Гайд для интервью

### Текущий workflow

- Расскажите, как сейчас определяется порядок очереди сканов.
- Кто может менять приоритет и в каких ситуациях?
- Какую информацию вы проверяете перед сменой приоритета скана?

### Недавний опыт

- Расскажите о последнем случае, когда порядок очереди имел значение.
- Опишите последний раз, когда критичное приложение ждало в очереди.
- Что произошло при последнем конфликте из-за приоритизации сканов?

### Последствия

- Какие операционные последствия, когда приоритизация очереди ошибочна?
- Как это влияет на remediation time для high-severity findings?
- Какие trade-offs возникают, когда одна команда приоритизирована над другой?

### Альтернативы

- Как вы решаете это сегодня без dedicated prioritization tooling?
- Какие policy, automation или workarounds уже есть?
- В каких случаях текущий процесс «достаточно хорош»?

### Процесс принятия решений

- Кто утверждает правила или исключения приоритизации?
- Какое evidence требуется для обоснования смены приоритета?
- Что заблокирует rollout manual-prioritization capability?

---

## Приоритеты исследования

### High Priority

- Проверить доступность контекста для безопасной приоритизации.
- Проверить измеримый efficiency impact (time-to-action, сокращение queue delay).
- Проверить governance acceptance для hybrid manual + policy model.

### Medium Priority

- Частота и границы сегмента queue pain.
- Buyer motivation и purchase framing (feature vs standalone category).
- Scalability assumptions при 50+ проектах.

### Low Priority

- Сравнение вторичных альтернатив, не меняющих near-term decision.

---

## Ожидаемые результаты

- Определить, достаточно ли частота проблемы в target segments для prioritization capabilities.
- Определить, должен ли value narrative быть efficiency-first, а не risk-reduction-first.
- Определить governance constraints для adoption в enterprise.
- Определить минимальный evidence threshold для backlog commitment.
