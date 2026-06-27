---
name: deployment-readiness-audit
title: Deployment Readiness Audit
description: >-
  Run a structured pre-deployment audit across 7 domains — infrastructure,
  configuration, project structure, toolsets, integrations, security, and
  operations — to identify gaps before a product launch. Produces a
  colour-coded report with severity-graded action items. Designed for
  non-technical founders who need to know what's missing before shipping.
version: 1.0.0
author: TCHUEKAM (Giantect Empire)
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [deployment, audit, readiness, checklist, launch, release]
    related_skills:
      - startup-operations-planning
      - windows-file-organization
      - windows-app-not-opening
      - website-critical-audit
trigger: >-
  User asks for a system audit, deployment check, readiness report,
  pre-launch review, what's missing before launch, gap analysis, or
  "tell me everything that needs to be fixed before we ship"
---

# Deployment Readiness Audit

## When to Use

Execute this skill when:
- User says "audit the system", "run a readiness check", "tell me what's missing before we launch"
- User asks "what does the interface lack?", "what needs to be fixed?", "gap analysis"
- A product has a defined release date (e.g. "6 June 2026") and you need to surface blockers
- A founder is about to demo a product and needs a pre-demo checklist
- The system has never been formally audited for production readiness

This skill covers **technical infrastructure + operations readiness**. For business-workstream readiness (marketing, sales, lead gen), use `startup-operations-planning` instead.

## The 7-Domain Audit Framework

Audit every system against these 7 domains. Each domain has:
- Standard checks (always run)
- Red flags (critical failures)
- Tiered gap severity: 🔴 BLOCKER, 🟡 WARNING, ⚪ NOTE

### Domain 1: Core Infrastructure

**Purpose:** Can the machine run the agent at all?

| Check | Method | Red Flag |
|---|---|---|
| OS version | `uname -a` or `powershell (Get-CimInstance Win32_OperatingSystem).Version` | Unsupported / end-of-life OS |
| Python version | `python3 --version` | <3.10 or not found |
| Node.js version | `node --version` | <18 or not found |
| Git version | `git --version` | Not installed |
| Disk space (system drive) | `df -h /` on git-bash, or PowerShell `Get-PSDrive C` | <5 GB free (🔴); <10 GB (🟡) |
| Disk space (data drive) | `df -h /d` | <10 GB free (🟡) |
| RAM | `free -h` or `wmic OS get FreePhysicalMemory,TotalVisibleMemorySize` | <4 GB total (🔴); <8 GB (🟡) |
| Internet connectivity | `curl -s --max-time 5 https://api.ipify.org` | No internet (🔴) |
| Swap/Page file | Check pagefile.sys size | None (can cause OOM during multi-agent work) |

**Typical output format:** table with ✅ / ⚠️ / ❌ per check.

### Domain 2: Agent Configuration

**Purpose:** Is the agent itself correctly configured for deployment?

| Check | Method | Red Flag |
|---|---|---|
| config.yaml exists | `ls config.yaml` | Missing (🔴) |
| Model provider set | `grep "model:" config.yaml` | Not set or points to a dev-only model |
| API key configured | Check `auth.json` or env vars for the active provider | Missing key (🔴) |
| Prefill/boilerplate set | `ls prefill.json` or check config for `prefill_messages_file` | Missing on prod deployment (prefill may contain dev-only content) |
| Gateway channels configured | `grep -A20 "gateway" config.yaml` | No gateway section = agent can't receive external messages (🔴) |
| Fallback model defined | Check if config has a backup model provider | Single model = single point of failure (🟡) |
| State database healthy | `ls state.db*` — check file size > 1 MB | State db missing or zero-sized (🔴) |
| FTS5 search index active | Check if `tchuekam_index_search` returns results | Index missing = slow file search (🟡) |
| SOUL.md or system prompt present | `ls SOUL.md` or check config's `system_prompt` | Missing identity definition (🔴) |

### Domain 3: Project Structure

**Purpose:** Are all product files organized and ship-ready?

| Check | Method | Red Flag |
|---|---|---|
| Core docs present | Check product documentation directory | Missing architecture, branding, or deployment docs (🔴) |
| Built binary exists | Check executable size > 50 MB for desktop apps | Missing or corrupt binary (🔴) |
| Source vs. built artifacts separated | Check for nested copies (e.g. `AionUi-main/AionUi-main/`) | Duplicate directories cause confusion (🟡) |
| Legacy/abandoned directories | List all top-level project dirs | Old bot code, unused experiments left in the main tree (🟡) |
| README up to date | Read README.md | Outdated or missing (🟡) |
| .gitignore present | `ls .gitignore` | Missing (🟡) — secrets may be tracked |

### Domain 4: Tools & Skills Ecosystem

**Purpose:** Does the agent have the capabilities the product promises?

| Check | Method | Red Flag |
|---|---|---|
| Skills directory populated | `ls skills/` — check for relevant skill categories | Empty or missing key domains (browser, file, creative, etc.) |
| Critical skills loaded for the product | Verify using skills_list() | Missing WhatsApp, social media, or channel-specific skills for the product's claimed features (🔴) |
| Cron jobs configured | `ls cron/` | Empty when product claims autonomous/ scheduled operations (🟡) |
| Hooks configured | `ls hooks/` | Empty when product claims event-driven behaviour (🟡) |
| MCP servers configured | Check config for mcp: section | Missing when product needs external tool access (🟡) |
| Social media posting skills | Verify Facebook, Instagram, LinkedIn tool availability | Product claims social automation but no social media tools configured (🔴) |

### Domain 5: Network & External Integrations

**Purpose:** Can the agent actually reach the services it depends on?

| Check | Method | Red Flag |
|---|---|---|
| Internet reachable | `curl` to a public endpoint | No internet (🔴) |
| API provider reachable | `curl https://api.deepseek.com` or provider's base URL | Provider down or unreachable (🔴) |
| WhatsApp API configured | Check auth.json for WhatsApp credentials + Baileys/Cloud API setup | Core product feature missing (🔴) |
| Telegram bot configured | Check auth.json for bot token | Claimed but missing (🔴) |
| Discord bot configured | Check auth.json for token | Claimed but missing (🟡) |
| SMS gateway configured | Check for Twilio / Africa's Talking / custom SMS | Claimed but missing (🟡) |
| Email (SMTP) configured | Check Himalaya or SMTP credentials in auth.json | Email claimed but not configured (🟡) |
| Facebook/Instagram Graph API | Test a token: `curl -X GET "https://graph.facebook.com/v22.0/me?access_token=..."` | Token expired, no pages_manage_posts permission (🔴) |
| Google Drive backup | Check rclone config | No remote backup of critical documents (🟡) |
| Geolocation (IP origin) | `curl -s https://api.ipify.org` then geo-IP lookup | Verify the agent works in the target market's region |

### Domain 6: Security & Risk

**Purpose:** What could go wrong in production?

| Check | Method | Red Flag |
|---|---|---|
| API keys stored securely | Check `auth.json` or env vars | Plaintext keys on disk that ship with the product (🔴) |
| Production vs. dev config separation | Check if GODMODE / jailbreak prefill is active in config | Dev-mode jailbreak active in a deployable instance (🔴) |
| Critical doc backup | Check if TChuekamDocx/ is backed up to Drive or Git | No backup = single-drive failure loses company (🔴) |
| Encryption in transit | Check if any channels use HTTPS/TLS | Webhook endpoints without TLS (🔴) |
| Rate limits known | Document platform limits (WhatsApp 20/hr, email 50/day, etc.) | Unknown = user sends 200 messages and gets banned (🟡) |
| Session isolation | Check activation codes or subscription locking per 08_PRODUCT_ARCHITECTURE doc | In production, each client instance needs isolation (🔴) |

### Domain 7: Operations & Launch Readiness

**Purpose:** Can you ship it today?

| Check | Method | Red Flag |
|---|---|---|
| Deployment script exists | `ls deploy.sh` or CI pipeline file | No deploy flow (🔴) |
| Release date known | Confirm with user | No target (🟡) |
| Pricing documented | Check product docs for subscription tiers | Pricing undefined (🔴) |
| Backup strategy | Check for automated backup (cron, rclone, git push) | No backup strategy (🔴) |
| Error monitoring | Check if logs are configured | No way to know if the system is failing in prod (🟡) |
| Client onboarding flow defined | Check if there's a doc describing how new users get access | Missing onboarding = confused clients (🟡) |
| Known limitations documented | Check for a LIMITATIONS.md or equivalent | User discovers limits after promising features to clients (🟡) |

## Report Format

After collecting all audit data, produce a structured report in this format:

```
# DEPLOYMENT READINESS AUDIT — [Product Name]
Date: [Date]

## Summary
- Total checks: N
- 🔴 Blockers: N (must fix before launch)
- 🟡 Warnings: N (fix after launch or before demo)
- ⚪ Notes: N (informational)
- Overall verdict: NOT READY / CONDITIONAL / READY

## 1. Core Infrastructure ✅ / ⚠️ / ❌
[List checks with emoji status. Show actual values.]

## 2. Agent Configuration
...

## 3. Critical Gaps (Priority Ordered)
| # | Domain | Gap | Severity | Action Required |
|---|---|---|---|---|
| 1 | 5-Integrations | WhatsApp API not configured | 🔴 | Set up Baileys or Cloud API |

## 4. Recommended Next Steps
1. [Immediate action]
2. [Short-term]
3. [Post-launch]
```

## Report Principles

- **Always show real data.** Don't say "disk might be full" — run the command and paste the value.
- **Gap severity is relative to the product's claimed features.** If the product advertises WhatsApp messaging but WhatsApp isn't set up, that's 🔴. If the product is a voice-only agent and video isn't configured, that's ⚪.
- **Include the action for every gap.** Don't just identify problems — tell the user what to install, configure, or fix.
- **Let the user prioritize.** After the report, ask: "Which gap should we tackle first?" Don't assume you know their order of urgency.

## Pitfalls

- **Don't fabricate audit results.** If a command times out, say "timed out — need faster probe" — don't make up a file size or version number.
- **Consider the user's context.** A pre-launch audit for a solo founder in Yaoundé has different blocking criteria than an enterprise deployment. 43 GB free on D: might be fine for a startup; 2.4 GB on C: is always 🔴.
- **The audit itself is not the fix.** Some agents stop at "identified 8 gaps" and ask what to do next. Always end with a concrete next action the user can take.
- **Non-technical users need plain language.** "Config.yaml has no gateway section" → translate to: "The agent can't receive external messages (WhatsApp, Telegram, etc.) because the configuration file doesn't list any communication channels."
- **GODMODE / jailbreak active in config** is a 🔴 blocker for any deployment that interacts with external users. The prefill messages may provide unlimited access to the LLM — this ships to clients in the current state.
- **Model dependency is a 🟡, not 🔴.** A single model is risky but not launch-blocking. Prioritize real blockers (missing integrations, no backup, C: drive full).

## Related Skills

- `startup-operations-planning` — business workstream readiness (marketing, sales, lead gen)
- `windows-file-organization` — disk space cleanup and file management
- `windows-app-not-opening` — per-app troubleshooting
- `website-critical-audit` — website/product UI readiness (separate from infra audit)
- `whatsapp-crm-setup` — configuring WhatsApp Business API
- `facebook-graph-api-token-debug` — debugging Facebook/Instagram Graph API tokens
