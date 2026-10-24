from __future__ import annotations

import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
CONTRACTS_MD = SKILL_ROOT / "references" / "workflow-contracts.md"
SHARED_PROTOCOL = SKILL_ROOT / "references" / "shared" / "interactive-decision-protocol.md"
ROOT_PROTOCOL = SKILL_ROOT.parents[1] / "references" / "interactive-decision-protocol.md"

SOLICIT_MARKER = "作为本轮产出物索取"
MENTION_COUNTEREXAMPLE = "PRD 该怎么写"
LIGHT_MARKER = "仅提及交付物名词"
KEYWORD_CRITERION = "是否提到"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def decision_block(text: str) -> str:
    """截取场景 5 的决策依据块，用于比对根级真值源与安装态投影。"""
    start = text.index("#### 场景 5: 协作强度选择")
    marker = text.index("**决策依据**：", start)
    end = text.index("\n\n", marker)
    return text[marker:end]


def contract_row(text: str, mode: str) -> str:
    for line in text.splitlines():
        if line.startswith(f"| {mode} |"):
            return line
    raise AssertionError(f"未找到协作强度表中的 {mode} 行")


class CollaborationModeContractTests(unittest.TestCase):
    """协作强度判据必须在 SKILL.md 与 workflow-contracts.md 保持一致。"""

    def test_both_sources_use_solicitation_not_mention(self) -> None:
        skill = read(SKILL_MD)
        contracts = read(CONTRACTS_MD)
        self.assertIn(SOLICIT_MARKER, skill)
        self.assertIn(SOLICIT_MARKER, contract_row(contracts, "产物沉淀"))

    def test_mention_only_request_stays_lightweight(self) -> None:
        skill = read(SKILL_MD)
        contracts = read(CONTRACTS_MD)
        self.assertIn(MENTION_COUNTEREXAMPLE, skill)
        self.assertIn(LIGHT_MARKER, skill)
        self.assertIn(LIGHT_MARKER, contract_row(contracts, "轻量讨论"))

    def test_judgement_order_checks_solicitation_first(self) -> None:
        skill = read(SKILL_MD)
        order = "先看是否把交付物作为本轮产出物索取"
        self.assertIn(order, skill)
        self.assertLess(
            skill.index(order),
            skill.index("最后才看是否要求落盘"),
            "判定顺序必须先把交付物索取放在落盘之前",
        )

    def test_no_stale_mention_only_wording(self) -> None:
        skill = read(SKILL_MD)
        contracts = read(CONTRACTS_MD)
        for text, name in ((skill, "SKILL.md"), (contracts, "workflow-contracts.md")):
            self.assertNotIn(
                "且未点名交付物",
                text,
                f"{name} 仍残留只看名词的旧判据",
            )
            self.assertNotIn(
                "点名 PRD",
                text,
                f"{name} 仍残留只看名词的旧判据",
            )


class SharedProtocolContractTests(unittest.TestCase):
    """场景 5 是首次交互的运行时资产，判据必须与主路径同口径。"""

    def test_shared_projection_uses_solicitation_criterion(self) -> None:
        projection = read(SHARED_PROTOCOL)
        self.assertIn(SOLICIT_MARKER, decision_block(projection))
        self.assertNotIn(
            KEYWORD_CRITERION,
            projection,
            "共享协议投影仍残留只看关键词的旧判据",
        )

    def test_root_protocol_uses_solicitation_criterion(self) -> None:
        if not ROOT_PROTOCOL.is_file():
            self.skipTest("独立安装态无根级真值源，投影已单独断言")
        root = read(ROOT_PROTOCOL)
        self.assertIn(SOLICIT_MARKER, decision_block(root))
        self.assertNotIn(
            KEYWORD_CRITERION,
            root,
            "根级真值源仍残留只看关键词的旧判据",
        )

    def test_root_and_projection_decision_blocks_match(self) -> None:
        if not ROOT_PROTOCOL.is_file():
            self.skipTest("独立安装态无根级真值源，投影已单独断言")
        self.assertEqual(
            decision_block(read(ROOT_PROTOCOL)),
            decision_block(read(SHARED_PROTOCOL)),
            "场景 5 的决策依据必须与根级真值源一致",
        )


if __name__ == "__main__":
    unittest.main()
