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
    market_analysis.md
    hypothesis_map.md
    hypothesis_digest.txt
    decision_review.md
    *.marker
```

Шаблон имени `RUN_DIR`: `runs/HYP-YYYY-MM-DD-NNN/`

---

## Принцип

Каждый прогон должен быть:

* изолированным
* воспроизводимым
* трассируемым
