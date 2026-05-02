# Security Policy

## Supported versions

This repository publishes the current skill content only. Use the latest `main` branch unless a release says otherwise.

## Sensitive data rules

Do not commit:

- Google Ads API credentials
- OAuth tokens
- manager account IDs or customer IDs
- real client exports
- generated client reports
- private email recipients used in Google Ads Scripts

The repository intentionally uses placeholders and fictional example data. Keep real account data in private working copies only.

## Reporting a vulnerability

Use GitHub private vulnerability reporting when available, or contact the maintainer privately. Include:

- affected file or workflow
- what data could be exposed
- steps to reproduce
- suggested fix, if known

Please do not open a public issue that contains credentials, account IDs, exported search terms, or private client performance data.
