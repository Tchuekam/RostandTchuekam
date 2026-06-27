# Facebook Token Debugging Recipe (Session 2026-05-27)

## Tokens Tested

3 tokens from user `Loic TchueKam` (FB ID: 122095782045351834).
All started with `EAA` (app-scoped, long-lived). All had different permission sets.

### Token 1 & 2: Business/Ads tokens
- **Permissions**: `pages_show_list`, `ads_management`, `business_management`, `leads_retrieval`, `pages_read_engagement`, `pages_manage_metadata`, `pages_manage_ads`, `catalog_management`, `public_profile`
- **CAN**: read profile, manage pages, run ads, read leads, moderate comments, message as page
- **CANNOT**: post text anywhere (missing `pages_manage_posts` and `publish_to_groups`)

### Token 3: Added video + fundraiser + WhatsApp
- **Permissions**: All of above PLUS `publish_video`, `manage_fundraisers`, `whatsapp_business_management`, `whatsapp_business_messaging`, `email`
- **CAN**: read profile, manage pages, run ads, publish video (untested — network timeout)
- **CANNOT**: post text (still missing `pages_manage_posts` and `publish_to_groups`)

## Page Found
- **Mbowazap** (Software Company) — Page ID: 1171093259412310
- Tasks available: MODERATE, MESSAGING, ANALYZE, ADVERTISE, CREATE_CONTENT, MANAGE
- Page token obtained via `GET /me/accounts?type=page` (new Pages experience)

## Network Quirk
Python `requests.get()` in the Hermes venv (`D:\TCHUEKAM-AGENT\hermes-agent\app\venv`) times out connecting to `graph.facebook.com`. Curl from `terminal()` (git-bash) works fine. Root cause unknown — likely proxy env vars or IPv6 resolution issue in the venv.

**Workaround**: Always use `curl` via `terminal()` for Facebook Graph API calls on this machine.

## Key Takeaways
1. Facebook has split permissions granularly. Even as admin with MANAGE/CREATE_CONTENT on a page, you cannot post if the generating user token lacks `pages_manage_posts`.
2. The `publish_video` permission is **separate** from `pages_manage_posts` — a token can post video but not text.
3. New Pages experience requires `?type=page` on the accounts endpoint, else error 190/2069032.
4. User has no pages other than Mbowazap. No groups found.
