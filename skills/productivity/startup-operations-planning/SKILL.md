---
name: startup-operations-planning
description: "Build comprehensive operations maps for early-stage startups — identify all workstreams (product, sales, marketing, content, brand, admin, lead gen), define daily/ weekly rhythms, prioritize by revenue impact, and document everything in structured references. For non-technical founders who need the full picture of running their business."
version: 1.0.0
author: giantect
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [startup, operations, planning, workflow, business, founder]
    related_skills: [writing-plans, b2b-marketing-copy, ai-product-market-research, website-critical-audit, ai-coding-tool-prompting]
---

# Startup Operations Planning

## When to Use

- User says "list everything we need to do" — asking for the full operations picture
- User mentions multiple workstreams (product, sales, video, scraping, social media) and wants them organized
- User is a non-technical founder with many moving parts and no clear process
- Session involves the Giantect Empire context specifically (Cameroon-based AI startup, $50 budget, founder-age-sensitive)
- User has an existing product but no systematic operations plan

## The "Market-First" Strategy (User Preference)
- **Constraint:** User works 8 AM - 6 PM with a 2-hour midday break. 
- **Preference:** Prioritize direct face-to-face B2B outreach over digital-only ads.
- **Workflow:** 
    1. **Asynchronous Preparation (Agent):** Prepare scripts, value sheets, and lead lists while user is at work.
    2. **Execution Window (User, Midday Break):** User uses the 2-hour break for high-leverage sales calls/visits.
    3. **"Trust-First" Acquisition:** Use domain + landing page for credibility, print materials (prospectus/flyers) for hand-offs, and very limited, controlled social media video ads (6,000 FCFA test budget) to generate warm leads.
- **Rules:** Never suggest Google Ads for low-budget ($50/25k FCFA) startup market penetration in Cameroon; focus on face-to-face networking and warm outreach.
- **Pitfall:** Avoid "Over-Engineering" (e.g., renting servers/VPS for static sites) when free alternatives (Vercel) exist; allocate every franc to tangible growth (ads, printing, data).


Every early-stage startup (especially software + service hybrid) breaks into these 8 workstreams. Use this as the default structure:

### 1. Product
- Core product development & deployment
- Subscription/pricing system
- Payment integration (Orange Money, MTN MoMo, Stripe for African markets)
- Client onboarding flow (trial → paid)
- Multi-channel deployment (WhatsApp, Telegram, SMS, CLI)
- Mobile deployment (Termux on Android — key for African market)

### 2. Lead Generation / Scraping
- Web scraping (Google Maps, directories, website contact pages)
- Lead database with dedup
- Lead scoring (hot/warm/cold based on contact info completeness)
- CRM / pipeline tracking
- WhatsApp cold messaging (20/hr limit — platform cap)
- Email cold outreach (50/day limit)
- DM automation (LinkedIn, Facebook, Instagram)
- Follow-up sequences (day 1, 3, 7, 14)

### 3. Video Production
- Product demo videos (60s, use-case per industry)
- Client testimonials
- Tutorial series
- Behind-the-scenes / founder story
- Post schedule (1 video every 2 days)
- Batch production (templates, scripts, 10 at a time)

### 4. Social Media Optimization
- Platform-specific audits: Facebook, Instagram, LinkedIn, TikTok, WhatsApp/Telegram
- Post frequency per platform
- DM automation for lead capture
- Ad budget allocation (start with small budgets — 5,000 FCFA)
- Profile optimization (consistent bio, link, profile pic across all)

### 5. Content Marketing
- Blog: 1 article/week on website
- Newsletter for unconverted leads
- Lead magnets (downloadable guides, case studies)
- Repurpose: one video → blog post → social posts → email

### 6. Sales & Pipeline
- Pipeline stages: Cold → Contacted → Warm → Demo → Negotiation → Closed → Onboarded
- Sales scripts (per channel: WhatsApp, email, in-person)
- Objection handling scripts (specific to market: "C'est trop cher", "Je verrai plus tard")
- Demo booking flow (Calendly or manual)
- Monthly targets: 10 demos booked, 3 closed

### 7. Brand & Design
- Website fixes and rebranding
- Brand guidelines document
- Sales deck (PowerPoint/Canva)
- One-pager PDF for WhatsApp sharing
- Social media templates (post, story, reel cover)
- Business cards (digital + print)
- Consistent profile pictures across all platforms

### 8. Back-Office / Admin
- Business registration (legal entity)
- Business bank account / mobile money account
- Invoicing system
- Terms of service + privacy policy on website
- Weekly financial tracking (money in/out, MRR)
- Weekly review (Sunday: review all 8 workstreams, plan next week)

## The Daily Rhythm Template

When the user has too many things to do and no structure, provide a daily time-block:

| Time | Activity |
|---|---|
| 8:00-8:30 | Review leads, approve outreach list |
| 8:30-10:00 | Outreach wave 1 (DMs + emails) |
| 10:00-11:00 | Respond to inbound messages |
| 11:00-13:00 | Product building / core work |
| 13:00-14:00 | Break |
| 14:00-15:00 | Video / content production |
| 15:00-16:00 | Outreach wave 2 |
| 16:00-17:00 | Social media posting |
| 17:00-18:00 | Pipeline review + next-day plan |

Customize based on the user's specific constraints (they may work from phone, have limited data, share a device).

### Constrained Schedule Variant (<=2h/day)

Some founders have extreme time constraints (4h sleep, full-time school/work, only 60-120 min/day for the startup). For these users, use a **weekly rotation** instead of a daily schedule:

Each day gets ONE focus area for the full 60-120 min. Rotate across the week so all workstreams get covered:

| Day | Focus Area | Time |
|---|---|---|
| Monday | SALES — WhatsApp outreach, follow-ups, pipeline update | 90 min |
| Tuesday | PRODUCT — build, fix bugs, deploy | 90 min |
| Wednesday | CONTENT — 1 video + 1 blog post | 90 min |
| Thursday | SOCIAL + BRAND — post content, design templates, engage | 90 min |
| Friday | LEADS — scrape, clean, enrich, export | 90 min |
| Saturday | ADMIN — finances, catch-up, plan next week | 90 min |
| Sunday | REST | 0 |

**Split the time into 2-3 task blocks per day** (e.g. 45+30+15 or 30+30+30). Never more than 3 tasks in a single day — the founder will skip the schedule if it feels overwhelming.

**Output preference:** When the user asks for a timetable/schedule, produce an `.xlsx` file on their Desktop rather than markdown or text. They need to edit, print, and share it. Use Node.js with the `excel4node` library (available globally at `C:\Users\CLINIC\AppData\Roaming\npm\node_modules\excel4node`). The workbook should include:
- Sheet 1: The weekly timetable with day + time + task columns
- Sheet 2: The 8 workstreams master list 
- Sheet 3: A lead pipeline tracker (pre-filled column headers, 20 empty rows)
- Sheet 4: A monthly financial tracker (pre-filled with key metrics and goals)

Always clean up the builder `.js` script after generating the `.xlsx` file.

## Prioritization Rule

When the user asks "what should I do first?" apply this order:

1. **Makes money fastest** — lead gen, sales outreach, closing clients
2. **Prevents losing money** — invoicing, payment setup, subscription enforcement
3. **Builds future pipeline** — content marketing, social media, video
4. **Brand & polish** — website fixes, design consistency
5. **Back-office** — legal, bank, admin

## The Agent Army Pattern

For AI founders building autonomous agent systems, the standard agent team is:

| Agent | Role |
|---|---|
| SCRAPER | Web scraping & lead collection |
| NEXUS | Sales outreach (DMs, emails, calls) |
| FORGE | Product development & coding |
| SENTINEL | Operations & client delivery |
| AURA | Brand & design |

Each agent = a specialized TCHUEKAM instance with focused tools and instructions. This is not a separate product — it's how you organize your AI workforce.

## Writing the Map

1. **Listen first.** Ask what the user already has (product? clients? website? content?). Don't assume.
2. **Map against the 8 workstreams.** Identify which are active, which are missing entirely.
3. **Surface hidden workstreams.** Non-technical founders often don't think about legal, invoicing, or pipeline tracking. Name them explicitly.
4. **Provide the daily rhythm** if they ask for a schedule.
5. **End with next-action clarity.** Don't leave them with a wall of text — ask "which workstream should we tackle first?"

## Pitfalls

- **Don't overwhelm.** An 8-workstream plan is information, not action. After presenting it, immediately guide to the highest-priority next step.
- **Don't assume they can do everything.** Early founders usually can execute 1-2 workstreams well per day. The map shows the universe — the conversation should narrow to one focus area.
- **African market specifics:** Mobile money (Orange Money, MTN MoMo) is the primary payment method, not cards. Mobile-first is not optional. French + English bilingual content is expected in Cameroon. WhatsApp is the dominant business communication channel.
- **$50 budget reality.** Every recommendation must be achievable with minimal capital. Recommend free tiers, open-source tools, manual processes before automation.
- **The founder may be young.** Giantect Empire founder is 18. Don't assume business maturity. Some legal/administrative gaps exist — flag them neutrally without judgment.
- **B2B Strategy:** Prioritize direct, door-to-door (business-to-business) sales over digital ads. Digital ads should be a low-budget experiment ("digital recon") to generate inbound interest, not the primary sales channel. Trust-first acquisition (face-to-face) is the highest conversion channel for AI tools.

## Related Skills

- `b2b-marketing-copy` — writing sales copy for the outreach workstream
- `ai-product-market-research` — competitive analysis to inform positioning
- `website-critical-audit` — auditing the website as part of brand workstream
- `ai-coding-tool-prompting` — writing prompts for Antigravity/Codex to build tools in the lead gen and product workstreams
- `whatsapp-crm-setup` — configuring WhatsApp for the sales workstream

## Reference Files

- `references/giantect-empire-master-operations-2026-05-29.md` — real-world 8-workstream operations map for Giantect Empire, including agent army architecture, daily rhythm, and prioritization.
