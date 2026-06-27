---
name: design-reference-analysis
category: creative
tags: [website-design, branding, visual-analysis, inspiration, mood-board, folder-analysis]
description: Analyze a folder of saved design references (images, videos) to extract a user's aesthetic preferences and recommend a concrete website direction. Covers file scanning, visual analysis (browser), categorization by style clusters, and synthesis into a brand-aligned recommendation.
---

# Design Reference Analysis

Analyze a user's folder of saved reference images/videos to determine the website style that suits them. Non-technical users often collect inspiration without knowing how to define their own taste — this skill bridges that gap.

## When to Use

- User says "I have images in a folder, help me find what suits me"
- User has a `Downloads/Enterprise branding`, `Desktop/website inspo`, or similar folder with design references
- User shares a Pinterest/saved-images collection and asks "what style is this?"
- User is vague about their brand direction but has a saved folder of inspo

## Workflow

### 1. Scan the Folder

```
ls -lh "/path/to/folder/" | grep -iE "\.jpg$|\.png$|\.jpeg$|\.gif$|\.webp$|\.svg$|\.mp4$|\.mov$"
```

Look for:
- Image file extensions (jpg, png, gif, webp)
- Video files (mp4, mov)
- Any .txt files that might contain prompts or brand info (read them)
- Note total count and total size for each media type

### 2. Categorize by Filename

Extract meaning from filenames before visual analysis:
- "futuristic", "VR", "neon", "dark", "cyber" → futuristic/tech aesthetic
- "AI", "automation", "robot", "brain" → AI/branding aesthetic
- "landing page", "high-conversion", "UI/UX" → conversion-focused design
- "agency", "creative", "modern" → agency-style layouts
- "Character" → brand mascot / identity character
- "Generated Image" → AI-generated concepts the user envisioned
- "ChatGPT Image" → user-generated prompts/visions

### 3. Visual Analysis via Browser

Use `browser_navigate` with `file:///` protocol to inspect key images:

```bash
file:///C:/Users/USERNAME/Path/To/Image.jpg
```

Focus on the most descriptive images first — those with meaningful filenames reveal more than numbered/random names.

**What to extract from each image:**
- Color palette (dark/light, neon/subtle, warm/cool)
- Typography style (sans-serif, serif, heavy, thin)
- Layout structure (hero+features, card grid, full-screen)
- UI elements (glow, gradients, shadows, borders)
- Mood (authoritative, playful, minimal, bold)

### 4. Identify Style Clusters

Group images into 2-4 distinct aesthetic clusters. Example clusters:
- **Dark Mode + Neon Accents**: dark backgrounds, cyan/purple glow, tech vibe
- **AI / Automation Branding**: robot characters, networks, data vis
- **High-Conversion Landing Pages**: clean layouts, call-to-action focused, agency-style
- **Minimalist / Corporate**: white/gray, clean lines, professional

### 5. Synthesize Recommendation

Map clusters to the user's actual brand:
- Pick the dominant cluster (most files, strongest emotional pull)
- Cross-reference with their brand (Giantect Empire, AI agent, African tech)
- Recommend concrete: dark/light mode, primary colors, font suggestion, animation style, layout approach

Structure the recommendation:
```
| Feature | Why It Fits |
|---|---|
| Dark theme | Every image you saved uses dark bg |
| Cyan + purple | Your VR/futuristic references use this palette |
| Animated hero | You saved N videos — you want motion |
| ... | ... |
```

## Common Pitfalls

- **Don't rely on `search_files` alone**: Use `tchuekam_index_search(query="keyword")` first for <50ms results across all drives. The user's folder might be under Desktop, Downloads, Documents, or D:\. Try multiple keyword variations before falling back to `Get-ChildItem`/`ls`.
- **File paths with special chars**: Spaces and emoji in filenames. Use `--data-urlencode` or proper escaping. On Windows paths in `file:///` URLs, use `%20` for spaces.
- **Empty .txt files**: Users sometimes create placeholder files. Always read them first, they're often empty.
- **Video analysis limit**: You can see file dimensions and name, but cannot play videos in browser. Describe what filename/meta suggests.
- **Browser rendering of local files**: `browser_navigate` on `file:///` paths shows the raw image — use `browser_console` to inspect `document.querySelector('img')` for dimensions and src. The page itself has no interactive elements, so ref IDs won't appear.
- **Large folders (50+ files)**: Don't analyze every file one-by-one. Batch by filename pattern, pick 5-8 representative images for visual inspection.

## Verification

After delivering the recommendation, ask: "Want me to build the HTML/CSS website based on this style, or show you a mockup first?"
