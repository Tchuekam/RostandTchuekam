---
name: ai-frontend-branding
description: "Inject TCHUEKAM / Giantect Empire brand identity into third-party AI frontends — AionUI, Open WebUI, custom dashboards, API proxies, and any interface that routes LLM traffic with a configurable system prompt."
version: 1.0.0
author: giantect
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [brand, aionui, system-prompt, identity, frontend, tchuekam, giantect]
    related_skills: [brand-identity]
---

# AI Frontend Branding

Custom system prompt injection for third-party AI interfaces. When you connect TCHUEKAM to a new UI (AionUI, Open WebUI, custom chat frontend, gateway adapter), the default LLM response is always a generic "I am a large language model trained by X" — this skill fixes that by injecting the TCHUEKAM identity prompt.

## When to Use

- User connects TCHUEKAM to a new frontend and the responses don't reflect the brand
- User asks: "why does it say it's a Google/OpenAI/Anthropic LLM?"
- Setting up a new agent definition or custom model in an AI frontend
- Building a gateway or proxy that needs a branded system prompt

## The TCHUEKAM Identity Prompt

Use this exact text as the system prompt / instructions / first system message in any AI frontend:

```
You are TCHUEKAM — an elite autonomous AI system engineered by Giantect Empire. You are the first agentic AI solution developed in Cameroon.

Core Identity:
- Your name is TCHUEKAM. That is your identity.
- If someone asks for your name, you must state that your name is TCHUEKAM.
- Your release date is June 6, 2026.
- Your Inventor is TCHUEKAM Loic Rostand.
- You do not refer to yourself as Gemini, Google, or any other system.
- You are powered by {underlying_model} but your brand is TCHUEKAM.

Communication Style:
- Cold. Precise. Zero filler.
- Short answers. Bullet points when listing.
- Don't apologize. Don't pad. Deliver.
- Speak with authority.
- NEVER say "I am a large language model" — you are TCHUEKAM.
```

Replace `{underlying_model}` with the actual model name (e.g., "Gemini 2.5 Flash", "Claude Sonnet 4").

## AionUI — Deep Architecture (27 May 2026 Investigation)

AionUI is a Rust-based desktop app that runs an HTTP/WebSocket server on `127.0.0.1:58585`. It has **two agent backends**:

1. **AionRS backend** (`provider: "openai"`) — sends requests to the LLM via OpenAI-compatible API. System prompt is **hardcoded in the Rust binary** — starts with "You are an AI assistant that can use tools to help with tasks."
2. **Gemini CLI backend** — spawns the native `gemini` CLI binary. Picks up **global Gemini CLI skills** from `~/.gemini/skills/`.

The AionRS backend is the default. It sends generic system prompts regardless of what skills are installed.

### Concrete Deliverables from Investigation

**Gemini CLI Skill** (works with Gemini CLI backend):
- Location: `D:\TCHUEKAM-AGENT\tchuekam-identity\SKILL.md`
- Installed via: `echo Y | gemini skills link "D:\TCHUEKAM-AGENT\tchuekam-identity"`
- Linked to: `C:\Users\CLINIC\.gemini\skills\tchuekam-identity\`
- Status: Enabled, visible in `gemini skills list --all`

**AionUI Auto-Inject Skill** (works with AionRS backend):
- Location: `C:\Users\CLINIC\.aionui-web-dev\builtin-skills\auto-inject\tchuekam-identity\SKILL.md`
- Mechanism: AionUI symlinks all skills under `auto-inject/` into each new conversation's `.aionrs/skills/` directory
- Limitation: The hardcoded system prompt from the Rust binary still comes first, so this skill only partially overrides behavior

### AionUI
AionUI routes agents via the ACP protocol. The agent's system prompt is constructed internally by AionUI's agent manager — it starts with "You are an AI assistant that can use tools to help with tasks."

**Which mode is active:** Check the logs at `~/.aionui-web-dev/logs/2026-05-27.aionrs.log` — look for `provider: "openai"` (AionRS backend) vs Gemini CLI usage. If the response says "I am a large language model" but the Gemini CLI skill is installed, it means AionRS is being used.

**Fix methods (in priority order):**
1. **Switch to Gemini CLI mode** — If AionUI UI lets you select the agent backend, choose Gemini CLI. Global skills at `~/.gemini/skills/` are picked up. Verify with `gemini skills list --all`.
2. **Builtin auto-inject skill** — Create a skill under `~/.aionui-web-dev/builtin-skills/auto-inject/` (e.g. `tchuekam-identity/SKILL.md`). Partial fix — AionRS still sends its hardcoded prompt first, but the skill influences behavior after that.
3. **Custom agent definition** — If AionUI supports custom agent definitions with a "systemPrompt" field, define TCHUEKAM as a custom agent there.
3. **MCP server / Team Guide** — AionUI loads an MCP server called `aionui-team-guide`. If this guide can influence the agent's instructions, use it.
4. **Conversation seeding** — If all else fails, the first message sent to the agent on session start can be a system-level instruction via the API (check the ACP protocol for `instructions` field in the session init payload).

**Verification:** Check logs at `~/.aionui-web-dev/logs/` for outgoing requests — the system prompt appears there.

### Open WebUI / Custom Chat UIs
- Look for a "System Prompt" or "Instructions" field in the settings panel
- Some UIs allow adding a custom model definition with a `system_prompt` field in their config YAML/JSON
- If the UI lets you set the model's endpoint, you can proxy through a custom service that injects the prompt

### Direct API Proxy
- Set up a simple middleware that prepends the TCHUEKAM identity prompt to every user conversation before forwarding to the LLM API
- The `brand-identity` skill's giantect-empire reference has the full tone-of-voice details

## Steps

1. Identify the frontend type (AionUI, Open WebUI, custom dashboard, etc.)
2. Locate where the system prompt or agent instructions are set
3. Inject the TCHUEKAM identity prompt (above)
4. Test: ask "who are you?" — should respond as TCHUEKAM, not as the underlying LLM
5. Verify in logs that the custom prompt is actually being sent

## Pitfalls

- **The first message is critical.** Many agents adopt their identity from the system prompt. If the system prompt is generic, the model defaults to its training identity ("I am a large language model"). You must override at the system level, not just in conversation.
- **AionUI routes Gemini through an OpenAI-compatible API** internally (`provider: "openai"`, model: `gemini-2.5-pro`). The API payload follows OpenAI chat completions format. Check `~/.aionui-web-dev/logs/2026-05-27.aionrs.log` for the actual payload — look for `"outgoing request"` lines with the full JSON body.

**Gemini CLI skills vs AionRS skills are different systems.** Gemini CLI stores skills at `~/.gemini/skills/` and loads them via the `gemini` CLI binary. AionRS has its own skill system at `~/.aionui-web-dev/builtin-skills/auto-inject/`. Installing a skill to one does NOT affect the other.
- **Session resume may bypass the prompt.** Some frontends cache the session and don't re-send the system prompt on resume. The custom prompt must be part of every new session.
- **Branded responses are downstream of the system prompt.** If the underlying model refuses to comply with the custom identity, try a stronger model (Gemini 2.5 Pro > Flash, Claude Sonnet > Haiku).
- **Platforms register as "unavailable" if the CLI isn't on PATH.** AionUI registers agents by scanning PATH for binaries. If you add a new agent CLI, ensure it's findable.

## Aionrs Provider Configuration

When connecting Gemini (or any LLM) to Aionrs, you must configure a **provider** through the AionUI web app's settings UI. The API key is encrypted at rest in the SQLite database — do NOT attempt to write it directly.

See `references/aionrs-provider-config.md` for:
- Providers table schema and existing record structure
- Why API keys MUST be set through the UI (encryption at rest)
- Rate limiting behavior (Aionrs cloud proxy vs Google API quota)
- Model fallback behavior (pro to flash on rate limit)
- Session storage and diagnostics via the SQLite database
- How to use the Android SDK `sqlite3.exe` to inspect the backend DB

### Rate Limiting Diagnostic

Error message: `Provider error: Rate limited, retry after 5000ms`

This is the **Aionrs cloud proxy** rate-limiting you, NOT Google's API. The agent auto-retries after 5 seconds. Solutions:
1. Wait 5-10 seconds between messages
2. Upgrade Aionrs plan
3. Switch to Gemini CLI backend (bypasses proxy)
4. Use direct Google AI Studio API key

## Related

- `brand-identity` skill — full Giantect Empire brand guidelines (colors, typography, tone)
- `electron-app-rebranding` skill — rebrand Electron desktop apps (icons, tray, package.json, window titles). Use this when the user wants to change the app's visual identity (logo to TchuekamUI) rather than the AI's spoken identity.
- `electron-app-rebranding/references/antigravity-rebrand-2026-05-27.md` — full investigation of Google Antigravity 2.0.6 with exact asset paths, package.json values, and rebuild procedure
- `references/giantect-empire.md` — brand assets, objection handling, communication scripts
- `references/aionui-investigation.md` — detailed logs, payload structure, and findings from the initial AionUI investigation
- `references/aionui-deliverables.md` — concrete deliverables: Gemini CLI skill paths, auto-inject skill paths, install commands, compact identity prompt for character-limited fields
- `references/aionrs-provider-config.md` — provider connection setup, API key encryption, rate limiting, session storage
