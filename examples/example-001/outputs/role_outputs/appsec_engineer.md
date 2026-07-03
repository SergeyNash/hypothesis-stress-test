# Ролевой анализ: Application Security Engineer

## Боль

Приоритет: CRITICAL

Инженеры AppSec балансируют coverage сканов и глубокий анализ критичных систем при ограниченной ёмкости сканирования.

Основные pain points:

* невозможность быстро реагировать на меняющиеся бизнес-приоритеты
* равное отношение к системам с разным уровнем риска
* ручные workarounds управления очередью
* сложность обосновывать prioritization decisions перед разработчиками

---

## Новые проблемы

* cognitive overload
* политическое давление от dev-команд
* отсутствие reproducibility решений
* риски манипуляции метриками
* дополнительная операционная нагрузка

---

## Альтернативы

* policy-driven prioritization
* metadata-based automation
* risk-based scanning
* parallel scanning
* FIFO как default model

---

## Контекст провала

* длительность скана уже мала относительно release cycles
* данные бизнес-критичности недоступны или ненадёжны
* низкая operational maturity для manual decisions
* политическое давление делает приоритизацию неустойчивой

---

## Границы применимости

### Работает когда

* wait times блокируют critical findings
* есть доступ к контексту бизнес-критичности
* 10–50 проектов, зрелый AppSec process

### Не работает когда

* automated risk-based scanning уже покрывает приоритизацию
* FIFO не создаёт operational pain

### Вредит когда

* решения нельзя audit или reproduce
* разработчики systematically bypass или геймят очередь
