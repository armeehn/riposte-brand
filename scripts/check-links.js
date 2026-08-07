#!/usr/bin/env node
/* Verify every relative link in the docs resolves to a real file.

   Fenced code blocks are skipped — they contain illustrative site-absolute paths
   (`/brand/riposte-brand.css`) that are correct in a deployed page but meaningless
   relative to this repo.

   Run: node scripts/check-links.js
*/
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');

function walk(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap(e => {
    if (e.name === '.git' || e.name === 'node_modules') return [];
    const p = path.join(dir, e.name);
    return e.isDirectory() ? walk(p) : [p];
  });
}

/* Drop fenced blocks and inline code so example paths aren't treated as links. */
const strip = s => s
  .replace(/^```[\s\S]*?^```/gm, '')
  .replace(/`[^`\n]*`/g, '')
  .replace(/<style[\s\S]*?<\/style>/gi, '');

let checked = 0, bad = 0;

for (const file of walk(ROOT).filter(f => /\.(md|html)$/.test(f))) {
  const src = strip(fs.readFileSync(file, 'utf8'));
  const links = [
    ...[...src.matchAll(/\]\(([^)\s]+)\)/g)].map(m => m[1]),
    ...[...src.matchAll(/(?:href|src)="([^"]+)"/g)].map(m => m[1]),
  ];
  for (const raw of links) {
    const l = raw.split('#')[0];
    if (!l) continue;                                     // pure anchor
    if (/^(https?:|mailto:|data:|\/\/)/.test(l)) continue; // external
    if (l.startsWith('/')) continue;                       // site-absolute
    checked++;
    if (!fs.existsSync(path.resolve(path.dirname(file), l))) {
      console.error(`  ✕ ${path.relative(ROOT, file)} -> ${l}`);
      bad++;
    }
  }
}

console.log(`checked ${checked} relative links, ${bad} broken`);
if (bad) process.exit(1);
