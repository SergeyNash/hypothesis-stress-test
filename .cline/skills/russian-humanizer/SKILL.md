---
name: russian-humanizer
description: Edit, humanize, and adapt Russian text without running Thinking Lab research. Use when the user asks to make Russian text more human, natural, less AI-like, less bureaucratic, or closer to an author/project voice; supports fiction, product content, business text, essays, and chat replies while preserving meaning.
---

# Russian Humanizer

## Overview

Use this skill to revise Russian text directly.

This is a portable editing skill, not a Thinking Lab research skill. It does
not require the Thinking Lab repository. It does not run modules, update
knowledge files, choose publication strategy, or add product/JTBD thinking
unless the selected mode or user request explicitly calls for it.

## Source Documents

Use the bundled references:

- `references/HUMANIZER_CORE.md`
- `references/MODES.md`
- `references/VOICE_ADAPTERS.md`

If the user specifically asks for Thinking Lab research/content flow, this is
the wrong skill.

## Project adapters (hypothesis-stress-test)

When working in this repository, bundled `references/` stay canonical. Add
project voice from:

- `humanizer/adapters/PRODUCT_SENSE_VOICE.md` — files under `product-sense/`
  (mode: `business` or `essay`)
- `humanizer/adapters/PUBLIC_EXPLAINER_VOICE.md` — public explainer texts,
  street pitches, parables (mode: `fiction` or `general`)

Do not humanize framework contracts:

- `layers/`
- `.clinerules/` including `workflows/`
- `.cline/skills/`
- `templates/input-schema.md`
- `examples/*/outputs/`
- `scripts/`

See `humanizer/USAGE.md` for mode + adapter selection.

## Installation

To use this skill globally in Codex, copy the whole skill folder to:

```text
%USERPROFILE%\.codex\skills\russian-humanizer
```

The folder is self-contained. It includes `SKILL.md`, `agents/openai.yaml`, and
all reference files needed for editing.

## Intake

Extract:

```markdown
Input text:
Mode:
Audience:
Project / author voice:
Strictness:
Must preserve:
Must avoid:
Output preference:
```

Defaults:

- Mode: infer from the text.
- Strictness: medium.
- Output preference: revised text plus short notes only when useful.
- Preserve meaning, scene, argument, facts, and author intent.

Ask only when the missing answer materially changes the edit.

## Mode Selection

Use modes from `references/MODES.md`. Canonical slugs:

| Slug | MODES.md heading |
| ---- | ---------------- |
| `general` | General |
| `product_content` | Product Content |
| `fiction` | Fiction |
| `business` | Business |
| `essay` | Essay |
| `chat_reply` | Chat Reply |

- `general`: neutral Russian drafts.
- `product_content`: product, engineering, security, management, technology.
- `fiction`: chapters, scenes, dialogue, narrative prose.
- `business`: memos, requirements, reports, emails.
- `essay`: long-form argument or reflective writing.
- `chat_reply`: conversational replies.

Do not apply the wrong mode. A book chapter should not receive product-content
logic. A business memo should not become chatty fiction.

## Core Workflow

Use this pipeline:

```text
input text -> mode selection -> voice constraints -> humanizer pass -> genre check -> revised text
```

During editing:

- preserve meaning;
- preserve author voice where visible;
- remove generic AI rhythm;
- remove bureaucratic and translated Russian;
- reduce artificial short fragments;
- avoid inline colons when they make prose sound mechanical;
- avoid "not A, but B" contrast tics unless they are truly needed;
- replace vague claims with concrete context;
- keep grammar and punctuation clean;
- do not add intentional mistakes.

If the text is weak by meaning, say what is missing instead of making it sound
confident.

## Fiction Mode

Use `fiction` for chapters, scenes, dialogue, and narrative prose.

Priorities:

- preserve atmosphere;
- preserve point of view;
- preserve character behavior and subtext;
- keep sensory detail concrete;
- make dialogue sound spoken;
- avoid adult essay voice;
- avoid product metaphors and business language;
- reduce short dramatic fragments unless they create a deliberate beat;
- avoid explanatory inline colons such as `Он не обернулся: во дворе...`;
- prefer natural causal links such as `ведь`, `потому что`, or simple sentence
  flow.

Example:

```text
Before: Крам не обернулся: во дворе всегда кто-нибудь ходил.
After: Крам не обернулся, ведь во дворе всегда кто-нибудь ходил, хлопал
дверями, заводил машину или ругался у подъезда.
```

Do not over-polish fiction. A scene can keep mild roughness if it belongs to
the voice.

## Product Content Mode

Use only for product, engineering, management, security, or technology texts.

Priorities:

- name user or team friction;
- remove promotional gloss;
- keep professional clarity;
- avoid LinkedIn theater;
- make abstract value concrete.

Do not apply this mode to fiction unless the user explicitly asks for a product
metaphor.

## Business Mode

Make the text clearer, not more casual.

Priorities:

- remove канцелярит;
- name actors and decisions;
- keep terms precise;
- preserve accountability;
- make requests and conclusions visible.

## Essay Mode

Priorities:

- preserve argument continuity;
- reduce repetitive signposting;
- keep transitions calm;
- make uncertainty legible;
- avoid motivational endings.

## Chat Reply Mode

Priorities:

- answer directly;
- keep warmth without sycophancy;
- remove assistant artifacts;
- avoid public-article polish.

Remove endings like:

```text
Надеюсь, это помогло.
Если хотите, могу продолжить.
```

unless the user is asking for an interactive assistant reply.

## Output

For short or medium text, return:

1. revised text;
2. brief notes only if they help the user understand important changes.

For long text, offer or use a staged approach:

- first pass: sample rewrite and style diagnosis;
- wait for user OK before rewriting the full document;
- second pass: full chapter/section rewrite;
- third pass: consistency pass.

When editing user manuscripts, do not overwrite files unless the user
explicitly asks for file changes.

## Safety Rails

Do not:

- invent missing facts;
- change plot events;
- change character motivation unless asked;
- add product/JTBD language outside product mode;
- apply Thinking Lab research flow;
- add intentional typos;
- break punctuation for "humanity";
- erase the author's voice.

The best result should feel like the author wrote a cleaner, more natural
version.
