# Agent Engineering Session State

> 用于让 Agent 在多轮任务中记住当前进行到哪一步、哪些问题已解决、哪些边界还未确定。对应项目状态文件：`.agent-engineering/current-session.md`。

## Session

- Project:
- Mode: Greenfield / Existing Project
- Current Stage:
- Primary Goal:
- Primary Skill:
- Supporting Skills:

## Stage Status

| Stage | Topic | Status | Notes |
|---|---|---|---|
| 0 | Problem Framing | Pending | |
| 1 | Success / Failure | Pending | |
| 2 | Architecture Level | Pending | |
| 3 | Autonomy Boundary | Pending | |
| 4 | Knowledge Boundary | Pending | |
| 5 | Tool / Side Effect Boundary | Pending | |
| 6 | State / Memory / Checkpoint | Pending | |
| 7 | Multi-Agent Boundary | Pending | |
| 8 | Runtime / Reliability | Pending | |
| 9 | Identity / Security / HITL | Pending | |
| 10 | Evaluation | Pending | |
| 11 | Observability / Operations | Pending | |
| 12 | Architecture Freeze | Pending | |
| 13 | Incremental Build | Pending | |

Status values:

- `Pending`
- `In Progress`
- `Resolved`
- `Deferred`
- `Not Required`
- `Blocked`

## Resolved Facts

- 

## Accepted Decisions

- 

## Deferred Decisions

- 

## Open Questions

只保留真正未解决、会影响架构或实现的问题：

1. 

## Current Recommendation


## Next User Decision

一次只暴露一个主要决策：

```text
Question:
A.
B.
C.
Recommended:
Why:
Boundary Impact:
```

## Agent Can Decide Without Asking

- 命名细节
- 私有函数拆分
- 小范围目录组织
- 不改变外部行为的实现细节
- 测试辅助代码
- 明显符合现有代码规范的实现选择

## Agent Must Surface Before Proceeding

- 业务目标变化
- Agent / Workflow / Multi-Agent 层级变化
- 新增高风险 Tool
- 新增外部副作用
- 权限模型变化
- 数据边界变化
- 破坏性 API / Schema 变化
- 成本等级明显变化
- 无法回滚的 Migration

## Resume Instruction

当会话继续时：

1. 先读取本 Session State；
2. 不重复询问 `Resolved Facts`；
3. 从 `Current Stage` 恢复；
4. 仅询问 `Next User Decision`；
5. 决策完成后同步更新 Decision Ledger 和 Boundary Canvas。
