---
name: whatsapp-crm-setup
title: WhatsApp CRM / Bot Project Setup
description: Set up, audit, and deploy WhatsApp-based CRM templates and bot projects using Meta Business API + Supabase. Covers wacrm, HolyZap Mbowazap, and similar self-hosted WhatsApp solutions.
category: productivity
tags:
  - whatsapp
  - crm
  - meta-api
  - supabase
  - nextjs
  - self-hosted
trigger: user wants to set up a WhatsApp CRM, deploy wacrm, configure WhatsApp Business API, get Meta access tokens, or integrate WhatsApp with a project.
---

# WhatsApp CRM / Bot Project Setup

## Architecture Pattern

These projects (wacrm, HolyZap, Mbowazap) all follow the same pattern:

```
WhatsApp Business API (Meta)
    ↕ (webhook + REST API)
Next.js App (self-hosted or Hostinger)
    ↕ (Supabase SDK)
Supabase (Postgres + Auth + RLS)
```

### Key Components

| Component | Purpose |
|---|---|
| **WhatsApp Business Account** | Meta-level account that owns phone numbers |
| **Phone Number ID** | Numeric ID of your WhatsApp number in Meta's system |
| **Access Token** | Bearer token for API calls (needs `whatsapp_business_messaging` scope) |
| **Verify Token** | Arbitrary string you set; Meta sends it back on webhook setup for verification |
| **WABA ID** | WhatsApp Business Account ID |
| **Webhook URL** | Endpoint Meta calls on inbound messages (e.g., `https://your-domain.com/api/whatsapp/webhook`) |
| **META_APP_SECRET** | Used to verify webhook HMAC-SHA256 signatures |

## Prerequisites

### Required Meta Assets

You need:
1. A **Meta Business Account** (business.facebook.com)
2. A **WhatsApp Business Account** linked to it
3. A **Meta App** created at developers.facebook.com with WhatsApp product added
4. A **Phone Number** (cannot be already registered with WhatsApp — must be fresh or migrated)

### Required Environment Variables (wacrm template)

```env
# REQUIRED
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<anon-key>
SUPABASE_SERVICE_ROLE_KEY=<service-role-key>

# Encryption for stored WhatsApp tokens (AES-256-GCM, 64 hex chars)
ENCRYPTION_KEY=<generate: node -e "console.log(require('crypto').randomBytes(32).toString('hex'))">

# Meta App Secret — verify webhook signatures
META_APP_SECRET=<from Meta Developer App Settings>

# OPTIONAL
NEXT_PUBLIC_SITE_URL=https://your-domain.com
AUTOMATION_CRON_SECRET=<generate: openssl rand -hex 32>
```

## Workflow

### 1. Audit existing project

When user says "regarde le dossier wacrm" or similar:

1. Check `.env.local` — what's filled vs missing
2. Check `README.md` — understand the project purpose
3. Check `package.json` — verify stack (Next.js version, deps)
4. Check `src/app/api/whatsapp/` — understand the webhook and config API routes
5. Check `src/lib/whatsapp/meta-api.ts` — verify Meta API version and endpoint

**wacrm specifics:**
- Stack: Next.js 16 + Supabase + Tailwind v4 + Meta API v21.0
- WhatsApp tokens are **encrypted at rest** (AES-256-GCM) via `ENCRYPTION_KEY`
- Webhook handler: `src/app/api/whatsapp/webhook/route.ts`
- Config save/verify: `src/app/api/whatsapp/config/route.ts`
- Template from: github.com/ArnasDon/wacrm

### 2. Get Meta access credentials

To obtain the necessary tokens:

1. Go to **developers.facebook.com** → Your App → WhatsApp → API Setup
2. Copy the **Temporary Access Token** (24h expiry — must be extended)
3. Get the **Phone Number ID** from the same page
4. Generate a **Permanent (Long-Lived) Token**:
   - Exchange short-lived token via: `GET /oauth/access_token?grant_type=fb_exchange_token&client_id={app-id}&fb_exchange_token={short-lived-token}`
   - This gives a 60-day token
   - Store it in the app's WhatsApp config (encrypted)

### 3. Configure webhook

1. Set webhook URL to: `https://your-domain.com/api/whatsapp/webhook`
2. Set Verify Token to a secret string you choose
3. Subscribe to: `messages`, `message_deliveries`, `message_reads`

### 4. Test connection

Use the app's built-in config test endpoint:
```
GET /api/whatsapp/config
POST /api/whatsapp/config
  body: { phone_number_id, waba_id?, access_token, verify_token? }
```

## User-Specific Notes for Loic / Giantect

- **Mbowazap Facebook Page ID**: 1171093259412310
- **Current tokens tested**: None have `pages_manage_posts` scope; `publish_video` works on some; `pages_messaging` works
- **Existing tools**: HolyZap CMD.docx (bot blueprint), wacrm (Next.js CRM template)
- **Supabase project**: xwwlvwtcrqkkztrltule.supabase.co (already configured in .env.local)
- **Missing from .env.local**: META_APP_SECRET, AUTOMATION_CRON_SECRET, actual WhatsApp credentials

## References

- `references/wacrm-audit-2026-05-28.md` — Full audit of user's wacrm project (Supabase config, env gaps, Node version)
- `references/baileys-bot-architecture.md` — Complete architecture of LuckyTechHub-Bot (Baileys-based multi-tenant WhatsApp bot), including anti-ban system, sales funnel flows, auto-reply engine, ~100 commands, and comparison of Baileys vs official API vs whatsapp-web.js ban risks

## Pitfalls

- **Phone number already registered**: Meta rejects numbers already attached to WhatsApp (personal or Business). Need a fresh SIM or migrate via Meta's number migration process.
- **Short-lived token expiry**: Temporary tokens from the dev dashboard expire after 24h. Always exchange for a long-lived (60-day) token.
- **Webhook verification fails**: Meta sends a GET request with `hub.verify_token` and `hub.challenge`. If your verify token doesn't match, the webhook setup fails silently. Double-check the env var.
- **Token encryption mismatch**: wacrm encrypts tokens with `ENCRYPTION_KEY` at save. If this key changes between environments (local vs Hostinger), stored tokens become undecryptable — user sees "token_corrupted". Solution: reset config and re-save.
- **phone_number_id already claimed**: wacrm is single-tenant per phone number. Two users cannot bind the same number. The API returns 409 if claimed.
- **Supabase RLS**: The config route uses SUPABASE_SERVICE_ROLE_KEY specifically to check cross-user duplicate phone numbers (bypasses RLS). Normal user queries use the `@supabase/ssr` client with session-based auth.
- **Node version**: wacrm requires Node >= 20.0.0 (Next.js 16 requirement).
- **npm install is heavy**: The project has many deps — `npm install` takes time. Exclude `node_modules/` from file operations and duplication scans.
