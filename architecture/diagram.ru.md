Язык: [English](./diagram.md) | **Русский**

# Диаграммы архитектуры

## Общий вид системы

<p align="center">
  <img src="../assets/architecture-overview.svg" width="760"/>
</p>

Слои фреймворка (Roles → Market → Synthesis → Decision Review) с адаптером Cline и Confluence MCP для local signals.

## Поток артефактов

<p align="center">
  <img src="../assets/artifact-flow.svg" width="820"/>
</p>

Как `hypothesis.md` превращается в структурированные артефакты решения через Cline skills и workflows.

## Поток выполнения Cline

<p align="center">
  <img src="../assets/cline-workflow.svg" width="800"/>
</p>

Rules, skills, workflows и Confluence MCP на пути выполнения.

## Модель сигналов

<p align="center">
  <img src="../assets/signal-model.svg" width="660"/>
</p>

Пять паттернов synthesis на основе столкновения внутренних и внешних сигналов (включая Local Optimization Trap).

## Интеграция Confluence MCP

<p align="center">
  <img src="../assets/cline-mcp-confluence.svg" width="700"/>
</p>

Confluence как основной источник local signals для Market Layer.
