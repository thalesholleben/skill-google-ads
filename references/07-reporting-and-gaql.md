# 07: GAQL, the API and reporting

> Load to write a GAQL query, pull account data, verify a change or build a report. Every query below ran on
> Google Ads API v25 in October 2026 (read only); the state line says what came back.

---

## 1. How to query

GAQL (Google Ads Query Language) runs through the Google Ads API (`googleAds:search` or `googleAds:searchStream`,
with any official client library or REST) and inside Google Ads Scripts (`AdsApp.search(query)`). The UI Report
Editor does not take GAQL.

```text
POST https://googleads.googleapis.com/v25/customers/<customer_id>/googleAds:search
{"query": "SELECT campaign.id, metrics.clicks FROM campaign WHERE segments.date DURING LAST_7_DAYS"}
```

`search` returns pages: follow `nextPageToken` until it is empty before you treat the result as complete (the
scripts here refuse a JSON that still has a `nextPageToken`).

**Version:** v25 (v25.2 stable since September 23, 2026) was the newest on October 3, 2026; v22 sunsets on October 7,
2026, and v25 is supported until August 2027 (sunset calendar at
`developers.google.com/google-ads/api/docs/sunset-dates`). Since September 9, 2026 the developer token access level
moved to the Google Cloud project (developer token policy page).

**Rules that prevent wrong conclusions:**
- Every query that becomes a claim about "the campaign" carries `campaign.id` in the SELECT (`geographic_view`,
  `campaign_criterion` and `campaign_asset` return rows of removed campaigns).
- A field used in WHERE also goes in SELECT (`EXPECTED_REFERENCED_FIELD_IN_SELECT_CLAUSE`).
- `LAST_N_DAYS` excludes today; for "up to now", `segments.date BETWEEN '<start>' AND '<today>'`.
- `DURING` only accepts the API's literals (`LAST_7_DAYS`, `LAST_14_DAYS`, `LAST_30_DAYS`, `LAST_MONTH`...):
  **`LAST_90_DAYS` does not exist** and returns "Invalid date literal". A 90-day window is `BETWEEN`.
- Recent days are provisional: conversions arrive late. Decide only on mature days (08, section 5).
- `metrics.conversions` is by **click** date; to match calls, use `metrics.conversions_by_conversion_date`.
- The search terms report hides part of the spend: reconcile with the total (query 7).
- Currency is the account's; `*_micros` values divide by 1,000,000.

---

## 2. Queries

### 1. Campaigns: performance and auction presence

```sql
-- validated on v25, returned rows
SELECT campaign.id, campaign.name, campaign.status, campaign.bidding_strategy_type,
  metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions, metrics.conversions_value,
  metrics.search_impression_share, metrics.search_budget_lost_impression_share,
  metrics.search_rank_lost_impression_share, metrics.search_absolute_top_impression_share
FROM campaign
WHERE segments.date DURING LAST_30_DAYS AND campaign.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```

### 2. Why the campaign is limited and what Google suggests

```sql
-- validated on v25, returned rows
SELECT campaign.id, campaign.name, campaign.status, campaign.primary_status, campaign.primary_status_reasons,
  campaign_budget.amount_micros, campaign_budget.recommended_budget_amount_micros
FROM campaign
WHERE campaign.status = 'ENABLED'
```

### 3. Marginal CPA (target simulation)

```sql
-- validated on v25, returned rows
SELECT campaign_simulation.campaign_id, campaign_simulation.type, campaign_simulation.modification_method,
  campaign_simulation.start_date, campaign_simulation.end_date,
  campaign_simulation.target_cpa_point_list.points
FROM campaign_simulation
WHERE campaign_simulation.type = 'TARGET_CPA' AND campaign_simulation.modification_method = 'SCALING'
```

Each point has `targetCpaMicros`, `biddableConversions`, `costMicros` and `requiredBudgetAmountMicros`. Marginal CPA =
delta cost / delta conversions between neighboring points (03, section 7). `type = 'BUDGET'` often comes back empty.

### 4. Conversion actions: which are primary and how they count

```sql
-- validated on v25, returned rows
SELECT conversion_action.id, conversion_action.name, conversion_action.type, conversion_action.category,
  conversion_action.primary_for_goal, conversion_action.include_in_conversions_metric,
  conversion_action.counting_type, conversion_action.status
FROM conversion_action
WHERE conversion_action.status = 'ENABLED'
```

The k of 08 is the number of primary actions with `counting_type = ONE_PER_CLICK`. Campaign-level goals live in
`campaign_conversion_goal` and `conversion_goal_campaign_config`.

### 5. Conversions by action and campaign

```sql
-- validated on v25, returned rows
SELECT campaign.id, segments.conversion_action, segments.conversion_action_name,
  metrics.conversions, metrics.conversions_by_conversion_date, metrics.all_conversions
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
```

### 6. Conversion delay

```sql
-- validated on v25, returned rows
SELECT campaign.id, segments.conversion_lag_bucket, metrics.conversions
FROM campaign
WHERE segments.date BETWEEN '2026-07-01' AND '2026-09-30'
```

### 7. Search terms coverage

```sql
-- validated on v25, returned rows
SELECT campaign.id, metrics.clicks, metrics.cost_micros
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
```

```sql
-- validated on v25, returned rows
SELECT campaign.id, metrics.clicks, metrics.cost_micros
FROM search_term_view
WHERE segments.date DURING LAST_30_DAYS
```

Coverage = the second sum / the first sum, per campaign. `scripts/n_gram_analysis.py` takes the campaign totals as
`--base-clicks`, `--base-conversions` and `--base-cost` and prints the coverage.

### 8. Search terms with the keyword that triggered them

```sql
-- validated on v25, returned rows
SELECT search_term_view.search_term, search_term_view.status, campaign.id, ad_group.id,
  segments.keyword.info.text, segments.keyword.info.match_type, segments.search_term_match_type,
  metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions
FROM search_term_view
WHERE segments.date DURING LAST_30_DAYS AND metrics.impressions > 0
ORDER BY metrics.cost_micros DESC
```

### 8b. Lifetime search terms (for the negative keyword test)

```sql
-- validated on v25, returned rows
SELECT search_term_view.search_term, campaign.id, metrics.clicks, metrics.cost_micros, metrics.conversions
FROM search_term_view
WHERE segments.date BETWEEN '2010-01-01' AND '2026-10-03'
```

Replace the end date with today. Save the full result (all pages) as `.json` and pass it to
`scripts/negatives.py --terms`: a negative is checked against the term's whole life, not 90 days (02, section 4).

### 9. Campaign-level search terms (Search and PMax)

```sql
-- validated on v25, returned rows (Search); PMax not seen with data
SELECT campaign.id, campaign.advertising_channel_type, campaign_search_term_view.search_term,
  metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions
FROM campaign_search_term_view
WHERE segments.date DURING LAST_30_DAYS
```

In Search it covers the same visible part as `search_term_view`, aggregated by campaign; in PMax it is the path to
the search terms.

### 10. AI Max search terms (term, headline and URL)

```sql
-- validated on v25, returns empty unless AI Max is on
SELECT campaign.id, ai_max_search_term_ad_combination_view.search_term,
  ai_max_search_term_ad_combination_view.headline, ai_max_search_term_ad_combination_view.landing_page,
  metrics.impressions, metrics.clicks, metrics.conversions
FROM ai_max_search_term_ad_combination_view
WHERE segments.date DURING LAST_30_DAYS
```

### 11. Keywords with Quality Score (current and historical)

```sql
-- validated on v25, returned rows
SELECT campaign.id, campaign.status, ad_group.status, ad_group_criterion.status,
  ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
  ad_group_criterion.quality_info.quality_score, ad_group_criterion.quality_info.creative_quality_score,
  ad_group_criterion.quality_info.post_click_quality_score, ad_group_criterion.quality_info.search_predicted_ctr,
  metrics.historical_quality_score, metrics.cost_micros, metrics.conversions
FROM keyword_view
WHERE segments.date DURING LAST_30_DAYS AND campaign.status = 'ENABLED' AND ad_group.status = 'ENABLED'
  AND ad_group_criterion.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```

### 12. Ads: Ad Strength, approval and real status

```sql
-- validated on v25, returned rows
SELECT campaign.id, campaign.status, ad_group.id, ad_group.status, ad_group_ad.status, ad_group_ad.ad.id,
  ad_group_ad.ad_strength, ad_group_ad.policy_summary.approval_status, ad_group_ad.primary_status,
  metrics.impressions, metrics.clicks, metrics.conversions, metrics.cost_micros
FROM ad_group_ad
WHERE segments.date DURING LAST_30_DAYS AND campaign.status = 'ENABLED' AND ad_group.status = 'ENABLED'
  AND ad_group_ad.status = 'ENABLED'
```

An ad's whole life (before pausing it under gate C): replace the date with
`segments.date BETWEEN '2010-01-01' AND '<today>'`.

### 13. Campaign assets serving

```sql
-- validated on v25, returned rows
SELECT campaign.id, campaign.status, asset.id, asset.type, asset.source, campaign_asset.field_type,
  campaign_asset.status, metrics.impressions, metrics.clicks, metrics.conversions
FROM campaign_asset
WHERE segments.date DURING LAST_30_DAYS AND campaign.status = 'ENABLED'
```

Metrics on a call asset **do not prove calls**: they are the conversions of the impressions where it served. Proof of
a call is `call_view` (query 17).

### 14. Negatives at every level

```sql
-- validated on v25, returned rows
SELECT shared_set.id, shared_set.name, shared_set.type, shared_set.member_count, shared_set.status
FROM shared_set
```

```sql
-- validated on v25, returned rows
SELECT campaign.id, campaign_shared_set.shared_set, campaign_shared_set.status
FROM campaign_shared_set
```

```sql
-- validated on v25, returned rows
SELECT customer_negative_criterion.id, customer_negative_criterion.type,
  customer_negative_criterion.negative_keyword_list.shared_set
FROM customer_negative_criterion
```

```sql
-- validated on v25, returned rows
SELECT campaign.id, campaign_criterion.criterion_id, campaign_criterion.keyword.text,
  campaign_criterion.keyword.match_type
FROM campaign_criterion
WHERE campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'
```

The keywords of the lists live in `shared_criterion`. The account-level negative list is the `shared_set` of type
`ACCOUNT_LEVEL_NEGATIVE_KEYWORDS` pointed to by `customer_negative_criterion.negative_keyword_list`.

### 15. Where people were (county, physical presence only)

```sql
-- validated on v25, returned rows
SELECT campaign.id, campaign.status, segments.geo_target_county, geographic_view.location_type,
  metrics.clicks, metrics.cost_micros, metrics.conversions
FROM geographic_view
WHERE segments.date DURING LAST_30_DAYS AND campaign.status = 'ENABLED'
  AND geographic_view.location_type = 'LOCATION_OF_PRESENCE'
```

`geographic_view.location_type` separates **presence** (`LOCATION_OF_PRESENCE`, where the person was) from **interest**
(`AREA_OF_INTEREST`, the place they searched about). Without the filter both mix; to claim physical location, filter
presence. The view is more granular than the target; the configured target lives in `campaign_criterion`. Geo names
come from `geo_target_constant`.

### 16. Device and hour

```sql
-- validated on v25, returned rows
SELECT campaign.id, segments.device, segments.day_of_week, segments.hour,
  metrics.clicks, metrics.cost_micros, metrics.conversions
FROM campaign
WHERE segments.date DURING LAST_30_DAYS AND campaign.status = 'ENABLED'
```

### 17. Calls one by one

```sql
-- validated on v25, returned rows
SELECT campaign.id, call_view.start_call_date_time, call_view.call_duration_seconds, call_view.type,
  call_view.call_status
FROM call_view
```

`call_view` accepts neither `segments.date` nor `metrics.calls`: filter the date on your side. To prove that an
action receives the calls, correlate by day with `conversions_by_conversion_date` of **every** call-category action.

### 18. Verifying a change the same day

```sql
-- validated on v25, returned rows
SELECT change_status.resource_type, change_status.resource_status, change_status.last_change_date_time,
  change_status.campaign, change_status.ad_group
FROM change_status
WHERE change_status.last_change_date_time >= '2026-10-01 00:00:00'
  AND change_status.last_change_date_time < '2026-10-02 00:00:00'
LIMIT 10000
```

- **A half-open window up to the next midnight, in the account time zone.** A date without a time means midnight:
  `<= '2026-10-01'` misses every change of that day. `change_status` requires a closed range and a `LIMIT` of up to
  10,000.
- **It is not immediate:** the official documentation says a change can take **up to 3 minutes** to show
  (`developers.google.com/google-ads/api/docs/change-status`), and 10 minutes has been observed. An empty result
  right after applying proves nothing.
- **The check is re-reading the changed resources** (is the expected state there?); `change_status` comes after at
  least 3 minutes, queried again every minute for up to 15 minutes, and only then proves that **nothing beyond** the
  plan changed: a baseline before, a delta after, matched by resource identity. `change_event` lags 15 to 20 minutes
  and does not show changes made by Google.

### 19. Account spending limit

```sql
-- validated on v25, returned rows
SELECT account_budget.status, account_budget.approved_spending_limit_micros,
  account_budget.amount_served_micros, account_budget.approved_end_time_type, account_budget.total_adjustments_micros
FROM account_budget
```

`total_adjustments_micros` is the promotional credit **granted**, not used (usage and expiry only in the UI, under
Billing > Promotions).

### 20. Weekly series

```sql
-- validated on v25, returned rows
SELECT campaign.id, segments.week, metrics.clicks, metrics.cost_micros, metrics.conversions
FROM campaign
WHERE segments.date BETWEEN '2026-07-01' AND '2026-09-30' AND campaign.status = 'ENABLED'
ORDER BY segments.week
```

---

## 3. What does not come out of the API

| Data | Why | Where to get it |
|---|---|---|
| Auction Insights | `auction_insight_*` metrics need an allowlist (403 `METRIC_ACCESS_DENIED`); `FROM auction_insight` does not exist | the UI or its CSV export |
| Promotional credit usage and expiry | the API only has what was granted | Billing > Promotions |
| Asset performance labels in small accounts | come back `NOT_APPLICABLE` | none; decide by CTR and conversions with sample (08) |
| Daily and hourly data older than 37 months | retention limited since June 2026 | none |

Resources that **do not exist** in v25 (older guides cite them): `hourly_metrics_view` (use `segments.hour` on
`campaign`), `asset_view` (use `campaign_asset`, `ad_group_asset`, `asset_field_type_view`, `asset_group_asset` for
PMax), `FROM auction_insight`. For counties, `segments.geo_target_county` (query 15), not `country_criterion_id`.

---

## 4. Client report

A monthly report the client reads in five minutes, built from the queries above (no template file needed):

1. **Summary of the month** (3 sentences): spend, contacts by kind (calls, forms, bookings), cost per contact, and the
   comparison with last month **and** the same month last year.
2. **What each number measures**: one line per primary action ("call of 60+ seconds", "quote form sent").
3. **Performance table** by campaign: spend, clicks, contacts, cost per contact; a metric that got worse stays on
   its own line, not hidden in the total.
4. **Where people were** (query 15) and **when** (query 16), only if it changed a decision.
5. **What we did** this month and **why** (each change with its number).
6. **Next steps**, specific ("pause keyword X", "test page Y"), never vague ("monitor").
7. **Budget**: current, proposed and the reason, when there is a proposal.

Checklist before sending:
- [ ] Period checked against the account; recent days mature or marked as partial.
- [ ] Contacts counted by primary action, with what each one measures written; clicks on a phone number never added
      to contacts.
- [ ] Calls add up every call action (Google can split calls between two actions).
- [ ] Comparison with last month **and** with the same month last year.
- [ ] No market benchmark where the conversion is not the same unit.
- [ ] Specific next steps.

---

## 5. Scripts

`scripts/n_gram_analysis.py` (n-grams with coverage and a guard), `scripts/negatives.py` (overblocking test for
negatives), `scripts/stats.py` (the math of 08), `scripts/budget.py` (spend limits, caps and budget windows) and
`scripts/self_test.py`. Usage in `scripts/README.md`.

---

## Sources

Google Ads API (October 2026): release notes (https://developers.google.com/google-ads/api/docs/release-notes, read
October 3, 2026); v25 fields (https://developers.google.com/google-ads/api/fields/v25/overview); segments
(https://developers.google.com/google-ads/api/fields/v25/segments); PMax reporting
(https://developers.google.com/google-ads/api/performance-max/reporting); AI Max
(https://developers.google.com/google-ads/api/docs/campaigns/ai-max-for-search-campaigns/getting-started); sunset
dates (https://developers.google.com/google-ads/api/docs/sunset-dates); developer token
(https://developers.google.com/google-ads/api/docs/api-policy/developer-token); change status
(https://developers.google.com/google-ads/api/docs/change-status); deprecations
(https://developers.google.com/google-ads/api/docs/deprecations). Google Ads Scripts reference
(https://developers.google.com/google-ads/scripts/docs/reference/adsapp/adsapp).
