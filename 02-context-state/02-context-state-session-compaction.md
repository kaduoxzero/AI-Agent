# Context Engineering、State、Session 与 Compaction

## 1. 为什么 Context Engineering 比 Prompt 更大

Agent 运行时模型实际看到的不只是 Prompt，而是：

```text
System Prompt
+ User Messages
+ Tool Schemas
+ Tool Results
+ Retrieved Documents
+ Memory
+ State Summary
+ Previous Agent Outputs
```

所以真正的问题是：

> 在有限 Context Window 中，当前这一步到底应该让模型看到什么？

这就是 Context Engineering。

## 2. 五个容易混淆的概念

### Prompt

对模型的指令。

### Context

当前一次模型调用可以读取的全部信息。

### State

程序层保存的任务状态，不要求全部发送给模型。

### Session

一段连续交互的逻辑会话，用于关联 History、State、Memory 等。

### Memory

需要跨 Step 或跨 Session 保留并可再次使用的信息。

## 3. State 设计

推荐显式 State Schema：

```python
class AgentState(TypedDict):
    task_id: str
    query: str
    plan: list[str]
    current_step: int
    evidence: list[dict]
    errors: list[str]
    retry_count: int
    status: str
```

State 不应该变成“所有信息大垃圾桶”。

按职责拆：

```text
Task State
Execution State
Business State
Evidence State
Control State
```

## 4. Context Selection

每次模型调用只选择必要内容。

例如 Reviewer 需要：

```text
Task Requirement
Final Draft
Evaluation Rubric
Key Evidence
```

通常不需要看到 Worker 的全部原始日志。

## 5. Context Pollution

**专业名词通义：Context Pollution**

无关、错误、重复或恶意信息持续进入上下文，使后续模型判断质量下降。

常见来源：

- 大量 Tool 原始响应；
- 已失效的历史计划；
- 前一轮错误推理产物；
- 网页中的 Prompt Injection；
- 多 Agent 互相复制长文本。

## 6. Context Compaction

长任务不能无限把历史消息原样追加。

Compaction 是将历史信息压缩成更短但可继续工作的表示。

```text
Raw History
 ↓
Summarize / Extract State
 ↓
Compact Context
 ↓
Continue Agent
```

压缩时要区分：

### 可以摘要

- 一般对话；
- 已完成步骤；
- 长 Tool Result。

### 不应只摘要

- 精确 ID；
- API 参数；
- 金额；
- 权限结果；
- 必须引用的原始证据。

这些应保存为结构化 State 或外部 Artifact。

## 7. Session

Session 至少绑定：

```text
session_id
user_id / tenant_id
task_id
message_history
state_pointer
memory_scope
```

不要只把 Session 理解为聊天记录。

## 8. Checkpoint 与 Session 的区别

- Session：逻辑会话；
- Checkpoint：执行状态的可恢复快照。

一个 Session 可以产生多个 Checkpoint。

```text
Session
├─ Checkpoint 1
├─ Checkpoint 2
└─ Checkpoint 3
```

## 9. Multi-Agent Context Isolation

多 Agent 不应该默认共享完整 Context。

推荐：

```text
Shared Task State
+ Agent-local Context
+ Explicit Handoff Payload
```

这样可以：

- 控制 Token；
- 降低隐私泄露；
- 防止 Context 污染；
- 让 Agent 边界更清楚。

## 10. Context Budget

为不同节点设置预算：

```yaml
planner:
  max_context_tokens: 30000
reviewer:
  max_context_tokens: 20000
worker:
  max_context_tokens: 50000
```

Context 预算与 Model Budget 一样应该被观测。

## 11. 工程实现建议

构建 Context Builder：

```python
class ContextBuilder:
    def build(self, state, role, budget):
        # 选择 Prompt
        # 选择相关 Memory
        # 选择 Evidence
        # 对历史做 Compaction
        # 最终控制 Token Budget
        ...
```

不要让每个 Node 各自拼字符串。

## 12. 检查清单

- [ ] Prompt、Context、State、Memory 是否明确区分？
- [ ] State 是否有 Schema？
- [ ] 是否限制 Tool Result 进入 Context 的大小？
- [ ] 长任务是否有 Compaction？
- [ ] 精确数据是否保留结构化原始值？
- [ ] Multi-Agent 是否做到 Context Isolation？
- [ ] 是否可以从 Checkpoint 恢复？
