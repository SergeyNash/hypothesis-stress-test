# Инвентарь evidence

## Статус retrieval

- Корень: `examples/example-001/kb-samples/`
- Лимиты: max_files_scanned=200, max_file_size=2 MB, max_evidence_items=20
- Отсканировано файлов: 4
- Пропущено: 0
- Evidence items: 16
- limit_reached: false
- retrieved_by: local-knowledge-retrieval

## Items

### EVID-001

- source_path: kb-samples/notes_2024/workshop_queue.md
- source_kind: markdown
- evidence_type: quote
- location: Цитаты / список буллетов
- observation: «Критичные проекты ждут несколько часов перед сканированием, когда очередь заполнена»
- relevance: scan queue latency
- relevance_reason: Прямое утверждение о wait time для критичных проектов при полной очереди
- retrieved_by: local-knowledge-retrieval

### EVID-002

- source_path: kb-samples/notes_2024/workshop_queue.md
- source_kind: markdown
- evidence_type: quote
- location: список буллетов
- observation: «Равное отношение к системам с разным риском — постоянная проблема»
- relevance: undifferentiated queue
- relevance_reason: FIFO/равный порядок назван как повторяющаяся проблема, а не разовый сбой
- retrieved_by: local-knowledge-retrieval

### EVID-003

- source_path: kb-samples/notes_2024/workshop_queue.md
- source_kind: markdown
- evidence_type: quote
- location: список буллетов
- observation: «Переставляем вручную через Slack, когда кто-то кричит громче всех»
- relevance: manual workaround
- relevance_reason: Текущий способ приоритизации — чат-эскалация, не формальный процесс
- retrieved_by: local-knowledge-retrieval

### EVID-004

- source_path: kb-samples/notes_2024/workshop_queue.md
- source_kind: markdown
- evidence_type: quote
- location: список буллетов / цитата
- observation: «Мы узнаём о перегрузке очереди только когда блокируется релиз»
- relevance: operational visibility
- relevance_reason: Сигнал о backlog очереди приходит через blocked release, не через мониторинг очереди
- retrieved_by: local-knowledge-retrieval

### EVID-005

- source_path: kb-samples/notes_2024/workshop_queue.md
- source_kind: markdown
- evidence_type: observation
- location: Whiteboard
- observation: На воркшопе цепочка зафиксирована как FIFO queue → manual reorder → «кто критичнее?» без единых критериев
- relevance: missing prioritization criteria
- relevance_reason: Участники не назвали общий критерий критичности, только вопрос без ответа
- retrieved_by: local-knowledge-retrieval

### EVID-006

- source_path: kb-samples/custdev raw/2025-03-appsec-interview-excerpt.md
- source_kind: markdown
- evidence_type: transcript_excerpt
- location: ответ AppSec Lead на «как решаете, что сканировать первым»
- observation: «Вручную. У нас нет автоматики по business-criticality — кто-то должен вспомнить пометить tier-1. Business-critical apps не идут первыми автоматически.»
- relevance: manual prioritization gap
- relevance_reason: Прямое описание текущего процесса и отсутствия automatic business-critical order
- retrieved_by: local-knowledge-retrieval

### EVID-007

- source_path: kb-samples/custdev raw/2025-03-appsec-interview-excerpt.md
- source_kind: markdown
- evidence_type: transcript_excerpt
- location: ответ на «что мешает»
- observation: «Нет единого источника правды о критичности. CISO хочет policy, мы делаем exceptions в Slack.»
- relevance: criticality data gap
- relevance_reason: Названы отсутствие SoT по критичности и конфликт policy vs Slack exceptions
- retrieved_by: local-knowledge-retrieval

### EVID-008

- source_path: kb-samples/custdev raw/2025-03-appsec-interview-excerpt.md
- source_kind: markdown
- evidence_type: transcript_excerpt
- location: ответ на «что мешает»
- observation: «Audit спрашивает «почему этот проект прыгнул в очереди» — ответа формального нет.»
- relevance: auditability gap
- relevance_reason: Прямое утверждение об отсутствии формального ответа для audit на смену порядка очереди
- retrieved_by: local-knowledge-retrieval

### EVID-009

- source_path: kb-samples/custdev raw/2025-03-appsec-interview-excerpt.md
- source_kind: markdown
- evidence_type: transcript_excerpt
- location: ответ на «снизило бы это production risk»
- observation: «Не уверен. Скорее мы быстрее увидим findings в важных репозиториях. Risk в проде — это remediation и ownership, не только порядок скана.»
- relevance: risk-outcome doubt
- relevance_reason: Оператор не подтверждает production risk reduction; отделяет порядок скана от remediation/ownership
- retrieved_by: local-knowledge-retrieval

### EVID-010

- source_path: kb-samples/custdev raw/whiteboard_scan_queues.txt
- source_kind: text
- evidence_type: image_observation
- extraction_note: подпись whiteboard (фото в прогоне отсутствует; извлечено из caption и меток диаграммы)
- observation: На диаграмме CI/CD между commit и SAST указано «waiting 4h+»
- relevance: queue bottleneck
- relevance_reason: Визуальная метка multi-hour wait между CI и шагом SAST
- retrieved_by: local-knowledge-retrieval

### EVID-011

- source_path: kb-samples/custdev raw/whiteboard_scan_queues.txt
- source_kind: text
- evidence_type: image_observation
- extraction_note: стикеры на whiteboard
- observation: Стикеры на доске: «FIFO default», «manual bump in Slack», «no audit trail»
- relevance: current queue operating model
- relevance_reason: Три метки фиксируют default, workaround и отсутствие следа решений
- retrieved_by: local-knowledge-retrieval

### EVID-012

- source_path: kb-samples/strategy/product-strategy-2025.md
- source_kind: markdown
- evidence_type: quote
- location: Стратегические приоритеты / пункт 1
- observation: «Выигрывать enterprise AppSec workflows — конкурировать операционной эффективностью в CI/CD, не generic risk dashboards.»
- relevance: strategic priority
- relevance_reason: Стратегия называет CI/CD operational efficiency, а не risk dashboard, как способ выигрывать enterprise
- retrieved_by: local-knowledge-retrieval

### EVID-013

- source_path: kb-samples/strategy/product-strategy-2025.md
- source_kind: markdown
- evidence_type: quote
- location: Стратегические приоритеты / пункт 3
- observation: «Дифференцироваться vs Appscreener и Checkmarx через developer experience и queue/workflow automation.»
- relevance: competitive positioning
- relevance_reason: Queue/workflow automation названа как ось дифференциации против конкретных конкурентов
- retrieved_by: local-knowledge-retrieval

### EVID-014

- source_path: kb-samples/strategy/product-strategy-2025.md
- source_kind: markdown
- evidence_type: quote
- location: Целевой покупатель
- observation: «Экономический покупатель: CISO / Head of Application Security»; «Не primary: individual developers как budget owners»
- relevance: buyer definition
- relevance_reason: Документ явно отделяет экономического покупателя от daily users и developer budget owners
- retrieved_by: local-knowledge-retrieval

### EVID-015

- source_path: kb-samples/strategy/product-strategy-2025.md
- source_kind: markdown
- evidence_type: quote
- location: GTM-фокус
- observation: «Land с workflow pain (scan pipeline, queue management, policy gates)»
- relevance: GTM land motion
- relevance_reason: Queue management назван как land-боль, с которой входят в аккаунт
- retrieved_by: local-knowledge-retrieval

### EVID-016

- source_path: kb-samples/strategy/product-strategy-2025.md
- source_kind: markdown
- evidence_type: quote
- location: GTM-фокус / бизнес-модель
- observation: «Фичи только для daily operators без CISO-visible value — риск upsell, не core driver»
- relevance: operator-only feature risk
- relevance_reason: Стратегия прямо маркирует operator-only фичи без ценности для CISO как не core
- retrieved_by: local-knowledge-retrieval
