@AGENTS.md

## Claude Code

- This is a skill package, not a runnable service. The primary artifact is `SKILL.md`.
- When the user asks about Google Ads, load `SKILL.md` first, then only the relevant `references/` file.
- Scripts in `scripts/` read CSV exports or Google Ads API JSON the user already has; they need no credentials.
- Before committing, run `python -B scripts/self_test.py`.
- No credentials, API keys or real account data are ever committed here.
