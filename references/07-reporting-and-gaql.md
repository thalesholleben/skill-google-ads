# 07 - Reporting, GAQL, and Python Automation

> Load this file when the user asks to generate reports, write GAQL queries, automate data extraction, or build Google Ads dashboards.

---

## 1. GAQL - Google Ads Query Language

GAQL is the query language of the Google Ads API. Its syntax is similar to SQL.

### Basic structure

```sql
SELECT
  [fields: resource.field, metrics.field, segments.field]
FROM
  [resource]
WHERE
  [conditions]
ORDER BY
  [field] DESC
LIMIT
  [n]
```

### Main resources

| Resource | Contains |
|---|---|
| `campaign` | Metrics by campaign |
| `ad_group` | Metrics by ad group |
| `keyword_view` | Metrics by keyword |
| `search_term_view` | Real triggered search terms |
| `ad_group_ad` | Metrics by ad |
| `geographic_view` | Metrics by location |
| `hourly_metrics_view` | Metrics by hour |
| `audience_view` | Metrics by audience |
| `asset_view` | Asset/extension metrics |
| `campaign_audience_view` | Audiences at campaign level |

---

## 2. Ready-to-use queries

### Campaign performance for the last 30 days

```sql
SELECT
  campaign.name,
  campaign.status,
  campaign.bidding_strategy_type,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.average_cpc,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value,
  metrics.cost_per_conversion,
  metrics.search_impression_share,
  metrics.search_budget_lost_impression_share,
  metrics.search_rank_lost_impression_share,
  metrics.search_absolute_top_impression_share
FROM campaign
WHERE
  segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```

---

### Search terms with spend and conversions

```sql
SELECT
  search_term_view.search_term,
  search_term_view.status,
  campaign.name,
  ad_group.name,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.average_cpc,
  metrics.cost_micros,
  metrics.conversions,
  metrics.cost_per_conversion
FROM search_term_view
WHERE
  segments.date DURING LAST_30_DAYS
  AND metrics.impressions > 0
ORDER BY metrics.cost_micros DESC
LIMIT 1000
```

---

### Keywords with Quality Score

```sql
SELECT
  keyword_view.resource_name,
  ad_group_criterion.keyword.text,
  ad_group_criterion.keyword.match_type,
  ad_group_criterion.quality_info.quality_score,
  ad_group_criterion.quality_info.creative_quality_score,
  ad_group_criterion.quality_info.post_click_quality_score,
  ad_group_criterion.quality_info.search_predicted_ctr,
  campaign.name,
  ad_group.name,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.cost_per_conversion,
  metrics.average_cpc
FROM keyword_view
WHERE
  segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED'
  AND ad_group_criterion.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```

---

### Auction Insights by campaign

```sql
SELECT
  auction_insight.resource_name,
  campaign.name,
  auction_insight.domain,
  metrics.auction_insight_search_impression_share,
  metrics.auction_insight_search_overlap_rate,
  metrics.auction_insight_search_position_above_rate,
  metrics.auction_insight_search_top_impression_percentage,
  metrics.auction_insight_search_absolute_top_impression_percentage,
  metrics.auction_insight_search_outranking_share
FROM auction_insight
WHERE
  segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
ORDER BY metrics.auction_insight_search_impression_share DESC
```

---

### Performance by device

```sql
SELECT
  segments.device,
  campaign.name,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.average_cpc,
  metrics.cost_micros,
  metrics.conversions,
  metrics.cost_per_conversion,
  metrics.conversion_rate
FROM campaign
WHERE
  segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```

---

### Performance by hour of day

```sql
SELECT
  segments.hour,
  segments.day_of_week,
  campaign.name,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.cost_per_conversion
FROM campaign
WHERE
  segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
ORDER BY segments.day_of_week, segments.hour
```

---

### Performance by location

```sql
SELECT
  geographic_view.country_criterion_id,
  geographic_view.location_type,
  campaign.name,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.cost_per_conversion
FROM geographic_view
WHERE
  segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```

---

### Ad performance with Ad Strength

```sql
SELECT
  ad_group_ad.ad.id,
  ad_group_ad.ad.responsive_search_ad.headlines,
  ad_group_ad.ad_strength,
  ad_group_ad.policy_summary.approval_status,
  campaign.name,
  ad_group.name,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.conversions,
  metrics.cost_micros
FROM ad_group_ad
WHERE
  segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED'
  AND ad_group_ad.status = 'ENABLED'
ORDER BY metrics.impressions DESC
```

---

### Zero-conversion wasted spend (search terms)

```sql
SELECT
  search_term_view.search_term,
  campaign.name,
  ad_group.name,
  metrics.cost_micros,
  metrics.clicks,
  metrics.conversions,
  metrics.impressions
FROM search_term_view
WHERE
  segments.date DURING LAST_30_DAYS
  AND metrics.conversions < 0.01
  AND metrics.cost_micros > 5000000
ORDER BY metrics.cost_micros DESC
LIMIT 200
```

`cost_micros > 5000000` means more than $5 spent without conversion.

---

### Weekly time series

```sql
SELECT
  segments.week,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.cost_per_conversion,
  metrics.conversion_rate
FROM campaign
WHERE
  segments.date BETWEEN '2026-01-01' AND '2026-04-27'
  AND campaign.status = 'ENABLED'
ORDER BY segments.week
```

---

## 3. Google Ads automation scripts (JavaScript)

### Budget pacing monitor, runs daily

```javascript
// Sends email if projected spend > monthly goal x 1.10

function main() {
  var today = new Date();
  var dayOfMonth = today.getDate();
  var daysInMonth = new Date(today.getFullYear(), today.getMonth()+1, 0).getDate();

  var MONTHLY_BUDGET = 1800; // USD
  var EMAIL_RECIPIENT = "your-email@example.com";

  var campaigns = AdsApp.campaigns()
    .withCondition("Status = ENABLED")
    .forDateRange("THIS_MONTH")
    .get();

  var totalSpent = 0;
  while (campaigns.hasNext()) {
    var c = campaigns.next();
    totalSpent += c.getStatsFor("THIS_MONTH").getCost();
  }

  var projected = (totalSpent / dayOfMonth) * daysInMonth;
  var paceRatio = projected / MONTHLY_BUDGET;

  if (paceRatio > 1.10 || paceRatio < 0.80) {
    MailApp.sendEmail(
      EMAIL_RECIPIENT,
      "Google Ads Pacing Alert - " + today.toDateString(),
      "Current spend: $" + totalSpent.toFixed(2) + "\n" +
      "Month projection: $" + projected.toFixed(2) + "\n" +
      "Goal: $" + MONTHLY_BUDGET + "\n" +
      "Pacing: " + (paceRatio * 100).toFixed(1) + "%\n" +
      (paceRatio > 1.10 ? "ABOVE budget!" : "BELOW budget!")
    );
  }
}
```

---

### CPA anomaly detector, runs daily

```javascript
function main() {
  var LOOKBACK_DAYS = 14;
  var CPA_SPIKE_FACTOR = 1.5;
  var EMAIL_RECIPIENT = "your-email@example.com";

  var campaigns = AdsApp.campaigns()
    .withCondition("Status = ENABLED")
    .get();

  var alerts = [];

  while (campaigns.hasNext()) {
    var c = campaigns.next();
    var statsYesterday = c.getStatsFor("YESTERDAY");
    var statsTrailing  = c.getStatsFor("LAST_14_DAYS");

    var convYesterday = statsYesterday.getConversions();
    var costYesterday = statsYesterday.getCost();
    var convTrailing  = statsTrailing.getConversions();
    var costTrailing  = statsTrailing.getCost();

    if (convTrailing < 5) continue; // not enough data

    var cpaYesterday = convYesterday > 0 ? costYesterday / convYesterday : 999;
    var cpaTrailing  = costTrailing / convTrailing;

    if (cpaYesterday > cpaTrailing * CPA_SPIKE_FACTOR) {
      alerts.push(c.getName() + ": CPA yesterday=$" + cpaYesterday.toFixed(0) +
                  " vs 14d avg=$" + cpaTrailing.toFixed(0));
    }

    if (convYesterday === 0 && costYesterday > 50) {
      alerts.push(c.getName() + ": $" + costYesterday.toFixed(0) + " spent, 0 conv yesterday!");
    }
  }

  if (alerts.length > 0) {
    MailApp.sendEmail(
      EMAIL_RECIPIENT,
      "Google Ads Anomaly Detected",
      alerts.join("\n")
    );
  }
}
```

---

### Broken URL checker, runs daily

```javascript
function main() {
  var EMAIL_RECIPIENT = "your-email@example.com";
  var brokenUrls = [];

  var ads = AdsApp.ads()
    .withCondition("Status = ENABLED")
    .withCondition("CampaignStatus = ENABLED")
    .get();

  while (ads.hasNext()) {
    var ad = ads.next();
    var url = ad.urls().getFinalUrl();
    if (!url) continue;

    try {
      var response = UrlFetchApp.fetch(url, {muteHttpExceptions: true});
      var code = response.getResponseCode();
      if (code >= 400) {
        brokenUrls.push(url + " -> HTTP " + code + " (" + ad.getCampaign().getName() + ")");
      }
    } catch(e) {
      brokenUrls.push(url + " -> Error: " + e.message);
    }
  }

  if (brokenUrls.length > 0) {
    MailApp.sendEmail(
      EMAIL_RECIPIENT,
      "Broken URLs - Google Ads",
      brokenUrls.join("\n")
    );
  }
}
```

---

## 4. `.docx` report format (Python)

The scripts in `scripts/` generate Word reports. Section structure:

### Internal report (`build_report.py`)

```text
1. Executive Summary
   - Period KPIs
   - Comparison vs previous month

2. Performance by Campaign
   - Table: campaign x impressions x clicks x conv x CPA x CTR

3. Performance by Device
   - Table: Mobile / Desktop / Tablet

4. Search Terms - Top Performers
   - Top 20 converting queries

5. Zero-Conv Waste
   - Queries that burned budget without conversions

6. Auction Insights
   - Top 5 competitors + interpretation

7. Performance by County / Geo
   - Table: location x conversions x CPA

8. Keyword Analysis
   - Average QS, paused keywords, recommendations

9. Negative Keywords Added
   - Period list

10. Action Plan
    - Prioritized next steps
```

### Client report (`build_report_cliente.py`)

```text
Monthly Summary (Heading 2 - appears in table of contents)

1. Period Results (Heading 3)
2. Traffic Quality (Heading 3)
3. Market Positioning (Heading 3)
4. Improvements Applied (Heading 3)
5. Goals vs Actuals (Heading 3)
6. Budget Reallocation (Heading 3)
7. Strategic Notes (Heading 3)

[Font: Montserrat | Tone: positive | Omits: internal failures]
```

---

## 5. N-gram analysis in Python - how to use

The script `scripts/n_gram_analysis.py` analyzes search terms from a CSV exported from Google Ads.

### Input: export from Google Ads

1. Go to **Keywords -> Search Terms**.
2. Select period: 30-90 days.
3. Required columns: `Search term`, `Clicks`, `Impressions`, `Cost`, `Conversions`, `CTR`, `Avg. CPC`.
4. Export -> CSV.

### Run the script

```bash
python n_gram_analysis.py search_terms.csv
```

Output: `ngram_report.csv` with 3 sheets/tables:
- `1grams` - single tokens.
- `2grams` - word pairs.
- `3grams` - word trios.

Each table is sorted by descending `Cost`, with columns `Clicks`, `Conversions`, `CPA`, `CTR`.

### Interpret results

```text
1-gram: "free" | Cost: $85 | Conv: 0 -> negative "free" (exact match)
1-gram: "removal" | Cost: $420 | Conv: 15 -> core keyword, keep

2-gram: "floor removal" | Cost: $220 | Conv: 12 -> great, promote to exact
2-gram: "diy floor" | Cost: $45 | Conv: 0 -> negative "diy" or phrase "diy floor"

3-gram: "remove tile yourself" | Cost: $30 | Conv: 0 -> negative phrase
3-gram: "floor removal orlando" | Cost: $180 | Conv: 9 -> EXACT MATCH NOW
```

---

## 6. Looker Studio - dashboard template

Connection: Google Ads Data Source -> select account.

### Recommended pages

**Page 1 - Executive Summary**
- Scorecards: Spend, Conversions, CPA, CTR, ROAS.
- Time series: Conv + CPA for last 90 days.
- Bar chart: Campaigns by Conversions, sorted.

**Page 2 - Keywords & Quality Score**
- Table: Keyword, QS, Impr, Clicks, Cost, Conv, CPA.
- Filter: QS slider from 1 to 10.
- Conditional formatting: QS <= 5 in red.

**Page 3 - Geo & Device**
- Geo map: Conversions by county.
- Table: Device, Conv, CPA, CTR.

**Page 4 - Auction Insights**
- Table: Competitor, IS, Overlap Rate, AbsTop Rate.
- Trend: weekly comparison.

**Page 5 - Search Terms**
- Table: Search term, Cost, Conv, CPA.
- Filter: Conversions = 0 for waste analysis.

### Useful calculated fields

```sql
-- ROAS
SUM(conversions_value) / SUM(cost)

-- CPA
SUM(cost) / SUM(conversions)

-- Conv Rate
SUM(conversions) / SUM(clicks)

-- Zero-conv waste %
SUM(IF(conversions = 0, cost, 0)) / SUM(cost)
```

---

## 7. Monthly report checklist

Before delivering any report, validate:

- [ ] Correct period: start and end dates checked against the account.
- [ ] Conversions: counting **Primary only**, not mixed with Secondary.
- [ ] CPA calculated from Primary conversions.
- [ ] Auction Insights uses the same period as the report.
- [ ] Benchmark: compare with previous month + same month last year for seasonality.
- [ ] Relevant period notes: product launch, landing change, new campaign.
- [ ] Next steps are **specific and actionable**, such as "pause keyword X", not vague like "monitor performance".

---

## 8. Sources (2026 research)

- [GAQL Overview - Google Ads API](https://developers.google.com/google-ads/api/docs/query/overview)
- [GAQL Grammar - Google Ads API](https://developers.google.com/google-ads/api/docs/query/grammar)
- [Google Ads Scripts 2026 - groas.ai](https://groas.ai/post/best-google-ads-scripts-2026-install-guide-automation-limits)
- [Automate Reporting with AI - Cotera](https://cotera.co/articles/automate-google-ads-reporting-ai)
- [Scripts Automation 2026 - Yeezypay](https://yeezypay.io/blog/google-ads-scripts-in-2026-how-to-automate-monitor)
- [N-gram Analysis - Adalysis](https://adalysis.com/blog/n-gram-analysis-the-secret-to-scalable-search-term-management-in-google-ads/)
- [Free Python N-gram Script - Ayima](https://www.ayima.com/insights/ngram-script-for-google-ads.html)
