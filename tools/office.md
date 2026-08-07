# Word · PowerPoint · Excel

**DOC NO. RL-BRAND-001-OFFICE · REV. A**

Office has a real theme format, so unlike Google Workspace you can set this up once
properly and hand the theme file around.

---

## 1 · Font

Install **JetBrains Mono** (400 / 700 / 800) on every machine that will open the file, or
**embed it** — Word and PowerPoint both support font embedding, and the SIL OFL permits it.

*File → Options → Save → Embed fonts in the file* (Windows).
On Mac, embedding is unavailable in some versions — export to PDF for distribution.

**Fallback if you can't install:** **Consolas**, which ships with Office everywhere. Note
the substitution.

---

## 2 · Build the theme

*Page Layout / Design → Colors → Customize Colors…*

| Theme slot | Colour | Hex |
|---|---|---|
| Text/Background – Dark 1 | Ink | `#1D1A17` |
| Text/Background – Light 1 | Bone | `#F6F1E7` |
| Text/Background – Dark 2 | Ink Head | `#2B2723` |
| Text/Background – Light 2 | Bone Dim | `#EAE4D6` |
| Accent 1 | Pink | `#F0477D` |
| Accent 2 | Marigold | `#FE9A0D` |
| Accent 3 | Teal | `#12B795` |
| Accent 4 | Pink Deep | `#D81150` |
| Accent 5 | Marigold Deep | `#A15E01` |
| Accent 6 | Teal Deep | `#0C7A63` |
| Hyperlink | Pink Deep | `#D81150` |
| Followed hyperlink | Teal Deep | `#0C7A63` |

Accents 1–3 in that order **is** the rotation rule — Office cycles them automatically for
chart series and SmartArt, which means charts come out on-brand for free.

Then *Fonts → Customize Fonts…* → both heading and body **JetBrains Mono**.

Save as **Riposte** (`.thmx`) and distribute it. It applies to Word, PowerPoint and Excel.

---

## 3 · PowerPoint

Widescreen 16:9. Background `#F6F1E7`, text `#1D1A17`.

| Role | Size | Weight | Case | Spacing |
|---|---|---|---|---|
| Cover statement | 90–110 | ExtraBold | UPPER | −1 |
| Slide title | 44–54 | Bold | UPPER | 1.5 |
| Sub-heading | 28 | Bold | UPPER | 2 |
| Body | 22–24 | Regular | Sentence | 0 |
| Label / chrome | 12–14 | Bold | UPPER | 2.5 |

PowerPoint's character spacing is in **points**, not em. Multiply the em value by the font
size: at 12pt, `.1em` → **1.2pt**; at 44pt, `.03em` → **1.3pt**. *Font → Advanced →
Spacing: Expanded By.*

### Slide masters to build

1. **Cover** — mark, display statement, corner marks (`DOC NO. RL-000-A`, `REV. A`)
2. **Section** — ink fill, `SEC.NN` chip, uppercase title
3. **Content** — chip + title + slash tag, 2.25pt rule beneath, content area
4. **Quote** — 6pt pink left bar, bold 32pt
5. **Closing** — colophon: ink rectangle left, tri-band right

### Shape defaults

- **Rounded corners → 0.** Use the rectangle, never the rounded rectangle. If you must use
  a rounded one, drag the yellow handle fully to the left.
- **Shadows off.** *Format Shape → Effects → Shadow → No shadow*, on every element. Then
  right-click a correctly-formatted shape → **Set as Default Shape**.
- **Hard offset instead:** duplicate the shape, fill with an accent, send backward, nudge
  right 4px and down 4px.
- **Lines:** 2.25pt structural, 0.75pt dashed dividers.

### Tri-band
Rectangle → *Format Shape → Fill → Gradient*, angle **105°**, six stops:
pink @0%, pink @36%, marigold @36%, marigold @64%, teal @64%, teal @100%. The doubled stops
are what make the boundaries hard.

---

## 4 · Word

Modify the built-in styles so they carry the brand — don't apply direct formatting.

| Style | Font | Size | Weight | Colour | Case |
|---|---|---|---|---|---|
| Title | JetBrains Mono | 28 | Bold | Ink | UPPER |
| Heading 1 | JetBrains Mono | 20 | Bold | Ink | UPPER |
| Heading 2 | JetBrains Mono | 16 | Bold | Ink | UPPER |
| Heading 3 | JetBrains Mono | 13 | Bold | Ink | UPPER |
| Normal | JetBrains Mono | 10 | Regular | Ink | Sentence |
| Caption | JetBrains Mono | 8 | Bold | Ink 65% | UPPER |

Line spacing 1.5, space after 8pt, margins 20mm. Page colour `#F6F1E7` — but note Word won't
print a background colour unless *Options → Display → Print background colours and images*
is on. For anything going to press, put the bone on the stock instead
([`../docs/08-print.md`](../docs/08-print.md#5--paper)).

- **Header:** `DOC NO. RL-000-A` left, `REV. A` right, 8pt
- **Footer:** `© 2026 RIPOSTE LABORATORIES INC.` left, page number right, 8pt
- **Rules:** a paragraph border, **1.5pt** — Word's default horizontal line is a hairline
  and disappears
- **Callouts:** 1×1 table, shading `#EAE4D6`, left border 6pt marigold, others none
- **Tables:** header row `#EAE4D6`, uppercase bold, 1.5pt bottom border; 0.5pt dashed between rows

---

## 5 · Excel

- Header row: ink fill, bone bold uppercase text
- No banded fills. A 0.5pt bottom border per row instead
- Conditional formatting: pass `#12B795`, warn `#FE9A0D`, fail `#F0477D`, always paired with
  a `✓ ! ✕` glyph in an adjacent column
- Charts: theme accents 1–3 give the rotation automatically. Turn off gridlines, gradients,
  3-D and shadows. Set every series border to 2.25pt ink

---

## 6 · Checklist

- [ ] `Riposte.thmx` built and applied
- [ ] JetBrains Mono installed or embedded (or Consolas, noted)
- [ ] Rounded corners 0; default shape set
- [ ] Shadows off everywhere
- [ ] Lines ≥ 1.5pt
- [ ] Accents 1–3 in rotation order so charts inherit it
- [ ] Colophon on the last slide / in the footer
