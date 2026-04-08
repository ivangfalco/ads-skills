# Ivan Falco's Ads Skills for Claude Code

**Turn Claude Code into your B2B advertising co-pilot.** 40+ strategy files, 39 API scripts, and battle-tested frameworks for LinkedIn, Meta, and Google Ads - built from managing $200K+/month in B2B ad spend across 12+ accounts.

Clone this repo, open Claude Code, and ask it anything about your ads. It knows the strategy, it can pull your data, and it can manage your campaigns.

## Built by

**Ivan Falco** - Head of Growth at [ColdIQ](https://coldiq.com) and Head of the Ads/ABM agency. Building AI-native advertising systems that make one person operate like five.

If you need help with ads operations, growth operations, or scaling your B2B campaigns - DM Ivan directly: [LinkedIn](https://www.linkedin.com/in/ivanfalco/)

---

## What's Inside

### 4 Skills

| Skill | Command | What it does |
|-------|---------|-------------|
| **LinkedIn Ads** | `/linkedin-ads` | Full campaign lifecycle - strategy, targeting, creative, analytics, bidding, demographics, audience uploads, lead forms |
| **Meta Ads** | `/meta-ads` | Meta for B2B - creative-as-targeting, audience strategy, campaign structure, optimization, fatigue detection |
| **Google Ads** | `/google-ads` | Intent-first search campaigns - keyword management, bid strategy, search terms auditing, performance analysis |
| **Onboarding** | `/onboarding` | Interactive 5-minute setup - API credentials, connection testing, getting started |

### 40+ Knowledge Base Files

**Ads Foundations (10 files):**
- 5-Stage Demand Engine (replaces traditional TOFU/MOFU/BOFU)
- Budget allocation by stage and channel
- Ad copywriting frameworks (voice-of-customer, 5-layer audit)
- Channel selection criteria
- Optimization signals (leading vs lagging)
- Scaling quadrant framework
- Offers strategy by funnel stage

**LinkedIn Ads (15 files):**
- Full-funnel framework (TOF/MOF/BOF with budget splits)
- Audience sizing rules (60K-400K cold, retargeting ranges)
- 6 campaign structure models + naming conventions
- Bidding strategy (automated → manual CPC progression)
- Creative by awareness stage (12 angles with rationale)
- ABM playbook (1:1, 1:few, 1:many approaches)
- Scaling progression (penetration-based)
- Format-specific: conversation ads, document ads, CTV
- 35-item audit checklist
- CTR/CPC/CPL benchmarks by funnel stage

**Meta Ads (16 files):**
- Meta Ads Operating System (the master decision framework)
- Creative Cadence OS (production pipeline, iteration hierarchy)
- Why Meta works for B2B (50% lower CPL vs LinkedIn when done right)
- Pixel + CAPI setup and event hierarchy
- Audience strategy (CRM lookalikes → third-party → broad)
- 3-phase campaign structure (ABO → CBO → Advantage+)
- Creative fatigue detection and rotation cadence
- Advantage+ automation guide
- Optimization playbook with B2B benchmarks
- Lead form optimization (social amnesia problem)
- ABM on Meta playbook
- Offer strategy by funnel stage

**Google Ads (1 file):**
- Campaign types cheatsheet (Search, Shopping, Display, PMax, Video)

### 39 Python Scripts

**LinkedIn Ads - 14 scripts:**
- `account_overview.py` - Account dashboard with period comparison
- `list_campaigns.py` - All campaigns with status, budget, metrics
- `get_campaign_performance.py` - Detailed analytics with daily breakdown
- `create_campaign.py` - Create campaigns (5 objectives, 3 bid strategies)
- `update_campaign.py` - Update status, budget, bids, name
- `list_creatives.py` - All creatives with type and campaign association
- `get_demographics.py` - 5-pivot demographics (job function, seniority, company size, industry, country)
- `upload_audience.py` - Upload TAL/contact lists as DMP segments
- `list_lead_forms.py` - All lead gen forms with questions
- `manage_bids.py` - View and update bid strategy and amounts
- `linkedin_api.py` - Core API client class
- `oauth_server.py` - OAuth token flow
- `config.py` / `client.py` - Shared configuration and auth

**Meta Ads - 12 scripts:**
- `account_overview.py` - Account dashboard with actions breakdown
- `list_campaigns.py` - Campaigns with inline insights
- `get_campaign_performance.py` - Analytics with daily breakdown
- `create_campaign.py` - Create campaigns (5 objectives, special ad categories)
- `update_campaign.py` - Update status, budget, name
- `list_ad_sets.py` - Ad sets with targeting summary and metrics
- `list_ads.py` - All ads with performance data
- `get_active_ads_copy.py` - Full creative/copy extraction (link, video, carousel, dynamic)
- `create_custom_audience.py` - Upload hashed customer lists
- `ad_scheduler.py` - Schedule automatic ad pauses
- `config.py` / `client.py` - Shared configuration and auth

**Google Ads - 13 scripts:**
- `account_overview.py` - Account snapshot with period comparison
- `list_campaigns.py` - All campaigns with metrics
- `get_campaign_performance.py` - Detailed analytics with daily/custom ranges
- `create_campaign.py` - Create campaigns (6 types, 5 bidding strategies)
- `update_campaign.py` - Update status, budget, name
- `create_ad_group.py` - Create ad groups with CPC bids
- `create_ad.py` - Create RSAs with headline/description validation
- `list_ads.py` - Ads with performance and approval status
- `add_keywords.py` - Add positive/negative keywords (broad, phrase, exact)
- `get_keyword_performance.py` - Keyword analytics with Quality Score
- `search_terms_report.py` - Search terms audit, wasted spend finder
- `config.py` / `client.py` - Shared configuration and auth

## Quick Start

```bash
# 1. Clone this repo
git clone https://github.com/ivangfalco/ads-skills.git
cd ads-skills

# 2. Open Claude Code
claude

# 3. Run the onboarding (5 minutes)
/onboarding
```

Or skip onboarding and just start asking:

```
"Audit my LinkedIn ad account"
"What's the right budget split for $50K/month?"
"Pull my active Meta ads and review the copy"
"Create a search campaign for our product"
"Which campaigns should I kill and which should I scale?"
```

## How It Works

These skills turn Claude Code into a specialized advertising assistant. Each skill file teaches Claude:

- **What to do** - strategy frameworks, decision trees, benchmarks
- **How to do it** - Python scripts that connect to ad platform APIs
- **When to reference what** - routing logic that loads the right knowledge for the task

The methodology is the Ivan Falco 5-Stage Demand Engine approach - battle-tested across 12+ B2B accounts, $200K+/month in managed spend. When Claude gives you advice through these skills, it's grounded in real campaign data, not generic best practices.

## Repo Structure

```
ads-skills/
├── CLAUDE.md                           # AI context - branding, rules, architecture
├── .claude/
│   └── skills/
│       ├── onboarding/                 # Interactive setup (SKILL.md)
│       ├── linkedin-ads/               # LinkedIn Ads skill
│       │   ├── SKILL.md                # Routing logic + methodology
│       │   ├── api-reference.md        # LinkedIn Marketing API docs
│       │   ├── knowledge-base/         # 15 strategy files
│       │   └── scripts/               # 14 Python scripts
│       ├── meta-ads/                   # Meta Ads skill
│       │   ├── SKILL.md
│       │   ├── api-reference.md
│       │   ├── knowledge-base/         # 16 strategy files
│       │   └── scripts/               # 12 Python scripts
│       └── google-ads/                 # Google Ads skill
│           ├── SKILL.md
│           ├── api-reference.md
│           ├── knowledge-base/         # 1 strategy file
│           └── scripts/               # 13 Python scripts
├── ads-foundations/                     # 10 cross-platform advertising frameworks
├── .env.example                        # Credential template
└── README.md                           # This file
```

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed
- Python 3.10+ (for running API scripts)
- API credentials for the platforms you use

## Who This Is For

- **B2B marketers** managing ad campaigns across multiple platforms
- **Growth operators** who want AI-assisted campaign management
- **Agencies** managing multiple client accounts
- **Founders** running their own paid acquisition

If you want to see what a full AI-native advertising operation looks like, check out what we're building at ColdIQ.

---

*Built by [Ivan Falco](https://www.linkedin.com/in/ivanfalco/) at [ColdIQ](https://coldiq.com). These skills are provided as-is. You are responsible for your own API usage, ad spend, and platform compliance.*
