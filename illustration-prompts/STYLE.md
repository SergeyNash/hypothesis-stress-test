# Visual style — Conference Minimal

Единая система для всех иллюстраций Hypothesis Stress Test (README, architecture, Product Sense).

## Принципы

- **Минимализм для сцены и README:** крупные блоки, мало текста, читаемо с проектора и на мобиле
- **Плоские заливки** — без градиентов, без 3D, без drop-shadow (допустима одна лёгкая обводка 1.5–2px)
- **Семантические цвета** — один цвет = один тип слоя/смысла на всех схемах
- **Стрелки:** 2px, цвет `#64748B`, простой треугольный наконечник
- **Фон:** `#FFFFFF` (слайды) или `#F8FAFC` (README embed)
- **Шрифт:** Inter, Arial или system sans-serif
- **Размеры текста:** title 22–24px bold; block label 14–16px bold; caption 11–12px regular
- **Соотношение сторон:** README/diagrams 1480×720 или 16:9; deck slides 1920×1080
- **Формат output:** SVG (предпочтительно) или PNG @2x

**Текущее состояние (RU primary):** Tier A в [`assets/ru/`](../assets/ru/) — PNG с русскими подписами. EN-версии и SVG — по мере готовности в `assets/en/` и `assets/ru/*.svg`.

## Палитра слоёв

| Слой / смысл | Fill | Stroke | Label (EN) |
|--------------|------|--------|------------|
| Input / Hypothesis | `#FEF3C7` | `#D97706` | INPUT |
| Roles | `#DBEAFE` | `#2563EB` | ROLES |
| Evidence / Local KB | `#E0F2FE` | `#0284C7` | EVIDENCE |
| Business Context | `#FCE7F3` | `#DB2777` | BUSINESS |
| Market | `#DCFCE7` | `#16A34A` | MARKET |
| Synthesis | `#EDE9FE` | `#7C3AED` | SYNTHESIS |
| Customer Discovery | `#FEF9C3` | `#CA8A04` | DISCOVERY |
| Decision Review | `#FFE4E6` | `#E11D48` | REVIEW |
| Human output / decision | `#FFF1F2` | `#BE123C` | HUMAN |
| Neutral / infra (Cline, MCP) | `#F1F5F9` | `#64748B` | — |
| Warning / trap pattern | `#FFF7ED` | `#F59E0B` | TRAP |

## Правила композиции

- Горизонтальный pipeline: слева направо, max 10 блоков на одной линии (для full overview — двухрядная нижняя полоса артефактов допустима)
- Talk-схемы: **max 4 блока** на главной линии
- Контрастные схемы (RAG vs pipeline): два столбца или split screen 50/50
- Матрица signal model: 2×2 grid + отдельная полоса снизу для Local Optimization Trap
- Отступы между блоками: 24–32px; corner radius: 12–16px

## Запрещено

- Stock photos, иконки-иллюстрации людей, мультяшный стиль
- Градиенты, неон, glassmorphism
- Мелкий текст (<10px), длинные параграфы внутри блоков
- Разные цветовые системы на разных схемах одного набора
- Security/AppSec jargon на Product Sense слайдах (кроме C5 если нужен минимальный footer)

## Парные версии

Каждая схема генерируется **дважды** с идентичной композицией:

- `assets/en/<name>.svg` — английские подписи
- `assets/ru/<name>.svg` или `assets/ru/<name>.png` — русские подписи (сейчас Tier A — PNG)

Product Sense talk assets:

- `product-sense/assets/ru/<name>.svg` (primary)
- `product-sense/assets/en/<name>.svg` (optional)

## Вставка в промпт

При генерации всегда включать абзац:

> Style: flat conference-minimal diagram, white background, semantic layer colors per STYLE.md, no gradients, large readable blocks, 2px gray arrows, sans-serif typography.
