# Contributing

Thanks for improving this Google Ads skill. This repository is a knowledge package plus a few standalone Python tools, not a web app or service.

## Good contributions

- Correct or update a platform fact, with the Google page (or labeled third-party source) and the date you checked it.
- Add or refine reference material in `references/`, one topic per file.
- Improve the scripts without adding dependencies: they stay standard library only (Python 3.10+).
- Add synthetic fixtures that make a test or an example clearer.
- Improve installation, security or agent instructions.

## Before opening a pull request

1. Read `SKILL.md` first.
2. Do not commit credentials, real customer IDs, account IDs, OAuth tokens or real client exports. Fixtures are synthetic and live in `assets/fixtures/`.
3. GAQL you add must run on the current API version; write its state next to it.
4. Run the self test (the CI runs the same on Python 3.10 and 3.12):

```bash
python -B scripts/self_test.py
```

It compiles every script with the bytecode outside the repo, runs the tool tests and checks repository hygiene. Do not run `python -m py_compile` on its own: it writes `__pycache__` into the repo.

## Style

- Practical account-operator guidance over generic PPC definitions.
- Short sections so agents can load only the relevant context.
- Copyable examples.
- State assumptions when a recommendation depends on volume, conversion tracking, attribution or budget.
- No em dashes and no spaced hyphens used as punctuation (the self test checks it).

## Security

If you find a security issue, do not publish private account data in an issue. Use GitHub private vulnerability reporting or contact the repository maintainer privately.
