# Logo & marks

**DOC NO. RL-BRAND-001-LOGO · REV. A**

---

## 1 · The wordmark

`RIPOSTE` set as a blackletter-derived wordmark with **esh** — the checkered jester figure,
she/her — integrated into the letterforms, caught mid-riposte.

**She is part of the wordmark, not an ornament attached to it. Never crop her out, never
separate her, never redraw her.**

| File | Fill | Use on |
|---|---|---|
| [`assets/logo/riposte-ink.svg`](../assets/logo/riposte-ink.svg) | `#1d1a17` | bone, bone-dim, white |
| [`assets/logo/riposte-bone.svg`](../assets/logo/riposte-bone.svg) | `#f6f1e7` | ink fields, pink fields |
| [`assets/logo/riposte-pink.svg`](../assets/logo/riposte-pink.svg) | `#f0477d` | accent moments only — rare |

Geometry: `viewBox="0 0 720 159"`, aspect ratio **4.528 : 1**.

Two harmonic variants exist for hero and sticker use, where esh's checker resolves into a
wave field: [`riposte-harmonic-ink.svg`](../assets/logo/riposte-harmonic-ink.svg) and
[`riposte-harmonic-bone.svg`](../assets/logo/riposte-harmonic-bone.svg). And
[`esh-ink.svg`](../assets/logo/esh-ink.svg) is esh standalone — for stickers, dies and
physical goods only, **not** as a logo substitute.

On ink fields the production site applies `filter: invert(1)` to the ink mark. That is
equivalent to `riposte-bone.svg` and is fine; prefer the real file where you can.

---

## 2 · Clear space

**One cap-height of the wordmark on all four sides.** Measure from the outermost ink, not
from the SVG bounding box — the file carries no padding.

```
┌─────────────────────────────┐
│         ↕ 1 cap-height      │
│   ┌───────────────────┐     │
│ ↔ │     RIPOSTE       │ ↔   │
│   └───────────────────┘     │
│         ↕                   │
└─────────────────────────────┘
```

Nothing enters that zone: no text, no rule, no image edge, no checker band. The one
sanctioned exception is the **topbar lockup**, where the letterspaced sub-line sits inside
the lower clear space by design (see §4).

---

## 3 · Minimum size

| Medium | Minimum width |
|---|---|
| Screen | **110px** |
| Print | **28mm** |
| Embroidery / moulded / engraved | **40mm** — below this, use `esh-ink.svg` alone |

Below the minimum, esh's checker fills merge and the mark turns to mud. There is **no
simplified small-size variant** and **no monogram**. If a favicon or app icon is needed,
that's an open task — do not improvise one by cropping the wordmark.

---

## 4 · The lockup

```
        RIPOSTE
L A B O R A T O R I E S   I N C .
```

- Sub-line: uppercase, weight **400** (not bold — the mark carries the weight)
- Tracking **`.55em`** (`--tracking-wordmark`)
- Cap height ≈ **1/8** of the wordmark's cap height
- **Optically centred.** `.55em` tracking adds trailing space after the final character,
  so subtract about half the tracking from the right or it sits visibly left of centre.

**Topbar variant** (production site): mark at `110px`, then a stacked cell —
`Laboratories Inc.` over `RL-000 · Rev.A` — separated by a dashed interior rule. This is
the only lockup that pairs the mark with document-control chrome.

---

## 5 · Backgrounds

| Background | Mark |
|---|---|
| `bone` / `bone-dim` / `white` | `riposte-ink.svg` |
| `ink` field | `riposte-bone.svg` |
| `pink` field | `riposte-bone.svg` |
| `marigold` or `teal` fill | `riposte-ink.svg` — but reconsider; the mark doesn't belong on a small accent fill |
| Photograph | Only on a flat, high-contrast, near-monochrome area. Otherwise put the mark on a bone or ink block first. |

**Hero treatment:** the mark may take `--mark-drop`
(`drop-shadow(5px 5px 0 rgba(234,228,214,.9))`) — a hard bone-dim offset, no blur. Hero
fields only, once per page.

---

## 6 · Misuse

Do not:

- **Recolour** it outside the three fills. No gradients. No photo fills. No outline-only.
- **Distort** it. Scale proportionally; the aspect ratio is 4.528:1 and stays there.
- **Rotate** it. The only rotation in the system is `.stamp` at `-2deg`, and that's a stamp.
- **Crop esh out**, isolate her *as the logo*, or redraw her.
- **Add effects** — glow, bevel, blur, drop shadow other than `--mark-drop`.
- **Re-typeset** it. The wordmark is artwork, not JetBrains Mono. Never set "RIPOSTE" in
  the brand font and call it the logo.
- **Put it inside a shape.** No circles, no rounded containers, no badges. Radius is 0 and
  the mark needs no holder.
- **Pair it with another wordmark** without a `2px` ink rule and one clear-space unit
  between them.

---

## 7 · Company name in text

- Full legal: **Riposte Laboratories Inc.**
- Second reference: **Riposte Labs**, or **Riposte**
- Never: "RipostéLabs", "riposte labs" mid-sentence, "RL" as a standalone brand
- Products: **Plastic Works** (injection moulding), **Project HEX** (battery tiles) —
  title case, both, as proper nouns
- **esh** is lowercase, always, even sentence-initial. She/her.
- Domain: `ripostelabs.xyz`
