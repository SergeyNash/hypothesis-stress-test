# Диаграммы архитектуры

## Общий вид системы

<p align="center">
  <img src="../assets/ru/architecture-overview.png" width="760"/>
</p>

Полный конвейер v2.4: от гипотезы и бизнес-контекста до артефактов и решения человека.

## Конвейер — 4 этапа

<p align="center">
  <img src="../assets/ru/pipeline-4-stages.png" width="760"/>
</p>

Упрощённая схема для сцены и быстрого объяснения: разделить POV → найти evidence → столкнуть сигналы → сформировать следующий шаг.

## Поток артефактов

<p align="center">
  <img src="../assets/ru/artifact-flow.png" width="820"/>
</p>

Как `input/hypothesis.md` превращается в структурированные артефакты решения через Cline skills и workflows.

Mermaid и таблица «кто пишет / кто читает»: [artifact-lifecycle.md](./artifact-lifecycle.md).

## Поток выполнения Cline

<p align="center">
  <img src="../assets/ru/cline-execution.png" width="800"/>
</p>

Правила, сценарий, навыки и MCP: Cline выполняет конвейер и сохраняет трассируемые артефакты.

## Поток бизнес-ценности

<p align="center">
  <img src="../assets/ru/business-value-flow.png" width="760"/>
</p>

Слой Business Context: от широкой идеи к проверяемой гипотезе с бизнес-рамкой. См. [layers/business-context-layer.md](../layers/business-context-layer.md).

## Модель сигналов

<p align="center">
  <img src="../assets/ru/signal-model.png" width="660"/>
</p>

Пять паттернов synthesis на основе столкновения внутренних и внешних сигналов (включая Local Optimization Trap).

## Срез human_report

<p align="center">
  <img src="../assets/ru/human-report-slice.png" width="760"/>
</p>

Как артефакты прогона собираются в `human_report.html` для принятия решения человеком.

## Источники доказательств

<p align="center">
  <img src="../assets/ru/evidence-sources.png" width="760"/>
</p>

Локальные и внешние источники evidence: Confluence, база знаний, интервью, рынок — в пул проверяемых наблюдений для Market Layer.
