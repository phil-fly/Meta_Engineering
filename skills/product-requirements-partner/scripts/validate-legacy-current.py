#!/usr/bin/env python3
"""Validate explicit legacy-current frontmatter on legacy product documents."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path


FIELD_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$")
TOKEN_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
REQUIRED_FIELDS = {"product_state", "legacy_scope", "legacy_version", "effective_at"}


def parse_document(path: Path, errors: list[str]) -> str | None:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        errors.append(f"{path}: cannot read file: {exc}")
        return None

    if not lines or lines[0].strip() != "---":
        errors.append(f"{path}: missing legacy-current frontmatter start '---'")
        return None
    try:
        end = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        errors.append(f"{path}: missing legacy-current frontmatter end '---'")
        return None

    fields: dict[str, str] = {}
    for line_number, line in enumerate(lines[1:end], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = FIELD_RE.match(line)
        if not match:
            errors.append(f"{path}:{line_number}: invalid frontmatter field")
            continue
        name, value = match.groups()
        if name in fields:
            errors.append(f"{path}:{line_number}: duplicate frontmatter field '{name}'")
        fields[name] = value.strip()

    missing = REQUIRED_FIELDS - fields.keys()
    for name in sorted(missing):
        errors.append(f"{path}: missing required frontmatter field '{name}'")
    if missing:
        return None

    if fields["product_state"] != "legacy-current":
        errors.append(f"{path}: product_state must be legacy-current")
    scope = fields["legacy_scope"]
    if not TOKEN_RE.fullmatch(scope):
        errors.append(f"{path}: legacy_scope must be a stable ID")
    version = fields["legacy_version"]
    if version != "N/A" and not TOKEN_RE.fullmatch(version):
        errors.append(f"{path}: legacy_version must be a stable ID or N/A")
    try:
        timestamp = datetime.fromisoformat(fields["effective_at"].replace("Z", "+00:00"))
    except ValueError:
        timestamp = None
        errors.append(f"{path}: effective_at must be ISO-8601")
    if timestamp is not None and (timestamp.tzinfo is None or timestamp.utcoffset() is None):
        errors.append(f"{path}: effective_at must include a timezone")
    return scope


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", required=True, nargs="+", type=Path, help="legacy product document(s)")
    args = parser.parse_args()

    errors: list[str] = []
    scopes: list[str] = []
    for path in args.path:
        if not path.is_file():
            errors.append(f"{path}: does not exist or is not a file")
            continue
        scope = parse_document(path, errors)
        if scope is not None:
            scopes.append(scope)

    for scope, count in Counter(scopes).items():
        if count > 1:
            errors.append(f"legacy_scope '{scope}' has multiple legacy-current documents")

    if errors:
        print("FAIL: legacy-current validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PASS: legacy-current validation ({len(scopes)} document(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
