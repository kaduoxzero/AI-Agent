# Skill Development Guide

## Standard Structure

Each skill must contain:

```
SKILL.md        execution protocol (frontmatter: name / version / description)
skill.yaml      machine-readable manifest
```

Recommended additions:

```
README.md
examples/
tests/
resources/
```

## Required Metadata

Defined in `skill.yaml` (canonical template: `skills/SKILL-MANIFEST-TEMPLATE.yaml`):

- name
- version
- category
- capabilities
- trigger
- input
- output
- dependencies
- risk
- status

## Rules

Core skills must remain industry neutral.
Domain skills provide business-specific extensions.

Validation is executed by `scripts/validate_skills.py` and enforced in CI.
