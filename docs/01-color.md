# Colour

**DOC NO. RL-BRAND-001-COLOR · REV. A**

Exact values, every notation, for every token:
**[`color-reference.md`](color-reference.md)** — generated from `brand/tokens.json`, so it
cannot drift.

This page is the *reasoning*. It tells you which colour to reach for and, more usefully,
which one not to.

---

## 1 · The story

An industrial spec sheet printed on bone paper, cut through with jester **mi-parti** —
the medieval convention of dividing a garment into contrasting halves. That is the whole
palette in one sentence:

- **The document** is ink on bone. Warm, printed, unglamorous, high contrast.
- **The jester** is pink, marigold and teal, applied in bands and blocks, never blended.

The tension between those two is the brand. Lose the ink-on-bone base and you get a
children's toy. Lose the accents and you get a tax form.

---

## 2 · Base — ink & paper

| Token | HEX | RGB | Use |
|---|---|---|---|
| `--ink` | `#1D1A17` | `29 26 23` | All text. All 2px rules. The dark field. |
| `--ink-raised` | `#241F1B` | `36 31 27` | Panel surface sitting on an ink field |
| `--ink-head` | `#2B2723` | `43 39 35` | Header fill on an ink field |
| `--ink-line` | `#5C554C` | `92 85 76` | Dashed dividers on an ink field. **Never text.** |
| `--bone` | `#F6F1E7` | `246 241 231` | The paper. Default background. |
| `--bone-dim` | `#EAE4D6` | `234 228 214` | Recessed paper: sunken panels, spec headers |
| `--white` | `#FFFFFF` | `255 255 255` | **One hero field per site.** That is the entire budget. |

**Why not `#000` on `#fff`?** Ink is a warm near-black (hue 30°, 12% saturation) and bone
is a warm off-white (hue 40°). Pure black on pure white is the default of every unstyled
document on earth; the 4-degree warm shift is what makes a Riposte page read as *printed
matter* rather than *a browser default*. It costs nothing — ink on bone is still 15.39:1.

**`ink-line` is a trap.** At `#5C554C` it hits 2.36:1 against ink. It is a divider colour.
If you catch yourself using it for de-emphasised text on a dark field, use
`--text-muted` instead, which is a `color-mix` guaranteed to stay legible.

---

## 3 · Accents — the mi-parti three

| Token | HEX | HSL | Text on it |
|---|---|---|---|
| `--pink` | `#F0477D` | `341 85% 61%` | `bone` |
| `--orange` | `#FE9A0D` | `35 99% 52%` | **`ink`** |
| `--teal` | `#12B795` | `168 82% 39%` | `bone` |

### They rotate. This is the rule people break.

The three accents are **equal citizens**. There is no primary. Across any repeated
element — cards, steps, section chips, top bars — cycle them in order using
`nth-child(3n)` or `nth-child(4n)`:

```css
.partner:nth-child(4n+1) { border-top: 6px solid var(--pink); }
.partner:nth-child(4n+2) { border-top: 6px solid var(--orange); }
.partner:nth-child(4n+3) { border-top: 6px solid var(--teal); }
.partner:nth-child(4n)   { border-top: 6px solid var(--line); }   /* ink, then repeat */
```

The 4-cycle (three accents plus ink) is preferred over the 3-cycle for cards, because the
ink beat stops the rotation from looking like a rainbow. Use the 3-cycle for small
elements — chips, `SEC.NN` numbers — where the ink beat would read as a disabled state.

**What "no favourite" means in practice:** `--accent` exists as a *working* accent for
one-off elements (a bullet glyph, an arrow, `.hi` emphasis) where rotation is meaningless.
It resolves to pink on bone and flips to teal on ink. That is the only sanctioned
asymmetry. It does not license a pink button and a pink heading and a pink underline on
the same page.

### Marigold is the odd one out, deliberately

`--orange` takes **ink** text; the other two take **bone**. This is not an aesthetic
whim — it is the contrast maths:

| | with `bone` | with `ink` |
|---|---|---|
| `pink` | 3.16:1 ✕ | 4.87:1 ✓ |
| `orange` | 1.90:1 ✕✕ | **8.12:1 ✓✓** |
| `teal` | 2.27:1 ✕✕ | 6.79:1 ✓ |

Marigold is far too light to hold bone text at any size. Ink on marigold is the single
best-contrasting accent pairing in the system, which is why marigold is the right choice
for `.note` callouts and warning states where the text actually has to be read.

---

## 4 · Deep accents — for accents that carry sentences

The bright three are **fill colours**. They are correct on chips, spec headers, section
bars, `.stat` numbers, and large uppercase display. They are wrong under a paragraph.

When a coloured surface has to hold body copy, or a colour has to *be* text on bone, use
the deep variant: identical hue and saturation, lightness dropped until bone clears
WCAG AA 4.5:1.

| Token | HEX | HSL | Bone on it |
|---|---|---|---|
| `--pink-deep` | `#D81150` | `341 85% 46%` | 4.53:1 ✓ |
| `--orange-deep` | `#A15E01` | `35 99% 32%` | 4.52:1 ✓ |
| `--teal-deep` | `#0C7A63` | `167 82% 26%` | 4.69:1 ✓ |
| `--teal-ink` | `#04463A` | `169 89% 15%` | 9.60:1 on `teal` — diagram labels |

`--teal-deep` and `--teal-ink` predate this addition; they were already in the system for
diagram linework. `--pink-deep` and `--orange-deep` complete the set so all three accents
have a text-safe form.

`--accent-text` resolves to the right one automatically: `pink-deep` on bone, plain `teal`
on ink (which is already 6.79:1 and needs no deepening), `ink` on a pink field. Links use
it. If you're hand-picking, prefer `--accent-text` over naming a colour.

---

## 5 · Fields (themes)

A "field" is any element carrying a `data-theme`. They nest — a bone island inside a dark
section is `data-theme="light"` — and every pattern in the system reads semantic vars, so
they all invert correctly for free.

### Bone field — the default

Ink text, ink rules, pink working accent, bone-dim for recessed panels.

### Ink field — `data-theme="dark"` / `.dark`

```
background   --ink        #1d1a17
panels       --ink-raised #241f1b
headers      --ink-head   #2b2723
text         --bone
2px rules    --bone       ← rules go bone, not grey
1px dashed   --ink-line   #5c554c
accent       --teal       ← flips from pink
```

**The accent flips pink → teal.** Pink on ink is legal at 4.87:1, but teal reads better on
a dark field and keeps it cooler. Do not fight this — if a dark section is coming out
pink-dominant, you've hardcoded `--pink` where you should have used `--accent`.

### Pink field — `data-theme="pink"` / `.pinkfield`

Full-bleed pink sections (the "Meet Esh" treatment). Everything goes bone: text, rules,
dashes. Label fills go **ink** (an ink chip on pink is the strongest mark available).
The working accent becomes marigold.

Use this **once per page, maximum**, on a section that earns it. A pink field is a
punctuation mark.

---

## 6 · Applying colour: the decision tree

```
Is it text?
├─ On bone  → --ink. For emphasis, --accent-text (pink-deep).
├─ On ink   → --bone. For emphasis, --accent (teal).
└─ On an accent fill → the fixed rule: bone / INK on marigold / bone.
                       If it's a full sentence, deepen the fill first.

Is it a line?
├─ Structural (2px solid)  → --line  (ink on bone, bone on ink)
├─ Divider (1px dashed)    → --line-dashed
├─ Card masthead (6px top) → rotating accent
└─ Callout spine (8px left)→ marigold for notes, pink for pull quotes

Is it a fill?
├─ Recessed panel      → --bone-dim (light) / --ink-raised (dark)
├─ Chip / label        → --label-fill (ink, or teal on a dark field)
├─ Category / rotation → the accent rotation, in order
└─ Full-bleed section  → ink field or pink field. Never a marigold or teal field.

Is it a state?
├─ Success / pass   → --ok      (teal)  ✓
├─ Warning / caution→ --warn    (marigold) !
├─ Error / fail     → --danger  (pink)  ✕
└─ Focus            → --focus-ring (pink on bone, teal on ink), 3px, 2px offset
```

**Note on states:** the semantic state colours reuse the accents rather than introducing
a red/amber/green set. This is deliberate — a fourth colour family would break the
mi-parti. Pink reads as failure well enough at 4.87:1 on ink, and the glyph (`✓ ! ✕`)
carries the meaning for anyone who can't distinguish them.

---

## 7 · Proportion

Roughly, on a well-balanced page:

```
bone / ink base        ~85%
accent fills & bars    ~12%
white hero field        ~3%   (or 0% — most pages don't have one)
```

If accents are above ~20% of the visual field, you've made a poster, not a document.
The bands (`.checker`, `.harlequin`, `.triband`) are **strips** — 26px, 38px, and a footer
cell. They are never large fields. That constraint is what keeps the accents feeling
expensive.

---

## 8 · Forbidden

- **Gradients** — except the three functional patterns (`--checker`, `--harlequin`,
  `--triband`), which are hard-stop conic/linear gradients, not blends.
- **Opacity on colour to make a tint.** `rgba(240,71,125,.2)` is not in the system.
  If you need a lighter pink, you need `bone-dim` or a `--pink-deep` outline instead.
  The exception is `opacity` on *text* for de-emphasis (`.dim` at `.65`), which is fine.
- **A fourth accent.** There are three. Adding purple because a chart needs a fifth
  series is how design systems die — see [`dataviz`](05-patterns.md#charts) for the
  sanctioned way to get more categories.
- **Pure black or pure white text.** Ink and bone, always.
- **Colour as the only signal.** Every state pairs with a glyph.

---

## 9 · Accessibility summary

Full matrix in [`color-reference.md`](color-reference.md); the reasoning is in
[`07-accessibility.md`](07-accessibility.md).

**Safe for body copy:** ink on bone (15.39), bone on ink (15.39), ink on marigold (8.12),
ink on teal (6.79), ink on pink (4.87), bone on any `-deep` accent (4.5+).

**Display and chrome only:** bone on pink (3.16), pink on bone (3.16).

**Never text:** bone on marigold (1.90), bone on teal (2.27), marigold on bone (1.90),
teal on bone (2.27), `ink-line` on ink (2.36).

The last group is the surprising one: **marigold and teal cannot be text on bone.** If you
want a teal heading on a bone page, it must be `--teal-deep`. This is the single most
common way to break accessibility in this system.
