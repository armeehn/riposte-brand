# Patterns & components

**DOC NO. RL-BRAND-001-PAT · REV. A**

Every class here ships in [`brand/riposte-brand.css`](../brand/riposte-brand.css), reads
semantic variables, and survives `.dark` / `.pinkfield` inversion without extra work.
Class names match the production site's markup — this is documentation of a real system,
not a proposal.

See it all rendered: [`specimen/index.html`](../specimen/index.html).

---

## 1 · The three signature patterns

The mi-parti kit. All three are **hard-stop gradients** — no blending, ever.

### Checker band — `.checker`

```
22px conic tiles · 26px band height (tile + 2 × 2px rule) · ink/bone
```

`.checker.teal` swaps ink for teal. On a dark field it auto-swaps to teal-on-ink.

### Harlequin band — `.harlequin`

```
34px diamonds (conic from 45deg) · 38px band height · pink/teal
```

### Tri-band — `--triband`

```
linear-gradient(105deg, pink 0 36%, marigold 36% 64%, teal 64% 100%)
```

Fills `.pagehead` banners and the right cell of `footer.colophon`.

### Rules for all three

1. **They are strips, never fields.** 26px, 38px, and a footer cell. A full-page harlequin
   is a circus tent.
2. **Alternate flavours down a page.** Checker, then harlequin, then checker. Two identical
   bands in a row reads as a rendering bug.
3. **One flavour per page maximum for the tri-band** — it's the pagehead, and repeating it
   demotes the page head.
4. **`aria-hidden="true"`.** They are decoration.

---

## 2 · Document chrome

The spec-sheet layer. This is what makes a page read as a filed document.

| Class | What it is |
|---|---|
| `.pagehead` + `.kicker` | Tri-band banner: kicker, `h1`, optional 62ch strapline |
| `.sechead` | `SEC.NN` chip + uppercase `h2` + right-aligned `// slash tag`, over a 2px rule |
| `.corner` (`.tl .tr .bl .br`) inside `.cornered` | Corner marks: `DOC NO. RL-000-A`, `REV. A` |
| `.slashtag` | The lowercase code-comment annotation, `.14em` tracked, 60% opacity |
| `.stamp` | Rotated `-2deg` marigold outline stamp — `DRAFT`, `ILLUSTRATIVE` |

`SEC.NN` chips rotate their fill: `.pinkno`, `.orangeno`, `.tealno`, or the default ink.
Number sections in order and let the colour cycle follow.

**Chrome is decorative.** Mark `SEC.NN` and corner marks `aria-hidden="true"` so the
heading announces as its title.

---

## 3 · Cards

### `.spec` — the workhorse

Header row (uppercase, `.16em` tracked, on `bone-dim`) over a `▸`-bulleted body with
dashed row dividers. Header fill variants: `.orangehead`, `.tealhead`, `.inkhead`.

### `.verdict` — yes / no / warn

Same anatomy, but the header is a full accent fill and the bullets carry meaning:

| Variant | Header | Bullet |
|---|---|---|
| `.yes` | teal | `✓` |
| `.no` | pink | `✕` |
| `.warn` | marigold | `!` |

Pair the glyphs with visually-hidden text — see [`07-accessibility.md`](07-accessibility.md#3--colour-is-never-the-only-signal).

### `.partner` — rotating masthead

A bordered card whose `6px` top bar cycles pink → marigold → teal → ink on `nth-child(4n)`.
The ink beat is what stops the rotation reading as a rainbow.

### `.stat` — the number

Large `800`-weight figure (`clamp(26px, 4vw, 44px)`, `-.02em`) over an uppercase label.
`.n.pink` / `.n.orange` / `.n.teal` colour the figure — and at that size the bright accents
clear the AA-Large threshold, so this is one of the few places accent-coloured text is legal.

---

## 4 · Callouts

| Class | Spine | Use |
|---|---|---|
| `.note` | `8px` marigold left bar, on `bone-dim` | Asides, caveats, warnings. Marigold because **ink on marigold is 8.12:1** — the callout people actually have to read. |
| `.pull` | `8px` pink left bar, no box | Pull quotes. `700`, 60ch max. |

---

## 5 · Flow

`.flow > .step` — bordered process steps joined by `→` arrows sitting in a `26px` right
margin. Top bars rotate on the 4-cycle. Below `640px` the steps stack and the arrow rotates
to `↓`.

This is the *only* off-scale spacing value in the system, and it's off-scale because a glyph
has to fit in the gap. See [`03-spacing.md`](03-spacing.md#5--grid--gutters).

The canonical Riposte flow is the fencing frame: **parry → riposte → return**.

---

## 6 · Small elements

| Class | Anatomy |
|---|---|
| `.chip` | `10px` uppercase, `.12em`, `3px 9px`, `2px` border. `.pink` `.orange` `.teal` `.ink` |
| `.pill` | `12px` uppercase, `2px` border, `7px 12px`. Larger, quieter |
| `.pills` | Flex wrapper, `8px` gap |
| `.marquee` | Ink ticker, `.18em`, 28s linear loop. `.c1/.c2/.c3` colour the words |

---

## 7 · Actions

| Class | Behaviour |
|---|---|
| `.cta` | Outline button. Hover: invert + `translate(-2px,-2px)` + `4px 4px 0` pink |
| `.bigmail` | Full-width block CTA. Hover: ink fill + `8px 8px 0 teal, 16px 16px 0 pink` |
| `button` / `.btn` | Same as `.cta`, applied to real buttons |

**The hover grammar, everywhere in the system:** move up-left 2px, drop a hard offset
shadow in an accent, invert the fill. No blur, no scale, no opacity fade.

The `--shadow-stack` double-offset is for **big CTAs only**. On a small button it reads as
a mistake.

---

## 8 · The colophon footer

```html
<footer class="colophon">
  <div class="l">&copy; 2026 Riposte Laboratories Inc. &middot; All rights reserved.</div>
  <div class="r">parry &#9851; riposte &#9851; recycle &#9851; repeat</div>
</footer>
```

Ink cell left, tri-band cell right, `2px` ink rule above, `11px` uppercase `.1em`.
Collapses to one column below `560px`.

**This is the standard close for every Riposte page.** Same two cells, same order, every
time. It's the signature at the bottom of the document.

---

## 9 · Diagrams

Hand-built **SVG line diagrams** in brand colours on the current field — the HEX unit, the
tessellation, the dome. Labelled in mono like an instrument faceplate.

- Stroke weights match the CSS rules: `2px` structural, `1px` dashed for construction lines
- `--teal-deep` for linework on teal, `--teal-ink` for labels on teal fills
- Labels uppercase, `--text-label` (11px), `.1em` tracked
- No fills except flat brand colours. No gradients, no soft shading
- `currentColor` wherever possible, so the diagram inverts with its field

**No icon fonts and no icon sets.** Anything that looks like an icon is either a glyph
(see [`02-typography.md`](02-typography.md#7--glyphs-not-icons)) or a hand-drawn SVG.

### Charts

Bordered boxes with flat accent fills — no axes lines beyond the structural rule, no
gridlines, no drop shadows.

**Need more than three categories?** Do not add a fourth accent. In order:

1. Rotate the three accents and add the **ink** beat — four series.
2. Add `bone-dim` fill with a `2px` ink border — five.
3. Add the `-deep` variants — eight, and still on-brand.
4. Beyond that, the chart is wrong. Split it, or use a table.

---

## 10 · Motion

```
120ms  --dur-flick   colour swaps: nav, links, chips
150ms  --dur-snap    pops: CTA hover, arrow slide, caret rotate
250ms  --dur-move    progress bars, larger repositions
 28s   --marquee-dur ticker loop, linear
```

Plain easing. Hover = invert or accent fill. Arrows slide in from `-5px`. Carets rotate.

**No scroll-triggered fades. No parallax. No entrance animations.** A Riposte page is
already there when you arrive — it's a printed document, not a presentation.

The one canvas moment: layered signal-wave sines in the three accents behind the hero mark.

---

## 11 · Layout helpers

```css
.wrap        min(1060px, 100vw - 2×4vw)
.wrap-wide   min(1160px, …)
.wrap-prose  min(900px,  …)
.section     padding-block: 64px
.grid        display:grid; gap:34px
.grid-2/3/4  columns at ≥760px
```

Prose helpers: `p.lead` (bold, 56ch), `.dim` (.65 opacity), `.hi` (bold + `--accent-text`),
`.slashtag`.
