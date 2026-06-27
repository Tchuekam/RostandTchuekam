# Poem Formatting in .docx

Based on the "L'Aube Intérieure" poem created for the user (session May 26, 2026).

## Layout Pattern for Poems

| Element | Setting |
|---------|---------|
| Title | HeadingLevel.HEADING_1, center-aligned, spacing after 200 |
| Subtitle | Italic, smaller size (20 half-pts), center, colored (#555555), spacing after 400 |
| Verses | Center-aligned, size 24 (12pt), spacing after 120 |
| Stanzas | 4 lines per stanza, spacing after 300 between stanzas |
| Signature | Italic, size 20, muted color (#777777), spacing before 200 |

## Poem Structure Template

```
Title (Heading 1, centered, spacing after 200)
"— A Poem —" (subtitle, italic, centered, spacing after 400)

Verse 1 (centered, spacing after 120)
Verse 2 (centered, spacing after 120)
Verse 3 (centered, spacing after 120)
Verse 4 (centered, spacing after 300)  ← stanza break

Verse 5-8 (same pattern)
...

— Signature (italic, muted, centered, spacing before 200)
```

## Color Palette for Poems

| Element | Color | Hex |
|---------|-------|-----|
| Body text | near-black (default) | `000000` |
| Subtitle | muted gray | `555555` |
| Signature | lighter gray | `777777` |
| Title | default (dark) | `000000` |

## Font Choice

- **Georgia** for classic/traditional poems (serif, elegant)
- **Calibri** for modern/minimal poems
- Title font can differ from body if desired

## Node.js Implementation Reference

```javascript
const docx = require('C:\\Users\\CLINIC\\AppData\\Roaming\\npm\\node_modules\\docx');
const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, AlignmentType, HeadingLevel } = docx;

// Font sizing: 24 half-points = 12pt
// Each verse is a Paragraph with AlignmentType.CENTER
// Use spacing: { after: 300 } between stanzas
// Add spacing: { after: 120 } within a stanza's lines
```
