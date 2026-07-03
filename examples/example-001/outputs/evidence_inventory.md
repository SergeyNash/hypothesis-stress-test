# Инвентарь evidence

## Статус retrieval

- Корень: `examples/example-001/kb-samples/`
- Лимиты: max_files_scanned=200, max_evidence_items=20
- Отсканировано файлов: 3
- Пропущено: 1 (audio без transcript)
- Evidence items: 4

## Items

### EVID-001

- Source: `kb-samples/notes_2024/workshop_queue.md`
- evidence_type: quote
- Observation: «Критичные проекты ждут несколько часов перед сканированием, когда очередь заполнена»
- Relevance: scan queue latency
- relevance_reason: Прямое утверждение о wait time для critical projects

### EVID-002

- Source: `kb-samples/notes_2024/workshop_queue.md`
- evidence_type: quote
- Observation: «О перегрузке очереди узнаём только когда блокируется релиз»
- Relevance: operational visibility
- relevance_reason: Связывает backlog очереди с release impact

### EVID-003

- Source: `kb-samples/custdev raw/2025-03-appsec-interview-excerpt.md`
- evidence_type: transcript_excerpt
- Observation: «Business-critical apps не идут первыми автоматически — кто-то должен вспомнить их пометить»
- Relevance: manual prioritization gap
- relevance_reason: Подтверждает отсутствие automatic business-critical prioritization

### EVID-004

- Source: `kb-samples/custdev raw/whiteboard_scan_queues.txt`
- evidence_type: image_observation
- extraction_note: caption whiteboard photo
- Observation: На диаграмме очередь «waiting 4h+» между CI commit и SAST queue step
- Relevance: queue bottleneck

### EVID-005 (metadata only — не promote to claim)

- Source: `2025-03-appsec-interview.m4a`
- evidence_type: metadata_only
- Note: Не использовать как factual claim в Market Layer
