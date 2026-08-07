# Illustrator · InDesign · Photoshop · Affinity

**DOC NO. RL-BRAND-001-ADOBE · REV. A**

The best-supported surface: real swatch import, real typography, real print output.

---

## 1 · Load the palette

[`../palettes/riposte.ase`](../palettes/riposte.ase) — 14 swatches in three groups
(`RIPOSTE / BASE`, `/ ACCENT`, `/ ACCENT DEEP`).

| App | How |
|---|---|
| Illustrator | Swatches panel → menu → **Open Swatch Library → Other Library…** |
| InDesign | Swatches panel → menu → **Load Swatches…** |
| Photoshop | Swatches panel → menu → **Import Swatches…** |
| Affinity (all) | Swatches panel → menu → **Import Palette → From File…** |

Also available: [`riposte.gpl`](../palettes/riposte.gpl),
[`riposte.sketchpalette`](../palettes/riposte.sketchpalette),
[`riposte.csv`](../palettes/riposte.csv), [`riposte.json`](../palettes/riposte.json).

**Document colour mode:**
- Screen → **RGB**, sRGB IEC61966-2.1
- Print → **CMYK**, and read [`../docs/08-print.md`](../docs/08-print.md) first. The ASE
  carries RGB values; converting to CMYK will shift **teal** hard. Specify spot inks for
  anything that matters.

---

## 2 · Type

Install **JetBrains Mono** (400 / 700 / 800). OFL — embedding in a PDF is permitted.

Character styles to build:

| Style | Size | Weight | Case | Tracking (‰) | Leading |
|---|---|---|---|---|---|
| Display | 74pt | ExtraBold | UPPER | **−10** | 102% |
| H1 | 54pt | Bold | UPPER | **30** | 115% |
| H2 | 40pt | Bold | UPPER | **30** | 115% |
| H3 | 30pt | Bold | UPPER | **30** | 115% |
| Lead | 19pt | Bold | — | 0 | 155% |
| Body | 15pt | Regular | — | 0 | 155% |
| Nav | 12pt | Bold | UPPER | **80** | 120% |
| Label | 11pt | Bold | UPPER | **100** | 120% |
| Tag | 11pt | Bold | UPPER | **140** | 120% |
| Spec | 11pt | Bold | UPPER | **160** | 120% |
| Kicker | 11pt | Bold | UPPER | **300** | 120% |
| Wordmark sub | — | Regular | UPPER | **550** | — |

Adobe and Affinity both measure tracking in **1/1000 em**, so the CSS `em` value × 1000 goes
straight in. Set case via the **All Caps** character attribute, not by typing caps.

For print sizes, see [`../docs/08-print.md`](../docs/08-print.md#4--type-on-paper) — 15pt
body is a screen value; on paper you want 9.5–10pt.

---

## 3 · Objects

- **Corner radius 0.** Set Live Corners to 0 and leave them there.
- **Strokes:** 2pt structural, 0.5pt dashed dividers, 6pt accent top bars, 8pt accent left
  bars. Align stroke to **outside** so the border doesn't eat the fill.
- **Effects: none.** No Drop Shadow, no Inner Glow, no Feather, no Gaussian Blur.
- **Hard offsets instead:** duplicate the object, fill with the accent, send backward,
  offset `+4pt / +4pt`. Or use *Effect → Distort & Transform → Transform* with Move
  `4pt/4pt` and 1 copy — non-destructive and editable.

---

## 4 · The three patterns

### Tri-band
Gradient, linear, **105°**, with paired stops so the boundaries are hard:
pink at 0% and 36%, marigold at 36% and 64%, teal at 64% and 100%.

### Checker
22pt ink square → 2×2 alternating block → **Object → Pattern → Make**. Band height 26pt
with 2pt ink rules top and bottom.

### Harlequin
34pt squares rotated 45°, alternating pink/teal, made into a pattern. Band height 38pt.

Save all three into a **Riposte** library (`.ai` CC Library / Affinity Assets).

---

## 5 · InDesign documents

| Setting | Value |
|---|---|
| Margins | 15mm minimum, 18mm preferred |
| Bleed | 3mm, bands extended into it |
| Baseline grid | Off. The system uses a stack order, not a baseline grid |
| Columns | Gutter 8mm (the print translation of 34px) |

Master pages carry the corner marks (`DOC NO.`, `REV.`), the page number, and the colophon
footer. Build paragraph styles from the table in §2 and never apply local overrides.

---

## 6 · Photoshop

Photoshop is for photo treatment, and the brand barely uses photography. If you must:

- Flat, high contrast, on bone. Never soft, never rounded, never vignetted.
- No layer styles — every one of them is a blur, a bevel or a glow.
- Export at 2× for screen. PNG for flat artwork, not JPEG.

---

## 7 · Export

| Target | Format |
|---|---|
| Web raster | PNG-24 (flat art), 2× for retina |
| Web vector | SVG, fonts converted to outlines **or** the CSS font stack referenced |
| Print | **PDF/X-4**, fonts embedded, 3mm bleed, crop marks |
| Office handoff | PDF, or PNG at 300dpi |

Before any print export, run the checklist in
[`../docs/08-print.md`](../docs/08-print.md#9--checklist) — especially the **1.5pt minimum
rule weight**.

---

## 8 · Checklist

- [ ] `riposte.ase` loaded
- [ ] JetBrains Mono installed, character styles built
- [ ] Radius 0, Live Corners 0
- [ ] No effects — hard offsets built from duplicated objects
- [ ] Strokes ≥ 1.5pt for print
- [ ] Accents rotating in order
- [ ] Colophon on the last page
