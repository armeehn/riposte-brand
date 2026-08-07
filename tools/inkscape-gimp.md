# Inkscape · GIMP · Krita · Scribus

**DOC NO. RL-BRAND-001-FOSS · REV. A**

The open-source stack, which is where most Riposte production artwork actually gets made.

---

## 1 · Install the palette

[`../palettes/riposte.gpl`](../palettes/riposte.gpl) — the GIMP palette format, shared by
Inkscape, GIMP and Krita.

| App | Install to |
|---|---|
| Inkscape (Linux) | `~/.config/inkscape/palettes/` |
| Inkscape (macOS) | `~/Library/Application Support/org.inkscape.Inkscape/config/inkscape/palettes/` |
| Inkscape (Windows) | `%APPDATA%\inkscape\palettes\` |
| GIMP | `~/.config/GIMP/2.10/palettes/` (or `3.0`) |
| Krita | Settings → Manage Resources → Import Resource |

```bash
# Linux, both at once
cp palettes/riposte.gpl ~/.config/inkscape/palettes/
cp palettes/riposte.gpl ~/.config/GIMP/2.10/palettes/
```

Restart. In Inkscape, pick **Riposte Laboratories** from the palette selector at the far
right of the swatch strip. In GIMP, *Windows → Dockable Dialogs → Palettes*.

**Scribus** reads GPL too: *Edit → Colours and Fills → Import → riposte.gpl*.

---

## 2 · Font

Install JetBrains Mono system-wide:

```bash
# Debian / Ubuntu
sudo apt install fonts-jetbrains-mono
# Arch
sudo pacman -S ttf-jetbrains-mono
# manual, any Linux
mkdir -p ~/.local/share/fonts && cp JetBrainsMono-*.ttf ~/.local/share/fonts/ && fc-cache -f
```

Verify: `fc-list | grep -i jetbrains`

---

## 3 · Inkscape

### Document
*File → Document Properties* — background `#F6F1E7FF` (note the alpha byte), display units
px, and enable a **2px grid** to match the system's spacing scale.

### Objects
- **Rectangles: `Rx`/`Ry` = 0.** Inkscape remembers the last corner radius you used, so
  reset it explicitly or every new rectangle inherits it.
- **Strokes:** 2px structural, 1px dashed dividers, 6px accent top bars, 8px left bars.
  Set *Stroke style → Join: miter*, *Cap: butt* — round joins soften the corners you just
  squared off.
- **No filters.** Inkscape's blur slider and every entry in *Filters → Shadows and Glows*
  are off-limits.
- **Hard offset:** duplicate (`Ctrl+D`), fill with the accent, *Page Down*, then
  `Transform → Move` by `4, 4` px.

### The three patterns
- **Checker:** 22px square → duplicate into a 2×2 alternating block → select →
  *Object → Pattern → Objects to Pattern* (`Alt+I`). Band 26px with 2px ink rules.
- **Harlequin:** 34px squares rotated 45°, alternating pink/teal → same pattern step.
  Band 38px.
- **Tri-band:** linear gradient at 105°, with **doubled stops** at 36% and 64% so the
  boundaries stay hard. Inkscape will interpolate otherwise.

### Export
- Web: *Export PNG*, 2× for retina; or Plain SVG (**not** Inkscape SVG — it carries editor
  cruft)
- Print: *Save As → PDF*, text as text with fonts embedded, 3mm bleed

---

## 4 · GIMP

Mostly for raster touch-up; the brand barely uses photography.

- Set the foreground colour from the palette dock rather than typing hex each time
- **No layer effects.** Every one is a blur, a bevel or a glow
- Text tool: JetBrains Mono, and set letter spacing in the tool options — GIMP's units are
  pixels, so at 12px, `.1em` ≈ **1.2px**
- Export PNG for flat artwork, never JPEG

---

## 5 · Krita

Charts, diagrams and illustration. Same rules: flat fills, hard edges, no blur, no
gradients except the three functional patterns. Import the GPL and work from it.

---

## 6 · Scribus

The FOSS print path. See [`../docs/08-print.md`](../docs/08-print.md) first.

- Import `riposte.gpl` via *Edit → Colours and Fills*
- Document: 15mm margins, 3mm bleed
- **Line weights ≥ 1.5pt.** Scribus will happily render a 0.25pt hairline that vanishes at
  press
- Master pages carry the corner marks and the colophon
- Export **PDF/X-4**, fonts embedded, bleed on, crop marks on

---

## 7 · Command line

Regenerate every palette export from `brand/tokens.json`:

```bash
node scripts/build.js
```

Convert artwork:

```bash
# SVG → PNG at 2x
inkscape logo.svg --export-type=png --export-width=1440 -o logo@2x.png

# SVG → PDF with text preserved
inkscape sheet.svg --export-type=pdf --export-text-to-path=false -o sheet.pdf

# recolour a logo variant (the three official fills)
sed 's/#1d1a17/#f6f1e7/g' assets/logo/riposte-ink.svg > riposte-bone.svg
```

---

## 8 · Checklist

- [ ] `riposte.gpl` installed and selected
- [ ] JetBrains Mono installed, `fc-cache` run
- [ ] Rectangle `Rx`/`Ry` reset to 0
- [ ] No blur filters anywhere
- [ ] Strokes: miter joins, butt caps, ≥1.5pt for print
- [ ] Plain SVG on export, not Inkscape SVG
- [ ] Colophon present
