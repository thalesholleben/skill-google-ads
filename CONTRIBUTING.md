# Contributing

Thanks for improving this Google Ads skill. This repository is a knowledge package plus a few standalone Python templates, not a web app or service.

## Good contributions

- Improve Google Ads strategy guidance with clear 2026 context.
- Add or refine reference material in `references/`.
- Improve the Python report and n-gram scripts without adding external service dependencies.
- Add synthetic examples that help agents understand how to use the skill.
- Improve installation, security, or agent instructions.

## Before opening a pull request

1. Read `SKILL.md` first.
2. Keep reference files focused on one topic.
3. Do not commit credentials, real customer IDs, account IDs, OAuth tokens, or real client exports.
4. Do not replace the fictional script data with private client data.
5. Run a basic syntax check for changed Python files:

```bash
python -m py_compile scripts/*.py
```

## Style

- Prefer practical account-operator guidance over generic PPC definitions.
- Use Markdown headings and short sections so agents can load only the relevant context.
- Keep examples copyable.
- Explain assumptions when a recommendation depends on volume, conversion tracking, attribution, or budget.

## Security

If you find a security issue, do not publish private account data in an issue. Use GitHub private vulnerability reporting or contact the repository maintainer privately.
