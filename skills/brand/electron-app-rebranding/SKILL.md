---
name: electron-app-rebranding
description: "Rebrand Electron desktop applications — replace logos, icons, window title, tray icons, display name, and remove third-party branding. Covers Antigravity, AionUI, and any Electron/ASAR-packaged desktop app on Windows."
version: 1.1.0
author: giantect
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [brand, electron, desktop, rebranding, asar, antigravity, tchuekamui]
    related_skills: [ai-frontend-branding, brand-identity]
---

# Electron App Rebranding

Rebrand third-party Electron desktop applications for your own brand identity. This skill covers replacing visual assets (icons, tray, splash), renaming the app in package.json, patching window titles, injecting icons into EXEs, and removing third-party branding — without touching the application's logic or features.

## When to Use

- User asks to "change the logo" or "rename the app" in an Electron desktop app
- User says "I want this to say TchuekamUI instead of Antigravity" or similar
- Need to remove third-party branding (Google, etc.) from a desktop agent
- Preparing a branded build of an open-source Electron app for distribution

## App Detection

Find Electron apps on Windows:

```bash
# Check common install locations
ls "/c/Users/$USER/AppData/Local/Programs/"
ls "/c/Program Files/"
ls "/c/Program Files (x86)/"

# Check custom install locations (user may have placed it anywhere)
find /c/Users/$USER -maxdepth 4 -name "app.asar" -type f 2>/dev/null
find /d/ -maxdepth 4 -name "app.asar" -type f 2>/dev/null

# Check desktop for shortcuts to find the actual target
ls -la "/c/Users/$USER/Desktop/" | grep -iE "\.lnk$"

# Read shortcut target (PowerShell):
powershell.exe -Command "\$shell = New-Object -COM WScript.Shell; \$shortcut = \$shell.CreateShortcut('C:\\Users\\$USER\\Desktop\\AppName.lnk'); Write-Output \$shortcut.TargetPath; Write-Output \$shortcut.WorkingDirectory"
```

## Rebranding Inventory: What to Change

### 1. Package Metadata (package.json inside asar)

| Field | What to Change | Example |
|---|---|---|
| `productName` | Display name in window title, taskbar, about dialog | `"TchuekamUI"` |
| `name` | Internal npm-style name (lowercase, no spaces) | `"tchuekam-ui"` |
| `description` | Short description | `"TchuekamUI - Agentic Desktop by Giantect Empire"` |
| `author.name` | Remove third-party author, add your brand | `"Giantect Empire"` |
| `author.email` | Your support email | `"support@giantect.cm"` |
| `homepage` | Your website URL | `"https://giantect.cm"` |

### 2. Application Icon

Two possible locations:
- **Inside the asar**: `\icon.png` (standard Electron convention)
- **Outside the asar**: `resources/app.png` or `resources/icon.png` (some apps keep the icon at resources root, NOT inside the asar)

Typically 512×512 PNG (Electron standard). **Replace with your own logo PNG at the same resolution.**
The icon shows in: taskbar, window header, task switcher, file manager.

**CRITICAL:** Check BOTH locations. The `resources/app.png` icon is the one Windows shows for the EXE in File Explorer and taskbar. If you only replace the one inside the asar, the external icon stays unchanged.

### 3. Tray Icons

Common patterns:
- `trayTemplate.png` (22×22) — small monochrome for system tray
- `trayTemplate@2x.png` (44×44) — Retina version of the same
- `tray.png` / `tray@2x.png` (some apps)
- Name may vary — check the app's `dist/tray.js` for icon filename references

Tray icons are typically **template images** (macOS-style: transparency = full area, black content = visible region). On Windows, any PNG works but keep it simple and high-contrast at small sizes.

### 4. Window Title

- Set via `productName` in `package.json` (most Electron apps use this as the window title)
- Some apps set it explicitly in `dist/main.js` or a constants file — search for:
  ```javascript
  title: 'Antigravity'
  // or
  `${productName}`
  ```
- The window title displays in the title bar and taskbar

### 5. Additional Branding (check during investigation)

- **Splash/loading overlay**: `loadingOverlay.html`, `loadingOverlay.js`
- **About dialog**: Hardcoded text in `dist/main.js`, `dist/menu.js`, or `dist/updater.js`
- **Update checker**: `electron-updater` configuration in `package.json` — may reference third-party update server
- **System menu**: `dist/menu.js` — look for "About Antigravity", "Check for Updates" text
- **Analytics/Sentry**: `dist/sentry/` — may need to disable if you don't use Sentry
- **Context menu labels**: Hardcoded text strings

## Workflow

### Before Starting: Prepare Your Logo

You need a source logo image. The user likely has a JPG/PNG on their Desktop.

**Find the source logo:**
```bash
ls -la "/c/Users/$USER/Desktop/" | grep -iE "logo|icon|png|jpg"
```

**Convert source image to required formats using ffmpeg:**

```bash
# To 512×512 PNG (for app icon replacement):
ffmpeg -i "/path/to/source.jpg" -vf "scale=512:512:force_original_aspect_ratio=increase,crop=512:512" /path/to/output.png -y

# To 256×256 ICO (for EXE icon injection):
ffmpeg -i "/path/to/source.jpg" -vf "scale=256:256:force_original_aspect_ratio=increase,crop=256:256" /path/to/output.ico -y
```

**Python Pillow fallback** (if ffmpeg unavailable):
```python
from PIL import Image
img = Image.open('source.jpg')
img.thumbnail((512,512))
new = Image.new('RGBA', (512,512))
new.paste(img, ((512-img.width)//2, (512-img.height)//2))
new.save('output.png', 'PNG')
```

**Known issue:** The user's Python environment may have a broken `re` module (SRE module mismatch) — ffmpeg is the reliable fallback.

### Step 0: Detect Install Location + Find All Branded Assets (Outside ASAR)

While inside the app's root directory, take an **inventory of all branding outside the asar**:

```bash
ls -la                                      # main EXE, uninstaller EXE
ls -la resources/                           # app.png, app-update.yml, manifest.webmanifest, sw.js, locales/
```

Look for these files **outside** the asar:
- `app.png` or `icon.png` — app icon in resources/
- `app-update.yml` — auto-update config (contains app name)
- `manifest.webmanifest` — PWA manifest (contains app name + icons)
- `sw.js` — service worker (may contain app name)
- `Uninstall *.exe` — uninstaller executable
- `locales/*.pak` — some apps embed branding in locale files

Also check for sibling folders:
- `bundled-*/` — bundled services
- `hub/` — companion apps
- `pwa/` — progressive web app layer
- `pet-states/` — AI companion states (may have standalone HTML/JS with hardcoded names)

### Step 1: Extract the ASAR

```bash
# Install asar CLI
npm install -g asar

# Navigate to the app's resources folder
cd "C:\Users\<user>\AppData\Local\Programs\<AppName>\resources"
# OR if custom install path:
cd "/d/MyApp/resources"

# Extract the asar
asar extract app.asar ./app_extracted
```

**Note:** For large asars (300+ MB with bundled node_modules), extraction can take 1-2 minutes. Be patient.

### Step 2: Replace Assets (Inside ASAR)

Replace these files in the extracted directory:
- `icon.png` — replace with your 512×512 PNG (if present)
- `trayTemplate.png` — replace with your 22×22 tray icon (if present)
- `trayTemplate@2x.png` — replace with your 44×44 tray icon (if present)

### Step 3: Replace Assets (Outside ASAR)

| File | Location | What to Do |
|---|---|---|
| `app.png` | `resources/app.png` | Replace with your 512×512 app icon PNG |
| `icon.png` | `resources/icon.png` | Same — some apps use this name instead |
| `app-update.yml` | `resources/app-update.yml` | Edit: rename `provider/owner/repo`, change app name references, disable auto-update by setting `publishAutoUpdate: false` |
| `manifest.webmanifest` | `resources/manifest.webmanifest` | Edit: update `name`, `short_name`, `description`, `icons[].src` paths |

### Step 4: Edit package.json

Update `productName`, `name`, `author`, `description`, `homepage`.

### Step 5: Check for Hardcoded Strings

The old app name appears in JS code (window titles, About dialogs, menu items, notification text, error messages). Search broadly:

```bash
grep -rn "OldName\|old.name\|oldname\|OLD_NAME\|old_name" . \
  --include="*.js" --include="*.json" --include="*.html" --include="*.css" \
  --exclude-dir=node_modules 2>/dev/null
```

**Important:** Do NOT rename internal identifiers like `OldNameScrollArea`, `OldNameSelect`, or npm package dependencies (e.g. `@oldname/web-host`). Only change:
- Display-name strings displayed in UI
- Product name in package.json
- Email addresses
- Copyright notices

Use `sed` for bulk replacement:
```bash
sed -i 's/OldName/NewName/g' file.js
sed -i 's/OLDNAME/NEWNAME/g' file.js
```

### Step 6: Repack the ASAR

```bash
cd "/path/to/app/resources"
asar pack ./app_extracted app.asar
```

**WARNING:** For large apps (376MB with node_modules), asar pack can take 5+ minutes. Run it in background:
```bash
cd "/path/to/app/resources" && asar pack ./app_extracted app.asar &
# Check progress periodically with:
ls -la app.asar
```

If the repack times out or the file hasn't appeared after 5 minutes, kill the process and try a different approach (see Pitfalls below).

### Step 7: Inject Icon into EXE (via rcedit)

The `resources/app.png` icon replacement covers the taskbar appearance, but the EXE file itself still shows the old icon in File Explorer. Use `rcedit` to inject the ICO directly.

**Download rcedit:**
```bash
curl -L -o /path/to/rcedit.exe \
  "https://github.com/electron/rcedit/releases/download/v2.0.0/rcedit-x64.exe"
```

**Inject the icon:**
```bash
# Use the .ICO file (converted earlier) — PNG will NOT work here
./rcedit.exe "NewName.exe" --set-icon "/path/to/logo.ico"

# Also do the uninstaller if it exists:
./rcedit.exe "Uninstall NewName.exe" --set-icon "/path/to/logo.ico"
```

**Set version info strings (recommended):**
```bash
./rcedit.exe "NewName.exe" \
  --set-version-string "FileDescription" "NewName - description" \
  --set-version-string "ProductName" "NewName" \
  --set-version-string "CompanyName" "Giantect Empire" \
  --set-version-string "LegalCopyright" "Copyright 2026 Giantect Empire. All rights reserved." \
  --set-version-string "OriginalFilename" "NewName.exe"
```

These strings appear in Windows file properties (right-click → Properties → Details).

### Step 8: Update Desktop Shortcut

```bash
# Write a PowerShell script:
cat > update_shortcut.ps1 << 'PSEOF'
$shell = New-Object -COM WScript.Shell
$shortcut = $shell.CreateShortcut("C:\Users\CLINIC\Desktop\OldName.lnk")
$shortcut.TargetPath = "D:\Path\To\NewName.exe"
$shortcut.WorkingDirectory = "D:\Path\To"
$shortcut.IconLocation = "D:\Path\To\logo.ico"
$shortcut.Save()
Write-Output "Shortcut updated to NewName"
PSEOF

# Run it:
powershell.exe -ExecutionPolicy Bypass -NoProfile -File "update_shortcut.ps1"
```

The shortcut filename can be manually renamed by the user (right-click → Rename).

### Step 9: Rename Executables

```bash
mv "OldName.exe" "NewName.exe"
mv "Uninstall OldName.exe" "Uninstall NewName.exe"
```

### Step 10: Restart the App

```bash
taskkill /F /IM "OldName.exe" 2>/dev/null
start "" "D:\Path\To\NewName.exe"
```

## Pitfalls

- **ASAR repack is slow for large apps** — 376MB asars with bundled node_modules can take 5+ minutes to repack. Run in background and monitor with `ls -la app.asar`. If it times out, try extracting, packing only the `out/` directory (the actual app code, excluding node_modules), then replacing the original asar's modified files by hex-patching the asar binary or using `asar extract-file` / `asar add`.
- **asar extract-file may fail** on some asar versions (TypeError: Cannot read properties of undefined). In that case, fall back to full extract + repack.
- **Windows file locks** — If the app is running, you can't overwrite the asar or rename EXEs. Kill it first (Task Manager or `taskkill /F /IM AppName.exe`).
- **Auto-updaters restore original branding** — `electron-updater` replaces `app.asar` on update. Either disable auto-updates in `app-update.yml` (`publishAutoUpdate: false`) or re-apply the rebrand after each update.
- **Sentry/analytics** — If the app uses Sentry (check `sentry/` folder in Roaming), it still reports to the original developer unless you disable or replace the DSN.
- **Code signing** — If the app has a digital signature, removing it may trigger Windows SmartScreen warnings. For internal use this is fine.
- **Not all text is in the asar** — Some Electron apps load UI from a remote URL (webview). Those are not rebrandable locally.
- **Python environment may be broken** — The user might have SRE module mismatch errors. Use ffmpeg for image conversion instead of Python Pillow.

## References

- `references/antigravity-rebrand-2026-05-27.md` — Full investigation log and asset paths for Google Antigravity 2.0.6 rebrand to TchuekamUI
- `references/aionui-desktop-rebrand-2026-05-27.md` — Full investigation log and asset paths for AionUI Desktop rebrand (non-AppData install, Chromium DLLs, PWA layer, asar unpacked)
