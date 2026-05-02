# 06 - Optimization Playbook (diagnosis, daily/weekly/monthly, benchmarks)

> Load this file when the user asks to optimize an account, run an audit, plan next steps, or needs an operating cadence reference.

---

## 1. 30-minute diagnosis (quick audit)

Workflow for reading a new or problematic account quickly. Use CSVs/UI in this order:

### Step 1 - Overview (5 min)

| Look at | What to look for |
|---|---|
| Performance tab -> last 30d | Trend of Conversions, CPA, CTR vs previous period |
| Recommendations tab | Optimization score, but treat carefully: many recommendations are pro-Google, not pro-account |
| Account-level alerts | Disapprovals, limited status, budget issues |

### Step 2 - Where the money goes (5 min)

| Look at | Symptoms |
|---|---|
| Campaign -> Cost descending | How much do the top 3 campaigns concentrate? Healthy concentration: 60-80% in top 3 |
| Campaign -> Conv. count descending | Is it the same order as Cost? If not, investigate gap |
| Campaign -> CPA | 3-5x variation between campaigns is normal; >10x is a red flag |

### Step 3 - Quality Score audit (5 min)

| Look at | Symptom |
|---|---|
| Keywords filtered by QS | Percentage of keywords with QS <= 5? If >30%, this is a major opportunity |
| Top 10 keywords by spend | Their QS? If <= 6, attack FIRST because improvement has high ROI |

### Step 4 - Search Terms (10 min)

| Look at | Action |
|---|---|
| Search Terms -> Cost descending, Conv = 0 | Negative candidates |
| Search Terms -> Conv > 5, high CTR | Candidates to promote to exact |
| Search Terms containing free, DIY, tutorial, salary, jobs | Obvious negatives list |

### Step 5 - Ad copy & extensions (3 min)

| Look at | Symptom |
|---|---|
| Ad Strength by ad group | How many are Poor or Average? These need refresh |
| Sitelinks / Callouts / Snippets | All filled? Minimum 6 sitelinks, 8 callouts |
| Extensions with Impr = 0 | Not serving; investigate rejection or low Ad Rank |

### Step 6 - Auction Insights (2 min)

| Look at | Symptom |
|---|---|
| Top 3 competitors | Who dominates overlap rate? |
| Position Above Rate | >50% for all means you are below; attack Ad Rank |
| Abs Top IS in Brand | <60% means competitor is buying your name |

### Diagnosis outputs

After 30 minutes you should have:

1. **3 largest sources of waste**, quantified in dollars.
2. **3 largest opportunities**, estimated in dollars or volume.
3. **3 immediate actions** for this week.
4. **3 structural actions** for the next 4 weeks.

---

## 2. Operating cadence

### Daily (5 min) - anomaly check

Run automated through script + email/Slack alert, or manual check.

**Alarm triggers:**
- Daily CPA > 1.5x trailing 14d average CPA.
- Daily spend > 1.3x trailing 14d average spend.
- Conv = 0 in a campaign with history of >3 conv/day.
- Daily CTR < 50% of average.
- Bid limited / budget limited for new campaigns.

**Common cause:** broken tracking, landing page down, ad disapproval.

### Weekly (60-90 min)

**Block 1 - Search Terms (20 min)**
- Mine top 100 search terms by spend.
- Add 5-20 negatives.
- Promote 1-3 top performer search terms to exact.

**Block 2 - Quality Score & Ad Performance (15 min)**
- Filter keywords with QS < 6 and spend > $X.
- Evaluate ad relevance / landing page experience flags.
- Pause headlines with Low performance rating.

**Block 3 - Bid review (15 min)**
- In Smart Bidding: adjust **target** if conversion volume is not meeting plan, but not every week.
- In Maximize Clicks/Manual: adjust granular bids if needed.
- Check IS Lost (Budget) and (Rank) by campaign.

**Block 4 - Extensions (10 min)**
- Which sitelinks have 0 impressions? Pause/replace.
- Add seasonal callouts if relevant.
- Verify location extension and GBP link.

**Block 5 - Audience review (5 min)**
- Performance of audience signals in PMax.
- Customer Match lists updated; refresh every 30 days is recommended.

### Every two weeks (90 min)

- **Budget reallocation**: campaigns hitting target with IS limited by Budget -> raise 20%; campaigns with CPA far above target -> cut or pause.
- **Auction Insights**: deep dive into competitor changes.
- **A/B testing decision**: define next experiment.
- **PMax asset refresh**: run Asset Reporting and replace low performers.

### Monthly (3-4 hours)

**Block 1 - Strategic analysis (60 min)**
- Month KPIs vs goals vs previous month.
- Track progress of active tests.
- Bid strategy decisions: migrate to tROAS? Add target tROAS?
- Plan for next month.

**Block 2 - N-gram analysis (30 min)**
- Run `scripts/n_gram_analysis.py` on last 30d search terms.
- Add batch of negatives + promote top n-grams.

**Block 3 - Auction Insights review (30 min)**
- Competitor changes.
- Brand defense status.
- New threat identification.

**Block 4 - Reporting (60 min)**
- Generate `.docx` with `scripts/build_report.py` for internal report and `scripts/build_report_cliente.py` for client report.
- Present findings to stakeholder.

**Block 5 - Tracking review (15 min)**
- Conversion actions: correct Primary actions?
- Conversion value up to date?
- Enhanced Conversions: active status and match rate >70%.
- DDA: ON.

### Quarterly (1 day)

- Complete structural audit.
- Match type & keyword strategy review.
- Account-level negatives review.
- Customer Match list cleanup.
- Campaign/ad group reorganization if needed.
- Budget allocation review based on ROI by campaign.

---

## 3. Advanced diagnosis by symptom

### Symptom: "CPA rose from $50 to $80 in 30 days"

Decomposition:

```text
CPA = Cost / Conv

CPA rises if:
  - Cost rises while conversions stay flat -> CPC rose OR CTR rose without conversion increase
  - Conversions fall while cost stays flat -> CR fell
  - Both
```

**Investigate in order:**

1. **Tracking** - did conversion volume collapse on a specific date? Check tag implementation and site changes.
2. **CPC** - did it rise? Auction Insights -> new competition? QS dropped?
3. **CR** - did it fall? Search Terms still relevant? Landing page changed? Form changed? Speed?
4. **Mix** - did an expensive campaign become a larger share? Did PMax scale?
5. **Seasonality** - compare against the same month last year.

### Symptom: "High CTR (8%) but very low conversion rate (1%)"

Diagnosis: **clickbait** or **ad-to-landing mismatch**.

**Actions:**
- Audit headlines: promising something the landing does not deliver?
- Search Terms: irrelevant queries clicking? Add negatives.
- Landing: message match with query/headline?
- Form: too long? Friction?

### Symptom: "Volume has been flat for 2 months, target is being hit"

Diagnosis: opportunity to **scale**.

**Actions in order:**
1. **Raise tCPA by 15%** or **cut tROAS by 10%** to create auction headroom.
2. **Check IS Lost (Budget)**; if >20%, raise budget first.
3. **Add broader match types**: phrase -> phrase + broad in discovery campaign.
4. **Add Search Themes** in existing PMax.
5. **Expand geos** if nearby geos have the same customer profile.
6. **Launch PMax** if not already present.

### Symptom: "Brand campaign CPA is $8 and Non-Brand CPA is $80"

That is normal. Brand is defense for people who already know you. But:

**Check:**
- Is Brand Abs Top IS >80%? If <60%, competitor is buying your name.
- Is Brand canibalizing organic? **Generally no** - the person who clicks the ad would often click organic if no ad existed. Test pausing for 2 weeks only if evidence is needed, and watch competitors.

### Symptom: "Ad Strength is Poor in all RSAs and I cannot improve it"

**Common causes:**
1. Keyword does not appear in headlines.
2. Headlines are repetitive.
3. Excessive pinning.
4. Lack of CTAs, benefits, and unique angles.

**Solution**: rebuild with 15 diverse headlines following the templates in `04-campaign-creation.md`.

---

## 4. Budget reallocation framework

### Principle

**Move budget from campaigns where `Actual CPA / Target CPA > 1.3` to campaigns where it is `< 0.8`**, but never increase a campaign by more than 30% at once because it can reset learning.

### Decision table

| Actual CPA / Target CPA | Conv. trend vs previous month | Action |
|---|---|---|
| < 0.8 | Stable or growing | Raise budget +20% |
| < 0.8 | Declining | Investigate saturation; keep for another 14d |
| 0.8-1.2 | Any | Maintain |
| 1.2-1.5 | Stable or growing | Tighten tCPA -10% before cutting budget |
| > 1.5 | Declining | Cut 30% or pause |

### Practical example

```text
Campaign A: budget $30/day, CPA $35 vs target $40, IS Lost (Budget) = 25% -> RAISE +20% = $36/day
Campaign B: budget $30/day, CPA $70 vs target $50, conversions falling -> CUT -30% = $21/day OR pause
Total: -$3/day, left for a new test or Display Remarketing
```

---

## 5. 2026 benchmarks for sanity checks

### Cross-industry Search medians

| Metric | 2026 median | YoY trend |
|---|---:|---:|
| CPC | $4.22 | +12% |
| CTR | 6.11% | +7% |
| Conv. Rate | 7.04% | -9% |
| CPA | $53.52 | +6% |

**2026 insight:** CPC rose more than CPA, meaning page-side conversion rate **absorbed** much of the CPC impact. Where the page did not keep up, CPA exploded. **Landing pages became the bottleneck.**

### By vertical, medians

| Vertical | CPC US$ | CTR | Conv Rate | CPA US$ |
|---|---:|---:|---:|---:|
| Local Services / Home Services | 3-8 | 5-8% | 8-15% | 30-80 |
| E-commerce | 0.80-3 | 2-6% | 1-4% | 25-80 |
| B2B SaaS | 3-8 | 3-6% | 2-6% | 80-250 |
| Legal | 6-15+ | 4-8% | 3-8% | 80-200+ |
| Health & Wellness | 1-4 | 5-10% | 5-12% | 30-100 |
| Automotive Service | 2-5 | 6-10% | 8-14% | 25-70 |
| Education | 2-5 | 4-7% | 3-8% | 50-150 |
| Real Estate | 1-4 | 5-8% | 3-7% | 50-150 |
| Finance/Insurance | 5-15 | 4-7% | 4-10% | 80-250 |

**Do not use these as targets**. Targets come from client economics. Use them as a **sanity check**: "my account is at $200 CPA in a vertical where median is $50 -> something is very wrong, or the client is a highly atypical case that must be justified."

### CTR by position in search

- Position 1 (Abs Top): 30-40% CTR in search with strong intent.
- Position 2: 12-18%.
- Position 3: 6-10%.
- Position 4+: 3-6%.

This decay justifies investment in Quality Score and extensions to move up.

---

## 6. Optimization anti-patterns

| Anti-pattern | Why it is bad | Do this |
|---|---|---|
| Changing tCPA every week | Resets learning, chaotic conversion trend | Change at most every 14 days |
| Pausing campaigns/keywords every week | Data does not accumulate; decisions are premature | Wait for 14 days of data |
| Negating 1 bad search term and ignoring n-grams | Infinite work, low impact | N-gram analysis every two weeks |
| Applying all Google Recommendations | Many are for Google, not for you | Evaluate ROI of each one |
| Ignoring Quality Score because "Smart Bidding handles it" | QS affects effective CPC, not just position | Attack QS<6 whenever possible |
| Comparing monthly CPA without mix adjustment | Mix changes are confused with efficiency changes | Decompose CPA by campaign first |
| Betting everything on PMax | Low visibility, loss of control | Search foundation + PMax as complement |
| "I will pause Brand to save budget" | Brand is defense; pausing lets competitor take the slot | Keep Brand always, optimize cost |
| Changing copy + landing + bid in the same experiment | Cannot isolate cause | 1 variable per test |
| No KPI dashboard | Reactive, not proactive decisions | Looker Studio / automated spreadsheet |

---

## 7. Signs the account needs restructuring, not only optimization

Incremental optimization cannot fix structural problems. Signs it is time to **restructure**:

- Multiple verticals/products in the same campaign set; Smart Bidding cannot learn distinct patterns.
- 90% of keywords in 2 ad groups; rebalance is urgent.
- Entire account on Manual CPC; underusing AI.
- No value tracking; stuck on tCPA when tROAS could be used.
- Pre-PMax campaign plus PMax canibalization.
- 30+ campaigns each spending under $5/day; consolidate.
- Sideways performance for 6+ months with no innovation.

---

## 8. Optimization plan template

Use this template when presenting a plan to the client.

```markdown
# Optimization Plan - [Account] - [Month]

## Diagnosis
- Spend: $X. Conv: Y. CPA: $Z (target: $W).
- 3 main symptoms:
  1. [symptom with quantified $ impact]
  2. [...]
  3. [...]

## Plan (4 waves)

### Wave 1 - This week (immediate impact)
- [ ] Negative [N] identified terms (estimated waste: $X/month)
- [ ] Pause keyword(s) with 0 conv and > $Y spend
- [ ] RSA refresh in [ad group X] (Ad Strength: Poor -> Good)

### Wave 2 - Next 2 weeks (structural fixes)
- [ ] Restructure ad group X by splitting into 2
- [ ] Raise campaign Y tCPA from $A to $B with gradual ramp
- [ ] Add Customer Match to exclude existing customers

### Wave 3 - Next 4 weeks (tests and expansion)
- [ ] Launch experiment: [hypothesis H]
- [ ] Add campaign for [new vertical/audience]
- [ ] N-gram analysis + negative batch

### Wave 4 - Next 60 days (strategic)
- [ ] Migrate to tROAS after implementing conversion value
- [ ] Implement OCI to qualify downstream leads
- [ ] Enable AI Max in existing campaigns after validation

## Expected results
- Q+30d: CPA falls from $Z to $Z' (-X%), volume stable or +Y%.
- Q+60d: test lift from tROAS / lead quality.
- Q+90d: cleaner structure, foundation for scaling.
```

---

## 9. Sources (2026 research)

- [Quality Score 2026 - Optmyzr](https://www.optmyzr.com/blog/google-ads-quality-score/)
- [Benchmarks 2026 - Digital Applied](https://www.digitalapplied.com/blog/google-ads-benchmarks-2026-cpc-ctr-cvr-industry)
- [Benchmarks by Industry 2026 - Foundry CRO](https://foundrycro.com/blog/google-ads-benchmarks-by-industry-2026/)
- [PPC Benchmarks 2026 - WebFX](https://www.webfx.com/blog/marketing/ppc-benchmarks-to-know/)
- [CRO Best Practices 2026 - Aimers](https://aimers.io/blog/conversion-rate-optimization-best-practices)
- [Landing Page Optimization 2026 - SaaS Hero](https://www.saashero.net/google-ppc/google-ads-landing-page-optimization/)
- [N-gram Wasted Spend - Taikun Digital](https://www.taikundigital.com/blog/remove-ppc-waste-n-gram-analysis/)
- [Google Ads Scripts 2026 - groas.ai](https://groas.ai/post/best-google-ads-scripts-2026-install-guide-automation-limits)
