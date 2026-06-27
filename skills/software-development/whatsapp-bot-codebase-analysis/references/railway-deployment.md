# Railway Deployment — Baileys WhatsApp Bot

## Prerequisites
- GitHub account
- Railway account (railway.app)
- Bot code already on your machine with Dockerfile and nixpacks.toml

## Step 1 — Push to GitHub
```bash
cd "/path/to/bot-folder"
git init
git add .
git commit -m "Initial commit"
# Create repo on github.com/new, then:
git remote add origin https://github.com/YOUR_USER/YOUR_REPO.git
git branch -M main
git push -u origin main
```

## Step 2 — Deploy on Railway
1. Go to https://railway.app/dashboard → **New Project**
2. Click **Deploy from GitHub repo** → select the repo you pushed
3. Railway auto-detects Node.js + nixpacks config → builds automatically (~3 min)

## Step 3 — Set Environment Variables
Go to the **Variables** tab and add:

| Variable | Value | Required |
|----------|-------|----------|
| `GROQ_API_KEY` | Your Groq API key | Yes |
| `TCHUEKAM_API_KEY` | Your Gemini API key | Yes (if using Gemini) |
| `DEEPSEEK_API_KEY` | Your DeepSeek API key | Yes (if using DeepSeek) |
| `OWNER_NUMBER` | e.g. `237653683174` | Yes |
| `PORT` | `8080` | Yes (Railway default) |
| `GIPHY_API_KEY` | For GIF features | Optional |

Even better: define all variables in `.env` locally, then use Railway's "Import from .env" bulk upload.

## Step 4 — Generate Pairing Code
1. Open Railway **Logs** tab
2. Look for: `[pairing] Pairing code for 237XXXX: XXXX-XXXX`
3. On your phone: WhatsApp → Linked Devices → Link a Device → enter the code
4. Wait for: `WhatsApp session connected successfully`

## Step 5 — Verify
- Check logs for: "WhatsApp session connected successfully"
- Send `.menu` or `.alive` to the bot from your WhatsApp
- Confirm bot responds

## Common Issues

| Problem | Fix |
|---------|-----|
| Build fails on npm install | Add `--legacy-peer-deps` to install script in package.json |
| Bot connects but doesn't respond | Check logs for "Error in messages.upsert" — may be Baileys ESM issue; ensure preload.js is the entry point |
| Pairing code doesn't appear | Increase `PAIRING_INIT_BUFFER_MS` in index.js from 3000 to 10000 |
| Session expires after deploy | Normal — just re-pair. Consider session persistence with Railway Volumes (experimental) |
| High memory usage | Verify `--max-old-space-size=400` is in the start command |

## Dockerfile Reference
The existing Dockerfile (node:20-slim) is suitable for Railway. Key points:
- Exposes port 8080 (Railway maps this automatically)
- Uses `node --no-warnings --expose-gc --max-old-space-size=400 preload.js` as CMD
- Pre-creates runtime directories: `data/sessions`, `data/config`, `tmp/pair_sessions`, `tmp`, `scratch`

## Notes
- Railway free tier supports 500 hours/month and 1 CPU core — sufficient for a single WhatsApp bot
- Pairing code authentication means the bot runs independently of your phone once paired (unlike QR)
- Session credentials stored in `data/sessions/{number}/` — lost on restart unless using Railway Volumes
