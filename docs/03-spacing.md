# Spacing

**DOC NO. RL-BRAND-001-SPACE · REV. A**

Riposte spacing is a **loose 2px grid**. "Loose" is doing work in that sentence: the scale
is not a strict geometric ramp, because it was lifted from a real production site where
the values earned their places. Use a step. If you find yourself wanting a value that
isn't on the scale, you almost certainly want the neighbouring step instead.

---

## 1 · The scale

```
--space-1   4px     --space-4  16px     --space-7  48px
--space-2   8px     --space-5  24px     --space-8  64px
--space-3  12px     --space-6  34px     --space-9  72px
```

Read it as three bands:

| Band | Steps | Governs |
|---|---|---|
| **Intimate** — inside a component | 1–3 (4/8/12) | Chip padding, gaps between a label and its value, list-item spacing |
| **Structural** — between components | 4–6 (16/24/34) | Card padding, paragraph spacing, column gaps, the space under a section head |
| **Architectural** — between regions | 7–9 (48/64/72) | Block separation, section padding, page rhythm |

The rule of thumb: **never jump more than one band at a time.** A 4px gap next to a 64px
gap reads as a mistake; 4 → 16 → 64 reads as hierarchy.

### Step-by-step

| Step | Value | Canonical use |
|---|---|---|
| `--space-1` | `4px` | Chip vertical padding (`3px 9px` rounds to this band), tight glyph gaps |
| `--space-2` | `8px` | Inline gaps in a `.pills` row, `<li>` bottom margin, spec-header gap |
| `--space-3` | `12px` | Button vertical padding, chip horizontal padding, small card inset |
| `--space-4` | `16px` | **The default.** Card padding, `<p>` bottom margin, note padding |
| `--space-5` | `24px` | Button horizontal padding, gap between two related blocks |
| `--space-6` | `34px` | Grid column gap; the space below a `.sechead`; between stacked cards |
| `--space-7` | `48px` | Between major blocks *within* one section |
| `--space-8` | `64px` | Section padding (`padding-block`) on subpages |
| `--space-9` | `72px` | Section padding on the homepage, where sections need more air |

---

## 2 · Containers

Every container is **viewport-capped**. This is not optional: an uncapped `1060px` container
touches the edge of a phone screen, and bone paper with no margin stops reading as paper.

| Token | Value | Use |
|---|---|---|
| `--container` | `min(1060px, 92vw)` | Standard section. The default. |
| `--container-wide` | `min(1160px, 94vw)` | TOC-plus-content and other two-rail layouts |
| `--container-prose` | `min(900px, 92vw)` | Blog posts, single-column documents |
| `--measure` | `66ch` | Body copy max width |
| `--gutter` | `4vw` | Minimum breathing room at any viewport |

```css
.wrap { width: min(var(--container), calc(100vw - 2 * var(--gutter))); margin-inline: auto; }
```

**Measure beats container.** A `1060px` container does not mean `1060px` of text. Body copy
caps at `66ch` (≈ 62rem at our size); lead paragraphs pull tighter to **56–62ch** because
bold text at a larger size needs a shorter line to stay readable. If a paragraph is running
the full width of a wide container, the container is wrong, not the measure.

---

## 3 · Vertical rhythm

There is no baseline grid. There is a **stack order**, and it is consistent:

```
section
├─ padding-block: 64px (--space-8)          ← the region's air
├─ .sechead                                  ← SEC chip + title + slash tag
│  └─ padding-bottom: 14px, border-bottom: 2px
├─ margin-bottom: 34px (--space-6)          ← the gap a sechead always earns
├─ content
│  ├─ p  margin-bottom: 16px (--space-4)
│  └─ .grid  gap: 34px (--space-6)
└─ next block: margin-top 48px (--space-7)
```

Three rules govern it:

1. **A section head always owns 34px beneath it.** Not 32, not 40. This single value is
   what makes different pages feel like the same document.
2. **Paragraph spacing is 16px and margins collapse downward only.** Headings carry
   `margin: 0 0 16px` — never top margin. Space belongs to the element *above* the gap.
3. **The last child of a container never adds trailing margin.** The container's padding
   is the bottom edge. `.spec li:last-child { border-bottom: none }` is the same instinct.

---

## 4 · The border-eats-padding rule

This is the one that trips people up, and it is specific to a system drawn in 2px rules.

Every structural border is **2px**, and every accent bar is **6px** (top) or **8px** (left).
Those widths sit *outside* the padding box. So a card with `border: 2px` and
`padding: 16px` has 18px of visual inset — and a card with `border-top: 6px solid pink`
has 16px of inset on three sides and 22px on top.

**Do not compensate.** The slight top-heaviness is correct: the accent bar is a masthead,
and mastheads sit proud. What you must *not* do is mix bordered and unbordered cards in the
same row — the 2px difference reads as misalignment across a grid.

| Component | Border | Padding | Effective inset |
|---|---|---|---|
| `.spec` header | `2px` bottom | `8px 12px` | 8/12 |
| `.spec` body | `2px` all | `16px 14px` | 18/16 |
| `.note` | `2px` + `8px` left | `14px 16px` | 16/18, 22 left |
| `.partner` | `2px` + `6px` top | `16px` | 18/18, 22 top |
| `.stat` | `2px` all | `20px 18px` | 22/20 |

---

## 5 · Grid & gutters

Columns are equal-width and the gap is **always `--space-6` (34px)**, at every breakpoint
where columns exist. Below `760px`, grids collapse to one column and the 34px becomes
vertical spacing — the value does not change, only its axis.

```css
.grid { display: grid; gap: var(--space-6); }
@media (min-width: 760px) {
  .grid-2 { grid-template-columns: repeat(2, 1fr); }
  .grid-3 { grid-template-columns: repeat(3, 1fr); }
  .grid-4 { grid-template-columns: repeat(4, 1fr); }
}
```

**The `.flow` exception.** Process steps are joined by `→` arrows that live in the gap, so
`.flow .step` uses `margin-right: 26px` rather than grid `gap` — the arrow needs a box to
be absolutely positioned into. At `≤640px` the arrow rotates to `↓`, the margin goes to 0
and a `22px` flex gap takes over. This is the only place in the system where a spacing
value is off-scale, and it is off-scale because a glyph has to fit inside it.

---

## 6 · Breakpoints

Three, and only three. The system is fluid between them via `clamp()`, so there is very
little to change at each stop.

| Breakpoint | What happens |
|---|---|
| `560px` | `footer.colophon` goes from two columns to one; the tri-band cell left-aligns |
| `640px` | `.flow` stacks; arrows rotate `→` to `↓` |
| `760px` | `.grid-2/3/4` gain their columns; below this everything is single-column |

Type does not need breakpoints — every heading step is a `clamp()`, so it scales
continuously. If you find yourself adding a font-size media query, use a `clamp()` instead.

---

## 7 · Spacing on an ink field

Dark fields need slightly *more* air than bone ones, because the 2px bone rules on ink are
visually heavier than 2px ink rules on bone. The system does not encode this as different
tokens — instead:

- Prefer `--space-5` where you'd use `--space-4` for *padding inside* a panel on ink.
- Section padding stays the same. The change is local to components, not regions.
- `--ink-line` (`#5c554c`) dashed dividers are lower contrast than their bone-field
  counterparts by design; give rows one extra step of vertical padding so the dash still
  separates.

---

## 8 · Print spacing

See [`08-print.md`](08-print.md) for the full print setup. The spacing translation:

| Screen | Print |
|---|---|
| `--space-4` `16px` | `4mm` |
| `--space-6` `34px` | `8mm` |
| `--space-8` `64px` | `15mm` |
| Page margin | `15mm` minimum, `18mm` preferred |
| Rules | `0.5pt` for `1px` dashed, **`1.5pt` for `2px` solid** — do not go below 1pt on the structural rule or it disappears at press |

---

## Quick reference

```css
/* the nine steps */
--space-1: 4px;   --space-4: 16px;  --space-7: 48px;
--space-2: 8px;   --space-5: 24px;  --space-8: 64px;
--space-3: 12px;  --space-6: 34px;  --space-9: 72px;

/* containers */
--container: 1060px;  --container-wide: 1160px;  --container-prose: 900px;
--measure: 66ch;      --gutter: 4vw;

/* the three numbers to memorise */
16px  default padding and paragraph spacing
34px  under every section head, and every grid gap
64px  section padding
```
