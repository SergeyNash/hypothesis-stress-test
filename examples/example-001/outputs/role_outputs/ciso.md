# Анализ роли: CISO

Персона `knowledge-base/personas/chief-information-security-officer-ciso.md` — initial profile, `source_interviews: []`, confidence: low. Используется как слабый supporting context, не как первичное evidence.

## Боль

Приоритет: SECONDARY

CISO отвечает за enterprise risk, compliance и объяснимость инвестиций, а не за ежедневный порядок SAST-очереди. Боль гипотезы для этой роли косвенная: critical systems могут сканироваться слишком поздно, нет visibility, почему ресурсы сканера распределены именно так, сложно показать board «мы оптимизируем allocation». В зрелых организациях предпочтение скорее к policy-based automation, чем к ручному operational control. Персона (слабый сигнал): tool sprawl без единой картины риска, сложность доказать ROI AppSec, недоверие к децентрализованным решениям, которые нельзя audit.

Гипотеза бьёт в боль CISO только если ручная приоритизация даёт auditable, объяснимое распределение ёмкости. Сама кнопка «поднять проект» эту боль не закрывает.

## Новые проблемы

- Эскалации приоритизации поднимаются на leadership без формального path
- Audit спрашивает «почему этот проект прыгнул» — нет ответа
- Зависимость от конкретных AppSec-инженеров (bus-factor)
- Плохая масштабируемость: то, что работает на 15 репозиториях, ломается на 100
- Искажение security metrics: coverage и SLA выглядят лучше из-за ad-hoc bump, а не из-за политики
- Perception, что security снова ручной exception-driven процесс

## Альтернативы

- Policy-driven automation (tier, regulated, internet-facing)
- GRC / service-catalog интеграции как источник критичности
- Risk-based security program вместо операторского контроля очереди
- Увеличение scanning capacity как капитальная альтернатива софту приоритизации
- CI/CD gating policies: не порядок очереди, а правило «critical не едет без скана»
- Documented exception workflow с TTL и approver

## Контекст отказа

- Низкая security maturity: ручной контроль добавляет хаос, а не управление
- Regulated среда требует воспроизводимых решений — Slack-bump неприемлем
- Scale beyond ~50 проектов без governance automation
- Engineering leadership не купит модель, где AppSec вручную двигает чужие релизы
- Нет способа показать risk reduction, только локальную ловкость очереди

## Границы применимости

### Работает когда

- Гибрид: policy по умолчанию, ручные исключения с владельцем, сроком и audit trail
- CISO видит, какие системы получают ёмкость сканера и почему
- Исключения редкие, а не основной режим работы

### Не работает когда

- Организация требует centralized policy-driven allocation и не допускает операторских исключений
- Ручная приоритизация заменяет automation, а не дополняет её
- Нет языка, на котором это объясняется board (риск, compliance, TCO)

### Вредит когда

- Метрики искажаются ради оправдания ad-hoc изменений очереди
- Escalation paths для конфликтов приоритизации не определены
- Daily operator получает власть без CISO-visible accountability
