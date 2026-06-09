Язык: [English](./confluence-mcp.md) | **Русский**

# Настройка Confluence MCP

Confluence — **основной MCP-источник** local signals для Market Layer.

## Почему Confluence первым

Внутренний Confluence часто содержит:

- Реальные проблемы пользователей и заметки discovery
- Прошлые продуктовые решения
- Архитектурные ограничения
- Артефакты customer research
- Исторические обсуждения гипотез

Это надёжнее внешних источников для **local signals**.

## Рекомендуется: Atlassian Rovo MCP Server (официальный)

Для **Confluence Cloud** с OAuth 2.1:

### Требования

- Atlassian Cloud с Confluence
- Node.js 18+ (для прокси `mcp-remote`)
- Расширение Cline в VS Code

### Настройка в Cline

1. Панель Cline → иконка **MCP Servers** (стопка серверов в тулбаре).
2. Вкладка **Configure** → **Configure MCP Servers**.
3. Добавьте удалённый сервер Atlassian:

```json
{
  "mcpServers": {
    "atlassian": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote@latest",
        "https://mcp.atlassian.com/v1/mcp/authv2"
      ],
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

4. Перезапустите MCP-сервер и пройдите OAuth в браузере.
5. Убедитесь, что инструменты поиска/чтения Confluence появились в списке.

> **Важно:** используйте endpoint `https://mcp.atlassian.com/v1/mcp/authv2` (не устаревший `/sse`).

Документация: [Atlassian Rovo MCP Server](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/)

## Альтернатива: community Confluence MCP (API token)

Если OAuth недоступен — community-сервер с API token.

### Пример: mcp-atlassian

```json
{
  "mcpServers": {
    "mcp-atlassian": {
      "command": "uvx",
      "args": ["mcp-atlassian"],
      "env": {
        "CONFLUENCE_URL": "https://your-company.atlassian.net/wiki",
        "CONFLUENCE_USERNAME": "your.email@company.com",
        "CONFLUENCE_API_TOKEN": "your_api_token"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

API token: Atlassian Account Settings → Security → API tokens.

Документация: [mcp-atlassian](https://github.com/sooperset/mcp-atlassian)

### Server / Data Center

Используйте Personal Access Token (PAT) вместо username + API token. См. документацию вашего MCP-сервера.

## Как Market Layer использует Confluence

При запуске Market Layer (skill `hypothesis-market-layer` или `/run-market-layer.md`):

1. Ищите в Confluence страницы по:
   - домену и сценарию гипотезы
   - похожим проблемам и прошлым инициативам
   - user research и обратной связи
   - архитектурным и процессным ограничениям

2. Для каждого finding записывайте в `market_analysis.md`:

```markdown
## Local Signals (Confluence)

- [описание finding]
  - signal: strong | weak | none
  - type: local
  - source: [Page Title](https://your-site.atlassian.net/wiki/spaces/...)
```

3. Если релевантных страниц нет — явно укажите:

```markdown
## Local Signals (Confluence)

No relevant local evidence found.

- signal: none
- note: Confluence search returned no matches for [query terms]
```

## Без Confluence MCP

Market Layer может работать, но обязан зафиксировать:

```markdown
## MCP Status
Confluence MCP: not configured

## Local Signals (Confluence)
missing local evidence — MCP not available
```

Не выдумывайте внутренние знания. External signals — только с одобрения пользователя.

## Безопасность

| Правило | Детали |
|---------|--------|
| Credentials | Только env или конфиг Cline MCP — не коммитить в репозиторий |
| autoApprove | Только для read-only search/get операций |
| Permissions | MCP уважает существующие права доступа в Confluence |
| Write tools | Отключить или не auto-approve для аналитических прогонов |

## Вторичные MCP-источники (будущее)

Опциональные расширения, не обязательны для v1:

- Jira / Linear — связанные задачи
- Slack — неформальные обсуждения
- Web search — внешние market signals
- Filesystem — локальные артефакты репозитория

Confluence остаётся основным источником local signals.
