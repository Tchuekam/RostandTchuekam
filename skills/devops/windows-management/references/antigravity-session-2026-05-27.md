# Antigravity (Google Cloud Code / IDX) — Won't Open Diagnosis

## Session Date

2026-05-27

## User Report

"I clicked Antigravity many times on the Desktop but it doesn't open."

## Root Cause

Antigravity is a Google Cloud Code Electron app that requires internet connectivity at startup for:
- OAuth token acquisition (`oauth2.googleapis.com`)
- Model/service discovery (`daily-cloudcode-pa.googleapis.com`)
- Telemetry (`play.googleapis.com`)

The user's internet was down / DNS was failing (`ERR_INTERNET_DISCONNECTED`, `ERR_NAME_NOT_RESOLVED`). The app processes started but no window appeared because it couldn't authenticate.

## Files Involved

| Item | Path |
|---|---|
| Shortcut | `C:\Users\CLINIC\Desktop\Antigravity.lnk` |
| Executable | `C:\Users\CLINIC\AppData\Local\Programs\Antigravity\Antigravity.exe` |
| App Data | `C:\Users\CLINIC\AppData\Roaming\Antigravity\` |
| Main log | `C:\Users\CLINIC\AppData\Roaming\Antigravity\logs\main.log` |
| Language server log | `C:\Users\CLINIC\AppData\Roaming\Antigravity\logs\language_server.log` |

## Key Commands Used

```powershell
# Read shortcut target
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut('C:\Users\CLINIC\Desktop\Antigravity.lnk')
Write-Output "Target: $($shortcut.TargetPath)"

# Kill all instances
Get-Process Antigravity -ErrorAction SilentlyContinue | Stop-Process -Force

# Launch fresh
Start-Process -FilePath 'C:\Users\CLINIC\AppData\Local\Programs\Antigravity\Antigravity.exe' -WindowStyle Normal

# Check window
Get-Process Antigravity | Format-Table Id, ProcessName, MainWindowTitle, Responding

# Bring window to front
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
[Win32]::ShowWindowAsync($p.MainWindowHandle, 1); 
[Win32]::SetForegroundWindow($p.MainWindowHandle)
```

## Notable Errors from Logs

From `main.log` (hourly auto-updater check cycle):
```
[error] Error: net::ERR_INTERNET_DISCONNECTED
[error] Error: net::ERR_NAME_NOT_RESOLVED
[error] Error: net::ERR_NETWORK_IO_SUSPENDED
[error] [AutoUpdater] Failed to check for updates
```

From `language_server.log`:
```
Failed to get OAuth token: failed to compute token: Post "https://oauth2.googleapis.com/token": dial tcp: lookup oauth2.googleapis.com: no such host
```

## Resolution

1. Killed all stale Antigravity processes (5 were running from repeated clicks)
2. Verified internet was working (Test-Connection passed)
3. Launched fresh instance
4. Brought window to foreground with Win32 API
5. App rendered normally once it could reach Google's servers
