# Preview discovery

Пример прогона — Local Evidence Discovery по mixed-source KB в `examples/example-001/kb-samples/`.

## Применённые лимиты

| Лимит | Значение |
| ----- | -------- |
| max_files_scanned | 200 |
| max_file_size | 2 MB |
| max_evidence_items | 20 |
| skip_binary_by_default | true |

Корень сканирования: `examples/example-001/kb-samples/` как unstructured KB island.

## Отсканированные файлы

| Путь | Тип | Результат |
| ---- | --- | --------- |
| `kb-samples/notes_2024/workshop_queue.md` | markdown | candidate |
| `kb-samples/custdev raw/2025-03-appsec-interview-excerpt.md` | markdown | candidate |
| `kb-samples/custdev raw/whiteboard_scan_queues.txt` | text | candidate |

## Пропущенные файлы

| Путь | Причина |
| ---- | ------- |
| `2025-03-appsec-interview.m4a` | audio — metadata only, нет transcript sidecar |

## Кандидаты

1. `workshop_queue.md` — заметки воркшопа о latency очереди
2. `2025-03-appsec-interview-excerpt.md` — excerpt custdev-интервью
3. `whiteboard_scan_queues.txt` — caption whiteboard / image observation

## Следующий шаг

V1: extraction автоматически после preview → `evidence_inventory.md`.
