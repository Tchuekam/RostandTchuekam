# Aionrs Provider Configuration (28 May 2026)

## Environment

- AionUI backend DB: `C:\Users\CLINIC\.aionui-web-dev\aionui-backend.db`
- AionRS logs: `C:\Users\CLINIC\.aionui-web-dev\logs\YYYY-MM-DD.aionrs.log`
- Session index: `C:\Users\CLINIC\.aionui-web-dev\aionrs-sessions\index.json`
- Session data: `C:\Users\CLINIC\.aionui-web-dev\aionrs-sessions\YYYY-MM-DD_<session_id>.json`
- Builtin skills: `C:\Users\CLINIC\.aionui-web-dev\builtin-skills\`
- Platform SQLite CLI (for DB inspection): `C:\Users\CLINIC\AppData\Local\Android\Sdk\platform-tools\sqlite3.exe`

## Providers Table Schema

The `providers` table in `aionui-backend.db` stores all LLM provider connections:

```sql
CREATE TABLE providers (
    id              TEXT PRIMARY KEY,     -- unique provider ID (e.g. "tchuekam-gemini")
    platform        TEXT NOT NULL,        -- provider platform (e.g. "gemini", "openai")
    name            TEXT NOT NULL,        -- human-readable name (e.g. "TChuekam Gemini")
    base_url        TEXT NOT NULL,        -- API base URL (e.g. "https://generativelanguage.googleapis.com")
    api_key_encrypted TEXT NOT NULL,       -- AES-ENCRYPTED API key (NOT plaintext)
    models          TEXT NOT NULL DEFAULT '[]',  -- JSON array of model IDs
    enabled         INTEGER NOT NULL DEFAULT 1,  -- 1=enabled, 0=disabled
    capabilities    TEXT NOT NULL DEFAULT '[]',
    context_limit   INTEGER,
    model_protocols TEXT,
    model_enabled   TEXT,                 -- JSON map of model->bool (e.g. {"gemini-2.5-flash":true})
    model_health    TEXT,
    bedrock_config  TEXT,
    created_at      INTEGER NOT NULL,      -- Unix ms timestamp
    updated_at      INTEGER NOT NULL,      -- Unix ms timestamp
    is_full_url     INTEGER NOT NULL DEFAULT 0
);
```

### Existing Provider Record (tchuekam-gemini as of 28 May 2026)

```
id:           tchuekam-gemini
platform:     gemini
name:         TChuekam Gemini
base_url:     https://generativelanguage.googleapis.com
api_key:      [AES-ENCRYPTED, NOT plaintext]
models:       ["gemini-2.5-pro", "gemini-2.5-flash"]
model_enabled: {"gemini-2.5-flash":true, "gemini-2.5-pro":true}
enabled:      1
```

## CRITICAL: API Key Encryption

API keys in Aionrs are **encrypted at rest** using the app's own encryption mechanism. You CANNOT:

- ❌ Update the key directly in SQLite with raw text — it will be stored as encrypted garbage and the app won't decode it
- ❌ Base64-encode the key manually — the encryption uses a key derived from the app's runtime secrets
- ❌ Bypass the encryption layer via SQL UPDATE

**✅ You MUST update API keys through the AionUI web app's settings UI.** The app encrypts the key before writing it to the database.

### How to Find the Settings

1. Open the AionUI web app in your browser
2. Look for a gear icon, menu button (≡), or settings link
3. Find "Providers", "API Keys", "Connections" or similar section
4. Locate the Gemini / TChuekam Gemini provider entry
5. Paste the new API key and save
6. The app encrypts it and writes to the DB

### Diagnostic: Verify the Key is Working

Check `~/.aionui-web-dev/logs/YYYY-MM-DD.aionrs.log` for:

| What to look for | Meaning |
|---|---|
| `provider: "openai"` | Using AionRS backend (routes through OpenAI-compatible proxy) |
| `session started` with correct model name | Provider connected |
| `"outgoing request"` with full JSON payload | Request successfully sent |
| `"sse chunk received"` with content | Model is responding |
| `Provider error: Rate limited, retry after 5000ms` | Rate limit hit — auto-retries in 5 seconds |

## Rate Limiting Behavior

Aionrs uses a **cloud proxy** that applies its own rate limits before requests reach the underlying LLM API (Google, OpenAI, etc.).

**Error signature:**
```
Aionrs agent error: Provider error: Rate limited, retry after 5000ms
```

**What happens:**
1. Aionrs proxy receives your request
2. Proxy checks its rate limit quota for your account
3. If over limit, returns HTTP 429 with "retry after 5000ms"
4. Aionrs agent automatically retries after 5 seconds
5. Request usually goes through on first or second retry

**This is NOT a Google Gemini API quota issue** — it's the Aionrs cloud service limiting your requests. The Google API (generativelanguage.googleapis.com) has its own 60 req/min free tier, but Aionrs adds another layer on top.

**Mitigation:**
- Wait 5-10 seconds between messages (the auto-retry handles it)
- Upgrade your Aionrs plan (if a paid tier exists with higher limits)
- Switch to Gemini CLI backend instead of AionRS (bypasses the cloud proxy entirely)
- Use a direct Google AI Studio API key (60 req/min free) through a direct integration

## Model Switching

The Aionrs agents switch models between sessions. From the session log:

| Session | Provider | Model |
|---|---|---|
| 1778f884 | openai | gemini-2.5-pro |
| 97b4af03 | openai | gemini-2.5-pro (initial) → gemini-2.5-flash (after rate limit) |
| eec2f383 | openai | gemini-2.5-flash |
| 322423ae | openai | gemini-2.5-pro |

The Aionrs backend auto-falls back from pro to flash when rate limits are hit.

## Session Storage

Each session is persisted as JSON at:
`C:\Users\CLINIC\.aionui-web-dev\aionrs-sessions\YYYY-MM-DD_<session_id>.json`

Structure includes: id, timestamps, provider, model, cwd, total_usage (token counts), full message history (role + content).

Index of all sessions:
`C:\Users\CLINIC\.aionui-web-dev\aionrs-sessions\index.json`

## Related

- `ai-frontend-branding` SKILL.md — main skill for branding TCHUEKAM on AionUI
- `references/aionui-investigation.md` — system prompt injection investigation
- `references/aionui-deliverables.md` — concrete deliverables (Gemini CLI skill, auto-inject paths)
