# Анализ рынка

## Статус MCP

Confluence MCP: not configured

## Локальные сигналы из базы знаний

- Критичные проекты ждут несколько часов в очереди SAST, когда очередь заполнена — signal: strong — evidence_id: EVID-001 — evidence_type: quote — source: kb-samples/notes_2024/workshop_queue.md
- На whiteboard CI/CD между commit и SAST стоит метка «waiting 4h+» — signal: strong — evidence_id: EVID-010 — evidence_type: image_observation — source: kb-samples/custdev raw/whiteboard_scan_queues.txt
- Равное отношение к системам с разным риском названо постоянной проблемой — signal: strong — evidence_id: EVID-002 — evidence_type: quote — source: kb-samples/notes_2024/workshop_queue.md
- Текущий workaround: ручной reorder через Slack, «кто кричит громче» — signal: strong — evidence_id: EVID-003 — evidence_type: quote — source: kb-samples/notes_2024/workshop_queue.md
- О перегрузе очереди узнают, когда блокируется релиз — signal: strong — evidence_id: EVID-004 — evidence_type: quote — source: kb-samples/notes_2024/workshop_queue.md
- Нет автоматики по business-criticality; tier-1 нужно помнить пометить вручную — signal: strong — evidence_id: EVID-006 — evidence_type: transcript_excerpt — source: kb-samples/custdev raw/2025-03-appsec-interview-excerpt.md
- Нет единого источника правды о критичности; CISO хочет policy, команда делает Slack exceptions — signal: strong — evidence_id: EVID-007 — evidence_type: transcript_excerpt — source: kb-samples/custdev raw/2025-03-appsec-interview-excerpt.md
- Audit не получает формального ответа, почему проект прыгнул в очереди — signal: strong — evidence_id: EVID-008 — evidence_type: transcript_excerpt — source: kb-samples/custdev raw/2025-03-appsec-interview-excerpt.md
- AppSec Lead не подтверждает, что порядок скана снизит production risk; отделяет finding latency от remediation/ownership — signal: strong (против заявленного outcome) — evidence_id: EVID-009 — evidence_type: transcript_excerpt — source: kb-samples/custdev raw/2025-03-appsec-interview-excerpt.md
- Default модели на доске: FIFO, manual bump in Slack, no audit trail — signal: strong — evidence_id: EVID-011 — evidence_type: image_observation — source: kb-samples/custdev raw/whiteboard_scan_queues.txt
- Стратегия: выигрывать enterprise workflows операционной эффективностью CI/CD, не generic risk dashboards — signal: strong (internal strategy, не внешний рынок) — evidence_id: EVID-012 — evidence_type: quote — source: kb-samples/strategy/product-strategy-2025.md
- Queue/workflow automation названа осью дифференциации vs Appscreener и Checkmarx — signal: weak как рыночный факт (это внутренний intent, не независимое подтверждение рынка) — evidence_id: EVID-013 — evidence_type: quote — source: kb-samples/strategy/product-strategy-2025.md
- Queue management входит в GTM land-motion — signal: weak как рыночный факт; strong как внутренний GTM intent — evidence_id: EVID-015 — evidence_type: quote — source: kb-samples/strategy/product-strategy-2025.md
- Operator-only фичи без CISO-visible value — не core driver — signal: strong (internal strategy constraint) — evidence_id: EVID-016 — evidence_type: quote — source: kb-samples/strategy/product-strategy-2025.md

## Сигналы Confluence

- missing confluence evidence — Confluence local evidence missing

## Внешние рыночные сигналы

- skipped — user did not approve external research

## Inferred signals

- Операционная боль очереди существует в observed AppSec workflow, но как повторяющийся паттерн внутри одной KB-выборки, не как доказанный market category — signal: strong locally / none externally — basis: EVID-001, EVID-003, EVID-006, EVID-010, EVID-011
- Заявленный механизм «раньше скан → ниже production risk» не следует из локальных фактов — signal: strong contradiction — basis: EVID-009
- Ручная приоритизация без SoT критичности воспроизведёт Slack-эскалации внутри продукта — signal: moderate — basis: EVID-003, EVID-005, EVID-007
- Capability имеет шанс как governed workflow (policy + exceptions + audit trail), а не как standalone risk feature — signal: moderate — basis: EVID-007, EVID-008, EVID-012, EVID-015, EVID-016
- Имена Appscreener / Checkmarx в стратегии не являются внешним подтверждением спроса на queue prioritization — signal: none as market proof — basis: EVID-013 (internal positioning only)

## Сводка сигналов

- Overall local KB signal: strong
- Overall confluence signal: none
- Overall external signal: none
- Missing evidence:
  - Confluence / internal wiki
  - внешний рынок (не запрашивался)
  - telemetry wait time / time-to-remediate
  - win/loss, подтверждающие queue/workflow как purchase driver
  - интервью CISO и разработчика (в KB есть только excerpt AppSec Lead)
- Opportunity window: MEDIUM — операционная боль локально сильная; внешняя категория и risk-outcome не подтверждены
