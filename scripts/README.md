# Scripts

Four tools and one test, in Python 3.10+ with the standard library only (nothing to install). They run from any
folder and leave no `__pycache__` in the repo. Offline test of everything: `python -B scripts/self_test.py`.

Common exit code: **2 is invalid input** (missing file, non-finite or negative number, paginated JSON, malformed
candidate), always with a message and never with a traceback. The other codes are in each section.

Inputs come from a Google Ads export (CSV, English or Portuguese UI) or from the Google Ads API as JSON
(`{"results": [...]}`, a list of rows or `searchStream` batches). A JSON that still has a `nextPageToken` is
refused: join every page first.

## `n_gram_analysis.py`: search term n-grams

Splits each term into 1, 2 and 3 word grams (accents stay, punctuation goes; `--strip-accents` merges spellings) and
adds up what every term containing the gram adds up.

```bash
python n_gram_analysis.py search_terms.csv
python n_gram_analysis.py search_terms.csv --min-cost 10 --out my_report.csv
python n_gram_analysis.py search_terms.csv --actions-per-click 2 --base-clicks 410 --base-conversions 9 --base-cost 2150
python n_gram_analysis.py search_terms.json --actions-per-click 1     # API JSON (search_term_view)
```

Without `--base-*`, only the visible part is known: the base comes from it and coverage is unknown. The export's
`Total: ...` rows are skipped, but a real term that starts with "total" stays. A value outside the export format
(text, `NaN`, a minus sign) or a row with fewer columns than the header exits with 2 and the line number.

| Suggestion | Meaning | Action |
|---|---|---|
| `REVIEW INTENT` | zero conversions with clicks ≥ the minimum for P(0) < 5% | read the terms; negatives only through the intent gate, pauses through gate B (references/08) |
| `LOW DATA` | zero conversions below the minimum | nothing on performance |
| `PROMOTE?` | 3+ conversions and CPA ≤ 70% of the base CPA | candidate for its own keyword |
| `NO BASE` | unknown unit (no `--actions-per-click` nor `--click-cvr`) | do not cut on performance |

No suggestion becomes a negative on its own. Output: UTF-8 CSV with BOM (`n, gram, queries, clicks, impr, cost,
conv, conv_value, ctr_pct, conv_per_click, cpc, cpa, roas, suggestion, reason`) and a summary (`--json` for JSON).

## `negatives.py`: what a negative would block

The overblocking test of the intent gate. It reads your search terms (ideally lifetime, see references/07 query 8b)
and, optionally, your active keywords (text, one per line, or API JSON of `ad_group_criterion`), and applies the
official negative keyword rules: accents and "&" count; broad and phrase only see the first 16 words; exact needs
the whole search identical; no close variants. Operators: `-word` is ignored ("dark -chocolate" works as "dark"),
`OR` and `site:` are dropped, periods and "+" are ignored; a period, "+", hyphen or apostrophe inside a word is
tested joined and split (it fails if either reading blocks). Asterisks, other operators with ":" and symbols Google
rejects exit with 2.

```bash
python negatives.py --terms lifetime_terms.json --keywords keywords.json --candidate '"best way"' --candidate '[wax]' --candidate repair
python negatives.py --terms search_terms.csv --candidates-file candidates.txt --json
```

| Verdict | Meaning | Exit |
|---|---|---|
| `BLOCKS CONVERSION` | blocks a term that converted, in the data given | 1 |
| `BLOCKS KEYWORD` | blocks an active positive keyword (a conflict) | 1 |
| `OK` | none of that in the data given; intent is still your call | 0 |

Any positive conversion credit protects a term (a fractional 0.004 counts). If no term in the data has
conversions, the output warns: check that the query selected `metrics.conversions` (the API omits zero metrics). A
single-word broad negative gets a warning. Terms hidden by the privacy threshold and misspellings (which Google
also blocks) are outside the test.

## `stats.py`: low-volume statistics

The unit is the **converted click** (the probability that one click produces at least one conversion). Since
Google counts actions, the default base is the conservative p = conversions / (clicks x k), with k = primary actions
counted "One". Without k or a p measured outside (`--click-cvr`), the answer is NO BASE (exit 3). Full explanation:
references/08-low-volume.md.

```bash
python stats.py base --conversions 33 --clicks 110 --actions-per-click 3     # p and minimum clicks
python stats.py zero --n 21 --click-cvr 0.02                                  # P(zero conversions) in 21 clicks
python stats.py clicks --conversions 33 --clicks 110 --actions-per-click 3 --risk 0.05
python stats.py poisson --events 5                                            # exact interval of a count
python stats.py cpa --cost 400 --conversions 5                                # CPA interval
python stats.py rate --successes 0 --trials 150                               # Wilson and rule of three
python stats.py compare --a 0/10 --b 4/10                                     # two-sided Fisher exact
```

Every subcommand accepts `--json` (infinity, such as the CPA upper bound with zero conversions, prints as `null`).
Exit 0 with an answer, 3 with NO BASE, 2 with invalid input.

## `budget.py`: spend limits, approved caps and budget windows

Official rule: up to 2x the budget on one day; on a change day, 2x the **highest** budget of the day; a month with a
constant budget since day 1 = daily x 30.4; when the budget changes, the monthly limit becomes spend so far + new
budget x days left (counting the change day) and stays fixed until the next change.

Each campaign declares its own history this month (`key=value`); without it the script refuses (exit 2) instead of
assuming 30.4:

| Situation | Campaign |
|---|---|
| changes now | `name=x,budget=30,new=36,spend=450` (+ `--days-left`) |
| constant since day 1 | `name=x,budget=30,history=constant` |
| changed earlier this month | `name=x,budget=10,spend_at_change=200,days_at_change=16` or `month_limit=360` |
| new | `name=x,budget=0,new=5,spend=0` |
| re-enabled | `name=x,budget=0,new=5,spend=120` (spend it already had this month) |
| already changed today | add `max_today=20` for the change-day limit |

```bash
python budget.py --days-left 16 --cap-day 60 --cap-month 1824 \
  --campaign name=search,budget=30,new=36,spend=450 --campaign name=brand,budget=30,new=21,spend=450
```

A shared budget counts as one campaign. Every `name` must be unique (use the campaign ID when names repeat). Exit 1
when the total goes over the cap (`EXCEEDS`).

**Budget window** (promotional credit, event budget): `--window-budget S --window-days N` gives the highest total
daily budget that stays under S over N days (counting the first and the last, in the account time zone), even if
Google spends 2x every day: S / (2 x N), rounded down to cents. That holds if no higher budget was chosen on the
first day. With `--campaign`, the script adds up the real exposure (first day at the highest budget of the day, the
others at 2x the new budget) and exits 1 when it goes over S. A window that starts today (`--window-start today`, the
default) needs `max_today=` on every campaign (the current budget, if it did not change today); `--window-start
tomorrow` does not. With `--cap-day` or `--cap-month`, window mode also checks the caps (it needs `--campaign` with the
month history): a cap that is given is never ignored.

```bash
python budget.py --window-budget 600 --window-days 10                                               # 30.00
python budget.py --window-budget 600 --window-days 10 --campaign name=s,budget=10,new=60,max_today=10   # EXCEEDS: up to 1,200
python budget.py --window-budget 600 --window-days 10 --campaign name=s,budget=90,new=30,max_today=90   # EXCEEDS: 720
```

## `self_test.py`

Tests every script against `assets/fixtures/` (English and Portuguese CSV exports, API JSON complete and paginated,
keyword lists), the refusal of invalid input with exit 2, and repo hygiene: compilation (bytecode outside the repo),
the SKILL.md description, paths cited in Markdown, no `__pycache__` or `.env`, no personal paths, and no em dash or
spaced hyphen used as punctuation. The CI runs it on Python 3.10 and 3.12.
