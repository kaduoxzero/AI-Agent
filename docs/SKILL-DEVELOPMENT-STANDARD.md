# Skill Development Standard

## Skill Package

Every skill must provide:

- `SKILL.md` — execution protocol; frontmatter carries name / version / description
- `skill.yaml` — machine-readable manifest (canonical template: `skills/SKILL-MANIFEST-TEMPLATE.yaml`)

Recommended:

- README.md
- examples/
- tests/
- resources/

## Manifest

`skill.yaml` describes:

- name
- version
- category
- capabilities
- triggers
- inputs
- outputs
- dependencies
- risk level
- status

The manifest `version` must equal the SKILL.md frontmatter `version`.

## Lifecycle

Draft -> Review -> Stable -> Deprecated -> Archived

## Layering

Core Skills are industry independent. Domain Skills provide optional extensions and must not modify core runtime files.

## Validation

`scripts/validate_skills.py` enforces structure, metadata consistency, registry coverage and reference integrity. CI runs it on every change under `skills/`, `runtime/` or `scripts/`.
