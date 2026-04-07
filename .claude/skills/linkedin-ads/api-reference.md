# LinkedIn Ads API Reference (v202601)

Comprehensive endpoint and schema reference for the LinkedIn Marketing API.

**Related files:**
- `linkedin_api.py` - Python client
- Knowledge base files in `knowledge-base/`

---

## Quick Start

```bash
cd "scripts/linkedin"
python3 <script>.py [args]
```

No venv needed - uses system Python with `requests` and `python-dotenv`.

## Configuration
- **Access token:** in `.env` as `LINKEDIN_ACCESS_TOKEN`
- **API version:** `202601` (set in `LinkedIn-Version` header)
- **Base URL:** `https://api.linkedin.com/rest`

---

## Headers (Required for ALL Calls)

```python
headers = {
    'Authorization': f'Bearer {token}',
    'LinkedIn-Version': '202601',
    'X-Restli-Protocol-Version': '2.0.0',
    'Content-Type': 'application/json',  # For POST/PUT
}
```

Additional method-specific headers:
- `X-RestLi-Method: PARTIAL_UPDATE` - for update operations
- `X-RestLi-Method: BATCH_CREATE` - for batch create
- `X-RestLi-Method: BATCH_PARTIAL_UPDATE` - for batch update
- `X-RestLi-Method: BATCH_GET` - for batch get
- `X-RestLi-Method: FINDER` - for search/criteria queries
- `X-RestLi-Method: DELETE` - for delete operations

---

## Account Hierarchy

```
Ad Account (sponsoredAccount)
  └── Campaign Group (sponsoredCampaignGroup)
       └── Campaign (sponsoredCampaign)
            └── Creative (sponsoredCreative) → references Post (ugcPost/share)
```

**Limits:**
- 5,000 campaigns per account (any status)
- 1,000 concurrent ACTIVE campaigns
- 2,000 campaigns per non-default campaign group
- 15,000 creatives per account
- 100 creatives per campaign (15 active + 85 inactive)

---

## Campaign Group Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| account | SponsoredAccountUrn | Yes | `urn:li:sponsoredAccount:{id}` |
| name | string | Yes | Max 100 characters |
| status | string | Yes | ACTIVE, PAUSED, DRAFT, ARCHIVED, CANCELLED, PENDING_DELETION, REMOVED |
| runSchedule.start | long | Yes | Epoch ms - inclusive start date |
| runSchedule.end | long | No | Epoch ms - exclusive end date. Required if totalBudget set |
| totalBudget.amount | BigDecimal | No | Max lifetime spend. Currency must match account |
| totalBudget.currencyCode | Currency | No | ISO currency code |
| dailyBudget | BigDecimal | No | Daily budget (only if budgetOptimization.budgetOptimizationStrategy is DYNAMIC, v202504+) |
| objectiveType | string | No | Immutable. Campaigns inherit this objective |
| budgetOptimization.bidStrategy | string | No | MAXIMUM_DELIVERY, MANUAL, COST_CAP (v202501+) |
| budgetOptimization.budgetOptimizationStrategy | string | No | DYNAMIC - shares budget across campaigns (v202501+) |
| backfilled | boolean | Read-only | true = default group (auto-created with account) |
| test | boolean | Read-only | true = test account |
| servingStatuses | string[] | Read-only | RUNNABLE, STOPPED, BILLING_HOLD, etc. |
| allowedCampaignTypes | string[] | Read-only | ENTERPRISE accounts only |
| id | long | Read-only | Campaign group ID |

**Notes:**
- Every ad account auto-creates a default campaign group (backfilled=true)
- ENTERPRISE accounts: cannot update default group via API, non-default groups only allow name and status updates
- No limit on number of campaign groups per account

---

## Campaign Schema

### Core Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| account | SponsoredAccountUrn | Read-only | Set automatically from URL path |
| name | string | Yes | Campaign name |
| campaignGroup | SponsoredCampaignGroupUrn | Yes | `urn:li:sponsoredCampaignGroup:{id}` |
| type | string | Yes | SPONSORED_UPDATES, SPONSORED_INMAILS, TEXT_AD, DYNAMIC |
| status | string | Yes | ACTIVE, PAUSED, DRAFT, ARCHIVED, COMPLETED, CANCELED, PENDING_DELETION, REMOVED |
| associatedEntity | URN | Conditional | `urn:li:organization:{id}` - required for Sponsored Content, Dynamic Ads, Lead Gen |
| objectiveType | string | Yes | See Objective Types table below |
| optimizationTargetType | string | No | See Bidding Matrix below |
| costType | string | Yes | CPM, CPC, CPV |
| format | string | Conditional | Required for DYNAMIC type and video/carousel. See Format Types |
| locale.country | string | Yes | Uppercase 2-letter ISO-3166 (e.g. "US") |
| locale.language | string | Yes | Lowercase 2-letter ISO-639 (e.g. "en") |
| targetingCriteria | object | Yes | See Targeting section |

### Budget & Bidding Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| dailyBudget.amount | BigDecimal | Conditional | Max daily spend (UTC). Either daily or total required |
| dailyBudget.currencyCode | Currency | Conditional | Must match account currency |
| totalBudget.amount | BigDecimal | Conditional | Max lifetime spend |
| totalBudget.currencyCode | Currency | Conditional | Must match account currency |
| unitCost.amount | BigDecimal | Yes | Bid amount. 0 for auto-bidding |
| unitCost.currencyCode | Currency | No | Defaults to account currency |

**Budget rules:**
- Either `dailyBudget` OR `totalBudget` required
- DYNAMIC type campaigns MUST set BOTH daily and total
- When switching optimizationTargetType, ALWAYS update unitCost too

### Creative & Delivery Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| creativeSelection | string | No | OPTIMIZED (default) or ROUND_ROBIN |
| audienceExpansionEnabled | boolean | No | Default: false |
| offsiteDeliveryEnabled | boolean | Yes | LinkedIn Audience Network delivery |
| connectedTelevisionOnly | boolean | No | CTV-only campaigns (v202408+) |
| storyDeliveryEnabled | boolean | No | Story format delivery |
| politicalIntent | string | Yes (v202508+) | NOT_POLITICAL, POLITICAL, NOT_DECLARED |

### Schedule Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| runSchedule.start | long | No | Epoch ms - inclusive start |
| runSchedule.end | long | No | Epoch ms - exclusive end |
| pacingStrategy | string | No | LIFETIME (optimize over duration) or ACCELERATED (max speed, v202501+) |

### Advanced Fields

| Field | Type | Description |
|-------|------|-------------|
| optimizationPreference | object | Frequency capping for Brand Awareness (v202408+) |
| offsitePreferences | object | IAB categories and publisher restrictions |

### Read-Only Fields

| Field | Description |
|-------|-------------|
| id | Campaign numeric ID |
| test | true = test account campaign |
| servingStatuses | Array of service-controlled statuses |
| versionTag | Increments with each update |
| changeAuditStamps | Created/modified timestamps and actors |

**DO NOT include on create:** `test`, `id`, `version`, `versionTag`, `changeAuditStamps`, `servingStatuses`

---

## Objective Types & Bidding Matrix

### Objective Types

| objectiveType | Description | Recommended optimizationTargetType |
|---------------|-------------|-----------------------------------|
| BRAND_AWARENESS | Maximize reach/impressions | MAX_IMPRESSION or MAX_REACH |
| ENGAGEMENT | Drive engagement on posts (includes Follow button) | MAX_CLICK |
| WEBSITE_VISIT | Drive traffic to website | MAX_CLICK |
| WEBSITE_CONVERSION | Drive conversions (requires Insight Tag) | MAX_CONVERSION |
| LEAD_GENERATION | Generate leads via lead gen forms | MAX_LEAD |
| VIDEO_VIEW | Maximize video views | MAX_VIDEO_VIEW |
| JOB_APPLICANT | Drive job applications | MAX_CLICK |
| TALENT_LEAD | Get talent leads | MAX_CLICK |

**IMPORTANT:** It's `WEBSITE_VISIT` (singular), NOT `WEBSITE_VISITS`

### Optimization Target Types

**Manual Bidding (advertiser sets bid):**

| optimizationTargetType | Description |
|------------------------|-------------|
| NONE | No optimization. Manual bid required |
| ENHANCED_CONVERSION | Bid adjustment based on conversion rates |

**Auto-Bidding (LinkedIn optimizes to exhaust daily budget):**

| optimizationTargetType | Allowed Objectives |
|------------------------|--------------------|
| MAX_IMPRESSION | BRAND_AWARENESS |
| MAX_REACH | BRAND_AWARENESS (v202408+) |
| MAX_CLICK | ENGAGEMENT, JOB_APPLICANT, TALENT_LEAD, WEBSITE_VISIT |
| MAX_CONVERSION | WEBSITE_CONVERSION |
| MAX_VIDEO_VIEW | VIDEO_VIEW |
| MAX_LEAD | LEAD_GENERATION |
| MAX_QUALIFIED_LEAD | LEAD_GENERATION (v202602+) |

**Target Cost Bidding (LinkedIn targets average cost):**

| optimizationTargetType | costType |
|------------------------|----------|
| TARGET_COST_PER_CLICK | CPC |
| TARGET_COST_PER_IMPRESSION | CPM |
| TARGET_COST_PER_VIDEO_VIEW | CPV |

**Cost Cap Bidding (LinkedIn maximizes results under cap):**

| optimizationTargetType | costType |
|------------------------|----------|
| CAP_COST_AND_MAXIMIZE_CLICKS | CPM |
| CAP_COST_AND_MAXIMIZE_IMPRESSIONS | CPM |
| CAP_COST_AND_MAXIMIZE_VIDEO_VIEWS | CPM |

### Common Combinations

| Use Case | objectiveType | optimizationTargetType | costType | unitCost |
|----------|---------------|------------------------|----------|----------|
| Website traffic (auto) | WEBSITE_VISIT | MAX_CLICK | CPM | 0 |
| Website traffic (manual) | WEBSITE_VISIT | NONE | CPC | {bid} |
| Lead gen (auto) | LEAD_GENERATION | MAX_LEAD | CPM | 0 |
| Lead gen (manual) | LEAD_GENERATION | NONE | CPC | {bid} |
| Brand awareness (auto) | BRAND_AWARENESS | MAX_IMPRESSION | CPM | 0 |
| Website conversion (auto) | WEBSITE_CONVERSION | MAX_CONVERSION | CPM | 0 |
| Video views (auto) | VIDEO_VIEW | MAX_VIDEO_VIEW | CPV | 0 |
| Engagement (auto) | ENGAGEMENT | MAX_CLICK | CPM | 0 |

---

## Campaign Format Types

| format | Campaign Type | Used For |
|--------|---------------|----------|
| STANDARD_UPDATE | SPONSORED_UPDATES | Single image ads |
| SINGLE_VIDEO | SPONSORED_UPDATES | Video ads |
| CAROUSEL | SPONSORED_UPDATES | Carousel ads (2-10 cards) |
| SPONSORED_UPDATE_NATIVE_DOCUMENT | SPONSORED_UPDATES | Document ads |
| SPONSORED_UPDATE_EVENT | SPONSORED_UPDATES | Event ads |
| TEXT | TEXT_AD | Text ads (right rail) |
| SPOTLIGHT | DYNAMIC | Spotlight dynamic ads |
| FOLLOW_COMPANY | DYNAMIC | Follower dynamic ads |
| JOBS | DYNAMIC | Job dynamic ads |
| SPONSORED_INMAIL | SPONSORED_INMAILS | Message ads (legacy) |
| SPONSORED_MESSAGE | SPONSORED_INMAILS | Conversation ads |

**Notes:**
- Video and carousel campaigns MUST set format on creation
- If format not set, it's determined by the first creative added
- DYNAMIC type campaigns MUST set format

---

## Creative Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign | SponsoredCampaignUrn | Yes | `urn:li:sponsoredCampaign:{id}` |
| content | object | Yes (or inlineContent) | `{"reference": "urn:li:ugcPost:{id}"}` or `{"reference": "urn:li:share:{id}"}` |
| intendedStatus | string | No | ACTIVE, PAUSED, DRAFT, ARCHIVED, CANCELED, PENDING_DELETION, REMOVED |
| name | string | No | Creative name for reference |
| leadgenCallToAction | object | Conditional | Required if campaign objective is LEAD_GENERATION |
| inlineContent | object | Conditional | For `action=createInline` - creates post + creative in one call |
| id | SponsoredCreativeUrn | Read-only | `urn:li:sponsoredCreative:{id}` |
| account | SponsoredAccountUrn | Read-only | Set automatically |
| review | object | Read-only | PENDING, APPROVED, REJECTED, NEEDS_REVIEW |
| isServing | boolean | Read-only | Currently serving or not |
| servingHoldReasons | string[] | Read-only | Why creative isn't serving |

### intendedStatus Values

| Status | Description |
|--------|-------------|
| ACTIVE | Complete, available for review and serving |
| PAUSED | Complete, temporarily not served |
| DRAFT | Incomplete, still being edited |
| ARCHIVED | Complete, not served, hidden from main UI |
| CANCELED | Hidden from queries, retrievable if post still valid |
| PENDING_DELETION | Deletion in progress |
| REMOVED | Deleted but fetchable due to performance data |

**IMPORTANT:** Creating with `intendedStatus: "PAUSED"` can error about review status. Use `ACTIVE` - the campaign being PAUSED prevents actual spend.

### LeadgenCallToAction (for Lead Gen campaigns)

| Field | Type | Description |
|-------|------|-------------|
| destination | AdFormUrn | `urn:li:adForm:{id}` - immutable once creative leaves DRAFT |
| label | string | APPLY, DOWNLOAD, VIEW_QUOTE, LEARN_MORE, SIGN_UP, SUBSCRIBE, REGISTER, REQUEST_DEMO, JOIN, ATTEND, UNLOCK_FULL_DOCUMENT |

### Updatable Fields

Only these fields can be updated after creation:
- `intendedStatus`
- `leadgenCallToAction` (only in DRAFT status)
- `name`
- `content/eventAd/hidePreviewVideo` (v202505+)

**Immutable after creation:** `campaign`, `content.reference`

### Creative Deletion Rules

| Condition | Method |
|-----------|--------|
| DRAFT status | `DELETE` method directly |
| Campaign in DRAFT | `DELETE` method directly |
| Video with PROCESSING_FAILED | `DELETE` method directly |
| All other creatives | Set `intendedStatus: "PENDING_DELETION"` via PARTIAL_UPDATE |

---

## Targeting Criteria Structure

### AND/OR Logic

```python
{
    "targetingCriteria": {
        "include": {
            "and": [
                # Each item in "and" is ANDed together
                {
                    "or": {
                        # Values within a facet are ORed
                        "urn:li:adTargetingFacet:locations": [
                            "urn:li:geo:103644278"  # United States
                        ]
                    }
                },
                {
                    "or": {
                        "urn:li:adTargetingFacet:seniorities": [
                            "urn:li:seniority:7",  # VP
                            "urn:li:seniority:8",  # CXO
                            "urn:li:seniority:9",  # Director
                            "urn:li:seniority:10"  # Partner/Owner
                        ]
                    }
                },
                {
                    "or": {
                        "urn:li:adTargetingFacet:staffCountRanges": [
                            "urn:li:staffCountRange:(51,200)",
                            "urn:li:staffCountRange:(201,500)",
                            "urn:li:staffCountRange:(501,1000)"
                        ]
                    }
                }
            ]
        },
        "exclude": {
            "or": {
                "urn:li:adTargetingFacet:industries": [
                    "urn:li:industry:1"  # Exclude specific industry
                ]
            }
        }
    }
}
```

### All Targeting Facets

| Facet URN | Entity URN Format | Notes |
|-----------|-------------------|-------|
| `urn:li:adTargetingFacet:locations` | `urn:li:geo:{id}`, `urn:li:country:{code}`, `urn:li:countryGroup:{code}`, `urn:li:state:(urn:li:country:{code},{state})`, `urn:li:region:{id}` | IP + profile location matching |
| `urn:li:adTargetingFacet:profileLocations` | Same as locations | Profile location only |
| `urn:li:adTargetingFacet:interfaceLocales` | `urn:li:locale:{lang}_{COUNTRY}` | e.g. `urn:li:locale:en_US` |
| `urn:li:adTargetingFacet:seniorities` | `urn:li:seniority:{id}` | 1=Unpaid, 2=Training, 3=Entry, 4=Senior, 5=Manager, 6=Director, 7=VP, 8=CXO, 9=Partner, 10=Owner |
| `urn:li:adTargetingFacet:jobFunctions` | `urn:li:function:{id}` | Cannot AND with titles |
| `urn:li:adTargetingFacet:titles` | `urn:li:title:{id}` | Current title. Cannot AND with seniorities or jobFunctions |
| `urn:li:adTargetingFacet:titlesAll` | `urn:li:title:{id}` | Current + past titles |
| `urn:li:adTargetingFacet:titlesPast` | `urn:li:title:{id}` | Past titles only |
| `urn:li:adTargetingFacet:industries` | `urn:li:industry:{id}` | Cannot AND with employers |
| `urn:li:adTargetingFacet:staffCountRanges` | `urn:li:staffCountRange:({min},{max})` | (1,1), (2,10), (11,50), (51,200), (201,500), (501,1000), (1001,5000), (5001,10000), (10001,2147483647). Cannot AND with employers |
| `urn:li:adTargetingFacet:employers` | `urn:li:organization:{id}` | Current employer |
| `urn:li:adTargetingFacet:employersAll` | `urn:li:organization:{id}` | Current + past |
| `urn:li:adTargetingFacet:employersPast` | `urn:li:organization:{id}` | Past only |
| `urn:li:adTargetingFacet:skills` | `urn:li:skill:{id}` | |
| `urn:li:adTargetingFacet:schools` | `urn:li:organization:{id}` | |
| `urn:li:adTargetingFacet:degrees` | `urn:li:degree:{id}` | |
| `urn:li:adTargetingFacet:fieldsOfStudy` | `urn:li:fieldOfStudy:{id}` | |
| `urn:li:adTargetingFacet:interests` | `urn:li:interest:{id}` | |
| `urn:li:adTargetingFacet:groups` | `urn:li:group:{id}` | Include-only. Disabled in EEA/Switzerland since May 2024 |
| `urn:li:adTargetingFacet:followedCompanies` | `urn:li:organization:{id}` | |
| `urn:li:adTargetingFacet:firstDegreeConnectionCompanies` | `urn:li:organization:{id}` | |
| `urn:li:adTargetingFacet:genders` | `urn:li:gender:FEMALE`, `urn:li:gender:MALE` | Include-only |
| `urn:li:adTargetingFacet:ageRanges` | `urn:li:ageRange:(18,24)`, `(25,34)`, `(35,54)`, `(55,2147483647)` | Include-only |
| `urn:li:adTargetingFacet:yearsOfExperienceRanges` | `urn:li:yearsOfExperience:{1-12}` | 1-2 URNs for range |
| `urn:li:adTargetingFacet:memberBehaviors` | `urn:li:memberBehavior:{id}` | Cannot AND with contact lists or website retargeting |
| `urn:li:adTargetingFacet:companyCategory` | `urn:li:organizationRankingList:{id}` | Fortune 500, Forbes lists |
| `urn:li:adTargetingFacet:growthRate` | `urn:li:growthRate:({min},{max})` | Percentage ranges |
| `urn:li:adTargetingFacet:revenue` | Firmographic URN | Company revenue ranges |
| `urn:li:adTargetingFacet:audienceMatchingSegments` | `urn:li:adSegment:{id}` | Contact/company lists (NOT retargeting) |
| `urn:li:adTargetingFacet:dynamicSegments` | `urn:li:adSegment:{id}` | Website/engagement retargeting only |

### Facet Conflict Rules (Cannot AND Together)

- `industries` cannot AND with `employers` (include only)
- `staffCountRanges` cannot AND with `employers` (include only)
- `jobFunctions` cannot AND with `titles`
- `seniorities` cannot AND with `titles`
- `memberBehaviors` cannot AND with contact audience segments or website retargeting
- `dynamicSegments` (website retargeting) cannot AND with member behaviors or interests
- `ageRanges`, `genders`, `groups`, `interfaceLocales` = include-only (cannot exclude)

### Targeting Entity Discovery

**List all entities for a facet:**
```
GET /rest/adTargetingEntities?q=adTargetingFacet&facet={encoded_facet_urn}&queryVersion=QUERY_USES_URNS&locale=(language:en,country:US)
```

**Search entities by text (typeahead):**
```
GET /rest/adTargetingEntities?q=typeahead&facet={encoded_facet_urn}&query={search_text}&queryVersion=QUERY_USES_URNS
```

**Find similar entities:**
```
GET /rest/adTargetingEntities?q=similarEntities&facet={encoded_facet_urn}&entities=List({encoded_urn})
```

**Resolve URNs to names:**
```
GET /rest/adTargetingEntities?q=urns&urns=List({encoded_urn1},{encoded_urn2})
```

---

## Audience Counts (Size Estimation)

Minimum audience size: 300 members to run a campaign.

```
GET /rest/audienceCounts?q=targetingCriteriaV2&targetingCriteria=(include:(and:List((or:(urn%3Ali%3AadTargetingFacet%3Alocations:List(urn%3Ali%3Ageo%3A103644278))),(or:(urn%3Ali%3AadTargetingFacet%3Askills:List(urn%3Ali%3Askill%3A17))))))
```

**Response:**
```json
{
    "elements": [{"active": 0, "total": 25312600}]
}
```

- `total` = total audience matching criteria (0 if <300 for privacy)
- `active` = members likely to visit LinkedIn

---

## Post Schema (for DSC Ads)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| author | URN | Yes | `urn:li:organization:{id}` for company posts |
| lifecycleState | string | Yes | `PUBLISHED` |
| visibility | string | Yes | `PUBLIC` (NOT "CONTAINER") |
| commentary | string | Yes | Ad body text |
| distribution.feedDistribution | string | Yes | `NONE` for DSC (not on org feed), `MAIN_FEED` for organic |
| content | object | Yes | Article, media (image/video), or carousel |
| adContext.dscAdAccount | URN | Yes | `urn:li:sponsoredAccount:{id}` |
| adContext.dscStatus | string | No | `ACTIVE` |
| adContext.dscName | string | No | Creative name |
| adContext.dscAdType | string | **Read-only** | `VIDEO`, `IMAGE`, etc. - do NOT include on create (422 error) |
| adContext.isDsc | boolean | **Read-only** | Auto-set by API - do NOT include on create (422 error) |
| contentCallToActionLabel | string | No | APPLY, DOWNLOAD, VIEW_QUOTE, LEARN_MORE, SIGN_UP, SUBSCRIBE, REGISTER, REQUEST_DEMO, JOIN, ATTEND |
| contentLandingPage | string | Conditional | REQUIRED if contentCallToActionLabel is set |
| isReshareDisabledByAuthor | boolean | No | |

### Content Types

**Article (single image with link):**
```json
"content": {
    "article": {
        "title": "Headline text",
        "source": "https://landing-page.com",
        "thumbnail": "urn:li:image:{id}"
    }
}
```

**Media - Image:**
```json
"content": {
    "media": {
        "title": "Image title",
        "id": "urn:li:image:{id}"
    }
}
```

**Media - Video:**
```json
"content": {
    "media": {
        "title": "Video title",
        "id": "urn:li:video:{id}"
    }
}
```

**Carousel:**
```json
"content": {
    "carousel": {
        "cards": [
            {
                "media": {"id": "urn:li:image:{id}", "title": "Card 1"},
                "landingPage": "https://example.com/page1"
            },
            {
                "media": {"id": "urn:li:image:{id}", "title": "Card 2"},
                "landingPage": "https://example.com/page2"
            }
        ]
    }
}
```

**Post immutability:**
- `commentary` is IMMUTABLE after creation (must delete and recreate)
- `contentCallToActionLabel` is IMMUTABLE after creation
- `content.reference` on creative is IMMUTABLE (must delete and recreate)

---

## Image Upload

```python
# Step 1: Initialize upload
POST /rest/images?action=initializeUpload
{"initializeUploadRequest": {"owner": "urn:li:organization:{org_id}"}}

# Response contains:
upload_url = resp["value"]["uploadUrl"]
image_urn = resp["value"]["image"]  # urn:li:image:{id}

# Step 2: Upload binary
PUT {upload_url}
Headers: {"Content-Type": "application/octet-stream"}
Body: raw image bytes
```

---

## Video Upload

Use the Videos API to upload video files.

```python
# Step 1: Initialize upload
POST /rest/videos?action=initializeUpload
{
    "initializeUploadRequest": {
        "owner": "urn:li:organization:{org_id}",
        "fileSizeBytes": file_size,
        "uploadCaptions": false,
        "uploadThumbnail": false
    }
}

# Response contains:
video_urn = resp["value"]["video"]  # urn:li:video:{id}
upload_instructions = resp["value"]["uploadInstructions"]
# Each instruction has: uploadUrl, firstByte, lastByte

# Step 2: Upload chunks (for each instruction)
PUT {upload_url}
Headers: {"Content-Type": "application/octet-stream"}
Body: chunk bytes

# Step 3: Finalize
POST /rest/videos?action=finalizeUpload
{"finalizeUploadRequest": {"video": video_urn, "uploadToken": "", "uploadedPartIds": []}}
```

**Video specs:** 3 sec to 30 min, 75KB to 500MB, MP4 format.

---

## Analytics (v202601)

### CRITICAL: v202601 Analytics Format

**DO NOT use dot-notation for dateRange params.** Use Rest.li tuple format.

### Statistics Finder (operational data - spend, clicks, impressions)

```python
url = 'https://api.linkedin.com/rest/adAnalytics'
params_str = (
    'q=statistics'
    '&pivots=List(ACCOUNT)'
    '&dateRange=(start:(year:2026,month:1,day:14),end:(year:2026,month:2,day:13))'
    '&timeGranularity=ALL'
    '&accounts=List(urn%3Ali%3AsponsoredAccount%3AYOUR_ACCOUNT_ID)'
    '&fields=costInLocalCurrency,costInUsd,impressions,clicks,externalWebsiteConversions,oneClickLeads,totalEngagements,pivotValues,dateRange'
)
resp = requests.get(f'{url}?{params_str}', headers=headers)
```

**Statistics pivots (q=statistics):** ACCOUNT, CAMPAIGN, CREATIVE, COMPANY (operational pivots only)

### Analytics Finder (demographic data)

```python
# Use q=analytics with singular 'pivot' param for demographics
url = 'https://api.linkedin.com/rest/adAnalytics'
params_str = (
    'q=analytics'
    '&pivot=MEMBER_JOB_FUNCTION'
    '&timeGranularity=ALL'
    '&accounts=List(urn%3Ali%3AsponsoredAccount%3AYOUR_ACCOUNT_ID)'
    '&dateRange=(start:(year:2026,month:1,day:1),end:(year:2026,month:2,day:1))'
    '&fields=impressions,clicks,costInLocalCurrency,oneClickLeads,pivotValues'
)
```

**Demographic pivots (q=analytics):** MEMBER_JOB_FUNCTION, MEMBER_JOB_TITLE, MEMBER_INDUSTRY, MEMBER_SENIORITY, MEMBER_COMPANY_SIZE, MEMBER_COUNTRY_V2, MEMBER_REGION_V2, MEMBER_COMPANY

### Key Learnings

1. **Use `q=statistics`** for account/campaign-level spend data with explicit fields
2. **Use `q=analytics`** for demographic breakdown data
3. **dateRange must be Rest.li tuple format:** `(start:(year:2026,month:1,day:14),end:(year:2026,month:2,day:13))`
4. **Lists must use `List()` syntax:** `accounts=List(urn%3Ali%3AsponsoredAccount%3AYOUR_ACCOUNT_ID)`
5. **URN colons must be URL-encoded** as `%3A` in URL params
6. **`fields` parameter is needed** to get `costInLocalCurrency`
7. **Use `oneClickLeads`** not `leads` (doesn't exist in v202601)
8. **`q=statistics` pivots** = operational (ACCOUNT, CAMPAIGN, CREATIVE, COMPANY)
9. **`q=analytics` pivot** = demographic (singular `pivot=`, not `pivots=List()`)

### What Does NOT Work

```
# BROKEN: dot-notation date params
dateRange.start.year=2026  # REJECTED: "QUERY_PARAM_NOT_ALLOWED"

# BROKEN: fields as single string
fields=costInLocalCurrency,impressions  # Gets URL-encoded wrong

# BROKEN: old-style array params
accounts[0]=urn:li:sponsoredAccount:YOUR_ACCOUNT_ID  # REJECTED in v202601
```

---

## All Endpoints

### Campaign Groups
| Operation | Method | Endpoint |
|-----------|--------|----------|
| Create | POST | `/adAccounts/{id}/adCampaignGroups` |
| Get | GET | `/adAccounts/{id}/adCampaignGroups/{groupId}` |
| Search | GET | `/adAccounts/{id}/adCampaignGroups?q=search&search=(status:(values:List(ACTIVE,PAUSED)))` |
| Update | POST | `/adAccounts/{id}/adCampaignGroups/{groupId}` + PARTIAL_UPDATE |
| Delete (DRAFT) | DELETE | `/adAccounts/{id}/adCampaignGroups/{groupId}` |
| Delete (other) | POST | PARTIAL_UPDATE with `status: "PENDING_DELETION"` |
| Batch Create | POST | `/adAccounts/{id}/adCampaignGroups` + BATCH_CREATE |
| Batch Get | GET | `/adAccounts/{id}/adCampaignGroups?ids=List({id1},{id2})` |
| Batch Update | POST | `/adAccounts/{id}/adCampaignGroups?ids=List({id1},{id2})` + BATCH_PARTIAL_UPDATE |

### Campaigns
| Operation | Method | Endpoint |
|-----------|--------|----------|
| Create | POST | `/adAccounts/{id}/adCampaigns` |
| Get | GET | `/adAccounts/{id}/adCampaigns/{campaignId}` |
| Search | GET | `/adAccounts/{id}/adCampaigns?q=search&search=(status:(values:List(ACTIVE,PAUSED)))&pageSize=100` |
| Update | POST | `/adAccounts/{id}/adCampaigns/{campaignId}` + PARTIAL_UPDATE |
| Delete (DRAFT) | DELETE | `/adAccounts/{id}/adCampaigns/{campaignId}` |
| Delete (other) | POST | PARTIAL_UPDATE with `status: "PENDING_DELETION"` |

### Creatives
| Operation | Method | Endpoint |
|-----------|--------|----------|
| Create | POST | `/adAccounts/{id}/creatives` |
| Create inline | POST | `/adAccounts/{id}/creatives?action=createInline` |
| Get | GET | `/adAccounts/{id}/creatives/{encoded_creative_urn}` |
| Search | GET | `/adAccounts/{id}/creatives?q=criteria&campaigns=List({urn})&intendedStatuses=List(ACTIVE)` |
| Update | POST | `/adAccounts/{id}/creatives/{encoded_urn}` + PARTIAL_UPDATE |
| Delete (DRAFT) | DELETE | `/adAccounts/{id}/creatives/{encoded_urn}` |
| Delete (other) | POST | PARTIAL_UPDATE with `intendedStatus: "PENDING_DELETION"` |
| Batch Create | POST | `/adAccounts/{id}/creatives` + BATCH_CREATE |
| Batch Get | GET | `/adAccounts/{id}/creatives?ids=List({urn1},{urn2})` + BATCH_GET |
| Batch Update | POST | `/adAccounts/{id}/creatives?ids=List({urn1},{urn2})` + BATCH_PARTIAL_UPDATE |

### Posts
| Operation | Method | Endpoint |
|-----------|--------|----------|
| Create | POST | `/posts` |
| Get | GET | `/posts/{encoded_post_urn}` |
| Batch Get | GET | `/posts?ids=List({urn1},{urn2})` + BATCH_GET |

### Images
| Operation | Method | Endpoint |
|-----------|--------|----------|
| Initialize upload | POST | `/images?action=initializeUpload` |
| Upload binary | PUT | `{uploadUrl}` (from init response) |

### Conversions
| Operation | Method | Endpoint |
|-----------|--------|----------|
| List account conversions | GET | `/conversions?q=account&account=urn%3Ali%3AsponsoredAccount%3A{id}` |
| Get campaign conversions | GET | `/campaignConversions?q=campaigns&campaigns=List({encoded_urn})` |
| Associate conversion | PUT | `/campaignConversions/(campaign:{encoded_campaign},conversion:{encoded_conversion})` |
| Remove conversion | DELETE | `/campaignConversions/(campaign:{encoded_campaign},conversion:{encoded_conversion})` |

### Lead Gen Forms
| Operation | Method | Endpoint |
|-----------|--------|----------|
| List forms | GET | `/leadForms?q=owner&owner=(sponsoredAccount:urn:li:sponsoredAccount:{id})` |

**Note:** `/rest/adForms` was deprecated July 2025. Use `/rest/leadForms` instead.

### Conversation Ads (Sponsored Messaging)

**Full workflow: 7 steps to create a conversation ad via API.**

Campaign type: `SPONSORED_INMAILS`, format: `SPONSORED_MESSAGE`.

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Create conversation container | POST | `/conversationAds` |
| **Read conversation container** | **GET** | **`/conversationAds/{encoded_convo_urn}`** - returns headlineText, firstMessageContent, parentAccount |
| **Read all message nodes** | **GET** | **`/conversationAds/{encoded_convo_urn}/sponsoredMessageContents`** - returns full HTML body, CTA buttons, form references for every node |
| Create message node | POST | `/conversationAds/{encoded_convo_urn}/sponsoredMessageContents` |
| Set first message | POST | `/conversationAds/{encoded_convo_urn}` + PARTIAL_UPDATE |
| Create InMail content | POST | `/inMailContents` |
| Read InMail content | GET | `/inMailContents/{encoded_inmail_urn}` |
| Send test InMail | POST | `/inMailContents?action=sendTestInMail` |

**Deprecated endpoints (DO NOT USE):**
- `/adInMailContents` - returns 403/426. Replaced by `/inMailContents`
- `/adConversations` - returns 404. Replaced by `/conversationAds`
- `/sponsoredConversations` - returns 404. Replaced by `/conversationAds`

#### Step 1: Create conversation container
```json
POST /conversationAds
{
  "parentAccount": "urn:li:sponsoredAccount:YOUR_ACCOUNT_ID"
}
```
Returns: `x-restli-id: urn:li:sponsoredConversation:{id}`

#### Step 2: Create leaf nodes first (lead gen form, thank you)
```json
POST /conversationAds/{encoded_convo_urn}/sponsoredMessageContents

// Lead gen form node:
{
  "bodySource": {
    "leadGenerationForm": "urn:li:adForm:{formId}"
  }
}

// Thank you / follow-up node:
{
  "bodySource": {
    "text": "Thanks message here (max 500 chars)"
  },
  "nextAction": {
    "options": [{
      "replyType": "EXTERNAL_WEBSITE",
      "optionText": "Visit our site",
      "landingPage": "https://example.com"
    }]
  }
}
```
Returns: `x-restli-id: urn:li:sponsoredMessageContent:(urn:li:sponsoredConversation:{id},{messageId})`

#### Step 3: Create root node with CTA buttons
```json
POST /conversationAds/{encoded_convo_urn}/sponsoredMessageContents
{
  "bodySource": {
    "text": "Interested?"
  },
  "nextAction": {
    "options": [
      {
        "replyType": "LEAD_GENERATION",
        "optionText": "Yes, let's do it",
        "nextContent": "urn:li:sponsoredMessageContent:(urn:li:sponsoredConversation:{id},{leadgenNodeId})"
      },
      {
        "replyType": "EXTERNAL_WEBSITE",
        "optionText": "Tell me more first",
        "landingPage": "https://example.com/learn-more"
      },
      {
        "replyType": "SIMPLE_REPLY",
        "optionText": "Not interested"
      }
    ]
  }
}
```

**CTA replyTypes:**
- `LEAD_GENERATION` - opens lead gen form. `nextContent` must point to a node with `bodySource.leadGenerationForm`
- `EXTERNAL_WEBSITE` - opens URL. Requires `landingPage` field
- `SIMPLE_REPLY` - branches to another message node via `nextContent`, or ends if no `nextContent`
- `LEAD_GENERATION_THANK_YOU` - terminal node after form submission

**Limits:** max 25 nodes per conversation, max 5 CTAs per node, `optionText` 1-35 chars, `bodySource.text` max 500 chars. No cyclical references.

#### Step 4: Set first message on conversation
```json
POST /conversationAds/{encoded_convo_urn}
X-RestLi-Method: PARTIAL_UPDATE
{
  "patch": {
    "$set": {
      "firstMessageContent": "urn:li:sponsoredMessageContent:(urn:li:sponsoredConversation:{id},{rootNodeId})"
    }
  }
}
```

#### Step 5: Create InMail content (subject line, sender, body)
```json
POST /inMailContents
{
  "account": "urn:li:sponsoredAccount:YOUR_ACCOUNT_ID",
  "name": "Internal label for this content",
  "subject": "Subject line here (max 60 chars, supports %FIRSTNAME%)",
  "sender": "urn:li:person:{PERSON_ID}",
  "htmlBody": "Full message body in HTML (supports %FIRSTNAME%, %COMPANYNAME%, <br> tags)",
  "subContent": {
    "guidedReplies": {
      "sponsoredConversation": "urn:li:sponsoredConversation:{id}"
    }
  }
}
```
Returns: `x-restli-id: urn:li:adInMailContent:{id}`

**htmlBody is the opening message recipients see.** This is the main copy (up to 8,000 chars). The conversation tree nodes contain the CTA buttons and follow-up messages AFTER the opening.

**Sender must have conversation ad sender permissions** granted in Campaign Manager (Account Settings > Manage access > Conversation ad senders).

#### Step 6: Create creative
```json
POST /adAccounts/{id}/creatives
{
  "campaign": "urn:li:sponsoredCampaign:{campaignId}",
  "content": {"reference": "urn:li:adInMailContent:{id}"},
  "leadgenCallToAction": {
    "destination": "urn:li:adForm:{formId}",
    "label": "SIGN_UP"
  },
  "intendedStatus": "ACTIVE",
  "name": "Creative name"
}
```
**Critical:** For LEAD_GENERATION campaigns, the conversation message tree MUST contain at least one node with `bodySource.leadGenerationForm` pointing to an `urn:li:adForm`. Without this, creative creation returns error `SPONSORED_MESSAGE_CONTENT_AD_FORM_URN_NOT_FOUND_IN_MESSAGE_TREE`.

**Critical:** The `leadgenCallToAction.destination` (form URN) on creatives is **IMMUTABLE**. You cannot update it via PARTIAL_UPDATE. The form in the creative MUST match the form in the sponsored message tree. To change the form on a conversation ad, you must create an entirely new conversation tree (new container, new message nodes, new InMail content, new creative).

#### Reading conversation ad content (full copy extraction)

To read the full message copy, CTA buttons, and form references from an existing conversation ad:

```python
# 1. Get the InMail content (sender, subject, conversation reference)
inmail_urn = requests.utils.quote('urn:li:adInMailContent:{id}', safe='')
resp = requests.get(f'{BASE_URL}/inMailContents/{inmail_urn}', headers=headers)
# Returns: sender, subject, name, subContent.guidedReplies.sponsoredConversation

# 2. Get the conversation container (headline, first message pointer)
convo_urn = requests.utils.quote('urn:li:sponsoredConversation:{id}', safe='')
resp = requests.get(f'{BASE_URL}/conversationAds/{convo_urn}', headers=headers)
# Returns: headlineText, firstMessageContent

# 3. Get ALL message nodes (full HTML body, CTA buttons, form references)
resp = requests.get(f'{BASE_URL}/conversationAds/{convo_urn}/sponsoredMessageContents', headers=headers)
# Returns: elements[] with bodySource.text (HTML), nextAction.options[] (CTA buttons),
#          bodySource.leadGenerationForm (form URN on lead gen nodes)
```

This is the ONLY way to read conversation ad copy via API. The `htmlBody` field on InMail content returns "n/a" for conversation ads - the actual copy lives in the message nodes.

#### Step 7 (optional): Send test InMail
```json
POST /inMailContents?action=sendTestInMail
{
  "adInMailContentId": "urn:li:adInMailContent:{id}",
  "campaign": "urn:li:sponsoredCampaign:{campaignId}",
  "creative": "urn:li:sponsoredCreative:{creativeId}",
  "account": "urn:li:sponsoredAccount:YOUR_ACCOUNT_ID"
}
```

#### Campaign creation for conversation ads
```json
POST /adAccounts/{id}/adCampaigns
{
  "type": "SPONSORED_INMAILS",
  "format": "SPONSORED_MESSAGE",
  "objectiveType": "LEAD_GENERATION",
  "optimizationTargetType": "MAX_IMPRESSION",
  "costType": "CPM",
  "unitCost": {"currencyCode": "EUR", "amount": "0.30"},
  "pacingStrategy": "LIFETIME",
  "creativeSelection": "ROUND_ROBIN",
  ...
}
```

**Key differences from standard campaigns:**
- `type` = `SPONSORED_INMAILS` (not `SPONSORED_UPDATES`)
- `format` = `SPONSORED_MESSAGE` (not `STANDARD_UPDATE`)
- `optimizationTargetType` = `MAX_IMPRESSION` (not `MAX_LEAD`)
- `unitCost` = `0.30` CPM (not `0`)
- `pacingStrategy` = `LIFETIME`
- `creativeSelection` = `ROUND_ROBIN` (not `OPTIMIZED`)

#### Finding sender URN
The API cannot resolve a LinkedIn profile URL to a member URN. To find it:
1. Create a test conversation ad in Campaign Manager UI with the desired sender
2. Read the InMail content: `GET /inMailContents/{encoded_urn}` - the `sender` field contains the person URN
3. Reuse that URN for API-created conversation ads

### DMP Segments (Audience Lists)
| Operation | Method | Endpoint |
|-----------|--------|----------|
| Create segment | POST | `/dmpSegments` |
| Generate upload URL | POST | `/dmpSegments?action=generateUploadUrl` |
| Upload CSV | POST | `{upload_url}` (from generate response) |
| Attach list to segment | POST | `/dmpSegments/{segmentId}/listUploads` |
| Get segment status | GET | `/dmpSegments/{segmentId}` |
| List segments | GET | `/dmpSegments?q=account&account=urn:li:sponsoredAccount:{id}&count=100` |
| Rename segment | POST | `/dmpSegments/{segmentId}` + PARTIAL_UPDATE |

### Analytics
| Operation | Method | Endpoint |
|-----------|--------|----------|
| Account/campaign stats | GET | `/adAnalytics?q=statistics&pivots=List(ACCOUNT)&...` |
| Demographic breakdown | GET | `/adAnalytics?q=analytics&pivot=MEMBER_JOB_FUNCTION&...` |

### Targeting
| Operation | Method | Endpoint |
|-----------|--------|----------|
| List facets | GET | `/adTargetingFacets` |
| List entities by facet | GET | `/adTargetingEntities?q=adTargetingFacet&facet={urn}` |
| Search entities | GET | `/adTargetingEntities?q=typeahead&facet={urn}&query={text}` |
| Similar entities | GET | `/adTargetingEntities?q=similarEntities&facet={urn}&entities=List({urn})` |
| Resolve URNs | GET | `/adTargetingEntities?q=urns&urns=List({urn1},{urn2})` |
| Audience count | GET | `/audienceCounts?q=targetingCriteriaV2&targetingCriteria=(...)` |

---

## Pagination

### Cursor-Based (search endpoints, v202401+)

```python
all_items = []
page_token = None
while True:
    url = f'{BASE_URL}/endpoint?q=search&...'
    if page_token:
        url += f'&pageToken={page_token}'
    resp = requests.get(url, headers=headers)
    data = resp.json()
    all_items.extend(data.get('elements', []))
    page_token = data.get('metadata', {}).get('nextPageToken')
    if not page_token:
        break
```

**Max pageSize:** 1,000 for campaigns/campaign groups, 100 for creatives.

### Offset-Based (non-search endpoints)

```python
url = f'{BASE_URL}/endpoint?start=0&count=100'
```

**Max count:** 1,000 for campaign groups non-search.

---

## URL Encoding URNs

When URNs appear in URL paths or query params, encode colons:

```python
import urllib.parse
encoded_urn = urllib.parse.quote(urn, safe='')
# urn:li:sponsoredCampaign:123 -> urn%3Ali%3AsponsoredCampaign%3A123
```

---

## PARTIAL_UPDATE Pattern

All edits use POST with special header:

```python
headers["X-RestLi-Method"] = "PARTIAL_UPDATE"
payload = {"patch": {"$set": {"fieldName": "newValue"}}}
requests.post(url, headers=headers, json=payload)
# Returns 204 No Content on success
```

To remove a field:
```python
payload = {"patch": {"$delete": ["totalBudget"]}}
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success (GET) |
| 201 | Created (POST) - ID in `x-restli-id` header |
| 204 | Success (PARTIAL_UPDATE, PUT, DELETE) |
| 400 | Bad request - check payload/params |
| 403 | Forbidden - check permissions/scopes |
| 404 | Not found |
| 422 | Validation error - check field values/enums |

---

## Token Management

- Access tokens expire in **60 days**
- Refresh via `oauth_server.py` when expired
- Required scopes: `rw_ads` (read/write) or `r_ads` (read-only)
- Check token: `.env` as `LINKEDIN_ACCESS_TOKEN`

---

## Existing Scripts

- `linkedin_api.py` - Core API client class (LinkedInCampaignManager)
  - NOTE: `get_account_analytics()` and `get_campaign_analytics()` use the OLD dot-notation format
  - For analytics, use the REST.li URL pattern documented above instead
- `oauth_server.py` - OAuth token generation
- `generate_audit_report.py` - Campaign audit reports
- `get_creatives.py` / `filter_creatives.py` - Creative management
