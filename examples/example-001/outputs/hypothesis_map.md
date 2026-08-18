# Единое резюме гипотезы

Ручная приоритизация очереди SAST заявлена как способ снизить production risk. После столкновения ролей, локального evidence, бизнес-контекста и рынка (без внешнего канала) видно другое: операционная боль очереди подтверждена, механизм risk reduction — нет. Стратегия уже хочет queue/workflow с CISO-visible governance; исходная формулировка продаёт другой outcome.

---

# Подтверждённые сигналы

* **Validated Opportunity (узкий):** перегрузка очереди и ручной Slack-reorder — CRITICAL боль AppSec совпадает с EVID-001, EVID-003, EVID-006, EVID-010, EVID-011. Роли YES + local KB YES.
* FIFO одинаково относится к разному риску — и воркшоп, и interview excerpt это называют текущим процессом, не гипотезой автора.
* Buyer vs user разведены одинаково в ролях и в стратегии: платит CISO, очередь крутит AppSec (EVID-014).

---

# Внутренние иллюзии

* **Раньше просканировали → ниже production risk.** Facilitator пометил это как недоказанное предположение. Local evidence его прямо ослабляет: AppSec Lead не уверен и указывает на remediation/ownership (EVID-009). Market (KB) не добавляет подтверждающего канала. Internal Illusion.
* **У инженеров есть контекст критичности, чтобы приоритезировать «правильно».** Гипотеза это подразумевает. EVID-006 и EVID-007 говорят обратное: tier-1 надо вспомнить пометить, SoT нет. Иллюзия входных данных, не только outcome.

---

# Упущенные возможности

* Стратегия уже ставит queue/workflow automation и land на queue management (EVID-013, EVID-015). Исходная гипотеза этот GTM-рычаг не использует — она говорит про production risk.
* Гибрид policy + documented exceptions с audit trail закрывает конфликт CISO/AppSec, который Facilitator назвал структурным. В формулировке гипотезы его нет — только «вручную приоритизировать».
* Метрика time-to-first-finding в важных репозиториях есть в словах оператора (EVID-009) и ближе к OKR time-to-value, чем risk score.

---

# Ловушки локальной оптимизации

* Roles YES + local market YES по боли очереди, но buyer/value chain для «снизить production risk» не собирается (Business Context: Operational Driver, Revenue/risk — неизвестно).
* EVID-016: фича только для daily operator без CISO-visible value — не core. Ручной bump без policy и следа — ровно этот паттерн.
* Риск: построить кнопку порядка очереди, которая воспроизводит Slack внутри продукта и не двигает win rate / governance / retention.

---

# Ключевые дивергенции

### Эффективность vs production risk (HIGH)

- Противоречие: формулировка обещает risk reduction; роли, EVID-009 и Business Context описывают workflow efficiency / time-to-action
- Бизнес-последствие: неверный нарратив для CISO и ложный success metric
- Приоритет проверки: HIGH

### Ручной контроль AppSec vs policy/audit CISO (HIGH)

- Противоречие: AppSec хочет гибкость; CISO и EVID-007/EVID-008 требуют policy и формальный ответ audit
- Бизнес-последствие: enterprise adoption блокируется, даже если операторам фича нравится
- Приоритет проверки: HIGH

### СоT критичности vs обещанный порядок очереди (HIGH)

- Противоречие: приоритизация предполагает знание, что critical; evidence говорит, что SoT нет (EVID-005, EVID-006, EVID-007)
- Бизнес-последствие: продукт без интеграции контекста останется «кто кричит громче»
- Приоритет проверки: HIGH

---

# Слепые зоны

* Platform / DevOps: кто встраивает порядок очереди в CI/CD и чем ограничена ёмкость раннеров — в ролях гипотезы нет, в evidence нет
* Голос CISO как интервью: в KB есть только слова AppSec Lead о том, чего хочет CISO, плюс strategy doc
* Разработчик: ролевой анализ есть, локального evidence нет
* Влияние bump на покрытие остальных проектов и на чужие релизы — не измерено
* Внешний рынок и Confluence — каналы пустые; нельзя утверждать отдельную категорию покупки queue prioritization

---

# Новая информация

Видно только после сравнения слоёв, не из любого артефакта по отдельности:

* Гипотеза, скорее всего, **решает другую проблему**, чем заявляет: latency очереди и отсутствие SoT, не production risk.
* Facilitator-конфликт AppSec vs CISO **не снимается рынком** — локальный transcript его усиливает (policy vs Slack exceptions, нет ответа audit).
* Business Context меняет знак strategic fit: Low для risk-framing, Medium для governed queue/workflow — при том же операционном рычаге.
* Стратегия уже содержит нужный reframe (CI/CD efficiency, queue management, CISO-visible value). Роли и исходная формулировка его не использовали.
* Пустые Confluence и external каналы значат: «рынок подтверждает боль очереди» в этом прогоне **неверно**. Подтверждает только local KB island.

---

# Границы применимости

## Работает когда

* 10–50 проектов, очередь реально конкурирует за ёмкость (EVID-001, EVID-010)
* Есть хотя бы грубый источник критичности **или** он создаётся вместе с фичей
* Ручные исключения поверх policy, с TTL и audit trail
* Метрика успеха — time-to-action / time-to-first-finding, не production risk score

## Не работает когда

* FIFO не создаёт боли (ёмкость достаточна)
* Automated risk-based порядок уже есть
* Нет данных о критичности и нет плана их завести
* Покупатель требует только измеримое снижение риска в проде

## Ломается когда

* Нет формального ответа «почему проект прыгнул» (EVID-008)
* Slack-модель переезжает в UI без правил
* Scale, где bus-factor на дежурном AppSec неприемлем для CISO
* Разработчики геймят «всё critical»

---

# Влияние на исходную гипотезу

**Reframe Problem** — сохранить операционный рычаг (порядок очереди), сменить outcome с «снизить production risk» на «ускорить time-to-action по важным репозиториям в governed workflow».

**Narrow Scope** — зрелые AppSec-команды с ограниченной ёмкостью сканера, не default для всей enterprise-установки.

**Require Validation** — SoT критичности, принятие CISO гибрида policy+exceptions, измеримый efficiency impact. Связь с production risk не использовать как claim до отдельных evidence.

**Reject Current Framing** как go-to-market и success metric. Не reject самой боли очереди.

---

# Приоритеты дальнейшей проверки

| Приоритет | Цель |
|----------|------|
| HIGH | Есть ли рабочий источник бизнес-критичности в момент решения по очереди (EVID-006, EVID-007) |
| HIGH | Примет ли CISO documented manual exceptions поверх policy (EVID-007, EVID-008, EVID-014) |
| HIGH | Меняет ли порядок очереди time-to-first-finding / time-to-action, не «риск в проде» (EVID-009) |
| MEDIUM | Частота blocked release из-за очереди в target accounts (EVID-004) |
| MEDIUM | Queue/workflow — land capability или часть более широкой платформы (EVID-015, EVID-016) |
| LOW | Внешний рынок как отдельная категория покупки — канал в этом прогоне пуст |
