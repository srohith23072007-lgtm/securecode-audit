# Remediation plan

This project includes an intentionally vulnerable, fake-data baseline only in `Test Cases/fixtures/vulnerable_demo.py`. It is never used by the application or pytest and is excluded from the default Bandit target.

| Baseline weakness | Risk | Remediation implemented in production code | Verification |
|---|---|---|---|
| Password represented by a hard-coded fake value | Secrets in source can leak through source control and logs. | Require an environment-supplied pepper; no operational credential is checked in. | Missing/short pepper test and source review. |
| MD5 used to hash a password | Fast hashes make offline password guessing much cheaper. | PBKDF2-HMAC-SHA-256 with 600,000 iterations, fresh 16-byte salt, and 32-byte output. | Registration and successful/failed login tests. |
| Username concatenated into an SQL query | Crafted input can alter query structure. | Validate the username and bind it with SQLite `?` placeholders. | Invalid injection-shaped username test and source review. |
| Broad exception swallowed | Database failures become invisible and behavior is misleading. | Translate only the expected duplicate constraint error; present generic safe CLI errors for expected failures. | Duplicate-registration test and manual review. |

## Operational follow-up

For a real service, add rate limiting and monitoring, authenticated transport, session/token lifecycle controls, secret provisioning/rotation, backup protection, dependency updates, and deployment-specific threat modeling. Do not deploy this demo as-is.
