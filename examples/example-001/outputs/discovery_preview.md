# Discovery Preview

Example run — Local Evidence Discovery against mixed-source KB samples under `examples/example-001/kb-samples/`.

## Limits Applied

| Limit | Value |
| ----- | ----- |
| max_files_scanned | 200 |
| max_file_size | 2 MB |
| max_evidence_items | 20 |
| skip_binary_by_default | true |

Scan root: repository workspace (example subset — `examples/example-001/kb-samples/` treated as unstructured KB island for this canonical run).

Excluded paths: `hypothesis-stress-test/`, `runs/`, `.git/`, `.clinerules/`, `.cline/`, `node_modules/`, `examples/example-001/outputs/`

## Files Scanned

| Path | Kind | Size | Result |
| ---- | ---- | ---- | ------ |
| `examples/example-001/kb-samples/notes_2024/workshop_queue.md` | markdown | 1.1 KB | candidate |
| `examples/example-001/kb-samples/custdev raw/2025-03-appsec-interview-excerpt.md` | markdown | 0.9 KB | candidate |
| `examples/example-001/kb-samples/custdev raw/whiteboard_scan_queues.txt` | text | 0.4 KB | candidate |

## Files Skipped

| Path | Reason |
| ---- | ------ |
| `examples/example-001/kb-samples/custdev raw/2025-03-appsec-interview.m4a` | audio — metadata only; no transcript sidecar in repo |
| `*.pdf`, `*.docx`, `*.html` (none found in sample island) | unsupported extension in V1 |

## Candidate Files

1. `examples/example-001/kb-samples/notes_2024/workshop_queue.md` — workshop notes on queue latency
2. `examples/example-001/kb-samples/custdev raw/2025-03-appsec-interview-excerpt.md` — custdev transcript excerpt
3. `examples/example-001/kb-samples/custdev raw/whiteboard_scan_queues.txt` — whiteboard caption / image observation source

## Top Relevant Files (planned evidence type)

| File | Planned evidence type | Relevance hint |
| ---- | --------------------- | -------------- |
| `workshop_queue.md` | quote | critical project wait time |
| `2025-03-appsec-interview-excerpt.md` | transcript_excerpt | manual prioritization behavior |
| `whiteboard_scan_queues.txt` | image_observation | queue wait time in workflow diagram |

## Next Step

V1: extraction continues automatically after preview → `evidence_inventory.md`.
