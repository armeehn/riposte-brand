# Print

**DOC NO. RL-BRAND-001-PRINT · REV. A**

The brand was designed as printed matter, so it prints well — but screen RGB and press CMYK
are different colour spaces and the accents are the ones that suffer.

---

## 1 · The honest warning about CMYK

The CMYK values in [`color-reference.md`](color-reference.md) and `palettes/riposte.csv`
are **naive device conversions**, computed arithmetically from RGB. They are a starting
point to hand a printer. They are **not** a colour specification.

Three of our colours sit outside or near the edge of the CMYK gamut:

| Colour | Problem on press |
|---|---|
| `teal` `#12B795` | Well outside CMYK gamut. Will print duller and darker than screen. The single biggest shift in the palette. |
| `pink` `#F0477D` | Near the gamut edge. Loses fluorescence; drifts toward a flatter rose. |
| `orange` `#FE9A0D` | Prints close, but can go muddy if the press pulls magenta. |

**Always ask for a physical proof** before a run of any size. Approve the proof, not the
numbers.

---

## 2 · Spot colour (recommended for anything that matters)

For business cards, stickers, packaging, labels and signage, specify **spot inks**. The
accents are the brand; a dull teal is a broken brand.

Starting points to confirm against a physical Pantone book under D50 light — **do not
approve from a screen**:

| Token | HEX | Nearest Pantone (Coated) — verify physically |
|---|---|---|
| `ink` | `#1D1A17` | Black 6 C, or Neutral Black C |
| `bone` | `#F6F1E7` | Warm Gray 1 C at low tint, or an uncoated natural stock |
| `pink` | `#F0477D` | 191 C / 1915 C |
| `orange` | `#FE9A0D` | 1375 C / 137 C |
| `teal` | `#12B795` | 3395 C / 339 C |

**Bone should usually be the paper, not an ink.** A warm uncoated natural stock is closer to
the brand than printing `#F6F1E7` onto white — and cheaper. See §5.

---

## 3 · Rule weights — the thing that breaks

The system is drawn in 2px screen rules. At print scale, translate as:

| Screen | Print | Why |
|---|---|---|
| `1px` dashed divider | **0.5pt** | Below this it drops out |
| `2px` solid structural rule | **1.5pt minimum**, 2pt preferred | **Do not go below 1pt.** The entire visual structure is these rules; if they vanish, the design vanishes |
| `6px` accent top bar | **3mm** | |
| `8px` accent left bar | **4mm** | |

Set all rules to **overprint off** and hold them at 100% of a single ink where possible —
a 1.5pt rule built from four-colour black will show registration fringing.

---

## 4 · Type on paper

| Role | Size | Notes |
|---|---|---|
| Body | **9.5–10pt** / 15pt leading | JetBrains Mono is wide; don't go below 9pt |
| `md` secondary | 8.5–9pt | |
| Labels, chrome | 7–7.5pt, `.1em` tracked | The tracking matters more in print, not less |
| h3 | 14–16pt | |
| h2 | 18–22pt | |
| h1 / page head | 28–36pt | |
| Display | 60pt+ | |

- **Embed the font.** JetBrains Mono is OFL — embedding and redistribution are permitted.
- Weight 400 for body, 700 for headings, 800 for display and stat figures.
- Ink text should be **100% K plus a touch of warmth** (e.g. `C0 M10 Y21 K89` from the
  conversion table) — not registration black, which cracks on folds and shows through.
- Reversed type (bone on ink) needs a **1pt minimum stroke weight**; at 7pt, tracked
  uppercase, thin strokes fill in with ink spread. Bump to 8pt reversed.

---

## 5 · Paper

The whole visual language is "printed on bone paper". Choose stock accordingly:

- **Uncoated, warm white or natural.** Not bright white, not coated gloss.
- Target something close to `#F6F1E7` in the stock itself. Then `bone` costs no ink and
  looks right by definition.
- Weights: 120–170 gsm text, 300–350 gsm cards and covers.
- **Avoid gloss.** The brand has no shine — no blur, no glow, no gradients. A soft-touch or
  uncoated finish is on-message; gloss lamination is not.
- Recycled and post-consumer stock is on-message in the most literal possible way. Say so
  in the colophon when you use it.

---

## 6 · Layout

| | |
|---|---|
| Margins | **15mm minimum, 18mm preferred** |
| Bleed | 3mm, with all bands and full-bleed fields extended into it |
| Spacing | `--space-4` → 4mm · `--space-6` → 8mm · `--space-8` → 15mm |
| Radius | **0.** Do not let a template round a corner |
| Bands | Checker 26px → **7mm** · Harlequin 38px → **10mm** |

Keep the `.pagehead` tri-band and the colophon footer. A printed Riposte document should be
recognisable as the same object as the web page.

---

## 7 · Web-to-print (`@media print`)

`brand/riposte-brand.css` ships a print block that:

- drops to true black on white (ink-on-bone at 15.39:1 is lovely on screen; on a home
  laser printer, bone becomes a grey wash)
- hides `.marquee`, `.checker` and `.harlequin` — decoration that wastes toner
- underlines links

If you're generating a PDF for actual press (not a desktop printer), **override that block**
and keep the real colours and bands. It exists for "someone hit Ctrl-P", not for production.

---

## 8 · Handing off to a printer

Send:

1. The artwork as **PDF/X-4**, fonts embedded, 3mm bleed, crop marks
2. [`palettes/riposte.ase`](../palettes/riposte.ase) — loads in Illustrator, InDesign,
   Affinity
3. [`palettes/riposte.csv`](../palettes/riposte.csv) — every value in every notation
4. This page

Ask for:

- A **physical proof** on the actual stock
- **Spot inks** for the three accents where budget allows
- Confirmation that **rules are holding at 1.5pt** and are not being auto-thinned

---

## 9 · Checklist

- [ ] Physical proof requested and approved on the real stock
- [ ] Structural rules ≥ 1.5pt
- [ ] Fonts embedded (OFL permits it)
- [ ] Radius 0 everywhere
- [ ] Bleed 3mm, bands extended into it
- [ ] Ink text is warm black, not registration black
- [ ] Reversed type ≥ 8pt
- [ ] Colophon present
- [ ] Teal checked on the proof specifically — it's the one that shifts most
