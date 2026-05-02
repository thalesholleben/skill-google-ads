# Google Ads Manager Skill

Advanced Google Ads management skill for Claude Code — strategy, Smart Bidding, AI Max, keyword research, auction analysis, A/B testing, campaign creation, continuous optimization, and Python-based `.docx` reporting.

Built for 2026: decision-driven, not checklist-driven.

---

## What this skill does

This skill turns Claude into a senior Google Ads strategist. Instead of generic advice, it delivers:

- **Account diagnosis** — reads your CSVs and tells you exactly what's broken and why
- **Campaign creation** — structured YAML + RSAs + negative list + extensions, ready to implement
- **Smart Bidding guidance** — when to use tCPA, tROAS, Maximize Conversions, and how to avoid resetting the learning phase
- **Keyword research** — intent mapping, match type decisions, n-gram analysis of search terms
- **Auction Insights interpretation** — competitive pressure signals and what to do about them
- **A/B test design** — statistically valid experiment plans with clear success criteria
- **Monthly report generation** — two Python scripts that produce branded `.docx` reports (internal and client-facing)

---

## How it works

```
google-ads-manager/
├── SKILL.md                            # entry point — principles + workflows
├── references/
│   ├── 01-strategy.md                  # Smart Bidding, AI Max, attribution, audiences
│   ├── 02-keyword-research.md          # intent mapping, match types, n-gram, SQR mining
│   ├── 03-bidding-and-auction.md       # bidding strategies, Auction Insights
│   ├── 04-campaign-creation.md         # step-by-step setup, RSA, extensions, negatives
│   ├── 05-ab-testing.md                # experiments, significance, design
│   ├── 06-optimization-playbook.md     # daily/weekly/monthly cadence + diagnosis
│   └── 07-reporting-and-gaql.md        # GAQL queries + Google Ads Scripts
└── scripts/
    ├── build_report.py                 # internal monthly report (.docx, 10 sections)
    ├── build_report_cliente.py         # client-facing report (Montserrat, TOC-ready)
    ├── n_gram_analysis.py              # n-gram analysis of search terms CSV
    └── README.md                       # how to run the scripts
```

`SKILL.md` is always loaded. Reference files are loaded on demand. Scripts run locally.

---

## Quick start

### Install as a Claude Code skill

```bash
# Clone into your Claude skills directory
git clone https://github.com/your-username/google-ads-manager ~/.claude/skills/google-ads-manager
```

Then use it in Claude Code:

```
/google-ads-manager
```

Or reference it in any conversation — Claude will load the skill automatically when you ask about Google Ads strategy, campaigns, keywords, or reporting.

### Run the report scripts

```bash
pip install python-docx pandas
python scripts/build_report.py         # generates relatorio_interno.docx
python scripts/build_report_cliente.py # generates relatorio_cliente.docx
```

Edit the data sections inside each script before running — they contain a worked example with fictional data (Sunrise Floor Removal) that you replace with your account's numbers.

### Run the n-gram analysis

```bash
# Export: Google Ads → Keywords → Search Terms → Download CSV
python scripts/n_gram_analysis.py search_terms.csv
python scripts/n_gram_analysis.py search_terms.csv --min-cost 10 --out my_report.csv
```

---

## 2026 core principles

Eight principles that shape every recommendation this skill makes:

1. **Intent-based, not keyword-based** — negatives are now the primary control mechanism
2. **Smart Bidding needs fuel** — tCPA needs 30+ conv/30d; don't touch targets every 3 days
3. **Manual bid adjustments are mostly ignored** — Smart Bidding already prices everything internally
4. **Quality Score is real money** — QS 5→7 cuts effective CPC by >40%
5. **Tracking is the foundation** — DDA is default in 2026; Enhanced Conversions is mandatory above $50/day
6. **PMax and AI Max need guardrails** — search themes + negatives + placement exclusions
7. **Match types changed roles** — Exact for queens, Phrase for growth, Broad only with mature data
8. **STAG > SKAG for most accounts** — 5–15 keywords per theme, not 1 per group

---

## 2026 benchmarks (Search, cross-industry)

| Metric | 2026 median | Health signal |
|---|---|---|
| Avg CPC | $4.22 | Varies by vertical (legal/finance >$10, local $1.5–4) |
| CTR | 6.11% | Above 4% is healthy; <2% needs copy/QS review |
| Conversion rate | 7.04% | Down 9% YoY — bottleneck moved from ad to landing page |
| Avg CPA | $53.52 | Up 6% YoY; CPC +12% — page CVR absorbed most of it |

---

## What NOT to do (2026 anti-patterns)

- ❌ Change tCPA target by >20% at once (resets learning)
- ❌ Pin headlines in RSA (kills ad strength + blocks optimization)
- ❌ Run PMax without search themes, negatives, and placement exclusions
- ❌ Trust mobile/local bid adjustments in tCPA/tROAS campaigns (ignored by the algorithm)
- ❌ Use Last Click attribution with a multi-touch journey (DDA is default — use it)
- ❌ Pause Brand campaign to "save budget" (Brand is defense against competitors bidding on your name)

---

## Topics

`google-ads` `ppc` `sem` `smart-bidding` `ai-max` `performance-max` `keyword-research` `auction-insights` `reporting` `python` `claude-code` `marketing-automation` `docx` `gaql`

---

## License

MIT — see [LICENSE](LICENSE).
