#!/usr/bin/env python3
"""Find pytest tests matching a name or keyword."""

from __future__ import annotations

import argparse
import subprocess
import sys


def find_tests(test_query: str, verbose: bool = False) -> int:
    """Run pytest --collect-only and filter lines matching test_query."""
    cmd = [sys.executable, "-m", "pytest", "--collect-only", "-q", "-k", test_query]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)

    if result.returncode not in (0, 5):  # 5 = no tests collected
        print(result.stderr or result.stdout, file=sys.stderr)
        return result.returncode

    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    matches = [line for line in lines if test_query in line or line.endswith(test_query)]

    if not matches:
        print(f"No tests found matching: {test_query}", file=sys.stderr)
        if verbose and lines:
            print("\nAll collected tests:", file=sys.stderr)
            for line in lines:
                print(f"  {line}", file=sys.stderr)
        return 1

    for line in matches:
        print(line)

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Find pytest tests by name or keyword.")
    parser.add_argument("--test", required=True, help="Test function name or keyword")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show all tests if no match")
    args = parser.parse_args()
    return find_tests(args.test, verbose=args.verbose)


if __name__ == "__main__":
    raise SystemExit(main())
