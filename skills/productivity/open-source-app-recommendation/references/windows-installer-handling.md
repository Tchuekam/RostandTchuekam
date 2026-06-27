# Windows Installer Handling Guide

## Overview
Installing open-source apps on Windows for a non-technical user. The user's machine uses winget (v1.28+) and manual .exe installers. Electron/Squirrel installers are common for open-source desktop apps and have quirks.

## Installer Types & Silent Flags

| Installer Type | Extension | Silent Flag | Works? | Notes |
|---|---|---|---|---|
| Squirrel (Electron) | .exe | `/S` | ❌ Often fails | Exit code 2 = silent not supported. Tell user to double-click. |
| Inno Setup | .exe | `/VERYSILENT /SUPPRESSMSGBOXES` | ✅ | Common for native Windows apps |
| NSIS | .exe | `/S` | ✅ | Common for simpler installers |
| MSI | .msi | `/quiet /qn` | ✅ | Use with msiexec |
| Microsoft Store | — | — | ✅ | Installed via winget automatically |

## Winget Workflow

1. **Search:** `winget search AppName`
2. **Install:** `winget install AppName`
3. **Check if actually installed:**
   ```bash
   winget list --query "AppName" 2>/dev/null
   which appname 2>/dev/null  # for CLI tools
   ls "C:\Users\$USER\AppData\Local\Programs\" | grep -i appname
   find /c/Users/$USER/AppData/Local -maxdepth 4 -iname "*appname*" -type d 2>/dev/null
   ```
4. **If registered but not installed:** winget downloads to `C:\Users\$USER\AppData\Local\<app>-updater\installer.exe`
   - The installer binary is downloaded, NOT run
   - Copy to D:\ (user's rule: no C: writes) then run manually:
   ```bash
   cp "/c/Users/$USER/AppData/Local/app-updater/installer.exe" /d/NewDownloadAgent/
   # Then user double-clicks, or try silent install from D:
   ```

## No-C Drive Rule
**CRITICAL:** Never write/install/save anything to C:. Check on C: is fine (reads allowed).
- All installers go to D:\NewDownloadAgent\
- All projects go to D:\ 
- All data/configs should avoid C: where possible

## When Silent Install Fails

1. Don't retry the same flag — it will fail again and frustrate the user
2. Try a different flag: `--msi`, `/quiet`, `-silent`
3. If all flags fail: copy installer to D:\, tell user to double-click
4. Verify installation after manual run with find/winget list

## Verification After Installation

```bash
# Find the installed app
find /c/Users/$USER/AppData/Local -maxdepth 4 -iname "*appname*" -type d 2>/dev/null
find "/c/Program Files" -maxdepth 2 -iname "*appname*" 2>/dev/null

# Check if it can be launched
tasklist 2>/dev/null | grep -i appname
ls "C:\Users\$USER\Desktop\*appname*" 2>/dev/null  # desktop shortcut
```

## Apps Installed in This Session

| App | Version | Installer Type | Silent Flag Result | Resolution |
|---|---|---|---|---|
| Obsidian | 1.12.7 | Squirrel/Electron | `/S` failed (exit 2) | Manual double-click needed |
| Logseq | 0.10.15 | Squirrel/Electron | `/S` failed | User ran manually |
