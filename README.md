# Riposte Laboratories — Brand & Design System

**DOC NO. RL-BRAND-001 · REV. A · EST. 2026**

> **Parry. Riposte.**

This is the single source of truth for how Riposte Laboratories Inc. looks, reads and
behaves — on the website, in a deck, in a README, on a sticker, in Canva, in Figma, in
a printed spec sheet. If two things disagree, this repo wins.

The aesthetic, in one line: **industrial spec-sheet × jester mi-parti**. Everything is
drawn like a numbered engineering document on bone paper, then cut through with
harlequin pink, marigold and teal.

---

## The five rules

If you remember nothing else, remember these. Every page in this repo is downstream of them.

| # | Rule | Why |
|---|---|---|
| 1 | **Ink on bone.** `#1d1a17` on `#f6f1e7`. Not black on white. | The warmth is the difference between a lab document and a tax form. |
| 2 | **Accents rotate.** pink → marigold → teal, in that order, forever. | They are equal citizens. Picking a favourite collapses the harlequin into a corporate accent colour. |
| 3 | **Radius 0.** Everywhere. No exceptions. | Sharp corners are the brand. The only curves in the system belong to the logo. |
| 4 | **No blur.** No soft shadows, no glows, no gradients except the three functional patterns. Depth comes from a hard `4px 4px 0` offset. | The system is *drawn*, not lit. |
| 5 | **One font.** JetBrains Mono, weights 400 / 700 / 800. | Hierarchy comes from size, weight, case and tracking — never from a second family. |

---

## Start here

| I want to… | Go to |
|---|---|
| Set up the brand in **Canva** | [`tools/canva.md`](tools/canva.md) |
| Set up **Figma** | [`tools/figma.md`](tools/figma.md) |
| Set up **Google Docs / Slides** | [`tools/google-workspace.md`](tools/google-workspace.md) |
| Set up **Word / PowerPoint** | [`tools/office.md`](tools/office.md) |
| Set up **Illustrator / Affinity / Photoshop** | [`tools/adobe-affinity.md`](tools/adobe-affinity.md) |
| Set up **Inkscape / GIMP / Krita** | [`tools/inkscape-gimp.md`](tools/inkscape-gimp.md) |
| Build a **website or app** | [`tools/web.md`](tools/web.md) |
| Get a thing **printed** | [`docs/08-print.md`](docs/08-print.md) |
| Look up an **exact colour value** | [`docs/color-reference.md`](docs/color-reference.md) |
| See it all rendered | [`specimen/index.html`](specimen/index.html) — open in a browser |

Deep reference: [colour](docs/01-color.md) · [type](docs/02-typography.md) ·
[spacing](docs/03-spacing.md) · [logo](docs/04-logo.md) · [patterns](docs/05-patterns.md) ·
[voice](docs/06-voice.md) · [accessibility](docs/07-accessibility.md) ·
[print](docs/08-print.md) · [document numbers](docs/09-document-numbers.md)

---

## The palette at a glance

Hex is normative. Every other notation is derived from it — see
[`docs/color-reference.md`](docs/color-reference.md) for RGB / HSL / OKLCH / CMYK on
every token, plus the full contrast matrix.

### Base — ink & paper

| | Token | HEX | Use |
|---|---|---|---|
| ⬛ | `ink` | **`#1D1A17`** | All text, all 2px rules, the dark field |
| ⬛ | `ink-raised` | `#241F1B` | Panel surface on a dark field |
| ⬛ | `ink-head` | `#2B2723` | Header fill on a dark field |
| ⬛ | `ink-line` | `#5C554C` | Dashed dividers on a dark field. **Never text.** |
| ⬜ | `bone` | **`#F6F1E7`** | The paper. Default background |
| ⬜ | `bone-dim` | `#EAE4D6` | Recessed paper: sunken panels, spec headers |
| ⬜ | `white` | `#FFFFFF` | One hero field per site. That's the whole budget |

### Accents — the mi-parti three

Rotate them. `nth-child(3n)` / `nth-child(4n)` across repeated elements.

| | Token | HEX | Text on it |
|---|---|---|---|
| 🟥 | `pink` | **`#F0477D`** | `bone` |
| 🟧 | `orange` | **`#FE9A0D`** | **`ink`** — the exception, and the reason marigold exists |
| 🟩 | `teal` | **`#12B795`** | `bone` |

### Accents, deep — for when an accent must carry a *sentence*

Same hue, same saturation, lightness dropped until bone text clears WCAG AA.
The bright three above are for fills, bars, chips and large uppercase display.
The moment a coloured surface has to hold body copy, switch to these.

| | Token | HEX | Bone on it |
|---|---|---|---|
| 🟥 | `pink-deep` | `#D81150` | 4.53:1 ✓ AA |
| 🟧 | `orange-deep` | `#A15E01` | 4.52:1 ✓ AA |
| 🟩 | `teal-deep` | `#0C7A63` | 4.69:1 ✓ AA |
| 🟩 | `teal-ink` | `#04463A` | 9.60:1 on `teal` — diagram labels |

> **The honest caveat.** `bone` on `pink` is 3.16:1 and `bone` on `teal` is 2.27:1.
> Both are *brand-correct* and both **fail** AA for body text. They are legal on chips,
> spec headers, section bars and uppercase display type at 24px+ — which is exactly
> where the production site uses them. They are not legal on a paragraph.
> [`docs/07-accessibility.md`](docs/07-accessibility.md) has the full story.

---

## Type

**JetBrains Mono** — one family, three weights (400 / 700 / 800), SIL OFL licensed,
free to embed and redistribute. [jetbrains.com/lp/mono](https://www.jetbrains.com/lp/mono/)

There is no second family. The spec-sheet feel comes from a single mono voice used at
different sizes, weights, cases and tracking. Headings are UPPERCASE; prose is sentence
case; the smaller and more "machine" the text, the wider the tracking.

| Step | Size | Case | Tracking | Use |
|---|---|---|---|---|
| `display` | `clamp(30px, 6.6vw, 74px)` | UPPER | `-.01em` | Slide and hero statements |
| `h1` | `clamp(30px, 5vw, 54px)` | UPPER | `.03em` | Page heads |
| `h2` | `clamp(24px, 3.2vw, 40px)` | UPPER | `.03em` | Section headings |
| `h3` | `clamp(20px, 2.6vw, 30px)` | UPPER | `.03em` | Sub-sections |
| `lead` | `clamp(16px, 2vw, 19px)` **700** | sentence | `0` | Lead paragraphs |
| `body` | `15px` (16px homepage) | sentence | `0` | Prose. Max 66ch |
| `md` | `14px` | sentence | `0` | Spec body, secondary prose |
| `nav` | `12px` | UPPER | `.08em` | Nav, SEC chips, tags |
| `label` | `11px` | UPPER | `.1em` | Kickers, spec headers, corner marks |
| `xs` | `10px` | UPPER | `.12em` | Chip micro-labels |

Full rules, including the tracking ladder and the letterspaced wordmark lockup:
[`docs/02-typography.md`](docs/02-typography.md).

**In tools without JetBrains Mono:** upload it (Canva Pro, Figma, Adobe all allow this —
the OFL permits it). Only if you truly cannot: Space Mono → Roboto Mono → Consolas.

---

## Spacing

A loose **2px grid**. Nine steps, and you should be able to justify any value that isn't
one of them.

```
4px   8px   12px   16px   24px   34px   48px   64px   72px
 1     2     3      4      5      6      7      8      9
```

| Step | Value | Where it goes |
|---|---|---|
| 1 | `4px` | Chip padding, tight icon gaps |
| 2 | `8px` | Inline gaps, list item spacing |
| 3 | `12px` | Button padding (vertical), small card padding |
| 4 | `16px` | **Default.** Card padding, paragraph spacing |
| 5 | `24px` | Button padding (horizontal), gap between related blocks |
| 6 | `34px` | Column gap; the space under a section head |
| 7 | `48px` | Between major blocks inside a section |
| 8 | `64px` | Section padding, subpages |
| 9 | `72px` | Section padding, homepage |

**Containers** — always viewport-capped so nothing touches the edge of a phone:

| Token | Value | Use |
|---|---|---|
| `container` | `min(1060px, 92vw)` | Standard section |
| `container-wide` | `min(1160px, 94vw)` | Table-of-contents + content layouts |
| `container-prose` | `min(900px, 92vw)` | Blog, single column |
| `measure` | `66ch` | Body copy max width (leads run 56–62ch) |

The complete guide — vertical rhythm, the border-eats-padding rule, grid gutters, and how
spacing changes on an ink field — is in [`docs/03-spacing.md`](docs/03-spacing.md).

---

## What's in this repo

```
brand/
  riposte-brand.css      ← the drop-in stylesheet. Tokens + base + patterns.
  tokens.json            ← SOURCE OF TRUTH. Everything else is generated from this.
  tokens.scss            generated
  tailwind.preset.js     generated
palettes/
  riposte.ase            Adobe CC, Affinity, Sketch, Figma plugins
  riposte.gpl            GIMP, Inkscape, Krita
  riposte.sketchpalette  Sketch
  riposte.csv            spreadsheets, print vendors, Canva copy-paste
  riposte.json           scripts
assets/
  logo/                  wordmark in ink / bone / pink, plus the harmonic marks
  fonts/                 self-hostable JetBrains Mono woff2 subsets
docs/                    the deep reference
tools/                   per-application setup recipes
specimen/index.html      the whole system rendered on one page
scripts/build.js         regenerates every export and verifies consistency
```

### Regenerating

`brand/tokens.json` is the only file you hand-edit for values. Then:

```bash
node scripts/build.js          # rewrite all exports, then verify
node scripts/build.js --check  # verify only; non-zero exit on drift
```

The verifier is not decorative. It fails the build if the stylesheet and `tokens.json`
disagree on any hex, if a `-deep` accent stops clearing 4.5:1, if a `border-radius`
other than 0 appears, if any shadow gains a blur radius, or if `riposte.ase` stops
round-tripping. CI runs `--check` on every push.

---

## Using this in another Riposte project

Every Riposte repo carries a `BRAND.md` stating how it applies this guide and what it
deliberately doesn't. For anything with a web surface:

```html
<link rel="stylesheet" href="https://ripostelabs.xyz/brand/riposte-brand.css">
```

…or vendor `brand/riposte-brand.css` into the project. Then close the page with the
standard colophon:

```html
<footer class="colophon">
  <div class="l">&copy; 2026 Riposte Laboratories Inc. &middot; All rights reserved.</div>
  <div class="r">parry &#9851; riposte &#9851; recycle &#9851; repeat</div>
</footer>
```

For documentation, use the brand colophon block at the foot of the README —
see any Riposte `BRAND.md` for the exact form.

---

## Licence

The **code and documentation** in this repo are MIT (see [`LICENSE`](LICENSE)).

The **Riposte Laboratories name, wordmark, esh figure and logo files in
`assets/logo/`** are not covered by that licence. They are company marks — usable to
refer to Riposte Laboratories, not to brand anything else.

**JetBrains Mono** is licensed under the SIL Open Font License 1.1 and is redistributed
here under those terms; see [`assets/fonts/README.md`](assets/fonts/README.md).

---

<table>
<tr>
<td><b>DOC NO. RL-BRAND-001</b><br>REV. A · EST. 2026</td>
<td align="right"><b>PARRY ♻ RIPOSTE ♻ RECYCLE ♻ REPEAT</b><br>Riposte Laboratories Inc.</td>
</tr>
</table>
