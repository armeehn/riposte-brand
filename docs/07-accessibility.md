# Accessibility

**DOC NO. RL-BRAND-001-A11Y · REV. A**

Riposte's base is exceptionally accessible — ink on bone is **15.39:1**, more than double
what WCAG AA asks. The risk in this system isn't the base. It's the accents.

Full numbers: [`color-reference.md`](color-reference.md), generated and verified on every
build.

---

## 1 · The one thing to know

**`bone` on `pink` is 3.16:1. `bone` on `teal` is 2.27:1.**

Both are *fixed brand rules*. Both **fail** WCAG AA for body text. This is not a defect to
be fixed by changing the brand — it's a constraint to be respected by using those pairings
only where they're legal:

| Legal | Illegal |
|---|---|
| `.chip`, `.pill`, `SEC.NN` numbers | Any paragraph |
| `.spec` and `.verdict` header rows | Any list of sentences |
| 6px top bars, 8px left bars (no text) | Form labels and help text |
| Uppercase display at 24px+ or bold 18.66px+ | Captions, footnotes, fine print |
| The `.triband` footer cell (short uppercase strings) | Links inside body copy |

WCAG's "AA Large" threshold is **3:1**, and applies at 24px+ regular or 18.66px+ bold.
`bone` on `pink` (3.16:1) clears it. `bone` on `teal` (2.27:1) **does not clear even that** —
teal fills may carry short uppercase chrome as a brand convention, but never anything a
reader has to parse. Where teal must hold real text, use `--teal-deep`.

### The fix, when you need one

Every accent has a text-safe deep variant. Same hue, same saturation, lightness dropped
until bone clears 4.5:1:

| Bright (fills) | Deep (text-bearing) | Bone on deep |
|---|---|---|
| `--pink` `#F0477D` | `--pink-deep` `#D81150` | 4.53:1 ✓ AA |
| `--orange` `#FE9A0D` | `--orange-deep` `#A15E01` | 4.53:1 ✓ AA |
| `--teal` `#12B795` | `--teal-deep` `#0C7A63` | 4.69:1 ✓ AA |

Or invert: **ink on marigold is 8.12:1** — the best-contrasting accent pairing in the
system, and the reason marigold is the correct fill for `.note` callouts, warnings, and
anything else where the words matter more than the vibe.

---

## 2 · Accent-coloured text on bone

The other common trap. Two of the three accents **cannot be text on a bone page**:

| | on bone | verdict |
|---|---|---|
| `pink` | 3.16:1 | Large/display only |
| `orange` | **1.90:1** | Never text |
| `teal` | **2.27:1** | Never text |

A teal heading on a bone page must be `--teal-deep`. A marigold heading must be
`--orange-deep` — and at 1.90:1 the bright version is nearly invisible to everyone, not
just to low-vision readers.

Use `--accent-text` rather than naming a colour. It resolves correctly per field:
`pink-deep` on bone, plain `teal` on ink (6.79:1 — already safe), `ink` on a pink field.

### De-emphasis: `--text-muted` and `--text-faint`

Every field carries two quieter tiers below `--text`. They are `color-mix()` expressions,
so their real ratios appear nowhere in `tokens.json`, and until this revision nothing
measured them. `scripts/build.js` now resolves the mixes and checks each tier against its
own field; the full table is in
[`color-reference.md`](color-reference.md) under *Semantic text tiers*.

| Field | `--text` | `--text-muted` | `--text-faint` |
|---|---|---|---|
| bone | 15.39:1 | 5.14:1 ✓ AA | 3.74:1 — chrome only |
| ink | 15.39:1 | 6.59:1 ✓ AA | 4.12:1 — chrome only |
| pink | 3.16:1 | 4.87:1 ✓ AA | 4.87:1 ✓ AA |

Two rules, both enforced by the build:

- **`--text-muted` stays body-legal.** On any field where `--text` clears 4.5, the muted
  tier has to clear it too. De-emphasis is a tone, not a licence to drop under AA.
- **`--text-faint` is chrome.** It clears the 3:1 large-text and non-text floor and
  nothing more. Corner marks, slash tags, unit labels. Never a sentence.

**The pink field has one tier, not two.** `bone` on `pink` is already 3.16:1 — there is no
contrast left to spend, and mixing bone toward pink took `--text-muted` down to 2.36:1,
no better than `ink-line` on `ink`, the value [`01-color.md`](01-color.md) holds up as the
trap to avoid. Both tiers now resolve to `--ink` (4.87:1), which on a hot field reads
*quieter* than bone rather than louder. Past that, hierarchy on a pink field comes from
size, weight and tracking, not colour.

`opacity` helpers are a separate risk the build cannot check. `.dim` at `.65` and
`.slashtag` at `.6` composite against whatever is actually painted behind the element,
which is a layout question rather than a token question. On bone and ink they land in the
same band as the muted and faint tiers; on a pink field they fall below the floor along
with everything else that tries to soften bone on pink. Treat them as decoration there.

---

## 3 · Colour is never the only signal

Every state in the system pairs a colour with a **glyph**:

```
✓  pass      teal      .verdict.yes
✕  fail      pink      .verdict.no
!  warning   marigold  .verdict.warn / .note
```

This holds for charts too: series are distinguished by fill *and* by label, direct-labelled
where possible rather than relying on a legend.

The accent rotation (pink → marigold → teal across cards) is decorative, not semantic. If a
reader can't tell the three apart, they lose nothing — the content is identical. Never
encode meaning in "the pink one".

---

## 4 · Focus

```css
:focus-visible { outline: 3px solid var(--focus-ring); outline-offset: 2px; }
```

`3px`, not 2 — a 2px ring is indistinguishable from the system's structural 2px borders.
The `2px` offset separates it from the element's own border.

`--focus-ring` is pink on bone (3.16:1 against bone — clears the 3:1 non-text UI threshold)
and teal on ink (6.79:1). **Never remove the outline.** The brand has no soft alternative
to fall back on; there's no glow, no shadow, no colour shift subtle enough to substitute.

---

## 5 · Motion

Motion is already minimal — 120/150/250ms, plain easing, no scroll-triggered fades, no
parallax. The stylesheet still honours the preference:

```css
@media (prefers-reduced-motion: reduce) {
  .marquee .track { animation: none; }
  *, *::before, *::after {
    animation-duration: .001ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: .001ms !important;
  }
  .cta:hover, .btn:hover, button:hover { transform: none; }
}
```

The `.marquee` ticker is the only continuous animation in the system, and it's the first
thing to stop. Hover pops lose their `translate` but keep their colour inversion, so the
state change is still visible.

---

## 6 · Structure

The visual system leans hard on borders and uppercase — neither of which conveys anything
to a screen reader. So:

- **Uppercase is `text-transform`, never typed.** Type `Process`, style it uppercase.
  A screen reader announcing `P-R-O-C-E-S-S` as letters is a real failure mode, and text
  typed in caps also can't be searched or translated properly.
- **`SEC.03` chips and `DOC NO.` marks are decorative chrome.** If they're not part of the
  document outline, mark them `aria-hidden="true"` so the heading reads as its title, not
  as `SEC.03 THE COUNTER-ATTACK`.
- **Glyph bullets come from `::before`,** so they're not in the accessible name. That's
  correct — `▸` shouldn't be announced. But `✓` and `✕` in `.verdict` *do* carry meaning,
  so pair them with visually-hidden text (`<span class="sr-only">Pass:</span>`) or an
  `aria-label` on the list.
- **`.checker` and `.harlequin` bands are pure decoration.** `aria-hidden="true"`.
- **Heading levels follow the document, not the type scale.** A `--text-h3`-sized heading
  can be an `<h2>`. Size is a style; level is structure.

---

## 7 · Type sizes

Body copy is `15px` (`16px` on the homepage) — at or just below the conventional `16px`
baseline. Monospace at 15px reads larger than a proportional face at 15px because the
x-height and character width are both generous, but:

- **Never go below `14px` for prose.** `--text-md` (14px) is the floor for anything
  sentence-shaped.
- The `10–12px` steps are for uppercase labels only, where tracking keeps them legible.
- Everything scales with browser zoom and `rem`-based user settings; nothing is locked to
  viewport units alone (`clamp()` always has a `px` floor).
- `-webkit-text-size-adjust: 100%` prevents iOS from silently inflating text.

---

## 8 · Print

Print styles drop to true black on white, hide the decorative bands, and underline links.
Structural rules go to **1.5pt minimum** — below 1pt, a 2px screen rule disappears at press
and the entire visual structure with it. See [`08-print.md`](08-print.md).

---

## 9 · The automated check

`scripts/build.js` fails the build if:

- a `-deep` accent stops clearing 4.5:1 against bone
- `ink` on `orange` stops clearing 4.5:1
- any field's `--text` or `--text-muted` drops under 4.5:1 on that field, or its
  `--text-faint` drops under 3:1 — the `color-mix()` steps are resolved first
- any contrast figure printed in the docs, the stylesheet comments, `tokens.json` or the
  specimen stops matching a ratio the generated reference actually publishes
- any `border-radius` other than 0 appears
- any `box-shadow` gains a blur radius
- `tokens.json` and `riposte-brand.css` disagree on a hex value
- `riposte.ase` stops round-tripping

It does **not** check your markup. Contrast maths is automatable; whether you put a
paragraph on a teal fill is not. That one's on you.

```bash
node scripts/build.js --check
```
