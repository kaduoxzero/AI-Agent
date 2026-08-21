# Multi-Agent 架构设计与职责拆分

## 1. Multi-Agent 的核心不是 Agent 数量

Multi-Agent 的价值来自职责隔离和协作，而不是“多开几个模型”。

合理例子：

```text
Orchestrator
├─ Research Agent：外部证据
├─ Data Agent：结构化数据
├─ Domain Agent：领域判断
└─ Reviewer：质量审查
```

不合理例子：

```text
Java Expert
Senior Java Expert
Very Senior Java Expert
```

如果它们目标、工具、Context 完全一致，这种拆分通常没有工程价值。

## 2. 拆 Agent 的五个依据

### 2.1 Goal Isolation

目标不同。

### 2.2 Tool Isolation

工具或权限不同。

### 2.3 Context Isolation

需要的信息不同。

### 2.4 Expertise / Policy Isolation

领域 Prompt、规则或 Eval 标准不同。

### 2.5 Independent Execution

子任务可以独立完成。

## 3. Agent Contract

每个 Agent 应定义契约：

```yaml
name: research-agent
goal: collect verifiable evidence
inputs:
  - research_question
outputs:
  schema: EvidenceBundle
tools:
  - web_search
  - document_fetch
permissions:
  write: false
handoff_to:
  - orchestrator
```

### 专业名词通义：Agent Contract

对 Agent 输入、输出、职责、权限和可委派对象的正式约定。

## 4. Shared State vs Local State

推荐：

```text
Global Task State
├─ goal
├─ status
├─ shared artifacts
└─ budgets

Agent-local State
├─ local plan
├─ local history
└─ local scratch data
```

不要把所有 Worker 原始消息都放 Shared State。

## 5. Context Isolation

Orchestrator 转交任务时只发送必要 Handoff Payload：

```json
{
  "task": "验证供应商A最近事件",
  "known_facts": [...],
  "constraints": [...],
  "expected_output": "EvidenceBundle"
}
```

Worker 不需要自动继承整个主会话。

## 6. Delegation

委派必须有限制：

```text
max_delegation_depth
allowed_handoffs
max_workers
max_subtasks
```

防止：

```text
A → B → C → A → ...
```

## 7. Communication Models

### 中央式

```text
Worker → Supervisor → Worker
```

最容易控制。

### Handoff

```text
Agent A → Agent B
```

任务所有权发生转移。

### Blackboard

```text
Agent A ─┐
Agent B ─┼→ Shared State / Blackboard
Agent C ─┘
```

### 去中心化

Agent 自行发现和协作，灵活但难控制。

## 8. Failure Propagation

Multi-Agent 中错误会传播。

设计：

```text
Worker Result
 ↓
Schema Validation
 ↓
Confidence / Evidence Check
 ↓
Orchestrator accepts or retry
```

不要默认信任 Worker 输出。

## 9. Cost

总成本近似：

```text
Σ Agent Model Calls
+ Tool Calls
+ Shared Context Duplication
+ Review Calls
```

Agent 数增加经常造成 Context 重复。

## 10. 检查清单

- [ ] 每个 Agent 是否有独立 Goal？
- [ ] 是否存在工具或 Context 隔离收益？
- [ ] 是否定义 Agent Contract？
- [ ] Handoff Payload 是否最小化？
- [ ] 是否限制委派深度？
- [ ] Worker 结果是否校验？
- [ ] 是否统计每个 Agent 的成本和成功率？
