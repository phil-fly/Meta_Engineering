#!/usr/bin/env python3
"""Detect, plan, scaffold, and validate target-repo protocol packages."""

from __future__ import annotations

import argparse
import difflib
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
DEFAULT_EVIDENCE_EXCLUDES = {
    "ai-agent-workspace/protocols",
    "ai-agent-protocols",
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
ENTRY_MARKER_START = "<!-- BEGIN AI AGENT PROTOCOL PACKAGE -->"
ENTRY_MARKER_END = "<!-- END AI AGENT PROTOCOL PACKAGE -->"
CHECKPOINT_PHASES = ["classify", "collect", "decide", "generate", "validate"]
CHECKPOINT_SCHEMA = "maintain-agent-protocols.checkpoints.v1"
SUPPORT_ASSET_MAX_DEPTH = 3
SUPPORT_ASSET_MAX_FILES = 64
SUPPORT_ASSET_MAX_BYTES = 256 * 1024
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
    min_content_samples: int = 2


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
        min_content_samples=1,
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


def evidence_exclude_prefixes(root: Path) -> tuple[str, ...]:
    prefixes = set(DEFAULT_EVIDENCE_EXCLUDES)
    try:
        skill_prefix = SKILL_ROOT.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        skill_prefix = ""
    if skill_prefix:
        prefixes.add(skill_prefix)
    return tuple(sorted(prefixes))


def is_evidence_excluded(rel_file: str, prefixes: tuple[str, ...]) -> bool:
    return any(rel_file == prefix or rel_file.startswith(f"{prefix}/") for prefix in prefixes)


def is_text_candidate(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTENSIONS or path.name in {"Dockerfile", "Makefile", "Procfile"}


def path_matches(path: str, pattern: str) -> bool:
    candidates = {path, f"./{path}"}
    # Python's fnmatch treats ** like *, so **/*.py misses a root-level file.
    # Match the equivalent root form explicitly while retaining nested matches.
    if pattern.startswith("**/"):
        candidates.add(path.split("/", 1)[-1])
        pattern = pattern[3:]
    return any(fnmatch.fnmatch(candidate, pattern) for candidate in candidates) or fnmatch.fnmatch(
        path, f"./{pattern}"
    )


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


def is_documentation_path(rel_file: str) -> bool:
    path = Path(rel_file)
    return path.suffix.lower() in {".md", ".txt"} or any(
        segment.lower() in {"docs", "doc", "examples", "example", "fixtures", "test", "tests"}
        for segment in path.parts
    )


def is_test_path(rel_file: str) -> bool:
    """Return whether a path is a test/fixture/example artifact, not production code."""
    path = Path(rel_file)
    segments = {segment.lower() for segment in path.parts[:-1]}
    name = path.name.lower()
    if segments.intersection({"test", "tests", "fixture", "fixtures", "snapshot", "snapshots", "examples", "example"}):
        return True
    if re.search(r"(?:\.test|\.spec)\.[^.]+$", name):
        return True
    if re.search(r"(?:^test_.*|.*_test)\.[^.]+$", name):
        return True
    return False


def is_implementation_path(rel_file: str) -> bool:
    return not is_documentation_path(rel_file) and not is_test_path(rel_file)


def prioritize_evidence_hits(
    glob_candidates: list[str],
    content_candidates: list[str],
    max_hits: int,
) -> tuple[list[str], list[str], list[str]]:
    """Keep production evidence ahead of tests/docs before applying the output cap."""
    ordered_groups = (
        [item for item in glob_candidates if is_implementation_path(item)],
        [item for item in content_candidates if is_implementation_path(item)],
        [item for item in glob_candidates if not is_implementation_path(item)],
        [item for item in content_candidates if not is_implementation_path(item)],
    )
    hits: list[str] = []
    for group in ordered_groups:
        for item in group:
            if item not in hits:
                hits.append(item)
                if len(hits) >= max_hits:
                    selected = set(hits)
                    return (
                        hits,
                        [candidate for candidate in glob_candidates if candidate in selected],
                        [candidate for candidate in content_candidates if candidate in selected],
                    )
    selected = set(hits)
    return (
        hits,
        [candidate for candidate in glob_candidates if candidate in selected],
        [candidate for candidate in content_candidates if candidate in selected],
    )


def evidence_confidence(
    rule: EvidenceRule,
    implementation_hits: list[str],
    documentation_hits: list[str],
    glob_hits: list[str],
    content_hits: list[str],
) -> float:
    if not glob_hits and not content_hits:
        return 0.0
    if implementation_hits:
        # A matching file shape is stronger than a semantic keyword in content.
        if glob_hits:
            return 0.85
        implementation_content_hits = set(implementation_hits).intersection(content_hits)
        # A lone semantic keyword in one implementation file is only a signal.
        # Require independent file samples before it can select a project route.
        return 0.65 if len(implementation_content_hits) >= rule.min_content_samples else 0.4
    if documentation_hits:
        return 0.2 if content_hits else 0.3
    return 0.4


def collect_protocol_entries(root: Path) -> dict[str, Any]:
    existing = [path for path in ENTRY_CANDIDATES if (root / path).is_file()]
    canonical = "ai-agent-workspace/protocols"
    compat = "ai-agent-protocols"
    package_dirs = [path for path in [canonical, compat] if (root / path).exists()]
    canonical_has_assets = bool((root / canonical).is_dir() and any((root / canonical).rglob("*")))
    compat_has_assets = bool((root / compat).is_dir() and any((root / compat).rglob("*")))
    package_dir_conflict = canonical_has_assets and compat_has_assets
    playbooks = [path for path in ["playbooks", "ai-agent-workspace/protocols/playbooks", "ai-agent-protocols/playbooks"] if (root / path).exists()]
    default_entry = "AGENTS.md"
    reason = "Codex/OpenAI 场景默认入口"
    if "AGENTS.md" not in existing and "CLAUDE.md" in existing:
        default_entry = "CLAUDE.md"
        reason = "未发现 AGENTS.md，继承既有 CLAUDE.md"
    return {
        "existing_entries": existing,
        "package_dirs": package_dirs,
        "package_dir_conflict": package_dir_conflict,
        "package_dir_matrix": {
            "canonical": {"path": canonical, "exists": (root / canonical).exists(), "has_assets": canonical_has_assets},
            "compat": {"path": compat, "exists": (root / compat).exists(), "has_assets": compat_has_assets},
            "entry_files": existing,
        },
        "playbook_dirs": playbooks,
        "selected_entry": default_entry,
        "selection_reason": reason,
    }


def protocol_directory_status(root: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    canonical = manifest["default_package_dir"]
    compat = manifest["compat_package_dir"]
    def has_assets(relative: str) -> bool:
        directory = root / relative
        return directory.is_dir() and any(path.is_file() for path in directory.rglob("*"))
    canonical_assets = has_assets(canonical)
    compat_assets = has_assets(compat)
    return {
        "canonical": canonical,
        "compat": compat,
        "canonical_has_assets": canonical_assets,
        "compat_has_assets": compat_assets,
        "conflict": canonical_assets and compat_assets,
        "selected": compat if compat_assets and not canonical_assets else canonical,
    }


def detect_repo(root: Path) -> dict[str, Any]:
    root = root.resolve()
    files = iter_files(root)
    rel_files = [rel(path, root) for path in files]
    excluded_prefixes = evidence_exclude_prefixes(root)
    evidence_files = [
        (path, rel_file)
        for path, rel_file in zip(files, rel_files)
        if not is_evidence_excluded(rel_file, excluded_prefixes)
    ]
    evidence: dict[str, list[str]] = {}
    evidence_quality: dict[str, dict[str, Any]] = {}
    text_cache: dict[Path, str] = {}

    for rule in EVIDENCE_RULES:
        glob_candidates: list[str] = []
        content_candidates: list[str] = []
        for _, rel_file in evidence_files:
            if any(path_matches(rel_file, pattern) for pattern in rule.globs):
                glob_candidates.append(rel_file)

        if rule.content_patterns:
            compiled = [re.compile(pattern, re.IGNORECASE) for pattern in rule.content_patterns]
            for path, rel_file in evidence_files:
                if rel_file in glob_candidates or not is_text_candidate(path):
                    continue
                if rule.content_extensions and path.suffix.lower() not in rule.content_extensions:
                    continue
                if path not in text_cache:
                    text_cache[path] = read_text_safely(path)
                content = text_cache[path]
                if content and any(pattern.search(content) for pattern in compiled):
                    content_candidates.append(rel_file)

        unique_hits, glob_hits, content_hits = prioritize_evidence_hits(
            glob_candidates, content_candidates, rule.max_hits
        )
        unique_hits = sorted(unique_hits)
        evidence[rule.key] = unique_hits
        implementation_hits = [item for item in unique_hits if is_implementation_path(item)]
        test_hits = [item for item in unique_hits if is_test_path(item)]
        documentation_hits = [item for item in unique_hits if is_documentation_path(item)]
        production_glob_hits = [item for item in glob_hits if is_implementation_path(item)]
        production_content_hits = [item for item in content_hits if is_implementation_path(item)]
        confidence = evidence_confidence(rule, implementation_hits, documentation_hits, production_glob_hits, production_content_hits)
        counter_evidence = []
        if unique_hits and not implementation_hits:
            if test_hits:
                counter_evidence.append("当前命中仅来自测试、fixture、snapshot 或 example 文件；不作为生产实现证据")
            else:
                counter_evidence.append("未发现实现或配置文件命中；当前命中主要来自文档/样例")
        implementation_content_hits = set(implementation_hits).intersection(production_content_hits)
        if (
            implementation_hits
            and not glob_hits
            and len(implementation_content_hits) < rule.min_content_samples
        ):
            counter_evidence.append(
                "实现文件内容命中数不足；缺少规则要求的独立样本或结构证据"
            )
        if not unique_hits:
            counter_evidence.append("未发现该能力的文件或内容证据")
        evidence_quality[rule.key] = {
            "files": unique_hits,
            "sample_count": len(unique_hits),
            "glob_hits": sorted(dict.fromkeys(glob_hits)),
            "production_glob_hits": sorted(dict.fromkeys(production_glob_hits)),
            "test_glob_hits": sorted(dict.fromkeys(item for item in glob_hits if is_test_path(item))),
            "content_hits": sorted(dict.fromkeys(content_hits)),
            "min_content_samples": rule.min_content_samples,
            "implementation_samples": implementation_hits,
            "test_samples": test_hits,
            "documentation_samples": documentation_hits,
            "confidence": confidence,
            "counter_evidence": counter_evidence,
        }

    return {
        "root": str(root),
        "protocol_entries": collect_protocol_entries(root),
        "evidence": evidence,
        "summary": {
            "files_scanned": len(files),
            "evidence_files_scanned": len(evidence_files),
            "excluded_prefixes": list(excluded_prefixes),
            "evidence_keys": sorted([key for key, hits in evidence.items() if hits]),
        },
        "evidence_quality": evidence_quality,
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


def source_files_for_route(rule: dict[str, Any]) -> list[Path]:
    sources = source_files_for_rule(rule)
    always_include = set(rule.get("always_include", []))
    if not always_include:
        return sources
    selected = [path for path in sources if path.name in always_include or path.as_posix().endswith(tuple(always_include))]
    # Keep the manifest's explicit baseline files even if a future source_glob changes.
    for relative in always_include:
        candidate = SKILL_ROOT / "references" / "engineering" / "frontend" / relative
        if candidate.is_file() and candidate not in selected:
            selected.append(candidate)
    # An explicit baseline is a real pruning contract, not an annotation on a
    # full-domain copy. Add future files only by changing the manifest.
    return sorted(set(selected))


def resolve_source_markdown_reference(source: Path, reference: str) -> Path | None:
    """Resolve a source-owned Markdown reference without guessing ambiguous basenames."""
    reference = reference.split("#", 1)[0].split("?", 1)[0]
    candidate = (source.parent / reference).resolve()
    engineering_root = (SKILL_ROOT / "references" / "engineering").resolve()
    if candidate.is_file() and candidate.suffix.lower() == ".md":
        try:
            candidate.relative_to(engineering_root)
        except ValueError:
            return None
        return candidate
    if "/" in reference or reference.startswith("."):
        return None
    matches = sorted(path.resolve() for path in engineering_root.rglob(reference) if path.is_file())
    return matches[0] if len(matches) == 1 else None


def markdown_reference_targets(source: Path) -> list[Path]:
    """Resolve source-owned Markdown references that point at engineering assets."""
    targets: list[Path] = []
    for reference in find_local_markdown_references(source.read_text(encoding="utf-8", errors="ignore")):
        candidate = resolve_source_markdown_reference(source, reference)
        if candidate:
            targets.append(candidate)
    return sorted(set(targets))


def support_assets_for_routes(route_files: list[Path]) -> tuple[list[Path], list[str]]:
    """Collect one package-wide bounded closure without duplicating formal routes."""
    seen = set(route_files)
    queue = [(path, 0) for path in route_files]
    support: list[Path] = []
    support_bytes = 0
    warnings: list[str] = []
    while queue:
        source, depth = queue.pop(0)
        for target in markdown_reference_targets(source):
            if target in seen or not target.is_relative_to(SKILL_ROOT / "references" / "engineering"):
                continue
            target_depth = depth + 1
            if target_depth > SUPPORT_ASSET_MAX_DEPTH:
                warnings.append(f"support asset depth exceeded: {target.relative_to(SKILL_ROOT).as_posix()}")
                continue
            if len(support) >= SUPPORT_ASSET_MAX_FILES:
                warnings.append(f"support asset file budget exceeded: {target.relative_to(SKILL_ROOT).as_posix()}")
                continue
            target_bytes = target.stat().st_size
            if support_bytes + target_bytes > SUPPORT_ASSET_MAX_BYTES:
                warnings.append(f"support asset byte budget exceeded: {target.relative_to(SKILL_ROOT).as_posix()}")
                continue
            seen.add(target)
            support.append(target)
            support_bytes += target_bytes
            queue.append((target, target_depth))
    return sorted(support), sorted(set(warnings))


def support_assets_reachable_from(route_files: list[Path], support_files: list[Path]) -> list[Path]:
    """Attribute package-wide support assets to the routes that can reach them."""
    allowed = set(support_files)
    seen = set(route_files)
    queue = list(route_files)
    reachable: set[Path] = set()
    while queue:
        source = queue.pop(0)
        for target in markdown_reference_targets(source):
            if target in seen:
                continue
            seen.add(target)
            if target in allowed:
                reachable.add(target)
                queue.append(target)
    return sorted(reachable)


def route_asset_target(source: Path, package_dir: str) -> str:
    relative = source.relative_to(SKILL_ROOT / "references" / "engineering")
    return f"{package_dir}/support/engineering/{relative.as_posix()}"


def evidence_supports(
    rule: dict[str, Any],
    evidence: dict[str, list[str]],
    evidence_quality: dict[str, dict[str, Any]],
) -> bool:
    supported = [
        evidence_quality.get(key, {}).get("confidence", 0.0)
        for key in rule.get("evidence_keys", [])
        if evidence.get(key)
    ]
    # Conditional means "load when the task has evidence", not "always copy".
    threshold = float(rule.get("min_confidence", 0.5))
    return bool(supported) and max(supported) >= threshold


def route_is_selected(
    rule: dict[str, Any],
    evidence: dict[str, list[str]],
    evidence_quality: dict[str, dict[str, Any]],
    mode: str,
) -> bool:
    if mode == "minimal":
        return False
    if mode == "full":
        return True
    return evidence_supports(rule, evidence, evidence_quality)


def artifact_is_active(
    artifact: dict[str, Any],
    design_system: bool,
    evidence_quality: dict[str, dict[str, Any]] | None = None,
) -> bool:
    if artifact.get("activation") != "design_system" or not design_system:
        return False
    frontend = (evidence_quality or {}).get("frontend_implementation", {})
    return bool(frontend.get("implementation_samples"))


def resolve_artifact_target(root: Path, artifact: dict[str, Any]) -> tuple[str | None, list[str]]:
    candidates = [artifact["default_target"], *artifact.get("compat_targets", [])]
    existing = [target for target in candidates if (root / target).is_file()]
    if len(existing) > 1:
        return None, existing
    return (existing[0] if existing else artifact["default_target"]), existing


def make_entry_body(package_dir: str, selected_routes: list[dict[str, Any]]) -> str:
    lines = [
        ENTRY_MARKER_START,
        "## AI Agent Protocol Package",
        "",
        f"协议资产入口：`{package_dir}/README.md`。",
        f"场景手册：`{package_dir}/playbooks/`；工程路由：`{package_dir}/routes/`；检查清单：`{package_dir}/checks/`。",
        "",
        "生成后请先运行协议包 validate；仅在入口、引用和检查均通过后视为生效。",
    ]
    if selected_routes:
        lines.extend(["", "已生成路由："])
        lines.extend(f"- `{package_dir}/{route['target_prefix']}/index.md`" for route in selected_routes)
    lines.extend([ENTRY_MARKER_END, ""])
    return "\n".join(lines) + "\n"


def entry_marker_is_valid(content: str, package_dir: str) -> bool:
    if content.count(ENTRY_MARKER_START) != 1 or content.count(ENTRY_MARKER_END) != 1:
        return False
    start = content.find(ENTRY_MARKER_START)
    end = content.find(ENTRY_MARKER_END)
    if start < 0 or end < 0 or end <= start:
        return False
    block = content[start:end + len(ENTRY_MARKER_END)]
    references = find_local_markdown_references(block)
    return bool(
        re.search(r"^## AI Agent Protocol Package\s*$", block, re.MULTILINE)
        and f"{package_dir}/README.md" in references
    )


def make_entry_patch(
    root: Path,
    entries: dict[str, Any],
    package_dir: str,
    selected_routes: list[dict[str, Any]],
) -> dict[str, Any]:
    entry_name = entries.get("selected_entry", "AGENTS.md")
    entry_path = root / entry_name
    old = entry_path.read_text(encoding="utf-8") if entry_path.is_file() else ""
    if entry_marker_is_valid(old, package_dir):
        return {
            "entry": entry_name,
            "status": "already-wired",
            "apply": False,
            "diff": "",
        }
    desired = make_entry_body(package_dir, selected_routes)
    start = old.find(ENTRY_MARKER_START)
    end = old.find(ENTRY_MARKER_END)
    if start >= 0 and end > start:
        end += len(ENTRY_MARKER_END)
        new = old[:start].rstrip() + ("\n\n" if old[:start].strip() else "") + desired + old[end:].lstrip("\n")
        status = "invalid-existing-marker"
    elif start >= 0 or end >= 0:
        cleaned = old.replace(ENTRY_MARKER_START, "").replace(ENTRY_MARKER_END, "").strip()
        new = cleaned + ("\n\n" if cleaned else "") + desired
        status = "invalid-existing-marker"
    else:
        new = old.rstrip() + ("\n\n" if old.strip() else "") + desired
        status = "patch-required"
    diff = "".join(
        difflib.unified_diff(
            old.splitlines(keepends=True),
            new.splitlines(keepends=True),
            fromfile=entry_name,
            tofile=entry_name,
        )
    )
    return {
        "entry": entry_name,
        "status": status,
        "apply": True,
        "diff": diff,
        "content": new,
    }


def plan_package(
    root: Path,
    manifest: dict[str, Any],
    mode: str = "project",
    design_system: bool = False,
) -> dict[str, Any]:
    detection = detect_repo(root)
    directory_status = protocol_directory_status(root, manifest)
    evidence = detection["evidence"]
    evidence_quality = detection.get("evidence_quality", {})
    package_dir = directory_status["selected"]
    selected_routes: list[dict[str, Any]] = []
    artifact_conflicts: list[dict[str, Any]] = []
    files: list[dict[str, Any]] = []

    files.append({"target": f"{package_dir}/README.md", "source": "generated", "kind": "readme", "action": "create"})
    files.append({"target": f"{package_dir}/protocol-package-state.json", "source": "generated", "kind": "state", "action": "create"})

    for template in manifest["templates"]:
        files.append({
            "target": f"{package_dir}/{template['target']}",
            "source": template["source"],
            "kind": "template",
            "action": "copy",
        })

    for artifact in manifest.get("conditional_artifacts", []):
        if not artifact_is_active(artifact, design_system, evidence_quality):
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
            "activation": artifact.get("activation"),
        })

    playbook_keys = list(manifest["playbooks"]["sections"].keys()) if mode == "full" else manifest["minimal_playbooks"]
    files.append({"target": f"{package_dir}/{manifest['playbooks']['target_dir']}/README.md", "source": "generated", "kind": "playbook-index", "action": "create"})
    for key in playbook_keys:
        files.append({
            "target": f"{package_dir}/{manifest['playbooks']['target_dir']}/{manifest['playbooks']['sections'][key]}",
            "source": f"{manifest['playbooks']['source']}#{key}",
            "kind": "playbook",
            "action": "extract-section",
        })

    check_keys = set(manifest["checks"]["sections"].keys()) if mode == "full" else set(manifest["minimal_checks"])
    route_rules = {rule["id"]: rule for rule in manifest["route_rules"]}
    selected_rule_ids = {
        rule["id"] for rule in manifest["route_rules"]
        if route_is_selected(rule, evidence, evidence_quality, mode)
    }
    route_files_by_id = {
        rule["id"]: (
            source_files_for_rule(rule)
            if mode == "full"
            else source_files_for_route(rule)
        )
        for rule in manifest["route_rules"]
        if rule["id"] in selected_rule_ids
    }
    all_route_files = sorted({
        source
        for route_files in route_files_by_id.values()
        for source in route_files
    })
    support_files, support_warnings = support_assets_for_routes(all_route_files)
    for rule in manifest["route_rules"]:
        if rule["id"] in selected_rule_ids:
            route_files = route_files_by_id[rule["id"]]
            route_support_files = support_assets_reachable_from(route_files, support_files)
            directly_supported = evidence_supports(rule, evidence, evidence_quality)
            supported_keys = [
                key for key in rule.get("evidence_keys", [])
                if evidence.get(key)
            ]
            if directly_supported:
                status = rule["status"]
                decision = "direct"
                decision_reason = "direct evidence threshold met"
            else:
                status = "完整覆盖"
                decision = "full-coverage"
                decision_reason = "selected by explicit full mode without direct project evidence"
            selected_routes.append({
                "id": rule["id"],
                "status": status,
                "target_prefix": rule["target_prefix"],
                "evidence_keys": supported_keys,
                "evidence_quality": {
                    key: evidence_quality.get(key, {}) for key in supported_keys
                },
                "decision": decision,
                "decision_reason": decision_reason,
                "evidence_complete": bool(directly_supported and supported_keys),
                "requires": list(rule.get("requires", [])),
                "read_dependencies": [
                    {
                        "id": dependency,
                        "generated": dependency in selected_rule_ids,
                        "target_prefix": route_rules.get(dependency, {}).get("target_prefix"),
                    }
                    for dependency in rule.get("requires", [])
                ],
                "conditional": bool(rule.get("conditional")),
                "always_include": sorted(rule.get("always_include", [])),
                "files": [path.relative_to(SKILL_ROOT).as_posix() for path in route_files],
                "support_assets": [path.relative_to(SKILL_ROOT).as_posix() for path in route_support_files],
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

    for source in support_files:
        files.append({
            "target": route_asset_target(source, package_dir),
            "source": source.relative_to(SKILL_ROOT).as_posix(),
            "kind": "support_asset",
            "action": "copy",
            "status": "reference-only",
        })

    files.append({"target": f"{package_dir}/routes/index.md", "source": "generated", "kind": "route-index", "action": "create"})
    files.append({"target": f"{package_dir}/{manifest['checks']['target_dir']}/README.md", "source": "generated", "kind": "check-index", "action": "create"})

    for key in sorted(check_keys):
        files.append({
            "target": f"{package_dir}/{manifest['checks']['target_dir']}/{manifest['checks']['sections'][key]}",
            "source": f"{manifest['checks']['source']}#{key}",
            "kind": "check",
            "action": "extract-section",
        })

    entry_patch = make_entry_patch(root, detection["protocol_entries"], package_dir, selected_routes)
    return {
        "mode": mode,
        "package_dir": package_dir,
        "entry": detection["protocol_entries"],
        "evidence": detection["summary"],
        "evidence_quality": evidence_quality,
        "selected_routes": selected_routes,
        "support_assets": [path.relative_to(SKILL_ROOT).as_posix() for path in support_files],
        "artifact_conflicts": artifact_conflicts,
        "protocol_directory": directory_status,
        "files": files,
        "entry_patch": entry_patch,
        "warnings": support_warnings,
        "checkpoint_state": {
            "schema": CHECKPOINT_SCHEMA,
            "mode": mode,
            "package_dir": package_dir,
            "entry": entry_patch["entry"],
            "entry_patch_status": entry_patch["status"],
            "required": CHECKPOINT_PHASES,
            "completed": ["classify", "collect", "decide"],
            "status": "planned",
        },
        "notes": [
            "scaffold 默认跳过既有文件；使用 --overwrite 才会覆盖。",
            "普通前端证据不创建 design-tokens.md；仅显式 --design-system 时创建或维护。",
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


def route_index_metadata(route: dict[str, Any]) -> tuple[str, float]:
    if route["decision"] == "full-coverage":
        trigger = "用户显式选择完整版；当前仓库无直接证据"
    else:
        trigger = "命中相关任务且本轮证据支持时读取" if route["conditional"] else "当前仓库证据支持"
    confidence = max(
        (item.get("confidence", 0.0) for item in route.get("evidence_quality", {}).values()),
        default=0.0,
    )
    return trigger, confidence


def make_route_index(selected_routes: list[dict[str, Any]]) -> str:
    lines = [
        "# 工程路由索引",
        "",
        "本索引只列本次计划实际生成的工程路由；阅读依赖不参与路由选择或证据置信度计算。",
        "",
        "| 状态 | 路由 | 触发条件 | 证据置信度 | 阅读依赖 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for route in selected_routes:
        trigger, confidence = route_index_metadata(route)
        dependencies = []
        for dependency in route.get("read_dependencies", []):
            dependency_id = dependency["id"]
            target_prefix = dependency.get("target_prefix")
            if dependency.get("generated") and target_prefix:
                target = Path(target_prefix).relative_to("routes") / "index.md"
                dependencies.append(f"[{dependency_id}]({target.as_posix()})")
            else:
                dependencies.append(f"{dependency_id}（源规则依赖未落盘）")
        dependency_cell = "、".join(dependencies) if dependencies else "无"
        lines.append(
            f"| {route['status']} | `{route['target_prefix']}/` | {trigger} | "
            f"{confidence:.2f} | {dependency_cell} |"
        )
    lines.append("")
    return "\n".join(lines)


def make_playbook_index(package_dir: str, playbook_keys: list[str], manifest: dict[str, Any]) -> str:
    lines = ["# 场景手册索引", "", "生成包内场景手册的唯一入口。", ""]
    for key in playbook_keys:
        lines.append(f"- `{manifest['playbooks']['sections'][key]}`")
    return "\n".join(lines) + "\n"


def make_check_index(check_keys: set[str], manifest: dict[str, Any]) -> str:
    lines = ["# 检查清单索引", "", "生成包内检查清单的唯一入口。", ""]
    for key in sorted(check_keys):
        lines.append(f"- `{manifest['checks']['sections'][key]}`")
    return "\n".join(lines) + "\n"


def make_state_file(plan: dict[str, Any]) -> str:
    state = {
        "schema": CHECKPOINT_SCHEMA,
        "mode": plan["mode"],
        "package_dir": plan["package_dir"],
        "required": CHECKPOINT_PHASES,
        "completed": CHECKPOINT_PHASES[:-1],
        "status": "generated",
        "entry": plan["entry_patch"]["entry"],
        "entry_patch_status": plan["entry_patch"]["status"],
    }
    return json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def scaffold_package(
    root: Path,
    manifest: dict[str, Any],
    mode: str,
    overwrite: bool,
    design_system: bool = False,
    apply_entry: bool = False,
) -> dict[str, Any]:
    plan = plan_package(root, manifest, mode, design_system)
    preflight_errors: list[str] = []
    if plan.get("protocol_directory", {}).get("conflict"):
        preflight_errors.append(
            "canonical 与 compat 协议目录同时包含可编辑资产，存在双真值源冲突；scaffold 已停止。"
        )
    if plan["artifact_conflicts"]:
        preflight_errors.append("存在未裁决的条件产物真值源冲突，scaffold 已停止。")
    if plan["warnings"]:
        preflight_errors.append("support asset 闭包超出预算，scaffold 已停止；请先收敛引用或调整预算。")
    if preflight_errors:
        return {
            "plan": plan,
            "written": [],
            "skipped": [],
            "warnings": plan["warnings"],
            "entry_apply_attempted": False,
            "entry_applied": False,
            "entry_rolled_back": False,
            "validation": None,
            "errors": preflight_errors,
        }
    package_dir = plan["package_dir"]
    written: list[str] = []
    skipped: list[str] = []
    playbook_sections = section_map(SKILL_ROOT / manifest["playbooks"]["source"])
    check_sections = section_map(SKILL_ROOT / manifest["checks"]["source"])
    playbook_keys = list(manifest["playbooks"]["sections"].keys()) if mode == "full" else manifest["minimal_playbooks"]
    check_keys = set(manifest["checks"]["sections"].keys()) if mode == "full" else set(manifest["minimal_checks"])
    asset_map = {
        item["source"]: item["target"]
        for item in plan["files"]
        if item["kind"] in {"route", "support_asset"}
    }

    for item in plan["files"]:
        target = root / item["target"]
        if item["kind"] == "readme":
            content = make_readme(package_dir)
        elif item["kind"] == "state":
            content = make_state_file(plan)
        elif item["kind"] == "playbook-index":
            content = make_playbook_index(package_dir, playbook_keys, manifest)
        elif item["kind"] == "check-index":
            content = make_check_index(check_keys, manifest)
        elif item["kind"] == "route-index":
            content = make_route_index(plan["selected_routes"])
        elif item["kind"] in {"template", "route", "support_asset", "conditional-artifact"}:
            content = (SKILL_ROOT / item["source"]).read_text(encoding="utf-8")
        elif item["kind"] == "playbook":
            key = item["source"].split("#", 1)[1]
            content = playbook_sections[key]
        elif item["kind"] == "check":
            key = item["source"].split("#", 1)[1]
            content = check_sections[key]
        else:
            raise ValueError(f"Unknown file kind: {item['kind']}")
        content = rewrite_generated_references(
            content,
            package_dir,
            item["kind"],
            item.get("source"),
            item.get("target"),
            asset_map,
        )
        item_overwrite = overwrite and item["kind"] != "conditional-artifact"
        write_file(target, content, item_overwrite, written, skipped)

    entry_apply_attempted = False
    entry_applied = False
    entry_rolled_back = False
    entry_path = root / plan["entry_patch"]["entry"]
    if apply_entry and plan["entry_patch"].get("apply"):
        entry_apply_attempted = True
        entry_existed = entry_path.is_file()
        original_entry = entry_path.read_text(encoding="utf-8") if entry_existed else None
        ensure_parent(entry_path)
        entry_path.write_text(plan["entry_patch"]["content"], encoding="utf-8")
        written.append(entry_path.as_posix())
        entry_applied = True
    else:
        entry_existed = entry_path.is_file()
        original_entry = entry_path.read_text(encoding="utf-8") if entry_existed else None

    plan["checkpoint_state"].update({
        "completed": CHECKPOINT_PHASES[:-1],
        "status": "generated",
    })
    validation = None
    errors: list[str] = []
    if apply_entry:
        validation = validate_package(root, manifest, package_dir, design_system)
        if not validation["ok"]:
            if entry_apply_attempted:
                if original_entry is None:
                    entry_path.unlink(missing_ok=True)
                else:
                    entry_path.write_text(original_entry, encoding="utf-8")
                if entry_path.as_posix() in written:
                    written.remove(entry_path.as_posix())
                entry_applied = False
                entry_rolled_back = True
                errors.append("入口应用后的协议包验证未通过，入口已回滚。")
            else:
                errors.append("协议包验证未通过；入口未发生变更。")
    return {
        "plan": plan,
        "written": written,
        "skipped": skipped,
        "warnings": plan["warnings"],
        "entry_apply_attempted": entry_apply_attempted,
        "entry_applied": entry_applied,
        "entry_rolled_back": entry_rolled_back,
        "validation": validation,
        "errors": errors,
    }


def rewrite_generated_references(
    content: str,
    package_dir: str,
    kind: str,
    source_rel: str | None = None,
    target_rel: str | None = None,
    support_map: dict[str, str] | None = None,
) -> str:
    if kind == "playbook":
        content = content.replace("../engineering/", "../routes/")
        content = content.replace("../checks/checklists.md", "../checks/README.md")
    if kind in {"route", "support_asset"} and target_rel:
        target_path = Path(target_rel)
        generated_targets = {
            "../../scenarios/playbooks.md": Path(package_dir) / "playbooks" / "README.md",
            "../../scenarios/index.md": Path(package_dir) / "playbooks" / "README.md",
            "../../checks/checklists.md": Path(package_dir) / "checks" / "README.md",
            "../../checks/index.md": Path(package_dir) / "checks" / "README.md",
            "../../protocol/index.md": Path(package_dir) / "README.md",
        }
        for original, generated in generated_targets.items():
            replacement = os.path.relpath(generated, target_path.parent)
            content = content.replace(original, Path(replacement).as_posix())
    if source_rel and target_rel and support_map:
        source_path = (SKILL_ROOT / source_rel).resolve()
        target_path = Path(target_rel)

        def replace_reference(match: re.Match[str]) -> str:
            raw = match.group(1)
            reference = raw.strip()
            suffix = ""
            if "#" in reference:
                reference, anchor = reference.split("#", 1)
                suffix = f"#{anchor}"
            if reference == "templates/design-tokens.md":
                replacement = os.path.relpath(
                    Path(package_dir) / "templates" / "design-tokens.md",
                    target_path.parent,
                )
                return match.group(0).replace(raw, f"{Path(replacement).as_posix()}{suffix}")
            candidate = resolve_source_markdown_reference(source_path, reference)
            if not candidate:
                return match.group(0)
            candidate_key = candidate.relative_to(SKILL_ROOT).as_posix()
            mapped = support_map.get(candidate_key)
            if not mapped:
                return match.group(0)
            replacement = os.path.relpath(Path(mapped), target_path.parent)
            if "/" not in replacement and not replacement.startswith("."):
                replacement = f"./{replacement}"
            return match.group(0).replace(raw, f"{Path(replacement).as_posix()}{suffix}")

        token_template = os.path.relpath(
            Path(package_dir) / "templates" / "design-tokens.md", target_path.parent
        )
        content = content.replace("`templates/design-tokens.md`", f"`{Path(token_template).as_posix()}`")
        content = re.sub(r"\[[^\]]+\]\(([^)]+)\)", replace_reference, content)
        content = re.sub(r"`([^`\s]+\.md(?:#[^`\s]+)?)`", replace_reference, content)
    return content


def find_explicit_markdown_links(content: str) -> list[str]:
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
    return references


def find_local_markdown_references(content: str) -> list[str]:
    references = find_explicit_markdown_links(content)

    def add(raw: str) -> None:
        value = raw.strip().split("#", 1)[0].split("?", 1)[0]
        if value and value.lower().endswith(".md") and value not in references:
            references.append(value)

    for match in re.finditer(r"`([^`\s]+\.md(?:#[^`\s]+)?)`", content):
        add(match.group(1))
    return references


def validate_entries(
    root: Path,
    package_dir: str,
    selected_entry: str | None = None,
) -> tuple[list[str], list[str], list[str]]:
    entry_files = [name for name in ENTRY_CANDIDATES if (root / name).is_file()]
    errors: list[str] = []
    warnings: list[str] = []
    if not entry_files:
        errors.append("缺少根级生效入口；需要 AGENTS.md、CLAUDE.md 或既有 CODEX.md/codex.md 兼容入口")
        return entry_files, errors, warnings

    entry_name = selected_entry or collect_protocol_entries(root)["selected_entry"]
    if entry_name not in ENTRY_CANDIDATES:
        errors.append(f"状态文件声明了非法入口：{entry_name}")
        return entry_files, errors, warnings
    if entry_name not in entry_files:
        errors.append(f"状态文件声明的生效入口不存在：{entry_name}")
        return entry_files, errors, warnings

    resolved_root = root.resolve()
    for name in entry_files:
        entry_path = root / name
        content = entry_path.read_text(encoding="utf-8", errors="ignore")
        marker_present = ENTRY_MARKER_START in content or ENTRY_MARKER_END in content or re.search(
            r"^## AI Agent Protocol Package\s*$", content, re.MULTILINE
        )
        if name == entry_name and not entry_marker_is_valid(content, package_dir):
            errors.append(
                f"{name} 缺少指向 {package_dir}/README.md 的规范化协议包 marker block"
            )
        elif name != entry_name and marker_present:
            if entry_marker_is_valid(content, package_dir):
                warnings.append(f"存在多个协议入口：{entry_name} 与 {name}；请声明 canonical entry/alias entry")
            else:
                errors.append(f"{name} 的协议 marker 未指向当前协议包 {package_dir}/README.md")
        for reference in find_local_markdown_references(content):
            candidate = root / reference.lstrip("/") if reference.startswith("/") else entry_path.parent / reference
            resolved = candidate.resolve()
            try:
                resolved.relative_to(resolved_root)
            except ValueError:
                errors.append(f"{name} 引用超出目标仓范围：{reference}")
                continue
            if not resolved.is_file():
                errors.append(f"{name} 引用不存在：{reference}")
    return entry_files, errors, warnings


def validate_package_references(
    root: Path, base: Path, allowed_external_references: set[str] | None = None
) -> list[str]:
    errors: list[str] = []
    allowed_external_references = allowed_external_references or set()
    if not base.is_dir():
        return errors
    for path in base.rglob("*.md"):
        relative_to_package = path.relative_to(base)
        if "templates" in relative_to_package.parts:
            continue
        content = path.read_text(encoding="utf-8", errors="ignore")
        explicit_links = set(find_explicit_markdown_links(content))
        for reference in find_local_markdown_references(content):
            if reference not in explicit_links and "/" not in reference and not reference.startswith("."):
                # Bare inline-code filenames may be prose asset mentions. Explicit
                # Markdown links are always navigation and must resolve.
                continue
            package_prefix = base.relative_to(root).as_posix()
            root_relative = (
                reference in allowed_external_references
                or reference.startswith(f"{package_prefix}/")
                or reference.startswith("/")
            )
            candidate = (root / reference).resolve() if root_relative else (path.parent / reference).resolve()
            if root_relative and reference in allowed_external_references:
                # Only manifest-declared canonical/compat artifact paths may
                # leave the protocol package.
                continue
            try:
                candidate.relative_to(base.resolve())
            except ValueError:
                errors.append(f"{relative_to_package.as_posix()} 引用超出协议包范围：{reference}")
                continue
            if not candidate.is_file():
                errors.append(f"{relative_to_package.as_posix()} 引用不存在：{reference}")
    return errors


def directory_contains_rule_id(directory: Path, pattern: re.Pattern[str]) -> bool:
    if not directory.exists():
        return False
    for path in directory.rglob("*.md"):
        if pattern.search(path.read_text(encoding="utf-8", errors="ignore")):
            return True
    return False


def validate_route_index(
    route_index: Path,
    base: Path,
    manifest: dict[str, Any],
    mode: str | None = None,
    expected_routes: list[dict[str, Any]] | None = None,
) -> list[str]:
    errors: list[str] = []
    if not route_index.is_file():
        return errors
    content = route_index.read_text(encoding="utf-8", errors="ignore")
    if "| 状态 | 路由 | 触发条件 | 证据置信度 | 阅读依赖 |" not in content:
        errors.append("routes/index.md 未包含完整路由与阅读依赖列")
        return errors
    valid_statuses = {"项目证据支持", "条件适用", "通用治理", "完整覆盖"}
    rows: dict[str, dict[str, Any]] = {}
    for line in content.splitlines():
        if not line.startswith("|") or line.count("|") < 6 or "---" in line:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 5 or cells[0] == "状态":
            continue
        route = cells[1].strip("`").rstrip("/")
        if route.startswith("routes/"):
            route = route[len("routes/"):]
        linked_dependencies = {
            dependency: target
            for dependency, target in re.findall(r"\[([A-Za-z0-9_-]+)\]\(([^)]+)\)", cells[4])
        }
        ungenerated_dependencies = set(
            re.findall(r"([A-Za-z0-9_-]+)（源规则依赖未落盘）", cells[4])
        )
        if route in rows:
            errors.append(f"routes/index.md 重复路由：{route}")
            continue
        rows[route] = {
            "status": cells[0],
            "trigger": cells[2],
            "confidence": cells[3],
            "linked_dependencies": linked_dependencies,
            "ungenerated_dependencies": ungenerated_dependencies,
        }
        if cells[0] not in valid_statuses:
            errors.append(f"routes/index.md 路由 {route} 状态非法：{cells[0]}")

    routes_root = base / "routes"
    actual = {
        path.parent.relative_to(routes_root).as_posix()
        for path in routes_root.rglob("*.md")
        if path.parent != routes_root
    } if routes_root.is_dir() else set()
    if set(rows) != actual:
        missing = sorted(actual - set(rows))
        extra = sorted(set(rows) - actual)
        if missing:
            errors.append(f"routes/index.md 缺少实际路由：{', '.join(missing)}")
        if extra:
            errors.append(f"routes/index.md 包含不存在路由：{', '.join(extra)}")

    rules = manifest.get("route_rules", [])
    rule_by_prefix = {rule["target_prefix"]: rule for rule in rules}
    rule_by_id = {rule["id"]: rule for rule in rules}
    for route in rows:
        if f"routes/{route}" not in rule_by_prefix:
            errors.append(f"routes/index.md 包含未知路由：{route}")
    selected_ids = {
        rule["id"]
        for route in rows
        if (rule := rule_by_prefix.get(f"routes/{route}"))
    }
    for route, row in rows.items():
        rule = rule_by_prefix.get(f"routes/{route}")
        if not rule:
            continue
        if row["status"] == "完整覆盖" and mode != "full":
            errors.append(f"routes/index.md 路由 {route} 只有 full 模式才能标记完整覆盖")
        elif row["status"] not in {rule["status"], "完整覆盖"}:
            errors.append(f"routes/index.md 路由 {route} 状态与 manifest 不一致：{row['status']}")
        expected_dependencies = set(rule.get("requires", []))
        actual_dependencies = set(row["linked_dependencies"]) | row["ungenerated_dependencies"]
        if actual_dependencies != expected_dependencies:
            errors.append(
                f"routes/index.md 路由 {route} 阅读依赖与 manifest 不一致："
                f"expected={sorted(expected_dependencies)}, actual={sorted(actual_dependencies)}"
            )
        for dependency in expected_dependencies:
            dependency_rule = rule_by_id.get(dependency)
            if dependency in selected_ids:
                target = row["linked_dependencies"].get(dependency)
                expected_target = None
                if dependency_rule:
                    expected_target = (
                        Path(dependency_rule["target_prefix"]).relative_to("routes") / "index.md"
                    ).as_posix()
                if target != expected_target or not (route_index.parent / (target or "")).is_file():
                    errors.append(
                        f"routes/index.md 路由 {route} 的已生成阅读依赖 {dependency} 不可达"
                    )
            elif dependency not in row["ungenerated_dependencies"]:
                errors.append(
                    f"routes/index.md 路由 {route} 的未生成阅读依赖 {dependency} 未显式标注"
                )

    if expected_routes is not None:
        expected_by_route = {
            Path(route["target_prefix"]).relative_to("routes").as_posix(): route
            for route in expected_routes
        }
        missing_from_plan = sorted(set(expected_by_route) - set(rows))
        unexpected_for_plan = sorted(set(rows) - set(expected_by_route))
        if missing_from_plan:
            errors.append(f"routes/index.md 缺少当前生成计划路由：{', '.join(missing_from_plan)}")
        if unexpected_for_plan:
            errors.append(f"routes/index.md 包含当前生成计划未选择路由：{', '.join(unexpected_for_plan)}")
        for route, expected in expected_by_route.items():
            row = rows.get(route)
            if row is None:
                continue
            expected_trigger, expected_confidence = route_index_metadata(expected)
            if row["status"] != expected["status"]:
                errors.append(
                    f"routes/index.md 路由 {route} 状态与当前生成计划不一致："
                    f"expected={expected['status']}, actual={row['status']}"
                )
            if row["trigger"] != expected_trigger:
                errors.append(f"routes/index.md 路由 {route} 触发决策与当前生成计划不一致")
            try:
                actual_confidence = float(row["confidence"])
            except ValueError:
                errors.append(f"routes/index.md 路由 {route} 证据置信度非法：{row['confidence']}")
            else:
                if actual_confidence != round(expected_confidence, 2):
                    errors.append(
                        f"routes/index.md 路由 {route} 证据置信度与当前生成计划不一致："
                        f"expected={expected_confidence:.2f}, actual={row['confidence']}"
                    )
    return errors


def validate_checkpoint_contract(
    state: dict[str, Any],
    package_dir: str,
) -> list[str]:
    errors: list[str] = []
    prefix = f"{package_dir}/protocol-package-state.json"
    if state.get("schema") != CHECKPOINT_SCHEMA:
        errors.append(f"{prefix} schema 无效")
    if state.get("required") != CHECKPOINT_PHASES:
        errors.append(f"{prefix} required 必须是有序完整阶段")

    mode = state.get("mode")
    if mode not in {"minimal", "project", "full"}:
        errors.append(f"{prefix} mode 无效或缺失：{mode}")
    if state.get("package_dir") != package_dir:
        errors.append(f"{prefix} package_dir 与当前协议包不一致")
    if state.get("entry") not in ENTRY_CANDIDATES:
        errors.append(f"{prefix} entry 无效或缺失：{state.get('entry')}")
    valid_patch_statuses = {
        "patch-required",
        "already-wired",
        "invalid-existing-marker",
        "not-applied",
    }
    if state.get("entry_patch_status") not in valid_patch_statuses:
        errors.append(f"{prefix} entry_patch_status 无效或缺失：{state.get('entry_patch_status')}")

    completed = state.get("completed")
    if not isinstance(completed, list):
        errors.append(f"{prefix} completed 必须是阶段列表")
        completed = []
    if completed != CHECKPOINT_PHASES[:len(completed)]:
        errors.append(f"{prefix} completed 必须是无重复的有序阶段前缀")

    status = state.get("status")
    expected_completed = {
        "planned": CHECKPOINT_PHASES[:3],
        "generated": CHECKPOINT_PHASES[:-1],
        "validated": CHECKPOINT_PHASES,
        "invalid": CHECKPOINT_PHASES,
    }
    if status not in expected_completed:
        errors.append(f"{prefix} status 无效：{status}")
    elif completed != expected_completed[status]:
        errors.append(f"{prefix} status={status} 与 completed 阶段不一致")
    return errors


def invalid_checkpoint_state(
    state: dict[str, Any],
    root: Path,
    package_dir: str,
) -> dict[str, Any]:
    """Return a schema-shaped invalid state without inventing a missing file."""
    entry = state.get("entry")
    if entry not in ENTRY_CANDIDATES:
        entry = collect_protocol_entries(root).get("selected_entry", "AGENTS.md")
    mode = state.get("mode")
    if mode not in {"minimal", "project", "full"}:
        mode = "minimal"
    patch_status = state.get("entry_patch_status")
    if patch_status not in {"patch-required", "already-wired", "invalid-existing-marker", "not-applied"}:
        patch_status = "not-applied"
    return {
        **state,
        "schema": CHECKPOINT_SCHEMA,
        "mode": mode,
        "package_dir": package_dir,
        "entry": entry,
        "entry_patch_status": patch_status,
        "required": CHECKPOINT_PHASES,
        "completed": CHECKPOINT_PHASES,
        "status": "invalid",
        "failed_from_status": state.get("failed_from_status", state.get("status")),
    }


def validate_package(
    root: Path,
    manifest: dict[str, Any],
    package_dir: str | None = None,
    design_system: bool = False,
) -> dict[str, Any]:
    root = root.resolve()
    if package_dir is not None:
        allowed_package_dirs = {
            manifest["default_package_dir"],
            manifest["compat_package_dir"],
        }
        requested_path = Path(package_dir)
        requested_base = (root / requested_path).resolve()
        try:
            requested_base.relative_to(root)
        except ValueError:
            package_dir_is_local = False
        else:
            package_dir_is_local = not requested_path.is_absolute()
        if package_dir not in allowed_package_dirs or not package_dir_is_local:
            return {
                "ok": False,
                "package_dir": package_dir,
                "entry_files": [],
                "entry_errors": [],
                "missing": [],
                "content_errors": [
                    "package_dir 必须是 manifest 声明且位于目标仓内的 canonical/compat 路径"
                ],
                "warnings": [],
                "placeholder_files": [],
                "checkpoint_state": {
                    "schema": CHECKPOINT_SCHEMA,
                    "required": CHECKPOINT_PHASES,
                    "completed": [],
                    "status": "missing",
                },
            }
    directory_status = protocol_directory_status(root, manifest)
    requested_package_dir = package_dir
    package_dir = package_dir or directory_status["selected"]
    base = root / package_dir
    missing: list[str] = []
    warnings: list[str] = []
    entry_files: list[str] = []
    entry_errors: list[str] = []
    content_errors: list[str] = []
    if directory_status["conflict"] and package_dir not in {directory_status["canonical"], directory_status["compat"]}:
        content_errors.append("协议目录参数不是 manifest 声明的 canonical/compat 路径")
    if directory_status["conflict"] and requested_package_dir is None:
        content_errors.append("canonical 与 compat 协议目录同时包含可编辑资产，存在双��值源冲突")
    elif directory_status["conflict"] and requested_package_dir is not None:
        warnings.append(f"已显式选择协议真值源：{package_dir}")
    required_dirs = ["templates", "playbooks", "checks", "routes"]
    for directory in required_dirs:
        if not (base / directory).exists():
            missing.append(f"{package_dir}/{directory}/")

    state_path = base / "protocol-package-state.json"
    checkpoint_state: dict[str, Any] = {
        "schema": CHECKPOINT_SCHEMA,
        "required": CHECKPOINT_PHASES,
        "completed": [],
        "status": "missing",
    }
    if not state_path.is_file():
        missing.append(f"{package_dir}/protocol-package-state.json")
    else:
        try:
            loaded_state = json.loads(state_path.read_text(encoding="utf-8"))
            if not isinstance(loaded_state, dict):
                content_errors.append(f"{package_dir}/protocol-package-state.json 必须是 JSON object")
            else:
                checkpoint_state = loaded_state
                content_errors.extend(validate_checkpoint_contract(checkpoint_state, package_dir))
        except (OSError, json.JSONDecodeError) as exc:
            content_errors.append(f"{package_dir}/protocol-package-state.json 无法读取：{exc}")

    selected_entry = checkpoint_state.get("entry") if isinstance(checkpoint_state, dict) else None
    entry_files, entry_errors, entry_warnings = validate_entries(root, package_dir, selected_entry)
    warnings.extend(entry_warnings)

    for template in manifest["templates"]:
        if not (base / template["target"]).exists():
            missing.append(f"{package_dir}/{template['target']}")

    evidence_quality = detect_repo(root).get("evidence_quality", {})
    for artifact in manifest.get("conditional_artifacts", []):
        if not artifact_is_active(artifact, design_system, evidence_quality):
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
        expected_routes = None
        state_mode = checkpoint_state.get("mode")
        if state_mode in {"minimal", "project", "full"}:
            expected_routes = plan_package(root, manifest, state_mode, design_system)["selected_routes"]
        content_errors.extend(
            validate_route_index(
                route_index,
                base,
                manifest,
                state_mode,
                expected_routes,
            )
        )
    else:
        missing.append(f"{package_dir}/routes/index.md")

    allowed_external_references = {
        target
        for artifact in manifest.get("conditional_artifacts", [])
        for target in [artifact["default_target"], *artifact.get("compat_targets", [])]
    }
    content_errors.extend(validate_package_references(root, base, allowed_external_references))

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

    status = checkpoint_state.get("status")
    completed = checkpoint_state.get("completed")
    if status == "planned" or (
        status == "invalid" and checkpoint_state.get("failed_from_status") == "planned"
    ):
        content_errors.append(f"{package_dir}/protocol-package-state.json 必须先完成 generate 阶段才能 validate")
    elif status == "generated" and completed != CHECKPOINT_PHASES[:-1]:
        content_errors.append(f"{package_dir}/protocol-package-state.json generated 状态必须完成 generate 阶段")
    elif status not in {"generated", "validated", "invalid"}:
        content_errors.append(f"{package_dir}/protocol-package-state.json 无法从 status={status} 进入 validate")

    ok = not missing and not placeholders and not entry_errors and not content_errors
    state_exists = state_path.is_file()
    if ok:
        checkpoint_state = {
            **checkpoint_state,
            "completed": CHECKPOINT_PHASES,
            "status": "validated",
        }
    elif state_exists:
        checkpoint_state = invalid_checkpoint_state(checkpoint_state, root, package_dir)
    if state_exists and state_path.parent.exists():
        temp_state = state_path.with_suffix(state_path.suffix + ".tmp")
        temp_state.write_text(json.dumps(checkpoint_state, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        temp_state.replace(state_path)
    return {
        "ok": ok,
        "package_dir": package_dir,
        "entry_files": entry_files,
        "entry_errors": entry_errors,
        "missing": missing,
        "content_errors": content_errors,
        "warnings": warnings,
        "placeholder_files": placeholders,
        "checkpoint_state": checkpoint_state,
    }


def cmd_detect(args: argparse.Namespace) -> int:
    dump_json(detect_repo(Path(args.repo)))
    return 0


def cmd_plan(args: argparse.Namespace) -> int:
    manifest = load_json(Path(args.manifest))
    dump_json(plan_package(Path(args.repo), manifest, args.mode, args.design_system))
    return 0


def cmd_scaffold(args: argparse.Namespace) -> int:
    manifest = load_json(Path(args.manifest))
    result = scaffold_package(
        Path(args.repo), manifest, args.mode, args.overwrite, args.design_system, args.apply_entry
    )
    dump_json(result)
    return 1 if result["errors"] else 0


def cmd_validate(args: argparse.Namespace) -> int:
    manifest = load_json(Path(args.manifest))
    result = validate_package(Path(args.repo), manifest, args.package_dir, args.design_system)
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
    plan.add_argument("--design-system", action="store_true", help="Include Design System governance artifacts.")
    plan.set_defaults(func=cmd_plan)

    scaffold = subparsers.add_parser("scaffold", help="Write protocol package files from a plan.")
    scaffold.add_argument("repo", help="Target repository root.")
    scaffold.add_argument("--mode", choices=["minimal", "project", "full"], default="project")
    scaffold.add_argument("--overwrite", action="store_true", help="Overwrite existing files. Default skips them.")
    scaffold.add_argument("--design-system", action="store_true", help="Include Design System governance artifacts.")
    scaffold.add_argument("--apply-entry", action="store_true", help="Apply the reviewed root entry patch and validate immediately.")
    scaffold.set_defaults(func=cmd_scaffold)

    validate = subparsers.add_parser("validate", help="Validate an existing protocol package.")
    validate.add_argument("repo", help="Target repository root.")
    validate.add_argument("--package-dir", help="Protocol package directory relative to repo root.")
    validate.add_argument("--design-system", action="store_true", help="Validate Design System governance artifacts.")
    validate.set_defaults(func=cmd_validate)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
