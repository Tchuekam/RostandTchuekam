# Antigravity IDE — Configuration Reference

Antigravity is a **VS Code fork** (Google's internal IDE released externally). It shares VS Code's configuration structure and extension system.

## Key Paths (Windows)

| What | Path |
|------|------|
| App data (settings, extensions) | `%APPDATA%\Antigravity IDE\` |
| User settings.json | `%APPDATA%\Antigravity IDE\User\settings.json` |
| Extensions | `%USERPROFILE%\.antigravity-ide\extensions\` |
| Extension index | `%USERPROFILE%\.antigravity-ide\extensions\extensions.json` |
| Runtime args | `%USERPROFILE%\.antigravity-ide\argv.json` |

## Injecting a Custom System Prompt

Antigravity has no built-in "system prompt" field. To brand it as TCHUEKAM, use one of:

1. **Continue.dev extension** — supports custom system instructions in its config
2. **Cody (Sourcegraph) extension** — supports custom instructions
3. **Gemini CLI Extension** — if available, inject via extension settings
4. **settings.json `"chat.customInstructions"`** — if the installed AI chat extension supports it

## Current User Config

As of 30 May 2026, `settings.json` contains only:
```json
{
    "python.languageServer": "Default"
}
```

## Architecture Notes

- Electron-based (same as VS Code)
- Uses `electron 38.4.0` (matching Logseq's version)
- Extensions are standard VS Code extensions — `.vsix` installable
- Settings are JSON — no YAML or EDN complexity

## Integration with TCHUEKAM Agent

Same approach as any VS Code fork: TCHUEKAM writes directly to `settings.json` or extension-specific config files.
