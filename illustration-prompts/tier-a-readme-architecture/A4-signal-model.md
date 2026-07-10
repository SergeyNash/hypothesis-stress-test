# A4 Signal model (synthesis matrix)

## Meta

| Поле | Значение |
|------|----------|
| Target output EN | `assets/en/signal-model.svg` |
| Target output RU | `assets/ru/signal-model.svg` |
| Canvas | 900×600 |
| Tier | A |
| Replaces | `assets/signal-model.svg` |

## Purpose

Матрица 2×2: столкновение Roles signal (Y) и Market signal (X), плюс отдельный блок Local Optimization Trap.

## Audience and context

- README — Decision model
- `architecture/diagram.md`

## Composition

### Layout

2×2 grid centered. Axis labels outside. Fifth category as full-width bar below grid with amber/warning border.

### Grid cells

|  | Market strong | Market weak |
|--|---------------|-------------|
| Roles strong | Validated Opportunity | Internal Illusion |
| Roles weak | Blind Spot | Weak Signal |

### Fifth bar

Local Optimization Trap — orange tint — "Pain confirmed, weak business value / buyer mismatch"

## Labels EN

Axes: Roles signal (vertical), Market signal (horizontal)
Column headers: Strong · Weak
Row headers: Strong · Weak
Cells: as table above
Trap title: Local Optimization Trap

## Labels RU

Оси: Сигнал ролей · Сигнал рынка
Столбцы: Сильный · Слабый
Строки: Сильный · Слабый
Ячейки: Подтверждённая возможность · Внутренняя иллюзия · Слепая зона · Слабый сигнал
Trap: Ловушка локальной оптимизации

## Generation prompt (copy-paste)

```
Minimal 2x2 matrix diagram "Signal Model (Synthesis)", 900x600, white background, flat style matching conference-minimal palette.

Title top center: "Signal Model (Synthesis)" 22px bold.

Y-axis left label vertical: "Roles signal". X-axis top: "Market signal".
Column labels: Strong | Weak. Row labels: Strong | Weak.

Four cells with light fills and 1.5px borders:
Top-left #EDE9FE: "Validated Opportunity" + small text "Internal + external align"
Top-right #DBEAFE: "Internal Illusion" + "Internal only"
Bottom-left #DCFCE7: "Blind Spot" + "External only"  
Bottom-right #F1F5F9: "Weak Signal" + "No strong evidence"

Below grid full width bar #FFF7ED stroke #F59E0B: "Local Optimization Trap" + "Pain confirmed, weak strategic business value / buyer mismatch"

No gradients. Sans-serif 14-16px. Clean grid lines.
```

### Russian variant note

```
Title "Модель сигналов (синтез)". Russian cell names and axis labels per Labels RU section.
```

## Post-generation checklist

- [ ] 5 patterns all visible
- [ ] Trap visually distinct from 2x2
- [ ] Style matches A1/A2 (not old gray boxes)
