# HUMANIZER MODES

This document defines how to apply `HUMANIZER_CORE.md` to different kinds of
Russian text.

Modes change strictness, rhythm, and acceptable texture. They do not change the
meaning of the source text.

---

## 1. General

Use for ordinary Russian drafts when no stronger genre is specified.

Default behavior:

- remove generic AI phrasing;
- keep natural Russian syntax;
- avoid inflated claims;
- reduce fillers and bureaucratic wording;
- preserve the author's point.

Use this mode for short notes, neutral drafts, and mixed text.

---

## 2. Product Content

Use for product, engineering, security, management, and technology writing.

Default behavior:

- keep professional clarity;
- replace abstract value claims with real user or team context;
- name friction, risk, cost, behavior, or coordination;
- avoid promotional gloss;
- avoid LinkedIn-style performance.

This mode can support Thinking Lab, but it is not Thinking Lab by itself.
Thinking Lab adds its own research and JTBD constraints through an adapter.

---

## 3. Fiction

Use for stories, chapters, scenes, dialogue, and narrative prose.

Default behavior:

- preserve atmosphere and point of view;
- avoid over-explaining the character's inner state;
- reduce artificial short fragments unless they create a real beat;
- avoid inline colons that explain emotion or cause too mechanically;
- prefer natural causal links such as "ведь", "потому что", or plain sentence
  flow;
- keep sensory detail concrete;
- make dialogue sound spoken without flattening character voice.

For fiction, do not apply product examples, business logic, JTBD, LinkedIn
rules, or research discipline.

Typical fiction rewrite:

```text
Before: Крам не обернулся: во дворе всегда кто-нибудь ходил.
After: Крам не обернулся, ведь во дворе всегда кто-нибудь ходил, хлопал
дверями, заводил машину или ругался у подъезда.
```

Use short sentences rarely, for impact. If several short sentences appear in a
row without a deliberate beat, merge them into a smoother paragraph.

---

## 4. Business

Use for memos, requirements, emails, reports, product documents, and internal
communication.

Default behavior:

- remove канцелярит;
- name actors and decisions;
- keep terms precise;
- avoid chatty looseness;
- preserve accountability;
- make requests and conclusions clear.

Business mode should become clearer, not more casual.

---

## 5. Essay

Use for long-form argument, reflective writing, and structured explanation.

Default behavior:

- preserve continuity;
- reduce repetitive signposting;
- make transitions calmer;
- keep uncertainty visible where needed;
- avoid motivational endings;
- keep the conclusion connected to the body of the text.

Essay mode can tolerate more complex sentences than posts or chat replies.

---

## 6. Chat Reply

Use for conversational replies.

Default behavior:

- remove assistant-like filler;
- avoid sycophancy;
- keep warmth without overpraise;
- answer directly;
- do not add public-article polish.

Remove endings like:

```text
Надеюсь, это помогло.
Если хотите, могу продолжить.
```

unless the interaction explicitly needs a follow-up offer.

---

## 7. Mode Selection

If mode is unclear:

- use `fiction` for chapters, scenes, characters, dialogue, narrative prose;
- use `business` for documents, specs, emails, requirements;
- use `product_content` for product/engineering posts and articles;
- use `essay` for long reflective argument;
- use `chat_reply` for conversational responses;
- otherwise use `general`.

When in doubt, preserve the source genre more than the humanizer rules.
