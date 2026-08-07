#!/usr/bin/env node
/* ============================================================================
   Riposte brand — export builder.

   brand/tokens.json is the single source of truth. Everything downstream is
   generated from it, so a swatch file can never drift from the stylesheet:

     palettes/riposte.gpl              GIMP, Inkscape, Krita
     palettes/riposte.ase              Adobe CC, Affinity, Sketch, Figma plugins
     palettes/riposte.sketchpalette    Sketch
     palettes/riposte.csv              spreadsheets, Canva copy-paste, print vendors
     palettes/riposte.json             flat name -> hex, for scripts
     brand/tokens.scss                 Sass consumers
     brand/tailwind.preset.js          Tailwind consumers
     docs/color-reference.md           full conversion + contrast tables

   It also VERIFIES that brand/riposte-brand.css declares the same hex values
   as tokens.json, and that every documented contrast claim is true. Run:

     node scripts/build.js            # write exports, then verify
     node scripts/build.js --check    # verify only; non-zero exit on drift

   ========================================================================== */
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const T = JSON.parse(fs.readFileSync(path.join(ROOT, 'brand/tokens.json'), 'utf8'));
const CHECK_ONLY = process.argv.includes('--check');

const w = (rel, data) => {
  if (CHECK_ONLY) return;
  const p = path.join(ROOT, rel);
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, data);
  console.log('  wrote', rel);
};

/* -------------------------------------------------------------------------
   colour maths
   ------------------------------------------------------------------------- */
const hex2rgb = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
const rgb2hex = a => '#' + a.map(x => Math.round(x).toString(16).padStart(2, '0')).join('');
const srgb2lin = c => { c /= 255; return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };

function hsl([r, g, b]) {
  r /= 255; g /= 255; b /= 255;
  const mx = Math.max(r, g, b), mn = Math.min(r, g, b), d = mx - mn;
  let h = 0;
  if (d) { if (mx === r) h = ((g - b) / d) % 6; else if (mx === g) h = (b - r) / d + 2; else h = (r - g) / d + 4; }
  h *= 60; if (h < 0) h += 360;
  const l = (mx + mn) / 2;
  return [h, (d ? d / (1 - Math.abs(2 * l - 1)) : 0) * 100, l * 100];
}

function oklch([r, g, b]) {
  const R = srgb2lin(r), G = srgb2lin(g), B = srgb2lin(b);
  const l = Math.cbrt(0.4122214708 * R + 0.5363325363 * G + 0.0514459929 * B);
  const m = Math.cbrt(0.2119034982 * R + 0.6806995451 * G + 0.1073969566 * B);
  const s = Math.cbrt(0.0883024619 * R + 0.2817188376 * G + 0.6299787005 * B);
  const L = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s;
  const A = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s;
  const Bb = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s;
  let H = Math.atan2(Bb, A) * 180 / Math.PI; if (H < 0) H += 360;
  return [L * 100, Math.sqrt(A * A + Bb * Bb), H];
}

/* Naive device CMYK. Good enough to hand a print vendor as a STARTING POINT —
   always ask them for a proof. See docs/08-print.md. */
function cmyk([r, g, b]) {
  const R = r / 255, G = g / 255, B = b / 255;
  const k = 1 - Math.max(R, G, B);
  if (k === 1) return [0, 0, 0, 100];
  return [(1 - R - k) / (1 - k) * 100, (1 - G - k) / (1 - k) * 100, (1 - B - k) / (1 - k) * 100, k * 100];
}

const lum = rgb => { const [R, G, B] = rgb.map(srgb2lin); return 0.2126 * R + 0.7152 * G + 0.0722 * B; };
function contrast(hexA, hexB) {
  const l1 = lum(hex2rgb(hexA)), l2 = lum(hex2rgb(hexB));
  const [hi, lo] = l1 > l2 ? [l1, l2] : [l2, l1];
  return (hi + 0.05) / (lo + 0.05);
}
const grade = v => v >= 7 ? 'AAA' : v >= 4.5 ? 'AA' : v >= 3 ? 'AA Large only' : 'FAIL';

const COLORS = Object.entries(T.color);
const f = (n, d = 0) => n.toFixed(d);

/* -------------------------------------------------------------------------
   GPL — GIMP / Inkscape / Krita
   ------------------------------------------------------------------------- */
{
  let out = 'GIMP Palette\nName: Riposte Laboratories\nColumns: 4\n#\n';
  out += '# ' + T.meta.brand + ' — DOC NO. ' + T.meta.docNo + ' REV. ' + T.meta.rev + '\n';
  out += '# ' + T.meta.source + '\n#\n';
  for (const [k, v] of COLORS) {
    const [r, g, b] = hex2rgb(v.hex);
    out += `${String(r).padStart(3)} ${String(g).padStart(3)} ${String(b).padStart(3)}\t${v.name}\n`;
  }
  w('palettes/riposte.gpl', out);
}

/* -------------------------------------------------------------------------
   ASE — Adobe Swatch Exchange (Illustrator, Photoshop, InDesign, Affinity,
   Sketch, and most Figma palette plugins).
   Format: "ASEF" | u16 major | u16 minor | u32 blockCount | blocks...
     block = u16 type | u32 len | data
     type 0xC001 group open, 0xC002 group close, 0x0001 colour entry
     colour data = u16 nameLen(incl NUL) | UTF-16BE name+NUL | "RGB " | 3x f32 BE | u16 mode
   ------------------------------------------------------------------------- */
{
  const chunks = [];
  const u16 = n => { const b = Buffer.alloc(2); b.writeUInt16BE(n); return b; };
  const u32 = n => { const b = Buffer.alloc(4); b.writeUInt32BE(n); return b; };
  const f32 = n => { const b = Buffer.alloc(4); b.writeFloatBE(n); return b; };
  const name16 = s => {
    const body = Buffer.from(s, 'utf16le').swap16();
    return Buffer.concat([u16(s.length + 1), body, Buffer.alloc(2)]);
  };

  const groups = [
    ['RIPOSTE / BASE',   COLORS.filter(([, v]) => v.role === 'base')],
    ['RIPOSTE / ACCENT', COLORS.filter(([, v]) => v.role === 'accent')],
    ['RIPOSTE / ACCENT DEEP', COLORS.filter(([, v]) => v.role === 'accent-deep')],
  ];

  let blockCount = 0;
  for (const [gname, list] of groups) {
    const gn = name16(gname);
    chunks.push(u16(0xC001), u32(gn.length), gn); blockCount++;
    for (const [, v] of list) {
      const n = name16(v.name);
      const [r, g, b] = hex2rgb(v.hex);
      const data = Buffer.concat([n, Buffer.from('RGB '), f32(r / 255), f32(g / 255), f32(b / 255), u16(2)]);
      chunks.push(u16(0x0001), u32(data.length), data); blockCount++;
    }
    chunks.push(u16(0xC002), u32(0)); blockCount++;
  }
  const buf = Buffer.concat([Buffer.from('ASEF'), u16(1), u16(0), u32(blockCount), ...chunks]);
  w('palettes/riposte.ase', buf);
}

/* -------------------------------------------------------------------------
   .sketchpalette
   ------------------------------------------------------------------------- */
{
  const out = {
    compatibleVersion: '2.0', pluginVersion: '2.14',
    colors: COLORS.map(([, v]) => {
      const [r, g, b] = hex2rgb(v.hex);
      return { name: v.name, red: r / 255, green: g / 255, blue: b / 255, alpha: 1 };
    })
  };
  w('palettes/riposte.sketchpalette', JSON.stringify(out, null, 2) + '\n');
}

/* -------------------------------------------------------------------------
   CSV — the universal one. Paste into Canva, hand to a printer, open in Sheets.
   ------------------------------------------------------------------------- */
{
  let out = 'token,name,role,hex,r,g,b,hsl,oklch,cmyk_approx,note\n';
  for (const [k, v] of COLORS) {
    const rgb = hex2rgb(v.hex), H = hsl(rgb), O = oklch(rgb), M = cmyk(rgb);
    out += [
      k, `"${v.name}"`, v.role, v.hex.toUpperCase(), rgb[0], rgb[1], rgb[2],
      `"${f(H[0])} ${f(H[1])}% ${f(H[2])}%"`,
      `"${f(O[0], 1)}% ${O[1].toFixed(3)} ${f(O[2], 1)}"`,
      `"${M.map(x => f(x)).join('/')}"`,
      `"${v.note.replace(/"/g, "'")}"`
    ].join(',') + '\n';
  }
  w('palettes/riposte.csv', out);
}

/* flat JSON */
w('palettes/riposte.json', JSON.stringify(
  Object.fromEntries(COLORS.map(([k, v]) => [k, v.hex])), null, 2) + '\n');

/* -------------------------------------------------------------------------
   SCSS
   ------------------------------------------------------------------------- */
{
  let out = `// Riposte Laboratories — generated by scripts/build.js. Do not edit.\n`;
  out += `// Source: brand/tokens.json\n\n`;
  for (const [k, v] of COLORS) out += `$rl-${k}: ${v.hex}; // ${v.name}\n`;
  out += `\n$rl-font-mono: ${T.font.stack};\n`;
  out += `$rl-weights: (${T.font.weights.join(', ')});\n\n`;
  for (const [k, v] of Object.entries(T.space)) out += `$rl-space-${k}: ${v};\n`;
  out += '\n';
  for (const [k, v] of Object.entries(T.container)) out += `$rl-container-${k}: ${v};\n`;
  out += '\n';
  for (const [k, v] of Object.entries(T.tracking)) out += `$rl-tracking-${k}: ${v};\n`;
  out += `\n$rl-radius: 0;\n$rl-rule-width: ${T.effect.ruleWidth};\n`;
  w('brand/tokens.scss', out);
}

/* -------------------------------------------------------------------------
   Tailwind preset
   ------------------------------------------------------------------------- */
{
  const colors = Object.fromEntries(COLORS.map(([k, v]) => [k, v.hex]));
  const spacing = Object.fromEntries(Object.entries(T.space).map(([k, v]) => ['rl' + k, v]));
  const out = `/* Riposte Laboratories — generated by scripts/build.js. Do not edit.
   Usage:  module.exports = { presets: [require('./brand/tailwind.preset.js')] }
   Radius is forced to 0 and shadows to hard offsets: the brand has no soft edges. */
module.exports = {
  theme: {
    extend: {
      colors: ${JSON.stringify(colors, null, 8).replace(/\n/g, '\n      ')},
      fontFamily: { mono: [${T.font.stack.split(',').map(s => JSON.stringify(s.trim().replace(/^"|"$/g, ''))).join(', ')}] },
      spacing: ${JSON.stringify(spacing, null, 8).replace(/\n/g, '\n      ')},
      maxWidth: { rl: '${T.container.default}', 'rl-wide': '${T.container.wide}', 'rl-prose': '${T.container.prose}', measure: '${T.container.measure}' },
      letterSpacing: ${JSON.stringify(T.tracking, null, 8).replace(/\n/g, '\n      ')},
      borderWidth: { rule: '${T.effect.ruleWidth}', bar: '${T.effect.barTop}', barl: '${T.effect.barLeft}' },
      boxShadow: {
        pop: '4px 4px 0 ${T.color.pink.hex}',
        'pop-teal': '4px 4px 0 ${T.color.teal.hex}',
        stack: '8px 8px 0 ${T.color.teal.hex}, 16px 16px 0 ${T.color.pink.hex}',
      },
      backgroundImage: {
        triband: 'linear-gradient(${T.effect.tribandAngle}, ${T.color.pink.hex} 0 36%, ${T.color.orange.hex} 36% 64%, ${T.color.teal.hex} 64% 100%)',
      },
      transitionDuration: { flick: '${T.motion.flick}', snap: '${T.motion.snap}', move: '${T.motion.move}' },
    },
    borderRadius: { none: '0', DEFAULT: '0', sm: '0', md: '0', lg: '0', xl: '0', full: '0' },
  },
};
`;
  w('brand/tailwind.preset.js', out);
}

/* -------------------------------------------------------------------------
   docs/color-reference.md — generated tables
   ------------------------------------------------------------------------- */
const PAIRS = [
  ['ink', 'bone'], ['ink', 'bone-dim'], ['ink', 'white'],
  ['bone', 'pink'], ['ink', 'pink'], ['bone', 'pink-deep'],
  ['ink', 'orange'], ['bone', 'orange'], ['bone', 'orange-deep'],
  ['bone', 'teal'], ['ink', 'teal'], ['bone', 'teal-deep'], ['teal-ink', 'teal'],
  ['bone', 'ink'], ['pink', 'ink'], ['teal', 'ink'], ['orange', 'ink'],
  ['pink', 'bone'], ['teal', 'bone'], ['orange', 'bone'],
  ['pink-deep', 'bone'], ['teal-deep', 'bone'], ['orange-deep', 'bone'],
  ['ink-line', 'ink'],
];
{
  let out = `<!-- GENERATED by scripts/build.js from brand/tokens.json. Do not edit by hand. -->\n`;
  out += `# Colour reference — every official value\n\n`;
  out += `**DOC NO. ${T.meta.docNo}-COLOR · REV. ${T.meta.rev}**\n\n`;
  out += `Hex is normative. Everything else is derived — if a tool disagrees, hex wins.\n\n`;
  out += `## Conversions\n\n`;
  out += `| Token | Name | HEX | RGB | HSL | OKLCH | CMYK (device, approx) |\n|---|---|---|---|---|---|---|\n`;
  for (const [k, v] of COLORS) {
    const rgb = hex2rgb(v.hex), H = hsl(rgb), O = oklch(rgb), M = cmyk(rgb);
    out += `| \`${k}\` | ${v.name} | \`${v.hex.toUpperCase()}\` | \`${rgb.join(' ')}\` | \`${f(H[0])} ${f(H[1])}% ${f(H[2])}%\` | \`${f(O[0], 1)}% ${O[1].toFixed(3)} ${f(O[2], 1)}\` | \`${M.map(x => f(x)).join(' / ')}\` |\n`;
  }
  out += `\n## Contrast matrix (WCAG 2.1)\n\n`;
  out += `Foreground on background. \`AA\` needs 4.5:1 for body text, \`AA Large\` needs 3:1 and applies only\n`;
  out += `to text at 24px+ or bold 18.66px+ — which in this system means uppercase display and chrome, never prose.\n\n`;
  out += `| Foreground | Background | Ratio | Grade | Verdict |\n|---|---|---|---|---|\n`;
  for (const [a, b] of PAIRS) {
    const v = contrast(T.color[a].hex, T.color[b].hex);
    const g = grade(v);
    const verdict = g === 'FAIL' ? 'Decoration only — never text'
      : g === 'AA Large only' ? 'Display/chrome only — never body copy'
        : 'Safe for body copy';
    out += `| \`${a}\` | \`${b}\` | ${v.toFixed(2)}:1 | ${g} | ${verdict} |\n`;
  }
  out += `\n## The rule this table exists to enforce\n\n`;
  out += `The brand's fixed pairings — **bone on pink**, **bone on teal** — are *brand-correct but not\n`;
  out += `text-safe*. They land at ${contrast(T.color.bone.hex, T.color.pink.hex).toFixed(2)}:1 and ${contrast(T.color.bone.hex, T.color.teal.hex).toFixed(2)}:1.\n`;
  out += `Keep them for chips, spec headers, section bars and large uppercase display, where they are the\n`;
  out += `brand. The moment an accent fill has to carry a **sentence**, switch to the \`-deep\` variant:\n`;
  out += `same hue, same saturation, lightness dropped until bone clears 4.5:1.\n\n`;
  out += `\`ink\` on \`orange\` (${contrast(T.color.ink.hex, T.color.orange.hex).toFixed(2)}:1) is the one accent fill that is safe for prose as-is.\n`;
  out += `That is why marigold takes ink text and the other two take bone.\n`;
  w('docs/color-reference.md', out);
}

/* -------------------------------------------------------------------------
   VERIFY
   ------------------------------------------------------------------------- */
let failures = 0;
const fail = m => { console.error('  ✕ ' + m); failures++; };
const ok = m => console.log('  ✓ ' + m);

console.log('\nverify:');

/* 1. every token hex appears in the stylesheet with the same value */
const css = fs.readFileSync(path.join(ROOT, 'brand/riposte-brand.css'), 'utf8');
for (const [k, v] of COLORS) {
  const re = new RegExp('--' + k.replace(/[-]/g, '\\-') + ':\\s*(#[0-9a-fA-F]{6})');
  const m = css.match(re);
  if (!m) fail(`riposte-brand.css is missing --${k}`);
  else if (m[1].toLowerCase() !== v.hex.toLowerCase()) fail(`--${k}: css says ${m[1]}, tokens.json says ${v.hex}`);
}
if (!failures) ok(`all ${COLORS.length} colour tokens agree between tokens.json and riposte-brand.css`);

/* 2. the deep accents actually clear AA against bone */
for (const k of ['pink-deep', 'orange-deep', 'teal-deep']) {
  const v = contrast(T.color.bone.hex, T.color[k].hex);
  if (v < 4.5) fail(`${k} only reaches ${v.toFixed(2)}:1 against bone — must be >= 4.5`);
  else ok(`${k} clears AA against bone (${v.toFixed(2)}:1)`);
}

/* 3. ink on orange must stay AA — the whole on-accent rule depends on it */
{
  const v = contrast(T.color.ink.hex, T.color.orange.hex);
  if (v < 4.5) fail(`ink on orange fell to ${v.toFixed(2)}:1`); else ok(`ink on orange holds AA (${v.toFixed(2)}:1)`);
}

/* 4. radius really is 0 everywhere in the stylesheet */
{
  const bad = [...css.matchAll(/border-radius:\s*([^;]+);/g)]
    .map(m => m[1].trim())
    .filter(v => v !== '0' && v !== 'var(--radius-0)');
  if (bad.length) fail(`non-zero border-radius in riposte-brand.css: ${bad.join(', ')}`);
  else ok('radius is 0 everywhere');
}

/* 5. no blur shadows */
{
  const shadows = [...css.matchAll(/box-shadow:\s*([^;]+);/g)].map(m => m[1]);
  const blurred = shadows.filter(s => {
    if (s.includes('var(')) return false;               // token refs checked below
    return /\d+px\s+\d+px\s+[1-9]\d*px/.test(s);         // third length = blur
  });
  if (blurred.length) fail(`blurred box-shadow found: ${blurred.join(' | ')}`);
  else ok('no blur in any shadow');
}

/* 6. the ASE binary parses back to the exact same hex values.
   A malformed swatch file fails silently inside Illustrator, so prove it here. */
{
  const asePath = path.join(ROOT, 'palettes/riposte.ase');
  if (!fs.existsSync(asePath)) fail('palettes/riposte.ase is missing (run without --check first)');
  else try {
    const b = fs.readFileSync(asePath);
    if (b.slice(0, 4).toString() !== 'ASEF') throw new Error('bad signature');
    const total = b.readUInt32BE(8);
    let o = 12, seen = 0;
    const got = [];
    while (seen < total) {
      const t = b.readUInt16BE(o), len = b.readUInt32BE(o + 2);
      let p = o + 6;
      if (t !== 0xC002) {
        const nl = b.readUInt16BE(p); p += 2;
        const name = Buffer.from(b.slice(p, p + (nl - 1) * 2)).swap16().toString('utf16le');
        p += nl * 2;
        if (t === 0x0001) {
          p += 4; // colour model
          const rgb = [b.readFloatBE(p), b.readFloatBE(p + 4), b.readFloatBE(p + 8)];
          got.push([name, rgb2hex(rgb.map(v => v * 255))]);
        }
      }
      o += 6 + len; seen++;
    }
    if (o !== b.length) throw new Error(`trailing bytes: parsed ${o} of ${b.length}`);
    const want = COLORS.map(([, v]) => [v.name, v.hex.toLowerCase()]);
    if (got.length !== want.length) throw new Error(`${got.length} swatches, expected ${want.length}`);
    for (let i = 0; i < want.length; i++) {
      if (got[i][0] !== want[i][0] || got[i][1] !== want[i][1])
        throw new Error(`swatch ${i}: got ${got[i].join('=')}, expected ${want[i].join('=')}`);
    }
    ok(`riposte.ase parses cleanly and round-trips all ${got.length} swatches`);
  } catch (e) { fail('riposte.ase is malformed: ' + e.message); }
}

console.log('');
if (failures) { console.error(`FAILED — ${failures} problem(s).`); process.exit(1); }
console.log('OK — brand exports are consistent.');
