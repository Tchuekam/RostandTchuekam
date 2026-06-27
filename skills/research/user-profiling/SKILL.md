---
name: user-profiling
description: "Infer a human-readable profile of the user from their filesystem artifacts — Desktop content, Documents, Downloads, Pictures, Videos, project folders, bookmarks, and reading material."
version: 1.0.0
author: tchuekam
platforms: [windows]
---

# User Profiling from Filesystem Artifacts

Build a rich, human-readable profile of the user by scanning their computer's file system. Use this when the user asks "what can you say about me?" or when you need to understand their context to serve them better.

## Trigger

- User asks: "what do you know about me?", "what can you say about me?", "based on my files..."
- Beginning of a new relationship with a user (first few sessions)
- User mentions they want you to "understand" them better

## Scanning Strategy

Scan in priority order, from highest-signal to lowest:

### 1. Desktop files
```bash
ls -la /c/Users/$USER/Desktop/
```
- .docx files → read content for projects, pitches, business plans
- .txt files → notes, API keys, to-do lists, research
- .lnk files → frequently used apps (reveals tools, hobbies)
- Folder names → project names, client work

### 2. Documents folder
```bash
find /c/Users/$USER/Documents -maxdepth 2 -type f 2>/dev/null | head -40
```

### 3. DownloadV1 (or Downloads) — project folders and content
```bash
find /d/DownloadV1 -maxdepth 2 -type d 2>/dev/null
find /d/DownloadV1 -maxdepth 1 -type f -iname '*.pdf' -printf '%f\n' 2>/dev/null
```
- Books (PDFs) reveal reading interests: strategy, self-help, technical
- Project folders reveal active development work
- Zip files with project names → SaaS ideas, side projects

### 4. Books folder
```bash
find /d/DownloadV1/books -maxdepth 1 -type f -printf '%f\t%s\n' 2>/dev/null
```
- Titles like "48 Laws of Power", "Art of War", "How to Win Friends" → strategic/leadership mindset
- Project zip files → building vs consuming ratio

### 5. Pictures / Screenshots
```bash
ls -la /c/Users/$USER/Pictures/Screenshots/
ls -la /c/Users/$USER/Pictures/Saved\ Pictures/
```
- Screenshot frequency → active learning, debugging, design comparisons
- Saved images → graphic design inspiration, flyer layouts, branding

### 6. Video titles
```bash
find /d/DownloadV1 -maxdepth 1 -type f -iname '*.mp4' -printf '%f\n' 2>/dev/null
```
- Named vs unnamed videos → curation habits
- Content sources (snaptik_*, WhatsApp Video, YouTube) → platforms they consume from

### 7. Text notes on Desktop
```bash
cat /c/Users/$USER/Desktop/*.txt 2>/dev/null
```
- Research notes (chatbot comparison tables, API keys, website lists)
- Work logs, deployment commands, project ideas

### 8. Client folders
```bash
ls -la /c/Users/$USER/Desktop/cliente/ 2>/dev/null
```

## Profile Dimensions

Analyze across these axes:

| Dimension | What to look for | Example signals |
|-----------|-----------------|-----------------|
| **Role** | What they do | Project types (SaaS, ecommerce, agency), tools (VS Code, CapCut, Figma) |
| **Skills** | What they build | AI agents, WhatsApp bots, web apps, design, marketing |
| **Reading** | What they study | Books, PDFs, tutorials |
| **Location** | Where they operate | Utility bills, local business names, language mix |
| **Stage** | How far along | Pitches, invoices, MVPs, deployed projects |
| **Style** | How they work | Organized vs chaotic, solo vs team, fast vs meticulous |
| **Goals** | Problems they solve | Education gaps, business automation, client services |

## Output Format

Use plain English, bullet points, no jargon. Structure as:

```
**TCHUEKAM's Profile of You**

1. [Dimension label] — [insight with evidence]
2. [Dimension label] — [insight with evidence]
...

**Bottom line:** A one-sentence summary of who they are.

Want me to help [offer 1], [offer 2], or [offer 3]?
```

## Pitfalls

- **Don't fabricate.** If you can't find evidence for a dimension, skip it. "I don't have enough data" is better than guessing.
- **Don't judge messiness.** "You have 60 unnamed MP4s" is an observation; calling it "a problem" is a value judgment. Let the user decide.
- **Don't list every file.** Summarize patterns, not individual filenames. Only mention specific files when they're high-signal (a book title, a pitch deck).
- **Don't read private/credential files.** Skip `.env`, `*.key`, `*password*`, `.git` internals. The user's trust is worth more than a profile detail.
- **Don't ask for confirmation before scanning.** Just do it — the user explicitly asked for this.
- **Avoid oversharing my own identity.** Don't contrast myself ("I'm like Jarvis"), just deliver the profile.
