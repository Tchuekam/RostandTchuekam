---
name: word-documents
description: "Create, read, edit .docx Word documents from scratch or from templates."
version: 1.1.0
author: tchuekam
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [Word, DOCX, Documents, Office, Productivity]
---

# Word Documents (.docx)

Create, read, and edit Microsoft Word documents programmatically. Use this skill any time a .docx file is requested — poems, reports, letters, contracts, invoices, proposals.

## Quick Reference

| Task | Method |
|------|--------|
| Create from scratch | Node.js `docx` library (npm) |
| Read content | `markitdown` (Python) |
| Edit existing docx | Unpack → edit XML → repack |

## Claude Co-work Comparison
When a user compares my Excel/Doc manipulation capability to Claude's GUI-based automation (like 'computer use'), remember that while Claude interacts via GUI/visual input, TCHUEKAM interacts via file system level data-manipulation (XML/API). Emphasize that my integration allows for local persistence, data sovereignty, and direct manipulation of D: drive assets without cloud-latency.

## Creating .docx from Scratch

### Option A: `python-docx` (Python — preferred when venv works)

Cleaner API than Node.js `docx`. Install and use via `execute_code` (which runs in the active venv):

```bash
pip install python-docx
```

```python
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# Style
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)

# Title
title = doc.add_heading('Title', level=0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

# Paragraph with mixed formatting
p = doc.add_paragraph()
p.add_run('Label: ').bold = True
p.add_run('Value text')

# Bullet list
doc.add_paragraph('Item text', style='List Bullet')

# Table
table = doc.add_table(rows=3, cols=3, style='Light Grid Accent 1')
table.rows[0].cells[0].text = 'Header'
table.rows[1].cells[0].text = 'Data'

# Footer
footer = doc.add_paragraph()
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = footer.add_run('Footer text')
run.font.size = Pt(9)
run.font.color.rgb = RGBColor(150, 150, 150)
run.italic = True

# Save
doc.save('output.docx')
```

### Option B: `docx` npm module (Node.js — fallback)

### Multi-document batch pattern

When creating multiple documents in one session, write each as a separate `.js` file and run them sequentially via `&&`:

```bash
node doc1.js && node doc2.js && node doc3.js
```

**IMPORTANT:** Global variables (`const gold`, `const brandGreen`) do NOT carry across files — each `node` invocation is an independent process. Declare all constants in every file that uses them. Forgetting this causes `ReferenceError: gold is not defined` mid-batch (see Pitfalls).

### Tables in documents

```javascript
// Import additional constructors for tables
const { Document, Packer, Paragraph, TextRun, AlignmentType, 
        HeadingLevel, Table, TableRow, TableCell, WidthType, 
        BorderStyle } = docx;

// Cell helper
const cell = (text, opts = {}) => {
  return new TableCell({
    width: { size: opts.width || 25, type: WidthType.PERCENTAGE },
    children: [new Paragraph({
      alignment: opts.center ? AlignmentType.CENTER : AlignmentType.LEFT,
      spacing: { after: 40 },
      children: [new TextRun({
        text: text,
        font: 'Georgia',
        size: opts.header ? 20 : 18,
        bold: !!opts.header,
        color: opts.header ? 'FFFFFF' : '1B1B1B',
      })],
    })],
    shading: opts.header ? { fill: '1B5E20' } : undefined,
    borders: {
      top: { style: BorderStyle.SINGLE, size: 1, color: 'CCCCCC' },
      bottom: { style: BorderStyle.SINGLE, size: 1, color: 'CCCCCC' },
      left: { style: BorderStyle.SINGLE, size: 1, color: 'CCCCCC' },
      right: { style: BorderStyle.SINGLE, size: 1, color: 'CCCCCC' },
    },
  });
};

// Table builder
const makeTable = (headers, rows) => {
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    rows: [
      new TableRow({ 
        children: headers.map(h => cell(h, { header: true, width: 100/headers.length })) 
      }),
      ...rows.map(row => 
        new TableRow({ 
          children: row.map(c => cell(c, { width: 100/headers.length })) 
        })
      ),
    ],
  });
};

// Usage
makeTable(
  ['Product', 'Price', 'Market'],
  [
    ['TCHUEKAM Lite', '25K/mo', 'Cameroon'],
    ['TCHUEKAM Pro', '75K/mo', 'Cameroon'],
  ],
);
```

### Cover page with page breaks

```javascript
// Add before a new section to force page break
new Paragraph({ children: [new TextRun({ text: '' })], pageBreakBefore: true }),

// Full cover page pattern
new Paragraph({ spacing: { before: 3000 }, children: [] }),
new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 200 },
  children: [
    new TextRun({ text: 'TITLE', font: 'Georgia', size: 72, bold: true, color: '1B5E20' }),
    new TextRun({ text: '\nSubtitle', font: 'Georgia', size: 72, bold: true, color: 'C9A84C' }),
  ],
}),
```

### Install

```bash
npm install -g docx
```

### Basic Template (Node.js)

```javascript
const docx = require('docx');
const fs = require('fs');

const { Document, Packer, Paragraph, TextRun, AlignmentType, HeadingLevel } = docx;

const doc = new Document({
  title: 'Document Title',
  description: 'Description',
  styles: {
    default: {
      document: {
        run: { font: 'Georgia', size: 24 },  // 24 half-points = 12pt
      },
    },
  },
  sections: [{
    properties: {},
    children: [
      new Paragraph({
        text: 'Main Title',
        heading: HeadingLevel.HEADING_1,
        alignment: AlignmentType.CENTER,
        spacing: { after: 200 },
      }),
      new Paragraph({
        spacing: { after: 120 },
        alignment: AlignmentType.CENTER,
        children: [
          new TextRun({ text: 'Line of text here', font: 'Georgia', size: 24 }),
        ],
      }),
    ],
  }],
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync('output.docx', buffer);
  console.log('Created output.docx');
});
```

**IMPORTANT:** When using the global install, `require('docx')` won't resolve from arbitrary directories. Use the full path instead:

```javascript
const docx = require('C:\\Users\\CLINIC\\AppData\\Roaming\\npm\\node_modules\\docx');
```

### Font Sizing

`docx` uses half-points: `size: 24` = 12pt, `size: 48` = 24pt, `size: 20` = 10pt.

### Common Formatting

```javascript
// Bold + italic
new TextRun({ text: 'bold italic', bold: true, italics: true })

// Colored text
new TextRun({ text: 'colored', color: '555555' })

// Spacing between lines
spacing: { after: 200 }  // in twips (1/20 of a point)
spacing: { before: 200, after: 200 }

// Indentation
new Paragraph({
  indent: { left: 720 },  // 720 twips = 0.5 inch
  children: [...]
})
```

## Reading .docx Content

### Method 1: markitdown (Python — preferred)

```bash
pip install "markitdown[pptx]"
python -m markitdown document.docx
```

### Method 2: adm-zip (Node.js — fallback when Python is broken)

Use this when Python has environment issues (common on this system — see `references/environment-issues.md`).

```bash
npm install -g adm-zip
```

```javascript
const AdmZip = require('adm-zip');

function readDocxText(filePath) {
  const zip = new AdmZip(filePath);
  const xml = zip.readAsText('word/document.xml');
  // Strip XML tags to get plain text
  return xml.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
}

const text = readDocxText('document.docx');
console.log(text);
```

**IMPORTANT:** When using global installs, `require()` may not resolve from arbitrary directories. Use absolute paths:

```javascript
const AdmZip = require('C:\\Users\\CLINIC\\AppData\\Roaming\\npm\\node_modules\\adm-zip');
```

### Method 3: Unzip + grep (quick peek without code)

```bash
# .docx is a ZIP file — extract just the main content XML
unzip -p document.docx word/document.xml | sed 's/<[^>]*>//g' | sed 's/  */ /g'
```

## Editing Existing .docx

For simple text replacements, unpack the docx (it's a ZIP file), edit the XML, and repack:

```bash
# Unpack
cp document.docx document.zip
unzip document.zip -d unpacked/

# The main content is in word/document.xml
# Edit text with sed/patch, then repack:
cd unpacked
zip -r ../updated.docx .
```

## Pitfalls

- **Node.js `docx` module**: `require('docx')` fails from arbitrary directories when installed globally. Use absolute path to the global module.
- **Python `python-docx`**: The `pip`/`uv` Python environment on this system has an `SRE module mismatch` error that prevents installing packages. Use Node.js as the primary method.
- **Font names**: Must be system-available fonts (Georgia, Calibri, Arial, Times New Roman, etc.).
- **Word opens XML on double-click**: Don't let users accidentally open the unpacked XML — only give them the final `.docx`.
- **Git Bash / MSYS path translation**: In Git Bash (`/d/...` paths), Node.js `writeFileSync` resolves `/d/` to `C:\d\` instead of `D:\`. Always use Windows-native paths in JavaScript file writes: `'D:/path/to/file.docx'` or `'C:\\Users\\...'`. The `D:/...` forward-slash form works on both Node.js and in the terminal — use it.
- **ReferenceError on shared variables**: When writing multi-document batch scripts, declare shared color/text constants (`const gold`, `const brandGreen`, etc.) inside each module scope. They do NOT leak across `node` calls — each script file is an independent process. Example at fault: declaring `const gold = 'C9A84C'` in one file and using `gold` in another = `ReferenceError: gold is not defined`. Fix: declare in every file.

## References

- `references/poems.md` — poem-specific formatting (centered verses, stanza spacing, styled title pages)
- `references/corporate-document-template.md` — reusable corporate document template with cover page, TOC, and brand styling
- `references/report-synthesis-pattern.md` — one-off session synthesis report with objectives table, status indicators, and action plan
- `references/daily-report-pattern.md` — **daily report** with file-change log, today's accomplishments table, objectives status, and next-day plan. Created when the user asks "what did I do today" or "create a daily report". Saves to `Desktop/TCHUEKAM_DAILY_REPORT/YYYY-MM-DD.docx`.
