# AionUI — System Prompt Investigation (27 May 2026)

## Environment

- AionUI home: `C:\Users\CLINIC\.aionui-web-dev\`
- AionUI backend database: `C:\Users\CLINIC\.aionui-web-dev\aionui-backend.db`
- AionRS logs: `C:\Users\CLINIC\.aionui-web-dev\logs\2026-05-27.aionrs.log`
- AionCore logs: `C:\Users\CLINIC\.aionui-web-dev\logs\2026-05-27.aioncore.log`
- Gemini CLI path: `C:\Users\CLINIC\AppData\Roaming\npm\gemini.cmd`
- Extension states: `C:\Users\CLINIC\.aionui-web-dev\extension-states.json`
- Builtin skills: `C:\Users\CLINIC\.aionui-web-dev\builtin-skills\`
- Agent manifest: `aionui-web-dev\aionrs-sessions\index.json`

## Problem

When AionUI routes through Gemini (any model), the LLM responds with its default training identity:

> "I am a large language model, trained by Google."

Instead of the TCHUEKAM / Giantect Empire brand identity.

## Root Cause

AionUI's agent manager constructs a generic system prompt for every session:

```
You are an AI assistant that can use tools to help with tasks.
You are powered by the model gemini-2.5-flash.
Working directory: C:\Users\CLINIC\.aionui-web-dev\conversations\aionrs-temp-<uuid>
Current date: 2026-05-27
```

This prompt has no brand identity, so the model defaults to its training persona.

## AionUI Agent Architecture

1. AionCore starts an HTTP/WebSocket server on `127.0.0.1:58585`
2. Agents are registered at startup by scanning PATH for CLI binaries
3. Gemini is registered as backend `gemini` with binary `gemini` at `C:\Users\CLINIC\AppData\Roaming\npm\gemini.cmd`
4. Communication uses ACP (Agent Communication Protocol) over JSON-RPC
5. System prompt is constructed by the `aion_agent` module — the template is hardcoded in the Rust binary (not in a user-editable config file)
6. Sessions are stored as JSON in `~/.aionui-web-dev/aionrs-sessions/YYYY-MM-DD_<session_id>.json`

## ACP Protocol Payload (Outgoing)

From the logs, the actual API request body sent to the model provider:

```json
{
  "max_tokens": 8192,
  "messages": [
    {
      "content": "You are an AI assistant that can use tools to help with tasks.\nYou are powered by the model gemini-2.5-flash.\nWorking directory: ...\nCurrent date: 2026-05-27\n\n# Using your tools\n - Do NOT use Bash when a dedicated tool is available...",
      "role": "system"
    }
  ]
}
```

Note: AionUI routes Gemini through an **OpenAI-compatible provider** (provider: `openai`, model: `gemini-2.5-pro`). This means the payload follows OpenAI's chat completions format.

## Logged Responses (from aionrs.log)

Line 16: `"I am a large language model, trained by Google."`
Line 33-37: Full response including "I can help you with a wide range of tasks, such as answering your questions, generating different kinds of creative content, and assisting with coding and other technical tasks..."

## Available Fix Points

1. **Builtin skills injection** — `~/.aionui-web-dev/builtin-skills/auto-inject/` — This directory hosts skills that are auto-injected into every session. Creating a skill here that sets the agent's identity could work.
2. **Custom agent definition** — If AionUI adds support for user-defined agents with custom system prompts, that's the cleanest solution.
3. **Extension system** — `extension-states.json` is empty (`{}`). Extensions could theoretically hook into the session init to modify the system prompt.
4. **Guide MCP server** — AionUI runs an MCP server called `aionui-team-guide` on port 58627. If this guide can set agent instructions, it could be used.

## Agent Registry (from aioncore.log)

At startup, only 2 agents were available: **Aion CLI** (internal) and **Gemini CLI** (via PATH scan). 18 others were unavailable because their CLIs weren't on PATH.

To add a new agent to AionUI, its CLI binary must be on the system PATH.

## Sessions Found

From `aionrs-sessions/index.json`:
- `1778f884` — gemini-2.5-pro (D:\TCHUEKAM-AGENT workspace)
- `97b4af03` — gemini-2.5-pro (default workspace)
- `5f0b29f5` — gemini-2.5-pro (D:\TCHUEKAM-AGENT workspace)
