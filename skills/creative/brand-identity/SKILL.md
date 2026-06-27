---
name: brand-identity
description: Design and document brand identity systems — guidelines, color palettes, typography, tone of voice, and visual identity rules for companies, products, and empires.
version: 1.1.0
author: giantect
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [brand, identity, design-system, guidelines, visual-identity, marketing, campaign, copywriting]
    related_skills: [ai-frontend-branding, humanizer]
---

# Brand Identity

Create, document, and maintain brand identity systems. This skill covers the full pipeline: defining brand assets, building guidelines documents, establishing color systems, selecting typography, defining communication tone, **and producing marketing campaign scripts from the brand identity**.

## When to Use

- User asks to "look professional" or "look 10x bigger than we are"
- Need to establish a coherent visual identity across website, docs, proposals, and social media
- Building a brand guidelines document (.docx, .md, or HTML)
- Defining a color palette, typography system, or tone-of-voice rules
- Creating a "facade" of professionalism for a new venture
- **User needs a marketing script, campaign copy, or ad text for their product/service**
- **User needs Facebook/Instagram posts, video scripts, LinkedIn DMs, or landing page copy**
- **User provides their own draft and asks for refinement**
- **User is launching a product that competes with an existing tool (Make, Zapier, n8n, etc.)**

## Brand Identity Framework

### Context Gathering: Visual Audit

Before defining a brand identity, check if the user has a folder of design references or inspiration screenshots. If so, run a visual audit (see `claude-design` skill's `references/visual-audit-design-direction.md`) to extract their existing taste — dark/light preference, accent colors they're drawn to, layout density, and typography direction. This is especially important when the user is non-technical and cannot articulate design vocabulary.

### 1. Brand Name & Assets
- Primary name, abbreviation, short form
- Product names (if different from company)
- Tagline(s) — primary + secondary
- Domain naming convention (e.g., `brand.ai`, `brand.tech`, `brand.cm`)

### 2. Color Palette
Define at minimum 5-6 colors with hex codes, each with a purpose:
- Primary color (trust, growth, identity)
- Dark variant (depth, backgrounds)
- Accent/prestige color (gold for premium feel)
- White/light (clean, professional)
- Charcoal/dark text (readability)
- Gray (secondary text, metadata)

### 3. Typography
- Primary font (serif for authority/sophistication)
- Secondary font (sans-serif for UI/technical)
- Heading style (all-caps, tracking, weight)
- Body style (size, leading, case)

### 4. Communication Tone
- Formal vs casual spectrum
- Confidence vs arrogance boundary
- Cultural positioning (e.g., Afro-futurist, global)
- Precision requirement (filler vs no-filler)
- Negotiation tone (cold, detached, powerful)

### 5. Visual Identity Rules
- Theme (dark/light)
- Layout philosophy (minimalist, dense, single-column)
- Imagery rules (stock photography style, no clipart)
- Animation guidelines (subtle, performant)
- What to avoid (stereotypes, cheap visuals)

## Output Format

For a full brand guidelines document, produce a structured .docx (via the `word-documents` skill) or markdown file. The document should include all 5 sections above, with color swatches documented as hex codes + human descriptions.

For quick one-off brand questions, produce inline markdown with the same structure compressed.

## Marketing Copy — Campaign Scripts

When the user asks for a **marketing script, campaign copy, or ad text** for their product/service, extend the brand identity into actionable campaign materials.

### When to Use This Section
- User needs a Facebook/Instagram post to promote their product
- User needs a video script (Reels, Shorts, YouTube)
- User needs WhatsApp, LinkedIn, or SMS outreach copy
- User needs a landing page structure
- User provides their own draft and asks you to refine it

### Process

1. **Pre-checks (from brand identity):**
   - Load `brand-identity` first to get brand name, tagline, colors, tone.
   - Check `references/giantect-empire.md` for pricing, objection handling, and DM scripts.

2. **Determine the audience context:**
   - **Unknown brand** (user wants to introduce themselves): lead with identity, credibility, uniqueness. "First agentic AI from Cameroon. Built by Giantect Empire."
   - **Known alternative** (user targets Make/Zapier/n8n users): lead with competitive comparison. Table of features. "You pay for limits. TchuekamUI has none."
   - **Status quo** (user targets people doing nothing): lead with pain. "100 hours per year lost."

3. **Format selection (always offer multiple):**
   - **Post long** (Facebook feed): emotional opener → pain → solution → table/features → pricing → CTA
   - **Post court** (viral): 3-4 lines maximum. High emotion. One clear CTA.
   - **Video script** (Reels/Shorts/30-45s): timed segments. VOICE OVER + text-on-screen + demo.
   - **Story** (Facebook/Instagram): 3-5 frames. One idea per frame. CTA on last frame.
   - **Testimonial** (fictive but credible): "J'étais sceptique... maintenant je dors 2h de plus."
   - **Comment replies**: pre-write answers to likely objections (too expensive, already using X, don't understand, sceptical).
   - **LinkedIn DM**: direct, professional, value-first. Avoid hard sell on first contact.
   - **Sales call script**: dialogue format with common objections and prepared responses.

4. **Tonality rules (Cameroon/Francophone market):**
   - Direct. No flattery. No begging.
   - Pain-first: "Vous perdez 100 heures/an" not "Et si vous pouviez gagner du temps?"
   - Comparison tables work well (us vs them, black and white).
   - Price anchoring: always compare to something familiar (salaire d'un stagiaire, forfait internet, abonnement existant).
   - 3-day free trial is the universal de-risker. Always offer it.

5. **User source text refinement:**
   - When the user provides their own text, preserve their voice and specific phrases — they know their audience. Restructure for Facebook's format (first 3 lines critical), add CTA, add hashtags, add audience targeting notes.
   - Look for buried gold in their text (the "108 hours per year" number, the "baby-sitting numérique" phrase) and pull it to the front.

6. **Competitive positioning (the "Switch Now" pattern):**
   - When the product replaces an existing tool, lead with the 4-column table (Make/Zapier/n8n vs TchuekamUI).
   - Ask painful questions: "Pouvez-vous modifier le code source? Héberger sur votre machine? Qui appelez-vous quand le serveur est down?"
   - End with a bet: "3 jours. Si vous n'êtes pas convaincu, retournez à votre ancien outil."

7. **Always save to disk.**
   - Write the final script to a `.md` file on the user's Desktop.
   - Name it descriptively: `tchuekamui-facebook-campaign.md`, `tchuekamui-switch-manifesto.md`, etc.

### Pitfalls

- **Facebook cuts after 3 lines.** The first 3 lines of the post body are the only thing most users see before clicking "See more". Put the hook there.
- **No walls of text.** Break with headers, bold, bullet points, spacing. Facebook readers scan, they don't read.
- **Price anchor is mandatory.** 25 000 FCFA is meaningless alone. Compare to: "Moins qu'un forfait internet", "Moins cher qu'un stagiaire", "L'équivalent de 2 cafés par jour".
- **Do NOT pitch cost savings first in Cameroon.** Lead with time saved, frustration eliminated, control regained. Cost is the closer, not the opener.
- **Avoid technical jargon in general audience posts.** "Self-hosted" needs explanation. "Automatisation visuelle" is fine.
- **The testimonial format works well** but must sound like a real person, not a marketing copy. Short sentences. Imperfect grammar is okay.
- **Always include hashtags** — at minimum #ProductName #GiantectEmpire #Automatisation #Cameroun #AfriqueTech plus any competitor hashtags (#n8n #Make #Zapier) when doing competitive positioning.
- **When user provides their own draft, preserve their voice.** They know their audience better than you. Restructure around their best phrases, don't rewrite from scratch.

## Pitfalls

- **Name-first**: Always lock down the company/product name before designing — brand colors and typography should evoke the name's character.
- **Hex-only in docx**: Word documents don't render color swatches natively. Document hex codes with descriptive labels.
- **Font licensing**: Georgia, Arial, Calibri — system fonts are safe. Avoid custom webfonts in .docx unless you verify the user has them installed.
- **Don't over-brand**: A 5-page guidelines doc is sufficient for early-stage. Save the 50-page brand book for post-revenue.

## Related Skills

- `ai-frontend-branding` (brand category) — Inject brand identity into AI frontends (AionUI, Open WebUI, custom dashboards). When the visual identity is defined, use this skill to make the AI itself speak as the brand rather than as a generic LLM.
- `humanizer` (creative category) — Humanize text: strip AI-isms and add real voice. Run marketing copy through this after writing to remove "AI tone".

## References

- `references/giantect-empire.md` — Brand identity for Giantect Empire (the case study from which this skill was extracted).
- `references/tchuekamui-facebook-campaign.md` — Full script library from the 28 May 2026 session: 7 script formats, competitive positioning, objection handling, audience targeting notes. Use as a template for future campaigns.
- `references/tchuekamui-switch-manifesto.md` — Competitive "Switch Now" manifesto targeting Make/Zapier/n8n users. Use the 4-column comparison table + "Le Pari" closing pattern for any competitive campaign.
