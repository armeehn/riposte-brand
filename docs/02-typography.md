# Typography

**DOC NO. RL-BRAND-001-TYPE · REV. A**

---

## 1 · One family

**JetBrains Mono.** Weights **400**, **700**, **800**. That is the entire type system.

| | |
|---|---|
| Designer | JetBrains / Philipp Nurullin, Konstantin Bulenkov |
| Licence | **SIL Open Font License 1.1** — free to use, embed, redistribute and bundle, including commercially |
| Download | [jetbrains.com/lp/mono](https://www.jetbrains.com/lp/mono/) · [Google Fonts](https://fonts.google.com/specimen/JetBrains+Mono) |
| Self-host | `assets/fonts/*.woff2` in this repo (latin, latin-ext, vietnamese subsets) |

```css
--font-mono: "JetBrains Mono", "IBM Plex Mono", ui-monospace, SFMono-Regular,
             Menlo, Consolas, "Liberation Mono", monospace;
```

**There is no second family.** Not for headings, not for prose, not for "a bit of
contrast". Hierarchy comes from four levers — size, weight, case, tracking — and those
four are enough. A humanist sans dropped into a Riposte layout to "warm up the body copy"
destroys the premise: this is a document produced by a machine shop.

**Why a mono for prose?** Because the brand is a spec sheet. The even rhythm of a
monospace is the texture of instrument faceplates, terminal output and dimensioned
drawings. It reads slightly slower than a proportional face, which is why the measure caps
at 66ch and the body sits at a generous 1.55 line-height — the system compensates rather
than compromising.

### When the real font is unavailable

Upload it. Canva Pro, Figma, Adobe Fonts (as a custom font), Google Workspace via add-on,
and every OS font book all accept an OFL font. The licence explicitly permits it.

Only if you genuinely cannot:

| Tool | Fallback | Notes |
|---|---|---|
| Canva (free tier) | **Space Mono** | Closest in flavour; heavier quirk. Then Roboto Mono. |
| Google Docs/Slides | **Roboto Mono** | Available natively; the safest cross-platform fallback |
| Word / PowerPoint | **Consolas** | Ships with Office on every platform |
| Anywhere | **IBM Plex Mono** | The best overall substitute if installable |

Record it when you do. A deck set in Roboto Mono is off-brand-but-legible; a deck set in
Arial is neither.

---

## 2 · The two registers

One voice, two registers. Everything on a Riposte surface is one of these.

### The document — UPPERCASE, tracked

Chrome and labels. Filed like a spec sheet.

```
DOC NO. RL-200-A      SEC.03      REV. A      SPEC / HEX UNIT      EST. 2026
```

Uppercase, `700` or `800`, positive tracking that widens as the size drops. This register
never carries a sentence — it carries an identifier.

### The engineer — sentence case, 400/700

Prose. Plainspoken, concrete, quietly witty. Numbers that matter are bold.

> A disposable vape is, functionally, a lithium cell wrapped in plastic and marketed as
> trash. Each holds a **14.46 Wh** cell measuring **45 × 13 mm**.

Section heads carry a lowercase slash-tag comment, right-aligned:
`// the counter-attack`, `// local loop injection molding`. This is the one place the two
registers touch — an uppercase heading with a lowercase code comment trailing it.

---

## 3 · The scale

| Token | Size | Weight | Case | Tracking | Leading | Use |
|---|---|---|---|---|---|---|
| `--text-display` | `clamp(30px, 6.6vw, 74px)` | 800 | UPPER | `-.01em` | 1.02 | Slide and hero statements |
| `--text-h1` | `clamp(30px, 5vw, 54px)` | 700 | UPPER | `.03em` | 1.15 | Page heads |
| `--text-h2` | `clamp(24px, 3.2vw, 40px)` | 700 | UPPER | `.03em` | 1.15 | Section headings |
| `--text-h3` | `clamp(20px, 2.6vw, 30px)` | 700 | UPPER | `.03em` | 1.15 | Sub-sections |
| `--text-lead` | `clamp(16px, 2vw, 19px)` | **700** | sentence | `0` | 1.55 | Lead paragraphs |
| `--text-body` | `15px` (16px homepage) | 400 | sentence | `0` | 1.55 | Prose |
| `--text-md` | `14px` | 400 | sentence | `0` | 1.55 | Spec body, secondary prose |
| `--text-nav` | `12px` | 700 | UPPER | `.08em` | — | Nav, `SEC.NN` chips, tags |
| `--text-label` | `11px` | 700 | UPPER | `.1em` | — | Kickers, spec headers, corner marks |
| `--text-xs` | `10px` | 700 | UPPER | `.12em` | — | Chip micro-labels |

Every heading step is a `clamp()`. **Do not add font-size media queries** — the type
already scales continuously between the min and max. If a heading is wrong at some
viewport, adjust the `vw` coefficient, not the breakpoint.

---

## 4 · The tracking ladder

The governing principle: **tracking widens as type gets smaller and more "machine."**
Big statements tighten; micro-labels spread out until they read as engraving.

```
-.01em   display        big statements pull together
 .03em   h1 / h2 / h3   uppercase headings need a hair of air
 .08em   nav            links, buttons
 .10em   label          chips, doc numbers
 .14em   tag            // slash tags, corner marks
 .16em   spec           spec-card headers, stamps
 .30em   kicker         pagehead kickers
 .55em   wordmark       L A B O R A T O R I E S   I N C .
```

Uppercase monospace at 10–12px is genuinely hard to read without tracking — the letterforms
are already even-width, so without extra space they fuse into a bar. The ladder is
functional, not decorative.

**Never track lowercase prose.** Tracking applies only to the uppercase register. Body
copy sits at `0`.

---

## 5 · Rules of use

1. **Headings and labels are UPPERCASE. Prose is sentence case.** No title case anywhere
   in the system. Ever.
2. **Bold the numbers that matter.** In prose, load-bearing figures and units go `700`:
   **14.46 Wh**, **45 × 13 mm**, **72%**. This is the engineer register's one flourish.
3. **Body copy maxes at 66ch.** Leads pull tighter, to 56–62ch.
4. **Leads are bold.** `--text-lead` is `700` by default. A lead paragraph set at 400 reads
   as body copy that happens to be bigger.
5. **`800` is reserved.** Deck headlines and `.stat` numbers only. If everything is 800,
   nothing is.
6. **No italics.** Monospace italics are weak and the system has no use for them.
   For emphasis inside prose use `700`, or `.hi` (which is `700` + `--accent-text`).
7. **No underlines except on links.** And links get `2px` thickness at `3px` offset —
   a hairline underline disappears against the mono texture.
8. **Line-height is 1.55 for prose, 1.15 for headings, 1.02 for display.** Tight display
   leading is what makes a two-line hero statement read as a single block.

---

## 6 · The wordmark lockup

The letterspaced sub-line beneath the mark:

```
L A B O R A T O R I E S   I N C .
```

- Tracking `.55em` (`--tracking-wordmark`)
- Uppercase, weight `400` — **not** bold; the mark above carries the weight
- Optically centred under the wordmark. Because `.55em` adds trailing space after the
  final character, subtract roughly half the tracking value from the right side or it
  will sit visibly left-of-centre.
- Size: about 1/8 the height of the wordmark's cap height

Full logo rules: [`04-logo.md`](04-logo.md).

---

## 7 · Glyphs, not icons

The system has **no icon font and no icon set.** Meaning is carried by characters that
JetBrains Mono already contains:

```
▸  list bullets (accent-coloured)
✓  pass / yes            ✕  fail / no            !  warning
→  flow, forward         ↓  flow, stacked        ▾  disclosure caret
◆  diamond marker        ♻  the loop             ✉  contact
```

No emoji beyond `♻` and `✉`, which are established site glyphs and render monochrome in
this context. Everything else that looks like an icon is a **hand-built SVG line diagram**
in brand colours — see [`05-patterns.md`](05-patterns.md#diagrams).

---

## 8 · Numbers, units and placeholders

- Units get a space: `14.46 Wh`, `45 × 13 mm`, `230 V`. Use `×` (U+00D7), not `x`.
- Ranges use an en dash with no spaces: `56–62ch`, `400–800`.
- Document control: `DOC NO. RL-000-A`, `REV. A`, `SEC.03`, `EST. 2026`.
- The ticker: `PARRY · RIPOSTE · RECYCLE · REPEAT ♻`
- **Placeholders are honest and loud.** `$[TAM]`, `[Q_/__]`, flagged
  `⚠ Illustrative — replace before sending`. A placeholder that looks like real data is a
  liability; make it impossible to ship by accident.

---

## 9 · Setting type in tools that aren't a browser

Sizes here are CSS pixels. For fixed-size media:

| Context | Body | H2 | Notes |
|---|---|---|---|
| Web | `15–16px` | `clamp(24px, 3.2vw, 40px)` | As specified above |
| Slides (16:9, 1920×1080) | `22–24px` | `54–64px` | Display statements 90–120px |
| A4 / Letter print | `9.5–10pt` | `18–22pt` | See [`08-print.md`](08-print.md) |
| Canva (1080×1080 social) | `28px` | `64px` | See [`../tools/canva.md`](../tools/canva.md) |

The ratios hold even when the absolute sizes don't: display is ~4× body, h2 is ~2.5× body,
labels are ~0.7× body.
