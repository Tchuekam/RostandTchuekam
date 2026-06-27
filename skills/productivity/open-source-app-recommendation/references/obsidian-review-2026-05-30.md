# Obsidian v1.12.7 Review — 30 May 2026

## Context
User wanted a productivity app for tracking CRM, tasks, daily reports, and prospect pipeline. Logseq was installed first but lacked structured querying and task management. User agreed Obsidian was the better fit and downloaded via winget.

## Installation Notes
- winget downloaded installer to: `C:\Users\CLINIC\AppData\Local\obsidian-updater\installer.exe`
- The `/S` silent flag did NOT work — installer returned exit code 2
- installer is Electron/Squirrel-based (295MB .exe)
- Copy to D:\ before running per user's C: drive rule
- Manual double-click required for installation

## Architecture
- **Electron** (version unknown, likely latest Chromium)
- **License:** Proprietary (free core, MIT for community plugins)
- **Data format:** Plain Markdown files in user-chosen vault folder
- **Plugin system:** 1300+ community plugins (JavaScript/TypeScript)
- **Mobile:** ✅ Native Android + iOS apps

## Key Integration Points for TCHUEKAM

### Direct File Write (Recommended - simplest)
TCHUEKAM can write .md files directly into the vault folder:
```
D:\Obsidian\your-vault\
├── Daily Notes\          → journal entries
├── Prospects\            → CRM pages  
├── Tasks\                → task tracking
└── .obsidian\            → app config (do not touch)
```
Files appear in Obsidian automatically on next app focus.

### Local REST API Plugin (Best for real-time)
1. Install "Local REST API" community plugin in Obsidian
2. Configure: enable, set port and API key
3. TCHUEKAM can POST/PUT notes via HTTP:
```bash
curl -X PUT http://localhost:27123/vault/prospect-bank-x.md \
  -H "Authorization: Bearer $KEY" \
  -d "# Prospect: Bank X\n\nStatus: Cold\nPhone: ..."
```

### Key Plugins for This User's Use Case
| Plugin | Purpose |
|---|---|
| Dataview | Query notes like a database (SQL-style) — track prospects, tasks, statuses |
| Tasks | Checkbox task management with dates, priorities, filtering |
| Kanban | Visual pipeline view of prospects/stages |
| Local REST API | HTTP bridge for TCHUEKAM to push/pull notes |
| Periodic Notes | Auto-create daily/weekly/monthly notes |
| Calendar | Visual calendar view of daily notes |

## Why Obsidian > Logseq for This User

| Capability | Obsidian | Logseq |
|---|---|---|
| Prospect CRM (structured data) | ✅ Dataview plugin | ❌ Manual only |
| Task management | ✅ Tasks plugin | ⚠️ Outliner only |
| Kanban pipeline | ✅ Kanban plugin | ❌ |
| HTTP API for agent integration | ✅ Local REST API | ❌ (unofficial plugin only) |
| Daily journaling | ✅ Periodic Notes | ✅ Built-in journal |
| Mobile | ✅ Android + iOS | ✅ Android + iOS |
| Plugin ecosystem | 1300+ plugins | ~100 plugins |
