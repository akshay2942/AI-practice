#!/usr/bin/env python3
"""Check 3-layer framework compliance for Python files."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]

VIOLATIONS: list[tuple[str, int, str, str]] = []


def _layer(path: Path) -> str | None:
    parts = path.parts
    if "tests" in parts:
        return "test"
    if "services" in parts:
        return "service"
    if "pages" in parts:
        return "page"
    return None


def _check_file(path: Path) -> None:
    layer = _layer(path)
    if layer is None:
        return

    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        VIOLATIONS.append((str(path), 0, "read_error", str(exc)))
        return

    lines = content.splitlines()

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue

        if layer in ("page", "service"):
            if re.search(r"\bassert\b", stripped) or "AssertionError" in stripped:
                VIOLATIONS.append((str(path), i, "assertion_in_layer", stripped))
            if "time.sleep(" in stripped or "wait_for_timeout(" in stripped:
                VIOLATIONS.append((str(path), i, "hardcoded_wait", stripped))

        if layer == "service" and re.search(r"self\.page\.(click|fill|type|press)\(", stripped):
            VIOLATIONS.append((str(path), i, "direct_playwright", stripped))

        if layer == "page" and re.search(r"def verify_\w+", stripped):
            VIOLATIONS.append((str(path), i, "verify_naming", stripped))

        if layer == "test":
            if re.search(r"page\.locator\(", stripped):
                VIOLATIONS.append((str(path), i, "raw_playwright_in_test", stripped))
            if re.search(r"LoginPage\(|InventoryPage\(", stripped) and "isinstance" not in stripped:
                VIOLATIONS.append((str(path), i, "direct_page_in_test", stripped))


def _collect_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for p in paths:
        if p.is_file() and p.suffix == ".py":
            files.append(p)
        elif p.is_dir():
            files.extend(sorted(p.rglob("*.py")))
    return files


def _git_diff_files() -> list[Path]:
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
        cwd=ROOT,
    )
    staged = subprocess.run(
        ["git", "diff", "--name-only", "--cached"],
        capture_output=True,
        text=True,
        check=False,
        cwd=ROOT,
    )
    names = set(result.stdout.splitlines()) | set(staged.stdout.splitlines())
    return [ROOT / n for n in names if n.endswith(".py") and (ROOT / n).exists()]


def main() -> int:
    parser = argparse.ArgumentParser(description="Check framework compliance.")
    parser.add_argument(
        "--path",
        action="append",
        default=[],
        metavar="PATH",
        help="File or directory to check (repeatable)",
    )
    parser.add_argument("--git-diff", action="store_true", help="Check changed Python files only")
    args = parser.parse_args()

    if args.git_diff:
        files = _git_diff_files()
    elif args.path:
        files = _collect_files([ROOT / p if not Path(p).is_absolute() else Path(p) for p in args.path])
    else:
        files = _collect_files([ROOT / "tests", ROOT / "services", ROOT / "pages"])

    for f in files:
        _check_file(f.relative_to(ROOT) if f.is_relative_to(ROOT) else f)

    if not VIOLATIONS:
        print("Compliance check passed.")
        return 0

    print(f"Found {len(VIOLATIONS)} issue(s):\n")
    for path, line, kind, detail in VIOLATIONS:
        print(f"  [{kind}] {path}:{line}")
        print(f"    {detail}\n")

    critical = sum(1 for _, _, k, _ in VIOLATIONS if k in ("assertion_in_layer", "direct_playwright"))
    return 1 if critical else 0


if __name__ == "__main__":
    raise SystemExit(main())
