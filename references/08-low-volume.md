# 08: Low-volume accounts

> Load before pausing, adding a negative, lowering a bid, judging a test or choosing a bidding strategy in a
> campaign with fewer than about 30 primary conversions a month. Most small businesses live here, and most
> "best practices" assume they do not.

Sources: `g/NNNN` = `https://support.google.com/google-ads/answer/NNNN`, checked on October 1, 2026. Third-party
numbers are labeled as such; heuristics are labeled as heuristics.

---

## 1. Which regime

Count **primary** conversions in 30 days, per campaign (or per portfolio, when the strategy is shared), on mature
days only.

| Regime | Primary conversions in 30 days | What changes |
|---|---|---|
| **Low** | fewer than 15 | Smart Bidding cannot be evaluated; cut only on intent (gate A) or with the statistical minimum (gate B); Google's A/B tests do not close |
| **Medium** | 15 to 49 | tROAS becomes possible (needs 15 in 30 days, `g/6268637`); tCPA can be evaluated with 30+ (`g/6268632`); tests only for large effects |
| **High** | 50 or more | the large-account rules of the rest of this skill apply as written |

Why these cuts: Google says tCPA can start **with no history** and "works for campaigns of all sizes", but
recommends **evaluating** it with 30 days and at least 30 conversions (`g/6268632`). A third-party study (Optmyzr,
14,584 accounts, 2024, excluding accounts under $1,500 a month) found that accounts with fewer than 25 conversions in
30 days do not reach the performance of those with more than 50. The two sides diverge, and the divergence stays
declared: the bidding decision in the low regime is yours, not the manual's.

---

## 2. Statistical unit first

Google Ads counts **actions**, not converted clicks. One click can produce two conversions (a call and a form), an
action counted "Every" counts several times per click, and data-driven attribution gives **fractional credit** (0.9992
of a conversion).

Every "how many clicks without a conversion are enough" calculation uses **p = the probability that one click
produces at least one conversion**. Aggregated data does not give that p, so the default is the **conservative p**:

```
p = conversions / (clicks * k)
k = the maximum number of primary conversions one click can produce
  = the number of primary actions counted "One" (ONE_PER_CLICK)
```

A smaller p asks for more clicks before cutting, so the error stays on the safe side. If any primary action counts
"Every" (`MANY_PER_CLICK`), or k is unknown, **there is no statistical cut recommendation**: the result is NO BASE.
The exception is a p measured outside the platform (unique clicks that became leads in your backend or CRM), passed
as `--click-cvr` with its source written.

To find k, read the primary actions and their counting:

```sql
-- validated on v25, returned rows
SELECT conversion_action.id, conversion_action.name, conversion_action.category,
  conversion_action.primary_for_goal, conversion_action.counting_type, conversion_action.status
FROM conversion_action
WHERE conversion_action.status = 'ENABLED' AND conversion_action.primary_for_goal = TRUE
```

Also check whether the campaign uses the account goals or its own (`conversion_goal_campaign_config` and
`campaign_conversion_goal`): an account primary action may not be in that campaign's conversions.

---

## 3. Pocket math

Everything below comes from `scripts/stats.py` (standard library only):

```bash
python scripts/stats.py clicks --conversions 33 --clicks 110 --actions-per-click 3   # minimum clicks
python scripts/stats.py zero --n 21 --click-cvr 0.02                                 # P(0) of a term
python scripts/stats.py poisson --events 5                                           # interval of a count
python scripts/stats.py cpa --cost 400 --conversions 5                               # CPA interval
python scripts/stats.py rate --successes 0 --trials 150                              # Wilson and rule of three
python scripts/stats.py compare --a 0/10 --b 4/10                                    # Fisher exact
```

**Zero conversions in n clicks.** If the term converted like the base, the chance of zero is P(0) = (1−p)^n. The
minimum for P(0) < 5% is n = ⌈ln 0.05 / ln(1−p)⌉:

| Converted-click p | 1% | 2% | 5% | 10% | 20% |
|---|---|---|---|---|---|
| clicks without a conversion for P(0) < 5% | 299 | 149 | 59 | 29 | 14 |

Example: with p of 2%, 21 clicks without a conversion happen 65% of the time on a perfectly good keyword. Pausing on
"zero conversions" at that point switches off keywords at random, often the very ones that will produce the next
lead.

**Rule of three.** Zero events in n trials give a 95% upper bound of about 3/n. Zero in 150 clicks: the real rate
can still be 2%.

**Exact Poisson interval** (count of conversions, 95%):

| conversions | 0 | 1 | 2 | 3 | 5 | 10 | 30 | 45 |
|---|---|---|---|---|---|---|---|---|
| interval of the mean | 0 to 3.69 | 0.03 to 5.57 | 0.24 to 7.22 | 0.62 to 8.77 | 1.62 to 11.67 | 4.8 to 18.4 | 20.2 to 42.8 | 32.8 to 60.2 |

With 5 conversions in a week and $400 of spend, the CPA of $80 has an interval of **$34 to $246**: a single week
decides nothing. With 3 conversions over the account's life, a CPA cannot be inferred.

**Comparing two rates with a small sample: Fisher exact, never z.** 0/10 against 4/10 gives p = 0.087 with two-sided
Fisher; an uncorrected z gives 0.025 and "approves" a difference that is not proven.

The Poisson interval holds for counts of independent events. With several actions per click the variance is larger
and the real interval wider: read the interval as the minimum uncertainty, not the maximum.

---

## 4. Cut gates

Every cut on performance goes through one of these gates, with the number written in the plan. Gates C and D are
heuristics and **only apply in medium or high regimes**. In any gate, the "zero conversions" branch needs gate B's
click minimum: zero conversions with few clicks is never grounds for a cut (with p of 2%, 2 clicks without a
conversion have P(0) = 96%).

| Gate | Applies to | Condition | Allowed action |
|---|---|---|---|
| **A, wrong intent** | term, keyword | the term contradicts the offer: do-it-yourself, jobs, courses, free when the offer is paid, a product you do not sell; read **by whole word**, and checked with `scripts/negatives.py` against the **lifetime** search terms (not just 90 days) and the active keywords. A store or competitor name does not qualify just for being a name (02, section 7) | a **phrase or exact** negative, without statistics, that blocks no converted term and no active keyword. A one-word broad negative only after the same test |
| **B, enough data** | keyword, term | zero conversions with clicks ≥ the minimum of section 3 (P(0) < 5%), over 90 days of mature days, and checked against the lifetime window | pause or a phrase negative, with the undo recorded |
| **C, ad** (medium and high) | ad | over its **lifetime**: 1,000+ impressions; CTR up to 75% of the best ad in the ad group; CPA 150%+ of the best, or zero conversions **with clicks ≥ gate B's minimum**; 2+ active ads remain in the ad group | pause only, never remove; re-evaluate at the next reading |
| **D, broad with a phrase sibling** (medium and high) | broad keyword | the same keyword in phrase in the same ad group; 100+ impressions; CTR up to 2.5%; zero conversions in 90 days **with clicks ≥ gate B's minimum** | pause only |

**Precedence:** gate A (intent) applies in any regime and does not depend on statistics. Cutting on performance in
the low regime is gate B only. Ending a test by the rule written before (section 8) is something else: it carries
out an approved decision, and the log says so, not "proven by performance".

**Abstention:** no mature day in the window, no base from section 2, or only provisional days: no cut on
performance. Gate A still applies.

What is **not** a reason to cut:
- "Spend above 3x the target CPA without a conversion." It is a **review trigger for intent**: by the Poisson
  approximation, if the term converted at the target, P(0) = e^−3 ≈ 5%; with several actions per click the real
  chance of zero is higher, so the rule is optimistic. "10x" and "a fixed $50" have no basis: $50 in an account with
  a CPA of 50 is 1x the CPA, where P(0) ≈ 37%.
- A window picked by eye. An ad with "zero conversions in 30 days" can have 6 in 90 days.
- A term classified by substring: "art" matches inside "smart watch" and drops terms into the wrong bucket.
  `scripts/n_gram_analysis.py` and `scripts/negatives.py` match whole words.

Negatives also cut good intent: `free` as a phrase negative blocks "free estimate" and "free quote"; "spreadsheet"
blocks buyers of software that replaces spreadsheets; a phrase with no conversions in 90 days can block terms that
converted earlier in the account's life. Every new negative goes through `scripts/negatives.py` with lifetime terms
(02, section 4).

---

## 5. Window, maturity and seasonality

- **Mature days only.** A day is complete after the conversion maturation window; a provisional day still receives
  late conversions. Read the real delay with `segments.conversion_lag_bucket` (in lead generation most conversions
  often land on the click day, but the tail can take a week or more).
- **30 days, 90 days and lifetime** before pausing anything on performance. Lifetime is
  `segments.date BETWEEN '2010-01-01' AND '<today>'`, never a cutoff date picked by eye.
- **Same week last year** before calling a drop an anomaly. Many local businesses have a weak week that repeats
  every year; an alert like "7-day CPA above 1.5x the 28-day CPA" fires a false positive every time it comes around.
- **Demand before merit.** An improvement (or a drop) with no change in the period reads first as demand and
  seasonality.
- **An isolated peak is an outlier**, not a baseline: compare with the average of 8 to 12 weeks.

---

## 6. Bidding with low volume

Official (`g/6268632`, `g/2472725`, `g/6268626`): tCPA can start with no history; Maximize clicks suits new
campaigns without enough data for tCPA or tROAS; Maximize clicks accepts a campaign max CPC and every bid
adjustment; eCPC no longer exists in Search since March 31, 2025 (`g/2464964`), so "Manual CPC" today is pure manual.

Practice of third parties for fewer than about 25 to 30 conversions a month (Search Engine Land, September 2026;
Optmyzr, 2024): Manual CPC or Maximize clicks with a cap, moving to Smart Bidding through an experiment once volume
arrives; a **configured** CPC cap that fits about 10 clicks in the daily budget. Micro-conversions as a signal only
help with differentiated values.

Patterns that repeat in small accounts (heuristics):

| Situation | What to do |
|---|---|
| Maximize clicks on broad B2B terms | it buys the cheapest click, which is the curious one; Manual CPC per keyword, with a cap, and headlines that filter |
| tCPA with high rank loss and budget to spare | do not buy volume with bids before reading the **marginal** CPA in `campaign_simulation` (03, section 7) |
| Budget / CPC gives few clicks a month | inventory limits before budget: budget / max CPC is a floor of clicks, not a ceiling; measure eligible impressions before asking for more money |
| The local search that converts costs more than the cap | the cap keeps you out of the auction that matters; raising it is a budget decision with a forecast, not a bid tweak |
| Bid and budget changed together | one lever per round, or you cannot tell which one moved |

Local demand is measured before promising volume: Keyword Planner volumes for the target geo, and the forecast
service for clicks and cost. An empty volume in the Planner means "below the reported minimum", not zero.

---

## 7. Testing with low volume

Google's experiments need dozens to hundreds of conversions per arm (05, section 2). With an 8% CVR, a 30% lift
needs about 2,300 clicks per arm. An account with 30 to 45 conversions a month needs 2 to 5 months to detect +50%
and 9 to 12 months for +30%. With a handful of conversions a month, it is impossible.

- **Ad rotation does not split people at random.** Two ads in the same ad group are not an A/B test: the reading is
  directional, never "proven".
- Only **big changes** are worth testing (offer, page, audience), judged by the interval of section 3.
- What replaces the test is the **rule written before** (section 8): it does not prove causality, but it stops the
  window and the criterion from being picked after seeing the number.

---

## 8. Rules written before launch

Before turning on a big change, write the launch date **L** and the rules by milestone, counted in complete days
since L. Each rule states a condition, an action, and whether the action is yours or a **proposal** for the owner
(budget and strategic direction are always proposals).

```markdown
Change: <what changes>        Launch date L: <YYYY-MM-DD>       Baseline: <window and numbers>
- L+7:  wrong-intent terms above X% of spend -> negatives (gate A) and tighter match types. [operator]
- L+14: an ad group with zero impressions for N days -> raise the bid within the cap; CTR below Y% with 300+
        impressions -> test new text. [operator]
- L+30: N clicks or more and zero leads -> proposal to review the page and the offer. [proposal]
- L+60: review with the owner: good leads, proposals, budget, criteria for offline conversions. [proposal]
Rollback: <how to undo, from the saved state>
```

---

## 9. Lead quality outside the platform

- **The Google Ads conversion is a reading; the lead that matters is the one in your backend or CRM.** Someone
  qualifies leads by hand in small accounts: keep that record next to the campaign data.
- **Before comparing CPA with a benchmark, check what the conversion measures.** An action named "form" that fires
  on a click to a third-party booking page measures an outbound click, not a sent form (proof: the page HTML has no
  `<form>`, and the public GTM container fires the tag on a link click). Its CPA does not compare with any market CPL.
- Sending good leads back to Google (Enhanced Conversions for Leads or offline import) only pays with volume: the
  qualified-leads goal asks for at least 15 conversions in 30 days (`g/13489421`), and since June 15, 2026 uploads go
  through the Data Manager API (`g/15713840`).

---

## Sources

Official (Google Ads Help, checked October 1, 2026): `g/6268632` Target CPA; `g/6268637` Target ROAS; `g/2472725`
choosing a strategy; `g/6268626` Maximize clicks; `g/2464964` end of eCPC; `g/13489421` qualified leads;
`g/15713840` Enhanced Conversions for Leads; `g/2453972` negative keywords.

Statistics: rule of three and Poisson intervals (van Belle, *Statistical Rules of Thumb*, chapter 2,
http://www.vanbelle.org/chapters/webchapter2.pdf; https://www.statsdirect.com/help/rates/poisson_rate_ci.htm);
interval and p duality (https://pmc.ncbi.nlm.nih.gov/articles/PMC4877414/).

Third parties: Optmyzr, impact of bidding strategies (https://www.optmyzr.com/blog/impact-of-ppc-bidding-strategies/);
Search Engine Land, manual versus automated (https://searchengineland.com/manual-automated-google-ads-campaigns-allocate-budget-487344)
and negatives by intent (https://searchengineland.com/negative-keywords-strategy-476563).
