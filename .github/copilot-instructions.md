# GitHub Copilot Instructions

This is a Claude Code and Codex skill for advanced Google Ads management.

## What this repo contains

- `SKILL.md` - entry point with 2026 principles and workflow routing
- `AGENTS.md` - portable coding-agent instructions
- `CLAUDE.md` - Claude Code bridge
- `llms.txt` - compact repository map for LLMs
- `references/` - deep knowledge files on strategy, keywords, bidding, campaigns, testing, optimization, reporting
- `scripts/` - Python scripts for generating `.docx` reports and running n-gram analysis on search term CSVs

## How to work with this code

**Reference files** are Markdown knowledge documents. They do not import or depend on each other.

**Python scripts** use `python-docx` and `pandas`. They are standalone templates — no shared modules, no config files. Run with:
```bash
pip install python-docx pandas
python scripts/build_report.py
```

**No credentials** are stored in this repository. Google Ads Scripts in `07-reporting-and-gaql.md` use `EMAIL_RECIPIENT = "you@example.com"` as a placeholder - always replace before deploying.

Generated `.csv`, `.xlsx`, and `.docx` files should stay local because they can contain private account data.

## Key constraints

- Python scripts target Python 3.10+ (uses `list[str]` and `str | None` type hints)
- `python-docx` does not support all Word features - formatting is done via OxmlElement for borders and shading
- The fictional example client in the scripts is "Sunrise Floor Removal" - any occurrence of a real client name is a mistake and should be removed
