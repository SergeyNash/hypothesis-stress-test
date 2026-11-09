# Local Evidence Discovery

Local Evidence Discovery — шаг retrieval до Market Layer.

Собирает трассируемые локальные доказательства из неструктурированной KB и пишет структурированные retrieval-артефакты.

---

## Назначение

Отделить retrieval от анализа:

- Discovery собирает evidence.
- Market Layer интерпретирует его.
- Synthesis сталкивает интерпретации.

Так retrieval не превращается в мини-Market Layer.

---

## Входы

Обязательно:

- `RUN_DIR/input/hypothesis.md`

Опционально:

- `RUN_DIR/outputs/hypothesis_summary.md`

---

## Outputs

- `RUN_DIR/outputs/discovery_preview.md`
- `RUN_DIR/outputs/evidence_inventory.md`
- `RUN_DIR/outputs/knowledge_retrieval_complete.marker`

---

## Базовые правила

- один evidence item = один атомарный сигнал
- без синтеза в наблюдениях
- нет evidence → нет утверждения
- сохранять трассируемость источника

---

## Guardrails V1

- ограниченный scan и extraction
- whitelist расширений
- PDF/DOCX/XLSX/HTML читаются штатными readers; пропускаются только неподдерживаемые форматы с причиной
- явные причины skip
- preview всегда создаётся первым
- extraction продолжается автоматически после preview
- перед отбором документов строится рекурсивный каталог; названия тематических вложенных папок учитываются до исключения родителя
- после inventory — проверка полноты с пользователем; marker создаётся после принятия или явно заданного пропуска паузы

---

## Связь с Market Layer

Market Layer читает `evidence_inventory.md` как вход локальных доказательств.

В market output каналы разделены:

- Local Signals from Knowledge Base
- Confluence Signals
- External Market Signals
- Inferred Signals

---

## Non-goals

- не чатбот по документам
- не полнотекстовый semantic search по всему vault
- не движок scoring уверенности источников

## Service-business profile

For service_business apply **Evidence** from [service-business.md](../profiles/service-business.md). This extends the current phase without adding a parallel pipeline. Existing digital_product runs keep their contract.
