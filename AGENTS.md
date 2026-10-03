# AGENTS.md: Claude Code + Codex Google Ads Skill

Instructions for AI agents working with this repository.

---

## What this repository is

A Google Ads skill for Claude Code, Codex and other coding agents. It is **not a web app, API or runnable service**:
it is a skill package of Markdown knowledge files and small Python tools that an agent loads to do Google Ads work.

---

## Repository map

```
google-ads-manager/
├── SKILL.md                        # entry point, always read first
├── AGENTS.md                       # this file
├── CLAUDE.md                       # Claude Code bridge
├── README.md                       # public documentation
├── CHANGELOG.md                    # versions
├── LICENSE                         # MIT
├── CONTRIBUTING.md                 # contribution guidance
├── SECURITY.md                     # sensitive data policy
├── llms.txt                        # compact map for LLMs
├── agents/openai.yaml              # Codex interface metadata
├── .gitignore                      # blocks local exports, reports and secrets
├── .github/
│   ├── copilot-instructions.md     # GitHub Copilot instructions
│   └── workflows/test.yml          # CI: runs scripts/self_test.py
├── references/                     # topic playbooks (load on demand)
│   ├── 01-strategy.md
│   ├── 02-keyword-research.md
│   ├── 03-bidding-and-auction.md
│   ├── 04-campaign-creation.md
│   ├── 05-ab-testing.md
│   ├── 06-optimization-playbook.md
│   ├── 07-reporting-and-gaql.md
│   └── 08-low-volume.md
├── scripts/                        # standard-library Python tools
│   ├── n_gram_analysis.py
│   ├── negatives.py
│   ├── stats.py
│   ├── budget.py
│   ├── self_test.py
│   └── README.md
└── assets/fixtures/                # synthetic test inputs
```

---

## How to use this skill

1. **Start with `SKILL.md`**: ground rules, checks, volume regimes, platform facts and routing.
2. **Load reference files only when needed**: each one covers one topic.
3. **Scripts read data you already have** (CSV exports or Google Ads API JSON). They never call Google and never
   need credentials.

---

## Working on the repository

- Run `python -B scripts/self_test.py` before every commit; the CI runs the same on Python 3.10 and 3.12. Do not run
  `python -m py_compile` on its own: it writes `__pycache__` into the repo and the hygiene check fails (the self test
  already compiles every script with the bytecode outside the repo).
- Every platform claim cites a source with a date (`g/NNNN` means `support.google.com/google-ads/answer/NNNN`).
  Third-party numbers and heuristics are labeled as such.
- GAQL in the references must have run on the current API version; write its state next to it.
- Public text: no em dashes and no spaced hyphens used as punctuation (the self test checks it).

---

## Security rules for agents

- **Never store credentials here**: no Google Ads API keys, OAuth tokens, developer tokens, account IDs, customer
  IDs or client secrets.
- **Do not commit client exports or generated reports**: `.csv`, `.xlsx` and `.docx` outputs are ignored because they
  commonly contain private account data. Fixtures are synthetic and live only in `assets/fixtures/`.
- **Examples are fictional.** Do not replace them with real client data.

---

## What agents should NOT do

- Do not change platform facts without a current source and a date.
- Do not add hardcoded account IDs, customer IDs or API keys to any file.
- Do not add dependencies to the scripts: they stay standard library only.
