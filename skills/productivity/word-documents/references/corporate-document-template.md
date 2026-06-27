# Corporate Document Template (Giantect Empire)

Use this pattern for any company document that needs to project a professional brand: constitutions, blueprints, strategy docs, whitepapers, proposals.

## Reusable Pattern

Every corporate document follows this structure:

```
Cover page (centered, large)
  → Table of Contents
  → Section 1 (page break before)
  → Section 2 (page break before)
  → ... 
  → Closing statement (centered, "— END OF DOCUMENT —")
```

## Brand Constants

```javascript
const brandGreen = '1B5E20';  // Primary: trust, growth, sovereignty
const gold = 'C9A84C';        // Accent: prestige, value
const dark = '0A1A0A';        // Background depth
const charcoal = '1B1B1B';    // Body text
const gray = '888888';        // Secondary text
const red = 'CC0000';         // Warnings, "CONFIDENTIAL"
```

## Cover Page Pattern

```javascript
new Paragraph({ spacing: { before: 3000 }, children: [] }),
new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 200 },
  children: [
    new TextRun({ text: 'TITLE', font: 'Georgia', size: 72, bold: true, color: brandGreen }),
    new TextRun({ text: '\nSUBTITLE', font: 'Georgia', size: 52, bold: true, color: gold }),
  ],
}),
new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 400, after: 100 },
  children: [new TextRun({ text: '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', font: 'Georgia', size: 24, color: gold })],
}),
new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 200 },
  children: [new TextRun({ text: 'Tagline text', font: 'Georgia', size: 28, italics: true, color: '555555' })],
}),
new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 600, after: 100 },
  children: [new TextRun({ text: 'Date\nLocation', font: 'Georgia', size: 22, color: '666666' })],
}),
new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 400 },
  children: [new TextRun({ text: 'CONFIDENTIAL — DO NOT DISTRIBUTE', font: 'Georgia', size: 20, bold: true, color: red })],
}),
```

## Table of Contents (Simple)

```javascript
new Paragraph({ text: 'TABLE OF CONTENTS', heading: HeadingLevel.HEADING_1, spacing: { after: 300 } }),
...['1. Section One', '2. Section Two', '3. Section Three'].map(item =>
  new Paragraph({
    spacing: { after: 80 },
    children: [new TextRun({ text: item, font: 'Georgia', size: 24, color: '333333' })],
  })
),
```

## Section with Page Break

```javascript
// Page break
new Paragraph({ children: [new TextRun({ text: '' })], pageBreakBefore: true }),

// Section heading
new Paragraph({ text: '1. SECTION TITLE', heading: HeadingLevel.HEADING_1, spacing: { after: 200 } }),

// Body paragraph
new Paragraph({
  spacing: { after: 120 },
  children: [new TextRun({ text: 'Body content here...', font: 'Georgia', size: 24 })],
}),

// Bullet list
...['Item 1', 'Item 2'].map(item =>
  new Paragraph({
    spacing: { after: 60 },
    indent: { left: 360 },
    children: [new TextRun({ text: '• ' + item, font: 'Georgia', size: 22 })],
  })
),
```

## Closing

```javascript
new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 400 },
  children: [new TextRun({ text: '— END OF DOCUMENT —', font: 'Georgia', size: 20, italics: true, color: gray })],
}),
```

## Page Margins

```javascript
properties: {
  page: {
    margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 },
  },
},
```
