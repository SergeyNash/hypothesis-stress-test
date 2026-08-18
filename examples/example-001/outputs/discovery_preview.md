# Preview discovery

Run-local KB island: `examples/example-001/kb-samples/`.

## Limits

- max_files_scanned: 200
- max_file_size: 2 MB
- max_evidence_items: 20
- skip_binary_by_default: true
- limit_reached: false

## Scanned

- kb-samples/notes_2024/workshop_queue.md
- kb-samples/custdev raw/2025-03-appsec-interview-excerpt.md
- kb-samples/custdev raw/whiteboard_scan_queues.txt
- kb-samples/strategy/product-strategy-2025.md

## Skipped

- нет файлов в пределах лимитов V1 (нет `.pdf` / `.docx` / `.html` / бинарных медиа без sidecar)

## Candidates

- kb-samples/notes_2024/workshop_queue.md — planned evidence_type: quote
- kb-samples/custdev raw/2025-03-appsec-interview-excerpt.md — planned evidence_type: transcript_excerpt
- kb-samples/custdev raw/whiteboard_scan_queues.txt — planned evidence_type: image_observation
- kb-samples/strategy/product-strategy-2025.md — planned evidence_type: quote

## Top relevant

- kb-samples/notes_2024/workshop_queue.md — quote — wait time критичных проектов, Slack-reorder, отсутствие критериев
- kb-samples/custdev raw/2025-03-appsec-interview-excerpt.md — transcript_excerpt — нет automation по criticality; сомнение, что порядок скана снижает production risk
- kb-samples/custdev raw/whiteboard_scan_queues.txt — image_observation — FIFO, waiting 4h+, no audit trail
- kb-samples/strategy/product-strategy-2025.md — quote — buyer CISO, land на queue/workflow, риск operator-only фич
