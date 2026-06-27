# Baileys-Based WhatsApp Bot Architecture (LuckyTechHub / MboWazap)

Reference for the LuckyTechHub-Bot project at `~/Desktop/LuckyTechHub-Bot-main/`.

## Stack

- **Baileys v6.7.21** (`@whiskeysockets/baileys`) — WhatsApp Web multi-device protocol (reverse-engineered, not official API)
- **Node.js >=20** (uses `--expose-gc` for memory management)
- **ESM-to-CJS bridge** (preload.js): Baileys v6.7+ ships as ESM-only; `preload.js` dynamic-imports it, monkeypatches Node's `require.cache`, then boots the real entry point (`index.js`)
- **No database** — flat JSON files for all state (sessions, memories, configs, reply counts)
- **Groq API** (Llama 3.3 70B) + DeepSeek + Gemini 2.0 Flash for AI and transcription
- **Tally.so** for order/lead forms (webhook-pull via API key)

## Project Structure

```
LuckyTechHub-Bot-main/
├── preload.js           — ESM-to-CJS bridge, boots baileys
├── index.js             — Core engine: multi-session, reconnect, health check HTTP server, watchdog
├── main.js              — Message router: 70+ .-prefixed commands in giant switch(true)
├── settings.js          — Config: API keys, bot personality (Davila AI), pricing, business info
├── config.js            — Third-party API endpoints and keys
├── flows/
│   ├── index.js         — Sales funnel (NEW → AWAITING_Q1/Q2 → TALLY_SENT → AWAITING_NAME → CLOSED)
│   └── intentDetector.js
├── commands/            — ~100 individual command files
├── lib/
│   ├── autoReplyManager.js  — Always-on AI receptionist: voice transcription, image vision, deal classifier
│   ├── sessionManager.js    — Multi-tenant socket map (phoneNumber → Baileys socket)
│   ├── aiProvider.js        — Wraps Groq / DeepSeek / Gemini API calls
│   ├── securityManager.js   — Rate limiting, hourly caps
│   ├── healthCheck.js       — HTTP health endpoint + uptime tracking
│   └── ...                  — Antilink, antibadword, sticker helpers, etc.
├── data/
│   ├── sessions/{number}/   — Per-business auth credentials (creds.json + keys)
│   ├── memory/{number}.json — Per-contact AI conversation memory (last 20 msgs)
│   └── config/{number}.json — Per-business custom system prompts + knowledge base
├── wacrm/               — Next.js + Supabase CRM dashboard (separate sub-project)
└── baileys_store.json   — Legacy Baileys store (may be stale)
```

## Key Architecture Decisions

### Multi-Tenancy

Each WhatsApp business number gets:
- Its own auth folder (`data/sessions/{phoneNumber}/`)
- Its own Baileys socket instance (stored in `sessionManager` Map)
- Business config override at `data/config/{phoneNumber}.json` (custom system prompt + knowledge base)
- Boot restores all previous sessions from disk

### Anti-Ban System

Built into `main.js`:

1. **Send pacing**: 5-second minimum gap between messages to non-owner recipients (bypasses `sendMessage`)
2. **Loop prevention**: Tracks bot-generated message IDs (last 2000), ignores replies to own messages
3. **Double-reply protection**: Max 2 replies per incoming message ID (persisted to `data/replyCounts.json`)
4. **Message dedup**: `processedIds` Set capped at 1000 entries
5. **Reconnect backoff**: Exponential (2s base → 60s max), stops after 5 attempts in 10-minute sliding window
6. **Session wipe**: Code 401/loggedOut = immediately delete session folder
7. **Conflict detection**: Code 440 = terminate, do not reconnect
8. **RAM watchdog**: Auto-restart if RSS exceeds 450MB (checked every 30s)
9. **GC**: Forces garbage collection every 60s (`--expose-gc` must be enabled)
10. **policyGuard**: Compliance mode that disables fake presence and privacy-bypass features

### Auto-Reply Engine (autoReplyManager.js)

The always-on AI receptionist handles every non-command private message:

1. Transcribes voice notes via **Groq Whisper** (`whisper-large-v3`)
2. Reads images via **Groq Vision** (llama-3.2-11b-vision-preview) → **Gemini 2.0 Flash** fallback
3. Maintains per-contact memory on disk (`data/memory/{number}.json`)
4. Human typing delay: 15–120 seconds (randomized)
5. **Deal Classifier**: AI detects "hot leads" (ready to pay) → pins chat, pauses AI 10min, notifies owner
6. **Fact Extractor**: AI extracts name/business/location/pack interest → builds long-term profile
7. **Security**: 20 AI replies/hour max per contact (configurable)

### Sales Funnel (flows/index.js)

Structured flow for new contacts:

```
NEW → Business Type buttons (Salon/Clinic/Large)
   → Objective list (Faster replies/Appointments/Scaled growth)
   → Tally form link sent
   → Name capture
   → Closing (Ready? / Questions?)
   → Commitment confirmation (pack + price)
   → CLOSED
```

- Background scanner runs every 60s: sends Tally reminder after 10min inactivity
- "Davila Fallback" — AI conversation for free-text responses outside flow buttons

## Bot Personality (settings.js)

The `botPersonality` field contains a complete Davila AI prompt:
- Identity: personal assistant to M. Tchuekam, founder of Tchuek-Tech, Yaoundé
- Language: auto-detect French (formal "vous") or English
- Tone calibration: cold → warm → solution-oriented based on user signals
- Response length: 1 line for greetings, structured for pricing, empathetic for complaints
- Sales persuasion: "influence through clarity, not pressure"
- Pricing: Starter 25k/mo, Business 75k/mo, Elite 350k/mo
- Payment: Orange Money 659248952 (name: TchueKam Loic Rostand)
- Formatting: WhatsApp ChatGPT style (*bold* pack names, _italic_ details, • bullet lists)

## Commands (~100)

| Category | Examples |
|----------|---------|
| AI | .ai, .gpt, .gemini, .llama3, .aidiag, .imagine (image gen) |
| Media Download | .play (audio), .song (MP3), .video (MP4), .tiktok, .instagram, .facebook, .spotify |
| Stickers | .sticker, .attp, .take, .crop, .tg (Telegram stickers), .emojimix |
| Group Admin | .ban, .unban, .kick, .promote, .demote, .mute, .unmute, .warn, .tagall, .hidetag |
| Moderation | .antilink, .antitag, .antibadword, .antidelete, .antiviewonce, .anticall, .pmblocker |
| Fun/Games | .joke, .meme, .quote, .fact, .dare, .truth, .8ball, .flirt, .ttt, .hangman, .trivia |
| Text Effects | .tts, .translate, .metallic, .ice, .neon, .fire, .glitch (13 textmaker styles) |
| Owner | .mode (public/private), .autoread, .autotyping, .autostatus, .setpp, .sudo, .update, .kill |
| Info | .weather, .news, .countryinfo, .define, .bible, .epl (football), .git |

## Deployment

- **Entry**: `node --no-warnings --expose-gc --max-old-space-size=400 preload.js`
- **Deployable**: Dockerfile included, Railway/nixpacks support
- **Health**: HTTP server on configurable port (returns uptime + active sessions)
- **First connect**: Pairing code mode (`--pairing-code` flag) or QR scan via `temp_qr` ephemeral session

## Baileys vs. Official API vs. web.js

| Method | Ban Risk | Cost | Setup Time | Reliability |
|--------|----------|------|------------|-------------|
| **Baileys** (this project) | HIGH — reverse-engineered protocol, frequent detection | Free | 10 min | Medium — breaks when Meta updates proto |
| **whatsapp-web.js** | MODERATE — automates real browser DOM | Free | 15 min | Medium — browser-dependent |
| **WhatsApp Cloud API** | NONE — official Meta API | Free tier (1000 convos/mo) then ~$0.005/msg | 1-7 days (verification) | High |
| **BSP (360Dialog/WATI)** | NONE — official | ~$5/mo base + per-message | 1-7 days | High |

**Key insight**: The bot's anti-ban measures (pacing, loop detection, reconnection backoff) reduce but do not eliminate Baileys ban risk. For production use with real clients, migrate to the official Cloud API.
