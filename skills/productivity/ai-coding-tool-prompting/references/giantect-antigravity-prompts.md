# Giantect Empire — Antigravity Prompts (Real Examples)

These are real prompts written for Google Antigravity during Giantect Empire sessions. Use as templates for similar future requests.

---

## Prompt Type 1: Website Fixes (Post-Audit)

**When to use:** The user says "write a prompt for Antigravity to fix my website" after a website audit.

**Template:**
```
[TOOL NAME], I need you to fix [N] issues on my website: [URL]

It's a [tech stack] site deployed on [platform]. The codebase is in my project folder.

[For each issue, use this format:]
ISSUE [N] — [Short title]
[1-2 sentences: what's wrong + exact fix needed + why it matters]

Make all changes directly. Show me a summary of what you changed.
```

**Real example from 2026-05-29:**
```
I need you to fix 4 issues on my website: https://tchuekamui-sovereign.vercel.app/

It's a Next.js/React site deployed on Vercel. The codebase is in my project folder.

ISSUE 2 — Partner logos credibility problem
The site shows Apple, Meta, Google, Sony, Samsung logos as "partners". If these aren't real formal partnerships, change them from "Partner" logos to "Trusted By" or "Used By" logos with smaller tech/startup logos instead, or add a disclaimer like "Technologies we integrate with". If the partnerships ARE real, add a brief verification line under each logo. Do NOT remove them entirely — they build credibility.

ISSUE 3 — Mobile responsiveness
The site is desktop-only right now. Make it fully responsive for mobile (320px and up). Use CSS media queries. Key things to fix: triple-repeated headings should collapse to single line on mobile, navigation should become a hamburger menu, text blocks need proper padding/margins for small screens, CTA buttons need full-width on mobile, grid sections need to stack vertically.

ISSUE 4 — No urgent CTA
Add a "Book a Free Discovery Call" button in the hero section and in the footer. Link it to a Calendly or a simple mailto:tchuekam@gmail.com. Make it visually distinct (accent color, slightly larger).

ISSUE 5 — Brand name confusion
Clarify the hierarchy on the hero section. Right now "GIANTECT EMPIRE" is the logo but the products are "TCHUEKAMUI" and "TCHUEKAMOS" and the domain is "tchuekamui-sovereign". Add a subtitle under the hero heading that reads: "by Giantect Empire" or add a brief line: "Giantect Empire presents the Tchuekam product line — sovereign AI for African enterprises."

Also fix the triple text repetition — every heading is repeated 3 times. Keep it as a SINGLE clean heading with a subtle CSS glitch/scan-line animation effect on hover instead of literal text repetition.
```

---

## Prompt Type 2: New Tool / Agent Build (Scraper)

**When to use:** The user says "write a prompt to Antigravity to create a webscrape agent for cold calls, DMs, and emails".

**Template:**
```
[TOOL NAME], I need you to build a [tool type] called [AGENT NAME] for my enterprise AI system ([company name]). This agent [purpose] and feeds into my existing [receiving agent/process].

Build this as a [tech stack] project. Include:

1. [SUBSYSTEM 1 — description, tech, behaviors]
2. [SUBSYSTEM 2 — description, tech, behaviors]  
3. [INTEGRATION POINT — how outputs connect to other systems]
4. [OUTPUT FORMAT — what each record looks like]
5. [SCHEDULER / RATE LIMITS — platform constraints]
6. [UI — dashboard or export]

[Tech stack: Node.js with Puppeteer, SQLite3, Express.js]
[Deployment: Vercel-compatible or cheap VPS]

Build the complete project. Test that it works. Show me the code and how to run it.
```

**Real example from 2026-05-29:**
```
I need you to build a web scraping agent called "SCRAPER" for my enterprise AI system (Giantect Empire). This agent collects business leads from the web and feeds them into my existing sales agent "NEXUS" for cold outreach via WhatsApp, email, and DM.

Build this as a Node.js/Python project. Include:

1. LEAD SCRAPER ENGINE
   - Google Maps scraper: extract business name, phone, website, category, rating from search results (use Puppeteer/Playwright)
   - Website contact scraper: given a URL, find contact pages, extract emails, phone numbers, social media links
   - Directory scraper: scrape business directories (pagesjaunes, annuaire, etc.) for Cameroon/Africa businesses
   - LinkedIn search scraper: extract profiles from LinkedIn search results by keyword/location

2. LEAD DATABASE (SQLite)
   - Store: business name, phone, email, website, source, category, location, date_scraped, contacted_status
   - Dedup by phone + email automatically
   - Export to CSV for manual review

3. NEXUS INTEGRATION
   - After scraping, format leads into a queue that NEXUS (my sales agent) can consume
   - Output per lead: { name, phone, email, intro_message_template, source, priority_score }
   - Priority scoring: business with website + phone + email = high priority, only phone = medium, only email = low

4. WHATSAPP MESSAGE GENERATOR
   - For each lead, generate a personalized cold message template using their business name and category
   - Message must be short, warm, Cameroonian-friendly, in French or English based on location
   - Example: "Bonjour [name], je suis de Giantect Empire à Yaoundé. Nous aidons les entreprises comme la vôtre à automatiser leurs opérations avec l'IA. Avez-vous 5 minutes cette semaine pour une démo rapide ?"

5. SCHEDULER
   - Rate-limit messages: max 20 WhatsApp DMs/hour, max 50 emails/day
   - Spread outreach across business hours (8am-6pm WAT)
   - Track which leads were contacted and when
   - Auto-retry failed messages once

6. UI (simple web dashboard)
   - List all leads with search/filter
   - Show stats: total leads collected, contacted, replied, converted
   - Manual send button per lead for testing
   - CSV download

Tech stack: Node.js with Puppeteer for scraping, SQLite3 for storage, Express.js for the dashboard UI. Deployable on Vercel or a cheap VPS.

Build the complete project. Test that the scraper can find at least 10 real business leads from a Cameroon-based Google Maps search. Show me the code and how to run it.
```

---

## Key Differences Between the Two Types

| Aspect | Website Fixes | New Agent Build |
|---|---|---|
| Starting point | Existing live URL | Nothing — greenfield |
| Tech stack | Already known (inspect page) | You must specify |
| Each issue | Standalone, can be done independently | Sequential, subsystems depend on each other |
| Edge cases | Visual/UX edge cases (mobile, loading states) | Data edge cases (rate limits, dedup, validation) |
| Verification | "Open the site and check" | "Test that X works, show output" |
