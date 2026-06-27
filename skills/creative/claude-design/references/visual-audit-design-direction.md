# Visual Audit → Design Direction

Extract a design direction from a user's folder of reference images, screenshots, and videos. Use this when the user says "I have a folder of inspo — look at it and tell me what style suits me" rather than describing what they want.

## When to Use

- User says: "look at these images in my folder and tell me what style I'm into"
- User says: "I have reference designs saved, figure out what I want"
- User is non-technical and cannot articulate design vocabulary (dark/light, minimalist/complex)
- User has a collection of saved Pinterest posts, Dribbble shots, AI-generated mockups, or website screenshots

## Step 1: Locate the Folder

Ask the user for the folder path, or if they say "my inspo folder" or similar, search proactively. Common locations on Windows:
- `$env:USERPROFILE\Desktop\` subfolders (branding/, inspiration/, design/)
- `$env:USERPROFILE\Downloads\` subfolders
- `$env:USERPROFILE\Pictures\` subfolders

On MSYS/bash (Hermes terminal): `/c/Users/$USER/Desktop/`, `/c/Users/$USER/Downloads/`

## Step 2: Catalog Contents by Extension

Find all image and video files using search_files or terminal:

```bash
search_files *.png, *.jpg, *.jpeg, *.gif, *.webp, *.svg
search_files *.mp4, *.mov, *.webm
```

Note the **total count** and the **meaningful filenames** — users often save images with descriptive names from Pinterest/Dribbble/Twitter that directly reveal what they were inspired by (e.g. "NeoVision – Futuristic Tech & VR Website Design", "Creative Agency Landing Page UI_UX", "Save this sleek SHRUHH login page concept").

## Step 3: Classify by Visual Theme

Read filenames and view images to classify across these axes:

| Axis | What to look for |
|---|---|
| **Light vs Dark** | Background color dominance |
| **Accent colors** | Repeated accent hues (cyan, purple, green, orange, gold) |
| **Layout density** | Sparse/editorial vs dense/data-rich |
| **Typography** | Serif (premium/editorial) vs sans-serif (modern/technical) vs monospace (developer) |
| **Effects** | Neon glow, gradients, glassmorphism, grain, 3D |
| **Content type** | Landing pages, dashboards, login screens, flyers, social media graphics |
| **Vibes** | Words from filenames: "futuristic", "VR", "creative agency", "AI", "enterprise", "minimal", "sleek" |
| **Video motion** | 3D rotation, scroll animations, particle effects, UI walkthroughs |

Use browser_navigate with the file:// URL to view key images and verify visual characteristics.

## Step 4: Count Clusters

Which style appears most? Count by:
- Number of files per cluster
- Recency (newest files = current taste, older = passing interest)
- Resolution/quality (high-res generated images = intentional, low-res screenshots = casual save)

## Step 5: Synthesize the Design Brief

Output a structured recommendation:

```markdown
## Your Design DNA

### Dominant Aesthetic
[One paragraph on the strongest pattern — e.g. "Dark futuristic tech with neon cyan/purple accents"]

### Color Palette (extracted)
- Backgrounds: 
- Primary accent: 
- Secondary accent: 
- Text/surfaces: 

### Typography Direction

### Layout Preferences

### Motion/Vibe

### References in your folder that capture this
- [filename 1] — describes the [specific element]
- [filename 2] — captures the [specific quality]

### What to AVOID (styles absent from your folder)
```

## Pitfalls

- **Don't ask the user what they want before analyzing.** The whole point is that they don't know. Look at the folder first, then present findings.
- **Don't list every file.** Group by pattern, name the clusters. Only cite individual files as examples of a cluster.
- **Ignore empty or zero-byte files** (common in Downloads folders from failed saves).
- **Text files in the folder may contain prompts** the user generated their images with — read them for clues.
- **Don't assume the most files = the right direction.** Sometimes 3 high-quality generated images matter more than 40 random Pinterest saves. Weight by intentionality.
- **Videos that are all 720w with hash-based names** are likely reposted/recompressed copies — treat as one cluster rather than 10 data points.
- **Browser file:// navigation works for single images** — use `browser_navigate(url="file:///C:/path/to/image.jpg")` to view images, then `browser_get_images()` to extract the src. This gives visual confirmation beyond filename analysis.
