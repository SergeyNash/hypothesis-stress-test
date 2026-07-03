# Резюме гипотезы

## Формулировка

Если инженеры Application Security смогут вручную приоритизировать проекты в очереди SAST-сканирования, то бизнес-критичные приложения будут сканироваться первыми, что сократит время обнаружения уязвимостей высокого риска и снизит общий production risk.

## Ключевая идея

Гипотеза предполагает, что ручная приоритизация очереди сканов улучшит response time для критичных систем и снизит бизнес-риск.

---

# Скрытые assumptions

## Assumption 1: Текущая приоритизация неэффективна
- Почему важно: без реальной боли нет adoption driver
- Evidence есть: role analysis — перегрузка очереди и workarounds
- Evidence нет: количественные данные о wait times и impact

## Assumption 2: У инженеров есть контекст бизнес-критичности
- Почему важно: приоритизация требует знания, какие apps важнее
- Evidence есть: нет прямого
- Evidence нет: интервью о доступности и качестве данных

## Assumption 3: Более раннее сканирование снижает production risk
- Почему важно: core value proposition зависит от risk reduction
- Evidence есть: только внутренняя логика
- Evidence нет: market/telemetry, связывающие порядок сканов с risk outcomes

## Assumption 4: Ручная приоритизация масштабируется
- Почему важно: enterprise adoption требует governance at scale
- Evidence есть: concerns CISO о scalability
- Evidence нет: proof sustainable process beyond 10–50 проектов

---

# Границы применимости

## Когда создаёт ценность

* Зрелые AppSec-команды с 10–50 активными проектами
* Доступны метаданные бизнес-критичности
* Wait times в очереди materially блокируют critical findings
* Гибрид: ручные исключения поверх policy automation

## Когда бесполезна

* Длительность скана уже мала относительно release cycles
* FIFO не создаёт operational pain
* Полностью automated risk-based scanning

## Когда вредна

* Децентрализованная приоритизация конфликтует с centralized risk governance
* Разработчики геймят очередь
* Audit не может воспроизвести решения о приоритизации

---

# Конфликты ролей

## Зоны согласия

* Перегрузка очереди сканов — реальная операционная проблема (AppSec, частично CISO)

## Зоны напряжения

* AppSec хочет control и responsiveness; CISO — policy consistency
* Developers хотят predictability; AppSec — flexibility reprioritize

## Зоны конфликта

* Ручная приоритизация усиливает AppSec, но ослабляет governance model CISO
* Быстрее сканы для critical apps могут задержать releases других команд

## Слепые зоны

* Penetration Tester недопредставлен
* Finance / procurement impact не проанализирован
* Platform CI/CD constraints не смоделированы явно

---

# Ключевые риски

* Фича решает efficiency, не risk reduction как в исходном framing
* Governance friction на enterprise scale
* Adoption blocked без business-context data

---

# Ключевые неопределённости

* Доступны ли надёжные данные бизнес-критичности
* Меняет ли приоритизация measurably time-to-remediation для critical findings
* Приемлема ли hybrid manual + automated model для CISO

---

# Оценка

## Promising

* Сильная CRITICAL боль AppSec при queue constraints
* Потенциал улучшения operational workflow

## Uncertain

* Связь порядка сканов с production risk reduction
* Enterprise scalability и governance acceptance

## Risky

* Политический конфликт децентрализации AppSec и централизации CISO
* Misaligned narrative (risk vs efficiency)

## Requires validation

* Интервью AppSec о queue workflows и context access
* Воркшоп CISO о governance model
* Пилот на одном mature account (10–30 проектов)
