# SecureCode-Audit

A beginner-friendly, local-only project for Task 3: Secure Coding Review. It demonstrates how to review a small Python authentication application, run Bandit static analysis, test security-sensitive behavior with pytest, and document findings and remediation.

> **Safety and scope:** The application uses a local SQLite database only. It does not contact external systems. The deliberately vulnerable file under `Test Cases/fixtures/` is test-only teaching material containing fake values; do not copy its patterns into real applications.

## What is included

- A secure Python account-registration/authentication service using PBKDF2-HMAC-SHA-256, per-user random salts, and constant-time digest comparison.
- Username/password validation and parameterized SQLite queries.
- A required, environment-provided password pepper; no live credentials are included.
- Safe CLI error messages that do not print exception details or password values.
- Pytest tests for validation, account creation, authentication, SQL-injection-shaped inputs, and duplicate users.
- A Bandit runner that scans production code by default and can separately scan the test-only vulnerable example.
- A checklist, remediation plan, final audit report, and sample scan output.

## Requirements

- Windows 10/11
- Python 3.10 or newer (the code uses only the standard library at runtime)
- Visual Studio Code with the Python extension

## Windows VS Code setup and run-through

Open this project folder in VS Code, then open **Terminal → New Terminal** (PowerShell). Run all commands below from the project root.

1. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal, then activate again.

2. Install the project tools:

   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

3. Run the automated tests:

   ```powershell
   python -m pytest
   ```

4. Run the Bandit scan on production code:

   ```powershell
   python "Security Tools\run_security_scan.py"
   ```

   A clean run reports **No issues identified**. For comparison, scan the explicitly test-only vulnerable example:

   ```powershell
   python "Security Tools\run_security_scan.py" --include-test-only
   ```

   That comparison is expected to report findings and return a non-zero exit code. It does not make network connections or alter production source.

5. Configure a local pepper for the demo. Use a unique random value for any actual deployment; this project value is only for a disposable local database. For the current PowerShell session:

   ```powershell
   $env:SECURECODE_AUDIT_PEPPER = "local-demo-pepper-change-this-32-chars"
   ```

   Optionally set a database path (the default is `securecode_audit.sqlite3` in the current directory):

   ```powershell
   $env:SECURECODE_AUDIT_DB = ".\securecode_audit.sqlite3"
   ```

6. Run the website demo in a browser. From the project root:

   ```powershell
   python "Source Code\web_app.py"
   ```

   Then open `http://127.0.0.1:5000` in a browser and register or log in with a demo user. If you prefer to stay in the terminal, the CLI flow still works:

   ```powershell
   Set-Location "Source Code"
   python -m securecode_audit.cli register demo_user
   python -m securecode_audit.cli login demo_user
   Set-Location ..
   ```

   Registration requires a password of 12–128 characters. The pepper must be supplied on every run. Do not put secrets in source files or commit them. The `.gitignore` excludes local database files and virtual environments.

7. Review `Security Analysis/`, `Reports/final_audit_report.md`, and `Reports/sample_bandit_output.txt` for the checklist, risk analysis, remediation record, and example output.

## Interpreting Bandit

Bandit reports an issue identifier, severity, confidence, file/line, and a short explanation. Severity and confidence are separate: severity estimates impact; confidence indicates how certain the rule match is. Review every finding in context rather than treating a clean scan as proof of security. The default scan is restricted to `Source Code/securecode_audit`; `--include-test-only` intentionally adds the unsafe fixture to demonstrate detections.

The sample output in `Reports/sample_bandit_output.txt` illustrates a clean post-remediation production scan. Exact formatting can differ across Bandit versions.

## Project structure

```text
Project Documentation/
  security_review_guide.md
Source Code/
  app.py
  securecode_audit/
    __init__.py
    cli.py
    database.py
    errors.py
    password.py
    service.py
    validation.py
Security Analysis/
  remediation_plan.md
  vulnerability_checklist.md
Security Tools/
  run_security_scan.py
Test Cases/
  conftest.py
  test_auth_service.py
  test_validation.py
  fixtures/
    vulnerable_demo.py
Reports/
  final_audit_report.md
  sample_bandit_output.txt
```

## Limitations

This is a teaching example, not a production-ready identity system. It omits rate limiting, account recovery, secure transport, session management, audit logging, deployment hardening, and operational secret rotation. A password pepper change invalidates authentication against hashes made with the old pepper unless a deliberate migration strategy is implemented.
