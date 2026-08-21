# ADR：Architecture Decision Records

> ADR（Architecture Decision Record，架构决策记录）用于训练和沉淀“为什么这样设计”，而不仅仅记录“最后用了什么技术”。

## 1. 为什么 Agent 项目特别需要 ADR

Agent 系统存在大量没有唯一答案的设计问题：

```text
Workflow 还是 Agent？
Single Agent 还是 Multi-Agent？
MCP 还是内部函数？
共享 State 还是 Artifact？
同步执行还是 Queue Worker？
是否允许 Browser / Computer Use？
什么时候需要 HITL？
强模型还是模型路由？
```

如果只记录实现结果，半年后很难理解当时的约束和权衡。

## 2. 推荐模板

```markdown
# ADR-XXX：标题

## Status
Proposed / Accepted / Deprecated / Superseded

## Context
当前业务、技术和约束是什么？

## Decision
最终选择什么？

## Alternatives
考虑过哪些方案？

## Consequences
得到什么，同时付出什么？

## Validation
如何通过 Eval / Benchmark / Load Test 验证？

## Revisit Trigger
什么条件发生时应重新评审？
```

## 3. 推荐至少完成的 ADR

```text
ADR-001  为什么先采用 Single Agent Baseline
ADR-002  为什么引入 LangGraph / Workflow Engine
ADR-003  为什么 Tool 采用最小权限 Gateway
ADR-004  为什么 Checkpoint 使用 PostgreSQL
ADR-005  为什么 Agent 间使用 Typed Artifact
ADR-006  为什么长任务采用 Queue + Worker
ADR-007  为什么高风险 Action 强制 HITL
ADR-008  为什么引入 Model Gateway
ADR-009  为什么某些 Tool 使用 MCP、某些不用
ADR-010  为什么生产系统不采用 Swarm
ADR-011  为什么采用 Tenant-isolated RAG
ADR-012  为什么使用 AG-UI Event Model
```

## 4. 示例：是否拆 Multi-Agent

### Context

单 Agent 已完成 Research + RAG + Data，但 Context 过长，工具权限混杂，三个子任务可以并行。

### Decision

拆为 Research / RAG / Data Worker，由 Orchestrator 调度。

### Alternatives

- 保持 Single Agent；
- Chain-of-Experts；
- Swarm。

### Consequences

收益：

- 权限隔离；
- Context 隔离；
- 并行执行；
- 独立 Eval。

成本：

- 调度复杂；
- Artifact Schema；
- 更多模型调用；
- 更复杂 Trace。

### Validation

比较：

```text
Task Success
P95 Latency
Cost / Task
Tool Error
Context Tokens
```

如果质量收益不足以覆盖复杂度，则回退 Single Agent。

## 5. ADR 不是会议纪要

ADR 应足够短，但必须包含：

```text
为什么
替代方案
代价
如何验证
何时重评
```

## 6. 学习要求

毕业项目每个关键架构决策至少写一份 ADR。目标是训练工程师具备“可解释的架构决策能力”，而不是只会照着教程拼组件。