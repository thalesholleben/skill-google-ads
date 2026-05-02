# 02 - Keyword Research and Match Types in 2026

> Load this file when the user asks for keyword research, intent mapping, match type decisions, search term analysis, or advanced negative keywords.

---

## 1. Core principle - Google Ads runs on INTENT, not words

In 2026, all match types operate through **intent matching**:

- **Exact** match: covers the exact query plus variants with the same meaning, including synonyms, reordered words, and implied terms.
- **Phrase** match: covers paraphrases that carry the same meaning as the phrase, even with words before/after or slightly different order.
- **Broad** match: uses the keyword as a starting point plus landing page, ad copy, and Smart Bidding signals to find relevant queries - sometimes far from the literal term.

**Practical implication:** keywords no longer strictly define traffic. **Negatives + Smart Bidding + landing page define traffic boundaries.**

---

## 2. Intent Mapping - the framework

Before listing keywords, map **journey stages**. This defines:
- Which campaign each keyword belongs to.
- Which landing page.
- Which bid and message.

### The 4 stages for B2B / lead gen

| Stage | How the user searches | Volume | Expected CPA |
|---|---|---|---|
| **Problem-aware** | "how to motivate remote team", "productivity dropping" | High | High: long path to conversion |
| **Solution-aware** | "project management tool", "PM software" | Medium-high | Medium |
| **Product-aware** | "Asana vs Monday", "best Kanban tool 2026" | Medium | Medium-low |
| **Brand-aware** | "[brand]", "[brand] login", "[brand] pricing" | Low, but converts | Very low |

### The 3 stages for e-commerce

| Stage | How the user searches | Match |
|---|---|---|
| **Discovery** | "best running shoes for flat feet" | Phrase + Broad |
| **Comparison** | "Nike Pegasus 41 vs Brooks Ghost 16" | Exact + Phrase |
| **Transactional** | "Nike Pegasus 41 size 10 buy" | Exact |

### Common mistake

Mixing stages in the same ad group -> one RSA tries to serve different intents -> relevance and CTR drop -> QS drops -> CPC rises.

**Rule**: 1 stage per ad group (STAG); align copy and landing page to that stage.

---

## 3. Keyword research process

### Step 1 - Seed list

Collect from 5 sources:

1. **Internal brainstorm**: 20-30 terms you would use.
2. **Client site**: extract titles, H2s, product lists.
3. **Competitor sites** (top 3): same extraction plus differentiators they highlight.
4. **Real search terms**: if an account has 30+ days of history, mine converting search terms.
5. **Customer service / sales**: what questions arrive? What pains do customers mention?

### Step 2 - Expand

- **Google Keyword Planner**: filter by monthly volume, competition, CPC range. Flag keywords with 100-10,000 volume as the sweet spot.
- **Search with `*` wildcard**: "best * software for [vertical]" generates ideas.
- **Google People Also Ask + autocomplete**: collect long-tail questions.
- **AnswerThePublic**: question-based queries.
- **Competitors through SEMrush/Ahrefs**: paid keywords they buy.
- **AI tools**: ask Claude/ChatGPT to generate 30 problem-aware keywords for X with estimated volume.

### Step 3 - Cluster by intent + theme

Use a spreadsheet. For each keyword:

| Column | Example |
|---|---|
| Keyword | "kanban software for small teams" |
| Volume | 1,200/month |
| Est. CPC | $4.50 |
| Intent | Solution-aware |
| Theme | Kanban |
| Suggested match | Phrase |
| Landing | /kanban-tool |

Group by **(Intent, Theme)** -> each group becomes an ad group.

### Step 4 - Decide match types by keyword

Use this logic, not a generic rule:

```text
IF keyword is brand -> Exact for defense
IF keyword has 30+ conversions with good CPA -> Exact to consolidate
IF medium volume + strong intent -> Phrase as growth engine
IF high volume + generic intent + mature Smart Bidding + budget -> Broad for discovery
IF low volume (< 50/month) + long tail -> Phrase or Broad in discovery campaign
```

### Step 5 - Negative seeds

Before launch, prepare obvious negatives:

```yaml
universal_negatives:
  - free, gratis, grátis, gratuit
  - download, torrent, crack, pdf
  - jobs, job, vagas, salary, salário
  - tutorial, courses, course, training, certification
  - DIY, "how to do" # context-dependent
  - reviews # if you do not want comparison traffic
  - meaning, definition, what is # top of funnel without intent
  - reddit, quora, forum # opinion-seeking, not buying
  - alternatives # negative if you are the leader; positive if challenger

ecommerce_specific:
  - used, segunda mão, refurbished
  - cheap, barato # unless this is your positioning
  - vs # unless this is a comparison campaign

b2b_specific:
  - student, estudante
  - personal use, individual
  - open source, free trial only

local_services_specific:
  - DIY, tutorial, video, youtube
  - rental, locação # if you sell/service, not rent
  - course, certification
```

---

## 4. Match Types - advanced 2026 manual

### Exact Match `[keyword]`

**When to use:**
- Proven queen keywords: 10+ conversions with good CPA.
- Brand defense: `[brand]`, `[brand login]`.
- Very high-volume + high-CPC cases where a ceiling is required.

**Risk:** even exact catches close variants. Monitor search terms weekly for bad variants.

### Phrase Match `"keyword"`

**When to use:**
- Main growth engine for most accounts.
- Medium volume + reasonably clear intent.
- When there is not enough data to promote to exact.

**2026 best practice:**
- Pair phrase + Smart Bidding (tCPA/tROAS) with 30-50 conversions in the campaign.
- Use multiple phrase variations instead of one exact keyword.

### Broad Match `keyword`

**Strict prerequisites before enabling:**
- Solid tracking: Enhanced Conversions ON, primary conversions well defined.
- 50-100 conversions/month in the campaign.
- Mature Smart Bidding: tCPA/tROAS running for 30+ days.
- Ability to review search terms weekly; broad creates noise.
- Robust negative list: at least 50-100 initial negatives.

**Without these prerequisites**, broad becomes a budget drain. With them, broad becomes the account's largest discovery source.

### Quick decision table

| Scenario | Recommended match |
|---|---|
| New account, no data, lead gen | Phrase + Exact, 50/50 |
| New account, e-commerce with Shopping | Phrase + Broad after 30d with Shopping active |
| Mature account, 100+ conv/month, stable tCPA | Phrase as main, exact queens, broad in separate discovery campaign |
| Brand campaign | Exact + Phrase for brand name and generic brand terms |
| Competitor campaign | Phrase on competitor name - NEVER exact |
| New product launch | Exact + Phrase, no Broad because Smart Bidding has no data yet |

---

## 5. N-gram analysis - systematic search term method

### What it is

Instead of reviewing search terms one by one, which is impossible at scale, break each query into **1-, 2-, and 3-word fragments** (1-grams, 2-grams, 3-grams) and aggregate metrics by fragment.

**Why:** "free" in "free download project management software" does not appear together with "best free PM tools". But the **token "free"** aggregates spend/conversions/CTR across **all** queries that contain it.

### How to run it

**Step 1**: export the Google Ads search terms report - 30-90 day window, all account search terms. Save as CSV.

**Step 2**: run `scripts/n_gram_analysis.py` included in this skill. Output:
- 1-gram table sorted by spend, with Conv, CPA, CTR.
- 2-gram table.
- 3-gram table.

**Step 3**: identify n-grams with **high spend and zero conversions** -> negative candidates.

**Step 4**: identify n-grams with **high CTR and great CPA** -> candidates to promote to exact match in a dedicated ad group.

### Decision heuristics

| Pattern | Action |
|---|---|
| 1-gram with >$50 spend and 0 conv | Add as negative if not vital |
| 1-gram with CPA 3x above average | Investigate; likely negative |
| 2-gram with 5+ conv and CPA below average | Promote to exact in focused ad group |
| 3-gram with 10+ distinct searches and good CTR | Promote to exact keyword: proven high intent |

### Recommended cadence

- Small accounts (< $1k/month): monthly.
- Mid-size accounts ($1-10k/month): every two weeks.
- Large accounts (> $10k/month): weekly.

### Limits and cautions

- N-grams ignore **context**: "free shipping" vs "free download". Always review top hits manually before adding a negative.
- 1-grams are powerful but dangerous - a one-word negative can block much more than expected. Use phrase or exact match on negatives to limit impact, for example negative phrase `"free trial"` only blocks terms where the words appear together.

---

## 6. Negative Keywords - advanced 2026 strategy

### Main 2026 changes

- **Expanded limit** (Mar/2026): **10,000 keywords per campaign** and **10,000 per ad group** (previously 5,000).
- **Account-Level Placement Exclusions** (Jan/2026): block sites/apps/YouTube channels across **all campaign types**, including PMax and Demand Gen, from a centralized list. Use this to fight MFA (Made-for-Advertising) and mobile game spam.
- **Account-level negatives** still apply to Search/Shopping; for PMax/Demand Gen, use Brand Lists, Negative Keyword Lists at account level now available for PMax, and placement exclusions.

### Negative hierarchy

```text
Account level         -> universal: free, jobs, salary, etc.
  |
Negative Keyword List -> reusable, shared across campaigns
  |
Campaign level        -> campaign-type specific
  |
Ad Group level        -> cross-pollination between groups
```

### Lists every account should have

1. **Universal Negatives** at account level: jobs, salary, free, download, torrent, crack, pdf, tutorial, course, certification, reddit, forum, what is, meaning, definition.
2. **Brand Defense** at account level: competitor brands you do NOT want to buy, and the inverse when protecting your brand.
3. **Cross-Pollination List** at ad group level: prevents ad group A keywords from capturing ad group B queries.
4. **Vertical-Specific Negatives**: industry terms that signal non-buying intent, such as legal "lawyer near me free" if you are a paid firm, or healthcare "home remedy" if you sell medication.

### N-gram-driven negatives

After every n-gram analysis, generate a **batch of negatives** and add it **in bulk** through Google Ads Editor. It is faster than the UI one by one.

---

## 7. Search Query Report (SQR) Mining - workflow

Recommended workflow for efficient mining:

### 1. Promote top performers
- Search terms with **5+ conversions** and CPA below average -> add as **exact match** in a dedicated ad group.
- Search terms with **high CR + good CPA + volume** -> create a new ad group if one does not exist.

### 2. Negative bottom performers
- Spend > 3x target CPA with no conversion -> immediate negative.
- Spend > 10x target CPA with 0 conversions -> 100% negative, no debate.

### 3. Identify gaps
- Search terms with **high impression share** but **0 clicks** -> copy/relevance problem: the query matches, but the ad does not convince.
- Search terms with **clicks but 0 conversions** -> landing page problem or intent mismatch: the query promises something the landing page does not deliver.

### 4. Detect intent shifts
- A new query appears and gains volume month over month -> trend; may deserve a dedicated campaign.
- A historical query lost volume -> competitor strategy changed or demand fell; check Trends.

---

## 8. Keyword tools - when to use each

| Tool | Strong at | Cost |
|---|---|---|
| **Google Keyword Planner** | Official volume, CPC range, trend | Free with Ads account |
| **SEMrush** | Competitor paid keywords, share of voice | $130+/month |
| **Ahrefs** | SEO difficulty, content gap, organic share | $100+/month |
| **AnswerThePublic** | Question-based, long-tail | Free limited / $99/month |
| **Soovle / Ubersuggest** | Multi-source autocomplete | Free / $29/month |
| **Claude/ChatGPT** | Brainstorming, clustering, copy generation | API/subscription |

**Rule**: if the client already pays for SEMrush/Ahrefs, start there for competitor data. For a new or low-budget account, Keyword Planner + AI is enough to start.

---

## 9. Common keyword research mistakes and fixes

| Mistake | Why it is bad | Fix |
|---|---|---|
| Listing 200 keywords and putting them into 1 ad group | RSAs become generic, QS collapses | Cluster into 8-12 STAGs with 5-15 keywords |
| Only product-aware keywords, ignoring problem-aware | Loses top-of-funnel; account depends on existing demand | Create separate problem-aware campaign with educational landing |
| Not researching negatives before launch | First weeks burn hundreds of dollars | Initial list of 50-100 universal negatives |
| Trusting Keyword Planner volume 100% | Underestimates long-tail and groups close variants | Validate with real search terms after 30 days |
| Buying only competitor keywords and no brand | Competitor buys yours and you are exposed | Always run Brand defense |
| Random match type decisions | Inconsistency -> Smart Bidding cannot learn a pattern | Use the decision table in section 4 |

---

## 10. Sources (2026 research)

- [Match Types 2026 - Growth Minded Marketing](https://growthmindedmarketing.com/blog/keyword-match-types/)
- [Match Types 2026 - Stackmatix](https://www.stackmatix.com/blog/google-ads-keyword-match-types-guide)
- [Broad Match 2026 Playbook - ATTN Agency](https://www.attnagency.com/blog/google-ads-broad-match-strategy)
- [Negative Keywords 2026 - Optmyzr](https://www.optmyzr.com/blog/negative-keywords/)
- [N-gram Analysis Adalysis](https://adalysis.com/blog/n-gram-analysis-the-secret-to-scalable-search-term-management-in-google-ads/)
- [N-gram Layered - googleadsopenresearch](https://googleadsopenresearch.com/research/advanced-ngram-analysis/)
- [Account-Level Placement Exclusions - Karooya](https://www.karooya.com/blog/negative-keywords-in-google-ads-2026-are-you-using-them-to-filter-traffic-or-control-it/)
- [Keyword Research 2026 - SaaS Hero](https://www.saashero.net/google-ppc/google-ads-agency-keyword-research/)
- [Google Ads runs on intent - Search Engine Land](https://searchengineland.com/google-ads-intent-not-keywords-468271)
