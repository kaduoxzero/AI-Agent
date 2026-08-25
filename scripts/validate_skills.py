#!/usr/bin/env python3
"""Validate the skills/ system of the AI-Agent repository.

Implements the runtime v2 validation rules declared in:
  runtime/skill-validator/rules/{structure,quality,security}.yaml
  runtime/skill-registry-schema.yaml
  runtime/skill-lifecycle/lifecycle.yaml

Checks:
1. Every skill directory has a SKILL.md with valid frontmatter:
   - name matches directory name and is unique
   - description non-empty
   - version follows MAJOR.MINOR.PATCH
2. Every skill directory has a skill.yaml manifest whose metadata is
   consistent with SKILL.md frontmatter (name, version) and complete
   (description, capabilities, trigger, risk.level, status).
3. Specialist skills contain a "Report Back" section.
4. SKILL-REGISTRY.md Capability Registry covers exactly the specialist set.
5. runtime/skill-registry.yaml covers all skills; status/category match
   manifests; supporting-skill limits agree across runtime configs (= 2).
6. dependency-graph route targets exist.
7. File references (backticks + markdown links) resolve across skills,
   runtime and other system directories.
8. Every required project-state artifact has a read-only template.
9. Top-level numbered directories have unique numbers.
10. skills/SKILL-MANIFEST-TEMPLATE.yaml parses and contains required keys.

Usage: python scripts/validate_skills.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
RUNTIME_DIR = REPO_ROOT / "runtime"
MASTER_DIR = "agent-engineering-master"
TEMPLATES_DIR = "templates"
SKIP_DIRS = {TEMPLATES_DIR}

VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")
BACKTICK_RE = re.compile(r"`([^`\n]+)`")
MD_LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
REPORT_BACK_RE = re.compile(r"^#{1,3}\s+.*Report Back", re.MULTILINE)

LIFECYCLE_STATES = {"draft", "review", "stable", "deprecated", "archived"}
RISK_LEVELS = {"low", "medium", "high", "critical"}
SUPPORTING_LIMIT = 2

MANIFEST_TEMPLATE_KEYS = {
    "name", "version", "description", "capabilities",
    "trigger", "risk", "dependencies", "status",
}

# Repo areas covered by reference-integrity scanning
SYSTEM_SCAN_DIRS = (
    "runtime",
    "architecture",
    "docs",
    "evaluation",
    "governance",
    "memory",
    "15-skill-engineering",
    "16-agent-operating-system",
    "17-benchmarks",
    "18-case-studies",
    "schemas",
)

# Internal English ID -> instantiated Chinese artifact (per
# skills/agent-engineering-master/resources/PROJECT-DOCUMENT-NAMING.md)
REQUIRED_STATE_TEMPLATES = {
    "项目状态.yaml": "project-state.yaml",
    "边界画布.md": "agent-boundary-canvas.md",
    "决策记录.md": "decision-ledger.md",
    "当前会话.md": "current-session.md",
    "项目调研.md": "project-intake.md",
    "架构设计.md": "architecture-summary.md",
    "影响分析.md": "change-impact.md",
    "验证报告.md": "verification-report.md",
}

# Tokens that are conceptual paths, never repo files
IGNORE_TOKEN_SUBSTRINGS = (
    ".agent-engineering",
    "<project>",
    "<task",
)

# Instantiated artifact filenames (Chinese, per PROJECT-DOCUMENT-NAMING.md)
# plus their internal English IDs — referenced conceptually across docs,
# never resolvable as repo paths.
STATE_FILENAMES = set(REQUIRED_STATE_TEMPLATES) | {
    "project.yaml",
    "boundary-canvas.md",
    "decision-ledger.md",
    "current-session.md",
    "project-intake.md",
    "architecture.md",
    "change-impact.md",
    "verification-report.md",
}

# Generic per-skill filenames
GENERIC_FILENAMES = {"SKILL.md", "skill.yaml", "README.md"}

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


# --------------------------------------------------------------------------
# Minimal YAML subset parser (nested dicts, lists, scalars). Sufficient for
# the controlled config files in this repo; avoids external dependencies.
# --------------------------------------------------------------------------

def _scalar(value: str):
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        return [v.strip().strip("'\"") for v in inner.split(",")] if inner else []
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        return value[1:-1]
    if value.isdigit():
        return int(value)
    return value


def parse_simple_yaml(text: str):
    """Parse the restricted YAML subset used by runtime configs."""
    lines = []
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if line.strip():
            lines.append(line)

    def block(i: int, indent: int):
        first = lines[i].lstrip()
        if first.startswith("- "):
            arr = []
            while i < len(lines):
                line = lines[i]
                ind = len(line) - len(line.lstrip())
                if ind != indent or not line.lstrip().startswith("- "):
                    break
                arr.append(_scalar(line.strip()[2:]))
                i += 1
            return arr, i

        obj: dict = {}
        while i < len(lines):
            line = lines[i]
            ind = len(line) - len(line.lstrip())
            if ind < indent:
                break
            content = line.strip()
            key, _, rest = content.partition(":")
            rest = rest.strip()
            if rest:
                obj[key.strip()] = _scalar(rest)
                i += 1
            else:
                if i + 1 < len(lines):
                    nxt = lines[i + 1]
                    nind = len(nxt) - len(nxt.lstrip())
                    if nind > ind:
                        val, i = block(i + 1, nind)
                        obj[key.strip()] = val
                        continue
                obj[key.strip()] = None
                i += 1
        return obj, i

    if not lines:
        return {}
    root_indent = len(lines[0]) - len(lines[0].lstrip())
    result, _ = block(0, root_indent)
    return result


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------

def parse_frontmatter(path: Path) -> dict[str, str] | None:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", text, re.DOTALL)
    if not match:
        return None
    meta: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line.startswith((" ", "\t")):
            continue
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip().strip("'\"")
    return meta


def discover_skills() -> dict[str, Path]:
    skills: dict[str, Path] = {}
    for entry in sorted(SKILLS_DIR.iterdir()):
        if not entry.is_dir() or entry.name in SKIP_DIRS:
            continue
        skill_md = entry / "SKILL.md"
        if not skill_md.exists():
            err(f"{entry.name}/: missing SKILL.md")
            continue
        skills[entry.name] = entry
    return skills


def check_frontmatter(skills: dict[str, Path]) -> dict[str, dict[str, str]]:
    metas: dict[str, dict[str, str]] = {}
    names_seen: dict[str, str] = {}
    for dirname, dirpath in skills.items():
        meta = parse_frontmatter(dirpath / "SKILL.md")
        if meta is None:
            err(f"{dirname}/SKILL.md: missing or malformed YAML frontmatter")
            continue
        metas[dirname] = meta
        name = meta.get("name", "")
        if name != dirname:
            err(f"{dirname}/SKILL.md: frontmatter name '{name}' != directory name")
        if name in names_seen:
            err(f"{dirname}/SKILL.md: duplicate skill name (also in {names_seen[name]})")
        names_seen[name] = dirname
        desc = meta.get("description", "")
        if len(desc) < 20:
            err(f"{dirname}/SKILL.md: description missing or too short")
        version = meta.get("version", "")
        if not VERSION_RE.match(version):
            err(f"{dirname}/SKILL.md: version missing or invalid ('{version}', expect MAJOR.MINOR.PATCH)")
    return metas


def check_manifests(skills: dict[str, Path], metas: dict[str, dict[str, str]]) -> dict[str, dict]:
    manifests: dict[str, dict] = {}
    for dirname, dirpath in skills.items():
        mpath = dirpath / "skill.yaml"
        if not mpath.exists():
            err(f"{dirname}/: missing skill.yaml manifest (required by runtime structure rules)")
            continue
        try:
            m = parse_simple_yaml(mpath.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover
            err(f"{dirname}/skill.yaml: unparseable ({exc})")
            continue
        manifests[dirname] = m

        if m.get("name") != dirname:
            err(f"{dirname}/skill.yaml: name '{m.get('name')}' != directory name")
        fm_version = metas.get(dirname, {}).get("version", "")
        if m.get("version") != fm_version:
            err(f"{dirname}/skill.yaml: version '{m.get('version')}' != SKILL.md frontmatter version '{fm_version}'")
        if not str(m.get("description", "")).strip():
            err(f"{dirname}/skill.yaml: description empty")
        caps = m.get("capabilities")
        if not isinstance(caps, list) or not caps:
            err(f"{dirname}/skill.yaml: capabilities must be a non-empty list")
        trigger = m.get("trigger")
        if not isinstance(trigger, dict) or not isinstance(trigger.get("keywords"), list):
            err(f"{dirname}/skill.yaml: trigger.keywords missing")
        risk = m.get("risk")
        level = risk.get("level") if isinstance(risk, dict) else None
        if level not in RISK_LEVELS:
            err(f"{dirname}/skill.yaml: risk.level invalid ('{level}')")
        status = m.get("status")
        if status not in LIFECYCLE_STATES:
            err(f"{dirname}/skill.yaml: status '{status}' not in lifecycle states")
        deps = m.get("dependencies") or []
        for dep in deps:
            if dep not in skills:
                err(f"{dirname}/skill.yaml: dependency '{dep}' does not exist")
    return manifests


def check_report_back(skills: dict[str, Path]) -> None:
    for dirname, dirpath in skills.items():
        if dirname == MASTER_DIR:
            continue
        text = (dirpath / "SKILL.md").read_text(encoding="utf-8")
        if not REPORT_BACK_RE.search(text):
            err(f"{dirname}/SKILL.md: missing 'Report Back to Master' section")


def check_registry_md(skills: dict[str, Path]) -> None:
    registry_path = SKILLS_DIR / MASTER_DIR / "SKILL-REGISTRY.md"
    if not registry_path.exists():
        err(f"{MASTER_DIR}: missing SKILL-REGISTRY.md")
        return
    registry_text = registry_path.read_text(encoding="utf-8")
    referenced = set(re.findall(r"\.\./([a-z0-9-]+)/SKILL\.md", registry_text))
    specialists = set(skills) - {MASTER_DIR}
    for name in sorted(specialists - referenced):
        err(f"SKILL-REGISTRY.md: specialist '{name}' not listed in Capability Registry")
    for name in sorted(referenced - specialists):
        err(f"SKILL-REGISTRY.md: references unknown skill '{name}'")


def check_machine_registry(skills: dict[str, Path], manifests: dict[str, dict]) -> None:
    reg_path = RUNTIME_DIR / "skill-registry.yaml"
    if not reg_path.exists():
        err("runtime/skill-registry.yaml: missing")
        return
    reg = parse_simple_yaml(reg_path.read_text(encoding="utf-8"))
    entries = reg.get("skills")
    if not isinstance(entries, dict):
        err("runtime/skill-registry.yaml: 'skills' section missing")
        return
    listed = set(entries)
    for name in sorted(set(skills) - listed):
        err(f"runtime/skill-registry.yaml: skill '{name}' not registered")
    for name in sorted(listed - set(skills)):
        err(f"runtime/skill-registry.yaml: unknown skill '{name}'")
    for name, entry in entries.items():
        if not isinstance(entry, dict):
            continue
        mf_status = manifests.get(name, {}).get("status")
        if entry.get("status") != mf_status:
            err(
                f"runtime/skill-registry.yaml: '{name}' status '{entry.get('status')}' "
                f"!= manifest status '{mf_status}'"
            )
        mf_category = manifests.get(name, {}).get("category")
        if entry.get("category") != mf_category:
            err(
                f"runtime/skill-registry.yaml: '{name}' category '{entry.get('category')}' "
                f"!= manifest category '{mf_category}'"
            )

    policy = reg.get("policy", {})
    loading = policy.get("loading", {}) if isinstance(policy, dict) else {}
    if loading.get("max_supporting_skills") != SUPPORTING_LIMIT:
        err(
            f"runtime/skill-registry.yaml: max_supporting_skills "
            f"'{loading.get('max_supporting_skills')}' != {SUPPORTING_LIMIT}"
        )


def check_routing_policy() -> None:
    path = RUNTIME_DIR / "skill-router" / "routing-policy.yaml"
    if not path.exists():
        warn("runtime/skill-router/routing-policy.yaml: missing")
        return
    cfg = parse_simple_yaml(path.read_text(encoding="utf-8"))
    routing = cfg.get("routing", {})
    supporting = routing.get("supporting_skills", {}) if isinstance(routing, dict) else {}
    if supporting.get("max_count") != SUPPORTING_LIMIT:
        err(
            f"routing-policy.yaml: supporting_skills.max_count "
            f"'{supporting.get('max_count')}' != {SUPPORTING_LIMIT} (master rule)"
        )


def check_dependency_graph(skills: dict[str, Path]) -> None:
    path = RUNTIME_DIR / "skill-registry" / "dependency-graph.yaml"
    if not path.exists():
        warn("runtime/skill-registry/dependency-graph.yaml: missing")
        return
    graph = parse_simple_yaml(path.read_text(encoding="utf-8"))
    known = set(skills)

    def walk(node) -> list[str]:
        if isinstance(node, list):
            return [x for x in node]
        return []

    declared: set[str] = set()
    for group in graph.get("nodes", {}).values() if isinstance(graph.get("nodes"), dict) else []:
        declared.update(walk(group))
    for name in sorted(declared - known):
        err(f"dependency-graph.yaml: node '{name}' does not exist")
    edges = graph.get("edges", {})
    if isinstance(edges, dict):
        for src, targets_by_kind in edges.items():
            if src not in known:
                err(f"dependency-graph.yaml: edge source '{src}' does not exist")
            if isinstance(targets_by_kind, dict):
                for kind, targets in targets_by_kind.items():
                    for t in walk(targets):
                        if t not in known:
                            err(f"dependency-graph.yaml: '{src}' {kind} target '{t}' does not exist")


def resolve_reference(token: str, from_file: Path) -> bool:
    candidates = [
        from_file.parent / token,
        REPO_ROOT / token,
        REPO_ROOT / "skills" / token,
        REPO_ROOT / "skills" / TEMPLATES_DIR / token,
    ]
    return any(c.exists() for c in candidates)


def _iter_md_files() -> list[Path]:
    files = [SKILLS_DIR / "README.md", SKILLS_DIR / "DEPLOY.md"]
    files += list(SKILLS_DIR.rglob("*.md"))
    files.append(REPO_ROOT / "README.md")
    for d in SYSTEM_SCAN_DIRS:
        path = REPO_ROOT / d
        if path.is_dir():
            files.extend(path.rglob("*.md"))
            files.extend(path.glob("*.yaml"))
    return sorted(set(files))


def check_file_references() -> None:
    for md in _iter_md_files():
        if not md.exists() or md.suffix == ".yaml":
            continue
        rel = md.relative_to(REPO_ROOT)
        text = md.read_text(encoding="utf-8")
        tokens = BACKTICK_RE.findall(text)
        for target in MD_LINK_RE.findall(text):
            if not target.startswith(("http://", "https://", "mailto:")):
                tokens.append(target)
        for token in tokens:
            token = token.strip()
            if not re.search(r"\.(md|ya?ml)$", token, re.IGNORECASE):
                continue
            if any(s in token for s in IGNORE_TOKEN_SUBSTRINGS):
                continue
            if token in STATE_FILENAMES or token in GENERIC_FILENAMES:
                continue
            if "*" in token or "<" in token:
                continue
            if not resolve_reference(token, md):
                err(f"{rel}: unresolved file reference '{token}'")


def check_numbered_dirs() -> None:
    seen: dict[str, str] = {}
    for entry in sorted(REPO_ROOT.iterdir()):
        match = re.match(r"^(\d+)-", entry.name)
        if entry.is_dir() and match:
            num = match.group(1)
            if num in seen:
                err(f"duplicate top-level directory number '{num}': {seen[num]} vs {entry.name}")
            seen[num] = entry.name


def check_manifest_template() -> None:
    path = SKILLS_DIR / "SKILL-MANIFEST-TEMPLATE.yaml"
    if not path.exists():
        err("skills/SKILL-MANIFEST-TEMPLATE.yaml: missing")
        return
    tpl = parse_simple_yaml(path.read_text(encoding="utf-8"))
    missing = MANIFEST_TEMPLATE_KEYS - set(tpl)
    if missing:
        err(f"SKILL-MANIFEST-TEMPLATE.yaml: missing keys {sorted(missing)}")


def check_templates() -> None:
    templates_dir = SKILLS_DIR / TEMPLATES_DIR
    for state_file, template in REQUIRED_STATE_TEMPLATES.items():
        if not (templates_dir / template).exists():
            err(
                f"templates/: missing '{template}' "
                f"(required to instantiate .agent-engineering/{state_file})"
            )


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print(f"FATAL: {SKILLS_DIR} does not exist")
        return 2

    skills = discover_skills()
    print(f"Discovered {len(skills)} skill directories under skills/")
    if not skills:
        err("no skill directories found")

    metas = check_frontmatter(skills)
    manifests = check_manifests(skills, metas)
    check_report_back(skills)
    check_registry_md(skills)
    check_machine_registry(skills, manifests)
    check_routing_policy()
    check_dependency_graph(skills)
    check_file_references()
    check_templates()
    check_numbered_dirs()
    check_manifest_template()

    for w in warnings:
        print(f"WARN: {w}")
    if errors:
        print(f"\nFAILED with {len(errors)} error(s):")
        for e in errors:
            print(f"  ERROR: {e}")
        return 1
    print("\nOK: all skills validation checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
