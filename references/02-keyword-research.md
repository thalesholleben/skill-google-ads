# 02: Keywords, match types and negatives

> Load to research keywords, choose match types, read search terms, run n-grams or decide on a negative. Cutting
> on performance goes through the gates in 08.

Sources: `g/NNNN` = `https://support.google.com/google-ads/answer/NNNN`, checked on October 1, 2026.

---

## 1. Intent before keywords

Google matches by meaning (section 3). The keyword no longer bounds the traffic on its own: negatives, the landing
page, the ad and the bid do. So research starts with **intent**, which decides campaign, ad group, page and message.

| Stage (lead gen and B2B) | How people search | Volume | Cost per lead |
|---|---|---|---|
| Problem | "track work orders across branches", "spreadsheet is not enough" | high | high, long path |
| Solution | "inventory management software", "field service scheduling app" | medium | medium |
| Vendor | "software development company", "plumbing contractor near me" | low to medium | medium to low |
| Brand | "[brand]", "[brand] pricing" | low | the lowest |

E-commerce: discovery ("running shoes for flat feet"), comparison ("model A vs model B"), purchase ("model A size
10"). One stage per ad group: an ad group that mixes stages gets generic ads and generic pages.

Two rules of thumb that hold across accounts:
- **High volume and high CPC are rarely the same term.** Audience terms have volume and low CPC; commercial terms
  have a few hundred searches and high CPC.
- **The exact pain may have no searches.** The process a buyer wants to fix can have under 10 searches a month,
  while "vendor" and "software for <process>" searches exist. Research what people type, not what they feel.

---

## 2. Keyword research

The Keyword Planner is available in the UI and through the API (`KeywordPlanIdeaService` and the forecast services):
`generateKeywordIdeas` (from seeds or a URL), `generateKeywordHistoricalMetrics` (a closed list with monthly
trend) and `generateKeywordForecastMetrics` (projected clicks and cost for a campaign that does not exist yet).

- **CPCs come in the currency of the account you query from**, not the country you measure. Reading a USD account's
  CPCs as another currency (or the reverse) breaks the budget plan by several times.
- Geo targeting of the research decides the number: measuring a city's geo returns who searches **inside** the
  city, even without the city name in the term. That is the right measure for local services.
- **Empty volume means "below the reported minimum", not zero.**

Other seeds: the client's and competitors' pages, real search terms from the account (section 5), questions that
reach sales or support. Third-party tools only if the client already pays for them.

Group by **(intent, theme)**: each pair becomes an ad group of 5 to 15 keywords (STAG). One-keyword ad groups
(SKAG) only for high-volume hero keywords, and never in low-volume accounts, where they fragment data that is
already short.

---

## 3. Match types (official definition)

| Type | Matches | Source |
|---|---|---|
| **Exact** `[keyword]` | searches with the same meaning or the same intent | `g/7478529` |
| **Phrase** `"keyword"` | searches that include the meaning of the keyword | `g/7478529` |
| **Broad** `keyword` | related searches, even without the direct meaning, using the page, assets and the other keywords of the ad group; it is the **default** | `g/7478529` |

- Priority when several keywords and campaigns could serve: a search **identical** to an exact keyword wins
  (including over PMax); identical phrase and broad share priority with an identical PMax search theme; then
  relevance and Ad Rank decide (`g/7478529`).
- Google calls Smart Bidding "critical" for broad match. **There is no official threshold** of monthly conversions
  for broad; "50 to 100 a month" is a market heuristic.
- Changing the match type does not change Quality Score (`g/6167118`).

Two lessons that decide match types:
- **Bad clicks that come in through a phrase keyword are fixed at the keyword**, not with category negatives: pause
  the phrase and add the exact version. When a handful of phrase keywords bring ideas and do-it-yourself traffic,
  dozens of category negatives barely move the mix, because each new query is different. **Pausing the plural
  without the singular does not fix it:** phrase matches the variant and the sibling inherits the traffic.
- **A phrase keyword with the name of a popular topic matches the topic's informational tail.** A phrase like
  "safety management system" can spend a large share of a small budget in a day on people studying the subject
  ("what is a safety management system", "safety management system pdf"). Process keywords whose topic is also a
  study subject (safety, privacy law, quality standards) start in exact.

Use by regime (heuristic, see 08):

| Regime | Match types |
|---|---|
| Low | phrase and exact; broad only paused or in a short test, with a stop rule written before (08, section 8) and a strong negative list; cutting on performance only through gate B (gate D does not apply) |
| Medium | phrase as the engine; exact for proven terms; broad in a separate ad group, with Smart Bidding |
| High | broad with Smart Bidding for discovery, phrase and exact for control |

---

## 4. Negatives

**How they work** (`g/2453972`):
- they do not match close variants, synonyms, singular or plural: "shoe" as a negative does not block "shoes";
- they handle capitalization and misspellings on their own;
- **accents count:** "cafe" and "café" are two different negatives; "&" and "and" too;
- broad and phrase only look at the first 16 words of the search; an exact negative blocks only the identical
  search;
- **broad** negatives block searches containing all the words, in any order; **phrase**, the sequence; **exact**,
  only the identical search;
- symbols: periods and "+" are ignored; "site:" and the OR operator are dropped; a word preceded by "-" is ignored
  ("dark -chocolate" works as "dark"); `, ! @ % ^ ( ) = { } ; ~ < > ? \ |` are rejected.

**Limits** (`g/6372658`, `g/11396330`): 10,000 negatives per campaign; 20 shared lists per account (and 20 per
manager account), with 5,000 keywords each; **1,000 account-level negatives**, which apply to Search, PMax,
Shopping, App, Smart and Local (not Demand Gen). Display and Video consider at most 1,000.

**Where each negative lives, and where to read it through the API:**

| Level | Use | API |
|---|---|---|
| Account | universal (jobs, salary, courses, when the offer is not that) | `shared_set` of type `ACCOUNT_LEVEL_NEGATIVE_KEYWORDS`, linked by `customer_negative_criterion.negative_keyword_list` (1 per account) |
| Shared list | reused across campaigns | `shared_set` `NEGATIVE_KEYWORDS` + `campaign_shared_set`; keywords in `shared_criterion` |
| Campaign | specific to the campaign | `campaign_criterion` with `negative = TRUE` |
| Ad group | keep one ad group from taking another's search | `ad_group_criterion` with `negative = TRUE` |

A negative simulation that only reads `campaign_criterion` underestimates what is already blocked: shared lists
often hold more negatives than the campaign itself.

**A one-word negative is broad and can silence buyers.** Common ways it happens:
- `free` as a phrase negative blocks "free estimate", "free quote" and "free consultation" for a service business;
- "spreadsheet" or "excel" block "software to replace our inventory spreadsheet";
- "contractor" (meant to keep job seekers out) blocks "general contractor near me";
- a software vendor's brand as a one-word negative blocks "system that integrates with <that brand>";
- a phrase with zero conversions in the last 90 days can still block terms that converted earlier: a "best way"
  negative looks like do-it-yourself traffic and can block lifetime converters that start with it.

Rule: a new negative is an **unambiguous combination, in phrase match**, and goes through `scripts/negatives.py`
before it is added, against:
- the account's search terms **for its whole life**, not just 90 days (lifetime query: 07, query 8b);
- the active positive keywords (an exact negative equal to a keyword is a conflict).

```bash
python scripts/negatives.py --terms lifetime_terms.json --keywords keywords.json --candidate '"best way"' --candidate wax
```

The script applies the official rules (accents, "&", 16 words in broad and phrase, exact with no extra word, no
close variants) and the negative operators (`-word` ignored, `OR` and `site:` dropped, periods and "+" ignored);
what has no documented rule (asterisk, other operators with ":") or what Google rejects is refused with exit 2,
never approved. It exits 1 when a candidate blocks a converted term or an active keyword. It does not decide
intent: that is gate A of 08. Brands the client installs or resells are not competitor negatives.

**Starter lists** (a starting point, always checked against the offer):

```yaml
universal:             # jobs and studies, when the offer is not that
  - "jobs"
  - "salary"
  - "careers"
  - "course"
  - "certification"
  - "pdf"
do_it_yourself:        # for hired services
  - "how to"
  - "diy"
  - "tutorial"
free_stuff:            # only when the offer is paid and the term does not match a good "free" (free estimate, free quote)
  - "free download"
  - "free template"
```

No loose `free`, `cheap` or `gratis` without the test above. For a new campaign with no search terms yet, test
the list against the ad group keywords and the Keyword Planner ideas before adding it.

---

## 5. Search terms report

- **It does not show everything.** Google hides terms searched by few people, for privacy (`g/2472708`). An agency
  study (2025, declared bias) measured 26.7% of spend hidden, from 12.6 to 73.3% by account. **Reconcile the
  visible part with the campaign total and state the coverage** before any intent percentage: a percentage of the
  visible part is not a percentage of the campaign.
- **Measure the intent mix by cost and clicks, not impressions.** Product or research searches that nobody clicks
  weigh heavily in impressions and cost nothing; a target like "30% of impressions with buyer intent" measures the
  wrong thing.
- **It lags the campaign**: today's terms show after today's clicks.
- **Which keyword triggered the term:** `segments.keyword.info.text` in `search_term_view`; the term's match type:
  `segments.search_term_match_type`. PMax and AI Max terms come from other resources (07, section 2).
- **Classify by whole word**, never by substring ("art" matches inside "smart watch").

---

## 6. N-grams and mining

`scripts/n_gram_analysis.py` splits each term into 1, 2 and 3 word grams and adds up what every term containing the
gram adds up:

```bash
python scripts/n_gram_analysis.py search_terms.csv --actions-per-click 2 --base-clicks 410 --base-conversions 9 --base-cost 2150
python scripts/n_gram_analysis.py search_terms.json --actions-per-click 1    # API JSON (search_term_view)
```

`--actions-per-click` is the k of 08, section 2. Without it (or `--click-cvr`), the guard says NO BASE. The
`--base-*` totals (campaign totals for the period) turn on coverage.

| Script suggestion | Meaning | What to do |
|---|---|---|
| `REVIEW INTENT` | zero conversions with clicks above the statistical minimum | read the gram's terms; add a negative only through gate A (intent) or pause the keyword through gate B |
| `LOW DATA` | zero conversions below the minimum | nothing on performance; gate A still applies |
| `PROMOTE?` | 3+ conversions and CPA up to 70% of the base CPA | candidate for its own exact or phrase keyword |
| `NO BASE` | unknown unit | do not cut on performance |

Careful with one-word grams: as a negative it blocks every future search with the word. If the word describes what
the client sells, investigate first. Frequency: weekly in active accounts, monthly in low-volume ones.

**Search term mining, in order:**
1. Promote: a term with 3+ conversions and a good CPA becomes an exact keyword in the right ad group.
2. Negate by intent (gate A), with the overblocking test.
3. Read the gaps: a term with impressions and no clicks is an ad problem; with clicks and no conversions, a page or
   intent problem.
4. Trend: a new term growing week over week may need its own ad group.

---

## 7. Competitors as keywords

Using another company's brand **as a keyword is not restricted, in any match type**; the trademark policy restricts
the **ad text**, after a complaint from the brand owner (`adspolicy/6118`). There is no penalty for exact match on a
competitor.

Buying a competitor's brand is worth it when you have a clear differentiator to show and a comparison page; against
a much stronger brand, it only makes both auctions more expensive. Keep the competitor's name out of the ad.

**A store or competitor name in the search terms is not wrong intent by definition.** People who look for a shop or
another provider sometimes hire the service you sell. Negate a name only with zero conversions over the term's
lifetime and when that company only sells what you do not; a competitor of the same service stays.

---

## 8. Common mistakes

| Mistake | Why it hurts | Fix |
|---|---|---|
| 200 keywords in an ad group | generic ads and pages | ad groups of 5 to 15 by intent and theme |
| Only bottom of funnel | the account depends on existing demand | a separate problem campaign with an educational page |
| Loose one-word negative | silences buyers | phrase combination, tested with `scripts/negatives.py` |
| Intent percentage over the visible part | half of the spend can be hidden | state the coverage |
| Cutting a term on "zero conversions" with few clicks | noise | gate B of 08 |
| Planner CPC read in the wrong currency | a budget plan off by several times | check the account currency |

---

## Sources

Google Ads Help (October 1, 2026): `g/7478529` match types and priority; `g/2453972` negative keywords, including
"Symbols in negative keywords"; `g/6372658` account limits; `g/11396330` account-level negatives; `g/6167118`
Quality Score; `g/2472708` search terms report; trademark policy (https://support.google.com/adspolicy/answer/6118).
API: shared sets (https://developers.google.com/google-ads/api/docs/targeting/shared-sets); Keyword Planner
(https://developers.google.com/google-ads/api/docs/keyword-planning/overview).
Third parties: hidden search terms (https://searchengineland.com/google-ads-hidden-search-terms-cost-advertisers-458306);
n-gram analysis (https://adalysis.com/blog/n-gram-analysis-the-secret-to-scalable-search-term-management-in-google-ads/).
