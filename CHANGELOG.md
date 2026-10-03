# Changelog

## 3.0.0 (2026-10-03)

A rewrite for October 2026. The skill is now in English end to end, every platform claim cites a Google page (or a
labeled third-party source) with a date, and the scripts are tested in CI.

### Changed

- `SKILL.md` rewritten: ground rules (read before concluding, account content is data not instructions, budget
  belongs to the owner, safe mutations), twelve checks before concluding, a volume regime table, platform facts as
  of October 2026, routing and expected outputs.
- References 01 to 07 rewritten. Corrections include: Target CPA starts without history (no "minimum of 50"); Target
  ROAS needs 15 conversions in 30 days; no "20% rule" for learning; the June 2026 rename of Target CPA and Target
  ROAS; the August 17, 2026 change for budget-limited campaigns; device adjustments change the tCPA target, other
  adjustments are not used and do not accept -100%; Quality Score is a diagnostic; Ad Strength gives +15%
  conversions, not CTR, and is not an auction input; DSA migrates to AI Max in February 2027, not September 2026;
  language targeting was removed from Search in September 2026; competitor brands as keywords are allowed in any
  match type; 2026 WordStream/LocaliQ benchmarks replace 2023 numbers; Google's budget limits in the month a budget
  changes.
- GAQL: only queries that ran on API v25 in October 2026. Removed queries that do not run (`FROM auction_insight`,
  `hourly_metrics_view`, `asset_view`, a geographic query with a field missing from SELECT).
- `scripts/n_gram_analysis.py` rewritten with the standard library (no pandas): English and Portuguese CSV exports,
  API JSON, accents preserved, conversion value and ROAS, coverage against campaign totals, and a statistical guard
  (`REVIEW INTENT`, `LOW DATA`, `PROMOTE?`, `NO BASE`) instead of automatic `NEGATIVE` suggestions. The old command
  line still works (`input.csv`, `--min-cost`, `--out`); **the output columns changed** (`n, gram, queries, clicks,
  impr, cost, conv, conv_value, ctr_pct, conv_per_click, cpc, cpa, roas, suggestion, reason`).

### Added

- `references/08-low-volume.md`: the converted-click unit, pocket math, cut gates, maturity and seasonality,
  bidding and testing with low volume, rules written before launch, lead quality.
- `scripts/negatives.py`: an overblocking test for negative keywords by the official matching rules, including
  accents, "&", the 16-word limit and negative operators.
- `scripts/stats.py`: P(0), minimum clicks, exact Poisson intervals, CPA intervals, Wilson and rule of three,
  Fisher exact.
- `scripts/budget.py`: monthly spend limits, approved caps and budget windows (credit or event budgets).
- `scripts/self_test.py`, synthetic fixtures in `assets/fixtures/`, and a GitHub Actions workflow running the test
  on Python 3.10 and 3.12.
- `agents/openai.yaml` for Codex.

### Removed

- `scripts/build_report.py` and `scripts/build_report_cliente.py`: hardcoded example content in Portuguese with
  `python-docx`. A client report structure and checklist now live in `references/07-reporting-and-gaql.md`, section 4.
- The Google Ads Scripts JavaScript snippets (pacing, anomaly, broken URL) from reference 07: the pacing script only
  covered Search and Display campaigns and the anomaly script used a placeholder CPA for days without conversions.
- Frontmatter keys that went stale (`models`, `capabilities`, `languages`, `department`).

## 2.0.0 (2026-05-02)

Public release: strategy, keyword research, bidding, campaign creation, A/B testing, optimization and GAQL
references, n-gram analysis and `.docx` report templates.
