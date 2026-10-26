# Security review guide

## Review method

1. Define scope: this review covers the local sample application in `Source Code/securecode_audit/`, the test-only baseline in `Test Cases/fixtures/`, its automated tests, and the Bandit scan.
2. Read authentication, validation, persistence, and error paths manually. Trace untrusted usernames and passwords to database operations.
3. Run tests with `python -m pytest`.
4. Run Bandit on the production package with `python "Security Tools\run_security_scan.py"`.
5. Compare the explicitly vulnerable teaching fixture using `--include-test-only`. Treat its warnings as expected findings, not as production scan failures.
6. Record each finding with impact, location, severity, confidence, and specific remediation.
7. Re-run tests and the production scan after a remediation. A test-only baseline remains intentionally unsafe and must not be mistaken for a completed application fix.

## Severity guide

- **Critical:** likely compromise of the full application or sensitive data at scale.
- **High:** material compromise of authentication, data confidentiality, or integrity under plausible conditions.
- **Medium:** meaningful weakness with constraints or mitigations that reduce likelihood or impact.
- **Low:** limited impact, defense-in-depth gap, or maintainability concern with security implications.

Bandit's Low/Medium/High severities and confidence ratings are tool outputs, not a complete risk assessment. The audit report combines automated evidence with manual review.

## Reproduction commands

From the project root in PowerShell:

```powershell
python -m pytest
python "Security Tools\run_security_scan.py"
python "Security Tools\run_security_scan.py" --include-test-only
```

The comparison scan is expected to exit with status 1 because the fixture contains deliberate findings.
