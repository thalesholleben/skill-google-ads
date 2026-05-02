# AGENTS.md - Claude Code + Codex Google Ads Skill

Instructions for AI agents working with this repository.

---

## What this repository is

A Claude Code and Codex skill for advanced Google Ads management in 2026. It is **not a web app, API, or runnable service** - it is a skill package: structured knowledge files + Python scripts that an AI agent loads to perform Google Ads strategy work.

---

## Repository map

```
google-ads-manager/
├── SKILL.md                        # entry point - always read this first
├── AGENTS.md                       # this file
├── CLAUDE.md                       # Claude Code bridge
├── README.md                       # public documentation
├── LICENSE                         # MIT
├── CONTRIBUTING.md                  # contribution guidance
├── SECURITY.md                      # sensitive data policy
├── llms.txt                         # compact map for LLMs
├── .gitignore                       # blocks local exports/reports/secrets
├── .github/
│   └── copilot-instructions.md      # GitHub Copilot instructions
├── references/                     # deep knowledge files (load on demand)
│   ├── 01-strategy.md              # Smart Bidding, AI Max, attribution, audiences
│   ├── 02-keyword-research.md      # intent mapping, match types, n-gram, SQR mining
│   ├── 03-bidding-and-auction.md   # bidding strategies, Auction Insights
│   ├── 04-campaign-creation.md     # step-by-step setup, RSA, extensions, negatives
│   ├── 05-ab-testing.md            # experiments, significance, design
│   ├── 06-optimization-playbook.md # daily/weekly/monthly + diagnosis framework
│   └── 07-reporting-and-gaql.md    # GAQL queries + Google Ads Scripts templates
└── scripts/                        # standalone Python scripts
    ├── build_report.py             # internal monthly .docx report
    ├── build_report_cliente.py     # client-facing .docx report
    ├── n_gram_analysis.py          # n-gram analysis of search terms CSV
    └── README.md                   # how to run the scripts
```

---

## How to use this skill

1. **Always start with `SKILL.md`** — it is the lightweight entry point with principles, workflows, and routing logic.
2. **Load reference files only when needed** — each one covers a specific topic. Do not pre-load all of them.
3. **Scripts are templates** - `build_report.py` and `build_report_cliente.py` contain worked examples with fictional data. The user replaces the data sections with real account numbers before running.
4. **No credentials are stored here** - Google Ads API access, account IDs, and customer IDs are never part of this skill.

---

## Running the scripts

Requirements:
```bash
pip install python-docx pandas
```

```bash
python scripts/build_report.py             # → relatorio_interno.docx
python scripts/build_report_cliente.py     # → relatorio_cliente.docx
python scripts/n_gram_analysis.py input.csv
```

---

## Security rules for agents

- **Never store credentials here** - no Google Ads API keys, OAuth tokens, account IDs, customer IDs, or customer secrets belong in this repository.
- **Do not commit client exports or generated reports** - `.csv`, `.xlsx`, and `.docx` outputs are ignored because they commonly contain private account data.
- **Email placeholders in scripts** - `07-reporting-and-gaql.md` contains Google Ads Script templates with `EMAIL_RECIPIENT = "you@example.com"`. Always replace with the actual recipient before deploying.
- **Example data is fictional** - `build_report.py` and `build_report_cliente.py` use "Sunrise Floor Removal" as a fictional example client. Do not treat these numbers as real.

---

## What agents should NOT do

- Do not modify `SKILL.md` principles without understanding the 2026 Google Ads context they encode.
- Do not add hardcoded account IDs, customer IDs, or API keys to any file.
- Do not replace the fictional example data in scripts with real client data before confirming it is intentional.
