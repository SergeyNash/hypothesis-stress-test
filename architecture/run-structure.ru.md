Язык: [English](./run-structure.md) | **Русский**

# Структура RUN_DIR

Каждый прогон гипотезы следует стандартной структуре архива:

```text
RUN_DIR/
  input/
    hypothesis.md
    attachments/
  run.md
  outputs/
    role_outputs/
    hypothesis_summary.md
    validation_questions.md
    discovery_preview.md
    evidence_inventory.md
    market_analysis.md
    hypothesis_map.md
    hypothesis_digest.txt
    customer_discovery_plan.md
    decision_review.md
    human_report.html
    knowledge_retrieval_complete.marker
    *.marker
```

Шаблон имени `RUN_DIR`: `runs/HYP-YYYY-MM-DD-NNN/`

---

## Принцип

Каждый прогон должен быть:

* изолированным
* воспроизводимым
* трассируемым
