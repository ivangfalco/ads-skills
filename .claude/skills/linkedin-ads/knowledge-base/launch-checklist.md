# LinkedIn Ads Launch Checklist

8-part checklist to follow before launching any new LinkedIn Ads campaign. Go through each part sequentially — each builds on the previous.

## Part 1: Design Your Group & Campaign Structure

- [ ] Align on group structure type (see campaign-structures.md for the 6 models)
  - Consider: Region, Offer/Persona as grouping dimensions
- [ ] Apply naming conventions to all groups
  - Format: `[Region] | [Product/Persona] | [Funnel Stage]`
- [ ] Ensure structure separates prospecting vs retargeting

## Part 2: Select Ad Formats

Choose the optimal ad format for your campaign goals:

| Format | Best Objective | Notes |
|--------|---------------|-------|
| Single Image | All stages | Most versatile, moderate performance |
| Carousel Image | MOF/BOF | Feature showcases, multi-point storytelling |
| Video | TOF awareness | Strong for building retargeting pools |
| Text Ads | MOF brand reinforcement | Cheapest, always-on |
| Spotlight | MOF reinforcement | Very cheap CPM (~$5.23) |
| Event | Event promotion | For webinars, product launches |
| Conversation | MOF/BOF | 1-5% CTR, interactive experience |
| Message Ads | BOF | Direct inbox delivery |
| Document | MOF nurture | High engagement, great for retargeting |

**Priority format:** TLAs (Thought Leader Ads) should be primary for most campaigns.

## Part 3: Choose Campaign Objective

Select the optimal objective for your goals:

| Objective | When to Use | Funnel Stage |
|-----------|------------|-------------|
| Brand Awareness | Maximum reach, early market entry | TOF |
| Website Visits | Drive traffic to content/landing pages | TOF/MOF |
| Video Views | Build retargeting pools, awareness | TOF |
| Engagement | Social proof, content amplification | TOF |
| Lead Generation | On-platform form fills (lower friction) | BOF |
| Website Conversions | Off-platform conversion tracking | BOF |
| Talent Leads | Recruiting campaigns | N/A |
| Job Applicants | Recruiting campaigns | N/A |

**Key rule:** Each campaign should have the correct conversion event selected.

## Part 4: Create the Ideal Campaign Structure

Brainstorm campaign structure based on:
- **Regions** — Group similar countries (CPAs vary significantly by region)
- **Personas** — Separate campaigns for distinct ICPs
- **Budget/Goals** — Ensure each campaign gets enough budget for 10+ results/week

**Critical settings to verify:**
- [ ] Audience Expansion -> **OFF**
- [ ] LinkedIn Audience Network -> **OFF**
- [ ] Age/gender/language targeting -> **NOT USED** (LinkedIn has limited data)

## Part 5: Calculate Starting Campaign Budget

Select budget type:
- **Daily budget** (recommended) — more predictable spend, easier to control
- **Lifetime budget** — only for time-bound campaigns with fixed end dates

**Budget sizing rule:** Each campaign needs enough daily budget to generate at least 10 results/week (ideally 30).

Quick math: If your target CPA is $50, you need at least $50 x 10 / 7 = ~$72/day per campaign.

## Part 6: Pick Bid Strategy & Optimization Goal

| Campaign Phase | Bid Strategy | Rationale |
|---------------|-------------|-----------|
| Week 1 (new campaign) | Automated / Maximum Delivery | Let algorithm learn |
| Week 2+ | Manual CPC at 20% below avg CPC | Significant cost reduction |
| Small retargeting/ABM | Keep automated | Manual bidding causes underdelivery on tiny audiences |

**Optimization goal** should match your campaign objective. Don't optimize for clicks if you want conversions.

## Part 7: Creative Reporting & Configuration

- [ ] **Turn on even ad rotation** — each ad gets equal budget initially
- [ ] **After 7-10 days** — review data, then switch to auto rotation
- [ ] **Apply naming conventions per ad** — enables clean reporting
  - Format: `[Persona]_[Format][#]_[Copy][#]_{Date}`
  - Example: `SalesDirector_Image1_Text1_2024-01`
- [ ] **Minimum 4 active ads per campaign**
- [ ] **Mix formats** — video, document, image, carousel

## Part 8: Final Launch Check

Before hitting "Launch", verify each of these:

- [ ] Group structure has clear naming conventions and logical organization
- [ ] Ad formats are optimal for your campaign goals
- [ ] Campaign settings are correct (audiences, locations, audience expansion OFF, bidding)
- [ ] UTM parameters are correct and verified with MOPs team for proper routing
- [ ] Budget is sufficient per campaign for the selected objective
- [ ] Ads are named properly for reporting
- [ ] Even ad rotation is enabled (switch to auto after 7-14 days)
- [ ] Conversion events fire on actual completion, not button click
- [ ] Website visitors excluded from prospecting campaigns
- [ ] Converted audiences excluded from ALL campaigns

## Post-Launch (First 7 Days)

After launching, monitor daily:
1. **Are campaigns spending?** If not, audience too small or bid too low
2. **Is the CTR reasonable?** Below 0.30%, creative or targeting issue
3. **Are conversions firing?** Check in Campaign Manager AND your analytics tool
4. **Demographics check** — any irrelevant titles/industries eating budget? Exclude immediately
