#!/usr/bin/env python3
"""Check packaged assets, reference templates, and shared runtime references."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[1]

PAIRS = [
    ("templates/user-protocol.md", "references/protocol/user-protocol-template.md"),
    ("templates/project-protocol.md", "references/protocol/project-protocol-template.md"),
    ("templates/route-card.md", "references/protocol/route-card-template.md"),
]

SHARED_COPY_PAIRS = [
    ("references/shared/target-workspace-layout.md", "references/target-workspace-layout.md"),
]

INTERACTIVE_RUNTIME = "references/shared/interactive-decision-protocol.md"
INTERACTIVE_SOURCE = "references/interactive-decision-protocol.md"
INTERACTIVE_REQUIRED_HEADINGS = [
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
]
INTERACTIVE_PROJECTION_BLOCKS = [
    ("## 设计原则", "## 交互式场景清单", "## 交互式场景清单"),
    ("#### 场景 1: 模型入口文件选择", "#### 场景 2: 生成模式选择", "#### 场景 2: 生成模式选择"),
    ("#### 场景 2: 生成模式选择", "#### 场景 3: 真值源冲突解决", "#### 场景 3: 真值源冲突解决"),
    ("#### 场景 3: 真值源冲突解决", "#### 场景 4: 工程路由裁剪策略", "#### 场景 4: 工程路由裁剪策略"),
    ("#### 场景 4: 工程路由裁剪策略", "### product-requirements-partner", "## 选项设计标准"),
    ("## 选项设计标准", "## 降级策略", "## 降级策略"),
    ("## 降级策略", "## 实施检查清单", "## 实施检查清单"),
    ("## 实施检查清单", "## 与现有协议的集成", "## 与现有协议的集成"),
    ("## 用户体验目标", "---", "---"),
]


def extract_block(content: str, start: str, end: str, offset: int = 0) -> str:
    start_index = content.index(start, offset)
    end_index = content.index(end, start_index + len(start))
    return content[start_index:end_index].strip()


def validate_interactive_runtime(runtime_content: str, source_content: str | None = None) -> list[str]:
    issues: list[str] = []
    if "product-requirements-partner" in runtime_content:
        issues.append("must not depend on product-requirements-partner")

    for heading in INTERACTIVE_REQUIRED_HEADINGS:
        if heading not in runtime_content:
            issues.append(f"missing runtime heading: {heading}")

    if source_content is None:
        return issues

    for heading in INTERACTIVE_REQUIRED_HEADINGS:
        if heading not in source_content:
            issues.append(f"missing source heading: {heading}")

    try:
        for start, source_end, runtime_end in INTERACTIVE_PROJECTION_BLOCKS:
            source_block = extract_block(source_content, start, source_end)
            runtime_block = extract_block(runtime_content, start, runtime_end)
            if source_block != runtime_block:
                issues.append(f"out-of-sync projection block: {start}")

        integration_heading = "## 与现有协议的集成"
        source_offset = source_content.index(integration_heading)
        runtime_offset = runtime_content.index(integration_heading)
        source_integration = extract_block(
            source_content,
            "### maintain-agent-protocols",
            "### product-requirements-partner",
            source_offset,
        )
        runtime_integration = extract_block(
            runtime_content,
            "### maintain-agent-protocols",
            "## 用户体验目标",
            runtime_offset,
        )
        if source_integration != runtime_integration:
            issues.append("out-of-sync maintain-agent-protocols integration")
    except ValueError as error:
        issues.append(f"cannot parse projection: {error}")
    return issues


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

    for packaged, authoring in SHARED_COPY_PAIRS:
        packaged_path = ROOT / packaged
        if not packaged_path.exists():
            missing.append(packaged)
            continue

        authoring_path = REPO_ROOT / authoring
        if authoring_path.exists() and packaged_path.read_bytes() != authoring_path.read_bytes():
            mismatches.append((packaged, authoring))

    interactive_runtime_path = ROOT / INTERACTIVE_RUNTIME
    if not interactive_runtime_path.exists():
        missing.append(INTERACTIVE_RUNTIME)
    else:
        runtime_content = interactive_runtime_path.read_text(encoding="utf-8")
        source_path = REPO_ROOT / INTERACTIVE_SOURCE
        source_content = source_path.read_text(encoding="utf-8") if source_path.exists() else None
        for issue in validate_interactive_runtime(runtime_content, source_content):
            mismatches.append((INTERACTIVE_RUNTIME, issue))

    if missing:
        print("FAIL: missing template file(s):", file=sys.stderr)
        for path in missing:
            print(f"  - {path}", file=sys.stderr)
        return 1

    if mismatches:
        print("FAIL: template/reference pairs differ:", file=sys.stderr)
        for left, right in mismatches:
            print(f"  - {left} != {right}", file=sys.stderr)
        return 1

    print("PASS: packaged assets, reference templates, and shared runtime references are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
