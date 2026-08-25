# AI-Agent v2.0 Architecture

## Positioning

AI-Agent is a general Agent Engineering Runtime Platform. It is industry-neutral and supports domain extensions through plugins.

## Layers

- Runtime Layer: bootstrap, loader, registry, router, orchestrator, validator, policy.
- Skill Layer: reusable agent capabilities.
- Domain Layer: industry-specific extensions.
- Evaluation Layer: capability and safety verification.
- Memory Layer: context, session, project, organization, knowledge memory.

## Design Principles

1. Core capabilities must not depend on any industry.
2. Domain logic must be implemented as extensions.
3. Every Skill requires metadata, boundaries, inputs, outputs, risks and evaluation criteria.
4. Agent execution requires validation and governance.
