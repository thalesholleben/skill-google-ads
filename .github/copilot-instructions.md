# GitHub Copilot Instructions

This is a Google Ads skill for Claude Code, Codex and other AI coding agents.

## What this repo contains

- `SKILL.md`: entry point with ground rules, checks, volume regimes, platform facts and routing
- `AGENTS.md`: portable coding-agent instructions
- `CLAUDE.md`: Claude Code bridge
- `llms.txt`: compact repository map for LLMs
- `references/`: topic playbooks on strategy, keywords, bidding, campaigns, testing, optimization, reporting and low volume
- `scripts/`: standard-library Python tools for n-grams, negative keyword tests, statistics and budget limits
- `assets/fixtures/`: synthetic inputs for the tests

## How to work with this code

**Reference files** are Markdown documents. Every platform claim cites a source with a date; keep it that way.

**Python scripts** target Python 3.10+ and use only the standard library. They read CSV exports or Google Ads API
JSON and exit with 2 on invalid input, never with a traceback. Test everything with:

```bash
python -B scripts/self_test.py
```

Do not run `python -m py_compile` on its own: it writes `__pycache__` into the repo. The self test already compiles
every script with the bytecode outside the repo.

## Key constraints

- No credentials, customer IDs, account IDs or real client exports in the repository.
- Fixtures are synthetic and stay in `assets/fixtures/`.
- Public text has no em dashes and no spaced hyphens used as punctuation.
