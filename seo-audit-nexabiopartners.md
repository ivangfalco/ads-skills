# SEO Audit: nexabiopartners.com

**Audit date:** 2026-05-13
**Audited URL:** https://nexabiopartners.com (apex) / https://www.nexabiopartners.com (live host)
**Audit type:** Full site audit (keyword research + on-page + content gaps + technical + competitor benchmarking + AI/LLM visibility)
**Site footprint:** 8 URLs declared in sitemap.xml; 2 additional indexed pages discovered (/leadership and /blank) that now return 404

---

## 1. Executive Summary

**Verdict: Critical issues. The site cannot rank in its current state.**

Nexa Bio Partners has the right strategic positioning, a clean ProfessionalService schema, an AI-friendly robots.txt, and four legitimately useful blog topics for biotech founders. None of that matters today because of three blocking technical issues that, together, make the site invisible to search engines: (1) every URL serves the same 4,302-byte HTML response with an empty body and a canonical tag pointing to the homepage, meaning Google is told all 8 pages are duplicates of the homepage; (2) the apex domain (nexabiopartners.com) 307-redirects to www, but the canonical tag, sitemap, and Open Graph URL all reference the apex - a split-brain that confuses every crawler; (3) the site is a client-rendered React SPA with no server-side content, so non-Google crawlers (Bing, DuckDuckGo, and most importantly GPTBot/ClaudeBot/PerplexityBot) see no body content at all, despite robots.txt explicitly inviting them in.

**Top 3 priorities (in order):**

1. **Fix the canonical/redirect/SPA architecture.** Either pre-render or server-render the 8 known URLs so each has its own title, meta, canonical, and full body content. Decide on apex vs www, redirect the other one, and update all canonicals and sitemap entries to match. Without this, nothing else moves the needle.
2. **Build the BARDA + ARPA-H pillar pages.** EverGlade owns BARDA with a 5,500-word guide. ARPA-H has almost no consultant content - mostly government sites. These two programs are where the largest non-dilutive checks land in 2026; one quality pillar each is worth more traffic than 20 generic blog posts.
3. **Stake out the longevity/aging grant niche.** Nobody in the competitive set owns this. With Apollo Health Ventures network credibility, Nexa can claim it with a single pillar page + 4-6 supporting posts. White space rarely stays open this long.

**Biggest strength:** Strategic positioning is sharp - AI-augmented + biotech-exclusive + transparent-pricing-eligible is a real wedge that none of the 14 incumbent competitors occupies cleanly.

**Biggest risk:** Every week this rendering issue persists, four blog posts that were published 6+ months ago are dropping out of any chance of indexation while competitors publish weekly.

---

## 2. Keyword Opportunity Table

Volume/difficulty signals here are **relative** (high/medium/low) because no Ahrefs/Semrush MCP is connected. They are inferred from SERP density, competitor coverage frequency, and the depth of incumbent content. Connect an SEO tool for precise scoring on a follow-up pass.

| # | Keyword | Cluster | Est. Difficulty | Opportunity | Current Ranking | Intent | Recommended Content Type |
|---|---------|---------|-----------------|-------------|-----------------|--------|--------------------------|
| 1 | non-dilutive funding biotech | Core | High | High | Not ranking | Commercial | Pillar page (existing homepage upgraded) |
| 2 | non-dilutive funding consultant biotech | Core | Medium | High | Not ranking | Commercial / BOFU | Service page |
| 3 | non-dilutive funding life sciences | Core | High | Medium | Not ranking | Informational | Pillar page (homepage) |
| 4 | SBIR Phase 1 vs Phase 2 | Grant programs | High | Medium | Existing post not indexable | Informational | Refresh existing /blog/sbir-phase-1-vs-phase-2 with comparison table + FAQ schema |
| 5 | NIH SBIR consultant biotech | Grant programs | Medium | High | Not ranking | Commercial | Service sub-page |
| 6 | BARDA funding application | Grant programs | Medium | High | Not ranking | Informational / commercial | Pillar page (long-form guide) |
| 7 | ARPA-H funding opportunities biotech | Grant programs | Low-Medium | Very High | Not ranking | Informational / commercial | Pillar page + funding alert hub |
| 8 | ARPA-H ISO application | Grant programs | Low | High | Not ranking | Informational | Long-form guide |
| 9 | CDMRP grant biotech | Grant programs | Medium | Medium | Not ranking | Informational | Program guide |
| 10 | grant readiness biotech | Buyer journey | Low-Medium | High | Existing post not indexable | Commercial | Refresh /blog/grant-readiness-in-14-days, add checklist tool |
| 11 | non-dilutive funding vs venture capital | Buyer journey | Medium | High | Existing post not indexable | Informational | Refresh /blog/non-dilutive-vs-vc with comparison table |
| 12 | how NIH SBIR reviewers score proposals | Buyer journey | Medium | High | Existing post not indexable | Informational | Refresh /blog/how-reviewers-think + interview former reviewers |
| 13 | SBIR grant writer cost | Buyer journey | Medium | Very High | Not ranking | Commercial / BOFU | Comparison page (only SBIR Grant Writers owns this today) |
| 14 | biotech grant writing services pricing | Buyer journey | Medium | High | Not ranking | Commercial / BOFU | Comparison page with transparent Nexa pricing |
| 15 | biotech venture debt | Adjacent | Medium | Medium | Not ranking | Informational | Guide + when-to-use-which framework |
| 16 | royalty financing biotech | Adjacent | Low-Medium | Medium | Not ranking | Informational | Guide (law firms dominate - opportunity for plain-English explainer) |
| 17 | revenue-based financing life sciences | Adjacent | Low | Low | Not ranking | Informational | Single blog post |
| 18 | longevity grants biotech startup | Niche / white space | Low | Very High | Not ranking | Informational / commercial | Pillar page + dedicated resource hub |
| 19 | NIA aging research grants startup | Niche / white space | Low | High | Not ranking | Informational | Program guide tied to longevity pillar |
| 20 | FreeMind Group alternative | Comparison / BOFU | Low | Medium | Not ranking | Commercial / BOFU | Comparison page |
| 21 | Eva Garland Consulting review | Comparison / BOFU | Low | Medium | Not ranking | Commercial / BOFU | Honest comparison page |
| 22 | SBIR grant writer comparison | Comparison / BOFU | Medium | High | Not ranking | Commercial / BOFU | Multi-provider comparison page |
| 23 | AI grant writing for biotech | Positioning | Low-Medium | High | Not ranking | Informational | Thought-leadership pillar addressing the anti-AI narrative |
| 24 | European biotech US SBIR | Niche | Low | Medium | Not ranking | Commercial | "US grant entry" guide for EU biotechs |
| 25 | non-dilutive funding for medtech | Core variant | Medium | Medium | Not ranking | Commercial | Sub-pillar specifically for medtech (since homepage targets both) |

**Quick read of the table:**
- Rows 4, 10, 11, 12 (the 4 existing blog posts) should be refreshed first because the URLs already exist and the topics are sound.
- Rows 6, 7, 18 (BARDA, ARPA-H, longevity) are the highest-leverage net-new pillars.
- Rows 13, 14, 22 (cost/comparison) are the highest commercial-intent gaps - they bring buyers, not browsers.

---

## 3. On-Page SEO Audit

**Critical context before reading the table:** Every URL on `nexabiopartners.com` currently serves the same 4,302-byte HTML response. The body is empty (`<div id="root"></div>`) and all metadata is identical to the homepage. The findings below reflect what crawlers actually see today - not what users see after JavaScript executes.

Severity legend: **Critical** (blocking indexation or rankings), **High** (major impact), **Medium** (best-practice violation), **Low** (minor).

| Page | Issue | Severity | Recommended Fix |
|------|-------|----------|-----------------|
| All 8 URLs | Body is empty `<div id="root"></div>` - no server-rendered content | **Critical** | Move to server-side rendering (Next.js, Remix, Astro) or static pre-rendering. Vercel supports this natively |
| All 8 URLs | Identical `<title>` tag across every page | **Critical** | Generate per-page title in the HTML head, not just via client-side JS |
| All 8 URLs | Identical `<meta name="description">` across every page | **Critical** | Generate per-page meta description in HTML head |
| All 8 URLs | Canonical tag = `https://nexabiopartners.com/` on every URL | **Critical** | Each page must have its own canonical matching its actual URL |
| All 8 URLs | Apex (nexabiopartners.com) 307-redirects to www, but canonical points to apex | **Critical** | Pick one host. Recommend www since site already lives there. Update canonicals + sitemap + OG URLs to www |
| All 8 URLs | `og:url` and `twitter:url` reference apex, not the live www URL | High | Update OG tags to match the canonical you pick |
| Homepage `/` | No FAQ, Service, or BreadcrumbList schema - only ProfessionalService | Medium | Add Service schema for each non-dilutive funding service offered |
| `/blog` | No CollectionPage or Blog schema, no per-post listings server-rendered | High | Render the blog index as a real HTML list with article titles, dates, excerpts, and links |
| `/booking` | Should be deindexed if it embeds a third-party calendar - or add noindex if it's a conversion-only page | Medium | Decide intent: if SEO-targeted ("book a consultation"), give it real H1, content, FAQs; if not, add `<meta name="robots" content="noindex">` |
| `/grant-radar` | Page priority 0.9 in sitemap (high) but content unknown to crawlers | High | This appears to be a key product page. Server-render with H1, value prop, tool preview, FAQ schema |
| `/blog/sbir-phase-1-vs-phase-2` | No Article/BlogPosting schema, no author, no publication date in HTML | Critical | Add BlogPosting schema with author, datePublished, dateModified, headline, image, articleSection |
| `/blog/grant-readiness-in-14-days` | Same as above + content not indexable | Critical | Same fix + add FAQ schema for "What is grant readiness?", "How long does it take?", etc. |
| `/blog/non-dilutive-vs-vc` | Same as above + missing comparison table in HTML | Critical | Server-render comparison table; add FAQPage schema for the most common comparison questions |
| `/blog/how-reviewers-think` | Same as above + best candidate for thought-leadership distribution | Critical | Add BlogPosting schema, quote a former reviewer (interview-style), pull citation-friendly stats into list items |
| `/leadership` | Page returns HTTP 404 but appears in Google index | High | Either restore the page (recommended - leadership pages drive trust and AI citations) or 410 it permanently |
| `/blank` | Page returns HTTP 404 and is a placeholder slug from a website builder | High | 410 the URL and ensure it's not regenerated. Avoid all `/blank`-style placeholder slugs |
| Homepage `/` | Meta keywords tag present (deprecated since ~2009) | Low | Remove - it does nothing for ranking and signals a less-than-modern setup |
| All pages | No `<h1>` visible in server HTML (relies on JS to render) | Critical | Render H1 server-side. The H1 should match (or closely match) the page title |
| All pages | No image alt text observable because images are JS-rendered | High | Ensure all rendered images have descriptive alt text, especially logos and proof-point graphics |
| All pages | No `<noscript>` fallback content | Medium | At minimum, render a usable summary inside `<noscript>` so crawlers without JS see something |

---

## 4. Content Gap Analysis

**Method:** Compared what Nexa publishes (4 blog posts, 1 homepage, 1 booking page, 1 grant-radar page) against what FreeMind, Eva Garland, EverGlade, SBIR Grant Writers, Grant Engine, Grantify, and BW&Co rank for in the SERPs sampled.

| Topic | Why it matters | Format | Priority | Effort |
|-------|---------------|--------|----------|--------|
| Complete Guide to Non-Dilutive Funding for Biotech | Anchor for the entire topical cluster. FreeMind and Latham BioPharm both rank on the head term; Nexa has no pillar | Pillar page, 3,000-5,000 words, with FAQ schema | High | Substantial (3-5 days) |
| BARDA Funding: Application Process, Programs, and What Reviewers Want | EverGlade owns this with a 5,500-word guide. Nexa has nothing | Pillar page with PDF download lead magnet | High | Substantial (4-5 days) |
| ARPA-H Funding Guide (ISO, OTA, SBIR/STTR pathways) | Almost no consultant content exists outside ARPA-H.gov and BW&Co. Net-new white space | Pillar page + monthly funding alert hub | High | Substantial (4 days) |
| Longevity & Aging Research Grants (NIA, ARPA-H, private foundations) | Zero competitor coverage. Apollo Health Ventures angle = credibility. Growing funding area | Pillar page + 4-6 supporting posts | High | Substantial (multi-week) |
| SBIR Grant Writer Cost Comparison (transparent pricing) | Only SBIR Grant Writers publishes a comparison. High commercial intent | Comparison page covering 8-12 providers including Nexa | High | Moderate (1-2 days) |
| Non-Dilutive vs VC: a real founder framework | Existing blog post exists but isn't indexable. Topic is crowded but Nexa's angle (biotech-specific, founder-economics-first) is differentiated | Refresh existing post with comparison tables, FAQ schema, calculator | High | Moderate (half-day) |
| Grant Readiness Assessment Tool | Matches the `/grant-radar` slug intent. SBIR Grant Writers has a Grant Finder; Grantify has gated assessment. No interactive tool exists for biotech specifically | Interactive web tool + landing page | High | Substantial (multi-week dev) |
| How NIH SBIR Reviewers Actually Score Proposals | Existing post + the topic ranks for Granted AI and Keep Your Equity. Nexa's post should be the authoritative version | Refresh existing post, add real reviewer quotes, scoring rubric image | High | Moderate (1-2 days) |
| Direct to Phase II SBIR for Biotech | Sub-niche of SBIR content. Nexa's Phase 1 vs Phase 2 post covers adjacent ground but not D2P2 | Blog post + decision-tree visual | Medium | Moderate (half-day) |
| EU Biotech to US SBIR/BARDA: An Entry Guide | FreeMind has European visibility but no specialized bridge content. EU companies forming US subs is a real demand pocket | Long-form guide + checklist | Medium | Moderate (1-2 days) |
| Comparison: Nexa Bio Partners vs FreeMind / vs Eva Garland / vs SBIR Grant Writers / vs Grantify | Brand-comparison BOFU pages convert better than anything else | 4-5 individual comparison pages | High | Moderate (half-day each) |
| AI-Augmented Grant Writing for Biotech: What it Actually Means | Addresses SBIR Grant Writers' anti-AI narrative head-on. Nexa needs to own this conversation, not duck it | Thought-leadership essay + data | High | Moderate (1-2 days) |
| Glossary: SBIR, STTR, BARDA, ARPA-H, CDMRP, NIH SEED, DRIVe, BAA, OTA, ISO | Glossary pages capture long-tail traffic and are excellent for AI citations | Glossary page with anchor links per term | Medium | Quick win (half-day) |
| Funding Calculator (Phase I vs Phase II vs venture debt vs equity) | Tools earn backlinks; calculators earn AI citations | Interactive calculator | Medium | Substantial (multi-week dev) |
| Founder Case Studies / Client Wins | Eva Garland has 6 case studies on homepage. Nexa has zero visible | Case study format with metrics, founder quotes | Medium | Moderate (gather + write, multi-week) |
| Newsletter signup hub + archive | Eva Garland publishes monthly newsletters; EverGlade has funding alerts. Nexa needs a content drip + an archive that earns organic traffic | Newsletter + indexed archive | Medium | Moderate (setup + ongoing) |

---

## 5. Technical SEO Checklist

| Check | Status | Details |
|-------|--------|---------|
| HTTPS enabled | Pass | Site forces HTTPS, HSTS header is present (`max-age=63072000`) |
| Apex vs www handling | **Fail** | `nexabiopartners.com/` 307-redirects to `www.nexabiopartners.com/`, but the canonical tag, sitemap entries, and Open Graph URLs all reference the apex. Split-brain. Pick one and align everything |
| Canonical tags | **Fail** | All 8 pages have the same canonical pointing to the homepage. Blog posts canonical to `/`, which tells Google they're duplicates of the homepage and shouldn't be separately indexed |
| Per-page metadata (title, description, OG) | **Fail** | All 8 pages serve identical title, meta description, og:title, og:description, og:url. No per-page differentiation in server-rendered HTML |
| Server-side rendering of body content | **Fail** | Body is `<div id="root"></div>` only. All content depends on client-side JavaScript execution. Most non-Google crawlers (including ClaudeBot, GPTBot, PerplexityBot) get no usable content despite robots.txt inviting them |
| Sitemap.xml present | Pass | 8 URLs, valid XML, includes lastmod, changefreq, priority |
| Sitemap accuracy | Warning | Sitemap URLs use apex domain (`nexabiopartners.com`) but site lives at www. After picking a canonical host, update sitemap |
| Robots.txt | Pass | Permissive (`Allow: /`), excludes `/admin` and `/_data/`, explicitly allows GPTBot, ClaudeBot, PerplexityBot, Google-Extended. Sitemap directive present |
| Open Graph + Twitter cards | Warning | All required tags present and well-formed, but URLs reference apex (mismatch with live site) |
| Organization / ProfessionalService schema | Pass | Well-structured ProfessionalService JSON-LD on every page with `knowsAbout` array of relevant funding programs |
| Article / BlogPosting schema on blog posts | **Fail** | No BlogPosting schema visible on any of the 4 blog posts in the server HTML |
| BreadcrumbList schema | **Fail** | Not present on any page |
| FAQ schema | **Fail** | Not present. Blog posts on "non-dilutive vs VC", "SBIR Phase 1 vs Phase 2", "grant readiness" are ideal FAQ candidates |
| Mobile responsiveness | Likely Pass | Vercel-hosted React app with `width=device-width` viewport set. Cannot verify rendered layout without JS execution. Recommend a Lighthouse run from DevTools |
| Page speed signals | Likely Pass | Vercel CDN, small initial HTML (4.3 KB), single JS bundle, single CSS file. LCP candidate is unclear without rendered DOM |
| Indexation - 404 pages still in Google | **Fail** | `/leadership` and `/blank` both return HTTP 404 but appear in Google search results. Decide: restore (leadership page) or 410 (blank) |
| HSTS | Pass | Strict-Transport-Security present with 2-year max-age |
| Favicon | Pass | SVG favicon set |
| GTM / analytics | Pass | Google Tag Manager loaded; noscript fallback present |
| Image optimization | Unknown | Cannot evaluate from server HTML alone. Inspect rendered DOM for alt text, lazy-loading, modern formats (WebP/AVIF) |
| Internal linking structure | **Fail** | No links in server HTML (all rendered by JS). Crawlers see zero internal links unless they execute JS. Even Google's renderer may miss links if hydration is slow |
| `noscript` fallback content | **Fail** | No `<noscript>` content tag with usable text |
| Meta keywords tag | Warning | Present (deprecated since ~2009). Harmless but unnecessary; remove for cleanliness |
| Hreflang / international SEO | N/A | Single-language site; no need yet. Revisit if EU-bridge content launches |

---

## 6. Competitor SEO Comparison

Estimates based on direct page fetches and SERP inspection. Precise keyword footprints require an SEO tool MCP.

| Dimension | Nexa Bio Partners | FreeMind Group | Eva Garland | Grant Engine | SBIR Grant Writers | EverGlade | Grantify | Winner |
|-----------|-------------------|----------------|-------------|--------------|--------------------|-----------|----------|--------|
| Server-rendered content | None (SPA) | Full | Full | Full | Full | Full | Full | Everyone but Nexa |
| Approx. homepage word count | <50 (visible to crawlers) | 2,000-2,500 | 2,000-2,500 | 1,500-2,500 | 2,000+ | 1,500-2,000 | 1,500-2,500 | Eva Garland / FreeMind |
| Indexed pages (sitemap) | 8 | 50+ | 80+ | 40+ | 30+ comparison + blog | 30+ | 100+ | Grantify |
| Dedicated pillar pages | 0 | Multiple (per program) | "Funding Your Science" hub | 3-pillar model (FIND/WIN/MANAGE) | Comparison + readiness | BARDA (5,500w) + ARPA-H | Multiple | EverGlade for BARDA / Eva Garland for hubs |
| Blog publishing frequency (last 6 months) | 4 total posts (1 per ~6 weeks) | Resource library updates | Monthly newsletters + webinars | Active | Active + quarterly updates | Active + funding alerts | High volume | Grantify / SBIR Grant Writers |
| Case studies / client proof | 0 visible | Some | 6+ on homepage | Named clients | 2,500+ awardees claim | $168M ModeX deal cited | Multiple named clients | Eva Garland |
| Transparent pricing | No | No | No | No | Yes ($5,495-$5,995 fixed) | No | Gated | SBIR Grant Writers |
| Books / authoritative publications | No | No | 2 books | No | Published reviewer study | No | No | Eva Garland |
| Schema markup depth | ProfessionalService only | Organization + Event | Organization + likely Article | Organization | Article + comparison data | Organization | Organization | SBIR Grant Writers / Eva Garland |
| AI search citations (sample query: "best SBIR grant writer for biotech") | Not cited | Mentioned | Mentioned | Cited | Cited | Mentioned | Cited | SBIR Grant Writers / Grantify |
| Domain age signal | Newer | ~25 years | ~13 years | ~13 years | 10+ years | Established | 5+ years | FreeMind |
| Brand-specific search results page | Yes (own homepage) | Strong (multiple SERP features) | Strong + Inc. 5000 PR | Strong | Strong (own comparison page) | Strong (PRNewswire releases) | Strong (Sunday Times PR) | Tied across incumbents |
| LinkedIn signal | Active | Strong | 3,433 followers | Active | Active | Active | Active | Eva Garland |

**Takeaways:**
- Nexa Bio Partners is competitive in **strategic positioning** (AI-augmented, biotech-exclusive) but is **structurally invisible to search** because of the SPA architecture. Every competitor renders content server-side.
- The fastest competitive flank-attack is the **transparent pricing + AI-augmented** wedge that no incumbent occupies. SBIR Grant Writers owns transparency without AI; Grantify owns AI without biotech-exclusivity. Nexa can own both.
- **Eva Garland's pillar-page strategy** (Funding Your Science hub + case studies + books) is the model to study most closely - it's the highest-leverage SEO play in this niche.

---

## 7. AI / LLM Search Visibility (Bonus)

robots.txt explicitly allows `GPTBot`, `ClaudeBot`, `PerplexityBot`, and `Google-Extended` - the four crawlers that feed ChatGPT, Claude, Perplexity, and Google's AI features respectively. This is correctly set up. **However, those crawlers will get zero usable content from any URL on the site because the body is empty without JS execution.** Most LLM crawlers do not execute JavaScript.

**Live observations (sample queries, 2026-05):**

| Query | Does Nexa appear? | Who is cited instead? |
|-------|-------------------|------------------------|
| "best non-dilutive funding consultant for biotech" | No | FreeMind, Latham BioPharm, CUBRC, Scorpius, SVB, BDO |
| "best SBIR grant writer recommendations biotech" | No | ScienceDocs, SBIR Grant Writers, QB3, Blue Haven, TurboSBIR |
| "BARDA funding consultant" | No | EverGlade, Excedr |
| "ARPA-H funding biotech consultant" | No | BW&Co Consulting, ARPA-H.gov, Michigan Bio |
| "how NIH SBIR reviewers score proposals" | No | SBIRland, NIH.gov, Keep Your Equity, Granted AI, ScienceDocs |
| Direct brand query: "Nexa Bio Partners" | Yes (homepage + LinkedIn + BIO conference page) | n/a |

**What it takes to get cited by LLMs in this niche:**
1. Server-rendered, statistic-dense content (LLMs love quotable numbers - dollar amounts, percentages, timeframes)
2. Q&A-formatted sections (mirrors the answer-engine intent)
3. Clear authorship and credentials (LLMs cite credentialed sources more)
4. Frequent updates with year-stamped data ("2026" in titles is a small but real boost)
5. Backlinks from `.gov`, `.edu`, and trade press

**Recommendations specifically for AEO/GEO:**
- Add FAQ schema to every blog post and pillar page
- Server-render a single citation-friendly statistic in the first 200 words of each page ("Nexa has secured $X in non-dilutive funding for Y biotech companies since…")
- Build the comparison table page (SBIR Grant Writers' template) as a content asset LLMs will quote
- Get one Substack mention or one trade press piece in Endpoints News / Fierce Biotech / BioSpace - LLM citation graphs lean heavily on those sources

---

## 8. Prioritized Action Plan

### Quick Wins (this week, <2 hours each)

| # | Action | Impact | Effort | Dependencies |
|---|--------|--------|--------|--------------|
| 1 | Decide apex vs www host, update Vercel redirects + canonicals + sitemap to match | High | 30 min | Engineering access |
| 2 | Restore `/leadership` page or 410 it permanently | High | 15 min | Decision on whether to bring it back |
| 3 | 410 the `/blank` URL and confirm it doesn't regenerate | Medium | 10 min | None |
| 4 | Remove the `meta keywords` tag from `<head>` | Low | 5 min | None |
| 5 | Add per-page `<title>` and `<meta name="description">` in the JS bundle (React Helmet or equivalent) for at least the 4 blog posts | High | 1 hour | Engineering |
| 6 | Add a `<noscript>` block with each page's title, H1, and a 1-paragraph summary so non-JS crawlers see something | Medium | 1 hour | Engineering |
| 7 | Add BlogPosting JSON-LD schema to the 4 existing blog posts (author, datePublished, dateModified, headline, image) | High | 1 hour | None |
| 8 | Add FAQ JSON-LD schema to `/blog/non-dilutive-vs-vc` and `/blog/sbir-phase-1-vs-phase-2` (5-7 Q&A pairs each) | High | 1.5 hours | Content drafting |
| 9 | Add Organization sameAs links (LinkedIn, BIO convention profile) to the ProfessionalService schema | Low | 20 min | None |
| 10 | Add BreadcrumbList JSON-LD to all sub-pages | Medium | 30 min | None |
| 11 | Add a clear H1 element to each page's server HTML (not just JS-rendered) | High | 1 hour | Engineering |
| 12 | Audit OG image - confirm `og-image.png` exists and renders correctly when scraped | Low | 15 min | None |
| 13 | Confirm Google Search Console is set up for both apex and www properties | High | 15 min | GSC access |
| 14 | Submit updated sitemap to GSC after canonical fix | Medium | 5 min | After Quick Win #1 |

### Strategic Investments (this quarter)

| # | Action | Impact | Effort | Dependencies |
|---|--------|--------|--------|--------------|
| 1 | Migrate to server-rendered architecture (Next.js / Astro on Vercel) so all 8+ pages have server-rendered HTML | Critical | 1-3 weeks of dev | Engineering |
| 2 | Build pillar page: "Complete Guide to Non-Dilutive Funding for Biotech" (3,000-5,000 words, FAQ schema, lead magnet) | High | 5-7 days | Content + dev |
| 3 | Build pillar page: "BARDA Funding Guide" (compete with EverGlade's 5,500-word piece) | High | 5-7 days | Content + dev |
| 4 | Build pillar page: "ARPA-H Funding Guide" (white space, mostly gov sites today) | High | 4-5 days | Content + dev |
| 5 | Build pillar page: "Longevity & Aging Grants Hub" - unique niche, no consultant owns it | High | 7-10 days | Content + dev |
| 6 | Build comparison pages: Nexa vs FreeMind / vs Eva Garland / vs SBIR Grant Writers / vs Grantify / vs Blue Haven | High | 2-3 days each | Content + dev |
| 7 | Build "SBIR Grant Writer Cost Comparison" page modeled after SBIR Grant Writers' but with Nexa's transparent pricing | High | 2-3 days | Pricing decision needed first |
| 8 | Build `/grant-radar` as a real interactive product page with screenshot, value prop, FAQ schema, signup form | High | 5-7 days | Product decision on what grant-radar actually is |
| 9 | Refresh the 4 existing blog posts with deeper content, FAQ schema, comparison tables, expert quotes | High | 2 days each | Content |
| 10 | Build a Glossary page covering SBIR, STTR, BARDA, ARPA-H, CDMRP, NIH SEED, DRIVe, BAA, OTA, ISO (long-tail magnet + AI citation source) | Medium | 2-3 days | Content |
| 11 | Launch monthly Newsletter "Nexa Grant Intel" + indexed web archive | Medium | Initial setup 1 week + ongoing | Content + email tool |
| 12 | Build 3 case studies from existing client wins (format: founder quote + metrics + timeline + lessons) | Medium | 1-2 weeks (depends on client cooperation) | Client outreach |
| 13 | Get 2-3 backlinks from biotech trade press (Endpoints News, Fierce Biotech, BioSpace) via thought-leadership pitches | High | 2-4 weeks of outreach | Founder time |
| 14 | Build a "Grant Readiness Assessment" tool tied to the `/grant-radar` slug | High | 3-4 weeks dev | Product decision |
| 15 | Connect an SEO tool MCP (Ahrefs / Semrush) + Google Search Console + Google Analytics 4 to enable precise tracking | High | 1 day setup | Tool licensing |

---

## Follow-up suggestions

This audit is the diagnosis; the next step is treatment. I can:
- Draft the title tags + meta descriptions for the 8 known URLs (Quick Win #5)
- Write the BlogPosting + FAQ + BreadcrumbList JSON-LD blocks ready to paste into the codebase (Quick Wins #7, #8, #10)
- Outline the BARDA pillar page (H2/H3 structure + word counts per section + FAQ block) for engineering and content to execute against
- Draft the SBIR-grant-writer comparison page with Nexa's pricing positioned against the 6 priority competitors
- Build a content calendar covering the 16 gap topics across a Q3/Q4 publishing schedule

Or pick a specific section to dive deeper on - the longevity niche, the SPA→SSR migration plan, the AEO/GEO play, or the comparison-page strategy are all worth dedicated treatment.

---

## Methodology notes

- **Tools used:** WebFetch for 8 Nexa URLs + 4 competitor pages, WebSearch for 9 SERP-composition checks, raw curl for HTTP header / HTML body inspection
- **Tools NOT used (and would sharpen findings):** Ahrefs / Semrush MCP (keyword volume + difficulty + backlink data), Google Search Console (verified indexation status, query data, click-through data), Google Lighthouse (Core Web Vitals)
- **Validity period:** Findings are accurate as of 2026-05-13. Re-run the canonical/redirect check after any deployment because Vercel redirect rules can change
- **Data confidence:** High for technical findings (verified via raw HTML), medium for competitor word counts (estimates from page fetches), medium for keyword opportunity scoring (relative, not measured)
