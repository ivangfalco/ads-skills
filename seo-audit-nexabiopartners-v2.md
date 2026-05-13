# SEO Audit v2: nexabiopartners.com

**Audit date:** 2026-05-13 (follow-up after SSR migration deploy)
**Previous audit:** [seo-audit-nexabiopartners.md](./seo-audit-nexabiopartners.md) (2026-05-13 morning)
**Audited URL:** https://www.nexabiopartners.com
**Audit type:** Verification + refocused action plan

---

## 1. Executive Summary

**Verdict: The site can now rank. Focus shifts from technical fixes to content depth and entity authority.**

The SSR migration shipped successfully. Every page now serves 30-56 KB of real, prerendered HTML with per-page titles, per-page canonicals, BlogPosting + BreadcrumbList + FAQPage schemas where appropriate, and the apex→www redirect is a proper 308. All three critical issues from the morning audit are resolved. The site is now actually crawlable and indexable.

What's left is no longer technical - it's positional. Three priorities:

1. **Mop up Google's stale index** (this week). `/leadership`, `/blank`, and (newly discovered) `/contact` still appear in `site:nexabiopartners.com` results. Two are 308-redirected and need re-crawl; `/contact` returns 404 and needs a redirect added. Submit the updated sitemap in GSC.
2. **Build the BARDA and ARPA-H pillar pages** (this month). The technical foundation is now ready to actually rank. EverGlade owns BARDA with 5,500 words; ARPA-H is mostly `.gov` + one consultant. These are the highest-leverage content investments.
3. **Stake the longevity/aging grant niche** (this quarter). No competitor occupies this. Apollo Health Ventures co-founder Florian Haupt is a credible spokesperson. White space rarely stays open this long.

**Biggest strength:** Schema markup depth (3 schemas per page type), per-page metadata, and AI-crawler-friendly robots.txt now position the site well for both Google and LLM citations.

**Biggest risk:** Brand SERP confusion. "Nexa Bio" sits next to Nexa Bioscience (nexa.bio), Nexa AI, Nexa Partners (nexapartners.ai), and Nexa Equity in branded search. Without entity disambiguation work (Knowledge Graph, Wikidata, founder profiles), direct brand traffic gets diluted.

---

## 2. What Got Fixed (since morning audit)

| Issue from v1 audit | Status |
|---------------------|--------|
| SPA shell with empty body (4.3 KB on every URL) | ✅ Fixed. Homepage now 56 KB, blog posts 19-35 KB, all prerendered server-side |
| Identical title/meta/canonical on every URL | ✅ Fixed. Per-page values via react-helmet-async + Puppeteer prerender |
| Canonical pointed to apex while site lived at www | ✅ Fixed. All canonicals now use www, matching the live host |
| Apex/www redirect was 307 (temporary) | ✅ Fixed. Now 308 (permanent) |
| `/leadership` and `/blank` returned 404 but were in Google's index | ✅ Both now 308 → `/#team` and `/` respectively |
| Meta keywords tag (deprecated) | ✅ Removed |
| No `<noscript>` fallback | ✅ Added (scoped style block + structured content for non-JS crawlers) |
| No FAQ schema on homepage | ✅ Added (mirrors the existing FAQ array, 8 Q&A pairs) |
| No BlogPosting schema on posts | ✅ Added per post (with image, author, publisher, dateModified) |
| No BreadcrumbList schema anywhere | ✅ Added to /blog, /booking, /grant-radar, and each blog post |
| Puppeteer failing silently on Vercel build | ✅ Switched to `@sparticuz/chromium` on Vercel; build now hard-fails on Chrome launch error so empty shells can never ship again |
| `vercel.json` rewrote all routes to /index.html (overriding prerendered files) | ✅ Removed rewrites for prerendered routes |

**Net effect:** Every quick-win from the v1 audit's action plan is in production except per-blog-post FAQ schemas, which require adding FAQ blocks to the markdown frontmatter (content work, not engineering).

---

## 3. Remaining Technical Issues

### Critical (this week)

| Issue | Page | Fix |
|-------|------|-----|
| `/contact` returns HTTP 404 but appears in Google's `site:` index as "Contact \| Nexa Bio Partners" | `/contact` | Add a redirect to `/booking` in `vercel.json` (same pattern as `/blank` and `/leadership`) |
| Sitemap URLs use apex (`nexabiopartners.com`) but canonical tags use www (`www.nexabiopartners.com`) | `sitemap.xml` | Update `SITE_URL` in `scripts/sitemap.cjs` from `https://nexabiopartners.com` to `https://www.nexabiopartners.com`. After deploy, resubmit sitemap in Google Search Console |
| Google still surfaces 4 stale URLs in `site:` search | `/leadership`, `/blank`, `/contact`, plus old non-www versions | Once `/contact` redirect ships, request re-indexing in GSC for each known stale URL. Optionally use the URL Removal tool for `/blank` |

### High (next 2 weeks)

| Issue | Page | Fix |
|-------|------|-----|
| No `LocalBusiness` schema. Company is in Boston, MA but no address or geo is exposed to crawlers | All pages | Extend the ProfessionalService JSON-LD with `address` (PostalAddress), `geo` (GeoCoordinates), and `telephone` if a public number exists. Helps Knowledge Graph + local intent queries |
| No per-blog-post FAQ schema (only homepage has one) | 4 blog posts | Add `faqs:` block to each markdown frontmatter, then surface as FAQPage schema in `BlogDetail`. Especially valuable on `/blog/non-dilutive-vs-vc` and `/blog/sbir-phase-1-vs-phase-2` |
| Single 520 KB JS bundle, no code splitting | All pages | Add `manualChunks` config in `vite.config.js` to split admin + grant-admin + grant-radar into separate chunks (those routes are admin-only and shouldn't load on public pages) |
| Blog post word count ~1,900 (competitors at 2,500-3,000 on the same topic) | `/blog/sbir-phase-1-vs-phase-2` and the other 3 posts | Refresh each post with a comparison table, FAQ section, and one reviewer quote (existing content is correct, just thin) |

### Medium (when convenient)

| Issue | Page | Fix |
|-------|------|-----|
| Brand entity confusion in SERPs (5+ "Nexa" companies competing for branded queries) | n/a | Create Wikidata entry for "Nexa Bio Partners" linked to founders, BIO Convention exhibitor page, LinkedIn company page. Push for unambiguous brand mention in 1-2 trade press pieces (Endpoints, Fierce Biotech) |
| Blog posts use ISO date format ("by Amro Eid") but no microformat | 4 blog posts | Already covered by BlogPosting schema's `datePublished`, but consider adding visible "Updated YYYY-MM-DD" to body to signal freshness on refresh |
| Homepage has 6 H2s but no anchor IDs visible in HTML for jump-links from FAQ | `/` | Add anchors (`id="how-we-work"`, `id="leadership"`, `id="faq"`) so the FAQ "How is NEXA different?" answer can deep-link to relevant sections |

---

## 4. Refocused Strategic Action Plan

The v1 audit's "Strategic Investments" section is still 100% valid - the technical fixes were a precondition, not a replacement. Re-stating priorities with sharper sequencing now that the foundation is solid:

### This month (pillar pages - biggest unlock)

| # | Action | Why now | Effort | Expected impact |
|---|--------|---------|--------|-----------------|
| 1 | **BARDA Funding Guide** pillar page (3,500-5,500 words, FAQ schema, downloadable PDF lead magnet) | EverGlade owns this with 5,500 words. With SSR working, Nexa can finally compete. BARDA = biggest single-deal sizes in this niche | 4-5 days | High - new keyword footprint + lead capture |
| 2 | **ARPA-H Funding Guide** pillar page (covers ISO, OTA, SBIR/STTR paths) | Almost no consultant content. Mostly `.gov` + BW&Co | 4-5 days | High - white-space land grab |
| 3 | **Longevity & Aging Grants Hub** pillar page + 3 supporting posts | Zero competitor coverage. Apollo Health Ventures angle (Florian Haupt) = unique credibility | 1-2 weeks | High - unique niche, attracts founders nobody else is talking to |

### This quarter (commercial intent + brand)

| # | Action | Why | Effort |
|---|--------|-----|--------|
| 4 | **Comparison pages**: Nexa vs FreeMind / vs Eva Garland / vs SBIR Grant Writers / vs Grantify (4 pages) | Bottom-of-funnel commercial intent. Brand-comparison pages are the highest-converting traffic in this category | 2-3 days per page |
| 5 | **SBIR Grant Writer Cost Transparency page** modeled on SBIR Grant Writers' comparison, but with Nexa's actual pricing | Only SBIR Grant Writers ranks for "SBIR grant writer cost" today | 2-3 days (depends on pricing decision) |
| 6 | **Refresh the 4 existing blog posts**: add comparison tables, FAQ sections (with FAQPage schema), reviewer quotes, take each to 2,800+ words | URLs and topics are already correct - just thin. Refresh > new post for ranking velocity | 1 day per post |
| 7 | **Build out Grant Radar product page** with case studies, "what we check for," outcome examples, and an embedded demo or video | Currently the page has only a domain-input form and a one-line value prop. SERP traffic for "grant matching tool biotech" wants more proof | 3-5 days |
| 8 | **Glossary page** covering SBIR, STTR, BARDA, ARPA-H, CDMRP, NIH SEED, DRIVe, BAA, OTA, ISO | Long-tail magnet + ideal for AI/LLM citations | 2-3 days |
| 9 | **Entity disambiguation**: create Wikidata entry, claim Knowledge Graph panel, get listed in 2-3 trade press pieces with "Nexa Bio Partners" as exact-match brand | Without this, brand SERP gets polluted by 5 other "Nexa" companies | 1-2 weeks of outreach |

### Cross-cutting (set up now, run continuously)

| # | Action | Effort |
|---|--------|--------|
| 10 | Connect Ahrefs or Semrush MCP to enable precise keyword tracking + backlink monitoring | 1 day setup, then ongoing |
| 11 | Set up Google Search Console for `www.nexabiopartners.com` (both as Domain property AND URL-prefix), verify ownership, submit updated sitemap, monitor Coverage and Performance | Half day |
| 12 | Connect GA4 for organic traffic attribution | Half day |
| 13 | Monthly newsletter "Nexa Grant Intel" with funding-cycle alerts and reviewer perspectives. Archive on `/blog` or `/newsletter` so it's also a content asset | 1 week setup, then weekly cadence |
| 14 | Pitch 2-3 thought-leadership pieces to Endpoints News / Fierce Biotech / BioSpace per quarter | Ongoing, 2-4 weeks of outreach |

---

## 5. Keyword Opportunity Table (refreshed)

Now that pages can actually rank, the keyword scoring is the same as v1 but with updated current ranking confidence. Repeating the highest-leverage rows here for execution focus. See [v1 audit](./seo-audit-nexabiopartners.md) for the full 25-row table.

| Keyword | Difficulty | Opportunity | Current rank | Intent | Target page |
|---------|-----------|-------------|--------------|--------|-------------|
| BARDA funding application | Medium | High | Not ranking | Informational | NEW pillar page |
| ARPA-H funding opportunities biotech | Low-Medium | Very High | Not ranking | Informational | NEW pillar page |
| longevity grants biotech startup | Low | Very High | Not ranking | Informational | NEW pillar page (white space) |
| SBIR grant writer cost | Medium | Very High | Not ranking | Commercial / BOFU | NEW comparison page |
| non-dilutive funding biotech | High | High | Not ranking | Commercial | Existing `/` (refresh copy) |
| SBIR Phase 1 vs Phase 2 | High | Medium | Should start crawling now | Informational | Existing `/blog/sbir-phase-1-vs-phase-2` (refresh + FAQ schema) |
| non-dilutive funding vs venture capital | Medium | High | Should start crawling now | Informational | Existing `/blog/non-dilutive-vs-vc` (refresh + comparison table) |
| grant readiness biotech | Low-Medium | High | Should start crawling now | Commercial | Existing `/blog/grant-readiness-in-14-days` (refresh + checklist tool) |
| how NIH SBIR reviewers score proposals | Medium | High | Should start crawling now | Informational | Existing `/blog/how-reviewers-think` (refresh + add real reviewer quote) |
| FreeMind Group alternative | Low | Medium | Not ranking | Commercial / BOFU | NEW comparison page |

---

## 6. Verification Commands

To confirm the audit's findings at any time without re-running the full skill:

```bash
# Apex must 308 to www
curl -sI https://nexabiopartners.com/ | grep -E "HTTP|location"
# Expect: HTTP/2 308 / location: https://www.nexabiopartners.com/

# Homepage must be 50+ KB with FAQ schema
curl -sL https://www.nexabiopartners.com/ | wc -c
# Expect: ~56,500
curl -sL https://www.nexabiopartners.com/ | grep -c '"@type":"FAQPage"'
# Expect: 1

# Blog post must have its own title + canonical
curl -sL https://www.nexabiopartners.com/blog/sbir-phase-1-vs-phase-2 | grep -E "<title>|canonical"

# /blank, /leadership, /contact must redirect (when fixed)
for u in /blank /leadership /contact; do curl -sI "https://www.nexabiopartners.com$u" | grep -E "HTTP|location"; done

# Sitemap should use www URLs (once sitemap.cjs is updated)
curl -sL https://www.nexabiopartners.com/sitemap.xml | grep -o "https://[^<]*"
```

---

## 7. What the next audit should check

Schedule a v3 audit ~30 days after the BARDA / ARPA-H / longevity pillars ship. At that point measure:

1. Has Google deindexed `/leadership`, `/blank`, `/contact` (and the apex versions of all URLs)?
2. Are the new pillar pages indexed and ranking on long-tail variants?
3. Does the brand SERP look cleaner (fewer competing "Nexa" entries above the fold)?
4. AI/LLM citation check: do ChatGPT, Claude, and Perplexity now mention Nexa Bio Partners in answers to "best non-dilutive funding consultant for biotech" or "BARDA consultant"?
5. Has anyone in trade press picked up a Nexa thought-leadership piece, and does that create the backlink that nudges Knowledge Graph?

A v3 audit should be lightweight - 30-45 minutes of work to verify items 1-5 against this baseline.
