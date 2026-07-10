# Illustration index

Матрица промптов → output files → документы → слайды.

## Tier A — README + Architecture

| ID | Prompt file | Output EN | Output RU | Used in |
|----|-------------|-----------|-----------|---------|
| A1 | [A1-architecture-overview.md](./tier-a-readme-architecture/A1-architecture-overview.md) | `assets/en/architecture-overview.svg` | `assets/ru/architecture-overview.png` | README, diagram.md, overview |
| A2 | [A2-pipeline-4-stages.md](./tier-a-readme-architecture/A2-pipeline-4-stages.md) | `assets/en/pipeline-4-stages.svg` | `assets/ru/pipeline-4-stages.png` | talk-outline §3, overview.ru |
| A3 | [A3-artifact-flow.md](./tier-a-readme-architecture/A3-artifact-flow.md) | `assets/en/artifact-flow.svg` | `assets/ru/artifact-flow.png` | README, diagram.md |
| A4 | [A4-signal-model.md](./tier-a-readme-architecture/A4-signal-model.md) | `assets/en/signal-model.svg` | `assets/ru/signal-model.png` | README Decision model |
| A5 | [A5-evidence-sources.md](./tier-a-readme-architecture/A5-evidence-sources.md) | `assets/en/evidence-sources.svg` | `assets/ru/evidence-sources.png` | diagram.md, quick-start |

## Tier B — Architecture deep-dive

| ID | Prompt file | Output EN | Output RU | Used in |
|----|-------------|-----------|-----------|---------|
| B1 | [B1-cline-execution.md](./tier-b-architecture-deep/B1-cline-execution.md) | `assets/en/cline-execution.svg` | `assets/ru/cline-execution.png` | README Cline, cline-contract |
| B2 | [B2-business-value-flow.md](./tier-b-architecture-deep/B2-business-value-flow.md) | `assets/en/business-value-flow.svg` | `assets/ru/business-value-flow.png` | business-context-layer |
| B3 | [B3-human-report-slice.md](./tier-b-architecture-deep/B3-human-report-slice.md) | `assets/en/human-report-slice.svg` | `assets/ru/human-report-slice.png` | README, demo-script |

## Tier C — Product Sense talk

| ID | Prompt file | Output RU (primary) | talk-outline | demo-script |
|----|-------------|---------------------|--------------|-------------|
| C1 | [C1-talk-hook-false-confidence.md](./tier-c-product-sense/C1-talk-hook-false-confidence.md) | `product-sense/assets/ru/talk-hook-false-confidence.svg` | §0 Зацепка | — |
| C2 | [C2-talk-rag-vs-pipeline.md](./tier-c-product-sense/C2-talk-rag-vs-pipeline.md) | `product-sense/assets/ru/talk-rag-vs-pipeline.svg` | §1 RAG | — |
| C3 | [C3-talk-llm-mistakes.md](./tier-c-product-sense/C3-talk-llm-mistakes.md) | `product-sense/assets/ru/talk-llm-mistakes.svg` | §6 Ошибки LLM | — |
| C4 | [C4-talk-framework-laws.md](./tier-c-product-sense/C4-talk-framework-laws.md) | `product-sense/assets/ru/talk-framework-laws.svg` | §7 Законы | — |
| C5 | [C5-talk-hr-pattern.md](./tier-c-product-sense/C5-talk-hr-pattern.md) | `product-sense/assets/ru/talk-hr-pattern.svg` | §4 HR demo | акты 1–4 context |
| C6 | [C6-talk-demo-report-map.md](./tier-c-product-sense/C6-talk-demo-report-map.md) | `product-sense/assets/ru/talk-demo-report-map.svg` | §4–5 | акты 1–6 |

## Talk-outline mapping

| talk-outline § | Recommended visuals | Prompt IDs |
|----------------|---------------------|------------|
| §0 Зацепка | False confidence | C1 |
| §1 RAG | RAG vs pipeline | C2 |
| §2 Идея стресс-теста | `идея → стресс-тест → решение` (text or mini A2) | A2 |
| §3 Конвейер 4 этапа | **Main stage diagram** | A2 |
| §4 HR demo | HR before/after + live human_report | C5, C6, B3 |
| §5 AppSec | example-001 human_report (screenshot, not prompt) | — |
| §6 Ошибки LLM | Three mistakes | C3 |
| §7 Законы | Seven laws poster | C4 |
| §8 Завершение | Text slide (no prompt) | — |

## Generation order (recommended)

1. A2 + C2 (establish visual language)
2. A1 + A3 + A4
3. C1, C3, C4, C5, C6
4. A5, B1, B2, B3

## After files exist

Update `<img src>` in:

- `README.md` → `assets/en/…`
- `README.ru.md` → `assets/ru/…`
- `architecture/diagram.md` / `diagram.ru.md`
- `product-sense/talk-outline.md` — add column «Файл слайда»

Legacy files until replaced: `assets/architecture-overview.svg`, `artifact-flow.svg`, `cline-workflow.svg`, `signal-model.svg`, `cline-mcp-confluence.svg`.
