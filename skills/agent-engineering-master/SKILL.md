---
name: agent-engineering-master
description: Master entry skill for end-to-end Agent engineering with Runtime orchestration.
---

# Agent Engineering Master

## Runtime First Architecture

This skill is the only recommended user entry point.

Execution pipeline:

```
User Goal
   ↓
Runtime Bootstrap
   ↓
Skill Registry
   ↓
Skill Router
   ↓
Skill Loader
   ↓
Policy Check
   ↓
Execute Skill
   ↓
Evaluation
   ↓
State Update
```

## Responsibilities

Master负责：

- 理解最终目标
- 判断任务类型
- 调度 Runtime
- 选择 Primary Skill
- 选择 Supporting Skill
- 管理项目状态
- 触发安全检查
- 验证最终结果

专项 Skill 负责：

- 专业领域执行
- 领域知识处理
- 具体工程操作

## Skill Loading Rules

禁止直接扫描全部 Skill。

必须经过：

1. Registry
2. Router
3. Loader

限制：

- Primary Skill: 1
- Supporting Skill: <=2

## Project Artifact Rules

所有项目级文档默认中文：

```
项目状态.yaml
边界画布.md
决策记录.md
当前会话.md
项目调研.md
架构设计.md
影响分析.md
验证报告.md
```

Skill 内部协议保持英文。

## Safety Rules

涉及以下内容必须经过 Policy Engine：

- 数据库
- 文件系统
- 外部 API
- Email
- MCP Tool
- 医疗数据
- 金融数据
- 权限变更

## Completion Lifecycle

```
Plan
 ↓
Execute
 ↓
Verify
 ↓
Evaluate
 ↓
Update State
 ↓
Archive Decision
```
