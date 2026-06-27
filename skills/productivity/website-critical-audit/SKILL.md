---
name: website-critical-audit
description: "Deliver a structured 10-pillar critical audit of any website — visual identity, code quality, UX, content, SEO, mobile responsiveness, performance, branding, and conversion paths. Produces ranked scores and prioritized fixes. Covers both live sites and local HTML/CSS/JS projects."
version: 1.0.0
author: giantect
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [audit, website, review, ux, seo, performance, conversion, code-review, design]
    related_skills: [dogfood, claude-design, sketch, popular-web-designs, codebase-inspection]
---

# Website Critical Audit

Deliver a professional 10-dimension critical examination of a website. Works for both live-hosted sites and local `file://` HTML/CSS/JS projects. Produces a numbered score (1-10) per pillar, an overall score, and a prioritized fix list.

## When to Use

- User asks "review my website", "critique my site", "examine my landing page", "what's wrong with my site"
- User shares a URL or local file path for a website they built
- User asks for a general assessment before launch
- Pre-purchase or pre-launch quality check on a client site

## Methodology — The 10 Pillars

Audit each pillar independently, then synthesize into a summary table and priority action plan.

### 1. Visual Identity & Consistency (6/10 base)
Examine: color palette, typography, spacing, visual hierarchy, dark/light mode, branded assets
Common pitfalls:
- Blanket `filter: grayscale(1)` on all images kills visual interest
- Overlays / `mix-blend-mode` that disappear into dark backgrounds
- Radial gradient masks that clip images awkwardly
- No accent color — entire site is grayscale or single-tone

### 2. Image Quality & Resource Management (3/10 base)
Examine: resolution, file format, filenames, optimization, lazy loading, alt text
Check:
- `loading="lazy"` on all below-fold images
- Width/height attributes to prevent layout shift
- No emoji or spaces in filenames (breaks Linux servers and CDNs)
- WebP format vs JPEG/PNG
- File size budget (15+ full-res images on one page = 5-10MB)
- Random alphanumeric filenames vs clean slugs

### 3. Code Quality & Structure (5/10 base)
**HTML:**
- Semantic elements (`<section>`, `<article>`, `<blockquote>`, `<nav>`, `<figure>`)
- Meta tags: description, viewport, charset, OG, Twitter Card
- Favicon present
- `lang` attribute on `<html>`
- Form elements with proper labels and `name` attributes

**CSS:**
- CSS custom properties (`:root` variables) — clean
- `clamp()` for fluid sizing — good modern approach
- Mobile breakpoints: are they sufficient or just 1-2 rules?
- Hardcoded heights (e.g. `height: 700px`) that break on mobile
- `@import` vs `<link>` for fonts (blocking vs async)

**JavaScript:**
- Is the search bar functional or cosmetic?
- Do buttons/CTAs have event handlers or only CSS styling?
- DOM manipulation: graceful degradation if elements are missing?
- Any truncated content, placeholder text, or half-finished features?

### 4. User Experience & Interaction (5/10 base)
Examine:
- Dead CTAs — buttons and links with `href="#"` or no onclick
- Non-functional features (cosmetic search bars, play buttons that do nothing)
- Navigation: is there a hamburger on mobile?
- Micro-interactions: hover states, transitions, feedback on action
- Accessibility: focus states, keyboard navigation, color contrast
- Meaningless decorative numbers or stats (e.g. "47.2% Reality" with no explanation)

### 5. Content & Copywriting (4/10 base)
Examine:
- Value proposition: can you understand what the company *does* in 5 seconds?
- Placeholder content: "Lorem ipsum" or unedited template text
- Truncated sentences, missing punctuation, cut-off quotes
- Generic author names that look like template defaults
- Fake testimonials — scraped social avatars erode trust
- Technical benefits vs marketing fluff ratio
- Contact info: is the email a `mailto:` link, phone clickable?

### 6. SEO & Performance (2/10 base)
NO METADATA = ZERO RANKING. Check:
- `<title>` tag
- `<meta name="description">`
- Open Graph tags (`og:title`, `og:description`, `og:image`, `og:url`)
- Twitter Card tags
- JSON-LD structured data (Organization, LocalBusiness, Product)
- Canonical URL
- Sitemap.xml
- Favicon
- Image optimization (WebP, compression, lazy loading)
- CDN / caching strategy
- Is the site even hosted? (file:// = not accessible to Google)

### 7. Mobile Responsiveness (4/10 base)
Examine:
- Number and granularity of media query breakpoints
- Navigation collapse (hamburger menu vs inline links)
- Fixed-height sections that overflow on smaller screens
- Font sizing: `clamp()` vs hardcoded px/rem
- Touch targets: are buttons large enough for thumbs?
- Image scaling: are huge background images clipped or compressed?
- Brand logo / partner logo strip: does it break on small screens?

### 8. Browser Compatibility & Edge Cases (6/10 base)
Examine:
- `backdrop-filter` support (Firefox 103+, Safari)
- CSS `mix-blend-mode` support
- Google Fonts: `font-display: swap` for fallback
- No `<noscript>` fallback — what happens with JS disabled?
- `-webkit-` prefixes for modern CSS features
- Custom fonts: what's the fallback stack?
- CSS `@supports` for progressive enhancement

### 9. Branding & Positioning (4/10 base)
Examine:
- Is the brand name unique or generic? (Search for conflicts)
- Does the copy differentiate or sound like a template?
- "Futuristic" / "Innovative" / "Next-gen" are genres, not differentiators
- Social proof: are partner logos real or placeholder images?
- Avatar/profile images: real people or AI-generated/scraped?
- Tone of voice: consistent across all sections?
- **Brand hierarchy clarity**: Is the relationship between parent company (e.g. Giantect Empire) and products (e.g. TchuekamUI, TchuekamOS) clear within 5 seconds? If a visitor can't tell what the company is vs what the product is, flag this.
- **Design gimmicks that harm readability**: Triple text repetition ("AUTONOMOUS INTELLIGENCE AUTONOMOUS INTELLIGENCE AUTONOMOUS INTELLIGENCE"), aggressive CSS glitch effects, or repeating heading text three times in the DOM. These often intend a "digital" aesthetic but read as rendering bugs to real users. Flag any instance of identical text repeated ≥2 times in the same heading element.
- **Trust signals vs trust risks**: Count real vs cosmetic trust signals. Partner logos from major brands (Apple, Meta, Google, Sony, Samsung) that aren't verified partnerships are a credibility risk — note that if they're aspirational rather than contractual, they may backfire with serious enterprise buyers.
- **African/emerging-market positioning**: If the site positions itself as local (e.g. "Yaoundé, Cameroon", "100% autonomous — Yaoundé"), does it lean into this as a strength or does the design feel like it's trying to look "Western"? Local authenticity is a differentiator — flag if the design language contradicts the geographic claim.

### 10. Actionability & Conversion (1/10 base)
This is where most sites fail. Count every clickable element and verify it has a real destination:
- Primary CTA button → where does it go?
- Secondary CTA links → real pages or `#`?
- Contact email → `mailto:` link or plain text?
- Phone number → `tel:` link or plain text?
- Social links → real profiles or `#`?
- Footer navigation → every link points to a real page?
- Any form → does it submit somewhere or is it cosmetic?
- Newsletter signup → exists?
- Pricing / demo booking → accessible?

**Common failures found in audits:**
- All 12+ footer links point to `href="#"`
- "Get Started" button has no event listener
- Email is plain text, not `mailto:`
- Social icons all go to `#`
- Search bar accepts input but does nothing on Enter

## Output Format

```
## SUMMARY SCORE: X/10

| Category | Score |
|---|---|
| Visual Identity | X |
| Image Quality | X |
| Code Quality | X |
| UX & Interaction | X |
| Content & Copy | X |
| SEO & Performance | X |
| Mobile Responsiveness | X |
| Browser Compatibility | X |
| Branding & Positioning | X |
| Conversion & Actionability | X |
| **OVERALL** | **X/10** |
```

Then append **URGENT FIXES** as a numbered priority list, with the most critical (dead CTAs, SEO, hosting) first.

## Procedure

1. **Load the files** — read `index.html`, `style.css`, `script.js` (or equivalent)
2. **Check image directory** — list all image files, check filenames for issues (spaces, emoji, random hashes)
3. **Render in browser** — navigate to the site URL or `file:///` path, take in the visual experience
4. **Check console** — browser console for JS errors, missing resources, failed image loads
5. **Score each pillar** — use the baseline scores above and adjust up/down based on actual quality
6. **Write the report** — structured with sub-bullets per pillar showing specific examples from the code

## Pitfalls

- Don't assume the user knows basic concepts. They may not understand what SEO metadata or lazy loading means. Frame fixes as concrete actions: Add this HTML to your <head> rather than improve your SEO.
- Don't only praise. A polite audit that avoids real criticism is worthless. The user is paying you for honesty.
- file:// URLs — if the site is local, note that many features forms, external API calls, analytics wont work from file://. Hosting is step 1.
- Template detection — many sites are unedited HTML templates. Flag placeholder content, generic Lorem Ipsum text, random author names, unchanged brand logos, and href=# on every link.
- Broken images — when images use relative paths (e.g. ../image.jpg), check the actual file exists at that path.
- Emoji in filenames — will fail on Linux servers, most CDNs, and some browsers. Flag with a rename suggestion.
- Truncated testimonials — check for sentences that end mid-word or without closing quotation marks.
- Always count dead links. Navigate the page and click everything. Count how many links have href=# — this is the most objective measure of site readiness.
- Triple text repetition in headings. Some templates repeat heading text three times in the DOM for a CSS glitch or digital effect. This renders as broken text in accessibility tools, screen readers, and search engine previews. Always flag this as critical — fix is to keep one instance in the DOM and use CSS pseudo-elements for the visual effect.
- Partner logo legitimacy. Sites with Apple, Meta, Google, Samsung logos: distinguish actual partnerships from aspirational use. Flag if logos may not represent real partnerships.
- Search bar on one-page sites. Test it — type and press Enter. If nothing happens, flag it. On a single-page site, a search bar makes no UX sense.
- Mobile-first for African markets. Cameroon, Nigeria, Kenya are 80%+ mobile. A desktop-only site for an African audience is a critical failure. Test at 375px width.

### After the Audit: Generating Fix Prompts for AI Coding Tools

After delivering an audit, the user will often say "write a prompt for Antigravity/Codex to fix these issues." This is the standard handoff pattern:

1. List each issue as a numbered section in the prompt (see `ai-coding-tool-prompting` skill for full methodology)
2. For each issue, include: WHAT is wrong + EXACT fix needed + WHY it matters
3. Add brand context (company name, colors, tone) so the tool doesn't invent them
4. Tell the tool to make changes directly and show a summary of what changed
5. End with: "Make all changes directly. Show me a preview URL or summary of what you changed."

Example from the Giantect Empire audit (see reference file):
```
ISSUE 2 — Partner logos credibility problem
The site shows Apple, Meta, Google, Sony, Samsung logos as "partners".
If these aren't real partnerships, change them from "Partner" logos to "Trusted By"
logos with smaller tech/startup logos instead.
```

The prompt IS the deliverable — the user copies and pastes it into their tool. Don't execute the changes yourself through the browser.

### After the Audit: Rebranding a Template to a Company Site

The audit often reveals a common scenario: the user has a **generic HTML template** and wants it converted to their **company's official website**. This is the natural follow-through after the audit.

### The Two-Step Process

**Step 1 — Audit** (this skill): Identify placeholder content, dead CTAs, generic copy, and structural issues.

**Step 2 — Rebrand** (the conversion): Turn the template into the company's official site.

### Rebranding Checklist

When the user asks "now I need to rebrand this to our company" after the audit, follow this process:

1. **Gather company details first, before writing a single line of code.** Use session_search/memory to recall known company info. If gaps exist, present the user with specific questions — do NOT start building until you have:
   - Company name and tagline
   - Brand colors (ask or infer from existing assets)
   - Core offering (what they actually DO)
   - Target audience
   - Contact info (real email, phone, address)
   - Pricing if applicable
   - Real testimonials or social proof (or note to remove section)

2. **Replace all placeholder content:**
   - Generic brand name (e.g. "NeoVision") → Company name
   - Lorem ipsum / AI filler copy → Real value proposition
   - Fake testimonials with scraped avatars → Remove section or use real clients
   - Placeholder contact info → Real contact details
   - Dead CTAs (href="#") → Real links or remove buttons
   - Generic author names → Real names or remove
   - Partner logos with random images → Remove if not real partnerships

3. **Fix images:**
   - Images with random numeric filenames (e.g. "1086282372601805720.jpg") → Rename with meaningful slugs
   - Avatar images that don't match the brand → Replace with brand-appropriate visuals
   - Emoji in filenames → Rename (breaks Linux servers)

4. **Fix code quality:**
   - Add meta description and Open Graph tags (SEO is usually zero on templates)
   - Remove dead UI elements (search bars that don't search, slider arrows that don't slide)
   - Add `loading="lazy"` to images below the fold
   - Fix `href="#"` anchors to point to real sections or remove

5. **Document the conversion.** Create a brand documentation file (Word doc or markdown) that captures:
   - Company description, mission, vision
   - Product/service offerings with pricing
   - Target market
   - Brand voice guidelines
   - This file becomes the source of truth for all future content decisions

### Pitfalls

- **Don't start writing code before you have the company's real info.** The user saying "write a documentation of our company" means you need to ask for specifics, not start building a generic document.
- **The audit and rebrand are separate requests.** The user may want the audit first, then decide on rebranding. Don't assume both in one response.
- **Template names (NeoVision, TechVision, FutureVision, etc.) are clues.** If the template brand name is generic, point it out. The rebrand to the real company name is a naming improvement.
- **Documentation first, site changes second.** When the user asks for company documentation, produce a standalone reference document (.docx or .md) BEFORE modifying the HTML. That document becomes the guide for all subsequent changes.
- **Broken image paths from relative file references.** Templates often use images in the same directory. When rebranding, check that new images resolve at the same relative path.

### Related Skills

- `brand/b2b-marketing-copy` — writing copy for the rebranded site (Facebook, landing pages, WhatsApp scripts)
- `brand/electron-app-rebranding` — if the rebrand also covers a desktop app
- `brand/ai-frontend-branding` — if the rebrand covers the AI's identity prompt
- `productivity/word-documents` — for creating the brand documentation .docx

### Reference Files

- `references/giantect-empire-website-audit-2026-05-29.md` — real-world audit of the Giantect Empire site. Shows branded startup website patterns: triple text repetition, partner logo legitimacy, brand hierarchy clarity, and African-market mobile priorities.

## Verification

- After fixing: re-navigate and click every interactive element
- Run the page through Google PageSpeed Insights if hosted
- Validate HTML at validator.w3.org
- Check contrast ratio with WebAIM contrast checker
