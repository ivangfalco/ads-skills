---
name: linkedin-ads
description: |
  LinkedIn Ads management skill for B2B SaaS campaigns. Routes to specialized sub-skills for campaign planning, performance analysis, account audits, and account management.
  MANDATORY TRIGGERS: LinkedIn Ads, LinkedIn campaign, LinkedIn advertising, B2B ads, paid social, LinkedIn paid, ad account, campaign manager, LinkedIn lead gen, LinkedIn retargeting, ad audit, ad performance, ad optimization, campaign plan, media plan, LinkedIn budget
---

# LinkedIn Ads Management

Orchestrator for all LinkedIn Ads tasks. Route to the correct sub-skill based on the user's request.

## Methodology

This skill implements the Ivan Falco B2B demand generation methodology — a full-funnel, 5-Stage Demand Engine approach to LinkedIn Ads that prioritizes audience precision, Thought Leader Ads, and systematic scaling through audience penetration.

## Routing Logic

Determine what the user needs and load the relevant knowledge-base files:

| User Intent | Load These Files | When to Use |
|-------------|-----------------|-------------|
| Build a new campaign plan | `full-funnel-framework.md`, `campaign-structures.md`, `audience-sizing.md`, `bidding-strategy.md`, `launch-checklist.md` | New client onboarding, new campaign setup, media plan creation, budget allocation |
| Analyze performance data | `benchmarks.md`, `bidding-strategy.md`, `scaling-strategy.md` | Weekly/monthly reporting, diagnosing underperformance, optimization recommendations |
| Audit an existing account | `audit-checklist.md`, `benchmarks.md`, `audience-sizing.md` | New client audit, periodic health check, account takeover, identifying issues |
| Creative development | `creative-strategy.md`, `copy-audit-framework.md`, `conversation-ads.md`, `document-ads.md` | Ad copy, creative briefs, format selection |
| Scaling decisions | `scaling-strategy.md`, `bidding-strategy.md`, `audience-sizing.md` | Increasing budgets, adding campaigns, expanding audiences |
| ABM campaigns | `abm-strategy.md`, `audience-sizing.md` | Account-based targeting, list management |

## Knowledge Base

All recommendations must be grounded in the knowledge base. Before executing any sub-skill, read the relevant knowledge-base files:

| File | Contains | Read When |
|------|----------|-----------|
| [full-funnel-framework.md](knowledge-base/full-funnel-framework.md) | TOF/MOF/BOF structure, budget allocation, timeline | Campaign planning, strategy discussions |
| [audience-sizing.md](knowledge-base/audience-sizing.md) | Audience size ranges, targeting rules, exclusions, job functions vs titles, splitting audiences, audience expansion models | Building audiences, reviewing targeting, scaling audiences |
| [campaign-structures.md](knowledge-base/campaign-structures.md) | 6 campaign group structure models, naming conventions, 5-Stage Demand Engine campaign groups framework, splitting methodology | Setting up campaign structure, scaling structure |
| [launch-checklist.md](knowledge-base/launch-checklist.md) | 8-part pre-launch checklist | Before launching any campaign |
| [bidding-strategy.md](knowledge-base/bidding-strategy.md) | Bidding approach, weekly optimization, audience penetration rules, group budget optimization | Optimizing bids, weekly management, budget decisions |
| [benchmarks.md](knowledge-base/benchmarks.md) | CTR/CPC/CPL benchmarks by stage | Performance analysis, setting expectations |
| [creative-strategy.md](knowledge-base/creative-strategy.md) | Creative by awareness stage, 12 angles with rationale, TLA strategy, templates | Creative development, ad copy |
| [conversation-ads.md](knowledge-base/conversation-ads.md) | Conversation ad best practices: copy, CTAs, sender, testing, TLA combo | Conversation ad campaigns, inbox messaging |
| [document-ads.md](knowledge-base/document-ads.md) | Document ad best practices: 7-slide formula, copy principles, design, audience variants | Document ad / carousel campaigns, MOF nurture |
| [copy-audit-framework.md](knowledge-base/copy-audit-framework.md) | 5-layer copy audit: accuracy, tone, structure, design, audience fit | Reviewing any ad copy before launch, quality control |
| [landing-pages.md](knowledge-base/landing-pages.md) | Landing page strategy per funnel stage, Lead Gen Form optimization | Campaign planning, conversion optimization |
| [scaling-strategy.md](knowledge-base/scaling-strategy.md) | Scaling progression (1 campaign to multiple accounts), penetration rules, 5-Stage Demand Engine campaign groups, forecasting, group budgets, objective experiments | Scaling campaigns, increasing budgets, advanced strategy |
| [abm-strategy.md](knowledge-base/abm-strategy.md) | ABM campaign types (1:1, 1:few, 1:many), company vs contact lists, list sizing, performance analysis | ABM campaigns, account-based targeting, list management |
| [audit-checklist.md](knowledge-base/audit-checklist.md) | 35-item audit checklist with priorities | Account audits, health checks |

## Core Rules

1. **Never cite external sources** in client-facing materials. All knowledge is presented as internal expertise.
2. **Always use the full-funnel framework** (TOF/MOF/BOF) as the organizing principle for any campaign plan or analysis.
3. **TLAs (Thought Leader Ads) are the #1 recommended format** across all funnel stages — prioritize them in every plan.
4. **Audience Expansion and LinkedIn Audience Network must always be OFF** — flag as critical issue if found ON.
5. **Benchmarks are B2B SaaS specific.** Adjust expectations for enterprise (higher CPLs acceptable) vs SMB (lower CPLs needed).
6. **Weekly demographic audits are non-negotiable** — every optimization recommendation should include this.
7. **Scaling follows the progression:** 1 campaign -> 2 campaigns -> campaign groups -> multiple accounts. Always read `scaling-strategy.md` before advising on scaling.
8. **Budget penetration drives scaling decisions.** 30-day penetration under 25% or 60-day under 40% = increase budget. Aim for 35%+ penetration.
9. **ABM campaigns should use company lists** over contact lists. Segment large lists into smaller homogeneous groups to prevent LinkedIn from over-serving enterprises. Read `abm-strategy.md` for ABM work.
10. **Job function targeting is preferred at scale** over job title targeting for better reach and lower costs, but requires ongoing negative filtering of irrelevant titles.

## Output Standards

- Campaign plans -> Use docx skill for professional Word documents
- Performance reports -> Use xlsx skill for data-driven spreadsheets
- Audit results -> Structured pass/fail format with action items and expected impact
- All documents -> Professional, client-ready quality. No agency jargon, no source citations.
