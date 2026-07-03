# HUMANIZER CORE

This document adapts Russian writing rules from
[`humanizer-ru`](https://github.com/SergeNS-mne/humanizer-ru) into a portable
Russian humanizer reference.

It is project-neutral. It does not define research method, product strategy,
platform formats, or the voice of a specific author. Project-specific style
rules should be added through adapters.

---

## 1. Purpose

`HUMANIZER_CORE.md` helps remove:

- generic AI rhythm;
- bureaucratic Russian;
- translated English syntax;
- inflated importance;
- promotional gloss;
- sterile structure;
- typographic markers of generated text;
- weak communication artifacts.

The goal is not to make text messy. The goal is to make it sound like a smart
person with a real point, not like a polished generic assistant.

---

## 2. Core Priority

Apply style rules in this order:

1. preserve the meaning of the source text;
2. preserve the author's or project's voice if it is known;
3. apply the selected mode from `MODES.md`;
4. apply this core humanizer layer;
5. adapt to the final medium.

If a humanizer rule would weaken the thought, ignore the rule.

If a text is empty by meaning, do not make it sound deep. Mark the weak place
or ask for missing context.

---

## 3. Modes

Use the same rules with different strictness depending on the text mode.
Detailed modes live in `MODES.md`.

Supported v0.1 modes:

- `general`;
- `product_content`;
- `fiction`;
- `business`;
- `essay`;
- `chat_reply`.

---

## 4. Humanizer Rule Template

Each rule follows the same logic:

```text
Signal:
Why it is weak:
Rewrite principle:
Bad:
Better:
Exceptions:
```

Exceptions are deliberate. They are not permission to keep lazy phrasing.

---

## 5. Content Patterns

### Rule 1. Era Cliches

Signal: "в современном мире", "в эпоху цифровой трансформации", "сегодня как
никогда", "технологии не стоят на месте".

Why it is weak: the text starts from atmosphere instead of tension.

Rewrite principle: begin with a concrete artifact, decision, conflict, or
work situation.

Bad:

```text
В современном мире технологии не стоят на месте.
```

Better:

```text
Git интересен не как ещё один инструмент разработки, а как система, которая
сделала промежуточное состояние нормальной частью работы.
```

Exceptions: acceptable only in historical context if the phrase names a
specific period and the next sentence gives evidence.

### Rule 2. Inflated Importance

Signal: "меняет правила игры", "революция", "прорыв", "новая эра", "важный
урок для всех".

Why it is weak: big words hide the mechanism.

Rewrite principle: say what changed in behavior, cost, risk, or coordination.

Bad:

```text
Этот подход меняет правила игры для команд.
```

Better:

```text
Команде стало дешевле проверить идею и вернуться назад, если решение оказалось
неудачным.
```

Exceptions: use large claims only when the text has already earned them.

### Rule 3. Promotional Gloss

Signal: "бесшовный опыт", "интуитивный интерфейс", "на одной странице",
"простое и удобное решение".

Why it is weak: product value becomes brochure language.

Rewrite principle: replace gloss with the user's job and the friction that
became smaller.

Bad:

```text
Пользователь получает бесшовный опыт на одной странице.
```

Better:

```text
Пользователю не нужно держать в голове три разных состояния заявки и искать,
где именно процесс застрял.
```

Exceptions: acceptable only when quoting actual product copy.

### Rule 4. False Scale

Signal: "каждая команда", "любой лидер", "все продукты", "никто не спорит".

Why it is weak: certainty appears before evidence.

Rewrite principle: narrow the claim to the actual audience or system.

Bad:

```text
Каждая продуктовая команда должна думать так.
```

Better:

```text
Это особенно заметно в командах, где решение проходит через продажи,
поддержку, разработку и релизную коммуникацию.
```

Exceptions: universal claims require strong evidence or a clearly framed
principle.

### Rule 5. Generic Lessons

Signal: "главный урок", "важный вывод", "что нужно запомнить".

Why it is weak: the ending sounds packaged.

Rewrite principle: end with a principle connected to the investigation.

Bad:

```text
Главный урок: командам нужно быть эффективнее.
```

Better:

```text
Поведение команды меняется не от лозунга про эффективность, а от стоимости
обычных действий: попробовать, ошибиться, откатиться, объяснить клиенту пользу.
```

Exceptions: short educational formats may use explicit lessons if they are
concrete.

---

## 6. Language Patterns

### Rule 6. Bureaucratic Nouns

Signal: "осуществление", "реализация", "использование возможностей",
"обеспечение качества".

Why it is weak: nouns hide who does what.

Rewrite principle: use verbs and actors.

Bad:

```text
Реализация проверки обеспечивает повышение качества релиза.
```

Better:

```text
Команда проверяет риск раньше и реже чинит решение в последний момент.
```

Exceptions: legal, compliance, or formal policy documents may need nouns.

### Rule 7. Genitive Chains

Signal: long chains like "улучшение качества процесса управления релизами".

Why it is weak: the reader must unpack the sentence backward.

Rewrite principle: split the chain into a subject and action.

Bad:

```text
Улучшение качества процесса подготовки релизной коммуникации...
```

Better:

```text
Команда раньше готовит релизную коммуникацию и быстрее замечает, где не может
объяснить ценность клиенту.
```

Exceptions: short technical terms may stay intact.

### Rule 8. "Является"

Signal: "является важным", "является причиной", "является инструментом".

Why it is weak: the verb usually adds no meaning.

Rewrite principle: use a direct verb or simple predicate.

Bad:

```text
Продукт является решением проблемы.
```

Better:

```text
Продукт решает эту проблему.
```

Exceptions: definitions may use it sparingly.

### Rule 9. "Данный"

Signal: "данный подход", "данная проблема", "данный инструмент".

Why it is weak: it sounds bureaucratic and distant.

Rewrite principle: use "этот", name the object, or remove the word.

Bad:

```text
Данный подход является эффективным.
```

Better:

```text
Этот подход работает, если команда видит риск до разработки.
```

Exceptions: formal specs may use "данный" when precision matters.

### Rule 10. Passive Without Need

Signal: "было принято решение", "была проведена проверка", "был создан
процесс".

Why it is weak: responsibility disappears.

Rewrite principle: name the actor when it matters.

Bad:

```text
Было принято решение перенести проверку на конец релиза.
```

Better:

```text
Команда перенесла проверку на конец релиза и слишком поздно увидела риск.
```

Exceptions: use passive when actor is unknown or irrelevant.

### Rule 11. Extra "который"

Signal: sentences chained by several "который".

Why it is weak: the sentence becomes heavy and procedural.

Rewrite principle: split, replace with participle only if natural, or use a
direct verb.

Bad:

```text
Команда, которая пишет релиз-ноты, которые должны объяснить ценность...
```

Better:

```text
Команда пишет релиз-ноты и пытается объяснить ценность клиенту.
```

Exceptions: keep "который" when it prevents ambiguity.

### Rule 12. AI Vocabulary

Signal: "важно отметить", "стоит подчеркнуть", "в конечном итоге", "как
показывает практика".

Why it is weak: signposting replaces thought.

Rewrite principle: remove the phrase or make the point directly.

Bad:

```text
Важно отметить, что Git снизил цену эксперимента.
```

Better:

```text
Git снизил цену эксперимента.
```

Exceptions: useful in long essays when guiding the reader through structure.

### Rule 13. English-Calque Explanations

Signal: "это про", "не просто", "может привести к", "играет роль в том, чтобы".

Why it is weak: Russian sentence copies English logic.

Rewrite principle: use causal Russian prose and concrete work context.

Bad:

```text
Это не про скорость, это про качество решений.
```

Better:

```text
Скорость здесь вторична. Команде важнее увидеть риск достаточно рано, пока
решение ещё можно изменить без большой политической цены.
```

Exceptions: spoken emphasis may stay if it appears once and earns its place.

### Rule 14. Rule of Three

Signal: "быстро, удобно и безопасно"; "ясно, просто и эффективно".

Why it is weak: generic triads sound polished but empty.

Rewrite principle: keep only the specific words or replace with a concrete
effect.

Bad:

```text
Решение стало быстрым, удобным и надёжным.
```

Better:

```text
Пользователь стал видеть статус заявки сразу, без переписки с поддержкой.
```

Exceptions: rhetorical triads are acceptable when they are concrete and not
stock phrases.

### Rule 15. Synonym Cycle

Signal: several nearby words mean almost the same thing: "важный, значимый,
ключевой".

Why it is weak: the text increases volume without increasing meaning.

Rewrite principle: choose one word or explain the difference.

Bad:

```text
Это важный, значимый и ключевой сигнал.
```

Better:

```text
Это сигнал: команда не может объяснить клиентскую пользу решения.
```

Exceptions: useful only when each word marks a different dimension.

### Rule 16. Hedge Fog

Signal: "возможно", "может быть", "как бы", "в некотором смысле" repeated.

Why it is weak: uncertainty becomes fog instead of honest limitation.

Rewrite principle: state what is known, then name the limit.

Bad:

```text
Возможно, в некотором смысле это может быть полезным.
```

Better:

```text
Это полезно как рабочая гипотеза, но пока не как доказанный вывод.
```

Exceptions: unfinished research may keep visible uncertainty, but it should be
legible.

### Rule 17. Exaggeration by Adverb

Signal: "абсолютно", "полностью", "кардинально", "радикально" without proof.

Why it is weak: adverb compensates for weak evidence.

Rewrite principle: remove the adverb or show the mechanism.

Bad:

```text
Git радикально изменил работу команд.
```

Better:

```text
Git сделал ветвление и откат обычными действиями, а не отдельным событием.
```

Exceptions: keep if the claim is historically supported and explained.

### Rule 18. Abstract "эффективность"

Signal: "повысить эффективность", "работать эффективнее".

Why it is weak: efficiency is not a job or mechanism.

Rewrite principle: say which cost, delay, risk, or coordination step changed.

Bad:

```text
Команда стала эффективнее.
```

Better:

```text
Команда стала меньше спорить о промежуточных изменениях, потому что их стало
проще показать, обсудить и откатить.
```

Exceptions: metrics discussion may use the word after defining it.

### Rule 19. Unclear "система"

Signal: "система работает", "система помогает", with no boundary.

Why it is weak: the reader does not know what system means.

Rewrite principle: name the actors, rules, tools, and feedback loop.

Bad:

```text
Система помогает команде быстрее двигаться.
```

Better:

```text
Команда видит изменение в коде, обсуждает его в ревью и может вернуться к
предыдущему состоянию без большого конфликта.
```

Exceptions: use "system" after defining the system boundary.

### Rule 20. Nominalized "возможность"

Signal: "даёт возможность осуществлять", "позволяет производить".

Why it is weak: the sentence becomes longer than the action.

Rewrite principle: use "может" or a direct verb.

Bad:

```text
Инструмент даёт возможность осуществлять откат изменений.
```

Better:

```text
Инструмент позволяет откатить изменение.
```

Exceptions: keep when discussing capability as a product concept.

---

## 7. Style Patterns

### Rule 21. Bold as Meaning

Signal: many bold phrases in a short post.

Why it is weak: formatting tries to create importance.

Rewrite principle: make the sentence carry the point.

Bad:

```markdown
**Главное:** команда должна **раньше** видеть **ценность**.
```

Better:

```text
Команда должна видеть ценность до разработки, иначе релиз-ноты становятся
поздней попыткой найти смысл в уже готовой работе.
```

Exceptions: use bold for navigation in long documents, not emotional pressure.

### Rule 22. Emoji as Tone

Signal: emojis used to make text warmer or more energetic.

Why it is weak: tone becomes decoration.

Rewrite principle: remove emojis unless the platform and author voice truly
need them.

Bad:

```text
Вот почему это важно 🚀
```

Better:

```text
Вот почему это важно для команды, которая выпускает продукт под давлением
сроков.
```

Exceptions: use emojis only when they are natural for the project, platform,
and author voice.

### Rule 23. Lists Without Reason

Signal: many bullets where prose would be more natural.

Why it is weak: structure replaces reasoning.

Rewrite principle: turn repeated questions or parallel claims into a paragraph.

Bad:

```text
Сколько стоит проверить гипотезу?
Сколько стоит откатить решение?
Сколько стоит признать ошибку?
```

Better:

```text
Git интересен тем, что меняет цену обычных действий: проверить гипотезу,
откатить решение, признать ошибку и не превратить её в событие для всей
команды.
```

Exceptions: checklists and reference docs may use lists.

### Rule 24. Fragment Headers Inside Prose

Signal: "Скорость:", "Качество:", "Главное:" as sentence starters.

Why it is weak: the post sounds like slide notes.

Rewrite principle: write the relation in a sentence.

Bad:

```text
Скорость: продукт работает быстрее.
```

Better:

```text
Скорость важна только тогда, когда пользователь быстрее завершает свою работу.
```

Exceptions: acceptable in compact checklists.

### Rule 25. Short Dramatic Fragments

Signal: "И всё.", "Вот так.", "Это правда.", "Особенно здесь."

Why it is weak: creates artificial drama.

Rewrite principle: connect the fragment to the surrounding thought.

Bad:

```text
Это правда. Особенно GitHub.
```

Better:

```text
GitHub усилил распространение Git, но не объясняет, почему сам Git оказался
удобной основой для повседневной работы.
```

Exceptions: one fragment may work as a spoken beat in a short post, chat reply,
or dialogue.

---

## 8. Typography

### Rule 26. Dash Overload

Signal: several em dashes or parenthetical dashes per paragraph.

Why it is weak: text starts to sound like generated explanatory prose.

Rewrite principle: use periods, commas, or split the thought.

Bad:

```text
Git — это инструмент — который изменил работу — потому что снизил цену ошибки.
```

Better:

```text
Git изменил работу команды, потому что снизил цену ошибки.
```

Exceptions: one dash can clarify a real aside.

### Rule 27. Semicolon

Signal: semicolon in conversational Russian.

Why it is weak: often sounds translated or overly formal.

Rewrite principle: split the sentence or use a comma.

Bad:

```text
Решение простое; код сразу заработает.
```

Better:

```text
Решение простое, и код сразу заработает.
```

Exceptions: long essays may use semicolons sparingly.

### Rule 28. Inline Colon

Signal: "Скорость: ...", "Вывод: ...", "Проблема: ...".

Why it is weak: reads like a generated outline.

Rewrite principle: use a normal sentence.

Bad:

```text
Вывод: команда увидела риск поздно.
```

Better:

```text
Команда увидела риск поздно, поэтому любое исправление стало дорогим.
```

Exceptions: acceptable in notes, not polished public prose.

### Rule 29. Quotation Marks as Distance

Signal: too many quoted everyday words.

Why it is weak: the author sounds detached from their own language.

Rewrite principle: quote only actual terms, interface labels, or speech.

Bad:

```text
Команда пытается объяснить "ценность" "фичи".
```

Better:

```text
Команда пытается объяснить ценность изменения для клиента.
```

Exceptions: use quotes for actual user language or suspicious terms.

### Rule 30. Letter Ё

Signal: inconsistent "е/ё" in words where ambiguity matters.

Why it is weak: inconsistency distracts in edited text.

Rewrite principle: use "ё" when ambiguity or readability matters; otherwise be
consistent inside one document.

Bad:

```text
Все поймут, что все уже готово.
```

Better:

```text
Все поймут, что всё уже готово.
```

Exceptions: follow publication platform conventions if they are explicit.

---

## 9. Communication Artifacts

### Rule 31. "Надеюсь, это помогло"

Signal: assistant-style closing.

Why it is weak: it breaks author voice.

Rewrite principle: remove it.

Bad:

```text
Надеюсь, это помогло.
```

Better:

```text
```

Exceptions: direct support messages may use it.

### Rule 32. Sycophancy

Signal: "отличный вопрос", "вы абсолютно правы", "гениальная мысль".

Why it is weak: the text performs agreement instead of thinking.

Rewrite principle: respond to the substance.

Bad:

```text
Отличный вопрос, вы абсолютно правы.
```

Better:

```text
Здесь правда важно отделить формат текста от исследовательской оптики.
```

Exceptions: brief conversational warmth is fine, but not in the artifact.

### Rule 33. Unnecessary Disclaimers

Signal: "я не эксперт", "это только моё мнение", "возможно, я ошибаюсь"
repeated.

Why it is weak: uncertainty becomes self-protection.

Rewrite principle: name the confidence level and evidence limit.

Bad:

```text
Я не эксперт, но мне кажется, возможно, это работает так.
```

Better:

```text
Пока это рабочая гипотеза: Git изменил поведение команды через цену
эксперимента. Доказательств для более сильного вывода здесь ещё мало.
```

Exceptions: personal essays may keep one honest caveat.

### Rule 34. Invitation to Continue

Signal: "если хотите, могу продолжить", "могу подробнее разобрать".

Why it is weak: it sounds like chat output, not finished writing.

Rewrite principle: remove from public drafts.

Bad:

```text
Если хотите, могу разобрать это подробнее.
```

Better:

```text
```

Exceptions: internal assistant replies may use it when asking for direction.

---

## 10. Morphology and Idiomatics

### Rule 35. Participial Adverb Abuse

Signal: "делая", "стараясь", "позволяя", when the main action becomes unclear.

Why it is weak: Russian text starts to mirror loose English clauses.

Rewrite principle: use two direct verbs or explain sequence.

Bad:

```text
Команда писала релиз-ноты, стараясь объяснить ценность.
```

Better:

```text
Команда писала релиз-ноты и пыталась объяснить ценность для клиента.
```

Exceptions: keep if the secondary action is truly secondary.

### Rule 36. Case Drift

Signal: sentence changes structure halfway through and breaks case agreement.

Why it is weak: the reader stumbles over grammar instead of thought.

Rewrite principle: simplify the sentence and check agreement.

Bad:

```text
Для команды важно понимать риск и как его можно снизить.
```

Better:

```text
Команде важно понимать риск и знать, как его снизить.
```

Exceptions: none in polished public text.

### Rule 37. Gender and Number Drift

Signal: subject and predicate disagree after edits.

Why it is weak: often appears after mechanical rewriting.

Rewrite principle: reread the final sentence aloud.

Bad:

```text
Команда понял, почему изменение важно.
```

Better:

```text
Команда поняла, почему изменение важно.
```

Exceptions: none.

### Rule 38. Verb Aspect Mismatch

Signal: imperfective/perfective verbs blur action completion.

Why it is weak: Russian loses timing and causality.

Rewrite principle: choose aspect based on process vs completed event.

Bad:

```text
Команда писала релиз-ноты и увидела проблему.
```

Better:

```text
Команда начала писать релиз-ноты и увидела проблему.
```

Exceptions: keep imperfective when the ongoing process matters.

### Rule 39. Missing Subject Where It Matters

Signal: too many impersonal sentences: "нужно", "важно", "следует".

Why it is weak: responsibility disappears.

Rewrite principle: name the team, user, customer, manager, system, or tool.

Bad:

```text
Нужно раньше видеть ценность.
```

Better:

```text
Продуктовая команда должна видеть ценность до разработки, иначе позднее будет
трудно объяснить клиенту, зачем изменение попало в релиз.
```

Exceptions: principles may use impersonal form if the subject is obvious.

### Rule 40. Literal English Idioms

Signal: "делать смысл", "иметь смысл для", "работает как магия", "играет роль
в том, чтобы".

Why it is weak: text sounds translated.

Rewrite principle: use normal Russian idioms.

Bad:

```text
Это имеет смысл для команды.
```

Better:

```text
Команде это понятно.
```

Exceptions: domain terms can remain English if they are natural for the
audience.

---

## 11. Fillers and Water

### Rule 41. Empty Intensifiers

Signal: "достаточно", "довольно", "крайне", "очень" repeated.

Why it is weak: intensity replaces precision.

Rewrite principle: remove or replace with evidence.

Bad:

```text
Это довольно важный и очень полезный сигнал.
```

Better:

```text
Это сигнал, что команда пока не может объяснить пользу изменения клиенту.
```

Exceptions: spoken short-form style may keep occasional "довольно" or "очень".

### Rule 42. Filler Openers

Signal: "в целом", "по сути", "на самом деле", repeated.

Why it is weak: the sentence takes time to start.

Rewrite principle: remove unless it changes the nuance.

Bad:

```text
По сути, на самом деле Git снижает цену эксперимента.
```

Better:

```text
Git снижает цену эксперимента.
```

Exceptions: "по сути" can mark a real compression after a complex passage.

### Rule 43. Redundant Recap

Signal: "таким образом", "подводя итог", after a short text.

Why it is weak: the reader already understands the ending.

Rewrite principle: end with the principle itself.

Bad:

```text
Таким образом, можно сделать вывод, что цена эксперимента важна.
```

Better:

```text
Цена эксперимента меняет поведение команды сильнее, чем лозунги про скорость.
```

Exceptions: long essays may need section conclusions.

---

## 12. "Too Perfect" Russian

Perfect Russian can be a diagnostic signal when it becomes too symmetrical,
too polished, and too clean for the author's actual voice.

Do not intentionally add mistakes.

Do not break punctuation for "humanity".

Instead, check whether the text has:

- a real point of view;
- specific work situations;
- natural paragraph rhythm;
- author-level preference or doubt;
- concrete product friction;
- fewer stock phrases.

If the text is too smooth, make it more specific, not less literate.

---

## 13. Future Voice Profile

Projects may later support a local author voice profile, but this version does
not create `.humanizer/`, `voice.json`, sessions, or auto-logs.

Future fields may include:

- default form of address;
- default formality level;
- preferred rhythm;
- recurring author phrases;
- banned phrases;
- channel defaults;
- English term tolerance;
- examples that sound like the author;
- examples of accepted rewrites.

The voice profile must never override meaning, genre, or project-specific
constraints.

---

## 14. Humanizer Pass

Before returning a revised Russian draft:

1. Preserve the source meaning.
2. Select the mode from `MODES.md`.
3. Apply this core reference.
4. Apply project-specific rules from a voice adapter if one exists.
5. Check that genre, voice, and important nuance survived.

The preferred rewrite shape:

```text
concrete situation -> visible friction -> cause -> consequence -> clean sentence
```

---

## 15. Summary

The short version:

> Humanize by making the text more specific, more causal, and more author-like.
> Do not humanize by adding mess.
> Do not use style to hide weak thinking.
