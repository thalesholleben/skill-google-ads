# Claude Code + Codex Google Ads Skill

Advanced Google Ads management skill for Claude Code, Codex, and AI coding agents: strategy, Smart Bidding, AI Max, keyword research, auction analysis, A/B testing, campaign creation, continuous optimization, GAQL templates, and Python-based `.docx` reporting.

Built for 2026: decision-driven, not checklist-driven.

Public repo: https://github.com/thalesholleben/google-ads-manager

---

## Why this exists

Most Google Ads prompts produce generic PPC advice. This repository packages practical 2026 Google Ads operating knowledge into agent-readable Markdown files and local Python scripts, so an AI agent can load the right context before advising on accounts, campaigns, keywords, experiments, or reports.

Use it as a reusable skill for:

- Claude Code Google Ads strategy work
- Codex Google Ads analysis and automation support
- AI agent PPC audits, keyword research, and campaign planning
- Google Ads reporting workflows with `.docx` outputs

---

## What this skill does

This skill turns an AI coding agent into a senior Google Ads strategist. Instead of generic advice, it delivers:

- **Account diagnosis** - reads CSVs and identifies what is broken, why it happened, and what to fix first
- **Campaign creation** - structured plans, RSAs, negatives, extensions, and launch criteria
- **Smart Bidding guidance** - when to use tCPA, tROAS, Maximize Conversions, and how to avoid resetting learning
- **Keyword research** - intent mapping, match type decisions, and n-gram analysis of search terms
- **Auction Insights interpretation** - competitive pressure signals and recommended actions
- **A/B test design** - statistically valid experiment plans with clear success criteria
- **Monthly report generation** - two Python scripts that produce branded `.docx` reports

---

## Agent-friendly files

- `SKILL.md` - main entry point for Claude Code, Codex, and other agents
- `AGENTS.md` - portable coding-agent instructions
- `CLAUDE.md` - Claude Code bridge that imports `AGENTS.md`
- `.github/copilot-instructions.md` - GitHub Copilot repository instructions
- `references/*.md` - topic-specific Google Ads playbooks
- `scripts/*.py` - standalone Python templates for reporting and n-gram analysis
- `llms.txt` - compact map for LLMs and documentation crawlers

---

## How it works

```text
google-ads-manager/
├── SKILL.md                            # entry point - principles + workflows
├── AGENTS.md                           # portable agent instructions
├── CLAUDE.md                           # Claude Code bridge
├── llms.txt                            # compact repository map for LLMs
├── .github/
│   └── copilot-instructions.md         # GitHub Copilot instructions
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

`SKILL.md` is always loaded first. Reference files are loaded on demand. Scripts run locally and do not require Google Ads API credentials.

---

## Quick start

### Install as a Claude Code skill

```bash
git clone https://github.com/thalesholleben/google-ads-manager ~/.claude/skills/google-ads-manager
```

Then use it in Claude Code:

```text
/google-ads-manager
```

Or reference it in any conversation. Claude should load the skill automatically when you ask about Google Ads strategy, campaigns, keywords, or reporting.

### Install as a Codex skill

```bash
git clone https://github.com/thalesholleben/google-ads-manager ~/.codex/skills/google-ads-manager
```

Then ask Codex for Google Ads strategy, account diagnosis, campaign creation, keyword research, or reporting. The agent should start from `SKILL.md` and load only the relevant reference files.

### Run the report scripts

```bash
pip install python-docx pandas
python scripts/build_report.py
python scripts/build_report_cliente.py
```

Edit the data sections inside each script before running. They contain a worked example with fictional data, not real account numbers.

### Run the n-gram analysis

```bash
python scripts/n_gram_analysis.py search_terms.csv
python scripts/n_gram_analysis.py search_terms.csv --min-cost 10 --out my_report.csv
```

Export source data from Google Ads: Keywords -> Search terms -> Download CSV.

---

## 2026 core principles

Eight principles shape every recommendation this skill makes:

1. **Intent-based, not keyword-based** - negatives are now the primary control mechanism.
2. **Smart Bidding needs fuel** - tCPA needs 30+ conversions in 30 days; avoid frequent target changes.
3. **Manual bid adjustments are mostly ignored** - Smart Bidding already prices most signals internally.
4. **Quality Score is real money** - improving QS can materially reduce effective CPC.
5. **Tracking is the foundation** - DDA and Enhanced Conversions matter before bidding tweaks.
6. **PMax and AI Max need guardrails** - search themes, negatives, and placement exclusions are mandatory controls.
7. **Match types changed roles** - Exact for proven terms, Phrase for growth, Broad only with mature data.
8. **STAG beats SKAG for most accounts** - group by intent theme, not one keyword per ad group.

---

## Security and privacy

- No Google Ads credentials, OAuth tokens, customer IDs, account IDs, or real client exports belong in this repository.
- Python report scripts contain fictional example data. Replace it locally before running, but do not commit real client numbers.
- Google Ads Script templates use placeholder emails such as `you@example.com`. Replace those only in private deployment copies.
- Generated reports and CSV exports should stay local. `.gitignore` blocks common report and data outputs.

---

## 2026 benchmarks

| Metric | 2026 median | Health signal |
|---|---:|---|
| Avg CPC | $4.22 | Varies by vertical; legal and finance are often much higher |
| CTR | 6.11% | Above 4% is usually healthy for search |
| Conversion rate | 7.04% | Landing page quality is often the bottleneck |
| Avg CPA | $53.52 | Must be judged against unit economics |

Use these as sanity checks, not universal targets. The real target comes from LTV, gross margin, close rate, and payback period.

---

## GitHub topics

Use these topics to make the repository easier to find:

```text
google-ads, ppc, sem, smart-bidding, ai-max, performance-max, keyword-research,
auction-insights, gaql, google-ads-scripts, marketing-automation, python, docx,
claude-code, codex, ai-agents
```

Suggested GitHub description:

```text
Claude Code and Codex skill for advanced Google Ads strategy, Smart Bidding, AI Max, keyword research, GAQL, and PPC reporting.
```

---

## Roadmap

- Add more vertical-specific negative keyword starters
- Add separate report templates for e-commerce and lead generation
- Add optional synthetic CSV fixtures for script demos
- Add Google Ads Script examples for anomaly alerts and budget pacing
- Publish docs through GitHub Pages with public `llms.txt`

---

## License

MIT - see [LICENSE](LICENSE).
