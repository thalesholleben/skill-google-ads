# 03 - Bidding Strategies and Auction Insights

> Load this file when the user asks about bidding strategy, adjustments, auctions, competition, Auction Insights, or impression share.

---

## 1. Quality Score and Ad Rank in depth

### How Ad Rank is calculated in each real-time auction

```text
Ad Rank = bid x Quality Score signals x extension impact x auction-time signals
```

**Quality Score signals** visible in the keyword report, while the real score is dynamic:
1. Expected CTR
2. Ad relevance
3. Landing page experience

**Auction-time signals** you do not see but that affect the auction:
- User device
- Exact location
- Time of day
- User's recent history
- Match type used
- Ad formats/extensions shown

### Quality Score weight in account economics

Conservative table, varies by vertical:

| QS | Effective CPC vs QS=10 |
|---|---|
| 10 | 1.0x, lowest |
| 7 | 1.4x |
| 5 | 2.0x |
| 3 | 4.0x |

**Moving from QS 5 to QS 7 reduces CPC by about 40%.** In an account spending $20,000/month, that can free $8,000 without increasing budget.

**36% of market keywords in 2026 are at QS <= 5** - this is the easiest money to recover in most audits.

### How to attack each component

#### Expected CTR
- Rewrite RSAs with **15 diverse headlines**: benefit, feature, social proof, CTA, urgency, differentiator.
- Ensure the **main ad group keyword appears in headlines** through Dynamic Keyword Insertion or hard-coded text.
- Pause headlines with low preference or "Low" rating.
- Ad Strength **Excellent** gives +15% CTR vs Poor according to Google data.

#### Ad Relevance
- Reduce keywords per ad group when theme diversity is high. **If one ad group contains "kanban" and "gantt chart" keywords, split it into 2.**
- Put keywords in RSA headlines.
- Align descriptions with the promise behind the keyword.

#### Landing Page Experience
- **Speed is #1**: moving from 5s to 2s can lift QS 2-3 points in a few weeks.
- **Message match**: landing H1 repeats the ad keyword/headline or a close synonym.
- Mobile-first design, since more than 60% of search traffic is mobile in most verticals.
- Form above the fold or clear CTA above the fold.
- No intrusive pop-ups because Core Web Vitals penalize them.
- HTTPS, privacy policy, visible contact information: trust signals Google evaluates.

### Hidden metric: history

Quality Score **persists over time**. A keyword with 6 months of strong history can tolerate a weak ad for a few weeks; a new keyword is judged mostly on immediate signals.

**Implication**: when migrating a campaign, **prefer reusing the existing campaign** and pausing weak keywords instead of creating a new one from scratch. Otherwise you throw away QS history.

---

## 2. Bidding Strategies - choose by context

### Decision flowchart

```text
Does the campaign have >=30 conversions/month?
|-- No -> Maximize Conversions without cap, or cap at 1.5x target CPA
|         OR Maximize Clicks if priority is traffic/awareness
|
`-- Yes -> Do you have conversion value, either revenue or estimate?
          |-- No -> Target CPA
          |         target = current CPA x 1.0 to 1.1
          |
          `-- Yes -> Target ROAS
                    target = current ROAS x 0.9 to start
```

### Operational details

**Maximize Conversions**
- Good for starting and leaving the learning phase.
- Without a cap, it can scale spend from $30/day to $80/day if demand exists.
- **Always** cap the budget to avoid surprises.

**Maximize Conversions with tCPA cap** as transition
- Use for 14-30 days between Max Conv and pure tCPA.
- Cap = 1.3-1.5x the final target CPA.

**Target CPA (tCPA)**
- Stable after 30+ conversions in 30 days.
- Gradual ramp: -10% to -15% every 14 days.
- **Mistake**: dropping tCPA from $50 to $30 in 7 days -> learning reset + volume drop.

**Target ROAS (tROAS)**
- Requires reliable **value**, not just "it is a conversion".
- E-commerce: real revenue. Lead gen: average lead value x close probability.
- Initial target: 90% of current ROAS.
- More sensitive than tCPA and varies more with seasonality.

**Maximize Clicks**
- Awareness, top-of-funnel, informational sites.
- Accepts bid adjustments, unlike most Smart Bidding.
- No conversion focus.

**Manual CPC**
- In 2026: only for very specific cases, such as compliance restrictions, bid A/B tests, or accounts with fewer than 10 conversions/month where Smart Bidding lacks data.

### Portfolio Bidding shared strategy

Allows **grouping campaigns** under the same target/strategy. Advantages:
- Cross-learning: 3 campaigns with 15 conversions each become "45 conversions" for the algorithm.
- Central management: change 1 target instead of 3.
- **Can pair with Shared Budget** -> +13% conversions on average according to Google data.

When to use:
- Multiple campaigns with the same objective and same CPA target.
- Low individual volume but reasonable combined volume.
- Multiple geos with similar performance.

### Shared Budgets

One budget for multiple campaigns. Google distributes it by real-time demand.

**When to use:**
- Campaigns with the same objective and similar targets.
- You want dynamic allocation without micromanagement.

**When NOT to use:**
- Campaigns with different objectives, such as Brand vs Non-Brand.
- When you need to guarantee minimum budget for a specific campaign.
- Experiments, because it is not compatible.
- PMax, because it is not compatible.

**Recommended allocation by objective:**
- 50-60% conversion-focused: Search exact/phrase, RLSA, Shopping.
- 20-30% prospecting: Search broad, PMax, Demand Gen.
- 10-20% Brand defense.

---

## 3. Bid Adjustments - what still works in 2026

### The big truth: Smart Bidding ignores almost everything

In campaigns with tCPA / tROAS / Maximize Conversions:

| Adjustment | Works? |
|---|---|
| Device | No, ignored except -100% |
| Location | No, ignored except -100% |
| Demographic | No, ignored except -100% |
| Audience | No, Smart Bidding already sees it |
| Ad Schedule / dayparting | No, ignored |

### What still works

1. **Exclusion (-100%)**: fully blocks the segment. Useful for:
   - Excluding mobile when the landing page is desktop-only.
   - Excluding geos you do not serve.
   - Excluding audiences such as current customers from acquisition.

2. **Bid Adjustments in Maximize Clicks / Manual CPC**: here they still work normally.

3. **Location targeting with different targets**: create 2 identical campaigns for 2 geos with different tCPA targets. **This gives real granular CPA control by geo.**

### Implication

Do not waste time configuring "+20% mobile, -15% night, +10% female 25-34" in Smart Bidding campaigns. **All of that is ignored noise.**

### Structure as bid adjustment

The 2026 way to "adjust bid by geo" is:

```text
Before (legacy):
1 campaign, target Florida + Orlando bid +30%

Now (2026):
Campaign A: target only Orlando, tCPA $40
Campaign B: target Florida excluding Orlando, tCPA $60
```

This gives real control. Same principle applies to device, geo, and daypart.

---

## 4. Auction Insights - complete reading

### Metrics explained

#### Impression Share (IS)

```text
IS = impressions received / eligible impressions
```

- 80%+ -> strong presence; consider PMax/Display to scale.
- 50-80% -> healthy.
- < 50% -> something is limiting; check IS Lost.

#### Search IS Lost (Budget)
- How much you lost because of **budget**.
- > 20% -> budget is limiting. Decision: raise budget if CPA is good, or raise tCPA if you want more volume.

#### Search IS Lost (Rank)
- How much you lost because of **Ad Rank**, driven by QS + bid.
- > 30% -> low QS or overly conservative bid. **Attack QS first**, because it is cheaper and more durable than raising bids.

#### Absolute Top Impression Share
- Percentage of times your ad appeared in the absolute **#1 position** above everything.
- Brand campaigns: ideal **>80%**. < 50% means a competitor is aggressively buying your name.
- Non-Brand: 30-50% is healthy.

#### Top Impression Share
- Percentage of times the ad appeared in top positions 1-4.
- Lead gen target: 60-80%.

#### Overlap Rate
- How often another advertiser appeared **in the same auction** as you.
- Identifies **direct** competitors. Focus on the top 3.

#### Position Above Rate
- When you and another advertiser are in the auction, the percentage of times they appeared above you.
- > 50% means they have better QS + bid. Study their copy and landing page.

#### Outranking Share
- Percentage of times **you** appeared above the other advertiser, or they did not appear.
- A "win" metric against a specific competitor.

### Interpretation by symptom

| Symptom | Diagnosis | Action |
|---|---|---|
| IS Lost (Budget) > 30% | Demand > budget | Raise budget if CPA is good, or tighten tCPA to spend where conversion probability is higher |
| IS Lost (Rank) > 40% | Weak QS or low bid | Improve Ad Strength + landing speed; test higher tCPA for 14d |
| Absolute Top IS < 30% in Brand | Competitor buying your brand | Raise Brand bid; aggressive defensive campaign |
| Overlap > 60% with X | Direct competitor | Deep analysis of their ad + landing; differentiate |
| Position Above Rate > 60% for all top 5 | Weak overall Ad Rank | Full review: copy, extensions, landing pages |
| Volume stable but IS dropped | Market expanded: more eligible auctions, you did not grow | Test broad match carefully; open more geos |

### Should you buy competitor Brand?

**Yes**: if you are a challenger in a dominated market and have a clear value proposition to differentiate. Use **phrase match** on the competitor name + "compare" copy + dedicated landing page.

**No**: if the competitor has a much stronger brand; you will only raise both their CPC and yours.

**Caution**: NEVER use exact match on the competitor name. Google penalizes this, and the user does not literally want the competitor. Do not use the competitor name in headlines because of Google trademark policies.

---

## 5. Diagnosis: "Why did my CPC increase?"

In order of likelihood:

### 1. Quality Score dropped
- Check average QS for the top 20 keywords by spend. Did it fall? If yes, this is likely the cause.
- Root causes: new weak ad, slow landing after update, seasonality.

### 2. Competition entered
- Auction Insights: new player in top 5? Did overlap rate increase?
- Response: full copy + extensions + landing review.

### 3. Match expansion through close variants
- Search terms report: new queries appeared in the last 4 weeks?
- Exact keywords may now be catching more expensive variants.
- Response: negative bad variants.

### 4. tCPA / tROAS too tight
- Did you recently lower the target? CPC can rise when the algorithm has to "buy" only expensive conversions to hit the target.
- Response: temporarily relax the target.

### 5. Seasonality
- Is it real seasonality such as Black Friday, end of month, holidays?
- Response: use Seasonality Adjustment if the event is predictable.

### 6. Auction structure changes by Google
- Google updates sometimes recalibrate auctions.
- Monitor the Google Ads blog.

---

## 6. When to raise or cut bids, even in Smart Bidding

In Smart Bidding, **you do not change bids keyword by keyword** - you change the **target**.

### Raise tCPA: higher CPA target means you accept paying more per conversion

- **When**: you are beating target strongly, such as real CPA 30% below target, and want more volume.
- **How**: increase tCPA by 15-20% and observe for 14 days.
- **Adjustment signal**: volume grows while target is still beaten -> good.

### Cut tCPA: more aggressive target

- **When**: real CPA is above target and you need to tighten.
- **How**: cut **gradually**, -10% to -15% every 2 weeks.
- **Risk**: volume may fall. If conversions fall proportionally, that is natural; if they fall **more than proportionally**, the target is too tight.

### When NOT to change

- After a recent change; wait 14 days.
- In very low-volume campaigns under 10 conversions/month, where signal is unreliable.
- During a seasonal event; wait for it to pass.

---

## 7. Sources (2026 research)

- [Quality Score - Google Ads Help](https://support.google.com/google-ads/answer/6167118)
- [Quality Score 2026 - Store Growers](https://www.storegrowers.com/google-ads-quality-score/)
- [Quality Score in automation-heavy accounts - Optmyzr](https://www.optmyzr.com/blog/google-ads-quality-score/)
- [Bid Adjustments 2026 - Bigeye](https://www.bigeyeagency.com/insights/google-ads-bid-adjustments-in-2026-what-still-works-whats-changed-and-where-most-campaign-managers-get-it-wrong)
- [Auction Insights - Google Ads Help](https://support.google.com/google-ads/answer/2579754)
- [Auction Insights 2026 - Growth Minded Marketing](https://growthmindedmarketing.com/blog/google-ads-auction-insights/)
- [Auction Insights to Outrank - Search Engine Land](https://searchengineland.com/google-ads-auction-insights-461513)
- [Shared Budgets 2026 - Digital Marketing Knight](https://www.digitalmarketingknight.com/using-shared-budgets-in-google-ads/)
- [Portfolio Bid Strategies - PixelRush](https://pixelrush.io/blog/how-to-use-portfolio-bid-strategies-in-google-ads-and-why-you-should/)
- [Ad Rank 2026 - Digital Marketing Knight](https://www.digitalmarketingknight.com/google-ads-ad-rank-explained/)
