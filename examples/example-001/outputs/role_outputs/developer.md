# Ролевой анализ: Enterprise Developer

## Боль

Приоритет: SECONDARY

Разработчики испытывают неопределённость в timing сканов и predictability релизов.

Pain points:

* непредсказуемое время завершения сканов
* critical findings в последний момент перед release
* perceived unfairness в приоритизации
* ожидание scan results блокирует delivery

---

## Новые проблемы

* perceived unfairness
* отсутствие transparency
* политическое давление на AppSec
* поведение «всё критично»
* смещение фокуса с quality кода на манипуляцию очередью

---

## Альтернативы

* shift-left scanning
* CI/CD-integrated scanning
* predictable schedules
* self-service scanning
* увеличение throughput

---

## Контекст провала

* критерии приоритизации неясны
* release deadlines игнорируются
* существуют informal bypasses
* release blocking становится operationally destructive
* нет visibility в изменения очереди

---

## Границы применимости

### Работает когда

* transparency timing сканов для dev-команд
* правила приоритизации predictable и documented

### Не работает когда

* изменения очереди opaque и unpredictable
* throughput сканов уже достаточен для release cadence

### Вредит когда

* возникает поведение «всё критично»
* фокус смещается с quality кода на queue manipulation
