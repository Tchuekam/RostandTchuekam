# Windows C: Drive Disk Scan Technique

**Problem:** When C: is 98% full (2.2 GB free / 106 GB total), standard tools like `du -sh` time out because of the sheer number of files.

**Solution:** Use a targeted PowerShell script instead of recursive `du`.

## Method: Targeted PowerShell via .ps1 File

1. Write a `.ps1` file to D:\ (never C:)
2. Call it with `powershell -NoProfile -ExecutionPolicy Bypass -File D:/path/to/script.ps1`

### Script Template

```powershell
$base = "$env:LOCALAPPDATA"
$folders = @(
    'Temp', 'npm-cache', 'pnpm-cache', 'pip', 'Package Cache',
    'SquirrelTemp', 'Google', 'Adobe', 'CapCut', 'Docker',
    'Android', 'Yarn', 'pnpm', 'Mozilla', 'Opera Software',
    'GitHubDesktop', 'WSL', 'ms-playwright', 'node-gyp',
    'Bytedance', 'Wondershare', 'Intel', 'claude-cli-nodejs'
)

foreach ($f in $folders) {
    $path = Join-Path $base $f
    if (Test-Path $path) {
        try {
            $size = (Get-ChildItem $path -Recurse -ErrorAction Stop | Measure-Object Length -Sum).Sum
            $mb = [math]::Round($size / 1MB, 1)
            if ($mb -gt 10) { Write-Output "$mb`t$f" }
        } catch { Write-Output "ERR`t$f" }
    }
}
```

### Why This Works

- **Write to .ps1 file first** — avoids bash-git quote escaping issues with inline PowerShell
- **Target known space hogs** — ~30 specific AppData folders vs full recursive scan
- **Skip silent folders** — don't scan 2000+ Temp files, just sum them
- **10 MB threshold** — filters noise; only report folders > 10 MB

## Cleanup Strategy for 98% Full Drive

| Folder | Typical Size | Safe to Delete? | Notes |
|--------|-------------|-----------------|-------|
| `Temp` | 1.5-2 GB | ✅ Yes | Windows temp files |
| `SquirrelTemp` | 500-600 MB | ✅ Yes | Electron installer temp |
| `npm-cache` | 1.5-2 GB | ✅ Yes | Rebuilds on next npm install |
| `pip` | 50-100 MB | ✅ Yes | Rebuilds on next pip install |
| `Package Cache` | 20-30 MB | ✅ Yes | Old installers |

**Total typically recoverable: 3.5-4.5 GB**

### C: Drive Rule

**Never write/install/save anything to C:.** Move installer.exe from C:\Users\%USER%\AppData\Local\<app>-updater\ to D:\NewDownloadAgent\ before running. If the file is locked (process still running), use `cp` instead of `mv`.
