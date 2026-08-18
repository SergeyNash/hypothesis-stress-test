# A5 Evidence sources (inventory-first)

## Meta

| Поле | Значение |
|------|----------|
| Target output EN | `assets/en/evidence-sources.svg` |
| Target output RU | `assets/ru/evidence-sources.svg` |
| Canvas | 1200×600 |
| Tier | A |
| Replaces | `assets/cline-mcp-confluence.svg` (narrative shift) |

## Purpose

Показать inventory-first модель: локальная KB → atomic evidence → Market Layer channels (не «только Confluence»).

## Audience and context

- `architecture/diagram.md`
- `implementations/quick-start.md`

## Composition

### Layout

Three-column flow:

1. **Sources** (left stack): Local KB files, interviews, notes, images
2. **Inventory** (center): `discovery_preview.md` + `evidence_inventory.md` with EVID-NNN atoms
3. **Market channels** (right): Local signals · Confluence · External · Inferred (separated, labeled)

Arrow: Sources → Inventory → Market interpretation (no mixing before inventory)

### Title

- EN: **Evidence-first flow**
- RU: **Сначала доказательства**

### Principle callout

- EN: No evidence → no claim
- RU: Нет доказательств → нет утверждения

## Labels EN

Sources: Local KB · CustDev notes · Strategy docs
Center: Evidence inventory · Atomic EVID items
Channels: Local · Confluence · External · Inferred

## Labels RU

Источники: Локальная KB · Заметки CustDev · Стратегия
Центр: Инвентарь evidence · Атомарные EVID
Каналы: Локальные · Confluence · Внешние · Выведенные

## Generation prompt (copy-paste)

```
Diagram "Evidence-first flow", 1200x600, flat minimal, white background.

Three columns left to right with bold arrows:

LEFT column "SOURCES" (stack of 3 gray-blue boxes): Local KB files, CustDev notes, Strategy docs — fills #F1F5F9 stroke #64748B

CENTER column "INVENTORY" (sky blue #E0F2FE): large box "evidence_inventory.md" with small items EVID-001, EVID-002, EVID-003 as pills. Above smaller "discovery_preview.md"

RIGHT column "MARKET CHANNELS" (green tint container) with 4 separated sub-boxes NOT merged:
- Local signals (from inventory)
- Confluence signals  
- External market signals
- Inferred signals (labeled, weak)

Bottom principle badge amber: "No evidence → no claim"

Title top: "Evidence-first flow". No Confluence logo dominant. Sans-serif.
```

### Russian variant note

```
Title "Сначала доказательства". Russian labels per section. Principle badge: "Нет доказательств → нет утверждения".
```

## Post-generation checklist

- [ ] Confluence is one channel among four, not the hero
- [ ] Inventory step visually mandatory before market
