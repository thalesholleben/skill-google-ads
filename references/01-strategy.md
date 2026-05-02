# 01 - Strategy (Smart Bidding, AI Max, Attribution, Audiences)

> Load this file when the user asks about bidding strategy, AI Max, attribution, audiences, seasonality, or high-level decision making.

---

## 1. Smart Bidding in 2026 - what changed

### The major shift: tROAS became the preferred default when value exists

For accounts with trackable conversion value, **tROAS** is the best default in 2026. Google optimizes for value, not only volume - the algorithm prioritizes a $200 conversion over ten $20 conversions. Without conversion value, you leave this advantage on the table.

| Strategy | When to use | Minimum volume | Risks |
|---|---|---|---|
| **Maximize Conversions** | Leaving the learning phase, new accounts, data collection | Any | No CPA ceiling - can scale spend without control |
| **Maximize Conversions + tCPA cap** | Transition between Max Conv and pure tCPA | 10-25 conv/month | Aggressive caps limit volume |
| **Target CPA (tCPA)** | Lead gen, known cost, efficiency focus | 30+ conv/30d (official: 50) | Can reduce volume; sensitive to >20% changes |
| **Target ROAS (tROAS)** | E-commerce, lead gen with lead value | 50+ conv/30d **+ value** | Worse than tCPA if value is unreliable |
| **Maximize Clicks** | Awareness, discovery, informational sites | Any | Does not optimize for conversions |
| **Manual CPC** | Very specific cases: compliance, tests | Any | High effort, losing all signals Smart Bidding reads |

### Notable 2026 changes

- **Cart Value Optimization** for e-commerce: when a user adds products to the cart, bids are adjusted by cart value in real time. Enable through Merchant Center.
- **Profit Margin Bidding**: upload margin by SKU to Merchant Center; Smart Bidding prioritizes high-margin over high-revenue. This kills the "beautiful ROAS, zero profit" trap.
- **Seasonality Adjustments**: warn the algorithm about predictable events such as Black Friday, launches, or trade shows. Without this, it overreacts to anomalies. Use for 1-14 day windows with expected CR change above 10%.

### Learning phase golden rules

The learning phase lasts **7-14 days** and resets when you:

- Change the bidding strategy.
- Change the tCPA/tROAS target by **more than 20%**.
- Change the budget by **more than 20%**.
- Add or remove significant keywords or ad groups.
- Pause and reactivate the campaign.

**Practical implications:**
- Do not touch targets every week. Wait 14 days before evaluating.
- If you need to cut CPA by 30%, do it in **two 15% steps** with 14 days between them.
- Do not copy or duplicate campaigns to "reset" without a strong reason - you throw away 100% of the learning.

### Setting realistic targets

- **Initial tCPA**: set it **equal to or 10-20% above current average CPA**. If current CPA is $50, start at $55.
- **Initial tROAS**: set it **below current ROAS** (90% of it) so the algorithm has room to optimize volume first.
- **Ramp**: reduce tCPA or increase tROAS by **10-15% every 2 weeks**, always confirming volume did not collapse.
- **Floor**: never set tCPA so low that the algorithm stops delivery - it will stop spending before accepting conversions.

---

## 2. AI Max for Search - 2026 migration guide

### What it is

AI Max **is not a new campaign type**. It is a set of 3 features that can be enabled inside existing Search campaigns:

1. **Search Term Matching**: broad-match-like expansion plus "keywordless targeting" - Google finds relevant queries you did not cover.
2. **Text Customization**: AI generates additional copy from the website and the assets already provided.
3. **Final URL Expansion**: automatically routes users to the best landing page on the site.

### Forced timeline

Starting in **September 2026**, Google **automatically migrates** all Dynamic Search Ads (DSA), Automatically Created Assets (ACA), and broad match into the AI Max framework. Accounts that have not migrated will be migrated.

### Expected performance (official Google)

- +14% conversions or value at similar CPA in the general case.
- +27% in campaigns that still rely mostly on exact + phrase.

### When to enable now vs wait

**Enable now if:**
- Tracking is solid: Enhanced Conversions ON, 30+ conv/month, conversion value configured.
- The site is well structured: dedicated landing pages, clean content.
- You can review search terms weekly.
- You already run broad match with Smart Bidding without major waste.

**Wait if:**
- Tracking is poor or uncertain.
- The site is generic or B2B with a single landing page.
- The vertical is sensitive: legal, finance, healthcare, where AI-generated text can create issues.
- You cannot review search terms and final URLs on a cadence.

### Mandatory controls after enabling AI Max

- **Brand exclusion lists**: block competitor brands where you do NOT want to appear.
- **Locations of interest**: specify geographies where an ad show is valuable, even if the user is outside the area.
- **Negative keywords**: strengthen them, do not loosen them. AI Max expands more than classic broad.
- **Final URL inclusions/exclusions**: define eligible and ineligible URL patterns.

---

## 3. Attribution in 2026 - Data-Driven Attribution (DDA)

### Current state

Only **2 models survive**: Last Click and Data-Driven Attribution. First click, linear, time-decay, and position-based models were retired.

**DDA is the default for all new conversion actions.** There is no longer a data minimum to use DDA, but Google recommends **200+ conversions + 2,000+ ad interactions in 30 days** for it to perform well.

### How DDA works

Machine learning compares paths from users who converted against paths from users who did not. It identifies which touchpoints made the difference and distributes **fractional credit** across all ad interactions in the journey.

### Why it matters for Smart Bidding

Smart Bidding **reads DDA credit** to decide bids. If you are on Last Click, you are telling the algorithm "only the final click counts" - it cannot properly value awareness or middle-funnel campaigns. **Move to DDA before any serious Smart Bidding optimization.**

### Enhanced Conversions - not optional in 2026

Enhanced Conversions sends hashed user data such as email or phone to match with the user's Google account. It recovers **20-40% of conversions lost** to cookies and iOS restrictions.

**Types:**
- **Enhanced Conversions for Web**: e-commerce and form fills.
- **Enhanced Conversions for Leads**: B2B and lead gen, matching the lead to the conversion when it closes offline.

**June 2026 change**: Enhanced Conversions for Web and for Leads will be **unified into a single toggle**. No more "which method should I use?".

### Offline Conversion Import (OCI) for lead gen

The flow:
1. Lead clicks -> GCLID is saved in the form as a hidden field.
2. CRM stores GCLID + hashed email with the lead.
3. When the lead closes, qualifies, or sells, the CRM sends the event back to Google Ads through API or upload.
4. Smart Bidding learns: "leads from this search/keyword profile close more often."

**Without OCI, you optimize for lead volume, not lead quality.** If 30% of leads become customers and 70% are junk, Smart Bidding does not know that and optimizes for the average.

### Consent Mode v2

In GDPR/LGPD markets: implement Consent Mode v2 so conversion signals from users who rejected cookies still feed modeling, not individual tracking.

---

## 4. Audience Targeting 2026

### Audience hierarchy by impact

1. **Customer Match (1P data)** - your list of customers, qualified leads, churned users. Use cases:
   - Exclude current customers from prospecting.
   - Build lookalike audiences for Demand Gen.
   - Use as an audience signal in PMax.
2. **Your Data Segments (formerly remarketing)** - site visitors, app users, video viewers.
3. **Custom Segments** - competitor keywords, competitor URLs, apps.
4. **In-Market** - Google identifies users actively researching the category.
5. **Affinity** - broad interests for top-of-funnel.
6. **Detailed Demographics** - age, parenthood, education, employment.

### What changed in 2026

- **Critical API change (April 1, 2026)**: Customer Match uploads through the Google Ads API stop working for developers who are not already using it. Migrate to the **Data Manager API**.
- **Lookalike**: now exclusive to **Demand Gen campaigns**. Minimum 1,000 active matched users in the seed list.
- **"Your data segments"**: the new name for remarketing lists - reflecting that these data feed Smart Bidding and PMax, not only retargeting.

### Audience strategy by funnel stage

| Stage | Audience | Campaign |
|---|---|---|
| **Aware** | Affinity, custom intent from blog/educational URLs | Display, Demand Gen |
| **Interest** | In-Market, competitor Custom Segments | Search broad + Display |
| **Consideration** | Site visitors, 75% video viewers | Search exact/phrase + RLSA |
| **Decision** | Cart abandoners, pricing page visitors | Aggressive RLSA bid + Shopping |
| **Customer** | Customer Match: exclude from acquisition, include in retention | RLSA upsell, email match Display |

### Audience signals in PMax

PMax accepts "audience signals" - you give the algorithm a hint, and it expands. The signal **does not lock targeting**; it is an input to the algorithm. Components:

1. **Customer Match**: top 10% LTV customers.
2. **Your Data**: visitors who viewed pricing.
3. **Custom Segments**: people searching for competitors.
4. **Demographics**: age/income ranges that historically convert.

### RLSA (Remarketing Lists for Search Ads)

RLSA lets you **change bids or copy** when someone in your list searches a generic term. Example: a returning visitor searches "best CRM" - you can bid +50% and show "Welcome back, ready to start?". In Smart Bidding campaigns, **lists become automatic signals** and do not require manual bid adjustments.

---

## 5. When to restructure strategy

Symptoms that it is **time to move to the next strategic phase**:

| Symptom | Next strategic step |
|---|---|
| CPA target is reached but volume has been flat for 2+ months | Consider tROAS with value or gradually increase tCPA |
| ROAS hits target but net profit is flat | Migrate to Profit Margin Bidding |
| Branded search grew organically | Add a Brand defense campaign with very high ROI |
| A strong competitor entered the auction | Defend Brand + invest in copy differentiation |
| Search saturated: IS > 80%, cost rising | Expand into PMax, Demand Gen, Display |
| Lead gen has known 30% lead-to-customer rate | Implement OCI to optimize for quality |
| Multiple verticals/products share the same structure | Split into separate accounts/campaigns so Smart Bidding can learn cleaner patterns |

---

## 6. Sources (2026 research)

- [Smart Bidding 2026 - groas.ai](https://groas.ai/post/google-ads-smart-bidding-strategy-guide-2026-target-cpa-vs-target-roas)
- [Value Based Bidding 2026 - Brainmine](https://www.brainminetech.com/blog/how-value-based-bidding-is-changing-the-way-google-ads-scales-profit-in-2026/)
- [About Target ROAS - Google Ads Help](https://support.google.com/google-ads/answer/6268637)
- [AI Max for Search Campaigns - Google Ads Help](https://support.google.com/google-ads/answer/15910187)
- [DSA upgrading to AI Max - Google Blog](https://blog.google/products/ads-commerce/dsa-upgrade-to-ai-max-2026/)
- [AI Max Migration Guide - Vizup](https://www.tryvizup.com/blog/replace-dynamic-search-ads-with-ai-max-your-2026-migration-guide)
- [Attribution Modeling 2026 - ALM Corp](https://almcorp.com/blog/attribution-modeling-google-ads/)
- [Future of attribution is data-driven - Google Blog](https://blog.google/products/ads-commerce/data-driven-attribution-new-default/)
- [Customer Match - Google Ads Help](https://support.google.com/google-ads/answer/6379332)
- [Customer Match API change April 2026 - ALM Corp](https://almcorp.com/blog/google-ads-api-customer-match-disabled-april-2026/)
- [Audience Targeting 2026 - AdNabu](https://blog.adnabu.com/google-ads/google-ads-audience-targeting/)
- [Enhanced Conversions for Leads - Google Ads Help](https://support.google.com/google-ads/answer/15713840)
