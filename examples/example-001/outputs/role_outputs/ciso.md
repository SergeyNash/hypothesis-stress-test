# Ролевой анализ: CISO

## Боль

Приоритет: SECONDARY

CISO отвечает за enterprise risk management и хочет visibility в allocation security resources.

Основные concerns:

* critical systems могут сканироваться недостаточно рано
* отсутствие visibility в prioritization decisions
* невозможность демонстрировать optimized risk allocation

В зрелых организациях чаще предпочитают policy-based automation вместо ручного operational control.

---

## Новые проблемы

* эскалация конфликтов приоритизации
* риски auditability
* зависимость от конкретных AppSec-сотрудников
* плохая scalability
* искажённые security metrics

---

## Альтернативы

* policy-driven automation
* GRC integrations
* risk-based security programs
* увеличение scanning capacity
* CI/CD gating policies

---

## Контекст провала

* низкая security maturity — ручной контроль добавляет хаос
* приоритизация не auditable для compliance
* bus-factor на отдельных AppSec engineers
* scale beyond 50+ проектов без governance automation

---

## Границы применимости

### Работает когда

* гибрид: policy automation с documented manual exceptions
* visibility и audit trail для каждого prioritization decision

### Не работает когда

* организация требует centralized policy-driven risk allocation
* manual prioritization заменяет, а не дополняет automation

### Вредит когда

* метрики искажаются для оправдания ad-hoc queue changes
* escalation paths для prioritization conflicts не определены
