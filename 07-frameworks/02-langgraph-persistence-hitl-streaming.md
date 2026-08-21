# LangGraph 高级工程：Persistence、Checkpoint、HITL、Streaming 与 Memory

## 1. 长任务为什么必须 Persistence

普通函数失败后从头运行即可；大型 Agent 可能已经：

- 搜索 20 次；
- 调用多个外部 API；
- 产生业务副作用；
- 等待人工审批。

因此需要 Durable Execution。

## 2. Checkpoint

LangGraph Persistence 会将 Graph State 保存为 Checkpoint，并按 Thread 组织。

```text
Thread 123
├─ checkpoint 1
├─ checkpoint 2
├─ checkpoint 3
└─ checkpoint 4
```

### 专业名词通义：Checkpoint

一次工作流状态快照，可用于恢复、调试或分叉执行。

## 3. Thread

Thread 是一系列相关 Graph Run 的持久状态标识。

通常通过 `thread_id` 找到对应 Checkpoint。

不要与 OS Thread 混淆。

## 4. Persistence 带来的能力

### Human-in-the-loop

暂停、人工修改 / 审批、继续。

### Conversation Memory

同一个 Thread 可以继续保留短期状态。

### Time Travel

读取过去 Checkpoint，重放或从历史状态 fork 新轨迹。

### Fault Tolerance

失败后从最后成功步骤继续。

## 5. interrupt / resume

典型节点：

```python
from langgraph.types import interrupt

def approval_node(state):
    decision = interrupt({
        "action": state["pending_action"],
        "risk": "high"
    })
    return {"approved": decision}
```

恢复时通过 Command 提供 resume value。

## 6. interrupt 的关键陷阱

LangGraph 恢复时节点会从节点开头重新执行，而不是 Python 精确从 `interrupt()` 下一行继续。

因此 interrupt 前的副作用必须幂等。

错误：

```text
charge_payment()
interrupt("approve?")
```

恢复时可能再次执行 charge。

正确：

```text
prepare_payment()
interrupt(approval_payload)
execute_payment(idempotency_key)
```

## 7. Streaming

Agent 延迟高，不能只在最终结束时一次返回。

需要流出：

- Token；
- Node Status；
- State Update；
- Tool Call；
- SubGraph Progress；
- Interrupt Event；
- Custom Event。

前端可以显示：

```text
[✓] 理解问题
[✓] 查询知识库
[→] 正在分析 12 份资料
[ ] 生成报告
```

这比只显示“正在思考”更有产品价值。

## 8. Short-Term 与 Long-Term Memory

LangGraph / LangChain 体系中应区分：

- Thread-scoped short-term state；
- Store 中跨 Thread 的 long-term memory。

不要把 Checkpointer 当成所有长期知识的数据库。

## 9. Pending Writes / Parallel Failure

并行 superstep 中，有些 Node 成功、有些失败时，成熟的 persistence 应避免成功节点无意义重跑。

设计自定义 Runtime 时也应借鉴这种思想：

```text
Parallel Tasks
├─ A success
├─ B success
└─ C fail
```

恢复时优先只重试 C。

## 10. Production Checkpointer

开发：In-memory 可以。

生产：应使用 durable database / supported persistent backend。

要求：

- 高可用；
- Tenant 隔离；
- 生命周期清理；
- 数据加密；
- 备份；
- 迁移策略。

## 11. Functional API 与 Graph API

如果现有 Python 逻辑已经大量使用 `if / loop / function`，可以考虑 Functional API 来获得 persistence、memory、HITL、streaming，而不是强行重构成显式 Graph。

如果需要固定拓扑、可视化、复杂 fan-out/fan-in，则 Graph API 更自然。

## 12. 检查清单

- [ ] 长任务是否有 durable checkpoint？
- [ ] 是否定义 thread_id / task_id 关系？
- [ ] interrupt 前副作用是否幂等？
- [ ] Streaming 是否包含任务进度而不只是 Token？
- [ ] Checkpoint 是否有清理策略？
- [ ] 是否区分 short-term state 和 long-term memory？

## 13. 参考

- Persistence：https://docs.langchain.com/oss/python/langgraph/persistence
- Interrupts：https://docs.langchain.com/oss/python/langgraph/interrupts
- Streaming：https://docs.langchain.com/oss/python/langgraph/streaming
