---
name: whatsapp-bot-codebase-analysis
description: Deep code analysis of Baileys-based multi-tenant WhatsApp bots — reverse-engineer structure, anti-ban measures, sales funnels, AI pipelines, and security architecture. Read the entire codebase end-to-end, not surface-level.
version: 1.1.0
author: TCHUEKAM
tags: [whatsapp, baileys, anti-ban, code-analysis, reverse-engineering, security]
---

# WhatsApp Bot Codebase Analysis

## When to Use This Skill
- User says "examine this, do not stop until completely examined"
- User hands you a WhatsApp bot folder and wants a full architectural breakdown
- User wants to understand anti-ban measures in an existing bot
- User needs security audit of a Baileys-based WhatsApp automation project

## Core Principle
When the user says "examine it, do not stop", they want **complete penetration** — every file read, every subsystem mapped, nothing surface-level. 100+ commands, 1800-line message routers, sales funnels, CRM integrations — read them all. Do not summarize until you've read the actual code.

## Required Reading Order

### Phase 1 — Surface Scan (5 files)
1. `package.json` — dependencies, scripts, node version
2. `settings.js` / `config.js` — API keys, providers, personalities, pricing, environment variables
3. `preload.js` — any ESM bridge or bootloader
4. `index.js` — session management, connection lifecycle, reconnect logic, event wiring
5. `README.md` — documentation claims vs reality

### Phase 2 — Core Architecture (2 files)
6. `main.js` — the message handler (often 1800+ lines). Read ALL of it in chunks. Maps every command, permission layer, anti-ban wrappers, dedup logic, channel info injection
7. `flows/index.js` — sales funnel / onboarding flow (state machine)

### Phase 3 — Infrastructure Layer
8. `lib/sessionManager.js` — multi-tenant socket management
9. `lib/autoReplyManager.js` — AI auto-reply engine (voice transcription, vision, hot lead detection, memory persistence)
10. `lib/aiProvider.js` — which AI providers, fallback chain, API key management
11. `lib/securityManager.js` — rate limiting, hourly caps, anomaly detection
12. `lib/isBanned.js`, `lib/isAdmin.js`, `lib/isOwner.js` — permission architecture

### Phase 4 — Support Systems
13. `lib/healthCheck.js` — uptime tracking, HTTP health endpoint
14. `lib/policyGuard.js` — compliance/privacy modes
15. `lib/lightweight_store.js` — message caching for getMessage
16. `lib/reactions.js`, `lib/welcome.js`, `lib/antilink.js`, `lib/antibadword.js` — feature modules

### Phase 5 — Commands (spot-check)
17. Sample 20% of `commands/` directory — focus on: `ai.js`, `campaign.js`, `antidelete.js`, `anticall.js`, `menu.js`

### Phase 6 — Extra Modules
18. `wacrm/` — if present, check `package.json` + `CLAUDE.md` for Next.js + Supabase CRM
19. `data/` — session store, memory store, config store patterns

## Key Things to Extract

### Anti-Ban Architecture
- SendMessage wrapper (pacing delay, loop prevention, double-reply protection)
- Presence management (always-online vs cycling)
- Reconnect backoff strategy (exponential, max attempts, conflict handling)
- Session wipe conditions (401, loggedOut, corrupted creds)
- Memory limits (processedIds cap, eviction strategy)
- Daily caps, quiet hours, content dedup

### Multi-Tenant Architecture
- How sessions are isolated per phone number
- Session folder structure: `data/sessions/{number}/`
- Socket registry: `sessionManager.getSocket/setSocket/deleteSocket`
- Boot restoration of previous sessions

### Sales Funnel (if present)
- State machine: NEW → AWAITING_Q1 → AWAITING_Q2 → TALLY_SENT → AWAITING_NAME → AWAITING_CLOSING → COMMITMENT → CLOSED
- Button/interactive message flow
- Background scanner (Tally reminders every 60s)
- Davila AI fallback for free-text

### AI Pipeline
- Provider chain: Groq (primary) → Gemini (vision fallback) → DeepSeek
- Voice: Groq Whisper transcription
- Vision: Groq Vision → Gemini Vision fallback
- Hot lead detection: AI classifies conversation, pins chat, pauses AI 10min, notifies owner
- Fact extraction: AI pulls name/business/location/pack from conversation history
- Memory persistence: `data/memory/{number}.json` with last 20 messages

## Common Security Gaps to Flag
1. `processedIds` not persisted to disk → re-response on restart
2. No content fingerprinting → duplicate command execution
3. No daily volume cap → potential ban from high volume
4. No quiet hours → suspicious 24/7 activity
5. Always-online presence → easily fingerprinted as bot
6. Baileys protocol fingerprinting (WebSocket patterns, missing browser headers)
7. API keys in plaintext in settings.js (not .env)

## Railway Deployment
See `references/railway-deployment.md` for the complete deploy workflow — GitHub push, Railway setup, env vars, pairing code generation.

## Verification After Applying Anti-Ban Fixes
Do a two-layer check:
1. **Syntax**: `node --check` on EVERY modified file (main.js, index.js, any lib/)
2. **Presence**: grep/findstr for each fix's unique variable name or log string
3. **Logic simulation**: use `node -e` to test boundary conditions — quiet hours block [23,0,1,2,3,4,5] and allow [6..22]; daily cap resets on new day (toDateString); presence cycling alternates offline→online
4. **Cross-file integrity**: verify `resetAntiBanState` also persists the cleared state to disk

## Pitfalls
- `main.js` is often 1800+ lines — read in 400-line chunks with offset/limit
- `settings.js` may contain real API keys — note them but do NOT share in output
- The bot may have anti-ban code that's already strong but missing the 5 critical gaps above
- The wacrm subfolder is often a separate project (Next.js) — don't confuse it with the bot core
- Baileys v6.7+ is ESM-only — the preload.js bridge is required to make CJS work
