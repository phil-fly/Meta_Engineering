#!/usr/bin/env python3
"""Check packaged assets, reference templates, and shared runtime references."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"
MAINTAIN_ROOT = SKILLS_ROOT / "maintain-agent-protocols"
PRP_ROOT = SKILLS_ROOT / "product-requirements-partner"

PAIRS = [
    ("templates/user-protocol.md", "references/protocol/user-protocol-template.md"),
    ("templates/project-protocol.md", "references/protocol/project-protocol-template.md"),
    ("templates/route-card.md", "references/protocol/route-card-template.md"),
]

# Shared runtime assets ship with every skill that reads them at runtime, so each
# consuming skill carries its own copy of the cross-skill authoring truth source.
SHARED_COPY_PAIRS = [
    (
        MAINTAIN_ROOT / "references/shared/target-workspace-layout.md",
        REPO_ROOT / "references/target-workspace-layout.md",
    ),
    (
        PRP_ROOT / "references/shared/target-workspace-layout.md",
        REPO_ROOT / "references/target-workspace-layout.md",
    ),
]

INTERACTIVE_SOURCE = REPO_ROOT / "references/interactive-decision-protocol.md"
FRONTEND_REVIEW_PROMPT = "templates/frontend-design-system-review-prompt.md"
FRONTEND_REVIEW_REQUIRED_MARKERS = [
    "## 0. 执行边界与证据规则",
    "## 1. 调查目标",
    "## 2. 扫描项目结构与真实来源",
    "## 3. 建立规范来源地图",
    "### 4.1 Color",
    "### 4.2 Typography",
    "### 4.3 Spacing",
    "### 4.4 Radius",
    "### 4.5 Border 与 Shadow",
    "## 5. Layout / Grid",
    "## 6. Component 规范与状态",
    "## 7. Page Pattern",
    "## 8. Responsive 与真实运行行为",
    "## 9. Accessibility、Theme 与工程验证",
    "## 10. AI / Vibe Coding 机制",
    "## 11. 协议优先级、继承与演进",
    "## 12. 问题分析",
    "## 13. 最终报告",
    "## 14. 完成门",
    "已有实际值 / 仅语义规则 / 模板占位 / 分散实现 / 未发现 / 不适用",
    "Inherit、Override、Extend 和 Exception",
    "反证检查：none / mitigated / contradicted / scope_limited / unknown",
    "P0 数 + P1 数 + P2 数 == 已确认问题总数",
]
DESIGN_TOKENS_TEMPLATE = "templates/design-tokens.md"
DESIGN_TOKENS_REQUIRED_MARKERS = [
    "初始化状态：待回填",
    "## 1. 文档状态",
    "## 2. 真值源关系",
    "## 3. Color",
    "## 4. Typography",
    "## 5. Spacing",
    "## 6. Size And Density",
    "## 7. Radius",
    "## 8. Border",
    "## 9. Shadow And Elevation",
    "## 10. Layout And Grid",
    "## 11. Breakpoints And Responsive Behavior",
    "## 12. Z-index And Layering",
    "## 13. Motion",
    "## 14. Icons",
    "## 15. Component Tokens",
    "## 16. Theme And Brand Modes",
    "## 17. Exceptions And Debt",
    "## 18. Maintenance Contract",
    "## 19. Change Log",
]
INTERACTIVE_PROJECTIONS = [
    {
        "skill": "maintain-agent-protocols",
        "excluded_skill": "product-requirements-partner",
        "path": MAINTAIN_ROOT / "references/shared/interactive-decision-protocol.md",
        "required_headings": [
            "## 设计原则",
            "#### 场景 1: 模型入口文件选择",
            "#### 场景 2: 生成模式选择",
            "#### 场景 3: 真值源冲突解决",
            "#### 场景 4: 工程路由裁剪策略",
            "## 选项设计标准",
            "## 降级策略",
            "## 实施检查清单",
            "### maintain-agent-protocols",
            "## 用户体验目标",
        ],
        "blocks": [
            ("## 设计原则", "## 交互式场景清单", "## 交互式场景清单"),
            ("#### 场景 1: 模型入口文件选择", "#### 场景 2: 生成模式选择", "#### 场景 2: 生成模式选择"),
            ("#### 场景 2: 生成模式选择", "#### 场景 3: 真值源冲突解决", "#### 场景 3: 真值源冲突解决"),
            ("#### 场景 3: 真值源冲突解决", "#### 场景 4: 工程路由裁剪策略", "#### 场景 4: 工程路由裁剪策略"),
            ("#### 场景 4: 工程路由裁剪策略", "### product-requirements-partner", "## 选项设计标准"),
            ("## 选项设计标准", "## 降级策略", "## 降级策略"),
            ("## 降级策略", "## 实施检查清单", "## 实施检查清单"),
            ("## 实施检查清单", "## 与现有协议的集成", "## 与现有协议的集成"),
            ("## 用户体验目标", "---", "---"),
        ],
        "integration_source_end": "### product-requirements-partner",
        "integration_runtime_end": "## 用户体验目标",
    },
    {
        "skill": "product-requirements-partner",
        "excluded_skill": "maintain-agent-protocols",
        "path": PRP_ROOT / "references/shared/interactive-decision-protocol.md",
        "required_headings": [
            "## 设计原则",
            "#### 场景 5: 协作强度选择",
            "#### 场景 6: 目标目录选择",
            "#### 场景 7: Scene 跳转确认",
            "#### 场景 8: [Meta] 层级判断",
            "## 选项设计标准",
            "## 降级策略",
            "## 实施检查清单",
            "### product-requirements-partner",
            "## 用户体验目标",
        ],
        "blocks": [
            ("## 设计原则", "## 交互式场景清单", "## 交互式场景清单"),
            ("#### 场景 5: 协作强度选择", "#### 场景 6: 目标目录选择", "#### 场景 6: 目标目录选择"),
            ("#### 场景 6: 目标目录选择", "#### 场景 7: Scene 跳转确认", "#### 场景 7: Scene 跳转确认"),
            ("#### 场景 7: Scene 跳转确认", "#### 场景 8: [Meta] 层级判断", "#### 场景 8: [Meta] 层级判断"),
            ("#### 场景 8: [Meta] 层级判断", "## 选项设计标准", "## 选项设计标准"),
            ("## 选项设计标准", "## 降级策略", "## 降级策略"),
            ("## 降级策略", "## 实施检查清单", "## 实施检查清单"),
            ("## 实施检查清单", "## 与现有协议的集成", "## 与现有协议的集成"),
            ("## 用户体验目标", "---", "---"),
        ],
        "integration_source_end": "## 用户体验目标",
        "integration_runtime_end": "## 用户体验目标",
    },
]


def extract_block(content: str, start: str, end: str, offset: int = 0) -> str:
    start_index = content.index(start, offset)
    end_index = content.index(end, start_index + len(start))
    return content[start_index:end_index].strip()


def validate_interactive_runtime(
    runtime_content: str,
    source_content: str | None,
    projection: dict[str, object],
) -> list[str]:
    issues: list[str] = []
    required_headings: list[str] = projection["required_headings"]  # type: ignore[assignment]
    blocks: list[tuple[str, str, str]] = projection["blocks"]  # type: ignore[assignment]
    skill = projection["skill"]
    excluded_skill = projection["excluded_skill"]

    if excluded_skill in runtime_content:
        issues.append(f"must not depend on {excluded_skill}")

    for heading in required_headings:
        if heading not in runtime_content:
            issues.append(f"missing runtime heading: {heading}")

    if source_content is None:
        return issues

    for heading in required_headings:
        if heading not in source_content:
            issues.append(f"missing source heading: {heading}")

    try:
        for start, source_end, runtime_end in blocks:
            source_block = extract_block(source_content, start, source_end)
            runtime_block = extract_block(runtime_content, start, runtime_end)
            if source_block != runtime_block:
                issues.append(f"out-of-sync projection block: {start}")

        integration_heading = "## 与现有协议的集成"
        source_offset = source_content.index(integration_heading)
        runtime_offset = runtime_content.index(integration_heading)
        source_integration = extract_block(
            source_content,
            f"### {skill}",
            projection["integration_source_end"],  # type: ignore[arg-type]
            source_offset,
        )
        runtime_integration = extract_block(
            runtime_content,
            f"### {skill}",
            projection["integration_runtime_end"],  # type: ignore[arg-type]
            runtime_offset,
        )
        if source_integration != runtime_integration:
            issues.append(f"out-of-sync {skill} integration")
    except ValueError as error:
        issues.append(f"cannot parse projection: {error}")
    return issues


def validate_frontend_review_prompt(content: str) -> list[str]:
    return [
        f"missing frontend review marker: {marker}"
        for marker in FRONTEND_REVIEW_REQUIRED_MARKERS
        if marker not in content
    ]


def validate_design_tokens_template(content: str) -> list[str]:
    return [
        f"missing design tokens marker: {marker}"
        for marker in DESIGN_TOKENS_REQUIRED_MARKERS
        if marker not in content
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

    for packaged_path, authoring_path in SHARED_COPY_PAIRS:
        packaged_rel = packaged_path.relative_to(REPO_ROOT).as_posix()
        if not packaged_path.exists():
            missing.append(packaged_rel)
            continue

        if authoring_path.exists() and packaged_path.read_bytes() != authoring_path.read_bytes():
            mismatches.append((packaged_rel, authoring_path.relative_to(REPO_ROOT).as_posix()))

    source_content = (
        INTERACTIVE_SOURCE.read_text(encoding="utf-8") if INTERACTIVE_SOURCE.exists() else None
    )
    for projection in INTERACTIVE_PROJECTIONS:
        runtime_path: Path = projection["path"]  # type: ignore[assignment]
        runtime_rel = runtime_path.relative_to(REPO_ROOT).as_posix()
        if not runtime_path.exists():
            missing.append(runtime_rel)
            continue
        runtime_content = runtime_path.read_text(encoding="utf-8")
        for issue in validate_interactive_runtime(runtime_content, source_content, projection):
            mismatches.append((runtime_rel, issue))

    frontend_review_path = ROOT / FRONTEND_REVIEW_PROMPT
    if not frontend_review_path.exists():
        missing.append(FRONTEND_REVIEW_PROMPT)
    else:
        frontend_review_content = frontend_review_path.read_text(encoding="utf-8")
        for issue in validate_frontend_review_prompt(frontend_review_content):
            mismatches.append((FRONTEND_REVIEW_PROMPT, issue))

    design_tokens_path = ROOT / DESIGN_TOKENS_TEMPLATE
    if not design_tokens_path.exists():
        missing.append(DESIGN_TOKENS_TEMPLATE)
    else:
        design_tokens_content = design_tokens_path.read_text(encoding="utf-8")
        for issue in validate_design_tokens_template(design_tokens_content):
            mismatches.append((DESIGN_TOKENS_TEMPLATE, issue))

    if missing:
        print("FAIL: missing template file(s):", file=sys.stderr)
        for path in missing:
            print(f"  - {path}", file=sys.stderr)
        return 1

    if mismatches:
        print("FAIL: template/reference validation failed:", file=sys.stderr)
        for left, right in mismatches:
            print(f"  - {left} != {right}", file=sys.stderr)
        return 1

    print("PASS: packaged assets, reference templates, and shared runtime references are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
