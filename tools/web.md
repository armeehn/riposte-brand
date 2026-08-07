# Web & apps

**DOC NO. RL-BRAND-001-WEB · REV. A**

---

## 1 · Drop it in

```html
<link rel="stylesheet" href="https://ripostelabs.xyz/brand/riposte-brand.css">
```

Or vendor it — copy [`../brand/riposte-brand.css`](../brand/riposte-brand.css) into the
project. One file: tokens, a base layer, and every pattern class.

Minimum viable page:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Thing · Riposte Laboratories</title>
  <link rel="stylesheet" href="/brand/riposte-brand.css">
</head>
<body>
  <header class="pagehead">
    <div class="inner">
      <div class="kicker">Riposte Laboratories</div>
      <h1>Thing</h1>
      <p>One sentence saying what it is and what it counters.</p>
    </div>
  </header>

  <main class="wrap section">
    <div class="sechead"><span class="no" aria-hidden="true">SEC.01</span>
      <h2>Overview</h2>
      <span class="tag" aria-hidden="true">// what this is</span></div>
    <p class="lead">The bold lead paragraph.</p>
    <p>Body copy. Bold the numbers that matter: <b>14.46 Wh</b>.</p>
  </main>

  <div class="checker" aria-hidden="true"></div>

  <footer class="colophon">
    <div class="l">&copy; 2026 Riposte Laboratories Inc. &middot; All rights reserved.</div>
    <div class="r">parry &#9851; riposte &#9851; recycle &#9851; repeat</div>
  </footer>
</body>
</html>
```

---

## 2 · Self-hosting the font

The CDN `@import` at the top of the stylesheet is the zero-config path — fine for
prototypes, artifacts and internal tools. For production, self-host: it's faster, it works
offline, and it doesn't leak visitors to a third party.

The subsets are in [`../assets/fonts/`](../assets/fonts/). Copy them to `/fonts/`, delete
the `@import` line, and use:

```css
@font-face{font-family:"JetBrains Mono";font-style:normal;font-weight:400 800;font-display:swap;
  src:url(/fonts/jetbrains-mono-latin.woff2) format("woff2");
  unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,
                U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,
                U+2212,U+2215,U+FEFF,U+FFFD;}
```

Preload only the latin subset; the others fetch lazily via `unicode-range`. `crossorigin`
is required even same-origin — fonts are always fetched in anonymous CORS mode, so omitting
it causes a duplicate fetch:

```html
<link rel="preload" href="/fonts/jetbrains-mono-latin.woff2" as="font" type="font/woff2" crossorigin>
```

---

## 3 · Fields

Any element can carry a field. They nest correctly.

```html
<section data-theme="dark">   <!-- ink field: bone text, bone rules, teal accent -->
<section class="pinkfield">   <!-- full pink: everything bone, ink labels -->
<div data-theme="light">      <!-- bone island inside a dark subtree -->
```

Everything in the stylesheet reads semantic variables, so patterns invert for free. If a
component doesn't invert, it's because it hardcoded `--ink` or `--pink` where it should have
used `--text` or `--accent`.

**System dark mode is not wired up by default** — the brand's dark field is an editorial
choice (a section that *should* be ink), not a user preference. If a product genuinely needs
`prefers-color-scheme`, opt in explicitly:

```css
@media (prefers-color-scheme: dark) { :root { /* copy the [data-theme="dark"] block */ } }
```

---

## 4 · Tailwind

```js
// tailwind.config.js
module.exports = { presets: [require('./brand/tailwind.preset.js')] };
```

Gives you `bg-ink`, `text-bone`, `border-pink`, `shadow-pop`, `bg-triband`,
`tracking-kicker`, `max-w-measure`, `duration-snap`, and friends. The preset forces
**every** `borderRadius` value to `0`, so `rounded-lg` is a no-op — deliberately.

The preset covers tokens only. For patterns (`.spec`, `.verdict`, `.colophon`, the bands),
load `riposte-brand.css` alongside it.

## 5 · Sass

```scss
@use 'brand/tokens' as rl;
.thing { background: rl.$rl-bone; border: 2px solid rl.$rl-ink; }
```

## 6 · JS / design tokens

[`../brand/tokens.json`](../brand/tokens.json) is the source of truth — colour, type scale,
spacing, tracking, effects, motion, logo geometry, glyphs, fixed strings. Feed it to Style
Dictionary or import it directly. [`../palettes/riposte.json`](../palettes/riposte.json) is
a flat `name → hex` map if that's all you need.

---

## 7 · Non-negotiables in code

```css
/* radius */          border-radius: 0;            /* always */
/* structural rule */ border: 2px solid var(--line);
/* divider */         border-bottom: 1px dashed var(--line-dashed);
/* hover pop */       transform: translate(-2px,-2px); box-shadow: 4px 4px 0 var(--pink);
```

Never:
- a `border-radius` other than 0
- a `box-shadow` with a non-zero blur radius
- a second font family
- `rgba()` tints of an accent to fake a lighter shade
- a fourth accent colour

**Body copy never sits on `--pink` or `--teal`.** Those fills are 3.16:1 and 2.27:1 against
bone. Use `--pink-deep` / `--teal-deep`, or put ink on marigold (8.12:1). See
[`../docs/07-accessibility.md`](../docs/07-accessibility.md).

---

## 8 · Charts

Load the `dataviz` guidance, then substitute the Riposte palette. Categorical series in
rotation: `pink → orange → teal → ink → bone-dim`. Beyond five, add the `-deep` variants;
beyond eight, the chart is wrong — split it or use a table.

Flat fills, 2px borders, no gridlines, no gradients, no drop shadows. Direct-label where
possible instead of relying on a legend, and never encode meaning in colour alone.

---

## 9 · Performance

- One font family, three weights, `font-display: swap`
- No icon font — glyphs and inline SVG only
- No JS required for anything visual; the marquee is CSS
- The whole stylesheet is a single file with no build step
- `@media (prefers-reduced-motion: reduce)` is already handled

---

## 10 · Checklist

- [ ] `riposte-brand.css` linked or vendored
- [ ] Font self-hosted (production) and latin subset preloaded with `crossorigin`
- [ ] `footer.colophon` present
- [ ] Decorative bands `aria-hidden="true"`
- [ ] `SEC.NN` chips and corner marks `aria-hidden="true"`
- [ ] Uppercase via `text-transform`, not typed
- [ ] `node scripts/build.js --check` passes if tokens were touched
