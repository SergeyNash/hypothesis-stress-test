# Заметки воркшопа — боль очереди сканов (2024)

Участники: 4 AppSec engineers, 1 AppSec lead

- «Критичные проекты ждут несколько часов перед сканированием, когда очередь заполнена»
- «Равное отношение к системам с разным риском — постоянная проблема»
- «Переставляем вручную через Slack, когда кто-то кричит громче всех»
- «Мы узнаём о перегрузке очереди только когда блокируется релиз»

Whiteboard: FIFO queue → manual reorder → «кто критичнее?» — нет единых критериев

## Цитаты

> Critical projects wait several hours before scanning when the queue is full.

> We only learn about queue backlog when a release is blocked.
