# Негативные фикстуры

Неполные или намеренно сломанные `RUN_DIR` для `scripts/validate_runs.py`.
Ожидаемые ошибки заданы в `manifest.json`.

| Фикстура | Что проверяет |
|----------|----------------|
| `vague-statement` | `VAGUE_STATEMENT` |
| `id-mismatch` | `RUN_DIR_ID_MISMATCH` |
| `missing-marker` | Market без Business Context marker |
| `empty-kb` | пустой inventory допустим, но preview обязан существовать |
| `mcp-unavailable` | Market без Confluence, MCP status |
| `external-research-declined` | External channel skipped |
