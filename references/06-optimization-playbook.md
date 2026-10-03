# 06: Optimization (audit, cadence, budget reallocation and benchmarks)

> Load to audit an account, build the monthly plan, decide a budget reallocation or sanity-check a number with a
> benchmark. Cuts on performance go through 08; queries, through 07.

Sources: `g/NNNN` = `https://support.google.com/google-ads/answer/NNNN`, checked on October 1, 2026.

---

## 1. Thirty-minute audit

Do it in order; each step can invalidate the next ones. **Mark every check `ok`, `issue`, `unknown` (the evidence is
missing: say which) or `n/a`**, and never fill an unknown with what accounts usually look like.

1. **Measurement (5 min).** Which actions are primary, how they count and what they actually measure (07, query 4;
   08, section 9). Did an action change behavior in the period? Without this, the rest measures the wrong thing.
2. **Where the money goes (5 min).** Spend, conversions and CPA by campaign and ad group, **with `campaign.id`**; is
   the spend order the conversion order? A query without `campaign.id` mixes removed campaigns with live ones.
3. **Why it is limited (5 min).** `primary_status_reasons`, budget and rank loss, recommended budget, marginal CPA
   (03, sections 6 and 7).
4. **Search terms (10 min).** Coverage of the visible part; wrong-intent terms (gate A); n-grams (02, section 6).
5. **Ads and assets (3 min).** RSAs per ad group and Ad Strength; sitelinks, callouts and snippets present and
   serving (`campaign_asset` with metrics); the final URL answers (fetch with a browser User-Agent; a 406 without a
   User-Agent is not a 404).
6. **Competition (2 min).** Impression share and absolute top through the API; Auction Insights in the UI.
7. **Hour and day (with Manual CPC).** Spend by hour and weekday (07, query 16) before proposing an ad schedule: a
   B2B account can spend a third of its budget between 11 pm and 4 am with no leads. Before comparing days or
   devices by CPA, split the actions by what they measure (a weekend can carry only one kind of conversion).

**Output:** the check list with its marks; the 3 biggest wastes (with value), the 3 biggest opportunities; actions
for the week and structural actions, each with its reading rule written before (08, section 8).

---

## 2. Cadence

| When | What |
|---|---|
| Daily (automated if possible) | data collection, conversion maturation, anomaly alerts calibrated to the account, budget changes, credentials expiring |
| Weekly or twice a week | due hypotheses, search terms and negatives, plan with written rules, changes, log |
| Monthly | client report (07, section 4), budget proposals |
| Quarterly | structure, negative lists, goals, the volume regime of each campaign |

Anomaly alerts that do not fire false positives: a baseline with at least 5 days of spend in the window; spend up to
2x the budget on one day is not an anomaly; a drop in a known seasonal week compared with the same period last year.

---

## 3. Diagnosis by symptom

**"CPA went up."** CPA = CPC / CVR. Follow the order of 03, section 8 (measurement, mix, auction, search terms,
target, seasonality, sample, demand). With few conversions, compute the CPA interval before calling it a rise.

**"High CTR and low conversion."** The ad promises what the page does not deliver, wrong-intent terms, or a form
with friction. Check the text against the page and the search terms.

**"Volume flat with the target met."** Read the marginal CPA before loosening the target; high budget loss with a
good CPA is a budget proposal for the owner; then new keywords with the same intent, a neighboring region with the
same profile, or PMax as a complement.

**"Brand CPA low and non-brand high."** Normal. Check the brand's absolute top (a competitor buying your name).
Pausing brand "to save" hands the top spot to the competitor.

**"Ad Strength Poor everywhere."** The ad group's keyword missing from headlines, repeated headlines, too many pins
or no sitelinks (04, section 5). Remember: the rating is not an auction input.

---

## 4. Budget reallocation

**Budget belongs to the account owner** (budgets, account spending limit, new campaigns with their own budget,
re-enabling): build the proposal with numbers and risk, and apply only what is approved.

**Spend limits by the official rule** (`g/6385083`, `g/10487143`):
- on one day, up to **2x the budget**; on the day the budget changes, 2x the **highest** budget chosen that day;
- in a month with a constant budget, **daily x 30.4**;
- in the month the budget changes, **spend so far + new budget x days left**, counting the day of the change; that
  limit **stays fixed until the next change**: a campaign that changed earlier in the month does not go back to
  x 30.4, and a re-enabled campaign carries the spend it already had in the month.

Before proposing, add up the exposure of every campaign (including new, re-enabled and shared budgets), each with
its own history this month, and compare with the approved cap. The script refuses the case where the history does
not determine the limit:

```bash
python scripts/budget.py --days-left 16 --cap-day 60 --cap-month 1824 \
  --campaign name=search,budget=28,new=30,spend=430 \
  --campaign name=brand,budget=32,new=30,spend=470
```

Spending more than the budget on one day is not an overspend: Google balances it within the month. A cap of 60 a
day is not "1,800 a month": Google's monthly limit for a constant 60 is 60 x 30.4 = 1,824.

**Budget windows** (a promotional credit, an event budget): to stay under S over N days, counting the first and the
last day in the account time zone, the sum of daily budgets stays at **S / (2 x N), rounded down to cents**, because
Google can spend 2x every day. With 600 of credit over 10 days, 60 a day looks right and exposes up to 1,200; the
safe cap is 30.00 (30.01 x 20 is already 600.20). **If the window starts today, day one uses the highest budget
chosen today:** lowering from 90 to 30 today still exposes 180 today and 720 in the window. `scripts/budget.py
--window-budget 600 --window-days 10 --campaign ...,max_today=<highest today>` adds up the real exposure and refuses a
window that starts today without `max_today`. Two conditions before proposing a window: the credit balance
confirmed in Billing > Promotions (the API only shows what was granted, not what was used), and someone scheduled
to undo the budget when the window ends (an automation that runs on weekdays cannot undo a window that ends on a
Sunday).

**How to decide a reallocation** (heuristic, with the marginal CPA of 03, section 7):

| Situation | Action |
|---|---|
| CPA below target, high budget loss, acceptable marginal CPA | propose an increase |
| CPA on target | keep |
| CPA above target with stable volume | adjust target or keywords before cutting budget |
| CPA far above and falling, with enough sample (08) | propose a cut or a pause |

**One lever per round.** Bid and budget together make it impossible to know which one moved the result.

---

## 5. Benchmarks (sanity only, never a goal)

WordStream/LocaliQ **2026**: 13,474 US small and mid-sized business Search campaigns, April 2025 to March 2026,
Google and Microsoft. They are **medians**. "Conversion" is any tracked action, and they call cost per conversion
CPL. The publisher sells management and software.

| Category | CTR | CPC (USD) | Conversion rate | Cost per conversion (USD) |
|---|---|---|---|---|
| All | 6.64% | 5.42 | 8.18% | 66.69 |
| Home & Home Improvement | 6.47% | 8.33 | 8.05% | 90.92 |
| Attorneys & Legal | 5.87% | 9.87 | 5.55% | 131.63 |
| Business Services (a B2B proxy) | 6.10% | 5.87 | 4.85% | 93.69 |
| Industrial & Commercial | 6.57% | 5.87 | 8.20% | 75.19 |

- 2026 was stable against 2025; cost per lead fell for the first time in 5 years.
- Outside the US there is rarely a benchmark with a published method: use the Keyword Planner and the account's
  own history.
- **Before comparing, confirm the unit.** If a "lead" action actually measures an outbound click, the account's CPA
  does not compare with any CPL benchmark; only the part that is a real lead does.
- CTR-by-position tables are left out on purpose: the ones that circulate are organic results.

---

## 6. Anti-patterns

| Anti-pattern | Why it hurts | Do instead |
|---|---|---|
| Moving the target every week | learning never closes a cycle | 1 to 2 conversion cycles between changes |
| Pausing on "zero conversions" with few clicks | noise becomes a decision | gate B of 08 |
| Negatives term by term without n-grams or coverage | endless work and wrong percentages | 02, sections 5 and 6 |
| Applying every Google recommendation | many raise spend, not results | evaluate one by one |
| Comparing month with month without mix and seasonality | mix changes look like efficiency | decompose by campaign and compare with last year |
| Everything in PMax | no visibility of search terms and channels | Search as the base, PMax as a complement |
| Comparing CPA with a benchmark without checking the unit | wrong conclusion about the account | section 5 |

---

## 7. When to restructure

- Different offers in the same ad group or campaign, with volume to split.
- 90% of keywords in 2 ad groups.
- A PMax campaign cannibalizing brand Search.
- Dozens of campaigns with small spend each (consolidate; with low volume, always).
- A new strategic direction from the owner (audience, offer): it becomes a plan with rules written before launch.

---

## 8. Plan template

```markdown
# Plan: <account>, <date>
## Diagnosis
- Spend, primary conversions (by action), CPA; search term coverage; volume regime (08).
- Audit checks marked ok, issue, unknown or n/a.
- 3 symptoms with numbers.
## Changes
| # | What changes | Why (number) | Expected effect | Reading rule (written before) | Undo |
## Proposals for the owner (budget, direction)
| Campaign | Current | Proposed | Reason | Risk |
## Open and due hypotheses
```

---

## Sources

Google Ads Help (October 1, 2026): `g/6385083` daily budget; `g/10487143` budget changes during the month.
Benchmarks: WordStream 2026 (https://www.wordstream.com/blog/2026-google-ads-benchmarks) and LocaliQ
(https://localiq.com/blog/search-advertising-benchmarks/).
