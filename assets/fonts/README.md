# JetBrains Mono — self-hosting subsets

**DOC NO. RL-BRAND-001-FONT · REV. A**

These are the woff2 subsets used in production on `ripostelabs.xyz`, extracted from the
Google Fonts build of JetBrains Mono.

| File | Covers |
|---|---|
| `jetbrains-mono-latin.woff2` | Latin — the only one worth preloading |
| `jetbrains-mono-latin-ext.woff2` | Latin Extended |
| `jetbrains-mono-vietnamese.woff2` | Vietnamese |

Each is a variable-weight file covering **400–800**, which is the full range the brand uses.
Load them with `unicode-range` so only the needed subset is fetched — see
[`../../tools/web.md`](../../tools/web.md#2--self-hosting-the-font) for the `@font-face`
block and the preload tag.

---

## Licence

JetBrains Mono is licensed under the **SIL Open Font License, Version 1.1**.

- Copyright © 2020 The JetBrains Mono Project Authors
- Upstream: <https://github.com/JetBrains/JetBrainsMono>
- Licence text: <https://github.com/JetBrains/JetBrainsMono/blob/master/OFL.txt>
- Also: <https://scripts.sil.org/OFL>

The full `OFL.txt` ships inside the upstream release archive. It is **not** duplicated here
— pull it from the release you actually deploy, so the copyright line matches the version
you're shipping.

Under the OFL you may use, study, modify and redistribute these files, including
commercially and including embedding them in documents and applications. The two conditions
that matter in practice:

1. **The licence travels with the font.** If you redistribute the font files (as this repo
   does, and as a Canva or Figma upload does), the OFL notice must go with them.
2. **Don't sell the fonts on their own,** and don't ship a modified version under the name
   "JetBrains Mono".

This is why the brand can be uploaded to Canva Pro, embedded in a PDF, bundled into a
PowerPoint, or installed on a print vendor's machine without a licence purchase.

---

## Getting the originals

For desktop use (Illustrator, Figma, Office, Inkscape) you want the `.ttf` files, not these
subsets:

```bash
# Arch
sudo pacman -S ttf-jetbrains-mono
# Debian / Ubuntu
sudo apt install fonts-jetbrains-mono
# Manual — any platform
# https://www.jetbrains.com/lp/mono/  →  Download  →  install JetBrainsMono-{Regular,Bold,ExtraBold}.ttf
```

Install **400 / 700 / 800 only**. The brand uses no other weights, and having the full
family installed makes it easy to reach for one by accident.
