# Campaign Group Structures & Naming Conventions

## 6 Campaign Group Structure Models

Choose the right structure based on account complexity. For new accounts, start with structures 1-4. Scale to Pick and Mix as the account grows.

### 1. Objective-Based Structure

Organize groups by campaign objective. Makes it easy to measure performance against goals.

| Group | Objective | Example Campaigns |
|-------|-----------|-------------------|
| Awareness | Brand Awareness, Video Views | Brand video campaigns, thought leadership |
| Engagement | Engagement, Website Visits | Content/blog promotion, resource downloads |
| Conversion | Lead Gen, Website Conversions | Demo requests, free trial signups |

**Best for:** Simple accounts with one product/audience, small budgets.

### 2. Audience-Based Structure

Segment groups by target audience. Best when you have diverse markets with different messaging needs.

| Segment Type | Example Groups |
|-------------|----------------|
| Demographic | VP+ Engineering, Director+ Marketing, C-Suite |
| Geographic | US - Marketing, UK - Product, DACH - Engineering |
| Interest-Based | AI/ML Practitioners, DevOps Community |

**Best for:** Companies targeting multiple distinct personas or regions with tailored messaging.

### 3. Funnel Stage Structure

Align groups with the buyer's journey. This is the approach most recommended across all sources.

| Group | Stage | Content Type |
|-------|-------|-------------|
| TOF - Problem Aware | Prospecting cold audiences | Educational content, pain-point validation |
| MOF - Solution Aware | Retargeting engaged users | Case studies, comparisons, demos |
| BOF - Product Aware | Retargeting high-intent | Direct CTA, social proof, Lead Gen Forms |

**Best for:** Most B2B SaaS accounts. This is the default recommendation.

### 4. Product or Service Line Structure

Organize around each product/service for focused messaging and better tracking.

| Segment Type | Example Groups |
|-------------|----------------|
| By Product/Service | Voice AI Platform, Contact Center Analytics |
| By Use Case | Outbound Calling, Inbound Support, Appointment Setting |

**Best for:** Multi-product companies or companies with distinct use cases.

### 5. Testing Structure

Dedicated groups for controlled experiments. Essential for optimizing performance over time.

| Test Type | What You're Testing |
|-----------|-------------------|
| A/B Creative Tests | Different creatives or messaging within the same audience |
| Audience Tests | Comparing performance across different audience segments |
| Offer Tests | Trialling different offers or CTAs to see what resonates |

**Best for:** Mature accounts with enough budget to allocate to experimentation.

### 6. Pick and Mix Structure (Advanced)

For large accounts at scale, combine elements from multiple structures into one unified approach.

**Group naming data points:** Region, Persona, Seniority, Company Size, Product Line, Objective

**Example:** `US | VP+ Engineering | Enterprise | Voice AI | TOF`

Each group contains multiple campaigns. This is the only way to manage campaigns at scale without losing control.

**Best for:** Accounts spending $10K+/month with multiple products, regions, and personas. For starters, structures 1-4 are enough.

## Naming Convention System

Consistent naming is critical for reporting, filtering, and management at scale.

### Campaign Group Naming

Two conventions in use. Choose based on how you're structuring:

**Convention A — Stage + Awareness (5-Stage Demand Engine template):**
Format: `[Region] - [Stage] - [Awareness] - [Type] - {Detail}`

Examples:
- `NA - Capture - Solution Aware - Prospecting - {Persona}`
- `NA - Capture - Product Aware - Remarketing (Offers)`
- `NA - Activate - Offer Aware - Remarketing (Free Users)`
- `NA - Revive - Offer Aware - Remarketing (Closed Lost)`

**Convention B — Product/Persona focused (simpler):**
Format: `[Region] | [Product/Persona] | [Funnel Stage]`

Examples:
- `US | Voice AI | TOF - Prospecting`
- `UK | Contact Center | MOF - Retargeting`
- `Global | Brand | BOF - Conversion`

Convention A is better for accounts using the 5-Stage Demand Engine model. Convention B is simpler for basic 3-layer funnels.

### Campaign Naming

Format: `[Audience Type] - [Targeting Detail] - [Objective]`

Examples:
- `Cold - VP+ Engineering - Engagement`
- `Retarget - Website Visitors 30d - Lead Gen`
- `Lookalike - Converted Users - Website Conversions`

### Ad Naming

Format: `[Persona]_[Format]_[Creative#]_[CopyVariant]_{Date}`

Examples:
- `SalesDirector_Image1_Text1_2024-01`
- `VP_Engineering_Video2_TextA_2024-02`
- `CTO_Carousel1_TextB_2024-03`

This naming system enables:
- Quick filtering by any dimension in Campaign Manager
- Clean data exports for reporting tools (Looker Studio, etc.)
- Easy identification of what's running and what needs rotation

## 7. The Five Campaign Groups (Advanced Scaling)

At scale, organize campaigns into five purpose-driven groups. This replaces the simple awareness/retargeting split when you have enough budget and campaigns.

| Group | Purpose | Content Type | Priority Order |
|-------|---------|-------------|----------------|
| Product Value | Showcase what your product does and why it matters | Product demos, feature highlights, use cases | 1st (start here) |
| Remarketing | Re-engage people who already interacted | Demo offers, case studies, testimonials | 2nd |
| Content | Drive traffic with valuable knowledge | Reports, guides, blog posts, educational content | 3rd |
| Social Proof | Build trust through third-party validation | Customer testimonials, case studies, awards, reviews | 4th |
| Thought Leadership | Build brand affinity through expertise | Founder insights, industry analysis, opinion pieces | 5th (add last) |

**Funnel mapping:**
- Awareness stage -> Thought Leadership + Product Value groups
- Consideration stage -> Content + Social Proof groups
- Conversion stage -> Remarketing group

**Best for:** Accounts with 5+ campaigns and $5K+/month budget. Start with Product Value + Remarketing, add the others as budget grows.

## Splitting Campaigns by Type

Different campaign types (static, video, document, carousel, conversation, message ads) have different auctions on LinkedIn. Diversifying ad types is an auction strategy, not just a creative one.

**Key insight:** Static ads have the most competition. Document ads targeting the same audience will have less auction competition, leading to cheaper cost per reach.

**When to introduce a new campaign type:**
- Current campaign meeting/exceeding KPIs (audience is receptive, test more)
- Current campaign underperforming with no obvious issues (audience not receptive to format, try different)

**Campaign group budget option:** LinkedIn's campaign group budget lets the algorithm split budget between campaigns in a group. Caveat: LinkedIn favors video ads — you may see 80%+ of budget go to video when mixing static + video. For full budget control, use separate campaigns. See scaling-strategy.md for detailed findings.

## Scaling the Group Structure

As you scale, group naming should evolve in layers:

**Level 1 — Persona + Intent:**
- `Marketing - Awareness`
- `Marketing - Remarketing`
- `Sales - Awareness`
- `Sales - Remarketing`

**Level 2 — Add campaign group type:**
- `Sales - Awareness - Product Value`
- `Sales - Awareness - Content`
- `Sales - Remarketing - Demo`
- `Sales - Remarketing - Case Studies`

**Level 3 — Add region:**
- `Sales - Awareness - EMEA - Content`

**Level 4 — Add company size:**
- `Sales - Awareness - Product Value - Enterprise`

**Level 5 — Add audience segment:**
- `Sales - Awareness - Product Value - Enterprise - Decision Makers`

Under each group: individual campaigns with different creative types (static, video, document campaigns).

**When to split groups:** Start right away. Even with only 4 campaigns, put them in separate groups by persona and intent. Waiting creates a mess where group-level metrics mask individual performance. One strong retargeting campaign can make the entire mixed group look healthy while awareness campaigns silently fail.

**Moving campaigns between groups:** LinkedIn doesn't allow it. You must duplicate the campaign (losing historical data). Short-term pain, long-term clarity.

## Creative Rotation Configuration

When launching new ads within a campaign:
1. **Start with even rotation** — so each ad gets equal budget
2. **After 7-10 days** — check the data to see which ads perform best
3. **Then switch to auto rotation** — let the algorithm optimize delivery toward winners

This prevents the algorithm from prematurely picking a "winner" before enough data is collected.
