# [ID] Название схемы

## Meta

| Поле | Значение |
|------|----------|
| Target output EN | `assets/en/<filename>.svg` |
| Target output RU | `assets/ru/<filename>.svg` |
| Format | Vector diagram (SVG) |
| Canvas | 1480×720 (README) / 1920×1080 (deck) |
| Style reference | [STYLE.md](./STYLE.md) |
| Tier | A / B / C |

## Purpose

Одно предложение: зачем эта схема существует.

## Audience and context

- Документы: …
- Слайд talk-outline: §…

## Composition

### Layout

Описание расположения (horizontal pipeline / 2 columns / matrix).

### Blocks

1. Block name — layer color — short content
2. …

### Arrows and grouping

Куда ведут стрелки; optional dashed lines for human decision.

### Title and caption

- Title: …
- Subtitle (optional): …

## Labels EN

Точный текст на каждом блоке (bullet list).

## Labels RU

Точный текст на каждом блоке (bullet list).

## Do NOT include

- …

## Generation prompt (copy-paste)

```
[Полный промпт для LLM / Figma / дизайнера — EN]
```

### Russian variant note

```
Same layout. Replace labels with: [RU labels list]
```

## Post-generation checklist

- [ ] EN and RU versions exported
- [ ] Colors match STYLE.md palette
- [ ] Readable from 5m projector distance
- [ ] No text overflow in blocks
- [ ] Filename matches Meta
