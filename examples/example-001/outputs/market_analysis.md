# Анализ рынка

## Статус MCP

Confluence MCP: не настроен (example run — без live Confluence search)

## Локальные сигналы из базы знаний

- Критичные проекты испытывают multi-hour задержки в очереди сканов
  - signal: strong
  - type: local
  - evidence: EVID-001, EVID-004
  - source: `workshop_queue.md`, `whiteboard_scan_queues.txt`

- О перегрузке очереди узнают только когда блокируется release
  - signal: medium
  - type: local
  - evidence: EVID-002
  - source: `workshop_queue.md`

- Business-critical apps не приоритизируются автоматически в текущем workflow
  - signal: strong
  - type: local
  - evidence: EVID-003
  - source: `2025-03-appsec-interview-excerpt.md`

- Для tier-1 / escalated apps нужен ручной flagging
  - signal: medium
  - type: local
  - evidence: EVID-001, EVID-003
  - note: tribal knowledge и Slack-driven reordering в источниках

## Сигналы Confluence

missing confluence evidence — example artifacts; для live runs настройте Confluence MCP

## Внешние рыночные сигналы

- Pipeline blocking friction в CI/CD security gates
  - signal: strong
  - type: external
  - source: industry pattern (SAST в CI/CD)

- SAST false positives и adoption failure
  - signal: strong
  - type: external
  - source: developer friction с security tools

- Risk-based prioritization как признанный market pattern
  - signal: strong
  - type: external
  - source: vendor landscape (Snyk, GitHub Advanced Security, Checkmarx)

- Scan queue prioritization как standalone problem category
  - signal: weak
  - type: external
  - note: не установлена как отдельная рыночная категория

## Inferred signals

- Security vs Delivery conflict структурен в enterprise AppSec
  - signal: strong
  - type: inferred
  - basis: EVID-002 + external pipeline friction

- Проблемы scalability ручной приоритизации на enterprise scale
  - signal: medium
  - type: inferred
  - basis: EVID-003 + trend policy-automation

## Ключевые стейкхолдеры

| Роль | Тип |
|------|-----|
| CISO | Buyer |
| AppSec Engineer | Primary user |
| Platform / DevOps | Operational owner |
| Enterprise Developer | Secondary user |

## Существующие рыночные решения

* Risk-Based Prioritization
* AI-Assisted Triage
* Developer Feedback Loops
* Policy-Based Automation
* Vendor-specific (Snyk, GitHub Advanced Security, Checkmarx)

## Пробелы в существующих подходах

* Нет гибкой приоритизации scan queue
* Конфликт Security vs Delivery
* Scalability issues ручной приоритизации
* Непрозрачные критерии приоритизации
* Зависимость от business context
* Adoption важнее detection quality

## Сводка сигналов

- Local KB signal: strong (4 extractable items)
- Confluence signal: none
- External signal: strong (related problems), weak (standalone queue prioritization)
- Missing evidence: Confluence research; full audio transcript (EVID-005 metadata only)
- Opportunity window: MEDIUM–HIGH
