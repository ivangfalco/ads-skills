# Audience Sizing & Targeting

## Cold Audience Sizing

No single ideal size — but all sources agree: too narrow kills performance.

| Recommended Range | Notes |
|------------------|-------|
| 60K-400K | Smaller can work (10K-100K) with right bidding |
| 50K-300K | If total addressable < 30K, skip TOF/BOF split — saturate with all layers |
| 100K+ for prospecting | ICP-first: start with ideal customers, expand over time |

**What happens when too narrow:**
- CPMs spike (can reach 896% above benchmark in extreme cases)
- Algorithm can't optimize — not enough data points
- Audience penetration stays low (can drop to only 5.5%)
- Budget doesn't spend fully regardless of bid amounts

## Retargeting Audience Sizing

Smaller audiences are fine here — these are warm prospects.

| Audience Type | Recommended Size | Window |
|--------------|-----------------|--------|
| Website visitors (all) | Varies | 30-day, 90-day, 180-day |
| Website visitors (high-intent pages) | 1K-5K | 30-day |
| Video viewers (50%+) | 5K-20K | 30-day, 90-day |
| Video viewers (97%+) | 1K-5K | 30-day (highest intent) |
| Ad engagers | 5K-20K | 90-day |
| Company page visitors/followers | Varies | 180-day or lifetime |
| Lead Gen Form openers (non-submitters) | Varies | 90-day |
| Demo/pricing page visitors | 1K-5K | 30-90 day |
| Conversation Ad clickers | Varies | 90-day |

## Retargeting Audience Setup Checklist

**Critical timing note:** Set up ALL retargeting audiences IMMEDIATELY — before launching any campaigns. LinkedIn retargeting audiences are NOT retroactive. They only start collecting members from the moment you create them. If you wait 3 months to set up a 90-day website visitor audience, you've lost 3 months of data that can never be recovered.

Create ALL of these before launching campaigns:

1. Website visitors: 30-day, 90-day, and 180-day windows (requires LinkedIn Insight Tag)
2. Video viewers (50%+): 30-day and 90-day
3. Video viewers (97%+): 30-day (for BOF)
4. Single image ad engagers: 90-day
5. Company page visitors/followers: 180-day or lifetime
6. Lead Gen Form openers (non-submitters): 90-day
7. Demo/pricing page visitors: 30-day and 90-day
8. Conversation Ad CTA clickers: 90-day

## What Happens When You Broaden an Audience

When you expand an audience (e.g., removing a company size filter, increasing the targeting scope), the following is **expected behavior**:

- **CPMs go down** — more inventory available, less competition for the broader pool
- **CPCs go down** — same reason, lower cost to reach people
- **CTR drops** — the broader audience is less relevant/targeted, so fewer people engage
- **Engagement rate drops** — same reason as CTR
- **CPCTLP may improve OR worsen** — depends on whether the cost savings outweigh the lower click-through rates

This is normal. A broader audience means LinkedIn's algorithm has more room to optimize delivery cost, but the people being reached are less precisely matched to the product. The trade-off is: lower cost per impression but lower engagement quality.

**Do not flag CTR or engagement rate declines as "unexpected" or "interesting" when the audience was broadened. It is the expected outcome.**

## Targeting Do's and Don'ts

| DO | DON'T |
|----|-------|
| Keep cold audiences 50K-300K | Split into micro-segments under 10K |
| Use 2-3 broad industry groups per campaign | Create separate campaigns per industry |
| Target Director+ seniority for decision-makers | Target specific job titles only (too narrow) |
| Turn OFF Audience Expansion | Leave Audience Expansion on (wastes budget) |
| Turn OFF LinkedIn Audience Network | Enable Audience Network (dilutes quality) |
| Build retargeting audiences for 30/90/180 days | Skip retargeting setup |
| Use AND narrowing for audience parameters | Use OR (too broad) |
| Exclude competitors and existing customers | Leave them in cold campaigns |
| Exclude converted audiences from all campaigns | Retarget people who already converted |
| Exclude unpaid, training, entry seniority | Target all seniority levels |
| Exclude agency/business employees | Let irrelevant roles eat budget |
| Group campaigns by similar countries | Mix countries with very different CPAs |
| Test lookalike audiences | Ignore lookalikes entirely |
| Don't use age/gender/language targeting | Use these — LinkedIn has limited data |

**Note on Job Titles vs Seniority:** On LinkedIn, job title targeting and seniority targeting are **mutually exclusive** — you cannot use both simultaneously in the same campaign. Choose one approach: either target specific job titles OR target by seniority level (e.g., Director+). This means excluding entry-level seniority is only possible when using seniority-based targeting, not when targeting specific job titles.

## Job Functions vs Job Titles: The $500K Test

A 6-month experiment spending $500K+ to compare job function targeting vs job title targeting.

**The problem:** Pipeline data showed 35 different job titles from the sales persona, with 80+ on a quarterly view. But LinkedIn demographics showed the variety of titles in the paid pipeline was less than half of the blended pipeline — paid ads were missing ICP members with unexpected titles.

**The test:** Switched underperforming campaigns from specific job titles to "job functions + seniorities" targeting.

**Results after 8 weeks:**
- Target audience size tripled
- Engagement rate stayed similar
- Reach was 2x better
- Cost per reach was 1.6x cheaper
- Required ongoing negative filtering of irrelevant titles (regional managers, call center supervisors, branch managers, fashion designers, telemarketers)

**The approach:** Monitor demographics report weekly. Exclude every irrelevant job title that appears — like adding negative keywords in Google Ads. Over ~8 weeks, the irrelevant titles stop appearing.

### When to Use Job Title Targeting
- You are 100% certain who your ICP is and their exact titles
- You want maximum focus and precision
- You're willing to pay higher costs for that precision
- Your audience is large enough with just title targeting

### When to Use Job Function Targeting
- Your ICP has multiple different titles (SDRs, MDRs, heads of sales, AEs, etc.)
- You want broader reach (e.g., marketers skilled in digital marketing, not just "digital marketers")
- Your audience size is too small with title targeting
- You want to explore a new persona and discover which titles exist
- You're scaling and need cost-efficient reach

**Summary:** Job titles give you focus. Job functions give you more options, cheaper reach, and better penetration — but require active negative filtering.

### Critical: Business Development Function Includes CEOs

LinkedIn's Business Development job function explicitly includes CEOs, CMOs, Managing Directors, and other executive roles involved in partnerships, M&A, and business initiatives. Do NOT exclude Business Development function if your ICP includes C-suite - you will lose CEOs from the audience.

**What BD function captures:**
- CEOs, CMOs, Managing Directors (ICP-relevant)
- Business Development Managers, M&A Specialists (may or may not be ICP)
- SDRs, BDRs, Regional Managers, Call Center Supervisors (usually not ICP)

**Correct approach:** Instead of excluding BD function, use seniority exclusions (Entry, Senior, Manager) to filter out non-executive BD roles while keeping CXO/VP/Director-level professionals. This is more precise than a blanket function exclusion.

## Splitting Audiences for Scale

Once initial campaigns are running, scale by splitting audiences across these dimensions. Priority order: intent > persona > region/company size > seniority.

### Splitting by Region

| Region Strategy | Recommendation |
|----------------|---------------|
| US | Always separate — most expensive market |
| UK | Separate if budget allows |
| DACH (Germany, Austria, Switzerland) | Separate from English-speaking markets — different language/content needed |
| UK + Canada + Australia | Can group together if budget is tight (English-speaking, similar costs) |
| Other markets | Group by language and cost similarity |

**Minimum audience per cold campaign:** 15,000 members. If splitting a region drops below this, combine with a similar region.

**Language considerations:**
- France and Germany: English ads underperform compared to local-language ads — create localized content
- Nordic countries, Netherlands, Middle East: English ads perform fine — no localization needed
- If grouping an expensive/crowded market (US, UK) with smaller markets, most budget goes to the crowded market, starving the others. Keep expensive markets separate.

### Splitting by Company Size

| Segment | Employee Count | Characteristics |
|---------|---------------|-----------------|
| SMB | 0-200 employees | Faster sales cycles, lower ACV, cost-sensitive |
| Mid-Market | 200-500 employees | Moderate sales cycles, balanced ACV |
| Enterprise | 500+ employees | Longer sales cycles, higher ACV, multi-stakeholder |

**Rules:**
- Use employee count, not revenue — LinkedIn has no access to private company revenue data, only estimates. Employee count is accurate.
- Start with 2 splits, not 3 (e.g., SMB + Enterprise combined, or SMB vs Mid-Market/Enterprise)
- The 500-employee threshold is the standard enterprise cutoff — buying processes get significantly slower above this
- Also split by industry when product has significantly different use cases per vertical
- **LinkedIn distribution bias:** If you target all company sizes together, LinkedIn will show your ads mostly to companies with 50-200 employees and 10,000+ employees (most LinkedIn users work at these sizes). Mid-market companies (200-5,000) get underserved. Splitting by size forces fair distribution.

### Splitting by Seniority / Audience Role

Split into decision-makers vs individual contributors when product is used by one group but purchased/approved by another.

**Why:** Decision-makers get ROI-focused ads. Individual contributors get daily-task-focused ads showing how the product helps their work. Contributors influence the purchase decision (sometimes called "dark social").

**Three ways to split:**

1. **Decision-makers vs Individual contributors** (most common)
   - Campaign 1: Directors, VPs, C-levels -> ROI/strategic messaging
   - Campaign 2: Managers, specialists, executives -> Productivity/daily-use messaging

2. **By job title groups**
   - Campaign 1: Marketing managers, specialists
   - Campaign 2: Marketing directors, VP Marketing, CMO

3. **By job function + seniority levels**
   - Campaign 1: Marketing function + entry, senior, manager seniorities
   - Campaign 2: Marketing function + director, VP, C-level seniorities

**Note:** Splitting by years of experience is rare and only useful when product use case depends on experience. LinkedIn counts total experience including unrelated jobs — "5+ years" may include unrelated prior roles. Splitting by member skills is very rare (pharmaceutical/highly technical products only).

**When to split by seniority:** Only after campaigns are already split by intent, persona, region, and company size. Each split requires unique messaging, creatives, and landing pages.

**Track influence, not just conversions:** One audience may not convert directly but influences the purchase. Use attribution tools to track the LinkedIn impression journey and tie impressions to pipeline even when they don't directly convert. Example: A CMO sees the ad, likes it, sends it to their team, and the team takes action — the CMO's campaign appears to have zero conversions but actually drove the deal. Set up self-reported attribution ("how did you find us?") alongside impression-based attribution to capture dark social influence.

## Audience Expansion Models

Three types of audience expansion on LinkedIn. Use as a **last resort** — try job functions, different industries, different regions first.

| Model | Source | How Created | Setup Time | Audience Size | When to Use |
|-------|--------|-------------|-----------|--------------|-------------|
| Audience Expansion | Professional demographics | LinkedIn algorithm finds similar profiles | Auto-enabled (turn OFF) | Depends on campaign + budget | Using specific facets where you might miss members |
| Lookalike | Any matched audience list | 1st-party data + LinkedIn algorithm | 48-72 hours | 5x-10x of source audience | Expanding account lists or retargeting lists |
| Predictive Audience | Contact list, conversions, or lead gen forms | Predictive AI + your data | 4-5 days | Adjustable slider, max 10% of location population | Controlling size by geo-location with conversion data |

**Critical:** Audience Expansion is auto-enabled in campaign setup. Always turn it OFF. LinkedIn's similarity matching is unreliable — e.g., targeting marketing managers -> LinkedIn finds Harvard attendance pattern -> targets Harvard alumni regardless of role.

**Match rates across all three models are generally low and unqualified.** Test extensively before committing meaningful budget.

## Cross-Channel Retargeting: Paid Search + LinkedIn

For companies spending $30K+/month on paid search (Google Ads, Bing Ads), create a cross-channel retargeting strategy:

**How it works:**
1. Tag all paid search traffic with UTM parameters (e.g., `utm_source=google`, `utm_medium=cpc`, or `utm_source=paid_search`)
2. Create a custom LinkedIn remarketing audience filtering for website visitors with those specific UTM parameters
3. Run LinkedIn retargeting campaigns specifically to people who came from paid search

**Why this is powerful:** Paid search visitors have demonstrated active buying intent (they searched for your solution). Retargeting them on LinkedIn with brand-building and social proof content reinforces the brand during their evaluation process. This combines intent signals from search with LinkedIn's professional targeting.

**Minimum threshold:** Only worth the effort if paid search drives $30K+/month in spend and generates meaningful traffic volume. Below that, the retargeting audience will be too small to serve ads to.

## LinkedIn Sales Navigator as Audience Extension

LinkedIn Sales Navigator provides a complementary organic outreach channel alongside paid ads.

**Profile visitor connection strategy:** When someone views your LinkedIn profile (often triggered by seeing your ads or TLAs), send them a blank connection request through Sales Navigator. Acceptance rate on these is approximately 60% — significantly higher than cold connection requests — because they've already shown interest by visiting your profile.

**How to operationalize:**
- Check profile visitors daily in Sales Navigator
- Send connection requests to visitors who match your ICP
- Do not include a sales pitch in the connection request (blank performs best)
- Once connected, nurture through organic content in their feed
- After a few touchpoints, initiate a conversation naturally

This creates a free, organic layer on top of your paid ABM and awareness campaigns.

## Audience Exclusion Layers

Apply these in order of priority:

1. **Essential:** Converted users excluded from ALL campaigns
2. **Essential:** Competitors and existing customers excluded from cold
3. **Essential:** Website visitors excluded from prospecting (they go to retargeting)
4. **Preferred:** Unpaid/entry-level seniority excluded
5. **Preferred:** Agency and business employees excluded
6. **Optional:** Lookalike audiences not mixed with job title/skill audiences in same ad set
