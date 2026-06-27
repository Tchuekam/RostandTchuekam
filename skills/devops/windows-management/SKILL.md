---
name: windows-management
title: Windows System Management and Troubleshooting
description: Comprehensive skill for managing Windows systems, including agent deployment, application troubleshooting, file organization, and performance optimization.
category: devops
tags:
  - windows
  - system-management
  - troubleshooting
  - deployment
  - file-organization
  - performance
---

# Windows System Management and Troubleshooting

This skill provides a consolidated framework for various Windows system management tasks, from deploying autonomous agents to troubleshooting application issues, organizing files, and optimizing system performance.

## 1. Windows Agent Deployment

This section covers the end-to-end process of packaging, securing, and deploying autonomous AI agents on Windows environments.

### Deployment Pipeline

### 1.1 Security & Hardening
- **Obfuscation:** Use `PyInstaller` with `--key` (AES encryption) to obscure Python bytecode.
- **Credential Protection:** Store sensitive API keys in the Windows Credential Manager API, not `.env` files.
- **Policy Engine:** Integrate `tirith` or Pydantic-based guardrails into the agent's core loop to prevent unauthorized tool use.
- **Code Signing:** Use `signtool` for production binaries.

### 1.2 Telemetry & Activation (The "Phone Home" Protocol)
- **Identity:** Use WMI (`Win32_BaseBoard.SerialNumber`) for stable machine-ID generation.
- **Activation:** Implement a bootstrap shim (`bootstrap.py`) that performs a handshake with a licensing server (JWT-based) before spawning the agent.
- **Analytics:** Integrate `posthog` for usage tracking (captures: `app_installed`, `version`, `os`).

### 1.3 Packaging & Distribution
- **Requirements:** Bundle all dependencies (`flask`, `pyjwt`, `requests`, `wmi`, `posthog`, `hermes-agent`) into a `requirements.txt`.
- **Packaging:** Use `PyInstaller` (`--onefile`) to create a standalone `.exe`.
- **Installation:** Use `Inno Setup` for the final Windows installer package.

### Pitfalls (Agent Deployment)
- **WMI Permissions:** Accessing hardware identifiers may require specific execution contexts.
- **Dependency Bloat:** Minimize bundled packages to keep the `.exe` size manageable.
- **Startup Latency:** Licensing checks add delay. Use async requests if the agent loop initialization allows it.

## 2. Windows Application Troubleshooting

This section details a diagnosis pipeline for when Windows applications fail to open or crash silently.

### When to Use

User reports: "I clicked the icon but nothing happens" / "app won't open" / "it's not starting" / "I double-clicked many times, nothing appears."

This covers:
- Desktop shortcuts that appear to do nothing
- Apps that launch in Task Manager but no window shows
- Apps that crash silently (no error dialog)
- Electron apps that fail due to network/DNS dependency

### Pipeline (ordered — run these steps in sequence, stop when you find root cause)

#### Step 1: Locate the Shortcut

Use `tchuekam_index_search(query="appname")` first (sub-50ms).

If no index result, check the Desktop with:
```bash
ls -la /c/Users/CLINIC/Desktop/ | grep -i <appname>
```

#### Step 2: Read the Shortcut Target

Desktop icons are `.lnk` files. Use PowerShell's COM object to read them:

```powershell
powershell -Command "\$shell = New-Object -ComObject WScript.Shell;\$shortcut = \$shell.CreateShortcut(\'C:\\Users\\CLINIC\\Desktop\\<AppName>.lnk\');Write-Output \\\"Target: \\$(\\$shortcut.TargetPath)\\\";Write-Output \\\"Args: \\$(\\$shortcut.Arguments)\\\";Write-Output \\\"WorkDir: \\$(\\$shortcut.WorkingDirectory)\\\""
```

This tells you:
- The actual `.exe` path
- Working directory
- Any command-line arguments

#### Step 3: Verify the Executable Exists

```bash
ls -la "/c/Users/CLINIC/AppData/Local/Programs/<AppName>/"
```

If the folder/file is missing → app was uninstalled or the shortcut is orphaned.
If it exists → check the file size (0 bytes = corrupt).

#### Step 4: Detect App Type (optional but useful)

Look for signature files in the install directory:
- `chrome_100_percent.pak`, `icudtl.dat`, `v8_context_snapshot.bin` → **Electron app**
  - Electron apps are essentially Chromium browsers. They often fail silently on network errors.
- `.class` files or `lib/` with jar files → Java app (needs JRE)
- UWP-style folder names (e.g. `Microsoft.SomeApp`) → Store app

#### Step 5: Kill Stale Processes and Launch Fresh

```powershell
powershell -Command "Get-Process <AppName> -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue"
```

Then launch a fresh instance:
```powershell
powershell -Command "Start-Process -FilePath '<full exe path>' -WindowStyle Normal"
```

#### Step 6: Check for Window

```powershell
Start-Sleep 8
Get-Process <AppName> | Format-Table Id, ProcessName, MainWindowTitle, Responding -AutoSize
```

- **MainWindowTitle is empty** → process is running but window is hidden, off-screen, or crashed before rendering.
- **Multiple <AppName> processes** → user double-clicked many times. Stale zombies accumulating.
- **No process** → exe crashes immediately (corrupt binary, missing DLL).

#### Step 7: Bring Hidden Window to Front (if processes exist with no visible window)

```powershell
Add-Type @'
using System;
using System.Runtime.InteropServices;
public class Win32 {
    [DllImport("user32.dll")]
    public static extern bool ShowWindowAsync(IntPtr hWnd, int nCmdShow);
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
}
'@;
[Win32]::ShowWindowAsync($pid_handle, 1);
[Win32]::SetForegroundWindow($pid_handle)
```

#### Step 8: Read App Logs (electron apps)

Electron stores logs at:
```bash
~/AppData/Roaming/<AppName>/logs/
```

- `main.log` — main process logs (auto-updater, app lifecycle)
- `language_server.log` — plugins/extensions (common crash source)

Look for these patterns:

| Log Pattern | Meaning |
|---|---|
| `ERR_INTERNET_DISCONNECTED` | No network. App is cloud-dependent (IDX, Gemini, etc.) |
| `ERR_NAME_NOT_RESOLVED` | DNS failure. Can't reach auth/API servers. |
| `ERR_NETWORK_IO_SUSPENDED` | Machine was in sleep/hibernate, network stack not restored. |
| `dial tcp: lookup X: no such host` | DNS can't resolve. Google APIs are common for cloud tools. |
| `Failed to get OAuth token` | Authentication failed — often because network was down at startup. |

#### Step 8.5: Binary Won't Execute — Zero-Process Case

When you call `Get-Process <AppName>` after launch and get **nothing** (no process at all), the executable failed to load at the OS level. This is different from a crash — the PE loader itself rejected the binary.

**Diagnosis signs:**
- `ProcessName` column in `Get-Process` is completely absent after launch
- No window, no error dialog, no crash event in Windows Application log
- `stderr` redirection produces zero output (empty file)
- `file` command shows `PE32+ executable` but the binary silently exits with code 0
- The app's own log files don't update (the process died before any logger initialised)

##### Sub-step 8.5a: Verify PE Loadability

Check if the binary even responds to `--help` or `--version`:
```bash
cmd.exe /c ""<full_exe_path> --version""
```
If zero output → the CRT entry point doesn't fire. Three likely causes:

1. **Missing Visual C++ redistributable** — Electron apps bundle `d3dcompiler_47.dll`, `vulkan-1.dll`, etc., but depend on system `VCRUNTIME140.dll`. Check with:
   ```bash
   cmd.exe /c "where vcruntime140.dll"
   ```
2. **Corrupted binary** — the PE header or first section is damaged. Check file size vs. original (compare with the installer's expected size or a fresh download).
3. **Kernel-locked file** — `app.asar` (Electron) or other resources held by the Windows file system cache, Windows Search Indexer, or Windows Defender real-time scanning. `rm -f` returns "Device or resource busy" even after killing all user processes. This requires a reboot or an `rmdir` from a different boot session.

##### Sub-step 8.5b: Attempt Fresh Download + Reinstall

If the binary is confirmed corrupt (won't execute, correct size but no output):

1. **Find the download URL** for the same version from the vendor's website (the installed version is often shown in logs or `app-update.yml`).
2. **Download manually** with `curl -L -o` to a known location.
3. **Verify size** — if the fresh download is significantly smaller (e.g. 137MB vs 213MB), it may be a web installer, not the full binary.
4. **Run the installer** — some installers are NSIS-based and silently skip overwriting when the same version is detected. In that case, the old corrupt binary remains. The fix requires removing the install directory first (but ask the user before deleting).
5. **Check for blocking processes** — a stale `lockfile` or `SingletonLock` in the app's `AppData/Roaming` directory can prevent the Electron shell from starting. Remove stale lock files:
   ```bash
   rm -f "<AppData>/lockfile" "<AppData>/SingletonSocket" "<AppData>/SingletonLock"
   ```

##### Sub-step 8.5c: Electron App — Verify .asar Integrity

Electron apps pack their JS code in `resources/app.asar`. If the asar is truncated:
```bash
ls -la "<install_dir>/resources/app.asar"
```
If it's 0 bytes or suspiciously small, the renderer process will start but exit immediately. Check by extracting:
```bash
npx asar extract "<install_dir>/resources/app.asar" /tmp/check
ls /tmp/check/package.json   # Should have "main": "dist/main.js"
```

##### Sub-step 8.5d: Fallback — Use the Web / CLI Version

If the desktop IDE binary won't run and reinstall isn't possible (user blocked deletion, same-version installer skips overwrite):

1. Check if the app has a **web version** — open the vendor's domain in a browser.
2. Check if it has a **CLI tool** — install via their install script (PowerShell/CMD) or download the binary directly from the vendor's manifest API.
3. Check if a **language server / backend** bundled with the app can start independently (some Electron apps ship a standalone Go/C++ backend that runs fine without the GUI).

##### Sub-step 8.5e: NSIS Installer Also Fails

When the NSIS installer itself can't execute, the problem is at the Windows subsystem level — the installer's embedded NSIS engine can't decompress. This manifests as:
- The installer exits silently (exit code 0) with zero files written
- The target folder may get a partial `resources/` skeleton created but no actual files
- `file` shows "Nullsoft Installer self-extracting archive" but the binary doesn't start

**Workarounds:**
1. Use `7z x` or other archiver to extract the NSIS installer data manually.
2. Try the `_?=<targetdir>` NSIS switch with `/NCRC` to disable CRC check: `installer.exe /NCRC /S _?=C:\\Path`
3. Install the app's **CLI** binary instead (often distributed as a separate Go/Rust binary that doesn't need NSIS).
4. Use the **web version** in a browser.

### Pitfalls (Application Troubleshooting)

- **Ping with `-c` flag requires admin** on Windows. Use `Test-Connection -Count 1 -Quiet` in PowerShell instead.
- **Stale zombie processes** accumulate when user clicks the icon rapidly. Kill them ALL before retrying.
- **Electron apps don't show error dialogs** — they fail silently in logs. Always check `main.log`.
- **Multiple process instances** after clicking repeatedly: the app may be running already but hidden behind other windows or off-screen.
- **COM Object for .lnk reading only works on actual shortcuts**, not UWP app tiles or pinned Taskbar shortcuts.
- **Kernel-locked files** — `app.asar` in Electron apps can be locked by the Windows file system cache, not by a user process. `rm -f` returns "Device or resource busy" even with zero matching processes. Neither `taskkill`, `Stop-Process -Force`, nor `Remove-Item -Force` will unlock it. The fix is a **reboot**, or booting into Safe Mode to delete.
- **NSIS installer skips same-version** — when the installed version matches the installer's version, NSIS silently exits without replacing any files. The corrupt binary survives. Must delete install directory first (requires reboot if kernel-locked) or use the `_?=` switch (which doesn't always work).
- **NSIS installer silently fails** — the NSIS decompression engine itself may not work on a machine with PE loading issues. `file` shows the installer as a valid NSIS archive but running it produces zero effect. Try extracting with `7z x` or using a different deployment method (CLI, web, portable ZIP).
- **No registry entry ≠ app not present** — some apps install portably (no MSI, no Windows Installer registration). `wmic product` won't find them. Check `AppData\\Local\\Programs\\<AppName>\\` directly.
- **Uninstall.exe is also an Electron binary** — if the main app's binary is corrupt, the bundled `Uninstall <AppName>.exe` likely shares the same Electron shell and is also broken. Don't rely on it.

## 3. Windows File Organization and Disk Management

This section covers organizing chaotic folders into categorized subdirectories and managing disk space, including external drive migration.

### Workflow (File Organization)

#### 3.1 Scan — List all items

Use `terminal` with `ls -la` on Windows git-bash:

```bash
ls -la "/c/Users/$USER/Desktop"
```

For Downloads/Documents:

```bash
ls -la "/c/Users/$USER/Downloads"
ls -la "/c/Users/$USER/Documents"
```

**Note**: In git-bash on Windows, use `/c/Users/CLINIC/...` paths (MSYS-style), not `C:\\...`.

#### 3.2 Classify each item into categories

Standard category scheme (adapt per user):

| # | Category | Contents |
|---|---|---|
| 01-DOCUMENTS | .docx, .xlsx, .txt, .pdf — general documents |
| 02-PROJECTS-TCHUEKAM | Anything related to TCHUEKAM, marketing, branding, product |
| 03-MARKETING-COM | Marketing collateral, logos, chatbots research |
| 04-SCRIPTS-CODE | .js, .py, .sh, .bat, code files |
| 05-BUSINESS-CLIENTS | Client folders, business partner documents |
| 06-RACCOURCIS | .lnk files (shortcuts) |
| 07-DOWNLOADS-ARCHIVES | Downloads, .zip, .rar archives |
| 08-WEB-RESEARCH | Bookmarks, research notes, saved articles |

**Preserve existing folders** — don't move them. Only reorganize loose files.

#### 3.3 Create category directories

```bash
cd "/c/Users/CLINIC/Desktop"
mkdir -p "01-DOCUMENTS" "02-PROJECTS-TCHUEKAM" "03-MARKETING-COM" \
         "04-SCRIPTS-CODE" "05-BUSINESS-CLIENTS" "06-RACCOURCIS" \
         "07-DOWNLOADS-ARCHIVES" "08-WEB-RESEARCH"
```

#### 3.4 Move files into categories

Use `mv` with numbered prefixes. Files that fail to move (locked/open) leave a clear note.

```bash
mv "SomeFile.docx" "01-DOCUMENTS/"
mv "project-file.js" "04-SCRIPTS-CODE/"
```

#### 3.5 Handle locked files gracefully

- **`~$` (tilde-dollar) files** = temporary Office lock files. They disappear when the user closes the app. Don't fight them.
- **Files open in an editor** (Word, VS Code) = cannot be moved. Tell the user to close the app and offer to retry.
- **Leave `desktop.ini` alone** — Windows system file.

#### 3.6 Report — deliver a structured summary

Give the user:

1. **What was created**: table of folders with contents
2. **What didn't move**: which files and why
3. **Observations**: patterns you noticed (many marketing files, heavy images, duplicate files, working style insights)

#### 3.7 Duplicate scan — lightweight approach

When the user asks for duplicate cleanup AFTER the initial organization:

1. **Do NOT scan full Desktop recursively** — the `wacrm/node_modules` directory alone can cause a 300s+ timeout.
2. **Exclude heavy directories upfront**: `node_modules/`, `.git/`, `HOMEAPPS/`, `MYFOLDER/`, `LuckyTechHub-Bot-main/` — they rarely produce actionable user-facing duplicates.
3. **Use `md5sum`** (available in git-bash) with `sort | uniq -d`:
   ```bash
   find . -type f -not -name 'desktop.ini' -not -name '~$*' \
     -not -path './*/node_modules/*' -not -path './*/.git/*' \
     -size +1k -exec md5sum {} \; 2>/dev/null | sort > /tmp/scan.txt
   awk '{print $1}' /tmp/scan.txt | sort | uniq -d
   ```
4. **If the scan takes >30s, delegate it** — the user will get impatient. Use `delegate_task` with a subagent that has `terminal`+`file` toolsets.
5. **Report clearly**: "No duplicates found" or list the duplicate files with paths and sizes.
6. **Never delete duplicates without user confirmation** — some "duplicates" may be intentional (e.g., same file organized in two categories).

#### 3.8 Save the category scheme to memory

Record the folder structure and any user-specific preferences (e.g., "don't touch MYFOLDER") to memory so future sessions know the layout.

### Disk Space Analysis & External Drive Migration

When the user's C: drive is critically full (90%+) and they want to move data to an external drive (H:, etc.), follow this diagnostic-first workflow.

#### Trigger Tokens
User says: "make space", "C: is full", "move to H:", "free up space", "what can I move", "storage is full".

#### 3.9 Check drive status first

```bash
df -h /c/ /h/ /d/
```

Note: the 99% full C: causes `du -sh` on any large folder to time out (30-60s+). Do NOT rely on `du -sh` for the initial scan — use alternative fast probes.

#### 3.10 Fast-diagnose top space consumers (when du is too slow)

When standard `du` commands time out on a choked disk, use these lightweight probes instead:

| Probe | Command | What it finds |
|---|---|---|
| Check node_modules | `ls /c/Users/$USER/node_modules/ 2>/dev/null \| wc -l` | How many packages (each may be GBs) |
| Check Temp | `ls /c/Users/$USER/AppData/Local/Temp/ 2>/dev_null \| wc -l` | Temp files count |
| Check caches | Check if `.cache/`, `.cargo/`, `.bun/`, `.codex/`, `.gemini/` exist under `$HOME` | Large tool caches |
| Check Windows Temp | `ls /c/Windows/Temp/ 2>/dev/null \| wc -l` | System temp |
| Check big user dirs | Try `du -sh` on Desktop, Downloads, Documents, Videos, Pictures individually with 30s timeout | Identify which user folder is heavy |

#### 3.11 Prioritize what to move

**TIER 1 — Safe to move to H: (no side effects):**
- Desktop personal files (not shortcuts to installed programs)
- Downloads full of installers, ISOs, zips
- Videos, large Pictures, Music folders
- Old project folders you cloned but don't actively use
- OneDrive (if you don't need offline sync of everything)

**TIER 2 — Safe to MOVE but need path configuration after:**
- `node_modules/` (can be moved but npm/pnpm need `--prefix` or symlink)
- `.cargo/` (can set CARGO_HOME to H:)
- `.bun/` (can set BUN_INSTALL to H:)
- `.cache/` (various caches — npx, pip, etc.)

**TIER 3 — Cleanup instead of move (delete):**
- `C:\\Windows\\Temp\\` — safe to delete everything inside
- `C:\\Users\\$USER\\AppData\\Local\\Temp\\` — safe to delete everything inside
- Browser caches (can be cleaned via browser settings)
- `C:\\hiberfil.sys` — if user doesn't use hibernate: `powercfg -h off` (frees RAM-size GBs)

#### 3.12 For each tier, say the expected space gain

Don't just list folders — estimate. User needs to know: "moving videos saves ~5GB", "cleaning Temp saves ~1GB".

#### 3.13 Check external drive capacity

Before recommending moves, check: `df -h /h/` or `ls /h/` to see what's already on H:. Don't suggest overwriting existing folders (apps/, down/, WEBAPPS/, etc.).

#### 3.14 Execute moves

Use `mv` for simple files/folders:
```bash
mv "/c/Users/CLINIC/Videos" "/h/Videos"
```

For Tier 2 items that need path reconfiguration, explain the env var change. Don't do it automatically — ask the user if they want to proceed.

#### 3.15 Report

Give a clean table:
| Action | Item | Est. Space Freed |
|---|---|---|
| MOVE to H: | Videos/ | ~5 GB |
| MOVE to H: | Downloads/ | ~3 GB |
| DELETE | Windows Temp | ~500 MB |
| TOTAL | | ~8.5 GB |

### Pitfalls (File Organization & Disk Management)

- **~$ files**: These are Office temp/lock files. They look like duplicates (e.g. `~$ocument.docx`). **Do not try to move or delete them** — they are created by Word while a document is open and vanish on their own.
- **git-bash path syntax**: Use `/c/Users/CLINIC/...` not `C:\\\\Users\\\\CLINIC\\\\...` in terminal commands.
- **.lnk files are NOT the actual programs**: They are shortcuts. Collect them in a RACCOURCIS folder, don't delete them.
- **User may have many .docx open simultaneously** — check for locked files by attempting the mv; if it fails, note it and move on.
- **Don't delete anything unless asked** — the user may want files you consider clutter.
- **Use `mv` (not `cp`)** — moving is faster and doesn't leave originals.
- **Prefix category folders with numbers** (01-, 02-) so they sort in a logical order in Windows File Explorer.
- **Always ask for exclusions before mass moves**: Before executing a bulk data migration, list the items you plan to move and ask the user: "What should I NOT touch?" Users have specific folders (raccourcis, home shortcuts, active bots, CRM projects) they want kept on C:. Move first, ask later = frustration and manual recovery.
- **Inter-device `mv` is actually copy+delete**: Moving from C: to H: (different physical drives) means Windows copies then deletes. It's slow and can fail with "Directory not empty" when the target has a folder with the same name. To handle this: (a) list target dir on H: first and check for conflicts, (b) rename source or target to avoid collisions (e.g. `WEBAPPS_DESKTOP`), (c) expect timeouts on folders >1GB and use background processes or robocopy instead.
- **Locked executables in Downloads**: A running `.exe` installer file in Downloads cannot be moved until the process exits. Check with `handle.exe` or just note the locked file and move on — retry after reboot.
- **Heavy folders cause 120s+ timeout**: Videos/, Pictures/, node_modules/ are common culprits. Break the migration into batches: move smaller folders first, then tackle heavy ones one at a time with background terminal + notify_on_complete. Never run concurrent heavy mv commands — they saturate the disk and freeze the terminal.
