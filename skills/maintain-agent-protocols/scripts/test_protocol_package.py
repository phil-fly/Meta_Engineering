from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
MODULE_PATH = SCRIPT_DIR / "protocol-package.py"
MANIFEST_PATH = SCRIPT_DIR / "protocol-package-manifest.json"
SPEC = importlib.util.spec_from_file_location("protocol_package", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Cannot load {MODULE_PATH}")
protocol_package = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = protocol_package
SPEC.loader.exec_module(protocol_package)


class ValidatePackageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp_dir.name)
        self.manifest = protocol_package.load_json(MANIFEST_PATH)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def scaffold(self) -> None:
        protocol_package.scaffold_package(self.repo, self.manifest, "minimal", False)

    def write_valid_entry(self) -> None:
        (self.repo / "AGENTS.md").write_text(
            "# Agent Protocol\n\n开发任务读取 [编码手册](ai-agent-workspace/protocols/playbooks/coding.md)。\n",
            encoding="utf-8",
        )

    def test_validate_fails_without_effective_entry(self) -> None:
        self.scaffold()

        result = protocol_package.validate_package(self.repo, self.manifest)

        self.assertFalse(result["ok"])
        self.assertEqual(result["entry_files"], [])
        self.assertTrue(result["entry_errors"])

    def test_validate_passes_after_entry_and_scaffold(self) -> None:
        self.scaffold()
        self.write_valid_entry()

        result = protocol_package.validate_package(self.repo, self.manifest)

        self.assertTrue(result["ok"], result)
        self.assertEqual(result["entry_files"], ["AGENTS.md"])
        self.assertEqual(result["entry_errors"], [])
        self.assertEqual(result["content_errors"], [])

    def test_validate_rejects_broken_entry_reference(self) -> None:
        self.scaffold()
        (self.repo / "AGENTS.md").write_text(
            "# Agent Protocol\n\n读取 [缺失手册](ai-agent-workspace/protocols/playbooks/missing.md)。\n",
            encoding="utf-8",
        )

        result = protocol_package.validate_package(self.repo, self.manifest)

        self.assertFalse(result["ok"])
        self.assertIn(
            "AGENTS.md 引用不存在：ai-agent-workspace/protocols/playbooks/missing.md",
            result["entry_errors"],
        )

    def test_validate_rejects_broken_inline_entry_reference(self) -> None:
        self.scaffold()
        (self.repo / "AGENTS.md").write_text(
            "# Agent Protocol\n\n开发任务读取 `docs/missing.md`。\n",
            encoding="utf-8",
        )

        result = protocol_package.validate_package(self.repo, self.manifest)

        self.assertFalse(result["ok"])
        self.assertIn("AGENTS.md 引用不存在：docs/missing.md", result["entry_errors"])

    def test_validate_rejects_empty_workflow_assets(self) -> None:
        self.scaffold()
        self.write_valid_entry()
        playbooks = self.repo / "ai-agent-workspace" / "protocols" / "playbooks"
        for path in playbooks.glob("*.md"):
            path.write_text("# Empty\n", encoding="utf-8")

        result = protocol_package.validate_package(self.repo, self.manifest)

        self.assertFalse(result["ok"])
        self.assertIn(
            "ai-agent-workspace/protocols/playbooks/ 未包含 WF-* 工作流",
            result["content_errors"],
        )

    def test_validate_rejects_workflow_id_mentioned_only_in_prose(self) -> None:
        self.scaffold()
        self.write_valid_entry()
        playbooks = self.repo / "ai-agent-workspace" / "protocols" / "playbooks"
        for path in playbooks.glob("*.md"):
            path.write_text("# Notes\n\nExpected workflow: WF-CODING.\n", encoding="utf-8")

        result = protocol_package.validate_package(self.repo, self.manifest)

        self.assertFalse(result["ok"])
        self.assertIn(
            "ai-agent-workspace/protocols/playbooks/ 未包含 WF-* 工作流",
            result["content_errors"],
        )

    def test_validate_rejects_empty_check_assets(self) -> None:
        self.scaffold()
        self.write_valid_entry()
        checks = self.repo / "ai-agent-workspace" / "protocols" / "checks"
        for path in checks.glob("*.md"):
            path.write_text("# Empty\n", encoding="utf-8")

        result = protocol_package.validate_package(self.repo, self.manifest)

        self.assertFalse(result["ok"])
        self.assertIn(
            "ai-agent-workspace/protocols/checks/ 未包含 CHK-* 检查项",
            result["content_errors"],
        )

    def test_validate_rejects_check_id_mentioned_only_in_prose(self) -> None:
        self.scaffold()
        self.write_valid_entry()
        checks = self.repo / "ai-agent-workspace" / "protocols" / "checks"
        for path in checks.glob("*.md"):
            path.write_text("# Notes\n\nExpected check: CHK-CODING.\n", encoding="utf-8")

        result = protocol_package.validate_package(self.repo, self.manifest)

        self.assertFalse(result["ok"])
        self.assertIn(
            "ai-agent-workspace/protocols/checks/ 未包含 CHK-* 检查项",
            result["content_errors"],
        )

    def test_cli_scaffold_validate_entry_gate_end_to_end(self) -> None:
        scaffold = subprocess.run(
            [sys.executable, str(MODULE_PATH), "scaffold", str(self.repo), "--mode", "minimal"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(scaffold.returncode, 0, scaffold.stderr)

        before_entry = subprocess.run(
            [sys.executable, str(MODULE_PATH), "validate", str(self.repo)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(before_entry.returncode, 1)
        self.assertTrue(json.loads(before_entry.stdout)["entry_errors"])

        self.write_valid_entry()
        after_entry = subprocess.run(
            [sys.executable, str(MODULE_PATH), "validate", str(self.repo)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(after_entry.returncode, 0, after_entry.stderr)
        self.assertTrue(json.loads(after_entry.stdout)["ok"])


if __name__ == "__main__":
    unittest.main()
