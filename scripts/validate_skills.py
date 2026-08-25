#!/usr/bin/env python3
"""Validate the skills/ directory of the AI-Agent repository.

Checks (structural, stdlib-only):
1. Every skill directory has a SKILL.md with valid frontmatter:
   - name matches directory name and is unique
   - description is non-empty
   - version follows MAJOR.MINOR.PATCH
2. Specialist skills contain a "Report Back" section.
3. SKILL-REGISTRY.md Capability Registry covers exactly the specialist set.
4. Backtick-quoted file references inside skills/*.md resolve to real files.
5. Every required .agent-engineering/ state file has a read-only template.

Usage: python scripts/validate_skills.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
MASTER_DIR = "agent-engineering-master"
TEMPLATES_DIR = "templates"
SKIP_DIRS = {TEMPLATES_DIR}

VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")
BACKTICK_RE = re.compile(r"`([^`\n]+)`")
REPORT_BACK_RE = re.compile(r"^#{1,3}\s+.*Report Back", re.MULTILINE)

# Required project state file -> source template in skills/templates/
REQUIRED_STATE_TEMPLATES = {
    "project.yaml": "project-state.yaml",
    "boundary-canvas.md": "agent-boundary-canvas.md",
    "decision-ledger.md": "decision-ledger.md",
    "current-session.md": "current-session.md",
    "project-intake.md": "project-intake.md",
    "architecture.md": "architecture-summary.md",
    "change-impact.md": "change-impact.md",
    "verification-report.md": "verification-report.md",
}

# Tokens that are conceptual paths, never repo files
IGNORE_TOKEN_SUBSTRINGS = (
    ".agent-engineering",
    "<project>",
    "<task",
)

# Instantiated project-state filenames without 1:1 template-name parity
STATE_FILENAMES = {
    "boundary-canvas.md",
    "architecture.md",
    "project.yaml",
}

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


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


def check_frontmatter(skills: dict[str, Path]) -> None:
    names_seen: dict[str, str] = {}
    for dirname, dirpath in skills.items():
        meta = parse_frontmatter(dirpath / "SKILL.md")
        if meta is None:
            err(f"{dirname}/SKILL.md: missing or malformed YAML frontmatter")
            continue
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


def check_report_back(skills: dict[str, Path]) -> None:
    for dirname, dirpath in skills.items():
        if dirname == MASTER_DIR:
            continue
        text = (dirpath / "SKILL.md").read_text(encoding="utf-8")
        if not REPORT_BACK_RE.search(text):
            err(f"{dirname}/SKILL.md: missing 'Report Back to Master' section")


def check_registry(skills: dict[str, Path]) -> None:
    registry_path = SKILLS_DIR / MASTER_DIR / "SKILL-REGISTRY.md"
    if not registry_path.exists():
        err(f"{MASTER_DIR}: missing SKILL-REGISTRY.md")
        return
    registry_text = registry_path.read_text(encoding="utf-8")
    referenced = set(re.findall(r"\.\./([a-z0-9-]+)/SKILL\.md", registry_text))
    specialists = set(skills) - {MASTER_DIR}
    missing = specialists - referenced
    extra = referenced - specialists
    for name in sorted(missing):
        err(f"SKILL-REGISTRY.md: specialist '{name}' not listed in Capability Registry")
    for name in sorted(extra):
        err(f"SKILL-REGISTRY.md: references unknown skill '{name}'")


def resolve_reference(token: str, from_file: Path) -> bool:
    candidates = [
        from_file.parent / token,
        REPO_ROOT / token,
        REPO_ROOT / "skills" / token,
        REPO_ROOT / "skills" / TEMPLATES_DIR / token,
    ]
    return any(c.exists() for c in candidates)


def check_file_references() -> None:
    md_files = [p for p in SKILLS_DIR.rglob("*.md")]
    for md in md_files:
        rel = md.relative_to(REPO_ROOT)
        text = md.read_text(encoding="utf-8")
        for token in BACKTICK_RE.findall(text):
            token = token.strip()
            if not re.search(r"\.(md|ya?ml)$", token, re.IGNORECASE):
                continue
            if any(s in token for s in IGNORE_TOKEN_SUBSTRINGS):
                continue
            if token in STATE_FILENAMES:
                continue
            if "*" in token or "<" in token:
                continue
            if not resolve_reference(token, md):
                err(f"{rel}: unresolved file reference '{token}'")


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
    found = len(skills)
    print(f"Discovered {found} skill directories under skills/")
    if found == 0:
        err("no skill directories found")

    check_frontmatter(skills)
    check_report_back(skills)
    check_registry(skills)
    check_file_references()
    check_templates()

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
