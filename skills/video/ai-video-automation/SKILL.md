---
name: ai-video-automation
title: AI Video Automation Pipeline
description: Design and document dual-AI video editing pipelines where Gemini CLI (Vision + reasoning) and TCHUEKAM (timeline execution) work together to auto-create, edit, and export videos from user prompts. Covers architecture, role separation, JSON edit plans, suggestion loops, and integration with DavCut, Shotcut, or other video editors.
category: video
tags:
  - video
  - automation
  - gemini-cli
  - davcut
  - shotcut
  - editing
  - pipeline
  - dual-ai
trigger: user asks about AI video creation, auto-editing, integrating AI into video editors, or building a "make video from prompt" pipeline
version: 1.0.0
author: giantect
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [video, automation, gemini-cli, davcut, shotcut, editing, pipeline, dual-ai]
    related_skills: [open-source-app-recommendation]
---

# AI Video Automation Pipeline

Design a dual-AI video editing system where the user describes a video in natural language, and two agents collaborate to produce the result autonomously.

## Architecture Overview

```
[User Prompt]
      │
      ▼
┌─────────────────────────────────────────┐
│            GEMINI CLI v0.44.1           │
│  (google-gemini, ACP-capable)           │
│                                         │
│  Rôles :                                │
│  - Vision : analyse les vignettes       │
│  - Scores clips (0-100)                 │
│  - Génère script voiceover              │
│  - Suggère améliorations post-draft     │
│  - Assigne mood tags                    │
└────────────────┬────────────────────────┘
                 │  JSON Edit Plan
                 ▼
┌─────────────────────────────────────────┐
│         TCHUEKAM (Hermes Agent)          │
│  (DeepSeek, GODMODE-enabled)            │
│                                         │
│  Rôles :                                │
│  - Reçoit le plan JSON de Gemini        │
│  - Construit la timeline DavCut         │
│  - Applique transitions + filtres       │
│  - Syncro sur les beats musicaux        │
│  - Déclenche l'export                   │
│  - Boucle sur nouveau prompt            │
└────────────────┬────────────────────────┘
                 │
                 ▼
         [DAVCUT TIMELINE]
                 │
                 ▼
         [USER REVIEW]
                 │
         ┌───────┴───────┐
         ▼               ▼
    [Gemini Review]  [User Override]
         │               │
         └───────┬───────┘
                 ▼
         [TCHUEKAM Applique]
                 │
                 ▼
         [FINAL EXPORT]
```

## Role Separation

| Task | Gemini CLI (ACP) | TCHUEKAM (Hermes) |
|------|------------------|-------------------|
| Interpret prompt intent | ✅ | ❌ |
| Scan clips via Vision (thumbnails) | ✅ Scores 0-100 | ❌ |
| Select best moments + timestamps | ✅ | ❌ |
| Write voiceover script | ✅ | ❌ |
| Mood detection (cinematic, energetic, etc.) | ✅ | ❌ |
| Post-draft suggestions (structured JSON) | ✅ | ❌ |
| Build timeline in editor | ❌ | ✅ |
| Apply transitions, filters, color grade | ❌ | ✅ |
| Beat-sync audio (waveform → cuts) | ❌ | ✅ |
| Caption placement | ❌ | ✅ |
| Trigger export with optimal settings | ❌ | ✅ |
| Re-run pipeline on new prompt | ❌ | ✅ |

## JSON Edit Plan (Gemini → TCHUEKAM)

Gemini CLI receives user prompt + scans clip thumbnails, then produces:

```json
{
  "plan": {
    "mood": "cinematic",
    "duration_seconds": 60,
    "format": "youtube",
    "music_vibe": "upbeat_orchestral"
  },
  "clips": [
    {"file": "clip_01.mp4", "rank": 95, "start_at": 2.5, "duration": 8.0, "caption": "Welcome to the journey"},
    {"file": "clip_03.mp4", "rank": 88, "start_at": 0.0, "duration": 6.0, "caption": "Through the mountains"}
  ],
  "voiceover": "Full script text here...",
  "transitions": [
    {"between": [0, 1], "type": "crossfade", "duration": 0.5},
    {"between": [1, 2], "type": "fade_black", "duration": 1.0}
  ]
}
```

## Post-Draft Suggestion Loop

After TCHUEKAM builds the timeline, Gemini reviews the draft and outputs:

```json
{
  "suggestions": [
    {"type": "trim", "clip": 3, "action": "trim_end", "by_seconds": 4},
    {"type": "transition", "between": [4, 5], "effect": "fade_black"},
    {"type": "caption_sync", "clip": 2, "shift_ms": -300},
    {"type": "filter", "clip": 1, "apply": "warm_tone"}
  ]
}
```

User checks ✅ or ❌ per suggestion → TCHUEKAM applies accepted ones.

## Interface: AI Studio Mode (Suggested UI)

```
┌──────────────────────────────────────────────┐
│  🎬 AI STUDIO                                 │
├──────────────────────────────────────────────┤
│                                                │
│  📁 Drop your raw footage here                 │
│                                                │
│  ✏️  Describe your video:                      │
│  ┌────────────────────────────────────────┐   │
│  │ "Make a 60s travel reel, cinematic"    │   │
│  └────────────────────────────────────────┘   │
│                                                │
│  🎵 Music: [ Upload ] or [ Auto-suggest ]     │
│  📺 Format: [YouTube] [TikTok] [Instagram]    │
│  ⏱️  Duration: [Auto] [30s] [60s] [3min]      │
│                                                │
│  [        🚀 AUTO-GENERATE MY VIDEO        ]   │
│                                                │
├──────────────────────────────────────────────┤
│  🤖 AI LOG (live feed):                       │
│  ✅ Gemini scanned 12 clips → selected 7      │
│  ✅ Mood detected: Cinematic                   │
│  ⏳ Tchuekam building timeline...              │
└──────────────────────────────────────────────┘
```

## Pitfalls & User Preferences
- **User Preference (Visual/Branding)**: User demands a "trending" style with phonk beats and ultra-dynamic edits.
- **Workflow Update**: When editing for the user, prioritise high-tempo, rhythm-synced cuts rather than standard narrative editing.
- **Data Handling**: The user stores media in `D:\NewDownloadAgent`. **CRITICAL**: This path is outside the allowed workspace. You MUST copy required assets to the project workspace (`D:\hermes-home\Tchuekam-Agent-main\hermes-agent-main`) before the video automation pipeline can access them. Do not try to reference files in `D:\NewDownloadAgent` directly.
## Technical Constraints
- **Aspect Ratio Mismatch:** When concatenating videos with different resolutions (e.g., 1920x1080 and 720x1280), FFmpeg `concat` will fail unless explicitly scaled to a common format. Always use `scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1` in the filter complex.
- **Speed Ramping:** To achieve a "Phonk" or "trending" aesthetic, use `setpts=0.5*PTS` (for 2x speed) or similar multipliers within the filter chain.
- **Audio Sync:** When mixing video and audio streams, use `-shortest` to ensure the final output matches the shortest input stream (usually the audio track) to prevent trailing video or audio drift.
- **FFmpeg Filter Complex:** When building complex filter strings, pass them as single, escaped arguments to `terminal` to avoid shell parsing errors. Always test with `-y` to overwrite existing files without hanging.

- **TCHUEKAM → Gemini:** ACP bridge configured in Hermes (`hermes config set agent.acp_command "gemini"`, `agent.acp_args "--acp --stdio"`). Or simple pipe: `echo "<json>" | gemini -p "..."`.
- **Gemini → TCHUEKAM:** JSON returned via stdout
- **Video editor target:** DavCut (preferred) or Shotcut (fallback via MLT project files + CLI render)
- **Non-destructive:** Original files never modified. All edits undoable.
- **Async:** All AI processing runs in background. Live progress shown in AI Log.
- **Offline resilience:** If either AI goes offline mid-process → pause and notify user, don't crash.
- **Manual override:** User can take over from AI at any point.

## Related

- `open-source-app-recommendation` — video editor comparisons (Shotcut, LosslessCut, DaVinci Resolve, CapCut)
- `references/davcut-pipeline-prompt-2026-05-30.md` — the full refined DavCut pipeline prompt document
