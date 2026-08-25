# AI-Agent Runtime Architecture v2

## Overview

AI-Agent is organized as a general Agent Engineering Runtime.

Layers:

- Runtime: lifecycle, routing, loading, policy, state
- Skills: reusable capabilities
- Domains: industry extensions
- Evaluation: quality verification
- Memory: persistent context management

## Execution Flow

User Task

→ Bootstrap

→ Registry Discovery

→ Skill Routing

→ Skill Loading

→ Orchestration

→ Validation

→ Final Output

## Design Principles

- Core is industry independent
- Domain capabilities are plugins
- Skills must declare metadata
- High risk actions require policy evaluation
