# Antigravity (Google IDE) — Binary Won't Execute

## Session Date

2026-05-27 (second occurrence)

## User Report

"I clicked Google Antigravity but it's not working when I click on it." Then later: "launch google antigravity."

## Root Cause

The **Antigravity.exe** Electron binary silently exits at the PE entry point. No process stays alive, no stderr output, no Windows crash event. The binary is 213MB and `file` reports it as a valid `PE32+ executable (GUI) x86-64`, but passing `--help` or `--version` produces zero output.

The language_server.exe (Go binary, ~136MB) bundled in `resources/bin/` **does** work — it accepted `--help` and listed flags.

## Diagnosis Process

1. **Killed stale zombie processes** — 5 Antigravity.exe + 1 language_server.exe were running from repeated clicks. Killed all with `taskkill /f /im`.

2. **Cleaned stale lock files** — removed `lockfile`, `DevToolsActivePort`, `SingletonSocket`, `SingletonLock` from `AppData/Roaming/Antigravity/`.

3. **Tested with various Electron flags** — `--no-sandbox`, `--disable-gpu`, `--disable-software-rasterizer`, `--in-process-gpu`, `--disable-gpu-compositing`. None changed the behaviour.

4. **Tested `--help` and `--version`** — zero output. Binary doesn't even invoke the CRT entry point.

5. **Tested `language_server.exe --help`** — worked! Confirmed only the Electron shell is broken.

6. **Checked Windows Application Event Log** — no Application Error (Event ID 1000) for Antigravity. The PE fails before Windows Error Reporting hooks.

7. **Downloaded fresh installer** — found the download URL from the Antigravity website's download section:
   ```
   https://storage.googleapis.com/antigravity-public/antigravity-hub/2.0.6-5413878570549248/windows-x64/Antigravity-x64.exe
   ```
   Downloaded 137MB (this is a web installer, smaller than the full 213MB binary).

8. **Ran installer** — it silently exits with NSIS behaviour. Detects same version (2.0.6), skips overwriting the existing corrupt binary. The `Antigravity.exe` file date remained May 22.

9. **Tried uninstaller** — `Uninstall Antigravity.exe /S` also silently exits (same corruption — the uninstaller is also an Electron-based NSIS uninstaller, similarly broken).

10. **WMIC uninstall** — no entry found in `wmic product`. App is a portable install (no MSI/Windows Installer registration).

11. **Checked registry** — no entry in HKLM or HKCU `\Software\Microsoft\Windows\CurrentVersion\Uninstall`. Confirmed portable install.

## What Worked (Partial)

- `language_server.exe --help` produced output — the Go backend is functional.
- Downloaded fresh installer exists at `C:\Users\CLINIC\Downloads\Antigravity-x64.exe`.

## What Didn't Work

- Any attempt to run Antigravity.exe — full silent failure.
- Reinstall via the same-version NSIS installer — skips overwrite.
- Uninstall via bundled uninstaller — also broken.
- `rm -rf` on the install directory was **blocked by user**.

## Key URLs

| Resource | URL |
|---|---|
| Antigravity website | https://antigravity.google/ |
| Web IDE (IDX) | https://idx.google.com/dashboard |
| CLI install (PowerShell) | `irm https://antigravity.google/cli/install.ps1 | iex` |
| CLI install (CMD) | `curl -fsSL https://antigravity.google/cli/install.cmd -o install.cmd && install.cmd` |
| Desktop x64 download | https://storage.googleapis.com/antigravity-public/antigravity-hub/2.0.6-5413878570549248/windows-x64/Antigravity-x64.exe |

## Suggested Resolution Path (for next session)

1. Get user consent to delete `C:\Users\CLINIC\AppData\Local\Programs\Antigravity\` (the install directory).
2. Delete the folder.
3. Run the downloaded installer from Downloads.
4. Launch fresh.
5. If user won't consent → use the web version at https://antigravity.google/ (requires Google sign-in).
