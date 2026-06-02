#!/usr/bin/env python3
"""Check protocol templates stay synchronized with copyable template assets."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

PAIRS = [
    (
        ROOT / "templates" / "user-protocol.md",
        ROOT / "references" / "protocol" / "user-protocol-template.md",
    ),
    (
        ROOT / "templates" / "project-protocol.md",
        ROOT / "references" / "protocol" / "project-protocol-template.md",
    ),
    (
        ROOT / "templates" / "route-card.md",
        ROOT / "references" / "protocol" / "route-card-template.md",
    ),
]


def main() -> int:
    mismatches = []
    missing = []

    for left, right in PAIRS:
        if not left.is_file():
            missing.append(str(left.relative_to(ROOT)))
            continue
        if not right.is_file():
            missing.append(str(right.relative_to(ROOT)))
            continue
        if left.read_text(encoding="utf-8") != right.read_text(encoding="utf-8"):
            mismatches.append(
                f"{left.relative_to(ROOT)} != {right.relative_to(ROOT)}"
            )

    if missing:
        print("Missing template files:", file=sys.stderr)
        for path in missing:
            print(f"  {path}", file=sys.stderr)
    if mismatches:
        print("Template files are out of sync:", file=sys.stderr)
        for pair in mismatches:
            print(f"  {pair}", file=sys.stderr)

    if missing or mismatches:
        return 1

    print("PASS: template assets are synchronized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
