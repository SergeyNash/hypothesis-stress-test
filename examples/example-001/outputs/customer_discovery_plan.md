# План Customer Discovery

## Цель исследования

Перед backlog commitment выяснить три вещи, без которых решение ложное: (1) есть ли у операторов рабочий источник критичности в момент bump очереди; (2) примет ли покупатель (CISO) гибрид policy + documented exceptions; (3) даёт ли смена порядка измеримый time-to-action — не снижение production risk.

---

## Что уже известно

- Перегрузка очереди и Slack-reorder — повторяющаяся операционная боль AppSec (EVID-001, EVID-003, EVID-006, EVID-010, EVID-011).
- SoT критичности нет; CISO хочет policy, команда делает exceptions в Slack; audit без формального ответа (EVID-007, EVID-008).
- AppSec Lead не подтверждает production risk reduction; отделяет порядок скана от remediation/ownership (EVID-009).
- Стратегия: land на queue/workflow, покупатель CISO, operator-only без CISO-visible value — не core (EVID-012 — EVID-016).
- Synthesis: reframe на governed workflow efficiency; исходный risk-framing отклонить как GTM/метрику.
- Confluence и внешний рынок в этом прогоне пустые — нельзя опираться на «категория рынка».

---

## Критические неизвестные

| Неизвестность | Тип риска | Приоритет | Evidence |
|---------------|-----------|-----------|----------|
| Есть ли в момент решения по очереди рабочий источник бизнес-критичности (каталог, tier, owner) или только память/Slack? | Workflow Risk | HIGH | EVID-006, EVID-007; иначе gap |
| Примет ли CISO documented manual exceptions поверх policy с audit trail? | Buyer Risk | HIGH | EVID-007, EVID-008, EVID-014; голос CISO в интервью — missing |
| Сокращает ли смена порядка time-to-first-finding / time-to-action по важным репозиториям? | Severity Risk | HIGH | EVID-001, EVID-009, EVID-010 |
| Связан ли порядок скана с remediation и production risk или это отдельный контур ownership? | Business Value Risk | HIGH | EVID-009; telemetry — missing |
| Как часто backlog очереди блокирует релиз в target accounts, не в одном воркшопе? | Frequency Risk | MEDIUM | EVID-004; выборка узкая |
| Масштабируется ли ручной режим beyond ~50 проектов без governance breakdown? | Strategic Fit Risk | MEDIUM | роли CISO; количественного evidence нет |
| Queue/workflow — land capability, за которую платят, или часть платформы без отдельного SKU? | Buyer Risk / Strategic Fit Risk | MEDIUM | EVID-015, EVID-016; win/loss — missing |
| Меняют ли разработчики поведение (гейминг «всё critical», эскалации) при непрозрачном bump? | Adoption Risk | MEDIUM | ролевой анализ; local evidence по разработчику — missing |
| Что платформа/CI позволяет сделать с приоритетом job без ломки pipeline-as-code? | Workflow Risk | MEDIUM | evidence: missing |
| Есть ли внутренние Confluence-решения по очереди сканов в реальных аккаунтах? | Problem Risk | LOW | confluence: missing |

---

## Рекомендуемые роли для интервью

- **AppSec Engineer** — ежедневный порядок очереди, SoT критичности, Slack-workarounds. Закрывает Workflow / Frequency. Вопросы Facilitator уже покрывают роль; не дублировать, использовать как есть.
- **AppSec Lead / Security Team Lead** — KPI, исключения vs норма, ответ audit. Нужен отдельно от IC: excerpt 2025-03 — это Lead, паттерн надо проверить на других аккаунтах.
- **CISO / Head of Application Security** — buyer, policy vs exceptions, что считается CISO-visible value. В KB нет прямого интервью, только слова оператора и strategy doc.
- **Enterprise Developer / Engineering Manager** — fairness, эскалации, влияние на релиз. Ролевой анализ есть, local evidence нет.
- **Platform / DevOps Engineer** — ёмкость воркеров, skip/bypass, совместимость bump с CI/CD. В гипотезе роль не была, это слепая зона Synthesis.

---

## Гайд для интервью

Блоки ниже — исследовательские цели. Конкретные формулировки: `validation_questions.md` (Facilitator + дополнение CDP). Не спрашивать «стали бы вы этим пользоваться».

### Текущий процесс

Понять, как очередь живёт сегодня: FIFO, кто bump'ает, откуда criticality, где это стыкуется с CI.

- Как сейчас выбирается следующий проект в очереди SAST?
- Кто ещё может сменить порядок и по какому поводу?
- Откуда в этот момент берётся tier / owner / production exposure?

### Последний опыт

Якорить на конкретный случай, не на мнение о фиче.

- Последний раз, когда критичный репозиторий ждал часы — что сделали руками?
- Последний blocked release из-за очереди — как узнали и чем кончилось?
- Последний запрос audit/CISO «почему этот проект прыгнул» — что ответили?

### Последствия

Отделить latency findings от remediation и от срыва чужого релиза.

- Что происходит с high-risk finding, если скан приехал раньше — кто берёт ownership?
- Какие trade-off, когда один репозиторий вытесняет другой?
- Меняется ли что-то в проде или только время до первого отчёта?

### Альтернативы

Зафиксировать уже живущие замены гипотезы.

- Slack-bump, ночной batch, skip job, рост ёмкости сканера, policy gates — что уже пробовали?
- В каких случаях FIFO «достаточно хорош»?
- Где уже есть automation по criticality и почему её нет здесь?

### Процесс принятия решений

Проверить buyer path, не feature wishlist.

- Кто утверждает правило очереди и кто — разовое исключение?
- Какое evidence нужно CISO, чтобы согласиться на manual exception?
- Что заблокирует rollout: audit, platform limits, fairness разработчиков?

---

## Приоритеты исследования

### Высокий приоритет

- SoT критичности в момент bump (без этого фича = Slack в UI).
- Acceptance CISO на policy + exceptions + audit trail (без этого нет покупки).
- Измеримый efficiency impact: wait time / time-to-first-finding, явно не production risk score.

### Средний приоритет

- Частота blocked releases в нескольких аккаунтах, не в одном воркшопе.
- Поведение разработчиков и гейминг очереди.
- CI/CD constraints с Platform/DevOps.
- Land vs platform: платят ли за queue capability отдельно.

### Низкий приоритет

- Внешний рынок как standalone категория — канал пуст, не блокирует near-term решение, если validation выше пройдена.
- Confluence-поиск исторических решений — имеет смысл после настройки MCP, не вместо интервью.

---

## Ожидаемые результаты обучения

- Понять, можно ли приоритизировать очередь без нового источника критичности или его нужно строить первым.
- Отделить: ускоряется ли появление findings в важных репозиториях от того, чинятся ли они и падает ли риск в проде.
- Услышать от CISO, какой минимальный governance (TTL, approver, след) делает exception приемлемым.
- Решить, какой нарратив вообще тестировать в пилоте: operational efficiency + governed workflow, не production risk reduction.
- Зафиксировать порог масштаба (порядка числа проектов), после которого ручной режим для покупателя неприемлем.
