# Agent Backend：长任务、Queue、Checkpoint 与任务状态机

## 1. 为什么大型 Agent 不能直接绑 HTTP 请求

简单 Demo：

```text
POST /chat
 ↓
run agent 60s
 ↓
HTTP response
```

生产问题：

- 网关超时；
- 页面刷新任务丢失；
- Worker Crash 无法恢复；
- 无法取消；
- 无法排队和限流。

因此长任务应该是独立 Task Resource。

## 2. 推荐架构

```text
Frontend
 ↓ POST /tasks
API Service
 ↓ create task
PostgreSQL
 ↓ enqueue
Message Queue
 ↓
Agent Worker
├─ Runtime
├─ Checkpoint
├─ Tools
└─ Event Publisher
 ↓
Task Events / Artifacts
 ↓
Frontend SSE / WebSocket
```

## 3. Task State Machine

推荐明确状态：

```text
PENDING
 ↓
RUNNING
 ├→ WAITING_APPROVAL
 ├→ WAITING_INPUT
 ├→ RETRYING
 ├→ COMPLETED
 ├→ FAILED
 └→ CANCELLING → CANCELLED
```

### 专业名词通义：State Machine

规定 Task 可以有哪些状态，以及哪些状态之间允许转换。

不要用一个 `status: string` 随意赋值。

## 4. Task Schema

```sql
agent_task(
    id,
    tenant_id,
    user_id,
    agent_type,
    status,
    input_ref,
    checkpoint_ref,
    result_ref,
    trace_id,
    created_at,
    started_at,
    finished_at,
    version
)
```

大输入 / 大结果放 Object Storage，DB 保存引用。

## 5. Queue

Queue 用于：

- 削峰；
- 异步；
- Worker 扩缩容；
- Retry；
- 优先级。

可以使用 RabbitMQ、Kafka、Redis Stream、云队列等，选择取决于可靠性和吞吐需求。

Agent Task 一般不是“超高 TPS 极短任务”，而是低到中等 QPS、执行时间长，所以要特别关注 in-flight task 和 worker capacity。

## 6. Worker Lease

避免两个 Worker 同时执行一个 Task。

可以使用：

```text
DB optimistic lock
queue ack
lease / heartbeat
```

Worker 长时间无 heartbeat 后，Task 可重新调度。

## 7. Checkpoint

Checkpoint 不能只保存“当前 Node 名”。

至少考虑：

```text
workflow state
completed steps
pending actions
budget usage
external ids
sandbox state reference
```

## 8. Side Effect 与 Exactly Once

分布式系统很难保证真正 Exactly Once。

更实际的方法：

```text
At-least-once delivery
+ Idempotent Tool
+ Idempotency Key
```

例如：

```text
send_report(task_id, report_version)
```

重复执行不会发送两次。

## 9. Cancellation

取消不是 `kill -9`。

设计：

```text
API sets CANCELLING
 ↓
worker checks cancel flag between steps
 ↓
stop new side effects
 ↓
save checkpoint / cleanup sandbox
 ↓
CANCELLED
```

对于无法中断的外部 Tool，需要等待返回或使用 Tool 自身 cancel API。

## 10. Approval / Input Waiting

Task 等待人工时不能占着 Worker 进程。

正确：

```text
save checkpoint
status=WAITING_APPROVAL
release worker
```

用户审批后重新入队恢复。

## 11. Retry

区分：

```text
LLM retry
Tool retry
Node retry
Task retry
```

不要整个 Task 一失败就从头重跑。

## 12. Dead Letter

超过最大重试次数的任务进入 Dead Letter Queue / Failed Store，由运营或自动补偿处理。

## 13. API 设计

```text
POST /tasks
GET /tasks/{id}
GET /tasks/{id}/events
POST /tasks/{id}/cancel
POST /tasks/{id}/resume
POST /tasks/{id}/approvals/{approval_id}
GET /tasks/{id}/artifacts
```

这比只有 `/chat` 更适合复杂 Agent 产品。

## 14. 检查清单

- [ ] 长任务是否脱离 HTTP 生命周期？
- [ ] Task 是否有状态机？
- [ ] Worker Crash 是否能恢复？
- [ ] Side Effect 是否幂等？
- [ ] WAITING 状态是否释放 Worker？
- [ ] 是否支持 Cancel？
- [ ] 是否有 Dead Letter？
- [ ] Task / Trace / Artifact 是否关联？
