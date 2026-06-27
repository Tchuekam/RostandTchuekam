# rclone Google Drive Quickstart

Alternative to the full OAuth2 setup (google-workspace setup.py). Uses rclone's built-in
OAuth flow — no Google Cloud Console project, no client secrets, no Python dependencies.

Best for: users who only need Drive (file listing/reading/uploading) and don't want
to create a Google Cloud project.

## Prerequisites

- rclone installed at a known path (e.g., `/d/hermes-home/bin/rclone.exe`)

## Installation

```bash
# Download rclone Windows binary
curl -L -o /tmp/rclone.zip "https://downloads.rclone.org/rclone-current-windows-amd64.zip"
cd /tmp && unzip -o rclone.zip
# Copy the exe from the extracted folder (version number varies)
cp rclone-*/rclone.exe /d/hermes-home/bin/
```

## Setup (single command)

```bash
rclone config create gdrive drive scope=drive
```

This creates the remote `gdrive:` with scope `drive` (full access to all Drive files).
The command auto-launches an OAuth browser window on the first run. On Windows Git Bash,
the browser may not open automatically — check the terminal output for the URL
(http://127.0.0.1:53682/auth?state=...) and open it manually.

On some Windows configurations the token is already captured by the `config create`
command itself (the browser redirect loop completes internally). Verify with:

```bash
rclone ls gdrive: --max-depth 1
```

The token is stored at `C:\Users\<USER>\AppData\Roaming\rclone\rclone.conf`.

## Available Scopes

| Scope | Access |
|-------|--------|
| `drive` | Full read/write access to all files |
| `drive.file` | Access only to files created/opened by rclone |
| `drive.readonly` | Read-only access |

## Common Operations

```bash
# List root files
rclone ls gdrive: --max-depth 1

# List recursively
rclone ls gdrive:

# Download a file to local
rclone copy gdrive:path/to/file.pdf /d/downloads/

# Upload a local file to Drive
rclone copy /d/myfile.pdf gdrive:folder/

# Get file size/details (use rclone lsjson for machine-readable output)
rclone lsjson gdrive: --max-depth 1

# Sync a local folder to Drive
rclone sync /d/projects gdrive:backups/projects
```

## When to Use This vs. google-workspace Setup

| Situation | Recommended |
|-----------|------------|
| Drive-only access | rclone (this guide) |
| Drive + Gmail + Calendar + Sheets | google-workspace full OAuth2 setup |
| Non-technical user, fast setup | rclone |
| Need email sending | himalaya skill (app password) |
| Need Drive + Gmail together | Both: himalaya for email + rclone for Drive |

## Pitfalls

- `rclone config create` may time out in foreground terminal mode because it waits for
  the OAuth callback. If this happens, the token may already be saved anyway — check
  `rclone.conf` before retrying.
- On Windows, the `--max-files` flag doesn't exist; use `--max-depth` instead.
- rclone paths use `remote:path/to/folder` syntax (colon separator).
