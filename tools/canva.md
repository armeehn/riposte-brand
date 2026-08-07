# Canva

**DOC NO. RL-BRAND-001-CANVA · REV. A**

Canva can't import a swatch file, so this is a copy-paste setup. Fifteen minutes once, then
every future design starts on-brand.

---

## 1 · Brand Kit — colours

**Brand → Brand Kits → Add new → Colour palette.** Create **three separate palettes** so the
rotation rule stays visible in the picker. Add colours by clicking `+`, then pasting the hex
including the `#`.

### Palette 1 — `RIPOSTE / BASE`

```
#1D1A17
#241F1B
#2B2723
#5C554C
#F6F1E7
#EAE4D6
#FFFFFF
```

### Palette 2 — `RIPOSTE / ACCENT`

Add these **in this order**. Canva shows palette colours in insertion order, and the order
*is* the rotation rule: pink → marigold → teal.

```
#F0477D
#FE9A0D
#12B795
```

### Palette 3 — `RIPOSTE / ACCENT DEEP`

For any accent surface that has to carry a **sentence**.

```
#D81150
#A15E01
#0C7A63
#04463A
```

> **The rule you will break first.** Bone text on the bright pink or teal is *brand-correct*
> but only legible at large uppercase sizes. The moment coloured fill sits under a
> paragraph, switch the fill to a `DEEP` colour. On marigold, use **ink** `#1D1A17` text —
> never bone. Details: [`../docs/07-accessibility.md`](../docs/07-accessibility.md).

---

## 2 · Brand Kit — fonts

**Brand → Brand Kits → Fonts → Upload a font.** (Requires Canva Pro. JetBrains Mono is
SIL OFL licensed, so uploading and embedding it is explicitly permitted.)

1. Download from [jetbrains.com/lp/mono](https://www.jetbrains.com/lp/mono/) — or use the
   `.ttf` files from the JetBrains release.
2. Upload **Regular (400)**, **Bold (700)** and **ExtraBold (800)**. Just those three.
3. Set Brand Kit font styles:

| Canva slot | Font | Size (1080×1080) | Settings |
|---|---|---|---|
| Heading | JetBrains Mono **Bold** | 64 | ALL CAPS, letter spacing **30** |
| Subheading | JetBrains Mono **Bold** | 32 | ALL CAPS, letter spacing **80** |
| Body | JetBrains Mono **Regular** | 28 | Sentence case, spacing **0**, line height **1.55** |

**No Canva Pro?** Use **Space Mono** — closest in flavour. Then Roboto Mono, then Courier
Prime. Never Arial, Montserrat, or anything Canva suggests. Note the substitution when you
share the file.

---

## 3 · Canva letter-spacing conversion

Canva's letter-spacing slider is in **units of 1/1000 em**, so multiply the CSS value by
1000:

| Role | CSS | Canva |
|---|---|---|
| Display | `-.01em` | **−10** |
| Headings | `.03em` | **30** |
| Nav / buttons | `.08em` | **80** |
| Labels, doc numbers | `.1em` | **100** |
| Slash tags, corner marks | `.14em` | **140** |
| Spec headers, stamps | `.16em` | **160** |
| Page-head kickers | `.3em` | **300** |
| `L A B O R A T O R I E S` | `.55em` | **550** |

---

## 4 · The three things Canva gets wrong by default

### Rounded corners → set to 0

Canva rounds corners on many shapes and every image frame. **Radius is 0 in this brand,
without exception.** Select the element → corner-rounding slider → **0**. Use the square
frame, never the rounded one.

### Shadows → off

Canva's shadow effects are all blurred. **The brand has no blur.** Turn every shadow off.

To get the brand's hard offset instead: duplicate the shape, fill the copy with the accent,
send it backward, nudge it **+4px right and +4px down**. That's `4px 4px 0` — the real
effect.

### Font suggestions → ignore

Canva will offer to "improve" the pairing with a display face. There is no second family.

---

## 5 · Rebuilding the signature patterns

Canva has no conic gradients, so build these once and save them as Brand Kit elements.

### Tri-band (page heads, footer cell)

The only one Canva does natively.

1. Rectangle → **Gradient** fill → **Linear**, angle **105°**
2. Three stops, hard: `#F0477D` at 0–36%, `#FE9A0D` at 36–64%, `#12B795` at 64–100%
3. Drag the stops so there's **no visible blend** — Canva will try to smooth them. Place
   two stops of the same colour adjacent at each boundary if it won't hold a hard edge.

### Checker band

1. Draw a `22 × 22 px` ink square (`#1D1A17`)
2. Duplicate into a 2×2 block: ink top-left, ink bottom-right, bone (`#F6F1E7`) on the other
   diagonal
3. Group, then duplicate across to a strip **26 px tall** (22px tile + 2px rule top and
   bottom)
4. Add `2px` ink lines above and below
5. **Save to Brand Kit → Elements**, named `RL / CHECKER BAND`

### Harlequin band

Same method, `34 × 34 px` diamonds (the square rotated 45°) alternating `#F0477D` /
`#12B795`, band height **38 px**, `2px` ink rules top and bottom.

**Band rules:** strips only, never large fields. Alternate checker and harlequin down a
page. Never two identical bands in a row.

---

## 6 · Logo

Upload all three to **Brand → Logos**:

| File | Use on |
|---|---|
| `assets/logo/riposte-ink.svg` | bone, bone-dim, white |
| `assets/logo/riposte-bone.svg` | ink fields, pink fields |
| `assets/logo/riposte-pink.svg` | accent moments only |

- **Clear space:** one cap-height of the wordmark on all four sides. Nothing enters it.
- **Minimum width:** 110px on screen, 28mm in print.
- Scale proportionally — hold **Shift**. Aspect ratio is 4.528:1.
- Never recolour, rotate, crop esh out, or put the mark inside a shape.

Full rules: [`../docs/04-logo.md`](../docs/04-logo.md).

---

## 7 · Sizes for common Canva artboards

| Artboard | Body | Sub | Heading | Display | Margin |
|---|---|---|---|---|---|
| Instagram post 1080×1080 | 28 | 32 | 64 | 120 | 64 |
| Instagram story 1080×1920 | 32 | 36 | 72 | 140 | 80 |
| Presentation 1920×1080 | 24 | 28 | 56 | 110 | 80 |
| A4 document | 10pt | 11pt | 20pt | 36pt | 15mm |
| Business card 85×55mm | 7pt | 8pt | — | — | 5mm |

Spacing on a 1080 artboard: `16px → 24` · `34px → 48` · `64px → 96`. Keep the ratios; the
absolute values scale with the canvas.

---

## 8 · The colophon

Close every multi-page Canva document the same way the website does:

1. A `2px` ink rule across the full width
2. Below it, two equal cells, full-bleed:
   - **Left:** ink fill `#1D1A17`, bone text — `© 2026 RIPOSTE LABORATORIES INC. · ALL RIGHTS RESERVED.`
   - **Right:** the tri-band gradient, **ink** text, right-aligned, bold — `PARRY ♻ RIPOSTE ♻ RECYCLE ♻ REPEAT`
3. Both at 11–12px (scaled to artboard), ALL CAPS, letter spacing **100**

Save it as a Brand Kit element: `RL / COLOPHON`.

---

## 9 · Setup checklist

- [ ] Three colour palettes added, accents in rotation order
- [ ] JetBrains Mono 400/700/800 uploaded (or substitution noted)
- [ ] Brand Kit text styles set with the right letter spacing
- [ ] All three logo files uploaded
- [ ] `RL / CHECKER BAND`, `RL / HARLEQUIN BAND`, `RL / COLOPHON` saved as elements
- [ ] Corner rounding 0 on your default shapes
- [ ] Shadows off

## 10 · Per-design checklist

- [ ] Radius 0 on every element
- [ ] No blurred shadows — hard offsets only
- [ ] Accents rotating pink → marigold → teal, none repeated out of order
- [ ] Ink text on marigold; bone on pink/teal **only at display size**
- [ ] Body copy on a `DEEP` fill, or on bone/ink
- [ ] Bands are strips, alternating, never large fields
- [ ] Logo clear space respected
- [ ] Colophon on the last page
- [ ] No exclamation marks, numbers bolded — [`../docs/06-voice.md`](../docs/06-voice.md)
