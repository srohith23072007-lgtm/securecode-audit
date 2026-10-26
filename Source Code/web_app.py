"""Entry point for the SecureCode-Audit web demo."""

import os
from securecode_audit.web import create_app

os.environ.setdefault(
    "SECURECODE_AUDIT_PEPPER",
    "local-demo-pepper-change-this-32-chars",
)

app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
