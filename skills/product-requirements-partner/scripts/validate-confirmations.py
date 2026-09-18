#!/usr/bin/env python3
"""Validate and project the current state from CONFIRMATIONS.md."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


CANONICAL_REGISTRY = Path("ai-agent-workspace/product/memory/CONFIRMATIONS.md")
LEGACY_REGISTRY = Path("docs/00_MEMORY/CONFIRMATIONS.md")
HEADING_RE = re.compile(r"^##\s+(CONF-[A-Za-z0-9][A-Za-z0-9._-]*)\b")
CONF_HEADING_RE = re.compile(r"^#{1,6}\s+CONF-")
FIELD_RE = re.compile(r"^-\s+\*\*([^*:]+):?\*\*:?[ \t]*(.*)$")
CONF_ID_RE = re.compile(r"^CONF-[A-Za-z0-9][A-Za-z0-9._-]*$")
REQ_ID_RE = re.compile(r"^REQ-[A-Za-z0-9][A-Za-z0-9._-]*$")
SCOPE_RE = re.compile(
    r"^[A-Za-z0-9][A-Za-z0-9._-]*@(?:N/A|[A-Za-z0-9][A-Za-z0-9._-]*)$"
)

REQUIRED_FIELDS = {
    "Confirmed at",
    "Source",
    "Object",
    "Requirement ID",
    "Scope/Version",
    "Decision state",
    "Change type",
    "Affected fields",
    "Accepted conclusion",
    "User quote",
    "Status",
    "Supersedes",
}
ALLOWED_DECISION_STATES = {"confirmed", "deferred", "rejected"}
ALLOWED_CHANGE_TYPES = {"add", "patch", "replace", "remove"}
ALLOWED_STATUSES = {"active", "superseded", "withdrawn"}
NULL_VALUES = {"", "N/A", "n/a", "-", "{...}"}


def parse_timestamp(value: str, location: str, errors: list[str]) -> datetime | None:
    try:
        timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{location}: Confirmed at must be ISO-8601")
        return None
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        errors.append(f"{location}: Confirmed at must include a timezone")
        return None
    return timestamp


def parse_records(path: Path, errors: list[str]) -> list[dict[str, object]]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        errors.append(f"{path}: cannot read file: {exc}")
        return []

    records: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    for line_number, line in enumerate(lines, start=1):
        heading = HEADING_RE.match(line)
        if heading:
            if current is not None:
                records.append(current)
            current = {"id": heading.group(1), "line": line_number, "fields": {}}
            continue
        if CONF_HEADING_RE.match(line):
            errors.append(f"{path}:{line_number}: confirmation headings must use level 2 (##)")
            continue
        if current is None:
            continue
        field = FIELD_RE.match(line)
        if not field:
            continue
        name, value = field.groups()
        fields = current["fields"]
        assert isinstance(fields, dict)
        if name in fields:
            errors.append(
                f"{path}:{line_number}: duplicate field '{name}' in {current['id']}"
            )
        fields[name] = value.strip()
    if current is not None:
        records.append(current)

    if not records:
        errors.append(f"{path}: no confirmation records found")
        return []

    seen_ids: set[str] = set()
    for record in records:
        record_id = str(record["id"])
        location = f"{path}:{record['line']} ({record_id})"
        if not CONF_ID_RE.fullmatch(record_id):
            errors.append(f"{location}: invalid confirmation ID")
        if record_id in seen_ids:
            errors.append(f"{location}: duplicate confirmation ID")
        seen_ids.add(record_id)

        fields = record["fields"]
        assert isinstance(fields, dict)
        missing = REQUIRED_FIELDS - fields.keys()
        for name in sorted(missing):
            errors.append(f"{location}: missing required field '{name}'")
        if missing:
            continue

        for name in REQUIRED_FIELDS - {"Affected fields", "Supersedes"}:
            value = str(fields[name]).strip()
            if value in NULL_VALUES or value.startswith("{"):
                errors.append(f"{location}: field '{name}' is empty or a placeholder")

        timestamp = parse_timestamp(str(fields["Confirmed at"]), location, errors)
        record["timestamp"] = timestamp

        requirement_id = str(fields["Requirement ID"])
        if not REQ_ID_RE.fullmatch(requirement_id):
            errors.append(f"{location}: Requirement ID must match REQ-*")
        scope = str(fields["Scope/Version"])
        if not SCOPE_RE.fullmatch(scope):
            errors.append(
                f"{location}: Scope/Version must be a stable scope_id@version token"
            )
        decision_state = str(fields["Decision state"])
        if decision_state not in ALLOWED_DECISION_STATES:
            errors.append(f"{location}: invalid Decision state '{decision_state}'")
        change_type = str(fields["Change type"])
        if change_type not in ALLOWED_CHANGE_TYPES:
            errors.append(f"{location}: invalid Change type '{change_type}'")
        status = str(fields["Status"])
        if status not in ALLOWED_STATUSES:
            errors.append(f"{location}: invalid Status '{status}'")

        affected = str(fields.get("Affected fields", "N/A"))
        if change_type == "patch" and affected in NULL_VALUES:
            errors.append(f"{location}: patch requires Affected fields")
        supersedes = str(fields.get("Supersedes", "N/A"))
        if change_type in {"patch", "replace", "remove"} and supersedes in NULL_VALUES:
            errors.append(f"{location}: {change_type} requires Supersedes")
        if change_type == "add" and supersedes not in NULL_VALUES:
            errors.append(f"{location}: add must not Supersede another record")
        if change_type == "remove" and decision_state not in {"rejected", "deferred"}:
            errors.append(f"{location}: remove must be rejected or deferred")
        record["key"] = (requirement_id, scope)
        record["supersedes"] = supersedes

    return records


def validate_relationships(records: list[dict[str, object]], errors: list[str]) -> None:
    by_id = {str(record["id"]): record for record in records}
    records_by_key: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)

    for record in records:
        key = record.get("key")
        if key is not None:
            records_by_key[key].append(record)

        supersedes = str(record.get("supersedes", "N/A"))
        if supersedes in NULL_VALUES:
            continue
        location = f"{record['id']} (line {record['line']})"
        target = by_id.get(supersedes)
        if target is None:
            errors.append(f"{location}: Supersedes references unknown {supersedes}")
            continue
        if target["id"] == record["id"]:
            errors.append(f"{location}: a record cannot supersede itself")
        if target.get("key") != key:
            errors.append(
                f"{location}: Supersedes must use the same Requirement ID and Scope/Version"
            )
        target_fields = target["fields"]
        assert isinstance(target_fields, dict)
        if target_fields.get("Status") not in {"superseded", "withdrawn"}:
            errors.append(f"{location}: superseded target {supersedes} must not remain active")
        timestamp = record.get("timestamp")
        target_timestamp = target.get("timestamp")
        if timestamp is not None and target_timestamp is not None and timestamp <= target_timestamp:
            errors.append(f"{location}: Confirmed at must be later than {supersedes}")

    for key, key_records in records_by_key.items():
        ordered = [record for record in key_records if record.get("timestamp") is not None]
        if len(ordered) != len(key_records):
            continue
        ordered.sort(key=lambda record: record["timestamp"])
        if str(ordered[0]["fields"].get("Change type")) != "add":
            errors.append(f"reconstruction key {key!r} must start with Change type add")
        for record in ordered[1:]:
            if str(record["fields"].get("Change type")) == "add":
                errors.append(f"reconstruction key {key!r} may contain only one add record")

        active_records = [
            record for record in ordered if record["fields"].get("Status") == "active"
        ]
        if len(active_records) != 1:
            ids = ", ".join(str(record["id"]) for record in active_records) or "none"
            errors.append(
                f"reconstruction key {key!r} must have exactly one active record; found {ids}"
            )
        elif active_records[0] is not ordered[-1]:
            errors.append(f"reconstruction key {key!r} active record must be the latest record")

        for previous, current in zip(ordered, ordered[1:]):
            if previous.get("timestamp") == current.get("timestamp"):
                errors.append(
                    f"reconstruction key {key!r} has an unresolvable timestamp tie: "
                    f"{previous['id']} and {current['id']}"
                )
            if current.get("supersedes") != previous["id"]:
                errors.append(
                    f"{current['id']}: Supersedes must reference the immediately previous "
                    f"record {previous['id']}"
                )

    for record in records:
        seen: set[str] = set()
        current = str(record["id"])
        while current not in NULL_VALUES and current in by_id:
            if current in seen:
                errors.append(f"{record['id']}: Supersedes chain contains a cycle")
                break
            seen.add(current)
            current = str(by_id[current].get("supersedes", "N/A"))


def resolve_registry(
    path: Path | None, project: Path | None, errors: list[str]
) -> Path | None:
    if path is not None:
        if not path.is_file():
            errors.append(f"{path}: does not exist or is not a file")
            return None
        return path

    assert project is not None
    candidates = [project / CANONICAL_REGISTRY, project / LEGACY_REGISTRY]
    existing = [candidate for candidate in candidates if candidate.is_file()]
    if len(existing) > 1:
        errors.append(
            "split-brain confirmation registries: both canonical and legacy paths exist; "
            "migrate to one source before delivery"
        )
        return None
    if not existing:
        errors.append(f"{project}: no CONFIRMATIONS.md found at a supported path")
        return None
    return existing[0]


def project_current_states(
    records: list[dict[str, object]], scope: str | None
) -> list[dict[str, str]]:
    current_states: list[dict[str, str]] = []
    for record in records:
        fields = record["fields"]
        assert isinstance(fields, dict)
        if fields.get("Status") != "active":
            continue
        scope_version = str(fields["Scope/Version"])
        if scope is not None and scope_version != scope:
            continue
        current_states.append(
            {
                "confirmation_id": str(record["id"]),
                "requirement_id": str(fields["Requirement ID"]),
                "scope_version": scope_version,
                "decision_state": str(fields["Decision state"]),
                "change_type": str(fields["Change type"]),
                "accepted_conclusion": str(fields["Accepted conclusion"]),
            }
        )
    return sorted(
        current_states,
        key=lambda state: (state["scope_version"], state["requirement_id"]),
    )


def emit_errors(errors: list[str], as_json: bool) -> None:
    if as_json:
        print(json.dumps({"status": "fail", "errors": errors}, ensure_ascii=False, indent=2))
        return
    print("FAIL: confirmation validation", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--path", type=Path, help="explicit CONFIRMATIONS.md path")
    source.add_argument("--project", type=Path, help="project root; supported paths are resolved")
    parser.add_argument("--scope", help="project only one Scope/Version token")
    parser.add_argument("--json", action="store_true", help="emit current-state JSON")
    args = parser.parse_args(argv)

    errors: list[str] = []
    if args.scope is not None and not SCOPE_RE.fullmatch(args.scope):
        errors.append("--scope must be a stable scope_id@version token")
    registry = resolve_registry(args.path, args.project, errors)
    records: list[dict[str, object]] = []
    if registry is not None:
        records = parse_records(registry, errors)
        validate_relationships(records, errors)
    current_states = project_current_states(records, args.scope) if not errors else []
    if not errors and registry is not None and args.scope is not None and not current_states:
        errors.append(f"{registry}: no active confirmation state for scope {args.scope}")

    if errors:
        emit_errors(errors, args.json)
        return 1

    assert registry is not None
    if args.json:
        print(
            json.dumps(
                {
                    "status": "pass",
                    "source": str(registry),
                    "record_count": len(records),
                    "current_states": current_states,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(
            f"PASS: {registry} ({len(records)} confirmation records, "
            f"{len(current_states)} current states)"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
