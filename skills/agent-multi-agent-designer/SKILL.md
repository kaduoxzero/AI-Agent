---
name: agent-multi-agent-designer
description: Design, review, or refactor Multi-Agent systems with clear role boundaries, supervisor or handoff control, typed artifacts, shared state, concurrency, permissions, and failure handling. Use when a project genuinely needs multiple specialized Agents, parallel expert work, delegation, debate, voting, blackboard coordination, or distributed Agent collaboration.
---

# Multi-Agent Designer

## Objective

设计真正有职责边界的 Multi-Agent 系统，避免“多个 Prompt = 多智能体”的伪架构。

## First Question

先证明为什么 Single Agent 不够。

只有满足以下至少一个条件时才优先 Multi-Agent：

- 权限边界不同；
- Context 需要隔离；
- 专业工具集明显不同；
- 子任务可并行；
- 需要独立评审 / 对抗；
- 单 Agent Prompt 已经复杂到不可维护；
- 不同任务生命周期需要独立恢复；
- 跨系统或跨团队 Agent 需要互操作。

## 1. Agent Boundary Contract

每个 Agent 都必须定义：

```text
Agent ID:
Goal:
Inputs:
Outputs:
Tools:
Permissions:
Context:
Memory:
State ownership:
Failure behavior:
Timeout:
```

如果两个 Agent 大部分字段相同，应重新考虑是否合并。

## 2. Select Coordination Pattern

### Supervisor

适合中央统一调度：

```text
User
→ Supervisor
→ Worker A / B / C
→ Supervisor
→ Final Artifact
```

风险：Supervisor 变成瓶颈和单点决策中心。

### Hierarchical

适合多层管理和大型任务拆解。

不要为了“组织结构好看”增加层级。

### Orchestrator-Workers

适合运行时动态拆分多个独立子任务并汇总。

### Handoff

适合一个 Agent 将控制权转交给另一个 Agent。

必须定义 Handoff Artifact，而不是直接拼接全部聊天历史。

### Chain-of-Experts

适合稳定的专家流水线。

### Debate / Voting

用于高不确定判断或需要独立观点时。

不要用 Debate 代替确定性规则。

### Blackboard / Shared State

适合多个 Agent 围绕共享工作区协作。

必须定义字段所有权和并发写策略。

### Swarm

仅在去中心化、动态协作本身确有价值时使用。

不要把 Swarm 当默认高级形态。

## 3. Control Ownership

任何时刻都必须能回答：

> 谁决定下一步？

控制权只能清晰存在于：

- Supervisor；
- Graph Router；
- 当前 Agent；
- deterministic state machine。

避免多个 Agent 同时认为自己拥有全局控制权。

## 4. Typed Artifact Between Agents

推荐：

```text
ResearchAgent
  ↓ ResearchReport
RiskAgent
  ↓ RiskAssessment
ReviewerAgent
  ↓ ReviewDecision
Finalizer
```

每一步用结构化 Artifact，而不是自由文本消息作为唯一接口。

## 5. Shared State Rules

共享 State 时定义：

- owner；
- read/write permissions；
- reducer / merge；
- version；
- conflict strategy；
- immutable fields；
- audit event。

禁止多个 Agent 随意覆盖同一大字典。

## 6. Context Isolation

每个 Agent 只接收完成任务需要的上下文。

不要默认把：

- 全部用户历史；
- 全部 Tool 输出；
- 全部 Agent 思考记录；
- 全部知识库结果；

广播给所有 Agent。

## 7. Permission Isolation

Agent Tool 权限应按职责分配：

```text
Research Agent → read/search
Risk Agent → read/score
Action Agent → write/execute + HITL
Reviewer Agent → read/review
```

高权限 Tool 不应因为某个 Agent “可能会用”就全局开放。

## 8. Parallelism

只有无依赖的任务才能并行。

设计：

```text
Fan-out
→ Parallel Workers
→ Typed Results
→ Fan-in
→ Merge / Judge
```

必须处理：

- partial failure；
- timeout；
- duplicate result；
- ordering；
- cancellation；
- result merge。

## 9. Loop Safety

Multi-Agent 特别容易出现 Handoff Loop。

必须限制：

- max handoffs；
- max rounds；
- max agent calls；
- max total cost；
- repeated route detection。

## 10. Evaluation

分别评估：

- 每个 Agent 的局部任务；
- Handoff 正确率；
- Artifact Contract；
- Supervisor 路由；
- 最终任务质量；
- Token / Latency / Cost；
- 单 Agent Baseline 对比。

Multi-Agent 必须证明比 Single Agent Baseline 有真实收益。

## 11. Migration From Single Agent

推荐：

```text
Identify overloaded responsibility
→ Extract typed contract
→ Extract one worker
→ Parity test
→ Add routing
→ Observe
→ Continue only if beneficial
```

不要一次拆成五六个 Agent。

## Anti-Patterns

- 一个 Agent 一个角色名，但工具完全相同；
- Supervisor 每一步都调用 LLM；
- Worker 之间用超长自然语言传状态；
- 所有 Agent 共享全部 Memory；
- Debate 没有终止条件；
- Voting 的多个 Agent 实际使用同一 Prompt / Context 导致伪独立；
- Multi-Agent 没有 Single Agent 对照评测。

## Completion Criteria

- 每个 Agent 有明确存在理由；
- Control Ownership 清晰；
- Agent 间使用 Typed Artifact；
- 权限按最小原则隔离；
- Loop 有硬上限；
- 并行路径有失败策略；
- 有 Single Agent Baseline；
- Multi-Agent 的质量收益足以覆盖新增成本和复杂度。
