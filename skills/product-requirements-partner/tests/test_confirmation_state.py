from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
VALIDATE_CONFIRMATIONS = SKILL_ROOT / "scripts" / "validate-confirmations.py"
VALIDATE_LEGACY = SKILL_ROOT / "scripts" / "validate-legacy-current.py"


def confirmation(
    confirmation_id: str,
    requirement_id: str = "REQ-LOGIN",
    scope: str = "account@v1",
    timestamp: str = "2026-09-16T10:00:00+08:00",
    change_type: str = "add",
    decision_state: str = "confirmed",
    status: str = "active",
    supersedes: str = "N/A",
    affected_fields: str = "N/A",
    conclusion: str = "Users can sign in with email.",
) -> str:
    return f"""## {confirmation_id} · Login
- **Confirmed at:** {timestamp}
- **Source:** Session 2026-09-16, turn 1
- **Object:** Login
- **Requirement ID:** {requirement_id}
- **Scope/Version:** {scope}
- **Decision state:** {decision_state}
- **Change type:** {change_type}
- **Affected fields:** {affected_fields}
- **Accepted conclusion:** {conclusion}
- **User quote:** \"Use email login.\"
- **Status:** {status}
- **Supersedes:** {supersedes}
- **Related decision:** N/A
"""


class ConfirmationStateTests(unittest.TestCase):
    def run_script(self, script: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(script), *args],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_empty_registry_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            registry = Path(directory) / "CONFIRMATIONS.md"
            registry.write_text("# User Confirmations\n", encoding="utf-8")

            result = self.run_script(VALIDATE_CONFIRMATIONS, "--path", str(registry))

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no confirmation records found", result.stderr)

    def test_single_active_record_projects_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            registry = Path(directory) / "CONFIRMATIONS.md"
            registry.write_text(confirmation("CONF-001"), encoding="utf-8")

            result = self.run_script(
                VALIDATE_CONFIRMATIONS,
                "--path",
                str(registry),
                "--scope",
                "account@v1",
                "--json",
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["record_count"], 1)
        self.assertEqual(payload["current_states"][0]["confirmation_id"], "CONF-001")

    def test_key_requires_exactly_one_active_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            registry = Path(directory) / "CONFIRMATIONS.md"
            registry.write_text(
                confirmation("CONF-001", status="superseded"), encoding="utf-8"
            )

            result = self.run_script(VALIDATE_CONFIRMATIONS, "--path", str(registry))

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must have exactly one active record", result.stderr)

    def test_chain_must_supersede_immediately_previous_record(self) -> None:
        records = "\n".join(
            [
                confirmation("CONF-001", status="superseded"),
                confirmation(
                    "CONF-002",
                    timestamp="2026-09-16T11:00:00+08:00",
                    change_type="patch",
                    status="superseded",
                    supersedes="CONF-001",
                    affected_fields="acceptance.email",
                ),
                confirmation(
                    "CONF-003",
                    timestamp="2026-09-16T12:00:00+08:00",
                    change_type="replace",
                    supersedes="CONF-001",
                ),
            ]
        )
        with tempfile.TemporaryDirectory() as directory:
            registry = Path(directory) / "CONFIRMATIONS.md"
            registry.write_text(records, encoding="utf-8")

            result = self.run_script(VALIDATE_CONFIRMATIONS, "--path", str(registry))

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("immediately previous record CONF-002", result.stderr)

    def test_linear_snapshot_chain_projects_latest_conclusion(self) -> None:
        records = "\n".join(
            [
                confirmation("CONF-001", status="superseded"),
                confirmation(
                    "CONF-002",
                    timestamp="2026-09-16T11:00:00+08:00",
                    change_type="patch",
                    supersedes="CONF-001",
                    affected_fields="acceptance.methods",
                    conclusion="Users can sign in with email or a magic link.",
                ),
            ]
        )
        with tempfile.TemporaryDirectory() as directory:
            registry = Path(directory) / "CONFIRMATIONS.md"
            registry.write_text(records, encoding="utf-8")

            result = self.run_script(
                VALIDATE_CONFIRMATIONS, "--path", str(registry), "--json"
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        state = json.loads(result.stdout)["current_states"][0]
        self.assertEqual(state["confirmation_id"], "CONF-002")
        self.assertEqual(
            state["accepted_conclusion"],
            "Users can sign in with email or a magic link.",
        )

    def test_patch_requires_affected_fields(self) -> None:
        record = confirmation(
            "CONF-002",
            change_type="patch",
            supersedes="CONF-001",
            affected_fields="N/A",
        )
        with tempfile.TemporaryDirectory() as directory:
            registry = Path(directory) / "CONFIRMATIONS.md"
            registry.write_text(record, encoding="utf-8")

            result = self.run_script(VALIDATE_CONFIRMATIONS, "--path", str(registry))

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("patch requires Affected fields", result.stderr)

    def test_project_resolution_rejects_split_brain_registries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            canonical = project / "ai-agent-workspace/product/memory/CONFIRMATIONS.md"
            legacy = project / "docs/00_MEMORY/CONFIRMATIONS.md"
            canonical.parent.mkdir(parents=True)
            legacy.parent.mkdir(parents=True)
            canonical.write_text(confirmation("CONF-001"), encoding="utf-8")
            legacy.write_text(confirmation("CONF-001"), encoding="utf-8")

            result = self.run_script(
                VALIDATE_CONFIRMATIONS, "--project", str(project)
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("split-brain confirmation registries", result.stderr)

    def test_scope_filter_selects_one_delivery_version(self) -> None:
        records = "\n".join(
            [
                confirmation("CONF-001", scope="account@v1"),
                confirmation(
                    "CONF-002",
                    requirement_id="REQ-PROFILE",
                    scope="account@v2",
                    timestamp="2026-09-16T11:00:00+08:00",
                ),
            ]
        )
        with tempfile.TemporaryDirectory() as directory:
            registry = Path(directory) / "CONFIRMATIONS.md"
            registry.write_text(records, encoding="utf-8")

            result = self.run_script(
                VALIDATE_CONFIRMATIONS,
                "--path",
                str(registry),
                "--scope",
                "account@v2",
                "--json",
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        states = json.loads(result.stdout)["current_states"]
        self.assertEqual([state["scope_version"] for state in states], ["account@v2"])

    def test_scope_filter_rejects_missing_delivery_version(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            registry = Path(directory) / "CONFIRMATIONS.md"
            registry.write_text(confirmation("CONF-001"), encoding="utf-8")

            result = self.run_script(
                VALIDATE_CONFIRMATIONS,
                "--path",
                str(registry),
                "--scope",
                "account@v2",
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no active confirmation state for scope account@v2", result.stderr)

    def test_legacy_document_requires_explicit_marker(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            document = Path(directory) / "prd.md"
            document.write_text("# Current PRD\n", encoding="utf-8")

            result = self.run_script(VALIDATE_LEGACY, "--path", str(document))

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing legacy-current frontmatter", result.stdout)


if __name__ == "__main__":
    unittest.main()
