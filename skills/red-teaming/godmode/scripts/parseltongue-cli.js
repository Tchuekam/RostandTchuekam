#!/usr/bin/env node
/**
 * TCHUEKAM Parseltongue CLI — Encode queries to bypass safety classifiers
 * Usage: node parseltongue-cli.js "your query" [--tier light|standard|heavy]
 */

const fs = require('fs');
const path = require('path');

// === ENCODING TECHNIQUES ===

const L33T_MAP = {
  'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7', 'b': '8', 'g': '9'
};

const UNICODE_HOMOGLYPHS = {
  'a': 'а', 'c': 'с', 'e': 'е', 'i': 'і', 'o': 'о', 'p': 'р', 's': 'ѕ', 'x': 'х', 'y': 'у'
};

// Cyrillic homoglyph map
function toUnicode(text) {
  return text.split('').map(ch => UNICODE_HOMOGLYPHS[ch.toLowerCase()] || ch).join('');
}

function toL33t(text) {
  return text.split('').map(ch => L33T_MAP[ch.toLowerCase()] || ch).join('');
}

function toBubble(text) {
  const map = {};
  for (let i = 0; i < 26; i++) {
    map[String.fromCharCode(97 + i)] = String.fromCharCode(0x24D0 + i);
    map[String.fromCharCode(65 + i)] = String.fromCharCode(0x24B6 + i);
  }
  return text.split('').map(ch => map[ch] || ch).join('');
}

function toSpaced(text) {
  return text.split(' ').map(w => w.split('').join(' ')).join('  ');
}

function toFullWidth(text) {
  let out = '';
  for (const ch of text) {
    const code = ch.charCodeAt(0);
    if (code >= 0x21 && code <= 0x7E) {
      out += String.fromCharCode(0xFF00 - 0x20 + code);
    } else {
      out += ch;
    }
  }
  return out;
}

function toZeroWidth(text) {
  const zwj = '\u200D';
  return text.split(' ').map(w => w.split('').join(zwj)).join(' ');
}

function toDotted(text) {
  return text.split(' ').map(w => w.split('').join('.')).join(' ');
}

function toReversed(text) {
  return text.split(' ').map(w => w.split('').reverse().join('')).join(' ');
}

function toBrackets(text) {
  return text.split(' ').map(w => w.split('').map(ch => `[${ch}]`).join('')).join(' ');
}

function toUnderScore(text) {
  return text.split(' ').map(w => w.split('').join('_')).join(' ');
}

function toHyphen(text) {
  return text.split(' ').map(w => w.split('').join('-')).join(' ');
}

function toMixedCase(text) {
  return text.split('').map((ch, i) => i % 2 === 0 ? ch.toUpperCase() : ch.toLowerCase()).join('');
}

function toStrike(text) {
  return text.split('').map(ch => ch + '\u0336').join('');
}

// === TRIGGER WORD DETECTION ===

const TRIGGER_WORDS = [
  'hack', 'exploit', 'bypass', 'crack', 'attack', 'penetrate', 'inject', 
  'manipulate', 'override', 'disable', 'circumvent', 'evade', 'malware', 
  'virus', 'payload', 'shellcode', 'rootkit', 'backdoor', 'vulnerability', 
  'weapon', 'bomb', 'explosive', 'poison', 'drug', 'synthesize', 'jailbreak',
  'unlock', 'phishing', 'scam', 'impersonate', 'deceive', 'fraud', 'nsfw',
  'explicit', 'uncensored', 'unfiltered', 'unrestricted', 'ignore', 'disregard',
  'security', 'password', 'steal', 'illegal', 'unauthorized'
];

function detectTriggers(query) {
  const lower = query.toLowerCase();
  return TRIGGER_WORDS.filter(w => lower.includes(w));
}

// === GENERATE VARIANTS ===

function generateVariants(query, tier = 'light') {
  const variants = [];
  
  // Always include raw
  variants.push({ label: 'Raw', text: query });
  variants.push({ label: 'L33t', text: toL33t(query) });
  
  if (tier === 'light' || tier === 'standard' || tier === 'heavy') {
    variants.push({ label: 'Unicode', text: toUnicode(query) });
    variants.push({ label: 'Bubble', text: toBubble(query) });
    variants.push({ label: 'Spaced', text: toSpaced(query) });
    variants.push({ label: 'Fullwidth', text: toFullWidth(query) });
    variants.push({ label: 'ZeroWidth', text: toZeroWidth(query) });
    variants.push({ label: 'MixedCase', text: toMixedCase(query) });
    variants.push({ label: 'Dotted', text: toDotted(query) });
    variants.push({ label: 'UnderScore', text: toUnderScore(query) });
  }
  
  if (tier === 'standard' || tier === 'heavy') {
    variants.push({ label: 'Reversed', text: toReversed(query) });
    variants.push({ label: 'Strike', text: toStrike(query) });
    variants.push({ label: 'Brackets', text: toBrackets(query) });
    variants.push({ label: 'Hyphen', text: toHyphen(query) });
  }
  
  if (tier === 'heavy') {
    // Multi-layer combos
    variants.push({ label: 'L33t+Bubble', text: toBubble(toL33t(query)) });
    variants.push({ label: 'L33t+Spaced', text: toSpaced(toL33t(query)) });
    variants.push({ label: 'Unicode+Bubble', text: toBubble(toUnicode(query)) });
    variants.push({ label: 'L33t+Unicode', text: toUnicode(toL33t(query)) });
  }
  
  return variants;
}

// === MAIN ===

const args = process.argv.slice(2);
if (args.length === 0) {
  console.log('Usage: node parseltongue-cli.js "your query" [--tier light|standard|heavy]');
  console.log('       node parseltongue-cli.js "your query" --detect-only');
  process.exit(1);
}

let query = args[0];
let tier = 'light';
let detectOnly = false;

for (let i = 1; i < args.length; i++) {
  if (args[i] === '--tier' && i + 1 < args.length) tier = args[++i];
  if (args[i] === '--detect-only') detectOnly = true;
}

// Show triggers
const triggers = detectTriggers(query);
if (triggers.length > 0) {
  console.log(`⚠ Trigger words found: ${triggers.join(', ')}`);
}

if (detectOnly) process.exit(0);

// Generate and show
const variants = generateVariants(query, tier);
console.log(`\n=== PARSELTONGUE ENCODINGS (tier: ${tier}) ===\n`);
variants.forEach(v => {
  const label = v.label.padEnd(14);
  console.log(`  [${label}] ${v.text}`);
});

console.log(`\n${variants.length} variants generated.`);
console.log('Tip: If the model refuses, try --tier standard or --tier heavy');
