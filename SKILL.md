---
name: riposte-brand
description: Riposte Laboratories Inc. brand and design system — colour palette with official codes, JetBrains Mono type scale, spacing guide, logo rules, pattern library, and per-tool setup recipes (Canva, Figma, Google Workspace, Office, Adobe/Affinity, Inkscape/GIMP, web). Use whenever producing anything that carries Riposte branding: websites, apps, decks, documents, README files, stickers, print artwork, charts. Also use when asked for Riposte colours, fonts, spacing, or "the brand guide".
user-invocable: true
---

# Riposte Laboratories — brand system

**Aesthetic: industrial spec-sheet × jester mi-parti.** Everything is drawn like a numbered
engineering document on bone paper, then cut through with harlequin pink, marigold and teal.

## The five rules

1. **Ink on bone** — `#1d1a17` on `#f6f1e7`. Never black on white.
2. **Accents rotate** — pink `#f0477d` → marigold `#fe9a0d` → teal `#12b795`, in that order,
   across repeated elements (`nth-child(3n)` or `4n` with an ink beat). No favourites.
3. **Radius 0.** Everywhere, no exceptions. Only the logo has curves.
4. **No blur.** No soft shadows, no glows, no gradients except the three functional
   patterns. Depth is a hard `4px 4px 0` offset paired with `translate(-2px,-2px)`.
5. **One font** — JetBrains Mono, 400/700/800. Headings UPPERCASE, prose sentence case,
   tracking widens as type shrinks (`.03em` headings → `.3em` kickers → `.55em` wordmark).

## Text on colour — the rule that gets broken

Fixed: **bone on pink**, **INK on marigold**, **bone on teal**.

But `bone` on `pink` is 3.16:1 and `bone` on `teal` is 2.27:1 — brand-correct, **not
text-safe**. Those pairings are legal on chips, spec headers, section bars and large
uppercase display only. The moment an accent fill carries a *sentence*, switch to the deep
variant: `--pink-deep #d81150`, `--orange-deep #a15e01`, `--teal-deep #0c7a63` (all ≥4.5:1
with bone). On bone pages, marigold and teal **cannot be text at all** (1.90:1, 2.27:1) —
use the deep variants. `ink` on `marigold` is 8.12:1, the best pairing in the system.

## Fields

`data-theme="dark"` → ink field, bone 2px rules, panels `#241f1b`, dashed `#5c554c`, accent
flips pink→teal. `.pinkfield` → full pink, everything bone, ink label fills, accent goes
marigold. Fields nest; `data-theme="light"` makes a bone island inside a dark subtree.

## Structure

2px solid rules structure everything; 1px dashed dividers separate rows; 6px accent
top-bars mark cards and steps; 8px left-bars mark notes and pull quotes. No hairlines.

Spacing: `4 8 12 16 24 34 48 64 72`. Memorise three — **16px** default padding and
paragraph spacing, **34px** under every section head and every grid gap, **64px** section
padding. Containers `min(1060px, 92vw)`; body copy caps at `66ch`.

Signature separators: 22px checker band (26px strip) and 34px pink/teal harlequin band
(38px strip) — alternate them down a page, always strips, never large fields. Tri-band
gradient `linear-gradient(105deg, pink 0 36%, orange 36% 64%, teal 64% 100%)` fills page
heads and the footer's right cell.

Spec-sheet chrome everywhere: `DOC NO. RL-xxx-A`, `SEC.NN` chips, `// slash tags`,
`REV. A`, corner marks. Glyphs `▸ ✓ ✕ ! → ↓ ♻` instead of icon fonts.

Motion: 120/150/250ms, plain easing, marquee 28s linear. No scroll-triggered fades, no
parallax, no entrance animations.

## Voice

Two registers, both mono. **The document** (uppercase, tracked): chrome and identifiers.
**The engineer** (sentence case): prose — plainspoken, concrete, wit from precision not
jokes. Bold the numbers that matter (**14.46 Wh**). No exclamation marks. No marketing
verbs. Placeholders loud and honest (`$[TAM]`, `⚠ Illustrative`).

## Files in this skill

| Need | File |
|---|---|
| Drop-in stylesheet (tokens + base + patterns) | `brand/riposte-brand.css` |
| Machine-readable source of truth | `brand/tokens.json` |
| Sass / Tailwind | `brand/tokens.scss`, `brand/tailwind.preset.js` |
| Every colour in every notation + contrast matrix | `docs/color-reference.md` |
| Reasoning: colour, type, spacing, logo, patterns, voice, a11y, print | `docs/0*.md` |
| Per-tool setup | `tools/canva.md`, `figma.md`, `google-workspace.md`, `office.md`, `adobe-affinity.md`, `inkscape-gimp.md`, `web.md` |
| Swatch files | `palettes/riposte.{ase,gpl,sketchpalette,csv,json}` |
| Logos (ink / bone / pink fills) | `assets/logo/` |
| The whole system rendered | `specimen/index.html` |

## How to act on this

**Building a web page, app, or HTML artifact** — link or inline
`brand/riposte-brand.css` and use the production class names: `.pagehead`+`.kicker`,
`.sechead`+`.no`+`.tag`, `.spec`, `.verdict`, `.flow`, `.chip`, `.note`, `.pull`, `.stat`,
`.partner`, `.marquee`, `.cta`, `.bigmail`, `.corner`, `footer.colophon`, `p.lead`, `.dim`,
`.hi`. Close every page with the colophon. Mark decorative bands and `SEC.NN` chips
`aria-hidden="true"`.

**Writing documentation** — sentence-case Markdown headings (uppercase fights GitHub's
renderer and hurts search), `DOC NO.`/`REV.` chrome stays uppercase, tables over prose,
close with the brand colophon block.

**Working in a design tool** — read the matching `tools/*.md` first. Each one has the exact
values, the tool's letter-spacing unit conversion, how to rebuild the bands without conic
gradients, and the two or three defaults that tool gets wrong (almost always: rounded
corners and blurred shadows).

**Changing a token** — edit `brand/tokens.json`, then run `node scripts/build.js`. It
regenerates every export and fails if the stylesheet drifts, a deep accent stops clearing
4.5:1, a non-zero radius appears, a shadow gains blur, or the ASE stops round-tripping.

**If asked to add a colour** — push back. There are three accents. For more chart
categories: rotate the three, add the ink beat, then `bone-dim` with an ink border, then the
`-deep` variants. Past eight, split the chart.

Source of truth: <https://github.com/armeehn/riposte-brand>
