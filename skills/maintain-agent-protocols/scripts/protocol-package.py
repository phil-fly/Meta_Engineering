#!/usr/bin/env python3
"""Detect, plan, scaffold, and validate target-repo protocol packages."""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = SKILL_ROOT / "scripts" / "protocol-package-manifest.json"
DEFAULT_EXCLUDES = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "vendor",
    ".venv",
    "venv",
    "__pycache__",
    "dist",
    "build",
    ".next",
    ".nuxt",
    "target",
}
TEXT_EXTENSIONS = {
    ".md",
    ".txt",
    ".json",
    ".toml",
    ".yaml",
    ".yml",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".py",
    ".go",
    ".java",
    ".rs",
    ".rb",
    ".php",
    ".cs",
    ".kt",
    ".swift",
    ".sql",
    ".env",
    ".ini",
    ".cfg",
}
ENTRY_CANDIDATES = ("AGENTS.md", "CLAUDE.md", "CODEX.md", "codex.md")
RULE_ID_PATTERNS = {
    "playbook": re.compile(r"^#{1,6}\s+WF-[A-Z0-9]+(?:-[A-Z0-9]+)*\b", re.MULTILINE),
    "check": re.compile(r"^\s*-\s+CHK-[A-Z0-9]+(?:-[A-Z0-9]+)*\b", re.MULTILINE),
}


@dataclass(frozen=True)
class EvidenceRule:
    key: str
    globs: tuple[str, ...] = ()
    content_patterns: tuple[str, ...] = ()
    max_hits: int = 12
    content_extensions: tuple[str, ...] = ()


EVIDENCE_RULES = [
    EvidenceRule(
        "frontend_implementation",
        (
            "index.html",
            "**/index.html",
            "**/*.tsx",
            "**/*.jsx",
            "**/*.vue",
            "**/*.svelte",
            "**/*.astro",
            "src/**/*.tsx",
            "src/**/*.jsx",
            "src/**/*.vue",
            "src/**/*.svelte",
            "src/**/*.css",
            "src/**/*.scss",
            "src/**/*.sass",
            "src/**/*.less",
            "app/**/*.tsx",
            "app/**/*.jsx",
            "pages/**/*.tsx",
            "pages/**/*.jsx",
            "components/**/*.tsx",
            "components/**/*.jsx",
            "frontend/**/*.tsx",
            "frontend/**/*.jsx",
            "frontend/**/*.vue",
            "frontend/**/*.svelte",
            "client/**/*.tsx",
            "client/**/*.jsx",
            "web/**/*.tsx",
            "web/**/*.jsx",
            "templates/**/*.html",
            "views/**/*.html",
        ),
        (
            r"\b(?:ReactDOM|createRoot|createApp|bootstrapApplication|customElements\.define|LitElement)\b",
            r"from\s+['\"](?:react|react-dom|vue|svelte|lit|@angular/core)['\"]",
        ),
        content_extensions=(".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".astro"),
    ),
    EvidenceRule("javascript_typescript", ("package.json", "tsconfig.json", "**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx")),
    EvidenceRule("go", ("go.mod", "**/*.go")),
    EvidenceRule("java", ("pom.xml", "build.gradle", "build.gradle.kts", "**/*.java")),
    EvidenceRule("rust", ("Cargo.toml", "**/*.rs")),
    EvidenceRule("python", ("pyproject.toml", "requirements.txt", "setup.py", "Pipfile", "**/*.py")),
    EvidenceRule("api", content_patterns=(r"\b(openapi|swagger|graphql|rest|router|controller|endpoint)\b",), max_hits=8),
    EvidenceRule("database", ("**/migrations/**",), (r"\b(sqlalchemy|prisma|typeorm|sequelize|diesel|gorm|jdbc|migration)\b",), 8),
    EvidenceRule("auth", content_patterns=(r"\b(auth|oauth|jwt|session|permission|role|acl|rbac)\b",), max_hits=8),
    EvidenceRule("logging", content_patterns=(r"\b(log|logger|logging|tracing|sentry|opentelemetry)\b",), max_hits=8),
    EvidenceRule("config", ("**/.env.example", "**/config.*",), (r"\b(config|feature flag|environment|dotenv)\b",), 8),
    EvidenceRule("security", content_patterns=(r"\b(secret|password|token|credential|encrypt|permission|audit|csrf|xss|sql injection)\b",), max_hits=8),
    EvidenceRule("performance", content_patterns=(r"\b(cache|latency|throughput|n\+1|profil|performance|web vitals)\b",), max_hits=8),
    EvidenceRule("deployment", ("Dockerfile", "docker-compose.yml", ".github/workflows/*.yml", "k8s/**", "helm/**")),
    EvidenceRule("observability", content_patterns=(r"\b(metrics|prometheus|grafana|opentelemetry|trace|span|observability)\b",), max_hits=8),
    EvidenceRule("gateway", content_patterns=(r"\b(gateway|nginx|ingress|load balancer|reverse proxy)\b",), max_hits=8),
    EvidenceRule("governance", ("AGENTS.md", "CLAUDE.md", "CODEX.md", "ai-agent-workspace/protocols/**", "ai-agent-protocols/**")),
]


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))


def should_skip_dir(path: Path) -> bool:
    return path.name in DEFAULT_EXCLUDES


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        dirnames[:] = [name for name in dirnames if not should_skip_dir(current / name)]
        for filename in filenames:
            files.append(current / filename)
    return files


def is_text_candidate(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTENSIONS or path.name in {"Dockerfile", "Makefile", "Procfile"}


def path_matches(path: str, pattern: str) -> bool:
    return fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(path, f"./{pattern}")


def read_text_safely(path: Path, max_bytes: int = 262144) -> str:
    try:
        content = path.read_bytes()[:max_bytes]
    except OSError:
        return ""
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError:
        return ""


def strip_inline_code(content: str) -> str:
    return re.sub(r"`[^`\n]*`", "", content)


def collect_protocol_entries(root: Path) -> dict[str, Any]:
    existing = [path for path in ENTRY_CANDIDATES if (root / path).is_file()]
    package_dirs = [path for path in ["ai-agent-workspace/protocols", "ai-agent-protocols"] if (root / path).exists()]
    playbooks = [path for path in ["playbooks", "ai-agent-workspace/protocols/playbooks", "ai-agent-protocols/playbooks"] if (root / path).exists()]
    default_entry = "AGENTS.md"
    reason = "Codex/OpenAI 场景默认入口"
    if "AGENTS.md" not in existing and "CLAUDE.md" in existing:
        default_entry = "CLAUDE.md"
        reason = "未发现 AGENTS.md，继承既有 CLAUDE.md"
    return {
        "existing_entries": existing,
        "package_dirs": package_dirs,
        "playbook_dirs": playbooks,
        "selected_entry": default_entry,
        "selection_reason": reason,
    }


def detect_repo(root: Path) -> dict[str, Any]:
    root = root.resolve()
    files = iter_files(root)
    rel_files = [rel(path, root) for path in files]
    evidence: dict[str, list[str]] = {}
    text_cache: dict[Path, str] = {}

    for rule in EVIDENCE_RULES:
        hits: list[str] = []
        for rel_file in rel_files:
            if any(path_matches(rel_file, pattern) for pattern in rule.globs):
                hits.append(rel_file)
                if len(hits) >= rule.max_hits:
                    break

        if len(hits) < rule.max_hits and rule.content_patterns:
            compiled = [re.compile(pattern, re.IGNORECASE) for pattern in rule.content_patterns]
            for path, rel_file in zip(files, rel_files):
                if rel_file in hits or not is_text_candidate(path):
                    continue
                if rule.content_extensions and path.suffix.lower() not in rule.content_extensions:
                    continue
                if path not in text_cache:
                    text_cache[path] = read_text_safely(path)
                content = text_cache[path]
                if content and any(pattern.search(content) for pattern in compiled):
                    hits.append(rel_file)
                    if len(hits) >= rule.max_hits:
                        break

        evidence[rule.key] = sorted(dict.fromkeys(hits))

    return {
        "root": str(root),
        "protocol_entries": collect_protocol_entries(root),
        "evidence": evidence,
        "summary": {
            "files_scanned": len(files),
            "evidence_keys": sorted([key for key, hits in evidence.items() if hits]),
        },
    }


def section_map(source: Path) -> dict[str, str]:
    content = source.read_text(encoding="utf-8")
    sections: dict[str, str] = {}
    matches = list(re.finditer(r"^##\s+(.+?)\s*$", content, re.MULTILINE))
    for index, match in enumerate(matches):
        title = match.group(1).strip()
        key = title.split()[-1]
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
        body = content[start:end].strip() + "\n"
        sections[key] = body
    return sections


def source_files_for_rule(rule: dict[str, Any]) -> list[Path]:
    files: list[Path] = []
    for pattern in rule["source_globs"]:
        files.extend(SKILL_ROOT.glob(pattern))
    return sorted({path for path in files if path.is_file()})


def evidence_supports(rule: dict[str, Any], evidence: dict[str, list[str]], mode: str) -> bool:
    if mode == "minimal":
        return False
    if mode == "full":
        return True
    if rule.get("conditional"):
        return True
    return any(evidence.get(key) for key in rule.get("evidence_keys", []))


def artifact_evidence_supports(artifact: dict[str, Any], evidence: dict[str, list[str]]) -> bool:
    return any(evidence.get(key) for key in artifact.get("evidence_keys", []))


def resolve_artifact_target(root: Path, artifact: dict[str, Any]) -> tuple[str | None, list[str]]:
    candidates = [artifact["default_target"], *artifact.get("compat_targets", [])]
    existing = [target for target in candidates if (root / target).is_file()]
    if len(existing) > 1:
        return None, existing
    return (existing[0] if existing else artifact["default_target"]), existing


def plan_package(root: Path, manifest: dict[str, Any], mode: str = "project") -> dict[str, Any]:
    detection = detect_repo(root)
    evidence = detection["evidence"]
    package_dir = manifest["compat_package_dir"] if (root / manifest["compat_package_dir"]).exists() else manifest["default_package_dir"]
    selected_routes: list[dict[str, Any]] = []
    artifact_conflicts: list[dict[str, Any]] = []
    files: list[dict[str, Any]] = []

    files.append({"target": f"{package_dir}/README.md", "source": "generated", "kind": "readme", "action": "create"})

    for template in manifest["templates"]:
        files.append({
            "target": f"{package_dir}/{template['target']}",
            "source": template["source"],
            "kind": "template",
            "action": "copy",
        })

    for artifact in manifest.get("conditional_artifacts", []):
        if not artifact_evidence_supports(artifact, evidence):
            continue
        target, existing = resolve_artifact_target(root, artifact)
        if target is None:
            artifact_conflicts.append({"id": artifact["id"], "existing_targets": existing})
            continue
        files.append({
            "target": target,
            "source": artifact["source"],
            "kind": "conditional-artifact",
            "action": "maintain-and-verify" if existing else "create-and-backfill",
            "evidence_keys": [key for key in artifact.get("evidence_keys", []) if evidence.get(key)],
        })

    playbook_keys = list(manifest["playbooks"]["sections"].keys()) if mode == "full" else manifest["minimal_playbooks"]
    for key in playbook_keys:
        files.append({
            "target": f"{package_dir}/{manifest['playbooks']['target_dir']}/{manifest['playbooks']['sections'][key]}",
            "source": f"{manifest['playbooks']['source']}#{key}",
            "kind": "playbook",
            "action": "extract-section",
        })

    check_keys = set(manifest["checks"]["sections"].keys()) if mode == "full" else set(manifest["minimal_checks"])
    for rule in manifest["route_rules"]:
        if evidence_supports(rule, evidence, mode):
            route_files = source_files_for_rule(rule)
            selected_routes.append({
                "id": rule["id"],
                "status": rule["status"],
                "target_prefix": rule["target_prefix"],
                "evidence_keys": [key for key in rule.get("evidence_keys", []) if evidence.get(key)],
                "conditional": bool(rule.get("conditional")),
                "files": [path.relative_to(SKILL_ROOT).as_posix() for path in route_files],
            })
            for source in route_files:
                name = source.name
                target_name = "index.md" if source.stem == rule["id"].split("-")[-1] and source.parent.name == "backend" else name
                files.append({
                    "target": f"{package_dir}/{rule['target_prefix']}/{target_name}",
                    "source": source.relative_to(SKILL_ROOT).as_posix(),
                    "kind": "route",
                    "action": "copy",
                    "status": rule["status"],
                })
            for check_key in manifest.get("project_checks_by_route", {}).get(rule["id"], []):
                check_keys.add(check_key)

    files.append({"target": f"{package_dir}/routes/index.md", "source": "generated", "kind": "route-index", "action": "create"})

    for key in sorted(check_keys):
        files.append({
            "target": f"{package_dir}/{manifest['checks']['target_dir']}/{manifest['checks']['sections'][key]}",
            "source": f"{manifest['checks']['source']}#{key}",
            "kind": "check",
            "action": "extract-section",
        })

    return {
        "mode": mode,
        "package_dir": package_dir,
        "entry": detection["protocol_entries"],
        "evidence": detection["summary"],
        "selected_routes": selected_routes,
        "artifact_conflicts": artifact_conflicts,
        "files": files,
        "notes": [
            "scaffold 默认跳过既有文件；使用 --overwrite 才会覆盖。",
            "仅在发现真实前端实现时创建或维护 design-tokens.md；package.json 单独存在不构成前端实现证据。",
            "新建 design-tokens.md 后必须按生产实现回填；模板的待回填状态不能作为完成结果。",
            "项目事实证据只输出到计划，不写入生成的协议正文。",
            "生效入口文件仍需由执行者按预览确认后维护。",
        ],
    }


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_file(path: Path, content: str, overwrite: bool, written: list[str], skipped: list[str]) -> None:
    if path.exists() and not overwrite:
        skipped.append(path.as_posix())
        return
    ensure_parent(path)
    path.write_text(content, encoding="utf-8")
    written.append(path.as_posix())


def make_readme(package_dir: str) -> str:
    return f"""# AI Agent Protocols

本目录由 `maintain-agent-protocols` 工具链生成，承载目标仓 AI Agent 协作协议资产。

## 路径映射

- 场景手册：`{package_dir}/playbooks/`
- 工程路由：`{package_dir}/routes/`
- 检查清单：`{package_dir}/checks/`
- 模板资产：`{package_dir}/templates/`

## 维护边界

- 项目协议正文只能有一个生效真值源。
- 兼容入口只写跳转和映射，不复制完整正文。
- 生成过程证据、仓库扫描结果和待确认项应进入生成报告，不写入本 README。
"""


def make_route_index(selected_routes: list[dict[str, Any]]) -> str:
    lines = ["# 工程路由索引", "", "本索引只列本次计划实际生成的工程路由。", "", "| 状态 | 路由 | 触发条件 |", "| --- | --- | --- |"]
    for route in selected_routes:
        trigger = "命中相关任务时读取" if route["conditional"] else "当前仓库证据支持"
        lines.append(f"| {route['status']} | `{route['target_prefix']}/` | {trigger} |")
    lines.append("")
    return "\n".join(lines)


def scaffold_package(root: Path, manifest: dict[str, Any], mode: str, overwrite: bool) -> dict[str, Any]:
    plan = plan_package(root, manifest, mode)
    if plan["artifact_conflicts"]:
        return {
            "plan": plan,
            "written": [],
            "skipped": [],
            "errors": ["存在未裁决的条件产物真值源冲突，scaffold 已停止。"],
        }
    package_dir = plan["package_dir"]
    written: list[str] = []
    skipped: list[str] = []
    playbook_sections = section_map(SKILL_ROOT / manifest["playbooks"]["source"])
    check_sections = section_map(SKILL_ROOT / manifest["checks"]["source"])

    for item in plan["files"]:
        target = root / item["target"]
        if item["kind"] == "readme":
            content = make_readme(package_dir)
        elif item["kind"] == "route-index":
            content = make_route_index(plan["selected_routes"])
        elif item["kind"] in {"template", "route", "conditional-artifact"}:
            content = (SKILL_ROOT / item["source"]).read_text(encoding="utf-8")
        elif item["kind"] == "playbook":
            key = item["source"].split("#", 1)[1]
            content = playbook_sections[key]
        elif item["kind"] == "check":
            key = item["source"].split("#", 1)[1]
            content = check_sections[key]
        else:
            raise ValueError(f"Unknown file kind: {item['kind']}")
        item_overwrite = overwrite and item["kind"] != "conditional-artifact"
        write_file(target, content, item_overwrite, written, skipped)

    return {"plan": plan, "written": written, "skipped": skipped, "errors": []}


def find_local_markdown_references(content: str) -> list[str]:
    references: list[str] = []

    def add(raw: str) -> None:
        value = raw.strip()
        if value.startswith("<") and ">" in value:
            value = value[1:value.index(">")]
        else:
            value = value.split(maxsplit=1)[0]
        value = value.split("#", 1)[0].split("?", 1)[0]
        if not value or not value.lower().endswith(".md"):
            return
        if value.startswith(("http://", "https://", "mailto:", "#")):
            return
        if value not in references:
            references.append(value)

    for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", content):
        add(match.group(1))
    for match in re.finditer(r"`((?:/|\.{1,2}/|[^`\s/]+/)[^`\s]*\.md(?:#[^`\s]+)?)`", content):
        add(match.group(1))
    return references


def validate_entries(root: Path) -> tuple[list[str], list[str]]:
    entry_files = [name for name in ENTRY_CANDIDATES if (root / name).is_file()]
    errors: list[str] = []
    if not entry_files:
        errors.append("缺少根级生效入口；需要 AGENTS.md、CLAUDE.md 或既有 CODEX.md/codex.md 兼容入口")
        return entry_files, errors

    resolved_root = root.resolve()
    for entry_name in entry_files:
        entry_path = root / entry_name
        content = entry_path.read_text(encoding="utf-8", errors="ignore")
        for reference in find_local_markdown_references(content):
            candidate = root / reference.lstrip("/") if reference.startswith("/") else entry_path.parent / reference
            resolved = candidate.resolve()
            try:
                resolved.relative_to(resolved_root)
            except ValueError:
                errors.append(f"{entry_name} 引用超出目标仓范围：{reference}")
                continue
            if not resolved.is_file():
                errors.append(f"{entry_name} 引用不存在：{reference}")
    return entry_files, errors


def directory_contains_rule_id(directory: Path, pattern: re.Pattern[str]) -> bool:
    if not directory.exists():
        return False
    for path in directory.rglob("*.md"):
        if pattern.search(path.read_text(encoding="utf-8", errors="ignore")):
            return True
    return False


def validate_package(root: Path, manifest: dict[str, Any], package_dir: str | None = None) -> dict[str, Any]:
    root = root.resolve()
    package_dir = package_dir or (manifest["compat_package_dir"] if (root / manifest["compat_package_dir"]).exists() else manifest["default_package_dir"])
    base = root / package_dir
    missing: list[str] = []
    warnings: list[str] = []
    entry_files, entry_errors = validate_entries(root)
    content_errors: list[str] = []
    evidence = detect_repo(root)["evidence"]
    required_dirs = ["templates", "playbooks", "checks", "routes"]
    for directory in required_dirs:
        if not (base / directory).exists():
            missing.append(f"{package_dir}/{directory}/")

    for template in manifest["templates"]:
        if not (base / template["target"]).exists():
            missing.append(f"{package_dir}/{template['target']}")

    for artifact in manifest.get("conditional_artifacts", []):
        if not artifact_evidence_supports(artifact, evidence):
            continue
        target, existing = resolve_artifact_target(root, artifact)
        if target is None:
            content_errors.append(
                f"{artifact['id']} 存在多个可编辑真值源：{', '.join(existing)}"
            )
            continue
        artifact_path = root / target
        if not artifact_path.is_file():
            missing.append(target)
            continue
        artifact_content = artifact_path.read_text(encoding="utf-8", errors="ignore")
        for marker in artifact.get("required_markers", []):
            if marker not in artifact_content:
                content_errors.append(f"{target} 缺少必备章节：{marker}")
        for marker in artifact.get("incomplete_markers", []):
            if marker in artifact_content:
                content_errors.append(f"{target} 仍包含待回填标记：{marker}")

    route_index = base / "routes" / "index.md"
    if route_index.exists():
        content = route_index.read_text(encoding="utf-8")
        for label in ["项目证据支持", "条件适用", "通用治理"]:
            if label not in content:
                warnings.append(f"routes/index.md 未包含状态标注：{label}")
    else:
        missing.append(f"{package_dir}/routes/index.md")

    if not directory_contains_rule_id(base / "playbooks", RULE_ID_PATTERNS["playbook"]):
        content_errors.append(f"{package_dir}/playbooks/ 未包含 WF-* 工作流")
    if not directory_contains_rule_id(base / "checks", RULE_ID_PATTERNS["check"]):
        content_errors.append(f"{package_dir}/checks/ 未包含 CHK-* 检查项")

    placeholder_re = re.compile(r"<(?:project|install-command|package-manager|framework|language|path)>", re.IGNORECASE)
    placeholders: list[str] = []
    if base.exists():
        for path in base.rglob("*.md"):
            if "templates" in path.relative_to(base).parts:
                continue
            content = path.read_text(encoding="utf-8", errors="ignore")
            if placeholder_re.search(strip_inline_code(content)):
                placeholders.append(path.relative_to(root).as_posix())

    ok = not missing and not placeholders and not entry_errors and not content_errors
    return {
        "ok": ok,
        "package_dir": package_dir,
        "entry_files": entry_files,
        "entry_errors": entry_errors,
        "missing": missing,
        "content_errors": content_errors,
        "warnings": warnings,
        "placeholder_files": placeholders,
    }


def cmd_detect(args: argparse.Namespace) -> int:
    dump_json(detect_repo(Path(args.repo)))
    return 0


def cmd_plan(args: argparse.Namespace) -> int:
    manifest = load_json(Path(args.manifest))
    dump_json(plan_package(Path(args.repo), manifest, args.mode))
    return 0


def cmd_scaffold(args: argparse.Namespace) -> int:
    manifest = load_json(Path(args.manifest))
    result = scaffold_package(Path(args.repo), manifest, args.mode, args.overwrite)
    dump_json(result)
    return 1 if result["errors"] else 0


def cmd_validate(args: argparse.Namespace) -> int:
    manifest = load_json(Path(args.manifest))
    result = validate_package(Path(args.repo), manifest, args.package_dir)
    dump_json(result)
    return 0 if result["ok"] else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST), help="Path to protocol-package manifest JSON.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    detect = subparsers.add_parser("detect", help="Scan a target repo and output structured evidence.")
    detect.add_argument("repo", help="Target repository root.")
    detect.set_defaults(func=cmd_detect)

    plan = subparsers.add_parser("plan", help="Create a protocol package generation plan.")
    plan.add_argument("repo", help="Target repository root.")
    plan.add_argument("--mode", choices=["minimal", "project", "full"], default="project")
    plan.set_defaults(func=cmd_plan)

    scaffold = subparsers.add_parser("scaffold", help="Write protocol package files from a plan.")
    scaffold.add_argument("repo", help="Target repository root.")
    scaffold.add_argument("--mode", choices=["minimal", "project", "full"], default="project")
    scaffold.add_argument("--overwrite", action="store_true", help="Overwrite existing files. Default skips them.")
    scaffold.set_defaults(func=cmd_scaffold)

    validate = subparsers.add_parser("validate", help="Validate an existing protocol package.")
    validate.add_argument("repo", help="Target repository root.")
    validate.add_argument("--package-dir", help="Protocol package directory relative to repo root.")
    validate.set_defaults(func=cmd_validate)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
