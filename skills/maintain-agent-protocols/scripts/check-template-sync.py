#!/usr/bin/env python3
"""Check that template assets and protocol reference templates stay in sync."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

PAIRS = [
    ("templates/user-protocol.md", "references/protocol/user-protocol-template.md"),
    ("templates/project-protocol.md", "references/protocol/project-protocol-template.md"),
    ("templates/route-card.md", "references/protocol/route-card-template.md"),
]


def read_bytes(path: str) -> bytes:
    full_path = ROOT / path
    if not full_path.exists():
        raise FileNotFoundError(path)
    return full_path.read_bytes()


def main() -> int:
    mismatches = []
    missing = []

    for left, right in PAIRS:
        try:
            left_content = read_bytes(left)
            right_content = read_bytes(right)
        except FileNotFoundError as exc:
            missing.append(str(exc))
            continue

        if left_content != right_content:
            mismatches.append((left, right))

    if missing:
        print("FAIL: missing template file(s):", file=sys.stderr)
        for path in missing:
            print(f"  - {path}", file=sys.stderr)
        return 1

    if mismatches:
        print("FAIL: template/reference pairs differ:", file=sys.stderr)
        for left, right in mismatches:
            print(f"  - {left} != {right}", file=sys.stderr)
        return 1

    print("PASS: template assets match protocol reference templates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
