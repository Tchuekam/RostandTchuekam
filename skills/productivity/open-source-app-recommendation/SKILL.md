---
name: open-source-app-recommendation
title: Open-Source App Recommendation
description: Systematically evaluate and recommend open-source desktop and mobile applications for non-technical founders. Covers architecture analysis, integration potential (agent/AI hook-in), mobile availability, licensing, and producing a ranked comparison. For founders who want to adopt existing software rather than build from scratch.
category: productivity
tags:
  - open-source
  - app-evaluation
  - recommendation
  - electron
  - desktop
  - mobile
  - foss
  - integration
  - agent-hook
trigger: user asks for app recommendations — "what app should I use for X", "recommend an open-source tool for Y", "I need a [category] app", "what's good for [task]", "compare [app X] and [app Y]"
version: 1.1.0
author: giantect
license: MIT
platforms: [windows, android, ios]
metadata:
  hermes:
    tags: [open-source, app-evaluation, recommendation, electron, foss, integration, agent-hook]
    related_skills: [electron-app-rebranding, ai-frontend-branding, startup-operations-planning, windows-file-organization]
---

# Open-Source App Recommendation

Evaluate and recommend open-source desktop + mobile applications for a non-technical founder who wants to adopt existing tools and integrate them with their AI agent (TCHUEKAM). The goal: recommend apps where the agent can hook in via file writes, plugins, HTTP APIs, or CLI commands.

## When to Use

- User says "I need a [category] app" and doesn't want to build
- User asks to compare two or more apps in the same category (e.g. Logseq vs Obsidian, Shotcut vs Kdenlive)
- User downloaded an app and wants you to review it → check D:\NewDownloadAgent\ and AppData\Local\Programs\
- User asks "can I integrate you with [app]?"
- User mentions wanting both desktop + mobile availability

## Evaluation Framework — 7 Axes

For each app under consideration, assess these 7 axes before making a recommendation:

### 1. Architecture & Tech Stack
- **Electron?** (Chrome-like, resource heavy, easy to mod via asar)
- **Native?** (C++, Qt, GTK — harder to mod but lighter)
- **Web-based?** (PWA, React Native, Tauri)
- Determine: `install location`, `data storage format`, `config files`, `plugin system`

Commands:
```bash
# Find install location
which appname 2>/dev/null
find /c/Users/$USER/AppData -maxdepth 4 -iname "*appname*" -type f 2>/dev/null | head -10
find /c/Program\ Files -maxdepth 2 -iname "*appname*" 2>/dev/null | head -10
find /d -maxdepth 3 -iname "*appname*" -type d 2>/dev/null | head -10

# Check license (package.json for Electron apps)
cat "path/to/resources/app/package.json" | grep -E '"license"|"version"|"productName"' 

# Check data directory
find /c/Users/$USER/AppData -maxdepth 4 -iname "*appname*" -type d 2>/dev/null
```

### 2. Data Storage & Accessibility
- **Plain files?** (Markdown, JSON, CSV) → agent can write directly = excellent
- **SQLite DB?** → agent can query/write = good, but needs SQL knowledge
- **Proprietary binary?** → agent cannot write = poor
- **Cloud-locked?** → agent cannot write offline = poor

### 3. Agent Integration Potential
How can TCHUEKAM hook into the app?

| Integration Level | Method | Example |
|---|---|---|
| **Direct file write** | Agent writes .md/.json to app's data folder | Obsidian/Logseq vaults |
| **HTTP API** | App exposes REST/WebSocket endpoint | Obsidian Local REST API, Logseq API plugin |
| **CLI commands** | App has a headless CLI | Shotcut `-filter`, FFmpeg |
| **Plugin system** | Agent installs a plugin that bridges communication | Obsidian plugins, Logseq plugins |
| **Launch & automate** | Agent starts the app with args / sends keystrokes | LosslessCut, video editors |

### 4. License & Business Fit
Check the license. For commercial use (selling a product/service built on top):
- **MIT / Apache 2.0** = safest, can integrate freely
- **GPL / AGPL** = must open-source derivative work (can still integrate but careful)
- **AGPL** = Logseq, some others — fine for internal use, may need lawyer for commercial redistribution

Command:
```bash
# From package.json (Electron apps)
grep "license" "path/to/package.json"

# From LICENSE file
head -5 "path/to/LICENSE"
```

### 5. Mobile Availability
| Status | Meaning |
|---|---|
| ✅ Native (Android + iOS) | Full mobile experience |
| ✅ PWA-only | Mobile browser accessible, limited native features |
| ❌ Desktop only | No mobile version |
| ⚠️ Third-party wrapper | Unofficial mobile port |

Always check the app's official website or GitHub README for mobile info. Don't assume.

### 6. Platform Coverage
| Windows | macOS | Linux | Android | iOS | Rating |
|---|---|---|---|---|---|
| ✅ | ✅ | ✅ | ✅ | ✅ | Excellent (true cross-platform) |
| ✅ | ✅ | ✅ | ❌ | ❌ | Desktop only |
| ✅ | ❌ | ❌ | ❌ | ❌ | Windows only (rare for FOSS) |

### 7. Maturity & Community
- GitHub stars / release cadence
- Plugin ecosystem size (for knowledge management apps)
- Active development (check last release date from VERSION file or package.json)
- Documentation quality
- Known bugs or limitations for your use case

## Recommendation Workflow

### 1. Understand the user's NEED, not just the app category

Don't just ask "what kind of app?" — surface the real need:

User says: "I need a productivity app"
→ Ask: "What do you want to track? Tasks? Projects? Daily reports? Prospects?"

User says: "I need a video editor"
→ Ask: "Cutting clips? Full production with effects? Just trimming? Making reels?"

### 2. Search system for existing apps first

Before recommending, check if the user already has the app installed:
```bash
winget list --query "AppName" 2>/dev/null
which appname 2>/dev/null
ls "C:/Users/$USER/AppData/Local/Programs/" 2>/dev/null
ls "/c/Users/$USER/AppData/Local/" | grep -iE "appname|keyword"
```

### 3. If user downloaded a specific app, review it first

Check in D:\NewDownloadAgent\ (the user's download staging folder):
```bash
ls -la /d/NewDownloadAgent/*appname* 2>/dev/null
```

If found, examine the installed version (not just the installer):
```bash
find /c/Users/$USER/AppData -maxdepth 4 -iname "*appname*" -type f 2>/dev/null
```

Then produce an analysis using the 7-axis framework above.

### 4. For comparison requests — produce a decision table

When user asks "A vs B", structure as a comparison table:

| Criterion | App A | App B | Winner |
|---|---|---|---|
| Data storage | Plain Markdown | Plain Markdown | Tie |
| Agent integration | Direct file + API | Direct file only | A |
| Mobile | ✅ Native | ✅ Native | Tie |
| License | AGPL-3.0 | MIT | B |
| Plugin ecosystem | Small | Massive | B |
| Learning curve | Easy (outliner) | Easy | Tie |
| **Your use case** | Good for journaling | Better for structured data | B |

End with a clear verdict: "For your [specific need], I recommend [app] because [reason]."

### 5. Always explain integration strategy concretely

Don't say "we can integrate it". Say exactly how:

- "I can write .md files to `~/Logseq/pages/` — they appear as pages in Logseq"
- "I can call `obsidian-api` plugin's REST endpoint to push notes"
- "I can feed Shotcut an MLT project file and it renders from CLI"

### 6. Address mobile explicitly

Non-technical African founders often do most of their work from their phone. If the app has no mobile version, say so clearly and suggest a mobile alternative.

## Standard Recommendations Reference

### Productivity / Knowledge Management

| App | Best For | Integration | Mobile | License | FOSS? |
|---|---|---|---|---|---|
| **Obsidian** | Structured notes, tasks, CRM | Direct file + HTTP API plugin | ✅ | Proprietary | ❌ NO — core is closed-source |
### Productivity / Knowledge Management

| App | Best For | Integration | Mobile | License | FOSS? |
|---|---|---|---|---|---|
| **Obsidian** | Structured notes, tasks, CRM | Direct file + HTTP API plugin | ✅ | Proprietary | ❌ NO — core is closed-source |
| **Logseq** | Journaling, outliner notes | Direct file | ✅ | AGPL-3.0 | ✅ Yes |
| **Notion** | All-in-one workspace | API via curl | ✅ | Proprietary | ❌ NO |

See `references/davcut-shotcut-fork-evaluation.md` — full DavCut architecture, Whisper/OpenCV/GGML components, MLT XML format, integration strategy, and dual-agent pipeline design.
See `references/logseq-review-2026-05-30.md` for full Logseq evaluation (architecture, integration analysis, capability matrix, comparison vs Obsidian).
See `references/logseq-direct-integration.md` for concrete workflow: writing journal entries and pages directly via file write.
See `references/obsidian-review-2026-05-30.md` for full Obsidian evaluation (integration, plugins, comparison vs Logseq).
See `references/logseq-direct-integration.md` for concrete workflow: writing journal entries and pages directly via file write.
See `references/obsidian-review-2026-05-30.md` for full Obsidian evaluation (integration, plugins, comparison vs Logseq).

### Video Editing

| App | Best For | Integration | Mobile | License | FOSS? |
|---|---|---|---|---|---|
| **Shotcut** | Full production (multi-track, keyframes, color) | CLI render via MLT project files | ❌ | GPL-3.0 | ✅ Yes |
| **DavCut** | **Shotcut fork** with Whisper + OpenCV + GGML baked in | CLI via melt.exe + MLT XML projects | ❌ | GPL-3.0 | ✅ Yes (derived from Shotcut) |
| **LosslessCut** | Fast trimming (no re-encode) | CLI `--cut` | ❌ | MIT | ✅ Yes |
| **DaVinci Resolve** | Professional grade | Studio API (paid) | ✅ (iOS) | Freemium | ❌ NO |
| **CapCut** | Quick reels | Manual only | ✅ | Proprietary | ❌ NO |

**DavCut (Shotcut fork):** Found at `D:\Battle\ProductivityApps\DavCut\`. Includes `libwhisper.dll` (transcription), `libopencv*.dll` (vision), `ggml.dll`/`ggml-vulkan.dll` (local AI inference), `melt.exe` (headless renderer), and full Qt6/MLT stack. Integration method: write `.mlt` XML project files, then run `melt.exe project.mlt -consumer avformat:output.mp4` for headless render. Or let user open the `.mlt` in DavCut GUI for preview + manual tweaks before export.

## Dual-Agent App Integration Pattern (Video Editing)

When the user wants TWO AIs working inside a third-party app (e.g. DavCut), the pattern is:

```
[User Prompt]
      │
      ▼
[TCHUEKAM CLI (Gemini)] ── Vision + Creativity
      │  - scans footage via Gemini Vision
      │  - scores clips 0-100
      │  - detects mood tag
      │  - writes voiceover script
      │  - post-draft: reviews and suggests improvements
      │
      │  JSON edit plan
      ▼
[TCHUEKAM (Hermes/DeepSeek)] ── Execution + Control
      │  - builds timeline in the app
      │  - applies transitions, filters, color grade
      │  - syncs cuts to music beats
      │  - adds captions
      │  - manages export
      ▼
[User Review] ←→ [Gemini suggests improvements]
      │
      ▼
[Hermes applies accepted suggestions]
```

**JSON exchange format:**
```json
// Edit plan (Gemini → Hermes)
{
  "clips": [{"file": "clip01.mp4", "rank": 95, "start_at": 2.5, "duration": 8.0, "caption": "..."}],
  "mood": "cinematic",
  "voiceover": "Full script...",
  "transitions": [{"between": [0, 1], "type": "crossfade", "duration": 0.5}]
}

// Suggestions post-draft (Gemini → Hermes)
{
  "suggestions": [
    {"type": "trim", "clip": 3, "action": "trim_end", "by_seconds": 4},
    {"type": "transition", "between": [4, 5], "effect": "fade_black"},
    {"type": "caption_sync", "clip": 2, "shift_ms": -300},
    {"type": "filter", "clip": 1, "apply": "warm_tone"}
  ]
}
```

**Rules:**
- Gemini does creativity (vision, script, suggestions). Hermes does execution (timeline, filters, export).
- No export without user approval.
- Every action in Undo history.
- Non-destructive: originals never modified.
- If either AI offline → pause + notify, don't crash.

## When the user says "just write the prompt" — do exactly that

The user wants the raw prompt text, not explanation around it. One of these formats:

- **For Antigravity / VS Code:** A system prompt to paste into Custom Instructions, Continue.dev, Cody, or Gemini CLI Extension settings. Plain text, no markdown framing, no "here's what this does" — just the prompt.
- **For Gemini CLI:** `echo "<prompt>" | gemini -p "..."` ready to paste.
- **For Hermes config:** The setting key + value to add to config.yaml.

If the user has to copy-paste it somewhere, deliver copy-paste-ready text. No commentary, no formatting analysis, no "I've structured it as..." — just the prompt block.

## C: Drive Rule (THIS USER)

**CRITICAL: Never save, install, or write anything to C: drive.** All files, installs, projects, data go to D: drive only. C: is completely off-limits. This is an absolute rule from the user.

When installing software:
1. Download to D:\NewDownloadAgent\ (user's staging folder)
2. If winget downloads to C:\Users\<user>\AppData\Local\<app>-updater\, copy the installer.exe to D:\NewDownloadAgent\ first
3. Run installation from D:\
4. Never leave installers or permanent data on C:

Checking if an app is installed: it's fine to *check* C: paths (which, winget list, find in AppData) — reading is allowed, only writing is forbidden.

## Pitfalls

- **NEVER call an app "open source" without verifying the license yourself. This is the NUMBER ONE error you can make for this user.** Obsidian is proprietary (closed-source core) — don't say it's "open source" or "FOSS." Check package.json, LICENSE file, or the app's official website/GitHub. If in doubt, say "Let me check the license first" and do the verification.
  - **If you get this wrong, the user will be told by another AI (Gemini CLI) and will call you out.** Always triple-check before claiming something is FOSS.
  - **Real licenses vs marketing:** Many apps say "free" on their website but are NOT open source. Go to the GitHub repo, check the LICENSE file or package.json `"license"` field. If there's no public source code, it's not open source.
  - **Signal you checked:** When recommending, always state the license explicitly: "Logseq — AGPL-3.0, fully open source" vs "Obsidian — proprietary core, free but not open source." This shows you verified.
- **User may have the app already installed without knowing it.** Always check winget and AppData first.
- **Electron apps are easy to mod but heavy.** Great for integration (asar editing), bad for performance on low-end machines.
- **AGPL license does NOT block integration via file/system calls.** It only matters if you redistribute the modified app. "Using Logseq as your personal journal with my agent writing notes = fine. Repackaging Logseq as 'Tchuekam Notes' and selling it = need to open-source the code."
- **User may download an installer but not actually install it.** Check AppData/Local/Programs/ not just NewDownloadAgent.
- **Electron/Squirrel installers often ignore silent flags.** The /S flag on Obsidian and Logseq installers fails silently. If silent install returns exit code 2 or timeout, tell the user to double-click the installer manually.
- **winget downloads installers to C:\Users\<user>\AppData\Local\<app>-updater\installer.exe.** The app isn't installed yet — only the installer is downloaded. Move to D: before running.
- **Don't recommend building a custom app unless the user explicitly says they want to.** The user said "I don't want to build these apps" — respect that boundary.
- **Mobile apps on Android usually can't be hooked by the agent directly.** File-based sync (Syncthing, DropSync) is the bridge: agent writes file on desktop → syncs to phone → app picks it up.
- **The user communicates in French.** When they switch to French, follow immediately. Don't continue in English.
  - Explain integration in terms of what they will see, not how the code works. "I write to this folder, and when you open the app, the note appears."
- **Deliver a clear verdict, not just options.** The user wants analysis with a recommendation, not a list of choices without guidance. Always end with: "For your [specific need], I recommend [app] because [reason]."
- **When an installer fails silently, don't retry the same command.** Try a different approach (copy to D:, use different flag, or ask user to run manually). The user gets frustrated with repeated failed attempts.
## Reference Files

- `references/logseq-review-2026-05-30.md` — Full Logseq v0.10.15 evaluation: architecture, integration analysis, capability matrix, comparison with Obsidian
- `references/antigravity-ide-config.md` — Antigravity IDE (VS Code fork) paths, settings injection, extension system
- `references/windows-disk-scan-c-drive.md` — Technique for scanning C: drive when `du` is too slow (98% full, thousands of files). PowerShell-based targeted scan of common space hogs.
