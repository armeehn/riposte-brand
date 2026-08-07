# Voice & content

**DOC NO. RL-BRAND-001-VOICE · REV. A**

---

## 1 · Who is speaking

An engineer who has actually done the thing, writing it down so someone else can do it too.

Riposte Laboratories counter-attacks the waste stream: discarded plastic (model-kit runners
and sprues) becomes injection-moulded goods — **Plastic Works**; reclaimed lithium cells
become modular solar power tiles — **Project HEX**.

The company is not selling a vision. It's reporting results. Write accordingly.

---

## 2 · The two registers

Same voice, two modes. Both JetBrains Mono; the difference is case, not family.

### The document — chrome

Uppercase, tracked, filed. Identifiers, never sentences.

```
DOC NO. RL-200-A     SEC.03     REV. A     SPEC / HEX UNIT     EST. 2026
```

Section heads carry a lowercase slash-tag, right-aligned, like a code comment:

```
SEC.02   THE COUNTER-ATTACK                    // local loop injection molding
```

### The engineer — prose

Sentence case, weights 400/700. Plainspoken, concrete, quietly witty. **The wit comes from
precision, not from jokes:**

> A disposable vape is, functionally, a lithium cell wrapped in plastic and marketed as
> trash.

That sentence is funny because it's accurate. That's the whole technique. It never winks,
never puns, never uses an exclamation mark.

---

## 3 · Rules

1. **Bold the numbers that matter.** Load-bearing figures and units go `700` in prose:
   **14.46 Wh**, **45 × 13 mm**, **72%**. Unbolded numbers are context; bolded numbers are
   the argument.
2. **Concrete over abstract.** "A 14.46 Wh cell measuring 45 × 13 mm" beats "high-density
   energy storage". If you can't name the number, you probably shouldn't make the claim.
3. **No marketing verbs.** Nothing *leverages*, *unlocks*, *revolutionises*, *empowers* or
   is *passionate about*. Things are made, tested, measured, shipped, and sometimes they
   fail.
4. **Fencing is the frame, not the decoration.** Parry → riposte → return is process
   language: the parry is the deflection (diverting waste), the riposte is the counter
   (making something), the return is the loop closing. Use it structurally. Don't pepper
   the copy with swordplay metaphors.
5. **Admit the limits.** If a figure is illustrative, say so, loudly. If a process only
   works at small scale, say that too. Credibility is the entire product.
6. **No exclamation marks.** None. Anywhere.
7. **Second person for instructions, first person plural sparingly.** "Sort the runners by
   resin code" — not "we recommend that users sort".

---

## 4 · Fixed strings

| String | Form |
|---|---|
| Ticker | `PARRY · RIPOSTE · RECYCLE · REPEAT ♻` |
| Tagline | **Parry. Riposte.** |
| Legal name | Riposte Laboratories Inc. |
| Short name | Riposte Labs · Riposte |
| Products | Plastic Works · Project HEX |
| Emblem | **esh** — lowercase always, she/her |
| Document control | `DOC NO. RL-000-A` · `REV. A` · `SEC.NN` · `EST. 2026` |
| Copyright | `© 2026 Riposte Laboratories Inc. · All rights reserved.` |
| Footer loop | `parry ♻ riposte ♻ recycle ♻ repeat` |

---

## 5 · Placeholders are honest and loud

A placeholder that looks like real data is a liability. Make it impossible to ship by
accident:

```
$[TAM]        [Q_/__]        [PARTNER NAME]

⚠ Illustrative — replace before sending
```

Use the `.stamp` component (rotated `-2deg`, marigold outline) for `DRAFT` and
`ILLUSTRATIVE` overlays on decks.

---

## 6 · Glyphs

```
▸  bullets       ✓  pass       ✕  fail       !  warning
→  flow          ↓  flow (stacked)           ▾  disclosure
◆  marker        ♻  the loop   ✉  contact
```

No emoji beyond `♻` and `✉`. Units use `×` (U+00D7), not `x`. Ranges use en dashes without
spaces: `56–62ch`.

---

## 7 · Documentation

Every Riposte repo's README follows the same shape:

```markdown
# Project Name

**DOC NO. RL-NNN-A · REV. A**

> One-sentence statement of what this is and what it counters.

[what it does — concrete, with numbers]

## Contents / Build / Use
...

---
<colophon>
```

- **Headings sentence case in Markdown.** GitHub renders Markdown in a proportional face
  with its own type scale; forcing UPPERCASE there fights the platform and hurts
  searchability. The uppercase register is for surfaces we control — HTML, decks, print.
  The document *chrome* (`DOC NO.`, `REV.`) stays uppercase because it's an identifier.
- **Lead with what it is,** not why it matters.
- **Tables over prose** for anything with more than three parallel facts.
- **Close with the colophon** — see any Riposte `BRAND.md`.
- Code blocks always get a language tag.

---

## 8 · Before you publish

- [ ] Every number checked, and load-bearing ones bolded
- [ ] No exclamation marks, no marketing verbs
- [ ] Placeholders either filled or loudly flagged
- [ ] Uppercase achieved with `text-transform`, not typed (screen readers)
- [ ] Colophon present
- [ ] `DOC NO.` and `REV.` correct
