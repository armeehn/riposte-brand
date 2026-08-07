# Figma

**DOC NO. RL-BRAND-001-FIGMA · REV. A**

---

## 1 · Colour — as variables, not styles

Use **variables** (not paint styles) so the ink/bone/pink fields switch as modes.

Create a collection **`Riposte`** with three modes: **Bone**, **Ink**, **Pink**.

### Primitive group — same in every mode

| Variable | Hex |
|---|---|
| `base/ink` | `#1D1A17` |
| `base/ink-raised` | `#241F1B` |
| `base/ink-head` | `#2B2723` |
| `base/ink-line` | `#5C554C` |
| `base/bone` | `#F6F1E7` |
| `base/bone-dim` | `#EAE4D6` |
| `base/white` | `#FFFFFF` |
| `accent/pink` | `#F0477D` |
| `accent/orange` | `#FE9A0D` |
| `accent/teal` | `#12B795` |
| `accent/pink-deep` | `#D81150` |
| `accent/orange-deep` | `#A15E01` |
| `accent/teal-deep` | `#0C7A63` |
| `accent/teal-ink` | `#04463A` |

### Semantic group — aliases that change per mode

| Variable | Bone | Ink | Pink |
|---|---|---|---|
| `bg` | `bone` | `ink` | `pink` |
| `surface` | `bone` | `ink-raised` | `pink` |
| `surface-sunken` | `bone-dim` | `ink-head` | `ink` |
| `text` | `ink` | `bone` | `bone` |
| `line` | `ink` | `bone` | `bone` |
| `line-dashed` | `ink` | `ink-line` | `bone` |
| `accent` | `pink` | `teal` | `orange` |
| `accent-text` | `pink-deep` | `teal` | `ink` |
| `label-fill` | `ink` | `teal` | `ink` |
| `label-ink` | `bone` | `bone` | `bone` |

Bind every component to the **semantic** group. Then a frame set to the Ink mode inverts
the whole tree for free — same behaviour as `data-theme="dark"` in CSS.

Faster start: install any "ASE / palette import" plugin and load
[`../palettes/riposte.ase`](../palettes/riposte.ase) to get the 14 primitives, then build
the semantic aliases by hand.

---

## 2 · Type

Install **JetBrains Mono** locally (or add it as a shared font on an Org plan). Weights
400 / 700 / 800 only.

Figma letter-spacing accepts `em` directly — use the CSS values as-is:

| Style | Font | Size | Weight | Case | Spacing | Line height |
|---|---|---|---|---|---|---|
| `Display` | JetBrains Mono | 74 | 800 | UPPER | `-1%` | 102% |
| `H1` | JetBrains Mono | 54 | 700 | UPPER | `3%` | 115% |
| `H2` | JetBrains Mono | 40 | 700 | UPPER | `3%` | 115% |
| `H3` | JetBrains Mono | 30 | 700 | UPPER | `3%` | 115% |
| `Lead` | JetBrains Mono | 19 | 700 | — | `0` | 155% |
| `Body` | JetBrains Mono | 15 | 400 | — | `0` | 155% |
| `Body SM` | JetBrains Mono | 14 | 400 | — | `0` | 155% |
| `Nav` | JetBrains Mono | 12 | 700 | UPPER | `8%` | 120% |
| `Label` | JetBrains Mono | 11 | 700 | UPPER | `10%` | 120% |
| `Tag` | JetBrains Mono | 11 | 700 | UPPER | `14%` | 120% |
| `Spec` | JetBrains Mono | 11 | 700 | UPPER | `16%` | 120% |
| `Kicker` | JetBrains Mono | 11 | 700 | UPPER | `30%` | 120% |

Set case via **Text → Case → Uppercase**, not by typing caps — it exports as
`text-transform` and keeps the source text searchable.

The heading sizes above are the `clamp()` **maxima**. For mobile frames use the minima:
display 30, h1 30, h2 24, h3 20.

---

## 3 · Spacing variables

Number variables in a `space` group: `1:4  2:8  3:12  4:16  5:24  6:34  7:48  8:64  9:72`.

Auto-layout defaults: **gap 34**, **padding 16**, section `padding-block` **64**.

Layout grids — stretch, 4vw-equivalent margins:

| Frame | Columns | Gutter | Margin |
|---|---|---|---|
| Desktop 1440 | 12 | 34 | 190 (→ 1060 content) |
| Tablet 768 | 6 | 34 | 31 |
| Mobile 390 | 4 | 16 | 16 |

---

## 4 · Effects

- **Corner radius 0 on everything.** Set it in the component defaults so nobody has to
  remember.
- **Drop shadows: X 4, Y 4, Blur 0, Spread 0**, colour `accent/pink` or `accent/teal`.
  Blur must be **0** — this is the single most-broken rule when people work in Figma,
  because Figma's default shadow has a blur of 4.
- Big CTAs stack two: `4,4,0 teal` and `8,8,0 pink` (scaled from the CSS `8/16`).
- Hover state: `translate(-2px,-2px)` + the offset shadow + inverted fill.

---

## 5 · The three patterns

Figma has no conic gradient. Build each once as a component:

- **Checker** — 22px squares in a 2×2 alternating block, tiled to a 26px-tall strip with
  2px ink rules top and bottom.
- **Harlequin** — 34px squares rotated 45°, alternating `pink` / `teal`, 38px band.
- **Tri-band** — linear gradient at **105°** with hard stops: pink 0–36%, orange 36–64%,
  teal 64–100%. Place paired stops at each boundary so Figma doesn't interpolate.

---

## 6 · Dev Mode

Variable names map straight to the CSS custom properties — `base/ink` → `--ink`,
`accent/pink-deep` → `--pink-deep`, `space/6` → `--space-6`. Engineers should be consuming
[`../brand/riposte-brand.css`](../brand/riposte-brand.css) directly rather than
copying values out of Dev Mode.

---

## 7 · Checklist

- [ ] Variables, not styles; three modes wired
- [ ] Components bound to semantic aliases, not primitives
- [ ] Radius 0 in component defaults
- [ ] Every shadow has blur **0**
- [ ] Case set via Text → Case, not typed
- [ ] JetBrains Mono at 400/700/800 only
