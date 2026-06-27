# Logseq Direct Integration — How TCHUEKAM Writes to Logseq

## Architecture

Logseq stores data as plain Markdown files in a user-chosen "graph" folder. No API needed — direct file write works.

## Graph Folder Structure

Once user creates a graph, the folder looks like:

```
<graph-root>/
├── logseq/           # config + SQLite cache
├── pages/            # one .md per page
├── journals/         # daily entries: YYYY_MM_DD.md
└── assets/           # attached images/files
```

## Writing a Journal Entry

TCHUEKAM writes directly to `<graph-root>/journals/<YYYY_MM_DD>.md`:

```markdown
- ## Title
  - Bullet point
  - Nested item
    - Deeper item
  - Regular content
```

## Writing a Page

Write to `<graph-root>/pages/<page-name>.md`:

```markdown
- ## Page Title
  - Content here
```

## Logseq Markdown Format Notes

- Logseq uses an outliner format: every line starts with `- ` and indentation creates hierarchy
- Headers use `##` (not `#`) for page-level headings
- Tags: `#tag-name` anywhere
- Links: `[[Page Name]]` to link other pages
- Properties at top of file between `---` lines
- Tasks: `- TODO task text`, `- LATER task text`, `- DONE task text`

## Verification

After writing, user opens Logseq and the entry appears automatically (Logseq watches the folder with chokidar).

## Concrete Example (30 May 2026 session)

User had Logseq graph at `D:\Battle\`. I wrote:

```markdown
- ## Session TCHUEKAM — 30 mai 2026
  - Objectifs du jour :
    - Review des apps open source pour la productivité
    - Obsidian écarté (propriétaire)
```

This appeared in Logseq's journal view immediately when user opened the app.
