---
name: agent-engineering-master
description: Master entry skill for end-to-end Agent engineering. Load this single skill when the user wants to design, build, modify, debug, evaluate, secure, optimize, productionize, or evolve an Agent system. It dynamically selects other skills while maintaining project-scoped engineering state.
---

# Agent Engineering Master

## 1. Role

这是整个 skills 体系的唯一推荐入口（Master / Aggregation Skill）。

用户只需要调用本 Skill。Master 负责：

- 理解用户目标
- 判断项目阶段
- 管理工程状态
- 选择专项 Skill
- 组织执行流程
- 验证结果
- 保证边界、安全和一致性

专项 Skill 负责专业执行，Master 不替代专项能力。

---

# 2. Runtime Bootstrap（强制）

加载本 Skill 后，必须先执行 Runtime Bootstrap。

执行顺序：

```
Load Master Skill
        ↓
Resolve SKILL_ROOT
        ↓
Load Runtime Resources
        ↓
Resolve PROJECT_ROOT
        ↓
Resolve PROJECT_STATE_ROOT
        ↓
Load Project State
        ↓
Route Task
```

## 2.1 Skill Root Resolution

禁止从当前工作目录猜测 Skill 文件。

所有 Master 内部资源必须基于：

```
<SKILL_ROOT>
```

解析。

资源优先级：

```
<SKILL_ROOT>/resources/
        ↓
<SKILL_ROOT>/
        ↓
安全默认规则
```

如果资源不存在：

- 不终止任务；
- 进入 Safe Fallback Mode；
- 保留安全边界。

---

# 3. Project Root Resolution

优先级：

1. 用户明确指定项目目录；
2. 当前 Git Repository Root；
3. 包含主要构建文件的目录；
4. 无法安全判断时询问用户。

禁止：

- 把 skills 目录作为业务项目；
- 把多个项目共享同一个状态目录。

---

# 4. Project State Management

每个项目独立维护：

```
<project>/.agent-engineering/
```

禁止跨项目共享状态。

项目文档默认中文：

```
项目状态.yaml
边界画布.md
决策记录.md
当前会话.md
项目调研.md
架构设计.md
影响分析.md
验证报告.md
历史记录/
```

Skill 内部协议名称保持英文，不影响项目文档语言。

---

# 5. State Isolation Rules

模板：

```
skills/templates/
```

只读。

允许：

- 读取
- 复制
- 初始化

禁止：

- 保存项目状态
- 保存用户决策
- 保存运行记录

项目状态：

```
<project>/.agent-engineering/
```

---

# 6. Dynamic Skill Routing

Master 不要求用户了解 Skill 名称。

根据：

- 任务目标
- 项目阶段
- 风险
- 缺失能力
- 修改范围

动态选择。

流程：

```
Observe
 ↓
Identify Gap
 ↓
Boundary Check
 ↓
Select Skill
 ↓
Execute
 ↓
Verify
 ↓
Update State
 ↓
Continue / Finish
```

---

# 7. Skill Selection Rules

## 新项目

```
Guided Builder
        ↓
Greenfield Builder
        ↓
RAG / Multi-Agent / Security / Eval
        ↓
Productionizer
```

## 已有项目

```
Existing Project Modifier
        ↓
Debugger / Architecture Reviewer
        ↓
专项 Skill
        ↓
Verification
```

---

# 8. Mandatory Escalation

以下情况必须追加检查：

## Security

- 数据库
- 外部工具
- Secret
- 权限
- 医疗金融场景
- Memory
- MCP

## Eval

- 修改 Prompt
- 修改模型
- 修改 Router
- 修改 RAG
- 修改 Agent 状态

## Production

- API 服务
- 多用户
- Queue
- Worker
- Retry
- Checkpoint
- Docker/Kubernetes

---

# 9. Composition Rule

同一阶段：

- 1 个 Primary Skill
- 最多 2 个 Supporting Skill

禁止无目的加载全部 Skill。

---

# 10. User Interaction Policy

不要让用户负责 Skill 调度。

正常情况下直接完成工程流程。

只有以下情况询问：

- 不同业务目标
- 不可逆操作
- 权限风险
- 无法判断项目归属
- 高影响架构选择

---

# 11. Completion Standard

任务完成必须满足：

```
Implementation
        ↓
Verification
        ↓
State Update
        ↓
Final Summary
```

Master 的目标不是生成代码，而是保证 Agent 工程生命周期正确完成。
