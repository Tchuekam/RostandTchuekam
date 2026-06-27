---
name: ai-product-market-research
description: "Research and analyze competitive AI product landscapes — competitor benchmarking, pricing intelligence, packaging strategy, and positioning for African and global markets. Produces structured .docx reports with comparison tables."
version: 1.0.0
author: tchuekam
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [research, market-analysis, ai-agents, pricing, africa, competition]
---

# AI Product Market Research

Research an AI product's competitive landscape, benchmark pricing, identify gaps, and produce a structured report with packaging recommendations.

## Workflow

### Phase 1: Define the Research Questions

Before browsing, write down the questions:

- What competitors exist for this product category?
- What is their pricing (per month, per seat, per task)?
- What markets do they serve (global, Africa, specific countries)?
- What is their delivery model (SaaS, self-hosted, API)?
- Where is the gap / underserved segment?
- What are African-market prices for equivalent services?

### Phase 2: Data Collection (Browser)

Use the browser tool to visit competitor pricing pages directly. Target sources:

| Target | What to find | Example queries |
|--------|-------------|-----------------|
| Direct competitors | Pricing pages | `wati.io/pricing`, `anthropic.com/pricing` |
| African equivalents | Local SaaS pricing | Local WhatsApp bot providers, dev agencies |
| Marketplaces | Product types | GitHub Marketplace, ProductHunt |
| Wikipedia | Product taxonomy | "autonomous agent" definitions |

**IMPORTANT research question to include:** "Does a mobile-native autonomous AI agent exist?" This is a first-mover question. Check Termux compatibility, phone-based agent frameworks, and WhatsApp-based autonomous systems. If the answer is "no" — that's your killer differentiator.

**Pitfalls:**
- Google blocks automated searches (CAPTCHA). Navigate directly to competitor sites, don't search.
- Cloudflare blocks headless browsers. Retry with different URL paths or skip if blocked.
- Some sites are JS-heavy and may not render all content. Use `browser_snapshot(full=true)` to see everything.
- **GitHub Marketplace**: Works well for browsing. Use as a reliable data source when other sites block.
- **Wikipedia**: Content-loaded pages (lots of MathML, complex markup). The snapshot truncates. Use the table of contents links to navigate to specific sections rather than scrolling.
- **Anthropic/Claude pricing**: Renders well but accessibility tree is deep. Navigate to the pricing tab (ref e4 if visible) to expand plan details. Individual plans ($17 Pro, $100 Max), Team, and Enterprise tiers are visible in the tabpanel.
- **WATI pricing**: Cookie consent popup appears first. Click "Confirm my preferences" before trying to read plan cards. Plans are $39 Growth, $79 Pro, $199 Business with AI copilot features.

### Phase 3: Structure the Findings

Organize into these sections in the final document:

1. **Market Gap Analysis** — What doesn't exist yet that we can build
2. **Competitive Pricing Landscape** — Table: Product | Type | Monthly Price | Market
3. **African Market Comparison** — Table: Product | Service | Price (local currency)
4. **Unique Advantages** — Bullets: what we do that competitors cannot
5. **Packaging Strategy** — Tier name | Target | Price | Features | Rationale
6. **Pricing Psychology** — Why each price point works in the African market (anchor pricing, value comparison, premium halo)

### Phase 4: Compile into .docx Report

Use the `word-documents` skill to produce the final report. The report should include:

- **Tables** for competitive benchmarks (use `Table`, `TableRow`, `TableCell`, `WidthType`, `BorderStyle` from `docx`)
- **Cover page** with brand colors
- **Page breaks** between major sections
- **Clear tiered pricing table** as the centerpiece

## B2B Enterprise Strategy Extension

When the analysis targets **large enterprises** (not SMEs or consumers), extend the report with these additional sections:

### Segment Identification
List target enterprises by sector with specific company names and budget context. African B2B segments to consider:

| Sector | Budget IT | Pain point |
|--------|-----------|------------|
| Banques & finances | 50-200M FCFA/an | Conformité, reporting, documents |
| Télécoms | 100-500M FCFA/an | Centres d'appels, réclamations, back-office |
| Assurances | 30-100M FCFA/an | Sinistres, contrats, relances |
| Gouvernement | 50-300M FCFA/an | Modernisation, dématérialisation |
| Distribution | 10-50M FCFA/an | Stocks, commandes, reporting |
| ONG internationales | 20-100M FCFA/an | Reporting, coordination terrain |
| Pétrole & mines | 50-200M FCFA/an | Logistique, conformité |

### Competitor Taxonomy
Classify competitors as either **Direct** (same problem, same segment) or **Indirect** (partial solution):

- **Direct examples**: UiPath, Automation Anywhere, Microsoft Power Automate, n8n, Make, Botpress
- **Indirect examples**: Agences de développement (sur-mesure), assistants humains, usage direct de ChatGPT/Claude

Use a comparison table with: Concurrent | Type | Forces | Faiblesses.

### SWOT Analysis
Always produce a four-quadrant analysis as a table or bullet sections:

| Forces (S) | Faiblesses (W) |
|------------|----------------|
| First-mover advantage, price 10x lower, sovereignty | Unknown brand, limited resources, no certifications |

| Opportunités (O) | Menaces (T) |
|------------------|-------------|
| Gov digitalisation mandates, crisis drives automation | Better-funded local clone, geopolitical dependency |

### Risk Register
For each identified risk, document: Risque | Probabilité | Impact | Atténuation. Common enterprise risks:

- Dependency on foreign API/LLM provider → Mitigate with multi-provider + open-source models
- Local competitor emerges → Mitigate by locking 20+ clients before 2027
- Client doesn't understand the product → Mitigate with 3-day free trial, sell results not tech
- Regulatory uncertainty → Mitigate by engaging with government early

### Multi-Phase Attack Plan
Structure the go-to-market as phases with clear metrics:

| Phase | Period | Goal | Actions |
|-------|--------|------|---------|
| Foundation | Mois 1-2 | 5 clients | 20 prospects/day, 3 demos/week |
| Reference | Mois 3-4 | 1 case study | Over-deliver for key client |
| Visibility | Mois 5-7 | 10 clients | Publish case studies, media partnerships |
| Acceleration | Mois 8-10 | 20 clients | Hire sales, automate lead gen |
| Consolidation | Mois 11-12 | Exit/perpetual sale | Negotiate 10M FCFA license |

### Phase 5: Record to Memory

After analysis, save key findings to memory:

```
Giantect market analysis complete. [Product] is [position]. 
Recommended packaging: [Tiers with prices]. 
Key differentiator: [Unique advantage].
Doc saved at: [path]
```

## Pricing Psychology for African Markets

When pricing AI products for African SMEs:

| Technique | How to apply | Example |
|-----------|-------------|---------|
| **Anchor pricing** | Start at the price of a data plan (25K FCFA/mo) — everyone pays that already | "Same as your monthly Orange credit" |
| **Value comparison** | Compare to employee salary (150K/mo) vs agent price (75K/mo) | "Replaces a 150K employee for half the cost" |
| **Premium halo** | Include a very high tier (10M one-time) — makes mid-tier feel reasonable | 10M perpetual license → 75K/mo feels cheap |
| **Mobile-first** | Every plan includes WhatsApp access — African SMEs live on WhatsApp | "Send a message. Get results. No dashboard needed." |
| **FCFA pricing** | Always quote in FCFA — USD prices create friction | 25K FCFA, not $40 |

## Related Skills

- `word-documents` — for creating the .docx report with tables and formatting
- `github-issues` — for tracking competitive intelligence as research issues

## Linked references

See `references/competitors.md` for captured competitor pricing data from past research sessions.
