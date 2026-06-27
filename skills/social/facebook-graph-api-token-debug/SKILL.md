---
name: facebook-graph-api-token-debug
category: social
description: Debug Facebook/Meta Graph API access tokens — test validity, check permissions, list managed pages, extract page tokens, and diagnose posting/API capability for any FB token.
trigger: User provides a Facebook access token and asks what it can do, whether it works, or why it won't post.
---

# Facebook Graph API Token Debug

Debug what a Facebook access token can and cannot do.

## Triggers
- User pastes an FB token and asks "can I use this?"
- User asks why a token won't post or access something
- User needs to know what permissions a token has
- User wants to extract a page token from their user token

## Workflow

### 1. Quick Validity Check

```bash
curl -s --max-time 8 -G "https://graph.facebook.com/v22.0/me" \
  --data-urlencode "fields=id,name" \
  --data-urlencode "access_token=$TOKEN"
```

Expected success: `{"id":"...","name":"..."}`
Expected fail: `{"error":{"code":190,...}}` — expired or invalid

### 2. Check All Permissions

```python
import requests
r = requests.get("https://graph.facebook.com/v22.0/me/permissions",
    params={"access_token": token}, timeout=10)
```

Look for these key permissions:
- `pages_manage_posts` — REQUIRED to post to a page feed
- `publish_to_groups` — REQUIRED to post to groups
- `publish_to_flow` — REQUIRED to post to personal timeline
- `pages_read_engagement` — read page insights
- `ads_management` — manage ads

### 3. List Managed Pages

New FB API requires `?type=page` parameter:

```bash
curl -s -G "https://graph.facebook.com/v22.0/me/accounts?type=page" \
  --data-urlencode "access_token=$TOKEN"
```

Returns: `{data: [{name, id, access_token, tasks, category}]}`

**Critical:** The `tasks` array shows what the page token can do:
- `CREATE_CONTENT` — can create posts
- `MANAGE` — admin level
- `MODERATE` — moderate comments
- `ADVERTISE` — run ads

### 4. Test Posting

```python
r = requests.post(f"https://graph.facebook.com/v22.0/{page_id}/feed",
    params={"message": "Test", "access_token": token}, timeout=10)
```

**Common error: `(#200) requires both pages_read_engagement and pages_manage_posts`**
→ Token was generated without `pages_manage_posts` permission. Need a new token.

### 5. Interpret Common Error Codes

| Code | Meaning |
|------|---------|
| `190` | Invalid/expired OAuth token |
| `190` + `2069032` | User token used where page token required (new Pages experience) |
| `200` | Missing permission — check which one |
| `100` | Bad request (missing param) |

## Permission Requirements Summary

| Action | Required Permission |
|--------|-------------------|
| Read profile | `public_profile` |
| Post to personal timeline | `publish_to_flow` |
| Post to group | `publish_to_groups` |
| Post to page feed (text) | `pages_manage_posts` + `pages_read_engagement` |
| Post video to page | `publish_video` (separate permission — DOES NOT require `pages_manage_posts`) |
| Manage fundraisers | `manage_fundraisers` |
| WhatsApp Business | `whatsapp_business_management` + `whatsapp_business_messaging` |
| Read page insights | `pages_read_engagement` |
| Run ads | `ads_management` |
| Read/manage messages | `pages_manage_metadata` |

## Pitfalls

- **Python requests vs curl**: On this user's machine, Python `requests.get()` to Graph API times out (network proxy/venv issue). Always use `curl` via `terminal()` for reliable API calls.
- **Old vs new Pages experience**: New FB Pages API requires `?type=page` on the accounts endpoint. Without it you get empty data or error 190/2069032.
- **Token truncation**: When copying from terminal, long tokens may be truncated. Always verify token length (~200 chars typical) before testing.
- **Rate limits**: FB Graph API has tight rate limits for user tokens. Space out calls.
- **Page token vs user token**: Even as page admin, your user token cannot post. You must use the page-specific token from `/me/accounts?type=page`.
- **Expiration**: Short-lived tokens expire in 1-2 hours. Long-lived tokens in 60 days. `EAA` prefix = app-scoped token.

## Verification

After any test, show the user a clear YES/NO answer:
- "This token CAN post to your page Mbowazap" ✓
- "This token CANNOT post — missing `pages_manage_posts`" ✗
- Then tell them exactly how to fix it (Graph API Explorer → add missing permission → regenerate)
