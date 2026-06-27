---
name: ai-coding-tool-prompting
description: "Write production-grade prompts for third-party AI code-generation tools (Google Antigravity, Codex CLI, OpenCode, Claude Code, Cursor). For non-technical founders who delegate all coding work to AI tools — translates what the user wants built into a structured prompt the tool can execute directly."
version: 1.0.0
author: giantect
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [prompt-engineering, antigravity, codex, coding, delegation, non-technical, founder]
    related_skills: [codex, opencode, claude-code, website-critical-audit, writing-plans]
---

# AI Coding Tool Prompting

## When to Use

- User says "write a prompt to [tool name] to do X"
- User wants to paste something into Antigravity, Codex CLI, OpenCode, Claude Code, or Cursor
- User has a non-technical request (build a scraper, fix a website, create an agent) and needs it translated into executable instructions for an AI coding tool
- User asks you to "write a prompt for Antigravity" specifically

## Core Principle

You are translating between two minds:
1. **The user** — knows WHAT they want, non-technical, thinks in outcomes
2. **The AI coding tool** — knows HOW to build, needs complete technical specs, will hallucinate if gaps exist

Your job: bridge the gap. Take the user's business-level request and write a prompt that the coding tool can execute without asking clarifying questions.

## Architecture of a Good Prompt

Every prompt to an AI coding tool needs these 7 elements:

### 1. Project Identity
Start with: what is this? One sentence.
> "I need you to build a web scraping agent called SCRAPER for my enterprise AI system (Giantect Empire)."

### 2. Tech Stack & Constraints
State the stack explicitly. If the user didn't specify, pick the right default:
- **Antigravity / Codex CLI** → Node.js with Puppeteer/Playwright, SQLite3, Express.js
- **Vercel deployment** → mention Vercel-compatible (serverless functions, no persistent FS)
- **User's context** → "Deployable on Vercel or a cheap VPS"
- **Mobile-first** for African users

### 3. What to Build (the Feature List)
Break the request into numbered subsystems. Each subsystem gets:
- What it does
- What tech it uses
- Any key behaviors (dedup, rate limiting, export)

Write these as bullet points, not paragraphs. The coding tool parses lists better.

### 4. Edge Cases & Rules (Critical!)
Non-technical users never think about edge cases. You must add them:
- Rate limits (e.g. "max 20 DMs/hr, 50 emails/day")
- Dedup rules (e.g. "dedup by phone + email automatically")
- Retry logic (e.g. "auto-retry failed messages once")
- Validation (e.g. "verify phone numbers are valid Cameroon format")
- Error handling (e.g. "if scraper gets blocked, rotate user agent and retry")

### 5. Output / Deliverable
Tell the tool what success looks like:
> "Build the complete project. Test that the scraper can find at least 10 real business leads. Show me the code and how to run it."

### 6. Timing / Priority
If parts are more important:
> "Build the scraper engine first, then the dashboard UI. The database can be a simple SQLite schema."

### 7. Style Signal
Add one line at the end about how you want the response:
> "Explain what you built and how to run it. Keep explanations minimal — focus on code."

## Tool-Specific Notes

### Google Antigravity (web)
- URL: `antigravity.google`
- This is Google's web-based AI coding tool (Gemini-powered)
- Prompts go into a chat textbox
- Antigravity can preview web builds and deploy
- **It expects full specs** — it won't ask you for clarification the way a human would
- Can write files directly into a project workspace
- For website fixes: give it the URL + specific changes needed
- For new projects: give it the full architecture prompt

### Codex CLI
- Runs in terminal via `codex` command
- Can execute code, not just generate it
- Better for backend/tool projects (scrapers, APIs, scripts)
- Can test its own code if the prompt includes test instructions
- Give it: tech stack, folder structure, file-by-file breakdown if complex
- Codex CLI will iterate if you give it feedback — include "test that X works"

### OpenCode
- Similar to Codex CLI but more focused on review
- Good for: improving existing code, adding features to existing projects
- Include file paths to existing code in the prompt

### Claude Code
- CLI tool (`claude` command)
- Best for: frontend, React, design-heavy builds
- Can read screenshots / images — use that for visual feedback
- Slower but more thorough than Codex

## Writing Prompts for Website Fixes (Post-Audit)

When the user wants you to write a prompt to fix a website you've audited (common pattern — see `website-critical-audit` skill):

1. Open the site in browser to confirm current state
2. List each fix as a separate numbered issue
3. For each issue, write: WHAT is wrong + EXACT fix needed + WHY it matters
4. Add brand context (company name, colors, tone) so the coding tool doesn't invent them
5. Tell the tool to make changes directly and show a summary

Example structure:
```
ISSUE 1 — Partner logo credibility
[what's wrong] [fix] [why]

ISSUE 2 — Mobile responsiveness
[what's wrong] [fix] [why]
```

## Writing Prompts for New Projects (Scrapers, Agents, Tools)

When the user wants a new tool built from scratch:

1. **Name the project** — one clear name (SCRAPER, NEXUS, etc.)
2. **State the business context** — who is this for, what problem does it solve
3. **List features as numbered subsystems**
4. **Add edge cases & constraints** (this is where most tools fail)
5. **Specify the tech stack**
6. **Define the output** (code, dashboard, CLI tool, API?)
7. **Add verification criteria** — how do we know it worked?

## Pitfalls

- **Don't assume the user knows their tech stack.** They're non-technical. If they say "Antigravity" but mean the web tool, confirm. If they say "Codex" but it's not installed, suggest alternatives.
- **Don't write prompts in the user's voice.** Write them as instructions FROM you TO the tool. The user is just the messenger.
- **Gaps kill prompts.** Missing a single constraint (rate limit, dedup rule, format spec) means the tool builds it wrong and the user comes back frustrated. Be paranoid about edge cases.
- **The tool will hallucinate features you didn't ask for.** If you don't specify that something should be simple, it will add authentication, Docker, Kubernetes, and a full CI/CD pipeline. Be explicit about scope: "This is a prototype — no auth, no Docker, no cloud deployment. Just run locally."
- **Don't let the coding tool write your own brand prompt.** If the user says "write a prompt for Antigravity", YOU write the prompt, don't hand it back to an LLM to compose for itself. You know the user's context, tools, and constraints better than the external tool does.
- **Non-technical users test visually.** They won't run tests, check logs, or use a debugger. If your prompt tells the tool to build something, also tell it to validate itself and report status.

## Related Skills

- `website-critical-audit` — audit a site first, then use this skill to write the fix prompt for Antigravity
- `codex` — running Codex CLI directly (delegation)
- `opencode` — running OpenCode CLI
- `claude-code` — running Claude Code CLI
- `writing-plans` — writing structured plans for the agent itself (different class — this skill is about writing prompts for EXTERNAL tools)

## Reference Files

- `references/giantect-antigravity-prompts.md` — real-world Antigravity prompts from Giantect Empire sessions (website fixes + scraper agent build). Use as copy-paste templates for similar requests.

## Common Prompts You'll Write

### Web Scraper Agent
```
I need you to build a web scraping agent called SCRAPER...
[Tech stack] [Features] [Edge cases] [Output]
```

### Cold Outreach System
```
I need you to build a contact database + outreach scheduler...
[NEXUS integration] [Rate limits] [Message templates]
```

### Website Fixes
```
I need you to fix [N] issues on my website: [URL]...
[Issue 1] [Issue 2] [Issue 3]...
```

### Dashboard / Admin Panel
```
I need a simple web dashboard that shows [data] with [features]...
[Tech stack] [Design] [Deployment]
```
