# Skill Engineering

## Purpose

建立 Agent 能力工程化体系，将 Skill 从提示词片段升级为可注册、可验证、可版本管理的能力单元。

## Architecture

```
Skill Definition
      ↓
Skill Registry
      ↓
Skill Router
      ↓
Skill Runtime
      ↓
Skill Evaluation
```

## Core Components

- skill.yaml Manifest
- Skill Schema Validation
- Capability Registry
- Skill Version Management
- Permission Control
- Skill Evaluation

## Engineering Goals

- Agent 能自动发现能力
- Agent 能动态加载能力
- Skill 可以独立测试和发布
- Skill 具备生命周期管理
