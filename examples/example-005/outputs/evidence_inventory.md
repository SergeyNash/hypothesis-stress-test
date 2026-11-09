# Инвентарь evidence

Все items — synthetic_fixture, один учебный сценарий, не рыночная выборка.

### EVID-001
- source_path: kb-samples/operations/events.csv
- source_kind: text
- evidence_type: observation
- location: line:3-6
- observation: 60 событий, 60 часов активной работы; два выбранных класса — 40 событий и 28 часов.
- relevance: сервисная гипотеза
- relevance_reason: Показывает размер предполагаемой области автоматизации, а не её результат.
- retrieved_by: local-knowledge-retrieval (учебный пример)
- source_origin: synthetic
- evidence_status: synthetic

### EVID-002
- source_path: kb-samples/operations/customer-context.md
- source_kind: markdown
- evidence_type: observation
- location: line:3
- observation: Изменения требуют подтверждения инженера клиента; автономные полномочия не заданы.
- relevance: сервисная гипотеза
- relevance_reason: Ограничивает исходное обещание автономности.
- retrieved_by: local-knowledge-retrieval (учебный пример)
- source_origin: synthetic
- evidence_status: synthetic

### EVID-003
- source_path: kb-samples/operations/customer-context.md
- source_kind: markdown
- evidence_type: observation
- location: line:5-6
- observation: Клиентский baseline воздействия и принятие цены неизвестны.
- relevance: сервисная гипотеза
- relevance_reason: Не позволяет подтвердить 30% эффекта и путь покупки.
- retrieved_by: local-knowledge-retrieval (учебный пример)
- source_origin: synthetic
- evidence_status: synthetic

### EVID-004
- source_path: kb-samples/operations/provider-capacity.md
- source_kind: markdown
- evidence_type: observation
- location: line:3-4
- observation: 640 − 440 − 120 = 80 расчётных часов; подключение 24 часа, обслуживание 18–30 часов.
- relevance: сервисная гипотеза
- relevance_reason: Проверка масштаба и нагрузки; замещение не подтверждено.
- retrieved_by: local-knowledge-retrieval (учебный пример)
- source_origin: synthetic
- evidence_status: synthetic

### EVID-005
- source_path: kb-samples/operations/provider-capacity.md
- source_kind: markdown
- evidence_type: observation
- location: line:5
- observation: 18 часов включают контроль, исключения, знания/агента и координацию.
- relevance: сервисная гипотеза
- relevance_reason: Автоматизация создаёт собственную работу; экономия не измерена.
- retrieved_by: local-knowledge-retrieval (учебный пример)
- source_origin: synthetic
- evidence_status: synthetic

### EVID-006
- source_path: kb-samples/commercial/assumptions.md
- source_kind: markdown
- evidence_type: observation
- location: line:3-5
- observation: Цена 90000; час 3000; инструменты 12000; резерв 9000; подключение 24 часа.
- relevance: сервисная гипотеза
- relevance_reason: Исходные допущения для чувствительности экономики.
- retrieved_by: local-knowledge-retrieval (учебный пример)
- source_origin: synthetic
- evidence_status: synthetic

### EVID-007
- source_path: kb-samples/strategy/service-direction.md
- source_kind: markdown
- evidence_type: observation
- location: line:3-4
- observation: Повторяемость и сохранение действующих обязательств — учебные приоритеты поставщика.
- relevance: сервисная гипотеза
- relevance_reason: Стратегический замысел не является спросом.
- retrieved_by: local-knowledge-retrieval (учебный пример)
- source_origin: synthetic
- evidence_status: synthetic
