# Final security audit report

**Project:** SecureCode-Audit  
**Task:** Task 3 — Secure Coding Review  
**Review date:** 2026-10-11  
**Scope:** Local Python authentication demo, SQLite repository, input validation, error handling, tests, and Bandit static analysis.

## Executive summary

The secure sample implementation uses salted PBKDF2 password hashes, an environment-provided pepper, bounded input validation, parameterized SQLite operations, and safe user-facing error messages. A deliberately unsafe comparison fixture is isolated under `Test Cases/fixtures/`; it uses only in-memory SQLite and fake placeholder data. It is not part of the application.

The baseline teaching fixture demonstrates four categories of issue: hard-coded secret-like value (fake), weak MD5 password hashing, SQL injection through string concatenation, and swallowed exceptions. These patterns were remediated in the production implementation. The production Bandit scan was run after remediation and reported no findings at any severity. Bandit is a static analyzer and cannot prove the absence of vulnerabilities.

## Findings and disposition

| ID | Severity | Finding | Affected file | Remediation / disposition |
|---|---|---|---|---|
| F-01 | Medium | A fake hard-coded password-like value demonstrates unsafe source-based secret management. It is not a real credential and is test-only. | `Test Cases/fixtures/vulnerable_demo.py` | Isolated to fixture; production password pepper must be provided through `SECURECODE_AUDIT_PEPPER`. |
| F-02 | High | MD5 is unsuitable for password storage because it is fast and unsalted in the demonstration. | `Test Cases/fixtures/vulnerable_demo.py` | Production uses salted PBKDF2-HMAC-SHA-256 with 600,000 iterations. |
| F-03 | High | Direct SQL string concatenation permits SQL injection if attacker-controlled input reaches the query. | `Test Cases/fixtures/vulnerable_demo.py` | Production validates usernames and uses parameterized SQLite queries. |
| F-04 | Low | A broad exception handler suppresses a database error, hiding failure conditions. | `Test Cases/fixtures/vulnerable_demo.py` | Production translates only expected uniqueness conflicts; other operational errors are not silently swallowed. |

Severity describes the unsafe pattern if used in an application. All four findings are retained solely as a test-only demonstration; they do not exist in the production package.

## Verification

Verification was performed with Python 3.14.6, pytest 8.4.2, and Bandit 1.9.4:

```powershell
python -m pytest
python "Security Tools\run_security_scan.py"
python "Security Tools\run_security_scan.py" --include-test-only
```

- **Tests:** 19 passed.
- **Production Bandit scan:** exit code 0; 0 Low, 0 Medium, and 0 High findings.
- **Comparison scan:** exit code 1, as expected; it reports the four issues intentionally retained in the test-only fixture.

The second Bandit run is expected to report findings and return a non-zero exit status because the unsafe teaching examples are included explicitly. See `Reports/sample_bandit_output.txt` for representative output.

## Residual risks and limitations

- Password pepper rotation invalidates existing hashes unless a migration approach is designed.
- No online service is exposed; therefore HTTP/session controls, rate limiting, CSRF protections, and transport security are out of scope.
- The local SQLite database is not encrypted. Its file permissions and backups require operating-system controls.
- Static analysis does not replace manual review, dependency auditing, runtime testing, or threat modeling.

## Conclusion

The production demonstration implements the requested secure coding controls and has focused automated tests and a repeatable static-analysis workflow. Keep the vulnerable fixture clearly labeled and excluded from deployable code.
