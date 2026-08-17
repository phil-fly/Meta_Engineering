from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
MODULE_PATH = SCRIPT_DIR / "check-template-sync.py"
SPEC = importlib.util.spec_from_file_location("check_template_sync", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Cannot load {MODULE_PATH}")
check_template_sync = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = check_template_sync
SPEC.loader.exec_module(check_template_sync)


class InteractiveRuntimeTests(unittest.TestCase):
    def test_installed_runtime_requires_all_headings_without_source_repo(self) -> None:
        issues = check_template_sync.validate_interactive_runtime("# 交互式决策协议\n")

        self.assertIn("missing runtime heading: ## 设计原则", issues)
        self.assertIn("missing runtime heading: ## 用户体验目标", issues)


class FrontendReviewPromptTests(unittest.TestCase):
    def test_rejects_compressed_prompt_without_required_review_dimensions(self) -> None:
        issues = check_template_sync.validate_frontend_review_prompt(
            "# Frontend Design System Review Prompt\n"
        )

        self.assertIn("missing frontend review marker: ### 4.1 Color", issues)
        self.assertIn("missing frontend review marker: ## 8. Responsive 与真实运行行为", issues)
        self.assertIn("missing frontend review marker: ## 14. 完成门", issues)

    def test_current_prompt_preserves_all_required_review_dimensions(self) -> None:
        prompt = (
            SCRIPT_DIR.parent / "templates" / "frontend-design-system-review-prompt.md"
        ).read_text(encoding="utf-8")

        self.assertEqual(check_template_sync.validate_frontend_review_prompt(prompt), [])


class DesignTokensTemplateTests(unittest.TestCase):
    def test_rejects_design_tokens_template_without_required_details(self) -> None:
        issues = check_template_sync.validate_design_tokens_template("# Design Tokens\n")

        self.assertIn(
            "missing design tokens marker: ## 2. 真值源关系",
            issues,
        )
        self.assertIn(
            "missing design tokens marker: ## 15. Component Tokens",
            issues,
        )
        self.assertIn(
            "missing design tokens marker: ## 18. Maintenance Contract",
            issues,
        )

    def test_current_design_tokens_template_preserves_required_details(self) -> None:
        template = (
            SCRIPT_DIR.parent / "templates" / "design-tokens.md"
        ).read_text(encoding="utf-8")

        self.assertEqual(check_template_sync.validate_design_tokens_template(template), [])

    def test_manifest_and_template_validator_require_the_same_design_token_sections(self) -> None:
        manifest = json.loads(
            (SCRIPT_DIR / "protocol-package-manifest.json").read_text(encoding="utf-8")
        )
        artifact = next(
            item
            for item in manifest["conditional_artifacts"]
            if item["id"] == "frontend-design-tokens"
        )

        self.assertEqual(
            set(artifact["required_markers"]),
            set(check_template_sync.DESIGN_TOKENS_REQUIRED_MARKERS) - {"初始化状态：待回填"},
        )
        template = (
            SCRIPT_DIR.parent / "templates" / "design-tokens.md"
        ).read_text(encoding="utf-8")
        self.assertTrue(all(marker in template for marker in artifact["incomplete_markers"]))


if __name__ == "__main__":
    unittest.main()
