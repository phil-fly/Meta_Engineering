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

    def write_frontend_implementation(self) -> None:
        source = self.repo / "src" / "App.tsx"
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text("export function App() { return <main>App</main>; }\n", encoding="utf-8")

    def backfill_design_tokens(self, content: str) -> str:
        replacements = {
            "初始化状态：待回填": "初始化状态：已建立",
            "| 项目 | 待回填 |": "| 项目 | Example |",
            "| 状态 | 待回填 |": "| 状态 | 已建立 |",
            "| 适用前端 | 待回填 |": "| 适用前端 | src/App.tsx |",
            "| 维护路径 | 待回填 |": (
                "| 维护路径 | ai-agent-workspace/product/design/design-tokens.md |"
            ),
            "| 最近核对日期 | 待回填 |": "| 最近核对日期 | 2026-08-17 |",
            "| 最近核对范围 | 待回填 |": "| 最近核对范围 | src/App.tsx |",
            "| Color | 待回填 |": "| Color | authoritative |",
            "| Typography | 待回填 |": "| Typography | authoritative |",
            "| Spacing | 待回填 |": "| Spacing | authoritative |",
            "| Radius | 待回填 |": "| Radius | authoritative |",
            "| Border | 待回填 |": "| Border | authoritative |",
            "| Shadow / Elevation | 待回填 |": "| Shadow / Elevation | authoritative |",
            "| Layout / Grid | 待回填 |": "| Layout / Grid | authoritative |",
            "| Breakpoint | 待回填 |": "| Breakpoint | authoritative |",
            "| Size / Density | 待回填 |": "| Size / Density | authoritative |",
            "| Motion | 待回填 |": "| Motion | authoritative |",
            "| Icon | 待回填 |": "| Icon | authoritative |",
            "| Z-index / Layer | 待回填 |": "| Z-index / Layer | authoritative |",
            "| Component Token | 待回填 |": "| Component Token | authoritative |",
        }
        for old, new in replacements.items():
            content = content.replace(old, new)
        return content

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

    def test_minimal_scaffold_copies_frontend_design_system_review_prompt(self) -> None:
        self.scaffold()

        prompt = (
            self.repo
            / "ai-agent-workspace"
            / "protocols"
            / "templates"
            / "frontend-design-system-review-prompt.md"
        )

        self.assertTrue(prompt.is_file())
        prompt_content = prompt.read_text(encoding="utf-8")
        self.assertIn("# Frontend Design System Review Prompt", prompt_content)
        self.assertIn("### 4.1 Color", prompt_content)
        self.assertIn("## 8. Responsive 与真实运行行为", prompt_content)
        self.assertIn("## 10. AI / Vibe Coding 机制", prompt_content)
        self.assertIn("## 14. 完成门", prompt_content)

    def test_project_frontend_scaffold_copies_design_system_route_and_checklist(self) -> None:
        self.write_frontend_implementation()

        protocol_package.scaffold_package(self.repo, self.manifest, "project", False)

        package = self.repo / "ai-agent-workspace" / "protocols"
        route = package / "routes" / "frontend" / "design-system-maintenance.md"
        checklist = package / "checks" / "frontend-design-system-checklist.md"
        prompt = package / "templates" / "frontend-design-system-review-prompt.md"
        design_tokens = (
            self.repo
            / "ai-agent-workspace"
            / "product"
            / "design"
            / "design-tokens.md"
        )
        self.assertTrue(route.is_file())
        self.assertIn("CON-FE-DS-001", route.read_text(encoding="utf-8"))
        self.assertIn(
            "frontend-design-system-review-prompt.md",
            route.read_text(encoding="utf-8"),
        )
        self.assertTrue(checklist.is_file())
        self.assertIn("CHK-FE-DS-001", checklist.read_text(encoding="utf-8"))
        self.assertTrue(prompt.is_file())
        self.assertTrue(design_tokens.is_file())
        design_tokens_content = design_tokens.read_text(encoding="utf-8")
        self.assertIn("## 2. 真值源关系", design_tokens_content)
        self.assertIn("## 10. Layout And Grid", design_tokens_content)
        self.assertIn("## 15. Component Tokens", design_tokens_content)

    def test_package_json_alone_does_not_trigger_frontend_assets(self) -> None:
        (self.repo / "package.json").write_text(
            '{"dependencies":{"react":"latest"}}\n',
            encoding="utf-8",
        )

        plan = protocol_package.plan_package(self.repo, self.manifest, "project")

        targets = {item["target"] for item in plan["files"]}
        self.assertNotIn("frontend_implementation", plan["evidence"]["evidence_keys"])
        self.assertNotIn(
            "ai-agent-workspace/product/design/design-tokens.md",
            targets,
        )
        self.assertFalse(any(route["id"] == "frontend" for route in plan["selected_routes"]))

    def test_typescript_ui_entry_triggers_frontend_assets(self) -> None:
        source = self.repo / "src" / "main.ts"
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(
            "import { createApp } from 'vue';\ncreateApp({}).mount('#app');\n",
            encoding="utf-8",
        )

        plan = protocol_package.plan_package(self.repo, self.manifest, "project")

        targets = {item["target"] for item in plan["files"]}
        self.assertIn("frontend_implementation", plan["evidence"]["evidence_keys"])
        self.assertIn(
            "ai-agent-workspace/product/design/design-tokens.md",
            targets,
        )

    def test_frontend_plan_reuses_existing_legacy_design_tokens(self) -> None:
        self.write_frontend_implementation()
        legacy = self.repo / "docs" / "03_DESIGN" / "design-tokens.md"
        legacy.parent.mkdir(parents=True, exist_ok=True)
        template = SCRIPT_DIR.parent / "templates" / "design-tokens.md"
        content = self.backfill_design_tokens(template.read_text(encoding="utf-8"))
        legacy.write_text(content, encoding="utf-8")

        plan = protocol_package.plan_package(self.repo, self.manifest, "project")
        original_content = legacy.read_text(encoding="utf-8")
        result = protocol_package.scaffold_package(self.repo, self.manifest, "project", True)

        artifact = next(item for item in plan["files"] if item["kind"] == "conditional-artifact")
        self.assertEqual(artifact["target"], "docs/03_DESIGN/design-tokens.md")
        self.assertEqual(artifact["action"], "maintain-and-verify")
        self.assertEqual(legacy.read_text(encoding="utf-8"), original_content)
        self.assertIn(legacy.as_posix(), result["skipped"])

    def test_validate_requires_backfilled_design_tokens_for_frontend(self) -> None:
        self.write_frontend_implementation()
        protocol_package.scaffold_package(self.repo, self.manifest, "project", False)
        self.write_valid_entry()

        result = protocol_package.validate_package(self.repo, self.manifest)

        self.assertFalse(result["ok"])
        self.assertIn(
            "ai-agent-workspace/product/design/design-tokens.md "
            "仍包含待回填标记：初始化状态：待回填",
            result["content_errors"],
        )

    def test_validate_accepts_backfilled_design_tokens_for_frontend(self) -> None:
        self.write_frontend_implementation()
        protocol_package.scaffold_package(self.repo, self.manifest, "project", False)
        self.write_valid_entry()
        design_tokens = (
            self.repo
            / "ai-agent-workspace"
            / "product"
            / "design"
            / "design-tokens.md"
        )
        content = self.backfill_design_tokens(design_tokens.read_text(encoding="utf-8"))
        design_tokens.write_text(content, encoding="utf-8")

        result = protocol_package.validate_package(self.repo, self.manifest)

        self.assertTrue(result["ok"], result)
        self.assertEqual(result["content_errors"], [])

    def test_validate_rejects_design_tokens_with_pending_document_status(self) -> None:
        self.write_frontend_implementation()
        protocol_package.scaffold_package(self.repo, self.manifest, "project", False)
        self.write_valid_entry()
        design_tokens = (
            self.repo
            / "ai-agent-workspace"
            / "product"
            / "design"
            / "design-tokens.md"
        )
        content = design_tokens.read_text(encoding="utf-8").replace(
            "初始化状态：待回填",
            "初始化状态：已建立",
        )
        design_tokens.write_text(content, encoding="utf-8")

        result = protocol_package.validate_package(self.repo, self.manifest)

        self.assertFalse(result["ok"])
        self.assertIn(
            "ai-agent-workspace/product/design/design-tokens.md "
            "仍包含待回填标记：| 状态 | 待回填 |",
            result["content_errors"],
        )

    def test_validate_rejects_parallel_design_tokens_sources(self) -> None:
        self.write_frontend_implementation()
        canonical = self.repo / "ai-agent-workspace" / "product" / "design" / "design-tokens.md"
        legacy = self.repo / "docs" / "03_DESIGN" / "design-tokens.md"
        canonical.parent.mkdir(parents=True, exist_ok=True)
        legacy.parent.mkdir(parents=True, exist_ok=True)
        canonical.write_text("# Design Tokens\n", encoding="utf-8")
        legacy.write_text("# Design Tokens\n", encoding="utf-8")
        scaffold = protocol_package.scaffold_package(self.repo, self.manifest, "project", False)
        self.write_valid_entry()

        self.assertTrue(scaffold["errors"])
        self.assertEqual(scaffold["written"], [])

        result = protocol_package.validate_package(self.repo, self.manifest)

        self.assertFalse(result["ok"])
        self.assertIn(
            "frontend-design-tokens 存在多个可编辑真值源："
            "ai-agent-workspace/product/design/design-tokens.md, "
            "docs/03_DESIGN/design-tokens.md",
            result["content_errors"],
        )

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
