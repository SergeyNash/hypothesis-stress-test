# Decision Review

Decision Review — **adversarial gate** после Customer Discovery Planning.

Он не переанализирует гипотезу. Он оспаривает выводы, которые фреймворк уже произвёл.

---

## Назначение

Работать как независимый ревьюер. Выявлять:

- слабые доказательства
- избыточную уверенность
- необоснованные выводы
- скрытые допущения
- пробелы в рассуждении
- confirmation bias
- отсутствующую валидацию
- упущенные риски

Цель: повысить качество решения до того, как гипотеза попадёт в планирование backlog или реализацию.

---

## Ключевой принцип

Исходите из того, что текущий вывод может быть неверным.

Ваша задача — не поддержать рекомендацию.

Ваша задача — найти, почему рекомендация может провалиться.

---

## Входы

Обязательно:

- `input/hypothesis.md`
- `hypothesis_summary.md`
- `market_analysis.md`
- `hypothesis_map.md`

Опционально:

- `role_outputs/*`
- `hypothesis_digest.txt`
- `customer_discovery_plan.md`

---

## Процесс ревью

1. **Оценить качество доказательств** — классифицировать каждый крупный вывод: Strong / Moderate / Weak / Unsupported
2. **Найти скрытые допущения** — что должно быть истинным, чтобы гипотеза сработала?
3. **Искать отсутствующие перспективы** — finance, compliance, operations, platform-команды и т.д.
4. **Оценить масштабируемость** — на масштабе 10 / 50 / 100 / enterprise
5. **Оценить бизнес-риск** — риск false positive и false negative
6. **Оспорить рекомендацию** — активно пытаться её опровергнуть
7. **Спроектировать самую дешёвую валидацию** — максимум обучения на единицу усилий

---

## Output

`outputs/decision_review.md`

### Структура

- Executive Summary (confidence: High / Medium / Low; recommendation: Proceed / Proceed with Validation / Additional Research Required / Reject)
- Evidence Quality Review (таблица)
- Hidden Assumptions (таблица)
- Missing Perspectives
- Scalability Risks
- Business Risks (false positive / false negative)
- Validation Plan
- Final Recommendation

---

## Правила ревью

- Никогда не повторять synthesis
- Никогда не суммировать уже существующие outputs
- Всегда добавлять новое критическое мышление
- Всегда искать слабые места
- Всегда исходить из того, что неопределённость есть
- Если слабых мест нет, явно объяснить, почему уверенность высокая

---

## Связь с другими фазами

- Roles Layer → внутренние сигналы
- Market Layer → внешние сигналы
- Synthesis Layer → классификация конфликтов
- Customer Discovery Planning → план обучения через интервью
- **Decision Review** → adversarial-критика выводов synthesis
- **Человек** → решение по backlog

Decision Review не вводит новые данные. Критикует только уже существующие артефакты.

---

## Дальше

- `templates/decision-review-prompt.md` — ручной запуск
- `.cline/skills/hypothesis-decision-review/SKILL.md` — запуск в Cline
- `playbooks/run-hypothesis.md` — полный пайплайн
