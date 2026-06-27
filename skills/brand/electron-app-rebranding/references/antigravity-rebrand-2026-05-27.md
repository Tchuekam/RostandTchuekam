# Google Antigravity → TchuekamUI Rebrand (27 May 2026)

## App Details

| Field | Value |
|---|---|
| App | Antigravity (Google) |
| Version | 2.0.6 |
| Type | Electron desktop app |
| Install path | `C:\Users\CLINIC\AppData\Local\Programs\Antigravity\` |
| Executable | `Antigravity.exe` |
| Resources | `resources\app.asar` (electron bundle) |
| Data dir | `C:\Users\CLINIC\.gemini\antigravity\` |

## Assets Found Inside app.asar

| Asset | Size | Purpose |
|---|---|---|
| `\icon.png` | 512×512 RGBA PNG | App icon (taskbar, window header, file explorer) |
| `\trayTemplate.png` | 22×22 RGBA PNG | System tray icon |
| `\trayTemplate@2x.png` | 44×44 RGBA PNG | HiDPI tray icon |
| `\package.json` | — | App metadata, name, author, display name |
| `\dist\main.js` | — | Electron main process (window title, menu) |
| `\dist\tray.js` | — | Tray icon setup code |
| `\dist\menu.js` | — | Application menu (About, Quit, etc.) |
| `\dist\loadingOverlay.js` | — | Loading/startup overlay |
| `\dist\updater.js` | — | Electron auto-updater |

## package.json (original)

```json
{
  "name": "antigravity",
  "productName": "Antigravity",
  "version": "2.0.6",
  "description": "Antigravity - Agentic Desktop Application",
  "homepage": "https://antigravity.google",
  "author": {
    "name": "Google",
    "email": "antigravity-support@google.com"
  },
  "main": "dist/main.js",
  "dependencies": {
    "chrome-devtools-mcp": "^0.23.0",
    "electron-log": "^5.4.3",
    "electron-updater": "^6.8.3",
    "shell-env": "^4.0.3"
  }
}
```

## Rebrand Steps

1. Extract: `asar extract app.asar ./app_extracted`
2. Replace `icon.png` with TCHUEKAM logo (512×512 PNG)
3. Replace `trayTemplate.png` (22×22) and `trayTemplate@2x.png` (44×44) with mini logo versions
4. Edit `package.json`:
   - `"name": "tchuekam-ui"`
   - `"productName": "TchuekamUI"`
   - `"author": {"name": "Giantect Empire", "email": "support@giantect.cm"}`
   - `"homepage": "https://giantect.cm"`
5. Check `dist/main.js` for hardcoded window title string
6. Check `dist/menu.js` for "About Antigravity" text
7. Repack: `asar pack ./app_extracted app.asar`
8. Kill running Antigravity, relaunch

## Google Antigravity CLI Path

```
C:\Users\CLINIC\.gemini\antigravity\bin\agentapi.bat
```

This bat file delegates to:
```
"C:\Users\CLINIC\AppData\Local\Programs\Antigravity\resources\bin\language_server.exe" agentapi
```

## Notes

- Electron auto-updater (`electron-updater`) will overwrite the rebranded asar on next update. Disable auto-updates or re-apply after each update.
- Sentry logging at `C:\Users\CLINIC\AppData\Roaming\AionUi\sentry\` — not Antigravity's, but if Antigravity has Sentry, consider disabling.
- The app's UI is served by the Electron renderer process, not remotely — so all local branding should be fully controllable.
