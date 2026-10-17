# Security policy

## Scope

This repository contains schemas, source metadata, documentation and read-only tooling. It should never contain API keys, access tokens, private conversation exports, credentials, or private recordings.

## Reporting a vulnerability

Please do not publish secrets or exploit details in a public issue. If GitHub's private vulnerability reporting is available for this repository, use the repository's **Security → Report a vulnerability** route. If that route is unavailable, contact the maintainer through the public GitHub profile and ask for a private reporting channel.

Include the affected path, commit or release, impact, and a minimal reproduction that contains no secrets or personal data. The maintainer is a solo volunteer and cannot promise a response-time SLA.

## Maintainer response

Triage, remediation, and release timing depend on severity and available capacity. Do not assume a report is fixed until a public commit or release documents the change. Rotate any potentially exposed credential in its issuing service; never include the replacement credential in an issue, pull request, log, or commit.
