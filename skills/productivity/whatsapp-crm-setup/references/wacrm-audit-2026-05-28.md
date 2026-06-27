# wacrm Audit — 28 May 2026

## Source
- **Repo**: github.com/ArnasDon/wacrm
- **Local path**: `C:\Users\CLINIC\Desktop\wacrm`
- **Author**: Arnas Donauskas
- **License**: MIT
- **Version**: 0.2.1
- **Stack**: Next.js 16 + Supabase + Tailwind v4 + Meta API v21.0

## Architecture Overview

The app uses:
- **Supabase Auth** for user login/session
- **Supabase RLS + Service Role** for cross-user data checks
- **Encrypted token storage** (AES-256-GCM) for WhatsApp credentials
- **Meta Cloud API** v21.0 (`graph.facebook.com/v21.0/`)
- **Flow engine** for no-code automations
- **Broadcast engine** for bulk WhatsApp template messages

## Environment Status

| Variable | Value | Status |
|---|---|---|
| NEXT_PUBLIC_SUPABASE_URL | xwwlvwtcrqkkztrltule.supabase.co | ✅ Set |
| NEXT_PUBLIC_SUPABASE_ANON_KEY | eyJhbG...6heA | ✅ Set |
| SUPABASE_SERVICE_ROLE_KEY | eyJhbG...YuRs | ✅ Set |
| ENCRYPTION_KEY | 67df2cc2...33daa | ✅ Set |
| META_APP_SECRET | your-meta-app-secret | ❌ **Placeholder** |
| NEXT_PUBLIC_SITE_URL | https://crm.example.com | ❌ **Placeholder** |
| AUTOMATION_CRON_SECRET | (not set) | ❌ **Missing** |

## Key API Routes

| Route | Method | Purpose |
|---|---|---|
| `/api/whatsapp/webhook` | GET | Webhook verification (Meta → your app) |
| `/api/whatsapp/webhook` | POST | Receive inbound messages |
| `/api/whatsapp/config` | GET | Test API connection / check health |
| `/api/whatsapp/config` | POST | Save encrypted WhatsApp credentials |
| `/api/whatsapp/config` | DELETE | Reset configuration |
| `/api/whatsapp/send` | POST | Send messages |
| `/api/whatsapp/templates/sync` | POST | Sync approved Meta templates |
| `/api/whatsapp/media/[mediaId]` | GET | Retrieve media from Meta |
| `/api/automations/engine` | POST | Execute automation triggers |
| `/api/automations/cron` | GET | Pending wait-step drain |

## WhatsApp Flow

1. Meta sends POST to `/api/whatsapp/webhook` on inbound message
2. Webhook handler looks up `whatsapp_config` by `phone_number_id` incoming (uses `.single()` — one phone = one user)
3. Decrypts stored `access_token` with `ENCRYPTION_KEY`
4. Routes message through automations/flows engine
5. Sends response via Meta API with decrypted token

## Next Steps for Loic

1. Get a **long-lived Facebook/Meta access token** with `whatsapp_business_messaging` scope
2. Get **Phone Number ID** from Meta Developer Dashboard
3. Fill **META_APP_SECRET** in `.env.local`
4. Deploy to Hostinger Managed Node.js (one-click from their panel)
5. Set up webhook URL in Meta Developer Dashboard
6. Test with `POST /api/whatsapp/config` then send a test message
