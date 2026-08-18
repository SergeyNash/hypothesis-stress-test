# Персоны

Персоны — синтезированные профили ролей, которые использует Roles Layer.

Это не сырые доказательства. Персона должна суммировать повторяющиеся паттерны из интервью, заметок customer discovery, внутренних исследований и экспертизы в домене.

## Контракт

Каждый файл персоны должен содержать frontmatter:

```yaml
persona: Application Security Engineer
slug: application-security-engineer
source_status: initial_profile | custdev_backed | mixed
source_interviews: []
last_updated: YYYY-MM-DD
confidence: low | medium | high
```

## Правило доказательств

Если `source_interviews` пуст, считайте персону слабым локальным сигналом.

Если персона опирается на связанные интервью или research-заметки, цитируйте эти источники в Market Layer и Decision Review, когда это уместно.

## Связь с интервью

- `knowledge-base/interviews/` хранит сырые CustDev-материалы и материалы интервью.
- `knowledge-base/persona-builds/` документирует, как персоны пересобирались из доказательств интервью.
- `knowledge-base/personas/` хранит текущие переиспользуемые артефакты персон.
