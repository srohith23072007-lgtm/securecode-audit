"""Run Bandit against production code, optionally including the unsafe fixture."""

import argparse
import importlib.util
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PRODUCTION_SOURCE = PROJECT_ROOT / "Source Code" / "securecode_audit"
TEST_ONLY_FIXTURE = PROJECT_ROOT / "Test Cases" / "fixtures" / "vulnerable_demo.py"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--include-test-only",
        action="store_true",
        help="Also scan the deliberately vulnerable, local-only teaching fixture.",
    )
    arguments = parser.parse_args()

    if importlib.util.find_spec("bandit") is None:
        print(
            "Bandit is not installed. Install project dependencies with "
            "'python -m pip install -r requirements.txt'.",
            file=sys.stderr,
        )
        return 2

    scan_paths = [str(PRODUCTION_SOURCE)]
    if arguments.include_test_only:
        scan_paths.append(str(TEST_ONLY_FIXTURE))
    command = [
        sys.executable,
        "-m",
        "bandit",
        "-r",
        *scan_paths,
        "-f",
        "screen",
    ]
    try:
        result = subprocess.run(command, check=False)
    except OSError:
        print("Bandit could not be started.", file=sys.stderr)
        return 2
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
