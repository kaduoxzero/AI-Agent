# Agent Runtime、Runner 与 Harness

## 1. 为什么 Agent 不只是一个模型

模型只负责推理。真正让 Agent 长时间工作的是 Runtime。

```text
                 Agent Definition
                       ↓
Input → Runner → Agent Loop
                 ├─ Context Builder
                 ├─ Tool Executor
                 ├─ State Store
                 ├─ Permission
                 ├─ Checkpoint
                 ├─ Trace
                 └─ Budget
```

## 2. Runtime

Runtime 负责“怎么执行”。

常见职责：

- Turn / Step；
- Tool Dispatch；
- State Update；
- Loop；
- Retry；
- Stop；
- Streaming；
- Cancellation；
- Resume；
- Trace。

### 专业名词通义：Turn

一次模型生成通常称为一个 Turn。一个 Turn 内可能产生一个或多个 Tool Call；Tool 执行后往往需要新的 Turn。

## 3. Runner

Runner 是发起和管理一次 Agent Run 的执行器。

可能负责：

```text
initialize context
run loop
handle handoff
execute tools
apply guardrails
emit events
return RunResult
```

## 4. Harness

Harness 是面向长、多步骤任务的更完整执行外壳。

现代 Harness 常见：

```text
Planning Mode
Todo Tracking
Context Compaction
Filesystem
Skills
Memory
Shell / Tools
Tool Approval
Observability
```

Microsoft Agent Framework 当前就将 Harness 明确作为 Agents 与 Workflows 之外的一级能力。

## 5. 为什么 Coding Agent 特别需要 Harness

Coding Agent 需要持续维护一个“工作世界”：

```text
Repository
Files
Git Diff
Tests
Shell State
Todo
Task Spec
Previous Attempts
```

单纯把这些全部塞 Conversation 不现实。

## 6. Todo / Planning

长任务应该显式维护：

```json
[
  {"task": "定位异常", "status": "done"},
  {"task": "修改实现", "status": "doing"},
  {"task": "增加回归测试", "status": "todo"}
]
```

Todo 不是展示用 UI，而是 Agent 的控制状态。

## 7. Run State 与 Business State

建议分离：

### Runtime State

- step；
- model calls；
- budget；
- pending approval。

### Business State

- report；
- patient data；
- order state。

这样 Runtime 不侵入业务模型。

## 8. Cancellation

大型任务必须支持取消。

```text
User cancel
 ↓
Task Service marks cancelling
 ↓
Worker receives signal
 ↓
stop new tool calls
 ↓
save checkpoint
 ↓
cancelled
```

不能依靠直接 kill 进程。

## 9. Budget

Runtime 应强制：

```text
max_turns
max_tool_calls
max_delegations
max_tokens
max_cost
max_duration
```

模型自己说“我会控制成本”不能代替 Runtime Budget。

## 10. Event Model

成熟 Runtime 应输出事件：

```text
RunStarted
TurnStarted
ModelCalled
ToolCalled
ToolCompleted
StateUpdated
Handoff
ApprovalRequested
CheckpointSaved
RunCompleted
RunFailed
```

UI、Trace、Eval 都可以消费统一 Event。

## 11. Runtime 架构示例

```text
API
 ↓
Task Service
 ↓
Queue
 ↓
Agent Worker
  ├─ Runner
  ├─ Context Builder
  ├─ Tool Executor
  ├─ Checkpoint Repository
  ├─ Event Publisher
  └─ Trace Exporter
```

## 12. 检查清单

- [ ] Agent Loop 是否有 Runtime 强制预算？
- [ ] 是否支持 Cancel？
- [ ] 是否支持 Checkpoint / Resume？
- [ ] 是否有 Event Model？
- [ ] Runtime State 与业务 State 是否分开？
- [ ] 长任务是否有 Todo / Planning？
- [ ] Context 是否支持 Compaction？

## 13. 参考

- Microsoft Agent Framework Harness：https://learn.microsoft.com/en-us/agent-framework/get-started/harness
