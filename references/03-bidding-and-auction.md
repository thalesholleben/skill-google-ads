# 03: Auction, Quality Score, bid adjustments and CPC/CPA diagnosis

> Load to understand why CPC or CPA moved, read impression share, decide a bid adjustment, a portfolio or a shared
> budget, or reason about how Target CPA behaves.

Sources: `g/NNNN` = `https://support.google.com/google-ads/answer/NNNN`, checked on October 1, 2026.

---

## 1. Ad Rank (what decides the auction)

Official factors (`g/1752122`): **bid**; **ad and landing page quality** (assessed in real time, in the auction);
**Ad Rank thresholds**; **auction competitiveness**; **search context** (location, device, time, terms, other ads);
**expected impact of assets and formats**. Ad Rank is computed again in every auction. There is no official
multiplicative formula ("bid x QS x extensions" is a simplification).

---

## 2. Quality Score: a diagnostic, not a KPI

Official (`g/6167118`, `g/6167123`):
- A 1 to 10 score per keyword, comparing you with advertisers who showed on **the same exact search over the last
  90 days**. Components: expected CTR, ad relevance, landing page experience.
- **The 1 to 10 number is not used in the auction**: the auction uses real-time assessments. Google says to use it
  as a diagnostic and **not to optimize Quality Score as a KPI**.
- Changing the match type does not change Quality Score.
- In the API: `ad_group_criterion.quality_info.*` (current score) and `metrics.historical_*_quality_score` (daily,
  accepts `segments.date`).

Third-party estimate, for order of magnitude only: WordStream (2013) modeled CPC as proportional to 1 / QS, which
gives QS 7 about **-29%** CPC against QS 5, QS 10 about -50% and QS 3 about +67% (3.3 times the CPC of QS 10). It is
not a Google number. The "5 to 7 cuts more than 40%" and "36% of keywords have QS 5 or less" that circulate have no
source.

How to move each component (what moves the real-time assessment):
- **Expected CTR:** headlines with the ad group's keyword and different angles; 2 good RSAs per ad group (04,
  section 5).
- **Relevance:** one theme per ad group; if the keywords ask for different texts, they are two ad groups.
- **Landing page:** speed, the same message as the ad, a visible form or button, trust signals. Landing page
  experience is not fixed in the ad.

**Quality Score 1 on several keywords of one ad group is usually structure, not bid.** Typical pattern: one ad
written for a couple dozen themes, a generic headline pinned in position 1, and a landing page that never uses the
search term, while the first-page bid estimate sits far above the bid. The order is: ad groups by theme with
headlines of the theme and the term written on the page; raising the bid first buys the same Quality Score at a
higher price.

---

## 3. Choosing a bidding strategy

```
Does the primary conversion measure what matters? (01, section 7)
├── No  -> fix measurement first. Until then: Manual CPC or Maximize clicks with a cap.
└── Yes -> How many primary conversions in 30 days, on mature days? (08, section 1)
          ├── < 15  -> Manual CPC with per-keyword caps, or Maximize clicks with a cap (08, section 6)
          ├── 15-49 -> Maximize conversions or Target CPA (target = 30-day average CPA adjusted for delay)
          │           tROAS only with real values and 15+ conversions in 30 days
          └── 50+   -> Target CPA or Target ROAS; portfolios when several campaigns share the goal
```

Details of each strategy, the June 2026 rename, learning and the August 17, 2026 change: 01.

---

## 4. Bid adjustments: what each strategy uses

Official (`g/2732132`, `g/6268632`, `g/6268637`):

| Adjustment | Manual CPC and Maximize clicks | Target CPA | tROAS, Maximize conversions and value |
|---|---|---|---|
| Device | used | **changes the target**: +40% on mobile with a target of 10 means a target of 14 on mobile | only -100% |
| Location | used | not used | not used |
| Ad schedule | used | not used (the schedule itself is respected) | not used (same) |
| Audience, demographics | used | not used | not used |

- Location and schedule adjustments **do not accept -100%** (they go from -90% to +900%). To stop showing in a
  place or at a time, **remove it from targeting** (remove the location, restrict the schedule): Smart Bidding
  respects that.
- For a geo that is already a target, creating a negative location for the same geo fails in the API: remove the
  target instead.
- Real control of CPA by region or device under Smart Bidding = **separate campaigns** with different targets, if
  each one has volume for its own bidding.

---

## 5. Portfolios, shared budgets and bid limits

- **Portfolio** (shared strategy): pools the data of campaigns with the same goal. **Bid limits** (minimum and
  maximum CPC) in tCPA and tROAS only exist in portfolios, apply only to the Search network, and Google does not
  recommend them (`g/6268632`).
- **Shared budgets** (`g/10487241`): +13% conversions on average for advertisers that adopt them with portfolios in
  Search (Google internal data, January 2024 to March 2025). Available in Search, Shopping, Display and Video;
  **not compatible** with campaigns in experiments, PMax, App and campaign total budgets. "Maximize" strategies that
  share a budget must be in the same portfolio.
- Do not put campaigns with different goals in one budget (brand and non-brand), nor one that needs guaranteed
  money.

---

## 6. Impression share and competition

Through the API, auction presence is **your own** and is always available:

| Metric | Where | Reading |
|---|---|---|
| `metrics.search_impression_share` | campaign, ad group, keyword | share of eligible impressions |
| `metrics.search_budget_lost_impression_share` | **campaign only** | lost to budget |
| `metrics.search_rank_lost_impression_share` | campaign, ad group, keyword | lost to Ad Rank |
| `metrics.search_top_impression_share`, `search_absolute_top_impression_share` | campaign, ad group, keyword | top and first position |

Readings:
- High budget loss with a good CPA: demand is bigger than the budget (a budget proposal for the owner).
- High rank loss: quality or bid; buying rank with bids is expensive (section 7).
- Gaining rank pushes the campaign into its budget later: budget loss that was 0% can start to appear right after
  quality improvements.
- Low absolute top on a **brand** campaign: someone is buying your brand; check Auction Insights.

**Auction Insights does not come out of the API for most developers** (the `metrics.auction_insight_*` metrics with
`segments.auction_insight_domain` need an allowlist from Google and answer 403 `METRIC_ACCESS_DENIED` otherwise;
there is no `FROM auction_insight`). Competitor comparison comes from the UI or its CSV export. Report metrics:
impression share, overlap rate, position above rate, top, absolute top and outranking share. Custom experiments
have no Auction Insights.

---

## 7. Target CPA in practice

- **tCPA aims at the average CPA; it does not cap the cost per click.** Some conversions cost more than the target
  and some less (`g/6268632`). A configurable CPC cap only exists in portfolios (section 5).
- **An economic reference, not a mechanism:** since average CPA = average CPC / CVR, if the average CPC already
  sits near target x average CVR (with a stable CVR and a similar auction mix), lowering the target tends to cut
  delivery. Example: target 40 x CVR 23% = 9.20 against a real CPC of 9.30 means there is little room below.
- **Marginal CPA decides whether buying volume is worth it.** `campaign_simulation` with `type = 'TARGET_CPA'` and
  `modification_method = 'SCALING'` returns about 10 points (0.5x to 4x the target) with conversions, cost and the
  required budget at each one. Marginal CPA = delta cost / delta conversions between neighboring points. When the
  average is 30 and the marginal is 100, raising budget or target buys each extra conversion at 100.
- **Why it is limited:** `campaign.primary_status_reasons` (`BUDGET_CONSTRAINED`, `SEARCH_VOLUME_LIMITED`...)
  models the current target, not the past, so it does not contradict a 0% budget loss. Budget suggestion:
  `campaign_budget.recommended_budget_amount_micros` (the recommendation resource does not carry the number in v25).
- Since August 17, 2026, a budget-limited campaign delivers close to the target, and one that beat the target loses
  the surplus (01, section 3).

---

## 8. "Why did CPC (or CPA) go up?"

Decompose before prescribing: **CPA = CPC / CVR**. Investigation order:

1. **Measurement.** Did conversions drop on a specific day? Did an action change behavior? (Google can start
   splitting calls between two call actions: add both.)
2. **Mix.** Did a more expensive campaign or ad group become a bigger share? Decompose by campaign before the total.
3. **Auction.** Did rank loss go up? A new competitor in Auction Insights (UI)?
4. **Search terms.** Did expansion bring new, worse terms? (Read `search_term_view` for the last 4 weeks.)
5. **Target.** Was the target tightened recently? Or is the campaign budget-limited after August 17, 2026?
6. **Seasonality.** Compare with the same week last year (08, section 5).
7. **Sample.** With few conversions, the CPA interval is too wide to call a rise (08, section 3).
8. **Demand before merit.** An improvement (or a drop) with no change in the period reads first as demand and
   seasonality, before crediting any change of yours.

---

## 9. When to move the target

- After a change, wait **1 to 2 conversion cycles** and do not change again within the same cycle (`g/10433846`).
- Low volume (low regime): the target cannot be evaluated; decisions follow rules written before (08).
- During a seasonal event: wait for it to pass, or use a seasonality adjustment for a short event (01, section 4).
- Bid and budget never in the same round.

---

## Sources

Google Ads Help (October 1, 2026): `g/1752122` Ad Rank; `g/6167118` and `g/6167123` Quality Score; `g/2732132` bid
adjustments; `g/6268632` Target CPA; `g/6268637` Target ROAS; `g/10487241` shared budgets; `g/10433846` target
changes. Google Ads API forum on Auction Insights (https://groups.google.com/g/adwords-api/c/8zPWm9AOwsI).
Third party: WordStream, Quality Score and cost (https://www.wordstream.com/blog/ws/2013/07/16/quality-score-cost-per-conversion).
