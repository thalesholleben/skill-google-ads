# 05 - A/B Testing (Drafts & Experiments) in 2026

> Load this file when the user asks about testing, experiments, A/B tests, statistical significance, or comparisons of copy, bidding, or landing pages.

---

## 1. When to use Drafts & Experiments vs alternatives

### Drafts & Experiments in-platform

**Use when** you want to test:
- Bid strategy: Maximize Conversions vs tCPA, tCPA vs tROAS.
- Bid target: tCPA $40 vs $50.
- Structural ad copy changes.
- Landing page with a different final URL.
- Search theme inclusion in PMax.
- Match type changes at scale.
- Audience signals in PMax.

**Advantages:**
- Automatic statistical significance: Jackknife resampling, 95% confidence.
- Random traffic split, not biased by hour/day.
- Native attribution, same as Smart Bidding uses.
- No external tool required.

**Limitations:**
- Does not compare external revenue metrics without Google Analytics/CRM.
- Requires at least 3-8 weeks for reliable results.
- Does not work on every campaign type; PMax has its own mechanics.

### Alternatives

**For landing pages**: Google Optimize was discontinued. Use **VWO, Optimizely, AB Tasty, Convert**, or bridge through **GA4 BigQuery + custom test**.

**For PMax creative**: use Asset Reporting and manually remove/add assets; there is no formal creative experiment.

**For low-risk changes**: apply directly, monitor for 14 days, roll back if worse. Suitable for extension changes, adding negatives, and bid target adjustments under 20%.

---

## 2. How to run an experiment in Google Ads

### Step-by-step setup

#### 1. Create Draft
- Go to Campaigns -> Drafts & Experiments -> Drafts -> New.
- Select the base campaign, the control.
- Apply **one single change**, following the one-variable rule.

#### 2. Convert to Experiment
- Drafts -> Apply -> Run as experiment.
- Configure:
  - **Name**: descriptive, for example "Test_tCPA_50_vs_60_2026Q2".
  - **Dates**: start date + end date. Minimum 3 weeks, ideal 6 weeks.
  - **Traffic split**: default 50/50. Risky test: 30 variation / 70 control.
  - **Search-based vs Cookie-based split**: cookie-based is default and cleaner.

#### 3. Goal metric

Define **the primary metric** that decides the test:
- Lead gen: **Cost per conversion**.
- E-commerce with value: **ROAS** or **conversion value**.
- Awareness: **CTR** or **CPM**.

### Minimum sample size rule of thumb

To detect a difference with 95% confidence:

| Relative lift to detect | Conversions needed per variant |
|---|---:|
| 50% | ~100 |
| 30% | ~250 |
| 20% | ~400 |
| 10% | ~1,500 |

If the campaign produces 100 conversions/month total, you can detect about a 30% lift in about 5 weeks: 250 / 50 = 5 weeks.

### Minimum duration

- **Minimum**: 3 weeks, covering weekly variation.
- **Recommended**: 4-6 weeks, covering biweekly seasonal events.
- **For tROAS / value**: 6-8 weeks because variance is higher.

**Do not stop early** even if one side is "winning". Random variation can reverse.

---

## 3. What to test, prioritized by impact

### Tier 1 - High impact, low effort
1. **Radical ad copy**: new RSA with a different angle.
2. **Landing page with strong message match vs generic**.
3. **Add Enhanced Conversions**: apply change and measure attributed conversion lift.
4. **tCPA +20% to unlock volume** in a campaign capped by target.

### Tier 2 - High impact, medium effort
5. **Bid strategy change**: Max Conv -> tCPA.
6. **Match type expansion**: add broad to exact-only campaign.
7. **Geo campaign split**: 1 campaign -> 2 with different targets.
8. **PMax + new audience signals**.

### Tier 3 - Validation
9. **Pinning vs no pinning**.
10. **Search Partners ON vs OFF**.
11. **More sitelinks: 6 vs 8**.
12. **Long descriptions vs short descriptions**.

### Tier 4 - Low impact, avoid testing
13. Button color.
14. Word-level headline changes.
15. Fine-tuned schedule in tCPA campaign, because it is ignored.

---

## 4. Anatomy of a well-designed test

### Clear hypothesis

Bad: "I want to test new copy."

Good: "Hypothesis: replacing 'Save Time' with 'Save 10+ Hours/Week' in 3 headlines will increase CTR by at least 10% in 4 weeks. Rationale: specificity increases credibility."

### Primary metric + guardrails

**Primary**: CTR.

**Guardrails** that cannot significantly worsen:
- Conversion rate: tolerance >= -5%.
- CPA: tolerance <= +10%.
- Average Quality Score: should not fall.

If the primary metric improves but a guardrail breaks, **reject the test**.

### Pre-registered decision criteria

Before starting, write:

```text
Winner if:
  - Primary metric difference > X with p < 0.05
  - All guardrails within tolerance

Inconclusive if:
  - p > 0.05
  - Sample size < 250 conv/variant

Rollback if:
  - Guardrail breaks
  - p < 0.05 but in the opposite direction of the hypothesis
```

### Single-variable rule

**Change ONE thing per experiment.** Multi-variate testing is tempting but:
- Confuses causality.
- Multiplies required sample size.
- In Google Ads, it is simply not supported by Drafts & Experiments.

Exception: mutually exclusive creative tests, such as 4 new RSAs in rotation, are not "1 change" technically, but creative testing naturally compares assets against each other.

---

## 5. Classic Google Ads A/B testing errors

### 1. "I paused after 1 week because it was obvious A was better"

Random variation can create a 30% gap in 7 days and erase it in 21 days. **Always complete the planned duration.**

### 2. "I changed the copy DURING the experiment"

This breaks the test. If you need to change something, such as a typo, pause the experiment and restart with a fresh sample.

### 3. "I compared week over week without a formal experiment"

Seasonality, trend, and external events all interfere. You have no control. Week 1 is not the control for week 2; they are different scenarios under different conditions.

### 4. "I applied the change to all campaigns at once"

You no longer have a control. Test in **1 campaign first** with a formal experiment, then roll out.

### 5. "Statistical significance means I will gain 30%"

Significance confirms the difference is real, not that it will stay at 30% in scale. Observed lift in small tests tends to be **inflated** because of regression to the mean.

### 6. "The test was inconclusive, so I will apply the variant anyway"

If you planned to apply it regardless, **do not run the test**. If you ran it, respect the result: inconclusive = no evidence of improvement = keep status quo.

### 7. "I detected an outlier and removed it from the dataset"

Outliers in paid media are usually **real data**, such as 1 expensive customer closing. Removing them biases the analysis. Use robust metrics such as median if outliers are concerning.

---

## 6. Common practical cases

### Case 1: testing a new bid strategy

```text
Hypothesis: migrating from Maximize Conv to tCPA $50 will reduce CPA by 15% without losing more than 10% of volume.

Setup:
- Draft from existing campaign.
- Change bid strategy to tCPA $50.
- Convert to experiment, 50/50 split, 6 weeks.

Decision:
- CPA experiment / CPA control < 0.85 + p < 0.05 + Conv volume > 0.90 -> APPLY
- Other cases -> ROLLBACK
```

### Case 2: new RSA with different angle

```text
Hypothesis: RSA with benefit headlines + social proof vs current feature-focused copy will increase CTR by at least 10%.

Setup:
- Draft from campaign.
- Pause current RSAs, create new RSA.
- Convert to experiment, 50/50, 4 weeks.

Decision:
- CTR > 1.10 x control + Conv rate >= control x 0.95 -> APPLY
- CTR > 1.10 x control but Conv rate < 0.90 x control -> REJECT as clickbait
```

### Case 3: new landing page

```text
Hypothesis: new landing with a 3-field form vs 7-field form will increase form completion by at least 30%.

Setup:
- Instead of Drafts & Experiments, use VWO/Optimizely for server-side split.
- Keep Google Ads Final URL unchanged; split happens client/server-side.
- 4 weeks, 50/50.

Decision:
- Form completion +30% + downstream lead quality >= control -> APPLY
- Form completion +30% but quality fell -> ANALYZE; may be acceptable if volume compensates
```

### Case 4: Search Themes in PMax

```text
Hypothesis: adding 30 specific search themes to PMax will increase conversion volume by at least 15%.

Setup:
- Drafts & Experiments does NOT support PMax the same way.
- Use Campaign Mix Experiments beta 2026 for cross-campaign testing.
- Alternative: create 2 PMax campaigns, 1 with themes and 1 without, allocate equal budget.
- Minimum 6 weeks.

Decision:
- Volume > 1.15 x control + CPA within 1.10 x control -> APPLY themes
```

---

## 7. Essential statistical concepts without jargon

### Significance level (p-value)

P-value = probability of observing a difference this large **if both variants were actually equal**.

- p < 0.05: 95% confidence that the difference is real.
- p < 0.01: 99% confidence.
- p > 0.05: insufficient evidence; do not reject the null hypothesis.

### Confidence interval

Instead of "lift of +12%", report "+12% +/- 4% with 95% confidence".

If the interval crosses 0, for example -2% to +18%, the test is **inconclusive** even if nominal p < 0.05.

### Power

Probability of detecting a real difference if it exists. Low power under 80% means that **even if the test is not significant, there may be a real difference you failed to detect**.

For 80% power, 5% significance:
- 50% lift -> 100 conv/variant.
- 30% lift -> 250 conv/variant.
- 20% lift -> 400 conv/variant.
- 10% lift -> 1,500 conv/variant.
- 5% lift -> 6,000 conv/variant.

### Multiple testing problem

If you run 20 simultaneous tests and accept p < 0.05, **statistically** 1 can appear significant by chance. For multiple tests, use Bonferroni correction (p < 0.05 / n) or FDR (Benjamini-Hochberg).

In practice: if running 5+ tests in the same period, **raise the criterion to p < 0.01**.

---

## 8. Ready-to-use templates

### Experiment plan template

```markdown
# Experiment: [short name]

**Hypothesis:** [variation] will increase/decrease [metric] by [magnitude] in [period],
because [rationale].

**Primary metric:** [CPA / CTR / CVR / ROAS / etc]
**Guardrails:**
  - [metric 1] cannot drop by more than X%
  - [metric 2] cannot increase by more than Y%

**Setup:**
  - Base campaign: [name]
  - Change: [one-sentence description]
  - Traffic split: 50/50
  - Start: [date]
  - Minimum duration: [3-6 weeks]
  - Target sample size: >= X conv/variant

**Decision criteria:**
  - APPLY if: primary lift > Y%, p < 0.05, guardrails OK.
  - ROLLBACK if: primary falls significantly OR guardrail breaks.
  - INCONCLUSIVE if: p > 0.05 at end of period -> keep status quo.

**Expected learning:**
  - Regardless of result, we will learn [insight].
```

### Pre-launch testing checklist

- [ ] Hypothesis written with expected magnitude.
- [ ] Primary metric + guardrails defined.
- [ ] Minimum sample size checked against conversion history.
- [ ] Planned duration, minimum 3 weeks.
- [ ] Only ONE variable changing.
- [ ] Decision criteria pre-registered.
- [ ] Calendar has no major seasonal event during the test, such as Black Friday.
- [ ] Stakeholder informed: "I will not read results before [date X]."

---

## 9. Sources (2026 research)

- [Statistical methodology of experiments - Google Ads Help](https://support.google.com/google-ads/answer/9232676)
- [Google Ads Experimentation Tips 2026 - Growthspree](https://www.growthspreeofficial.com/blogs/best-tricks-and-tips-for-google-ads-experimentation-in-2026)
- [A/B Testing in Google Ads 2026 - site2b.ua](https://www.site2b.ua/en/web-blog-en/a-b-tests-in-google-ads-how-to-run-them-correctly-in-2026.html)
- [Google Ads Experiments B2B SaaS - Growthspree](https://www.growthspreeofficial.com/blogs/google-ads-experiments-b2b-saas-statistical-significance-methodology)
- [Experiment Center 2026 Guide - ALM Corp](https://almcorp.com/blog/google-ads-experiment-center-guide/)
- [Campaign Mix Experiments Beta - ALM Corp](https://almcorp.com/blog/google-ads-campaign-mix-experiments-complete-guide/)
- [Drafts Explained - Digital Marketing Knight](https://www.digitalmarketingknight.com/google-ads-draft-campaigns-explained/)
- [Ultimate Guide A/B Testing - AdNabu](https://blog.adnabu.com/google-ads/google-ads-ab-testing/)
