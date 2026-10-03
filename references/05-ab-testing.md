# 05: Testing (experiments, sample size and what to do when volume does not close)

> Load to test bidding, targets, ad text, landing pages or structure, or to judge a test. In low-volume accounts,
> section 4 and reference 08 rule.

Sources: `g/NNNN` = `https://support.google.com/google-ads/answer/NNNN`, checked on October 1, 2026.

---

## 1. Google's tools

| Tool | For | Official detail |
|---|---|---|
| **Custom experiment** | bidding, targets, text, landing page, structure in Search, Display, Demand Gen and Video | the **cookie-based split is recommended**; the **search-based** split exists only in Search and can reach significance faster; a 50% split is recommended; up to 5 scheduled per campaign, 1 running at a time; **no Auction Insights and no search terms report** inside the experiment (`g/6261395`, `g/10683687`) |
| **Save as experiment** | you edited the campaign and want to test before applying | a button when saving the change (`g/6268632`, `g/10683687`) |
| **PMax experiments** | Uplift (adding PMax), Upgrade (Shopping, DSA or Display to PMax), Optimization (final URL expansion, assets) | `g/12997711` |
| **Campaign Mix Experiments** | comparing campaign mixes | **alpha** as of October 1, 2026; up to 5 arms, 95, 80 or 70% confidence, 6 to 8 weeks (`g/16009098`) |

**Google's method** (`g/9232676`): the split is applied before targeting; jackknife over 20 buckets per arm; a
two-sided test with a 95% interval. Officially, give the treatment arm **7 to 14 days** to stabilize (learning takes
about 7). "At least 3 weeks, ideally 4 to 8" is a heuristic to cover weekly cycles.

**Without an experiment:** a low-risk change (an asset, an intent negative) is applied directly, with the reading
rule written before (08, section 8). Landing page tests outside Google: the site's A/B tool or one arm per URL.

---

## 2. How much you need

Lehr's rule (two-sided alpha 5%, 80% power): visitors per arm ≈ 16 · p̄(1−p̄) / Δ², with Δ = the absolute rate
difference. In **conversions in the control arm** (with a CVR between 3 and 20%), that gives:

| Relative lift to detect | Conversions per arm (approx.) |
|---|---|
| 50% | 60 to 100 |
| 30% | 155 to 250 |
| 20% | 340 to 425 |
| 10% | 1,300 to 1,600 |
| 5% | 5,100 to 6,400 |

Calculators return **visitors** (clicks); conversions = clicks x CVR. With an 8% CVR, detecting +30% needs about
2,300 clicks per arm. A campaign with 100 conversions a month split 50/50 needs about 3 to 5 months to detect +30%.

---

## 3. Designing a test

- **A hypothesis with a size:** "changing X to Y raises [metric] by at least Z% in N weeks, because [reason]".
- **One variable per test.** Text, page and bid together do not tell you which one moved.
- **Primary metric plus guardrails:** the primary (for example, CPA); guardrails that cannot get worse beyond a
  limit (conversion rate, lead quality, spend).
- **Criteria written before:**
  - apply: a difference in the hypothesis direction with p < 0.05 and guardrails within limits;
  - inconclusive: p ≥ 0.05 at the end of the period, keep what was there;
  - roll back: a guardrail broke, or a significant difference in the opposite direction.
- **Calendar:** no big seasonal event in the middle; nobody peeks before the date.

---

## 4. Low volume

- Section 2 shows the size of the problem: an account with 30 to 45 conversions a month needs 2 to 5 months to
  detect +50%; accounts with a handful of conversions cannot close any test.
- **Ad rotation does not split people at random.** Two RSAs in the same ad group are not an A/B test; the reading is
  directional, never "proven".
- What to do: test only **big changes** (offer, page, audience), judged by the interval (08, section 3), and **write
  the rules before** (08, section 8). Upper-funnel indicators (CTR, cost per landing page visit, form start rate)
  help decide text and page when conversions do not close.
- Comparing two rates with a small sample: **Fisher's exact test** (`scripts/stats.py compare`), never a z test.

---

## 5. Essential statistics

- **p-value:** the chance of seeing a difference this large if the variants were equal. p < 0.05 does not mean the
  gain at scale will be the observed one: small-test lifts tend to be inflated.
- **Interval and p from the same model are dual:** a 95% interval that crosses zero implies p > 0.05. If they
  disagree, they came from different methods (for example, an interval of the relative lift and a test of the
  difference); report both from the same method.
- **Low power:** a test that did not reach significance with power below 80% does not prove there is no effect.
- **Many tests at once:** with 20 tests at p < 0.05, one is "significant" by chance; with 5 or more in the period,
  require p < 0.01 (or Bonferroni or Benjamini-Hochberg).
- **Outliers are usually real data** (an expensive customer closed). Removing them biases; use the median if worried.

---

## 6. Classic mistakes

1. Stopping before the date because one side "is winning".
2. Changing the test midway (text, target, budget): it restarts.
3. Comparing week with week without an experiment: both ran under different conditions.
4. Applying to every campaign at once: the control disappears.
5. Applying the "inconclusive" anyway: if you were going to apply it regardless, you did not need to test.

---

## 7. Test plan template

```markdown
# Test: <short name>
Hypothesis: <variation> changes <metric> by <size> in <period>, because <reason>.
Primary metric: <CPA, CTR, form rate...>   Guardrails: <metric: limit>
Base campaign: <name and id>   Change: <one sentence>   Split: 50/50, cookie-based
Start: <date>   Minimum duration: <days>   Target sample: <conversions per arm, from section 2>
Decision: apply if <...>; inconclusive if <...>; roll back if <...>
Rollback: <how to undo>
Expected learning, whatever the result: <...>
```

---

## Sources

Google Ads Help (October 1, 2026): `g/6261395` custom experiments; `g/10683687` about experiments; `g/9232676`
statistical methodology; `g/12997711` PMax experiments; `g/16009098` Campaign Mix Experiments; `g/6268632` Target
CPA (Save as experiment).
Statistics: van Belle, *Statistical Rules of Thumb*, chapter 2 (http://www.vanbelle.org/chapters/webchapter2.pdf);
interval and p duality (https://pmc.ncbi.nlm.nih.gov/articles/PMC4877414/).
