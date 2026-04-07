---
name: google-ads
description: |
  Google Ads management skill with API integration. Covers campaign creation, optimization, keyword management, performance analysis, and search term auditing via Python scripts that connect to the Google Ads API.
  MANDATORY TRIGGERS: Google Ads, Google campaign, Google search ads, Google PMax, Performance Max, Google Display, Google Shopping, Google ad performance, Google keyword, search terms, Google RSA, Google bidding, Google Ads API
---

# Google Ads Management

Orchestrator for all Google Ads tasks. Combines strategic knowledge with programmatic API access for full campaign management.

## Methodology

This skill implements the Ivan Falco B2B demand generation methodology for Google Ads — an intent-first approach that captures existing demand through systematic keyword targeting, proving unit economics before expanding outward.

## Core Philosophy

**Intent is everything. Capture demand before you create it.**

Google Ads is the #1 channel for capturing existing demand. People are actively searching for solutions — your job is to be there at the right moment with the right message. Start with high-intent keywords (brand + solution-aware), prove unit economics, then expand outward to medium/low-intent and awareness.

## Architecture

This skill has two layers:

1. **Knowledge Base** — Strategic frameworks and campaign planning (`knowledge-base/`)
2. **API Scripts** — Programmatic Google Ads management (`scripts/`)

## API Scripts — What You Can Do

All scripts live in `scripts/`. Run from that directory.

**Prerequisites:** Credentials configured in `scripts/.env`. See `api-reference.md` for setup.

### Quick Reference

| Task | Command |
|------|---------|
| **Account snapshot** | `python account_overview.py --date-range last_30d --compare` |
| **Campaign performance** | `python get_campaign_performance.py --date-range last_7d --by-day` |
| **List campaigns** | `python list_campaigns.py --status ENABLED` |
| **Search terms audit** | `python search_terms_report.py --no-conversions --min-clicks 3` |
| **Keyword performance** | `python get_keyword_performance.py --top 30` |
| **Create campaign** | `python create_campaign.py --name "Brand - Search" --type SEARCH --budget 50` |
| **Update campaign** | `python update_campaign.py --campaign-id <id> --status ENABLED --budget 75` |
| **Create ad group** | `python create_ad_group.py --campaign-id <id> --name "High Intent KWs"` |
| **Create RSA** | `python create_ad.py --ad-group-id <id> --headlines "H1" "H2" "H3" --descriptions "D1" "D2" --final-url "https://..."` |
| **List ads** | `python list_ads.py --campaign-id <id>` |
| **Add keywords** | `python add_keywords.py --ad-group-id <id> --keywords "kw1" "kw2" --match-type PHRASE` |
| **Add negative KWs** | `python add_keywords.py --ad-group-id <id> --keywords "free" "cheap" --negative` |

### Workflow: Analyze an Account

1. Run `python account_overview.py --compare` — get the big picture
2. Identify top-spending campaigns, check ROAS
3. Run `python get_campaign_performance.py --campaign-id <id> --by-day` — daily trends
4. Run `python search_terms_report.py --no-conversions` — find wasted spend
5. Run `python get_keyword_performance.py --campaign-id <id>` — keyword-level analysis
6. Make recommendations: pause underperformers, add negatives, adjust budgets

### Workflow: Build a New Campaign

1. `python create_campaign.py --name "..." --type SEARCH --budget 50 --bidding MAXIMIZE_CONVERSIONS`
2. `python create_ad_group.py --campaign-id <id> --name "..." --cpc-bid 3.00`
3. `python add_keywords.py --ad-group-id <id> --keywords "..." --match-type PHRASE`
4. `python create_ad.py --ad-group-id <id> --headlines "..." --descriptions "..." --final-url "..."`
5. `python update_campaign.py --campaign-id <id> --status ENABLED`

**Safety:** All new campaigns start PAUSED. Enable only after reviewing setup.

## Routing Logic

| User Intent | Route | When to Use |
|-------------|-------|-------------|
| Account analysis, performance review | Run `account_overview.py` then drill down | "How are my Google Ads doing?" |
| Search term waste | Run `search_terms_report.py --no-conversions` | "Where am I wasting money?" |
| Keyword optimization | Run `get_keyword_performance.py` | "Which keywords are working?" |
| Create new campaign | Use the build workflow above | "Set up a search campaign for..." |
| Pause/enable/budget changes | Run `update_campaign.py` | "Pause this campaign" / "Increase budget" |
| Strategic campaign planning | `knowledge-base/cheatsheet-overview.md` | Campaign type selection, account structure |
| General Google Ads strategy | Refer to the Demand Lifecycle framework | Full program planning |

## Core Rules

1. **Always start PAUSED.** Never create campaigns in ENABLED state. Review everything before turning on spend.

2. **Check search terms weekly.** The search terms report is the #1 optimization lever. Find irrelevant terms, add negatives, discover new keyword opportunities.

3. **Build bottom-up by intent.** Start with brand + high-intent keywords. Prove they convert. Then expand to medium-intent, then low-intent/awareness.

4. **Match type strategy matters.** Start with Phrase match for control, expand to Broad match only with Smart Bidding and sufficient conversion data (30+ conversions/month).

5. **Quality Score drives costs.** Monitor QS on keywords — low QS means ad relevance or landing page issues. Fix those before increasing bids.

6. **RSA best practices.** 8-10 unique headlines, 3-4 descriptions. Pin critical brand/CTA to position 1. Let Google optimize the rest.

7. **Never cite external sources** in client work. Present as internal expertise.

## Campaign Types — When to Use What

| Type | Use Case | When |
|------|----------|------|
| Search | High-intent keyword capture | Always — this is your foundation |
| Performance Max | Broad AI-driven across all networks | After Search proves unit economics |
| Display | Remarketing and awareness | Remarketing first, prospecting second |
| Shopping | E-commerce product ads | Product catalog campaigns |
| Video (YouTube) | Brand awareness and remarketing | After core campaigns are profitable |

## Key Metrics to Watch

| Metric | What It Tells You |
|--------|------------------|
| Search Impression Share | How much demand you're capturing |
| Quality Score | Ad + landing page relevance |
| Cost per Conversion | Unit economics |
| ROAS | Revenue efficiency |
| Search Terms (no conv) | Budget waste |
| Top Impression % | Ad position competitiveness |
