# Decision Review

## Краткое резюме

Synthesis правильно ломает risk-framing и оставляет операционную боль. Это ещё не основание строить: локальный KB island узкий, голоса покупателя нет, внешний и Confluence каналы пустые. Рекомендация «reframe и валидировать» может быть слишком уверенной относительно качества выборки.

Уверенность: Средняя
Токен рекомендации: proceed_with_validation
Рекомендация: Продолжить с валидацией

## Оценка качества evidence

| Вывод | Сила evidence | Source artifact | Notes |
|-------|---------------|-----------------|-------|
| Очередь SAST создаёт многочасовое ожидание критичных проектов | Moderate | evidence_inventory.md (EVID-001, EVID-010) | Два источника одной demo-KB; нет telemetry и второй организации |
| Порядок очереди сейчас чинят в Slack без критериев и audit trail | Strong | evidence_inventory.md (EVID-003, EVID-007, EVID-008, EVID-011) | Воркшоп, transcript и whiteboard сходятся |
| Нет единого источника критичности | Strong | evidence_inventory.md (EVID-006, EVID-007); hypothesis_summary.md | Прямая речь оператора; гипотеза это игнорирует |
| Ручная приоритизация снизит production risk | Unsupported | evidence_inventory.md (EVID-009); hypothesis_map.md | Оператор явно не подтверждает; других фактов нет |
| Queue/workflow — способ выигрывать enterprise и land в GTM | Weak | business_context_analysis.md; EVID-012, EVID-013, EVID-015 | Это внутренний intent, не win/loss и не рынок |
| CISO не примет operator-only bump | Moderate | role_outputs/ciso.md; EVID-014, EVID-016 | Персона без интервью + strategy; прямого CISO-интервью нет |
| Боль очереди — рыночная категория | Unsupported | market_analysis.md | External skipped; Confluence missing; local ≠ market |
| Разработчики пострадают от непрозрачного bump | Weak | role_outputs/enterprise_developer.md | Только персона / ролевой анализ, EVID по разработчику нет |

## Скрытые допущения

| Assumption | Risk | Impact | Source artifact |
|------------|------|--------|-----------------|
| Demo-KB (воркшоп 2024 + один excerpt 2025-03) репрезентативна для mid/large AppSec | High | Пилот и roadmap на нетипичном аккаунте | discovery_preview.md; customer_discovery_plan.md |
| «Вручную приоритизировать» можно сделать не превратив продукт в Slack | High | Фича копирует workaround вместо его замены | EVID-003; hypothesis_map.md |
| Источник критичности появится «рядом» с очередью | High | Кнопка порядка без данных даст случайный FIFO+эскалации | EVID-006, EVID-007; customer_discovery_plan.md |
| Time-to-action достаточно как buyer metric | Medium | CISO всё равно спросит про риск и coverage — пилот не убедит | EVID-009, EVID-014; business_context_analysis.md |
| Hybrid policy+exceptions примут без отдельного GRC-проекта | Medium | Scope раздувается в «сервис-каталог + audit platform» | EVID-008; role_outputs/ciso.md |
| Пустой внешний канал можно игнорировать, потому что local strong | Medium | Overfit на внутреннюю боль, которую не покупают | market_analysis.md |

## Недостающие перспективы

- **CISO как респондент** — в RUN_DIR есть только слова AppSec Lead о CISO и strategy doc. Buyer Risk в CDP помечен HIGH; Decision Review не может считать governance-блокер доказанным, только правдоподобным.
- **Platform / DevOps** — ограничение гипотезы («сосуществовать с CI/CD») не проверено evidence. Bump очереди может упереться в квоты раннеров, а не в UX AppSec.
- **Compliance / audit** — EVID-008 ставит вопрос, но нет требований конкретного фреймворка (кто подписывает exception, какой retention лога).
- **Finance / procurement** — нет пути от Operational Driver к SKU / capacity pricing.
- **Второй AppSec Lead / другой аккаунт** — один transcript. Нельзя исключить, что в выборке просто слабый service catalog.

## Риски масштабирования

- 10 проектов: ручной порядок может работать у зрелой команды; bus-factor ещё терпим.
- 50 проектов: координация и «кто критичнее» без SoT становятся ежедневной политикой — это уже видно в Slack-модели (EVID-003, EVID-005).
- 100+ / enterprise: без policy default и audit trail CISO-персона и EVID-016 предсказывают отказ, но это не измерено.
- Скрытый scale-риск не в UI очереди, а в **данных критичности**: если SoT нет, масштабировать нечего, кроме эскалаций.

## Бизнес-риски

### False Positive Risk

Собрать manual queue bump, получить локальный кайф AppSec, не закрыть audit и не дать CISO метрику. Engineering effort уходит в operator-only фичу, которую стратегия сама маркирует как не core (EVID-016). Нарратив «снизим production risk» ещё и создаёт ложный success criterion.

### False Negative Risk

Отбросить queue/workflow целиком, потому что risk-framing мёртв, хотя GTM уже ставит queue management как land (EVID-015) и дифференциацию vs названных конкурентов (EVID-013). Конкуренты могут забрать workflow pain, пока мы спорим про production risk.

Асимметрия: false positive дороже в build-неделях; false negative дороже в позиционировании. Дешёвая валидация снимает оба, полный build — нет.

## Почему текущая рекомендация synthesis может быть неверной

1. «Боль подтверждена рынком» — в этом прогоне рынок не смотрели. Local KB island ≠ market. Если воркшоп — внутренняя лаборатория, Validated Opportunity схлопывается в Weak Signal.
2. Reframe на efficiency может быть удобным для команды и чужим для CISO: buyer всё ещё живёт в языке риска и audit. Тогда «правильный» нарратив тоже не продаётся без другой упаковки (governance), а не только смены слов.
3. Требование SoT критичности может оказаться большим проектом, чем очередь. Тогда гипотеза — неверный первый шаг: сначала каталог/tier, потом порядок сканов.
4. EVID-009 можно прочитать иначе: оператор не верит в risk, потому что его не измеряют, а не потому что связи нет. Пилот только с time-to-action эту альтернативу не убивает.

Опровержение proceed_with_validation: два интервью CISO + AppSec Lead в другом аккаунте, где очередь не болит или policy уже закрывает порядок — тогда additional_research или reject current framing полностью.

## План валидации

| Цель | Ожидаемое обучение | Effort |
|------|-------------------|--------|
| 5 интервью AppSec Engineer / Lead по последнему полному очереди дню | Есть ли SoT критичности; Slack-bump — норма или exception; wait time повторяется | Low |
| 3 разбора реальных queue workflows (экран + логи CI, не воспоминание) | Частота 4h+ wait, кто bump'ает, есть ли след решения | Low |
| Воркшоп 90 мин с CISO / Head of AppSec: policy default vs exception | Минимальный audit trail, который сделает manual bump приемлемым; купят ли efficiency-нарратив | Low |
| 4 интервью Enterprise Developer / EM про последний blocked/delayed scan | Fairness и эскалации — гипотеза ролей или факт | Low |
| Пилот на 1 mature account, 10–30 проектов, метрика time-to-first-finding и wait time по tier | Меняет ли порядок очереди операционный outcome | Medium |
| Не делать в этом цикле: production risk score, внешний market scan, build UI bump | Не закрывает HIGH unknowns дешевле интервью | — |

## Финальная рекомендация

**Продолжить с валидацией**, не full build и не «просто reframe в слайдах».

Уверенность средняя, не высокая: операционный workaround подтверждён несколькими артефактами одной KB, buyer и рынок — нет. Исходный claim про production risk отклонить как формулировку гипотезы до отдельных фактов. Не отклонять саму боль очереди.

Следующий шаг — дешёвый контур из CDP: SoT критичности, CISO на policy+exceptions, замеры time-to-action. Backlog commitment только если (a) критичность откуда-то берётся или её согласны завести, (b) CISO называет приемлемый exception model, (c) wait time воспроизводится вне demo-файлов. Иначе — additional_research, не build.
