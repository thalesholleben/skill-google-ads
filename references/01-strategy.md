# 01: Strategy (bidding, AI Max, measurement and audiences)

> Load to choose or change a bidding strategy, move a target, decide on AI Max, review conversions and
> attribution, or build audiences. For campaigns with few conversions, read 08 first.

Sources: `g/NNNN` = `https://support.google.com/google-ads/answer/NNNN`, checked on October 1, 2026, unless another
date is given. The full list is at the end. Heuristics are labeled as heuristics.

---

## 1. Bidding strategies in Search

| Strategy | For | Requires | Source |
|---|---|---|---|
| **Manual CPC** | per-keyword control in accounts with very few conversions, tests, compliance | nothing; no eCPC since March 31, 2025 (campaigns on eCPC became Manual CPC) | `g/2464964`, `g/2390250` |
| **Maximize clicks** | new campaign without data, traffic | accepts a campaign max CPC and every bid adjustment; no per-keyword CPC | `g/6268626` |
| **Maximize conversions** | conversion volume within the budget | a primary conversion configured | `g/7381968` |
| **Target CPA** | average CPA at the target | starts **with no history**, works for any size; evaluate with 30 days and **30+ conversions** | `g/6268632` |
| **Maximize conversion value** | value within the budget | a value per conversion | `g/7381968` |
| **Target ROAS** | average ROAS at the target | **15+ conversions in 30 days** in Search and Shopping; Google suggests coming from tCPA and reporting values for 4 weeks (or 1 to 2 conversion cycles) first | `g/6268637` |
| **Target impression share** | presence (brand defense): absolute top, top or anywhere, with a CPC cap | does not optimize conversions; Google Search network only | `g/9121108` |

**June 2026 rename** (`g/10353027`): "Maximize conversions with a target CPA" is now called **Target CPA**, and
"Maximize conversion value with a target ROAS" is **Target ROAS**. It is a label: behavior is the same, and the API,
Editor and app may show the old name during the transition. "Max conversions with a tCPA cap" and "Target CPA" **are
the same strategy**, not two phases.

Choice by volume regime (details in 03 section 3 and 08 section 6):
- **Low** (< 15 conversions in 30 days): Manual CPC with per-keyword caps, or Maximize clicks with a cap. Smart
  Bidding without a target can run, but there is no way to evaluate it; the choice is yours and stays written.
- **Medium** (15 to 49): Maximize conversions or Target CPA; tROAS only with real values.
- **High** (50+): Target CPA or Target ROAS, portfolios when several campaigns share the goal.

---

## 2. Learning ("Learning" status)

The status has three official triggers (`g/13020501`, `g/6263057`): a **new or re-enabled** strategy, a **setting
change** and a **composition change** (campaigns, ad groups or keywords added or removed). It usually lasts **1 to
2 conversion cycles**, depending on volume and strategy; it does not apply to Manual CPC.

- **There is no official 20% rule**, no fixed 7 to 14 days, and budget is not on the trigger list. A large target
  change produces an impact of similar size on spend or volume (`g/10433846`).
- After changing a target, wait 1 to 2 cycles and do not stack target changes within one cycle.
- Heuristic: move targets in 10 to 15% steps with a cycle between them, because it keeps the effect of each step
  readable, not because Google requires it.

---

## 3. Targets: starting value, adjustments and the August 17, 2026 change

- **Official starting value:** recommended tCPA = the average CPA of the last 30 days adjusted for conversion delay
  (`g/6268632`); recommended tROAS = the actual ROAS of recent weeks, without the last days (`g/6268637`). "Start
  10 to 20% above" and "tROAS at 90%" are market heuristics.
- **Compare results with the "average target"** (Avg. target CPA), not the typed target: it already includes
  device adjustments and target changes in the period (`g/6268632`).
- **August 17, 2026** (`g/17061251`): a tCPA or tROAS campaign **limited by budget** delivers close to the declared
  target, including when the budget changes. Campaigns that were beating the target (target 10, real CPA 5) tend
  to rise to the target; Google does not move the target for you. The **Bid Target Adjustment Tool** (since July
  6, 2026; "Review your campaign targets" or Campaign > Settings > Bidding) applies a target from recent
  performance. It covers Search, Shopping, PMax, Demand Gen and Travel. Old targets on budget-limited campaigns
  need a review.
- **Save as experiment** (`g/6268632`): a target or strategy change can run as an experiment instead of being
  applied directly (see 05).

---

## 4. Seasonality and data exclusions

- **Seasonality adjustment** (`g/10369906`): only when you expect a **large** conversion rate change in a short
  event. Ideal for **1 to 7 days**; it can work poorly above 14. In Search, only with tCPA and tROAS.
- **Data exclusion** (`g/10370710`): for measurement failures (broken tag, site down, wrong import), with Smart
  Bidding on conversions or value. It excludes clicks: cover at least 90% of the affected clicks including
  conversion delay, and do not use it often or for long periods.
- Predictable seasonality of the account itself does not call for an adjustment: compare with the same week last
  year before acting (08, section 5).

---

## 5. Bidding and budget features, 2025 to 2026

| Feature | State | Source |
|---|---|---|
| **Smart Bidding Exploration** | opt-in, Search with **Target ROAS** only: a ROAS tolerance to capture new search categories within current targeting; extension to PMax (beta) and Shopping announced at GML 2026 | `g/15489627`, GML 2026 blog |
| **Journey-aware bidding** | beta (GML, May 20, 2026): Search with tCPA learns from journey goals from lead to sale, biddable or not | GML 2026 blog |
| **Campaign total budgets** | Search, Shopping and PMax: a budget for a period of 3 to 90 days, new campaigns only, never charges above the total; not compatible with shared budgets | `g/10486938` |
| **Demand-led pacing** | announced at GML 2026, no help page yet | GML 2026 blog |

---

## 6. AI Max for Search

It is not a campaign type: it is a set of features inside a Search campaign (`g/15910187`; API guide at
`developers.google.com/google-ads/api/docs/campaigns/ai-max-for-search-campaigns/getting-started`).

| Feature | Level | What it does |
|---|---|---|
| Search term matching | on or off per ad group | matches searches beyond your keywords (broad and keywordless expansion) |
| Text customization (formerly ACA) | campaign | generates text from your site and assets |
| Final URL expansion | campaign; requires text customization | picks the landing page; with it on, **pins can be ignored** |

Controls: **brand inclusions** (campaign and ad group) and **brand exclusions** (campaign), **locations of
interest** per ad group (the person still has to be inside the campaign targeting), **URL inclusions** (ad group)
and **exclusions** (campaign), **text guidelines** (beta: up to 25 excluded terms of 30 characters and 40
restrictions of up to 300). **AI Brief** (closed beta since April 30, 2026; Dutch, French, German, Italian,
Japanese, Portuguese and Spanish added on September 23, 2026): steers AI Max in natural language with
**messaging**, **matching** and **audience** guidelines, with previews of sample assets and searches before you
commit; existing text guidelines move into messaging guidelines. AI Max also reached Shopping campaigns and travel
formats, and final URL expansion supports mandatory text disclaimers (Google blog, April 30, 2026).

Reporting: search terms show the "AI Max" match type with its source, and there is a combined view of term,
headline and URL (`ai_max_search_term_ad_combination_view` in the API). A unified report (search term, the asset
the person saw and the landing page) was announced on September 23, 2026 for later in the year, without a date.

Lift reported by Google: +14% conversions or value at a similar CPA or ROAS (internal 2025 data, outside retail);
+27% only for campaigns with more than 70% of conversions from exact or phrase; the full package yields +7% over
search term matching alone. AI Max does little in budget-limited campaigns.

**Migration (what actually happened):**
- Creating DSA, automatically created assets (ACA) and the campaign-level broad setting has been blocked since
  **August 3, 2026**.
- **ACA and the campaign-level broad setting** migrated from **September 1 to 30, 2026**.
- **DSA was postponed** (update of June 11, 2026): automatic migration from **February 1 to 28, 2027**, notice on
  January 15, 2027.
- **Regular broad keywords do not migrate.**
- API versions released after September 1, 2026 remove those objects; in v25 you can still read
  `campaign.aca_migration_date_time` and `campaign.broad_match_migration_date_time`.

When to turn it on: in medium or high regimes, with a conversion that measures what matters and the capacity to
read search terms every week. In low-volume B2B, a third-party case saw CPL go from $493 to $850 with AI Max (Search
Engine Land, 2026). Once on: reinforce negatives, use brand and URL exclusions, and read "AI Max" terms separately.

---

## 7. Measurement

**Goals** (`g/10995103`): a **primary** conversion counts in "Conversions" and in bidding, if the campaign uses its
goal; a **secondary** one only shows in "All conversions". A campaign uses the account default goals or its own
(1 custom goal per campaign). "Include in Conversions" is the old name for primary. Promoting a secondary action to
primary just "to feed bidding" poisons the signal.

**First, what the action measures.** Name and category prove nothing: check the source (tag, GA4, call), the
counting ("One" or "Every") and, on the site, what fires the tag. A "submit lead form" action on a site whose
buttons all link to a third-party booking domain is measuring an outbound click. To check: fetch the final URL with
a browser User-Agent (many servers answer 406 or 403 to clients without one, which is not a 404), look for a
`<form>`, and read the public Google Tag Manager container (`https://www.googletagmanager.com/gtm.js?id=GTM-XXXX`)
for the trigger of the conversion tag.

**Attribution** (`g/6259715`, `g/6394265`): only **last click** and **data-driven** exist since 2023; data-driven is
the default, with no data minimum, and Google recommends 200+ conversions and 2,000+ interactions in 30 days for it
to work well. Bidding reads the credit of the chosen model.

**Enhanced Conversions** (`g/16884284`, `g/15712870`): since April 2026 Google Ads accepts user-provided data from
the tag, Data Manager and the API at the same time; since **June 2026**, web and leads are **one on/off switch**,
migrated automatically. The size of the gain shows in the account's impact report (the "20 to 40%" that circulates
has no official source).

**Offline conversion import and EC for Leads:** since June 15, 2026 they go through the **Data Manager API**
(`g/15713840`); the Google Ads API blocks them for developers without legacy access. Qualified leads goal: at least
15 conversions in 30 days (`g/13489421`). For lead generation the flow is: GCLID saved with the form, kept in the
backend or CRM, and the lead stage (qualified, sale) sent back to Google. Without that loop, bidding optimizes
volume, not quality.

**Consent Mode:** Google's requirement is for users in the EEA (with handling for the UK and Switzerland); elsewhere
the obligation comes from local privacy law, on the advertiser (`g/10000067`, `g/12329599`).

---

## 8. Audiences

1. **Customer Match** (your list): exclude customers from acquisition, signal in PMax. Since **April 1, 2026**, a
   developer token with no Customer Match request between October 1, 2025 and March 31, 2026 gets
   `CUSTOMER_NOT_ALLOWLISTED_FOR_THIS_FEATURE`: the path is the Data Manager API (API deprecations page).
2. **Your data segments** (formerly remarketing): site visitors, video viewers, app users.
3. **Custom segments**: competitor keywords and URLs.
4. **In-market** and **affinity**: top of funnel.

- **Demand Gen lookalikes** (`g/13541369`): since March 2026 they work in **suggestion mode**: the seed list becomes
  a signal and stops restricting. The "1,000 active users minimum" is a Display & Video 360 rule, not Google Ads.
- With Smart Bidding, audiences in Search are automatic signals; audience bid adjustments are not used (03, section
  4). Audiences in "Observation" are for reading, not restricting.
- Audience signals in PMax guide, they do not restrict.

---

## 9. When to change phase

| Symptom | Next step |
|---|---|
| Target hit, volume flat for 2+ months | read the marginal CPA (03, section 7) before loosening the target; tROAS only with real values |
| ROAS on target, profit flat | values by margin (Merchant Center) or lead values by stage |
| Lead gen with a known close rate | offline conversions by stage (section 7), once volume passes ~15 in 30 days |
| Heavy new competitor | impression share and rank loss (03, section 6); Auction Insights in the UI |
| Search saturated (high share, rising cost) | PMax or Demand Gen as a complement, never a replacement |
| Several offers in one campaign | split when each one's volume supports its own bidding; otherwise, a portfolio |

---

## Sources

Google Ads Help (checked October 1, 2026): `g/6268632` Target CPA; `g/6268637` Target ROAS; `g/10353027` Search
bidding reorganized; `g/13020501` and `g/6263057` learning and bid strategy status; `g/10433846` goals and target
changes; `g/17061251` the August 17, 2026 change; `g/2464964` end of eCPC; `g/2390250` Manual CPC; `g/6268626`
Maximize clicks; `g/7381968` Maximize conversions; `g/9121108` target impression share; `g/10369906` seasonality
adjustments; `g/10370710` data exclusions; `g/15489627` Smart Bidding Exploration; `g/10486938` campaign total
budgets; `g/15910187` AI Max; `g/10995103` conversion goals; `g/6259715` and `g/6394265` attribution; `g/16884284`
and `g/15712870` Enhanced Conversions; `g/15713840` EC for Leads; `g/13489421` qualified leads; `g/13541369`
lookalikes; `g/10000067` and `g/12329599` consent.

Official blogs: GML 2026 bidding and budgets (https://blog.google/products/ads-commerce/bidding-budgeting-google-marketing-live-2026/);
DSA upgrade to AI Max (https://blog.google/products/ads-commerce/dsa-upgrade-to-ai-max-2026/); AI Max turns 1 and
AI Brief (https://blog.google/products/ads-commerce/ai-max-new-features/, April 30, 2026); AI Brief in more
languages and unified reporting (https://blog.google/products/ads-commerce/ai-max-language-reporting-features/,
September 23, 2026); campaign-level broad match and ACA migration
(https://ads-developers.googleblog.com/2026/08/migrate-campaign-level-broad-match-and.html); API deprecations
(https://developers.google.com/google-ads/api/docs/deprecations).

Third party: Search Engine Land, B2B lead gen (https://searchengineland.com/google-ads-stronger-foundation-b2b-lead-gen-485288).
