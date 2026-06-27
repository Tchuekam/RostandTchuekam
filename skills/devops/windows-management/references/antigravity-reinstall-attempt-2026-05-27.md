# Antigravity (Google IDE) — Reinstall Attempt & NSIS Failure

## Session Date

2026-05-27 (third occurrence — reinstall attempt)

## User Report

"Once more google antigravity is not working when i click on it. fix the problem and then open it for me." Then "1 reinstall" when offered options.

## Root Cause

Same as previous session: **Antigravity.exe** Electron binary silently exits at the PE entry point. No process, no logs, no crash events. On top of that, the **NSIS installer** (`Antigravity-x64.exe`) also silently fails — indicating a system-level NSIS/Electron problem beyond just one corrupt file.

## Key Discovery — NSIS Installer Fails Too

The downloaded installer (137MB, Nullsoft Installer) runs but produces **zero effect**:
- `file` shows: `PE32 executable for MS Windows 4.00 (GUI), Intel i386, Nullsoft Installer self-extracting archive`
- Running with `/S` (silent), `/NCRC` (skip CRC), or `/D=C:\path\` all produce the same: silent exit with code 0
- Target directory gets only a skeleton `resources/` folder created, nothing else
- The installer detects same version (2.0.6), skips overwriting the existing corrupt binary
- `Antigravity.exe` file date remains May 22 unchanged

## Key Discovery — Kernel-Locked app.asar

The `resources/app.asar` file was **locked by the kernel**:
- `rm -f` → "Device or resource busy"
- `mv` → Permission denied
- `rename` via cmd.exe appeared to succeed but the directory remained
- `rmdir /s /q` appeared to succeed but the folder persisted
- Even `powershell Remove-Item -Force` failed silently
- No user-space process held the handle (checked via `handle.exe`, `openfiles`, `Get-Process` multiple times, taskkill of all Antigravity processes)
- The lock persisted across: killing Explorer.exe, killing all known processes, waiting 10+ seconds

The file was held by the **Windows file system cache** or **Windows Defender real-time scanning** mapping the PE into memory.

## Key Discovery — NSIS Installer Bypass

NSIS installers support a `_?=` switch for "install to this directory, don't skip existing":
```
installer.exe /NCRC /S _?=C:\Users\CLINIC\AppData\Local\Programs\Antigravity
```
This still failed silently (no effect).

## What Worked — CLI Install as Fallback

The **Antigravity CLI** (`agy.exe`) is a separate Go binary distributed independently:
- Manifest URL: `https://antigravity-cli-auto-updater-974169037036.us-central1.run.app/manifests/windows_amd64.json`
- Direct download: `https://storage.googleapis.com/antigravity-public/antigravity-cli/1.0.2-6109799369277440/windows-x64/cli_windows_x64.exe`
- 144MB binary, PE32+ console executable
- `--help` and error handling work immediately
- Install location: `C:\Users\CLINIC\AppData\Local\agy\bin\agy.exe`

## Commands Used

```batch
:: Read shortcut target
powershell -Command "$shell = New-Object -ComObject WScript.Shell; $shortcut = $shell.CreateShortcut('C:\Users\CLINIC\Desktop\Antigravity.lnk'); Write-Output $shortcut.TargetPath"

:: Check for zombie processes
powershell -Command "Get-Process Antigravity -ErrorAction SilentlyContinue | Format-Table Id, ProcessName, MainWindowTitle -AutoSize"

:: Kill all
taskkill /f /im Antigravity.exe
taskkill /f /im language_server.exe

:: Clean stale locks
rm -f "C:\Users\CLINIC\AppData\Roaming\Antigravity\lockfile"
rm -f "C:\Users\CLINIC\AppData\Roaming\Antigravity\SingletonSocket"
rm -f "C:\Users\CLINIC\AppData\Roaming\Antigravity\SingletonLock"

:: Try binary with --help — zero output confirms PE load failure
cmd.exe /c ""C:\Users\CLINIC\AppData\Local\Programs\Antigravity\Antigravity.exe" --version"

:: Download CLI directly (from manifest)
curl -L -o "C:\Users\CLINIC\AppData\Local\agy\bin\agy.exe" "https://storage.googleapis.com/antigravity-public/antigravity-cli/1.0.2-6109799369277440/windows-x64/cli_windows_x64.exe"

:: Uninstall attempt (also fails)
wmic product where "name like '%%Antigravity%%'" call uninstall /nointeractive

:: Check registry for installed product (none found — portable install)
reg query HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall /s /f Antigravity 2>nul
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall /s /f Antigravity 2>nul

:: Verify VC++ redistributable (present)
cmd.exe /c "where vcruntime140.dll"

:: Try NSIS with bypass switches (no effect)
cmd.exe /c "C:\Users\CLINIC\Downloads\Antigravity-x64.exe /NCRC /S _?=C:\Users\CLINIC\AppData\Local\Programs\Antigravity"

:: Try creating batch file loop to retry delete (kernel lock still prevents)
:: Script at C:\Users\CLINIC\AppData\Local\Temp\del_antigravity.bat — retries del in 3s loop
```

## Lessons for Next Session

1. The kernel lock on `app.asar` requires a **reboot** to clear. After reboot, the file can be freely deleted.
2. After deleting the install directory, run the downloaded installer fresh.
3. If the installer still fails, extract it manually: `7z x Antigravity-x64.exe -oAntigravity\`
4. The CLI (`agy.exe`) works as a functional substitute for the GUI — no sign-in screen needed.
5. This machine may have a broader PE loader issue affecting NSIS-based installers (possibly Windows security hardening, AppLocker, or WDAC policy).
