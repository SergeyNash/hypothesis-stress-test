# VOICE ADAPTERS

A voice adapter layers a project, author, or genre voice on top of the portable
humanizer core.

The core answers:

> How do we make Russian text more natural?

The adapter answers:

> Natural for whom, in what project, and for which reader?

---

## 1. Purpose

Use adapters when the same humanizer rules must support different projects:

- Thinking Lab research posts;
- fiction chapters;
- children's or young adult books;
- product documents;
- business communication;
- personal essays.

Adapters prevent universal rules from leaking into the wrong genre.

---

## 2. Adapter Fields

A minimal adapter should define:

```markdown
Project / author:
Default mode:
Audience:
Voice:
Preferred rhythm:
Allowed texture:
Forbidden patterns:
Domain terms:
Examples that sound right:
Examples that sound wrong:
Review checklist:
```

Keep adapters short. They should guide editing, not become a second core.

---

## 3. Research Content Adapter Example

A research-content project may add:

- research-first discipline;
- evidence and uncertainty preservation;
- humanized product voice;
- JTBD as a useful lens;
- platform formats;
- anti-LinkedIn theater.

Those rules should live in that project's own adapter. They should not be
applied to fiction by default.

---

## 4. Fiction Adapter Example

For a book chapter, an adapter may say:

```markdown
Project / author: Cat superhero book
Default mode: fiction
Audience: children / young teens and adults reading aloud
Voice: clear, atmospheric, slightly ironic, emotionally warm
Preferred rhythm: smooth paragraphs with occasional short beats
Allowed texture: sensory detail, mild spoken roughness in dialogue
Forbidden patterns: explanatory colons, too many short dramatic fragments,
adult essay voice, product metaphors
Review checklist: preserve scene, character action, mystery, and emotional
subtext
```

This adapter would allow a sentence like:

```text
Крам не обернулся, ведь во дворе всегда кто-нибудь ходил, хлопал дверями,
заводил машину или ругался у подъезда.
```

and reject a more mechanical version like:

```text
Крам не обернулся: во дворе всегда кто-нибудь ходил.
```

---

## 5. Adapter Rule

Adapters may tighten or redirect core rules, but they should not:

- invent content;
- erase author voice;
- impose another project's style;
- override genre;
- turn every text into a post.

The best adapter makes the core humanizer feel native to the project.
