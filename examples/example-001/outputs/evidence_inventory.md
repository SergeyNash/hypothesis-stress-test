# Инвентарь evidence

## Статус retrieval

- Корень: `examples/example-001/kb-samples/`
- Лимиты: max_files_scanned=200, max_evidence_items=20
- Отсканировано файлов: 3
- Пропущено: 1 (audio без transcript)
- Evidence items: 5
- limit_reached: false

## Items

### EVID-001

- source_path: kb-samples/notes_2024/workshop_queue.md
- source_kind: markdown
- evidence_type: quote
- observation: «Критичные проекты ждут несколько часов перед сканированием, когда очередь заполнена»
- relevance: scan queue latency
- relevance_reason: Прямое утверждение о wait time для critical projects
- retrieved_by: local-knowledge-retrieval

### EVID-002

- source_path: kb-samples/notes_2024/workshop_queue.md
- source_kind: markdown
- evidence_type: quote
- observation: «О перегрузке очереди узнаём только когда блокируется релиз»
- relevance: operational visibility
- relevance_reason: Связывает backlog очереди с release impact
- retrieved_by: local-knowledge-retrieval

### EVID-003

- source_path: kb-samples/custdev raw/2025-03-appsec-interview-excerpt.md
- source_kind: markdown
- evidence_type: transcript_excerpt
- observation: «Business-critical apps не идут первыми автоматически — кто-то должен вспомнить их пометить»
- relevance: manual prioritization gap
- relevance_reason: Подтверждает отсутствие automatic business-critical prioritization
- retrieved_by: local-knowledge-retrieval

### EVID-004

- source_path: kb-samples/custdev raw/whiteboard_scan_queues.txt
- source_kind: text
- evidence_type: image_observation
- extraction_note: derived from diagram labels and layout
- observation: На диаграмме очередь «waiting 4h+» между CI commit и SAST queue step
- relevance: queue bottleneck
- relevance_reason: Визуальная метка latency в очереди между CI и SAST
- retrieved_by: local-knowledge-retrieval

### EVID-005

- source_path: 2025-03-appsec-interview.m4a
- source_kind: audio
- evidence_type: metadata_only
- observation: Аудиоинтервью без transcript sidecar
- relevance: potential primary evidence
- relevance_reason: Файл существует, но содержимое недоступно в V1
- retrieved_by: local-knowledge-retrieval
