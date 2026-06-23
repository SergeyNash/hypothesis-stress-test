# Evidence Inventory

## Retrieval Status

- Workspace root: hypothesis-stress-test (example subset: `examples/example-001/kb-samples/`)
- Limits: max_files_scanned=200, max_evidence_items=20
- Files scanned: 3
- Files skipped: 1 (audio without transcript)
- Candidate files: 3
- Evidence items: 4

## Items

### EVID-001

- Source: `examples/example-001/kb-samples/notes_2024/workshop_queue.md`
- Source kind: markdown
- Evidence type: quote
- Location: lines 8-9
- Observation: "Critical projects wait several hours before scanning when the queue is full"
- Relevance: scan queue latency
- Relevance reason: Direct statement about wait time for critical projects in SAST queue — matches hypothesis about prioritization and time-to-scan
- Retrieved by: local-knowledge-retrieval (example-001)

### EVID-002

- Source: `examples/example-001/kb-samples/notes_2024/workshop_queue.md`
- Source kind: markdown
- Evidence type: quote
- Location: lines 19-20
- Observation: "We only learn about queue backlog when a release is blocked."
- Relevance: operational visibility
- Relevance reason: Links queue backlog to release impact — supports business-critical scanning urgency in hypothesis
- Retrieved by: local-knowledge-retrieval (example-001)

### EVID-003

- Source: `examples/example-001/kb-samples/custdev raw/2025-03-appsec-interview-excerpt.md`
- Source kind: markdown
- Evidence type: transcript_excerpt
- Location: AppSec Lead response, paragraph 2
- Observation: "Business-critical apps aren't automatically first — someone has to remember to flag them."
- Relevance: manual prioritization gap
- Relevance reason: Confirms absence of automatic business-critical prioritization — core assumption in hypothesis statement
- Retrieved by: local-knowledge-retrieval (example-001)

### EVID-004

- Source: `examples/example-001/kb-samples/custdev raw/whiteboard_scan_queues.txt`
- Source kind: text
- Evidence type: image_observation
- Extraction note: derived from facilitator caption describing whiteboard photo labels and layout
- Observation: Diagram labels queue "waiting 4h+" between CI commit and SAST queue step
- Relevance: queue bottleneck
- Relevance reason: Visual workflow sketch shows multi-hour wait in scan pipeline — concrete latency signal for hypothesis
- Retrieved by: local-knowledge-retrieval (example-001)

### EVID-005 (metadata only — not promoted to claim)

- Source: `examples/example-001/kb-samples/custdev raw/2025-03-appsec-interview.m4a`
- Source kind: audio
- Evidence type: metadata_only
- Observation: Audio file referenced in transcript header; no transcript sidecar available in repo
- Relevance: custdev source
- Relevance reason: Companion media exists but content not extractable in V1 without transcript
- Retrieved by: local-knowledge-retrieval (example-001)
- Note: Do not use as factual claim in Market Layer
