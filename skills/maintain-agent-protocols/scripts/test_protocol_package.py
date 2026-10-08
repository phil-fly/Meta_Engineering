from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


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
            "# Agent Protocol\n\n"
            + protocol_package.make_entry_body("ai-agent-workspace/protocols", []),
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

    def test_minimal_scaffold_copies_issue_tracking_template(self) -> None:
        self.scaffold()

        issues = (
            self.repo
            / "ai-agent-workspace"
            / "protocols"
            / "templates"
            / "issues.md"
        )

        self.assertTrue(issues.is_file())
        issues_content = issues.read_text(encoding="utf-8")
        self.assertIn("# 问题清单", issues_content)
        self.assertIn("修复前必须达到 `planned`", issues_content)
        self.assertIn("### ISSUE-0001 标题", issues_content)

    def test_validate_rejects_missing_issue_tracking_template(self) -> None:
        self.scaffold()
        self.write_valid_entry()
        issues = (
            self.repo
            / "ai-agent-workspace"
            / "protocols"
            / "templates"
            / "issues.md"
        )
        issues.unlink()

        result = protocol_package.validate_package(self.repo, self.manifest)

        self.assertFalse(result["ok"])
        self.assertIn(
            "ai-agent-workspace/protocols/templates/issues.md",
            result["missing"],
        )

    def test_validate_rejects_incomplete_issue_tracking_template(self) -> None:
        self.scaffold()
        self.write_valid_entry()
        issues = (
            self.repo
            / "ai-agent-workspace"
            / "protocols"
            / "templates"
            / "issues.md"
        )
        issues.write_text("# 问题清单\n", encoding="utf-8")

        result = protocol_package.validate_package(self.repo, self.manifest)

        self.assertFalse(result["ok"])
        self.assertTrue(any("issues.md 缺少必备内容" in error for error in result["content_errors"]))

    def test_root_issue_ledger_is_reused_and_references_are_rewritten(self) -> None:
        source = SCRIPT_DIR.parent / "templates" / "issues.md"
        (self.repo / "issues.md").write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

        result = protocol_package.scaffold_package(
            self.repo, self.manifest, "minimal", False, False, True
        )

        self.assertEqual(result["errors"], [], result)
        self.assertFalse((self.repo / "ai-agent-workspace" / "issues.md").exists())
        troubleshooting = (
            self.repo
            / "ai-agent-workspace"
            / "protocols"
            / "playbooks"
            / "troubleshooting.md"
        ).read_text(encoding="utf-8")
        self.assertIn("`issues.md`", troubleshooting)
        self.assertTrue(result["validation"]["ok"], result)

    def test_parallel_issue_ledgers_stop_scaffold(self) -> None:
        source = SCRIPT_DIR.parent / "templates" / "issues.md"
        (self.repo / "issues.md").write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        default = self.repo / "ai-agent-workspace" / "issues.md"
        default.parent.mkdir(parents=True, exist_ok=True)
        default.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

        result = protocol_package.scaffold_package(self.repo, self.manifest, "minimal", False)

        self.assertTrue(result["errors"])
        self.assertTrue(any("真值源冲突" in error for error in result["errors"]))
        self.assertEqual(result["written"], [])

    def test_project_frontend_scaffold_copies_design_system_route_and_checklist(self) -> None:
        self.write_frontend_implementation()

        protocol_package.scaffold_package(self.repo, self.manifest, "project", False)

        package = self.repo / "ai-agent-workspace" / "protocols"
        route = package / "routes" / "frontend" / "design-system-maintenance.md"
        checklist = package / "checks" / "frontend-design-system-checklist.md"
        time_checklist = package / "checks" / "time-and-timezone-checklist.md"
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
        self.assertTrue(time_checklist.is_file())
        self.assertIn("CHK-TIME-009", time_checklist.read_text(encoding="utf-8"))
        self.assertTrue(prompt.is_file())
        self.assertFalse(design_tokens.exists())

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

    def test_typescript_ui_entry_selects_frontend_routes_without_design_tokens(self) -> None:
        source = self.repo / "src" / "main.ts"
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(
            "import { createApp } from 'vue';\ncreateApp({}).mount('#app');\n",
            encoding="utf-8",
        )

        plan = protocol_package.plan_package(self.repo, self.manifest, "project")

        targets = {item["target"] for item in plan["files"]}
        self.assertIn("frontend_implementation", plan["evidence"]["evidence_keys"])
        self.assertNotIn(
            "ai-agent-workspace/product/design/design-tokens.md",
            targets,
        )
        self.assertTrue(any(route["id"] == "frontend" for route in plan["selected_routes"]))

    def test_explicit_design_system_option_includes_design_tokens(self) -> None:
        self.write_frontend_implementation()
        plan = protocol_package.plan_package(self.repo, self.manifest, "project", True)
        targets = {item["target"] for item in plan["files"]}
        self.assertIn("ai-agent-workspace/product/design/design-tokens.md", targets)

    def test_explicit_design_system_without_frontend_evidence_does_not_plan_tokens(self) -> None:
        plan = protocol_package.plan_package(self.repo, self.manifest, "project", True)
        targets = {item["target"] for item in plan["files"]}
        self.assertNotIn("ai-agent-workspace/product/design/design-tokens.md", targets)

    def test_validate_rejects_default_when_both_protocol_directories_have_assets(self) -> None:
        self.scaffold()
        compat = self.repo / "ai-agent-protocols"
        compat.mkdir(parents=True)
        (compat / "README.md").write_text("# Compatibility package\n", encoding="utf-8")
        self.write_valid_entry()

        result = protocol_package.validate_package(self.repo, self.manifest)

        self.assertFalse(result["ok"])
        self.assertTrue(any("双" in error for error in result["content_errors"]))

    def test_validate_allows_explicit_protocol_directory_selection(self) -> None:
        self.scaffold()
        compat = self.repo / "ai-agent-protocols"
        compat.mkdir(parents=True)
        (compat / "README.md").write_text("# Compatibility package\n", encoding="utf-8")
        self.write_valid_entry()

        result = protocol_package.validate_package(self.repo, self.manifest, "ai-agent-workspace/protocols")

        self.assertTrue(result["ok"], result)
        self.assertTrue(any("已显式选择协议真值源" in warning for warning in result["warnings"]))

    def test_validate_rejects_package_directory_outside_manifest_without_mutation(self) -> None:
        outside = self.repo.parent / f"outside-protocols-{self.repo.name}"
        outside.mkdir()
        state_path = outside / "protocol-package-state.json"
        original = '{"sentinel": "unchanged"}\n'
        state_path.write_text(original, encoding="utf-8")

        result = protocol_package.validate_package(
            self.repo, self.manifest, "../outside-protocols"
        )

        self.assertFalse(result["ok"])
        self.assertTrue(any(
            "manifest" in error and "package_dir" in error
            for error in result["content_errors"]
        ))
        self.assertEqual(state_path.read_text(encoding="utf-8"), original)

    def test_validate_rejects_unknown_and_duplicate_route_rows(self) -> None:
        self.write_frontend_implementation()
        protocol_package.scaffold_package(self.repo, self.manifest, "project", False)
        self.write_valid_entry()
        route_index = self.repo / "ai-agent-workspace" / "protocols" / "routes" / "index.md"
        content = route_index.read_text(encoding="utf-8")
        row = next(line for line in content.splitlines() if line.startswith("| 项目证据支持 |"))
        route_index.write_text(content + row + "\n| 项目证据支持 | `routes/mystery/` | 当前仓库证据支持 | 0.85 | 无 |\n", encoding="utf-8")

        result = protocol_package.validate_package(self.repo, self.manifest)

        self.assertFalse(result["ok"])
        self.assertTrue(any("重复路由" in error for error in result["content_errors"]))
        self.assertTrue(any("未知路由" in error for error in result["content_errors"]))

    def test_validate_rejects_project_route_forged_as_full_coverage(self) -> None:
        self.write_frontend_implementation()
        protocol_package.scaffold_package(self.repo, self.manifest, "project", False)
        self.write_valid_entry()
        route_index = self.repo / "ai-agent-workspace" / "protocols" / "routes" / "index.md"
        route_index.write_text(route_index.read_text(encoding="utf-8").replace("| 项目证据支持 |", "| 完整覆盖 |", 1), encoding="utf-8")

        result = protocol_package.validate_package(self.repo, self.manifest)

        self.assertFalse(result["ok"])
        self.assertTrue(any("只有 full 模式" in error for error in result["content_errors"]))

    def test_validate_does_not_create_missing_state_file(self) -> None:
        self.scaffold()
        self.write_valid_entry()
        state_path = self.repo / "ai-agent-workspace" / "protocols" / "protocol-package-state.json"
        state_path.unlink()

        result = protocol_package.validate_package(self.repo, self.manifest)

        self.assertFalse(result["ok"])
        self.assertFalse(state_path.exists())

    def test_validate_rejects_planned_state_without_generate(self) -> None:
        self.scaffold()
        self.write_valid_entry()
        state_path = self.repo / "ai-agent-workspace" / "protocols" / "protocol-package-state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["status"] = "planned"
        state["completed"] = ["classify", "collect", "decide"]
        state_path.write_text(json.dumps(state), encoding="utf-8")

        result = protocol_package.validate_package(self.repo, self.manifest)

        self.assertFalse(result["ok"])
        self.assertTrue(any("完成 generate 阶段" in error for error in result["content_errors"]))
        persisted = json.loads(state_path.read_text(encoding="utf-8"))
        self.assertEqual(persisted["status"], "invalid")
        self.assertEqual(persisted["completed"], protocol_package.CHECKPOINT_PHASES)

    def test_frontend_plan_reuses_existing_legacy_design_tokens(self) -> None:
        self.write_frontend_implementation()
        legacy = self.repo / "docs" / "03_DESIGN" / "design-tokens.md"
        legacy.parent.mkdir(parents=True, exist_ok=True)
        template = SCRIPT_DIR.parent / "templates" / "design-tokens.md"
        content = self.backfill_design_tokens(template.read_text(encoding="utf-8"))
        legacy.write_text(content, encoding="utf-8")

        plan = protocol_package.plan_package(self.repo, self.manifest, "project", True)
        original_content = legacy.read_text(encoding="utf-8")
        result = protocol_package.scaffold_package(self.repo, self.manifest, "project", True, True)

        artifact = next(item for item in plan["files"] if item["kind"] == "conditional-artifact")
        self.assertEqual(artifact["target"], "docs/03_DESIGN/design-tokens.md")
        self.assertEqual(artifact["action"], "maintain-and-verify")
        self.assertEqual(legacy.read_text(encoding="utf-8"), original_content)
        self.assertIn(legacy.as_posix(), result["skipped"])

    def test_validate_requires_backfilled_design_tokens_for_frontend(self) -> None:
        self.write_frontend_implementation()
        protocol_package.scaffold_package(self.repo, self.manifest, "project", False, True)
        self.write_valid_entry()

        result = protocol_package.validate_package(self.repo, self.manifest, design_system=True)

        self.assertFalse(result["ok"])
        self.assertIn(
            "ai-agent-workspace/product/design/design-tokens.md "
            "仍包含待回填标记：初始化状态：待回填",
            result["content_errors"],
        )

    def test_validate_accepts_backfilled_design_tokens_for_frontend(self) -> None:
        self.write_frontend_implementation()
        protocol_package.scaffold_package(self.repo, self.manifest, "project", False, True)
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

        result = protocol_package.validate_package(self.repo, self.manifest, design_system=True)

        self.assertTrue(result["ok"], result)
        self.assertEqual(result["content_errors"], [])

    def test_validate_rejects_design_tokens_with_pending_document_status(self) -> None:
        self.write_frontend_implementation()
        protocol_package.scaffold_package(self.repo, self.manifest, "project", False, True)
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

        result = protocol_package.validate_package(self.repo, self.manifest, design_system=True)

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
        scaffold = protocol_package.scaffold_package(self.repo, self.manifest, "project", False, True)
        self.write_valid_entry()

        self.assertTrue(scaffold["errors"])
        self.assertEqual(scaffold["written"], [])

        result = protocol_package.validate_package(self.repo, self.manifest, design_system=True)

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

    def test_detect_excludes_skill_material_from_project_evidence(self) -> None:
        skill_doc = self.repo / "skills" / "maintain-agent-protocols" / "references" / "security.md"
        skill_doc.parent.mkdir(parents=True, exist_ok=True)
        skill_doc.write_text("auth router database security performance gateway\n", encoding="utf-8")
        business_source = self.repo / "skills" / "app" / "main.py"
        business_source.parent.mkdir(parents=True, exist_ok=True)
        business_source.write_text("print('business app')\n", encoding="utf-8")

        detection = protocol_package.detect_repo(self.repo)

        self.assertNotIn("skills", detection["summary"]["excluded_prefixes"])
        self.assertIn("skills/app/main.py", detection["evidence_quality"]["python"]["glob_hits"])
        self.assertLess(detection["evidence_quality"]["auth"]["confidence"], 0.5)

    def test_documentation_keyword_is_counter_evidence_not_route_support(self) -> None:
        (self.repo / "README.md").write_text(
            "This document discusses auth, router, performance and security patterns.\n",
            encoding="utf-8",
        )

        plan = protocol_package.plan_package(self.repo, self.manifest, "project")

        self.assertFalse(plan["selected_routes"])
        self.assertLess(plan["evidence_quality"]["auth"]["confidence"], 0.5)
        self.assertTrue(plan["evidence_quality"]["auth"]["counter_evidence"])

    def test_single_implementation_keyword_is_signal_not_route_support(self) -> None:
        source = self.repo / "scripts" / "validate.py"
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text("label = 'stable version token'\n", encoding="utf-8")

        plan = protocol_package.plan_package(self.repo, self.manifest, "project")

        route_ids = {route["id"] for route in plan["selected_routes"]}
        security = plan["evidence_quality"]["security"]
        self.assertNotIn("security", route_ids)
        self.assertEqual(security["implementation_samples"], ["scripts/validate.py"])
        self.assertEqual(security["confidence"], 0.4)
        self.assertEqual(security["min_content_samples"], 2)
        self.assertTrue(any("内容命中数不足" in item for item in security["counter_evidence"]))

    def test_independent_implementation_keyword_samples_support_route(self) -> None:
        first = self.repo / "src" / "auth.py"
        second = self.repo / "src" / "secrets.py"
        first.parent.mkdir(parents=True, exist_ok=True)
        first.write_text("credential = request.headers.get('token')\n", encoding="utf-8")
        second.write_text("secret = load_value()\n", encoding="utf-8")

        plan = protocol_package.plan_package(self.repo, self.manifest, "project")

        route_ids = {route["id"] for route in plan["selected_routes"]}
        security = plan["evidence_quality"]["security"]
        self.assertIn("security", route_ids)
        self.assertEqual(security["confidence"], 0.65)
        self.assertEqual(security["min_content_samples"], 2)
        self.assertEqual(len(security["implementation_samples"]), 2)

    def test_detects_root_level_implementation_and_skills_business_source(self) -> None:
        (self.repo / "main.py").write_text("print('app')\n", encoding="utf-8")
        (self.repo / "App.tsx").write_text("export function App() { return null; }\n", encoding="utf-8")
        business = self.repo / "skills" / "app" / "main.py"
        business.parent.mkdir(parents=True, exist_ok=True)
        business.write_text("print('business')\n", encoding="utf-8")

        detection = protocol_package.detect_repo(self.repo)

        self.assertIn("main.py", detection["evidence_quality"]["python"]["glob_hits"])
        self.assertIn("skills/app/main.py", detection["evidence_quality"]["python"]["glob_hits"])
        self.assertIn("App.tsx", detection["evidence_quality"]["frontend_implementation"]["glob_hits"])

    def test_test_hit_limit_does_not_hide_production_implementation(self) -> None:
        tests = self.repo / "tests"
        tests.mkdir()
        for index in range(12):
            (tests / f"test_{index:02d}.py").write_text(
                "print('test')\n", encoding="utf-8"
            )
        source = self.repo / "src" / "main.py"
        source.parent.mkdir()
        source.write_text("print('production')\n", encoding="utf-8")

        plan = protocol_package.plan_package(self.repo, self.manifest, "project")

        python = plan["evidence_quality"]["python"]
        self.assertIn("src/main.py", python["implementation_samples"])
        self.assertIn("backend-python", {route["id"] for route in plan["selected_routes"]})

    def test_project_frontend_keeps_support_assets_out_of_route_selection(self) -> None:
        self.write_frontend_implementation()
        plan = protocol_package.plan_package(self.repo, self.manifest, "project")

        route_ids = {route["id"] for route in plan["selected_routes"]}
        targets = {item["target"] for item in plan["files"]}
        self.assertEqual(route_ids, {"frontend"})
        self.assertIn(
            "ai-agent-workspace/protocols/checks/time-and-timezone-checklist.md",
            targets,
        )
        self.assertTrue(any(item["kind"] == "support_asset" for item in plan["files"]))
        self.assertTrue(all(
            max((q.get("confidence", 0.0) for q in route["evidence_quality"].values()), default=0.0) < 1.0
            for route in plan["selected_routes"]
        ))

    def test_frontend_bare_markdown_references_are_copied_and_rewritten(self) -> None:
        self.write_frontend_implementation()

        result = protocol_package.scaffold_package(
            self.repo, self.manifest, "project", False
        )

        self.assertEqual(result["errors"], [], result)
        package = self.repo / "ai-agent-workspace" / "protocols"
        route = package / "routes" / "frontend" / "javascript-typescript.md"
        content = route.read_text(encoding="utf-8")
        for name in (
            "api-and-data.md",
            "interaction-and-permission.md",
            "state-and-cache.md",
            "tooling-and-verification.md",
        ):
            support = package / "support" / "engineering" / "frontend" / name
            self.assertTrue(support.is_file(), name)
            self.assertIn(f"../../support/engineering/frontend/{name}", content)

    def test_validate_rejects_missing_rewritten_bare_reference_target(self) -> None:
        self.write_frontend_implementation()
        scaffold = protocol_package.scaffold_package(
            self.repo, self.manifest, "project", False, False, True
        )
        self.assertEqual(scaffold["errors"], [], scaffold)
        missing = (
            self.repo
            / "ai-agent-workspace"
            / "protocols"
            / "support"
            / "engineering"
            / "frontend"
            / "api-and-data.md"
        )
        missing.unlink()

        result = protocol_package.validate_package(self.repo, self.manifest)

        self.assertFalse(result["ok"])
        self.assertTrue(any("api-and-data.md" in error for error in result["content_errors"]))

    def test_backend_cross_domain_bare_references_are_copied_and_rewritten(self) -> None:
        (self.repo / "go.mod").write_text("module example.com/app\n", encoding="utf-8")

        result = protocol_package.scaffold_package(
            self.repo, self.manifest, "project", False, False, True
        )

        self.assertEqual(result["errors"], [], result)
        package = self.repo / "ai-agent-workspace" / "protocols"
        architecture = package / "routes" / "backend" / "go" / "architecture.md"
        content = architecture.read_text(encoding="utf-8")
        self.assertIn("../../../support/engineering/core/api-design.md", content)
        self.assertTrue(
            (package / "support" / "engineering" / "core" / "api-design.md").is_file()
        )
        self.assertTrue(result["validation"]["ok"], result)

    def test_frontend_always_include_is_a_real_pruning_contract(self) -> None:
        self.write_frontend_implementation()
        plan = protocol_package.plan_package(self.repo, self.manifest, "project")
        route_files = {
            item["source"] for item in plan["files"] if item["kind"] == "route"
        }
        self.assertEqual(
            route_files,
            {
                "references/engineering/frontend/index.md",
                "references/engineering/frontend/javascript-typescript.md",
                "references/engineering/frontend/design-system-maintenance.md",
            },
        )

    def test_validate_persists_validate_checkpoint(self) -> None:
        self.scaffold()
        self.write_valid_entry()
        result = protocol_package.validate_package(self.repo, self.manifest)
        state = json.loads(
            (self.repo / "ai-agent-workspace" / "protocols" / "protocol-package-state.json").read_text()
        )
        self.assertTrue(result["ok"])
        self.assertIn("validate", state["completed"])
        self.assertEqual(state["status"], "validated")

    def test_validate_rejects_invalid_checkpoint_status(self) -> None:
        self.scaffold()
        self.write_valid_entry()
        state_path = self.repo / "ai-agent-workspace" / "protocols" / "protocol-package-state.json"
        state = json.loads(state_path.read_text())
        state["status"] = "pretend"
        state_path.write_text(json.dumps(state), encoding="utf-8")
        result = protocol_package.validate_package(self.repo, self.manifest)
        self.assertFalse(result["ok"])
        self.assertTrue(any("status 无效" in error for error in result["content_errors"]))

    def test_validate_rejects_hollow_checkpoint_contract(self) -> None:
        self.scaffold()
        self.write_valid_entry()
        state_path = self.repo / "ai-agent-workspace" / "protocols" / "protocol-package-state.json"
        original = json.loads(state_path.read_text())

        for field in ("mode", "package_dir", "entry"):
            with self.subTest(field=field):
                state = dict(original)
                state.pop(field)
                state_path.write_text(json.dumps(state), encoding="utf-8")
                result = protocol_package.validate_package(self.repo, self.manifest)
                self.assertFalse(result["ok"])
                self.assertTrue(any(field in error for error in result["content_errors"]))

    def test_validate_rejects_invalid_checkpoint_mode_and_patch_status(self) -> None:
        self.scaffold()
        self.write_valid_entry()
        state_path = self.repo / "ai-agent-workspace" / "protocols" / "protocol-package-state.json"
        original = json.loads(state_path.read_text())

        for field, value in (("mode", "pretend"), ("entry_patch_status", "magic")):
            with self.subTest(field=field):
                state = dict(original)
                state[field] = value
                state_path.write_text(json.dumps(state), encoding="utf-8")
                result = protocol_package.validate_package(self.repo, self.manifest)
                self.assertFalse(result["ok"])
                self.assertTrue(any(field in error for error in result["content_errors"]))

    def test_validate_rejects_undeclared_design_tokens_reference(self) -> None:
        self.scaffold()
        self.write_valid_entry()
        route = self.repo / "ai-agent-workspace" / "protocols" / "playbooks" / "coding.md"
        route.write_text("# WF-CODING\n\n[ghost](ghost/design-tokens.md)\n", encoding="utf-8")
        result = protocol_package.validate_package(self.repo, self.manifest)
        self.assertFalse(result["ok"])
        self.assertTrue(any("ghost/design-tokens.md" in error for error in result["content_errors"]))

    def test_scaffold_apply_entry_runs_validation(self) -> None:
        result = protocol_package.scaffold_package(self.repo, self.manifest, "minimal", False, False, True)
        self.assertTrue(result["entry_applied"])
        self.assertTrue(result["entry_apply_attempted"])
        self.assertFalse(result["entry_rolled_back"])
        self.assertIsNotNone(result["validation"])
        self.assertTrue(result["validation"]["ok"], result)

    def test_apply_entry_failure_restores_existing_entry(self) -> None:
        entry = self.repo / "AGENTS.md"
        original = "# Existing protocol\n"
        entry.write_text(original, encoding="utf-8")
        with mock.patch.object(
            protocol_package, "validate_package", return_value={"ok": False}
        ):
            result = protocol_package.scaffold_package(
                self.repo, self.manifest, "minimal", False, False, True
            )

        self.assertEqual(entry.read_text(encoding="utf-8"), original)
        self.assertTrue(result["entry_apply_attempted"])
        self.assertFalse(result["entry_applied"])
        self.assertTrue(result["entry_rolled_back"])

    def test_apply_entry_failure_removes_new_entry(self) -> None:
        entry = self.repo / "AGENTS.md"
        with mock.patch.object(
            protocol_package, "validate_package", return_value={"ok": False}
        ):
            result = protocol_package.scaffold_package(
                self.repo, self.manifest, "minimal", False, False, True
            )

        self.assertFalse(entry.exists())
        self.assertTrue(result["entry_apply_attempted"])
        self.assertFalse(result["entry_applied"])
        self.assertTrue(result["entry_rolled_back"])

    def test_entry_patch_rejects_header_empty_marker_and_old_package_path(self) -> None:
        entry = self.repo / "AGENTS.md"
        cases = {
            "header-only": "## AI Agent Protocol Package\n",
            "empty-marker": (
                f"{protocol_package.ENTRY_MARKER_START}\n"
                f"{protocol_package.ENTRY_MARKER_END}\n"
            ),
            "old-path": protocol_package.make_entry_body("old/protocols", []),
        }
        for name, content in cases.items():
            with self.subTest(name=name):
                entry.write_text(content, encoding="utf-8")
                plan = protocol_package.plan_package(self.repo, self.manifest, "minimal")
                self.assertNotEqual(plan["entry_patch"]["status"], "already-wired")
                self.assertTrue(plan["entry_patch"]["apply"])

    def test_validate_rejects_noncanonical_entry_marker(self) -> None:
        self.scaffold()
        (self.repo / "AGENTS.md").write_text(
            "## AI Agent Protocol Package\n\nThis is unrelated.\n",
            encoding="utf-8",
        )

        result = protocol_package.validate_package(self.repo, self.manifest)

        self.assertFalse(result["ok"])
        self.assertTrue(any("marker block" in error for error in result["entry_errors"]))

    def test_support_asset_budget_warning_blocks_scaffold(self) -> None:
        self.write_frontend_implementation()
        with mock.patch.object(protocol_package, "SUPPORT_ASSET_MAX_FILES", 0):
            plan = protocol_package.plan_package(self.repo, self.manifest, "project")
            result = protocol_package.scaffold_package(
                self.repo, self.manifest, "project", False
            )

        self.assertTrue(plan["warnings"])
        self.assertTrue(any("file budget exceeded" in warning for warning in plan["warnings"]))
        self.assertTrue(result["errors"])
        self.assertEqual(result["written"], [])

    def test_support_asset_closure_runs_once_for_the_whole_package(self) -> None:
        with mock.patch.object(
            protocol_package,
            "support_assets_for_routes",
            wraps=protocol_package.support_assets_for_routes,
        ) as closure:
            plan = protocol_package.plan_package(self.repo, self.manifest, "full")

        self.assertEqual(closure.call_count, 1)
        route_sources = {
            item["source"] for item in plan["files"] if item["kind"] == "route"
        }
        support_sources = [
            item["source"] for item in plan["files"] if item["kind"] == "support_asset"
        ]
        self.assertTrue(route_sources.isdisjoint(support_sources))
        self.assertEqual(len(support_sources), len(set(support_sources)))

    def test_full_mode_selection_does_not_claim_direct_project_evidence(self) -> None:
        plan = protocol_package.plan_package(self.repo, self.manifest, "full")

        self.assertTrue(plan["selected_routes"])
        for route in plan["selected_routes"]:
            with self.subTest(route=route["id"]):
                self.assertEqual(route["status"], "完整覆盖")
                self.assertEqual(route["decision"], "full-coverage")
                self.assertFalse(route["evidence_complete"])
                self.assertEqual(route["evidence_quality"], {})

        result = protocol_package.scaffold_package(
            self.repo, self.manifest, "full", False, False, True
        )
        self.assertEqual(result["errors"], [], result)
        route_index = (
            self.repo / "ai-agent-workspace" / "protocols" / "routes" / "index.md"
        ).read_text(encoding="utf-8")
        self.assertIn("| 完整覆盖 |", route_index)
        self.assertIn("当前仓库无直接证据 | 0.00 |", route_index)

    def test_route_index_persists_generated_and_ungenerated_read_dependencies(self) -> None:
        self.write_frontend_implementation()
        backend = self.repo / "server.py"
        worker = self.repo / "worker.py"
        backend.write_text(
            "router = 'api'; permission = 'token'; cache = 'performance'\n",
            encoding="utf-8",
        )
        worker.write_text(
            "endpoint = 'rest'; credential = 'secret'; latency = 'performance'\n",
            encoding="utf-8",
        )
        result = protocol_package.scaffold_package(
            self.repo, self.manifest, "project", False
        )
        self.assertEqual(result["errors"], [], result)
        route_index = (
            self.repo / "ai-agent-workspace" / "protocols" / "routes" / "index.md"
        ).read_text(encoding="utf-8")

        self.assertIn("[core](core/index.md)", route_index)
        self.assertIn("[security](security/index.md)", route_index)
        self.assertIn("[performance](performance/index.md)", route_index)
        self.assertIn("platform（源规则依赖未落盘）", route_index)
        package = self.repo / "ai-agent-workspace" / "protocols"
        self.assertTrue((package / "routes" / "core" / "time-and-timezone.md").is_file())
        time_check = package / "checks" / "time-and-timezone-checklist.md"
        self.assertTrue(time_check.is_file())
        self.assertIn("CHK-TIME-009", time_check.read_text(encoding="utf-8"))

    def test_route_index_validator_rejects_dependency_mismatch(self) -> None:
        self.write_frontend_implementation()
        scaffold = protocol_package.scaffold_package(
            self.repo, self.manifest, "project", False, False, True
        )
        self.assertEqual(scaffold["errors"], [], scaffold)
        route_index = self.repo / "ai-agent-workspace" / "protocols" / "routes" / "index.md"
        content = route_index.read_text(encoding="utf-8").replace(
            "core（源规则依赖未落盘）", "[core](core/index.md)"
        )
        route_index.write_text(content, encoding="utf-8")

        result = protocol_package.validate_package(self.repo, self.manifest)

        self.assertFalse(result["ok"])
        self.assertTrue(any(
            "阅读依赖" in error and "core" in error
            for error in result["content_errors"]
        ))

    def test_plan_exposes_reviewable_entry_patch_and_checkpoints(self) -> None:
        plan = protocol_package.plan_package(self.repo, self.manifest, "minimal")

        self.assertEqual(plan["entry_patch"]["status"], "patch-required")
        self.assertIn("AI Agent Protocol Package", plan["entry_patch"]["diff"])
        self.assertIn(protocol_package.ENTRY_MARKER_START, plan["entry_patch"]["diff"])
        self.assertEqual(plan["checkpoint_state"]["status"], "planned")
        self.assertEqual(plan["checkpoint_state"]["completed"], ["classify", "collect", "decide"])

    def test_validate_checks_generated_package_markdown_references(self) -> None:
        self.scaffold()
        self.write_valid_entry()
        broken = self.repo / "ai-agent-workspace" / "protocols" / "playbooks" / "coding.md"
        broken.write_text(
            "# WF-CODING\n\n读取 `../routes/missing.md`。\n",
            encoding="utf-8",
        )

        result = protocol_package.validate_package(self.repo, self.manifest)

        self.assertFalse(result["ok"])
        self.assertIn(
            "playbooks/coding.md 引用不存在：../routes/missing.md",
            result["content_errors"],
        )

    def test_validate_rejects_explicit_bare_markdown_link(self) -> None:
        self.scaffold()
        self.write_valid_entry()
        broken = self.repo / "ai-agent-workspace" / "protocols" / "playbooks" / "coding.md"
        broken.write_text(
            "# WF-CODING\n\n[missing](missing.md)\n",
            encoding="utf-8",
        )

        result = protocol_package.validate_package(self.repo, self.manifest)

        self.assertFalse(result["ok"])
        self.assertIn(
            "playbooks/coding.md 引用不存在：missing.md",
            result["content_errors"],
        )


class TaskGovernanceBehaviorTests(unittest.TestCase):
    def test_ten_required_scenarios_have_enforceable_contracts(self) -> None:
        read = lambda path: (SCRIPT_DIR.parent / path).read_text(encoding="utf-8")
        playbooks = read("references/scenarios/playbooks.md")
        collaboration = read("references/protocol/collaboration-boundaries.md")
        frontend = read("references/engineering/frontend/design-system-maintenance.md")
        scenarios = [
            ("01 rename", playbooks, ("A | 低复杂度 + 低风险", "最小修改 → 局部验证 → Completion → Stop")),
            ("02 blue button", frontend, ("普通页面、按钮、文案或局部样式修改不触发", "`design-tokens.md` 缺失也不触发")),
            ("03 delete data", playbooks, ("B | 低复杂度 + 高风险", "不可逆或授权不清时确认")),
            ("04 Go refactor", playbooks, ("C | 高复杂度 + 低风险", "影响分析 → 分阶段实施 → 回归验证")),
            ("05 auth redesign", playbooks, ("D | 高复杂度 + 高风险", "方案与证据 → Confirmation → 分阶段实施 → 高强度验证")),
            ("06 API 500", playbooks, ("静态检查完成不能替代结果验证", "必须验证用户可观察结果")),
            ("07 inspect", collaboration, ("讨论或审查请求保持只读",)),
            ("08 protocol sentence", collaboration, ("局部、可逆、低风险编辑直接执行", "不因文件名或“协议”类别自动确认")),
            ("09 related optimization", playbooks, ("相关但不阻塞的优化只记录或提示，不自动修改",)),
            ("10 simplify", playbooks, ("用户明确目标、范围、非目标与授权", "不加载未命中的治理流程")),
        ]
        self.assertEqual(len(scenarios), 10)
        for name, contract, clauses in scenarios:
            with self.subTest(name=name):
                for clause in clauses:
                    self.assertIn(clause, contract)


if __name__ == "__main__":
    unittest.main()
