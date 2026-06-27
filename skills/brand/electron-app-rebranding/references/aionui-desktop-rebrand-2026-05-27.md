# AionUI Desktop → TCHUEKAM Rebrand (28 May 2026)

## App Details

| Field | Value |
|---|---|
| Original App | AionUI Desktop |
| New Name | TchuekamUI |
| Version | 2.1.5 |
| Type | Electron/Chromium desktop app |
| Install path | `D:\TCHUEKAM-AGENT\AionUi\` |
| Original EXE | `AionUi.exe` (204 MB) → `TchuekamUI.exe` |
| Resources asar | `resources\app.asar` (376 MB) |
| Desktop shortcut | `C:\Users\CLINIC\Desktop\AionUi.lnk` → updated |

## Logo Source

- `C:\Users\CLINIC\Desktop\logo of tchuekam.jpg` (4.96 MB JPEG)
- Converted to 512×512 PNG + 256×256 ICO via ffmpeg

## What Changed

**Inside asar (extracted + edited):** 254 replacements of "AionUi" → "TchuekamUI" in `out/main/index.js`, plus 30+ renderer JS files, preload files, index.html, manifest, package.json. Skipped npm dependency names and internal component identifiers (Aionrs, AionScrollArea, AionSelect).

**Outside asar:** `resources/app.png` replaced, `app-update.yml` updated (owner→GiantectEmpire, autoUpdate→false), `manifest.webmanifest` updated.

**EXE:** `TchuekamUI.exe` + uninstaller — icons injected via rcedit, version info strings set.

**Shortcut:** Updated via PowerShell to point to new EXE with new icon.

## Status

asar repack was still running at session end (background process). Backup at `app.asar.backup`. PWA icons (`pwa/icon-192.png`, `pwa/icon-512.png`) not yet updated.
