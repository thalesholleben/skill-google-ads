@AGENTS.md

## Claude Code

- This is a skill package, not a runnable service. The primary artifact is `SKILL.md`.
- When the user asks about Google Ads strategy, load `SKILL.md` first, then the relevant `references/` file.
- Scripts in `scripts/` are Python templates with fictional example data - offer to run them only when the user has replaced the data sections.
- No credentials, API keys, or real account data should ever be committed here.
- The public repository is intended to be discoverable as a Claude Code and Codex Google Ads skill.
