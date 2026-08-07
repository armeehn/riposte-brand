# Document numbers

**DOC NO. RL-BRAND-001-DOCNO · REV. A**

The `DOC NO.` chrome is not decoration. Every Riposte surface is filed, and this is the
register. If a document carries a number, that number is here.

---

## Format

```
RL-NNN-R          RL   Riposte Laboratories
                  NNN  document number, from the series below
                  R    revision letter, A onward
```

Written in full as `DOC NO. RL-300-A`, with `REV. A` alongside it when the two are
separated (corner marks, titleblocks, colophons).

Sections within a document are `SEC.NN`, numbered in order from `SEC.01`. Those are local to
the document and are not registered here.

## Series

| Range | Class |
|---|---|
| `RL-000` – `RL-099` | Company: the website, identity, legal, corporate documents |
| `RL-100` – `RL-199` | Plastic Works — injection moulding |
| `RL-200` – `RL-299` | Project HEX — battery tiles |
| `RL-300` – `RL-399` | Tools & software |
| `RL-400` – `RL-499` | Partnerships, proposals, decks |
| `RL-BRAND-NNN` | The design system itself |
| `RL-Z0` | Channel Z0 — a designation, not a number (`DESIG RL-Z0`), predates this register |
| Project-specific | Hardware carries its own part-number series, which outranks a document number — e.g. `IF-BG01` |
| `DB-NNN` | Daily Bread — a separate publication brand, filed apart on purpose |

## Registry

| Number | Document | Repo |
|---|---|---|
| `RL-000-A` | ripostelabs.xyz — the website | [riposte-labs](https://github.com/armeehn/riposte-labs) |
| `RL-BRAND-001-A` | Brand & design system | [riposte-brand](https://github.com/armeehn/riposte-brand) |
| `RL-Z0-A` | Channel Z0 — station and playout | [channel-z0](https://github.com/armeehn/channel-z0) |
| `RL-300-A` | bean — natural language to QuickBooks Online | [bean](https://github.com/armeehn/bean) |
| `RL-310-A` | Cutsheet — print sheet layout and cut lines | [cutsheet](https://github.com/armeehn/cutsheet) |
| `RL-320-A` | e-paper dashboard | [epaper-dashboard](https://github.com/armeehn/epaper-dashboard) |
| `RL-330-A` | FLIPDOT 28×14 — simulator and hardware | flipdot-28x14 |
| `RL-340-A` | RAV4 / Van44 roof rack isolated 12 V busbar | [rav4busbar](https://github.com/armeehn/rav4busbar) |
| `IF-BG01` | Iris ball-lock fastener — build dossier | [iris-ball-lock-fastener](https://github.com/armeehn/iris-lox) |
| `DB-100-A` | Daily Bread — brand relationship | [daily-bread](https://github.com/armeehn/daily-bread) |

Sub-documents append a suffix rather than taking a new number: `RL-BRAND-001-COLOR`,
`RL-BRAND-001-PRINT`, `RL-BRAND-001-CANVA`.

## Revisions

- Start at **`REV. A`**. It is a starting point, not a requirement to reset — a project with
  real revision history keeps it (`IF-BG01` is at `REV. F` and should stay there).
- Bump the letter when the *content* changes materially, not when a typo is fixed.
- The revision letter belongs to the document, not the repo. A README at `REV. C` in a repo
  at v2.1.0 is normal.

## Every repo carries a `BRAND.md`

It states three things, and it is an audit rather than a badge:

1. **Conforms** — what already follows the guide.
2. **Deliberately diverges** — what does not, *and why*. This is the important section.
   Channel Z0's CRT phosphor palette, FLIPDOT's yellow-on-black panel simulation,
   e-paper dashboard's Bootstrap UI and Daily Bread's whole identity are all correct
   divergences, and each is recorded so nobody "fixes" them.
3. **Queued** — real conformance debt, with the concrete mapping to apply.

A divergence that is written down is a decision. A divergence that isn't is a bug.
