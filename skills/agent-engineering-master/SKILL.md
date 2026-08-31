---
name: agent-engineering-master
version: 2.0.0
description: Master entry skill for end-to-end Agent engineering with Runtime orchestration.
---

# Agent Engineering Master

## Runtime First Architecture

This skill is the only recommended user entry point.

Execution pipeline:

```text
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

## Bootstrap

Before dispatching any specialist skill, read:

```text
PROJECT-STATE-POLICY.md                 project state isolation rules (SSoT)
SKILL-REGISTRY.md                       capability registry and switching contracts (SSoT)
resources/PROJECT-DOCUMENT-NAMING.md    project artifact naming/language/history rules (SSoT)
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

所有项目级实例文档默认必须做到“**文件名中文 + 正文简体中文**”：

```text
项目状态.yaml
边界画布.md
决策记录.md
当前会话.md
项目调研.md
架构设计.md
影响分析.md
验证报告.md
```

硬性要求：

- 文档标题、章节名、表头、说明、检查清单、结论默认使用简体中文；
- 技术名词、代码标识符、Schema Key、API、库名可以保留英文；
- 不允许只把文件名改成中文而正文继续沿用英文模板；
- 用户明确指定其他语言时，以用户要求为准；
- Skill 内部协议保持英文。

项目状态文件统一使用 `.agent-engineering/项目状态.yaml`，禁止再以 `.agent-engineering/project.yaml` 作为项目实例文件判断入口。

## History Artifact Rules

归档文件必须使用固定宽度时间作为第一个排序键：

```text
.agent-engineering/history/YYYYMMDD-HHmmss-<task-id>-<中文主题>.md
```

要求：

- 时间字段全部补零；
- 使用 `项目状态.yaml` 中稳定的 `project_timezone`；
- 文件名字典序升序必须等于真实时间升序；
- 同秒冲突添加 `-01`、`-02` 序号；
- 不得混用日期格式或把 task-id 放在时间前面。

完整规则见 `resources/PROJECT-DOCUMENT-NAMING.md`。

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

```text
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
