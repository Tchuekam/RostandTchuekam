# PC Slow — Identify Hog & Remove App (LM Studio)

## Session Date

2026-05-27

## User Report

"My computer is a little slow. If it's because of LM Studio, delete the app and all related files."

## Diagnosis Pipeline

### 1. Identify Top RAM Consumers

```powershell
Get-Process | Sort-Object WorkingSet64 -Descending |
    Select-Object -First 20 Name,
        @{N='MB';E={[math]::Round($_.WorkingSet64/1MB,1)}},
        CPU, StartTime | Format-Table -AutoSize
```

Also check private memory (the real allocation, not just working set):

```powershell
Get-Process 'LM Studio' | Select-Object Id, ProcessName,
    @{N='MB';E={[math]::Round($_.WorkingSet64/1MB,1)}},
    @{N='PrivateMB';E={[math]::Round($_.PrivateMemorySize64/1MB,1)}}
```

### 2. Get User Confirmation Before Deleting

Present the findings clearly. Let the user decide. This builds trust.

### 3. Kill the Process

```powershell
Get-Process 'LM Studio' -ErrorAction SilentlyContinue | Stop-Process -Force
```

### 4. Find Install Location

Check multiple places:

| Location | Command |
|---|---|
| Registry (system-wide) | `Get-ItemProperty 'HKLM:\SOFTWARE\...\Uninstall\*'` |
| Registry (current user) | `Get-ItemProperty 'HKCU:\SOFTWARE\...\Uninstall\*'` |
| Program Files | `C:\Program Files\<App>\` |
| AppData Local | `C:\Users\<user>\AppData\Local\<App>\` |
| AppData Roaming | `C:\Users\<user>\AppData\Roaming\<App>\` |
| User home hidden | `C:\Users\<user>\.<app>\` (stores models, configs, conversations) |

The registry shows the uninstaller path:

```powershell
Get-ItemProperty 'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*' |
    Where-Object { $_.DisplayName -like '*LM Studio*' } |
    Select-Object DisplayName, InstallLocation, UninstallString
```

### 5. Run Official Uninstaller First

```powershell
Start-Process -FilePath '<Uninstall LM Studio.exe>' -ArgumentList '/currentuser /S' -Wait -NoNewWindow
```

### 6. Wipe Residual Directories

After the uninstaller runs, manually delete what's left:

```powershell
Remove-Item -Path '<InstallFolder>' -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path 'C:\Users\<user>\.<app>' -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path 'C:\Users\<user>\AppData\Roaming\<App>' -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path 'C:\Users\<user>\AppData\Local\<App>' -Recurse -Force -ErrorAction SilentlyContinue
```

### 7. Clean Shortcuts

```powershell
Get-ChildItem -Path 'C:\Users\<user>\Desktop', 'C:\Users\<user>\AppData\Roaming\Microsoft\Windows\Start Menu' `
    -Recurse -Filter '*LM Studio*' -ErrorAction SilentlyContinue | Remove-Item -Force
```

### 8. Verify Deletion

```powershell
Test-Path 'C:\Users\<user>\.<app>'   # Should return False
```

Also verify by checking process list.

### 9. Confirm RAM Improvement

```powershell
$os = Get-CimInstance Win32_OperatingSystem
'Free RAM: ' + [math]::Round($os.FreePhysicalMemory/1MB, 1) + ' GB / ' + [math]::Round($os.TotalVisibleMemorySize/1MB, 1) + ' GB'
```

## Key Data Points from This Session

| Metric | Before | After |
|---|---|---|
| Top RAM consumer | LM Studio (5.4 GB private) | Chrome (503 MB) |
| Free RAM | Nearly full | 2 GB / 7.9 GB |
| LM Studio disk usage | 5.4 GB (models + app) | 0 |
| LM Studio install | `D:\DATASAVE\LMstudio\LM Studio\` | Deleted |
| LM Studio models | `C:\Users\CLINIC\.lmstudio\models\` (3.2 GB) | Deleted |
| LM Studio cache | `C:\Users\CLINIC\AppData\Roaming\LM Studio\` | Deleted |

## Pitfalls

- **No registry entry under HKLM** — some per-user installs only appear in HKCU.
- **Model files are huge** — LM Studio downloads GGUF models (3+ GB) to `~/.lmstudio/models/`. The uninstaller often leaves these behind. Always delete `~/.lmstudio/` manually.
- **Multiple processes** — LM Studio spawns several sub-processes (backend, UI, language server). Kill them ALL before uninstalling.
- **Uninstaller switches vary** — LM Studio's uninstaller needed `/currentuser /S` for silent mode. Not all apps use the same flags.
- **Always measure before/after** — proving the free RAM improved gives the user confidence the removal was worth it.
