# Multi-Agent 协作模式：Supervisor、Handoff、Debate、Voting、Blackboard 与 Swarm

## 1. Supervisor / Hierarchical

```text
Supervisor
├─ Worker A
├─ Worker B
└─ Worker C
```

Supervisor 负责：

- Routing；
- Task Decomposition；
- Worker Selection；
- Progress；
- Join；
- Termination。

适合企业系统，因为控制点清楚。

## 2. Orchestrator-Workers

Hierarchical 的动态版本之一：Orchestrator 运行时决定 Worker Task。

对于 Deep Research、Coding 大任务尤其常见。

## 3. Chain-of-Experts

```text
Requirement Expert
 ↓
Architecture Expert
 ↓
Implementation Expert
 ↓
Security Reviewer
```

重点是固定专家顺序。

### 适合

需要明确审批链、每一阶段依赖上一阶段结果。

### 风险

上游错误会逐层传递。

## 4. Handoff

```text
Triage Agent
 ↓ handoff
Billing Agent
```

Handoff 与“Agent as Tool”不同：

- Agent as Tool：主 Agent 仍然拥有任务；
- Handoff：控制权 / 对话处理权转给另一个 Agent。

## 5. Debate

```text
               Pro Agent
              /
Problem → Contra Agent → Judge
              \
               Risk Agent
```

不同 Agent 被赋予不同分析立场。

### 适合

- 方案评审；
- 风险分析；
- 高价值决策辅助。

### 不适合

简单问题，因为 Token 成本会成倍增加。

## 6. Voting / Ensemble

```text
Agent A → high
Agent B → high
Agent C → medium
 ↓
Aggregator → high
```

### Weighted Voting

不同 Agent 有不同权重。

### 注意

多个 Agent 如果使用同一个模型、同样 Prompt 和相同数据，错误高度相关，投票不会神奇地产生独立判断。

需要差异性：

- 不同模型；
- 不同 Evidence；
- 不同 Role；
- 不同方法。

## 7. Blackboard / Shared State

```text
          Blackboard
       /      |       \
   Agent A Agent B Agent C
```

Agent 通过共享 State / Artifact 协作，而不是互相复制完整消息。

适合：

- 复杂项目；
- 多 Worker 写同一份任务状态；
- 大量中间 Artifact。

需要处理并发写冲突和 State Schema。

## 8. Swarm

去中心化协作：

```text
A ↔ B
↕   ↕
C ↔ D
```

没有唯一 Supervisor，Agent 根据当前任务自主选择其他 Agent。

### 优点

- 灵活；
- 局部自治；
- 可探索复杂组织。

### 缺点

- 难 Debug；
- 容易循环；
- 成本不可预测；
- 状态一致性困难；
- 安全治理更难。

普通企业项目不建议从 Swarm 起步。

## 9. 模式选择

| 场景 | 推荐 |
|---|---|
| 企业复杂任务 | Supervisor / Orchestrator |
| 专业固定审核链 | Chain-of-Experts |
| 客服专业转接 | Handoff |
| 多观点分析 | Debate |
| 分类集成 | Voting |
| 多 Agent 共享项目空间 | Blackboard |
| 高自治探索 | Swarm |

## 10. 组合模式

真实项目经常是：

```text
Supervisor
├─ Research SubGraph (MapReduce)
├─ Data Agent
└─ Reviewer (Evaluator-Optimizer)
```

Pattern 可以组合，不要追求“系统只能属于一种模式”。
