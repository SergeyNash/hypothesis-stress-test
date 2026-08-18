# Customer Discovery Planning Layer

Customer Discovery Planning — **слой планирования исследования** после Synthesis и до Decision Review.

Он превращает неразрешённую неопределённость в практичный план customer-интервью.

---

## Назначение

Этот слой отвечает на вопрос:

> Что нам ещё нужно узнать, прежде чем принимать решение?

Он не валидирует гипотезы.

Он не принимает продуктовые решения и решения по backlog.

---

## Входы

Обязательно:

- `hypothesis_summary.md`
- `market_analysis.md`
- `hypothesis_map.md`
- `evidence_inventory.md`
- `business_context_analysis.md` или `missing_business_context.md`

Опционально:

- `validation_questions.md`
- `role_outputs/*`

Условие старта:

- `synthesis_complete.marker`

---

## Что производит слой

| Артефакт | Назначение |
|----------|------------|
| `customer_discovery_plan.md` | Практичный план исследования, готовый к интервью |
| `customer_discovery_planning_complete.marker` | Сигнал готовности к Decision Review |

---

## Основной процесс

1. Извлечь критические неизвестные из допущений, слабых сигналов, противоречий и отсутствующих доказательств.
   Отдельно сохранить пробелы Business Context как Business Value / Strategic Fit / Buyer Risk, не заполняя их предположениями.
2. Классифицировать неопределённость по типу риска:
   - Problem Risk
   - Frequency Risk
   - Severity Risk
   - Buyer Risk
   - Adoption Risk
   - Workflow Risk
   - Business Value Risk
   - Strategic Fit Risk
3. Превратить неизвестные в цели исследования.
4. Выбрать роли интервью, которые могут дать прямые доказательства.
5. Собрать interview guide, основанный на поведении.
6. Приоритизировать неизвестные по влиянию на решение (HIGH / MEDIUM / LOW).
7. Задать ожидаемые результаты обучения.

Слой использует только существующие Roles, Local Evidence, Business Context, Market и Synthesis артефакты. Он не выполняет новый retrieval/research, не создаёт новые evidence-сигналы и не выдаёт запланированную валидацию за проведённую.

---

## Правило интервью

Избегать вопросов про мнение, например:

- Вы бы этим пользовались?
- Вы бы это купили?
- Вам нужна эта фича?

Фокус на поведении, workflow, недавних событиях, ограничениях и реальных решениях.

---

## Связь с другими фазами

- Facilitator (Roles Layer) -> внутренний pressure test и заготовки вопросов для интервью
- Local Evidence -> существующие evidence и пробелы
- Business Context -> stakeholder/value flow, strategic fit или явный gap
- Market Layer -> внешние доказательства
- Synthesis -> карта противоречий и неизвестных
- **Customer Discovery Planning** -> план customer research
- Decision Review -> adversarial-критика и quality gate рекомендации
- Человек -> финальное решение по backlog
