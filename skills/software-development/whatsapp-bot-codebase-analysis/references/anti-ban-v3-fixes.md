# Anti-Ban v3 — 5 Critical Fixes

Applied to a Baileys multi-tenant WhatsApp bot. Each fix targets a specific vulnerability that WhatsApp/Meta uses to detect automation.

## Fix 1 — Persist processedIds to Disk

**Problem**: `processedIds` Set lives in memory. On bot restart, it's empty. WhatsApp replays undelivered messages on reconnect, and the bot re-responds to everything — triggering rate/duplicate detection.

**Solution**: Save to `data/processedIds.json` on a 5-minute interval. Load on boot.

```js
const PROCESSED_IDS_FILE = './data/processedIds.json';
// Load on boot
try {
    if (fs.existsSync(PROCESSED_IDS_FILE)) {
        const saved = JSON.parse(fs.readFileSync(PROCESSED_IDS_FILE, 'utf8'));
        if (Array.isArray(saved)) saved.forEach(id => processedIds.add(id));
    }
} catch (e) {}
// Persist every 5 minutes
setInterval(() => {
    const arr = Array.from(processedIds).slice(-2000);
    fs.writeFileSync(PROCESSED_IDS_FILE, JSON.stringify(arr), 'utf8');
}, 300_000);
```

## Fix 2 — Content Fingerprint Dedup

**Problem**: Same sender sends identical text twice within short window (retry, network glitch, user rage-tapping). Bot processes both.

**Solution**: Hash `senderId + bodyText.toLowerCase()`. If same hash seen within 60s, drop the message.

```js
global._contentFingerprints = global._contentFingerprints || new Map();
const fpKey = `${senderId}:${bodyText.toLowerCase()}`;
const fpLast = global._contentFingerprints.get(fpKey);
if (fpLast && (Date.now() - fpLast) < 60_000) return;
global._contentFingerprints.set(fpKey, Date.now());
```

## Fix 3 — Daily Message Cap per Sender

**Problem**: No upper bound on messages per sender per day. Automated or aggressive users can trigger 500+ messages, which WhatsApp flags.

**Solution**: Track `senderId + date` in a Map. Cap at 30 commands/day per sender. Silently absorb beyond that.

```js
global._dailyCounts = global._dailyCounts || new Map();
const dailyKey = `${senderId}:${new Date().toDateString()}`;
const count = (global._dailyCounts.get(dailyKey) || 0) + 1;
global._dailyCounts.set(dailyKey, count);
if (count > 30) return;
```

## Fix 4 — Quiet Hours

**Problem**: Bot responds at 3 AM. No human does this consistently. WhatsApp logs activity timestamps and flags 24/7 accounts.

**Solution**: Silently absorb all non-owner messages between 11PM and 6AM (Cameroon UTC+1).

```js
const nowHour = new Date().getHours();
if (nowHour >= 23 || nowHour < 6 && !message.key.fromMe) return;
```

## Fix 5 — Human-like Presence Cycling

**Problem**: Sending `sendPresenceUpdate('available')` every 30 seconds = always-online. WhatsApp sees this and flags as automation.

**Solution**: Alternate between online (3–8 min) and offline (5–15 min) with random intervals.

```js
let cycleOnline = true;
setInterval(async () => {
    cycleOnline = !cycleOnline;
    if (cycleOnline) await sock.sendPresenceUpdate('available');
}, cycleOnline
    ? (180_000 + Math.floor(Math.random() * 300_000))
    : (300_000 + Math.floor(Math.random() * 600_000)));
```

## Where to Inject

| Fix | File | Insert Point |
|-----|------|-------------|
| Fix 1 | `main.js` | Near `processedIds = new Set()` at top of file |
| Fix 2 | `main.js` | Inside `handleMessages()`, after msgId check, before double-reply check |
| Fix 3 | `main.js` | Same as Fix 2, before business logic |
| Fix 4 | `main.js` | Same as Fix 2-3, before reply routing |
| Fix 5 | `index.js` | Replace the heartbeat interval inside `connection.update` → 'open' handler |
| Cap + Quiet | `lib/autoReplyManager.js` | Inside `handleAutoReply()`, at the very top before any processing |

## Daily Cap Values Used

| Layer | Cap | Scope |
|-------|-----|-------|
| Commands (main.js) | 30/day | Per sender JID |
| Auto-replies (autoReplyManager.js) | 20/day | Per sender JID |

## Content Hash Eviction

Keep Map size ≤ 500 entries. Evict oldest entry when exceeded to prevent memory leak.
