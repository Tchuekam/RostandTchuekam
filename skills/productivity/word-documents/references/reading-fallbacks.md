# Reading .docx Content — Fallback Methods

Discovered during session May 26, 2026: Python `markitdown` was unavailable (SRE module mismatch). Node.js fallback pipeline was used instead.

## Fallback Pipeline (Node.js + adm-zip)

### Install

```bash
npm install -g adm-zip
```

### Script: read all docx files in Desktop

```javascript
const AdmZip = require('C:\\Users\\CLINIC\\AppData\\Roaming\\npm\\node_modules\\adm-zip');
const fs = require('fs');

function readDocxText(filePath) {
  const zip = new AdmZip(filePath);
  const content = zip.readAsText('word/document.xml');
  return content.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
}

const files = [
  'C:\\Users\\CLINIC\\Desktop\\example.docx'
];

files.forEach(f => {
  console.log('=== ' + f.split('\\').pop() + ' ===');
  console.log(readDocxText(f));
  console.log('\n');
});
```

### Output from Desktop docs (May 26 session)

- **HolyZap CMD.docx**: Mixed motivational quotes + sales script for Giantect/Mbowazap WhatsApp automation product.
- **MonProject.docx**: Pitch deck draft for "BetterAbroad" — platform connecting African students to foreign universities.
- **A_Poem_For_You.docx**: Original poem "L'Aube Intérieure" — 12 verses about dawn, strength, and new beginnings.

## Notes

- `adm-zip` extracts `word/document.xml` which contains the full text with XML tags.
- The stripped text loses formatting info (bold, italic, font sizes) — only plain text.
- For formatting-preserving extraction, fix the Python env and use `markitdown`.
