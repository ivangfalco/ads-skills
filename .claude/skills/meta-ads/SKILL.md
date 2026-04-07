---
name: meta-ads
description: |
  Meta Ads (Facebook/Instagram) management skill for B2B campaigns. Covers audience strategy, campaign structure, creative testing, and lead form optimization specifically for B2B SaaS on Meta's platform.
  MANDATORY TRIGGERS: Meta Ads, Facebook Ads, Instagram Ads, Facebook campaign, Meta campaign, Facebook advertising, Meta advertising, Facebook lead gen, Meta lead forms, Facebook retargeting, Meta remarketing, Facebook lookalike, Meta audience, Advantage Plus, Meta B2B, Facebook B2B
---

# Meta Ads Management for B2B

Orchestrator for all Meta Ads (Facebook/Instagram) tasks. Meta Ads for B2B can deliver half the cost per lead and lower cost per qualified opportunity compared to LinkedIn — but only when audience data quality is right and creative does the targeting work.

## Methodology

This skill implements the Ivan Falco B2B demand generation methodology for Meta — a data-first, creative-as-targeting approach that leverages Meta's algorithm (Andromeda + Gem) with high-quality audience inputs and systematic creative testing.

## Core Philosophy

**On Meta, your data is everything. Your creative is your targeting.**

Meta's native targeting can't match LinkedIn's B2B precision (no job title, company, seniority filters). The way to make Meta work for B2B is to bring your own high-quality audience data (CRM, third-party providers) and use creative specificity to filter for ICP. The algorithm (Andromeda + Gem) does the rest.

## Routing Logic

### Always Load First

**Any Meta work starts here:**

| Intent | File | Priority |
|--------|------|----------|
| **ANY operational decision** (pause, scale, graduate, budget, creative count) | [meta-ads-operating-system.md](knowledge-base/meta-ads-operating-system.md) | ALWAYS LOAD FIRST. This is THE decision framework. All formulas, thresholds, and actions live here. |
| **Auditing an account** (pull data, classify ads, produce recommendations) | Load the OS file above + run `scripts/get_active_ads_copy.py` | Pull active ads, classify by OS rules, produce recommendations. |
| **Creative production decisions** (what to build, when to iterate, cadence, formats) | [creative-cadence-operating-system.md](knowledge-base/creative-cadence-operating-system.md) | Iteration hierarchy, concept sourcing, format playbook, testing cadence, fatigue detection, quality scoring. |

### Deeper Context (Load When Needed)

These files provide detailed methodology on specific topics. The OS drives decisions; these explain the deeper why and how.

| User Intent | Knowledge Base File | When to Use |
|-------------|-------------------|-------------|
| Full Meta B2B overview, algorithm, strategy | [meta-b2b-overview.md](knowledge-base/meta-b2b-overview.md) | Andromeda + Gem, strategy, "what works" - overview and quick reference |
| Pixel, tracking, first campaign setup | [meta-setup-and-tracking.md](knowledge-base/meta-setup-and-tracking.md) | Installing the pixel, Events Manager, domain verification, CAPI, pre-launch |
| CAPI, conversion events, HubSpot vs n8n | [meta-capi-and-events.md](knowledge-base/meta-capi-and-events.md) | Conversions API, event hierarchy, CRM to CAPI, deduplication, Event Match Quality |
| Webinar/event, third-party conversion | [meta-third-party-conversion-tracking.md](knowledge-base/meta-third-party-conversion-tracking.md) | Off-domain conversion (Luma, etc.), pixel in platform vs thank-you page |
| Audience targeting, data strategy, lookalikes | [audience-strategy.md](knowledge-base/audience-strategy.md) | Building audiences, data sources, audience validation, third-party tools |
| Detailed campaign structure, phases, roadmap | [campaign-structure.md](knowledge-base/campaign-structure.md) | Phase 1/2/3 deep dive, naming conventions, campaign architecture, month-by-month roadmap |
| Creative concepts, copy, formats | [creative-strategy.md](knowledge-base/creative-strategy.md) | Creative development, concept testing, placement optimization, creative-as-targeting |
| Creative fatigue detection, rotation system | [creative-fatigue-detection.md](knowledge-base/creative-fatigue-detection.md) | Full fatigue workflow, rotation cadence, pipeline management, format-specific notes |
| Advantage+ setup and details | [advantage-plus.md](knowledge-base/advantage-plus.md) | When to use Advantage+, setup steps, budget requirements, ABM considerations |
| Optimization playbook, benchmarks | [optimization-playbook.md](knowledge-base/optimization-playbook.md) | Decision trees, B2B benchmarks, seasonal patterns, weekly cadence, scaling protocol |
| Ad quality scoring, message validation | [message-validation.md](knowledge-base/message-validation.md) | Scoring ads against revenue quality, winner scaling pattern, validation process |
| Lead forms, conversion optimization | [lead-form-optimization.md](knowledge-base/lead-form-optimization.md) | Lead form setup, work email validation, custom questions, social amnesia |
| ABM on Meta | [abm-on-meta.md](knowledge-base/abm-on-meta.md) | ABM targeting, Advantage+ conflicts, manual vs hybrid approach |
| Offer strategy by funnel stage | [offer-strategy.md](knowledge-base/offer-strategy.md) | What offers to run at each funnel stage |

## Core Rules

1. **Never cite external sources** in client-facing materials. Present methodology as internal expertise.

2. **Data quality determines Meta success for B2B.** Always follow the data hierarchy: CRM lookalikes (Tier 1) -> Third-party data (Tier 2) -> Broad targeting (Tier 3). Never skip to broad without testing data-driven audiences first.

3. **Validate audience quality before scaling creative.** Use ABO (ad set budget) campaigns with one ad set per audience source and the same ads across all. Audit lead quality by job title and company. Only scale winning audiences with CBO.

4. **Creative concept testing, not micro-variations.** Test dramatically different concepts (UGC vs before/after vs meme vs product demo), not minor tweaks (blue vs green button). The algorithm needs creative diversity to learn.

5. **Creative IS targeting on Meta.** Your ad copy must explicitly call out who the ad is for. When running broader audiences, the creative does the filtering work — it should act as "mosquito repellent" for non-ICP.

6. **Lead forms need intentional friction for B2B.** Always require work email validation. Add 1-3 custom qualification questions. Use Higher Intent form type. This combats social amnesia and improves lead quality.

7. **Build in this order: Remarketing -> Prospecting -> Acceleration.** Start with remarketing (lowest risk, highest ROI, creates omnipresence). Layer prospecting once remarketing is running. Add acceleration for open pipeline if applicable.

8. **Cross-channel remarketing is a superpower.** Create Meta retargeting audiences from LinkedIn/Google traffic using UTM parameters. You retarget validated audiences on Meta at a fraction of the cost.

9. **Broad targeting only works for large TAM.** If you're doing ABM or targeting niche enterprise, broad will not work — stick to Tier 1 and Tier 2 data sources. Broad is for SMB/lower mid-market with massive addressable markets.

10. **Meta's algorithm (Andromeda + Gem) needs creative volume.** Maintain 4-6 unique creative concepts per campaign. The algorithm processes ads to learn what works — more diverse inputs = better optimization.

## Key Differences from LinkedIn

| Aspect | Meta | LinkedIn |
|--------|------|----------|
| Native B2B targeting | Weak — bring your own data | Strong — job title, company, seniority |
| Cost per lead | ~50% of LinkedIn | Higher but more precise |
| Algorithm role | Heavy — drives targeting through creative signals | Light — advertiser controls targeting |
| Creative volume needed | High (4-6+ unique concepts) | Moderate (4-6 per campaign) |
| Remarketing strength | Excellent — cheap, cross-platform omnipresence | Good but more expensive |
| Lead form quality | Requires friction management (social amnesia risk) | Higher quality by default (work email auto-fill) |
| Best for | Large TAM, SMB/mid-market, remarketing, pipeline acceleration | Enterprise, ABM, precise ICP targeting |

## Output Standards

- Campaign plans -> Use docx skill for professional Word documents
- Performance reports -> Use xlsx skill for data-driven spreadsheets
- Creative briefs -> Structured concept descriptions with placement specs
- All documents -> Professional, client-ready quality. No source citations.

## When to Combine with LinkedIn

Meta and LinkedIn are not competitors — they're complementary channels:

- **LinkedIn for precision prospecting** (right person, right company) + **Meta for cheap remarketing** (stay top of mind across platforms)
- **LinkedIn for ABM** (company-level targeting) + **Meta for ABM extension** (via third-party tools like Primer/Metadata.io)
- **LinkedIn for enterprise** (where precision justifies the cost) + **Meta for mid-market/SMB** (where volume and cost efficiency matter more)
- Use cross-channel UTM remarketing to bridge the two platforms
