# C2 Talk — RAG vs stress-test pipeline

## Meta

| Поле | Значение |
|------|----------|
| Target output RU | `product-sense/assets/ru/talk-rag-vs-pipeline.svg` |
| Canvas | 1920×1080 |
| Tier | C |
| Talk section | §1 Почему RAG не принимает решения (5 min) |

## Purpose

Контраст: один чат (смешивает всё) vs 4-этапный конвейер (разделяет ответственность).

## Composition

Two columns:

**Left — "One chat"** gray, single large box "Ask LLM" with messy arrows inside to mixed labels: opinions, market, strategy, roles — all tangled

**Right — "Stress test"** use A2 four blocks miniature version, clean horizontal

Bottom line: RAG finds documents · Stress test reduces uncertainty

## Labels RU

Один чат · Смешивает роли и рынок · Стресс-тест · 4 этапа · RAG находит документы · Снижает неопределённость

## Generation prompt (copy-paste)

```
1920x1080 conference comparison slide, flat minimal.

Title RU: "Почему RAG не принимает продуктовые решения"

Two equal columns:

LEFT header gray #F1F5F9 "Один чат" — one big box "Запрос к LLM" with tangled internal arrows connecting messy labels "мнения" "рынок" "стратегия" "роли" — visual chaos but simple line art

RIGHT header white "Стресс-тест" — clean 4-block mini pipeline (use blue/sky/purple/yellow semantic colors): Разделить POV → Найти evidence → Столкнуть → Следующий шаг

Footer full width: left text "RAG находит документы" | right bold "Снижает неопределённость"

No gradients. Russian labels. High contrast.
```

## Post-generation checklist

- [ ] Right column matches A2 visual language
- [ ] Left column looks "messy" not "evil"
