# Google Docs, Slides & Sheets

**DOC NO. RL-BRAND-001-GWS · REV. A**

Google Workspace can't upload fonts and its theming is shallow, so this is the most
compromised surface the brand runs on. Build the templates once, then copy them.

---

## 1 · Font

Google Fonts includes **JetBrains Mono**, but it isn't in the Docs/Slides font menu by
default. Add it:

**Font dropdown → More fonts → search "JetBrains Mono" → add.**

If it doesn't appear on your account, use **Roboto Mono** — natively available and the
safest cross-platform fallback. Note the substitution when you share the file.

---

## 2 · Custom colours

Google's colour picker has no palette import. Enter hex values once via
**Custom → hex field** and they'll stay in your recent-colours row for that document. Copy
the finished document rather than re-entering them.

```
INK          #1D1A17      BONE          #F6F1E7
INK RAISED   #241F1B      BONE DIM      #EAE4D6
INK LINE     #5C554C      WHITE         #FFFFFF

PINK         #F0477D      PINK DEEP     #D81150
MARIGOLD     #FE9A0D      MARIGOLD DEEP #A15E01
TEAL         #12B795      TEAL DEEP     #0C7A63
```

**Text on accent fills:** bone on pink, **ink on marigold**, bone on teal — and only at
large uppercase sizes. Body copy on a coloured fill needs a `DEEP` colour underneath it.

---

## 3 · Slides

**Slide → Edit theme** — do this once, then reuse the deck as a template.

### Theme setup

| Setting | Value |
|---|---|
| Page size | Widescreen 16:9 |
| Background | `#F6F1E7` |
| Text | `#1D1A17` |
| Font | JetBrains Mono (or Roboto Mono) |

### Type on a 1920×1080 slide

| Role | Size | Weight | Case |
|---|---|---|---|
| Display / cover statement | 90–110 | Bold | UPPER |
| Slide title | 44–54 | Bold | UPPER |
| Sub-heading | 28 | Bold | UPPER |
| Body | 22–24 | Regular | Sentence |
| Label / chrome | 12–14 | Bold | UPPER |

Google Slides has **no letter-spacing control**. Two options for the tracked chrome:

1. Type spaces between characters: `S E C . 0 3`. Ugly to edit, right on the eye.
2. Accept untracked labels. Better than faking it with a different font.

### Slide furniture

- **Corner marks:** a 12pt text box top-left `DOC NO. RL-000-A`, top-right `REV. A`,
  bottom-right the slide number. 75% opacity.
- **Checker band:** insert `assets/patterns/checker-band.png` (or build a 22px square, group
  a 2×2, duplicate across).
- **Section dividers:** full-bleed ink rectangle, bone title. This is the ink field.
- **Corner rounding: 0.** Shape options → shape → the square, never the rounded rectangle.
- **Shadows off.** Format options → uncheck Drop shadow, on every element.

### Master slides to build

1. **Cover** — mark, display statement, corner marks
2. **Section** — ink field, `SEC.NN` chip, uppercase title
3. **Content** — `SEC.NN` chip + title + slash tag, 2px rule, content area
4. **Quote** — 8px pink left bar, bold 32pt, attribution below
5. **Closing** — colophon: ink cell left, tri-band cell right

---

## 4 · Docs

### Styles (Format → Paragraph styles → Options → Save as my default styles)

| Style | Font | Size | Weight | Colour | Case |
|---|---|---|---|---|---|
| Title | JetBrains Mono | 28 | Bold | `#1D1A17` | UPPER |
| Heading 1 | JetBrains Mono | 20 | Bold | `#1D1A17` | UPPER |
| Heading 2 | JetBrains Mono | 16 | Bold | `#1D1A17` | UPPER |
| Heading 3 | JetBrains Mono | 13 | Bold | `#1D1A17` | UPPER |
| Normal | JetBrains Mono | 10 | Regular | `#1D1A17` | Sentence |

Line spacing **1.5**, space after paragraph **8pt**, margins **20mm** all round.

### Furniture

- **Header:** `DOC NO. RL-000-A` left, `REV. A` right, 8pt, 75% grey
- **Footer:** `© 2026 RIPOSTE LABORATORIES INC.` left, page number right, 8pt
- **Horizontal rules:** Docs' `---` rule is a hairline and reads as nothing. Use a
  **1×1 table with only a top border set to 1.5pt `#1D1A17`** instead.
- **Callouts:** 1×1 table, background `#EAE4D6`, left border **6pt `#FE9A0D`**, others none.
- **Tables:** header row `#EAE4D6`, header text uppercase bold, 1.5pt bottom border on the
  header, 0.5pt dashed between rows.

---

## 5 · Sheets

- Header row: `#1D1A17` background, `#F6F1E7` bold uppercase text
- Banding: off. Use a 0.5pt bottom border per row instead — the brand separates with rules,
  not fills
- Conditional formatting: pass `#12B795`, warn `#FE9A0D`, fail `#F0477D` — always with a
  `✓ ! ✕` glyph in an adjacent column, never colour alone
- Charts: flat accent fills in rotation, no gradients, no 3-D, no drop shadows, gridlines off

---

## 6 · Known limits

| Limit | Do this |
|---|---|
| No letter spacing in Slides | Space characters manually, or accept untracked |
| No conic gradients | Insert the band images from `assets/patterns/` |
| No font upload | Add JetBrains Mono via More fonts; else Roboto Mono |
| Shallow theming | Build the template once and **copy the file**, don't rebuild |
| Rounded shapes by default | Always pick the square variant, rounding 0 |

---

## 7 · Checklist

- [ ] JetBrains Mono added (or Roboto Mono, noted)
- [ ] Custom hex values entered
- [ ] Bone background, ink text — not white/black
- [ ] Radius 0, shadows off
- [ ] Rules at 1.5pt, not hairlines
- [ ] Accents rotating in order
- [ ] Colophon on the last slide / in the footer
