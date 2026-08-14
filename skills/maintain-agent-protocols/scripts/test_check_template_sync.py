from __future__ import annotations

import importlib.util
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


if __name__ == "__main__":
    unittest.main()
