# Event-Driven 与 Proactive Agent

> 目标：跳出“用户发一句话，Agent 回一句话”的 Chat 范式，掌握真正企业自动化常见的事件驱动 Agent。

## 1. 为什么需要 Event-Driven Agent

大量生产 Agent 并不是聊天触发，而是：

```text
Cron
Webhook
Message Queue
Database Change
CDC
Monitoring Alert
Email Event
File Upload
IoT Event
```

触发。

例如：

```text
Prometheus Alert
 ↓
Incident Agent
 ↓
查日志 / Trace / Metrics
 ↓
生成诊断
 ↓
低风险自动修复
高风险等待审批
```

## 2. 专业名词通义

- **Event-Driven（事件驱动）**：系统因为“某件事发生了”而启动处理，而不是等待同步请求。
- **Proactive Agent（主动型 Agent）**：无需当前用户聊天请求，也能根据计划、条件或事件主动执行任务。
- **Trigger（触发器）**：启动 Agent Run 的来源，例如 Cron、Webhook、Queue Message。
- **CDC（Change Data Capture）**：捕获数据库数据变化并转换成事件。
- **Event Bus（事件总线）**：发布和订阅事件的基础设施。
- **Replay（重放）**：重新消费历史事件，用于恢复或重新计算。

## 3. 总体架构

```text
Event Sources
├─ Cron
├─ Webhook
├─ MQ
├─ CDC
├─ Alert
└─ Email
   ↓
Event Gateway
   ↓
Filter / Dedup / Policy
   ↓
Task Service
   ↓
Queue
   ↓
Agent Runtime
   ↓
Artifact / Action / Notification
```

## 4. Event 不等于 Prompt

错误设计：

```text
Kafka message
 ↓
字符串拼成 Prompt
 ↓
LLM
```

推荐先转换成 Typed Event：

```python
class BusinessEvent(BaseModel):
    event_id: str
    event_type: str
    tenant_id: str
    occurred_at: datetime
    subject_id: str
    payload_ref: str | None
    metadata: dict
```

然后由确定性 Router 判断是否需要 Agent。

## 5. Trigger Policy

不是所有事件都应该触发 LLM。

```text
Event
 ↓
Deterministic Filter
 ├─ ignore
 ├─ aggregate
 ├─ rule action
 └─ create agent task
```

例如 CPU 瞬时 81% 不一定要启动一个 Incident Agent。

## 6. Idempotency

消息系统可能重复投递。

必须：

```text
event_id → idempotency_key
```

保证相同 Event 不会：

- 重复下单；
- 重复发邮件；
- 重复写 Memory；
- 重复创建 Task。

## 7. Debounce 与 Aggregation

高频事件不要每个都启动 Agent。

```text
100 alerts / 30s
 ↓
Aggregate by service
 ↓
1 incident task
```

专业名词：

- **Debounce**：短时间连续事件只触发一次。
- **Aggregation**：把多个相关事件合成一个上下文。

## 8. Scheduled Agent

定时 Agent：

```text
Scheduler
 ↓
Task Template
 ↓
Agent Run
```

配置应包含：

```yaml
schedule: "0 8 * * *"
agent_id: morning-risk-report
max_duration: 600
budget_usd: 1.0
failure_policy: notify
```

不能让 Agent 自己无限“记住下一次什么时候运行”。

## 9. Conditional Watch

例如：

```text
每小时检查库存风险
只有 risk >= high
才生成通知
```

应该拆成：

```text
Scheduler
 ↓
Check
 ↓ condition false → complete silently
   condition true  → Agent / Notification
```

## 10. Event Security

外部 Webhook 是输入攻击面。

必须：

- 验签；
- Replay Protection；
- Schema Validation；
- Tenant Resolution；
- Rate Limit；
- Payload Size Limit；
- Prompt Injection Isolation。

Event Payload 不能直接拥有更高 Prompt 优先级。

## 11. Long-Running Event Task

事件触发的 Agent 仍然要进入统一 Task System：

```text
Event
 ↓
Task CREATED
 ↓
QUEUED
 ↓
RUNNING
 ↓
WAITING_APPROVAL / COMPLETED / FAILED
```

不要写成 MQ Consumer 中一个超长同步函数。

## 12. Dead Letter Queue

不能处理的 Event：

```text
retry exhausted
 ↓
DLQ
 ↓
operator inspect / replay
```

DLQ 中应保留：

```text
event_id
failure_reason
attempt_count
last_trace_id
payload_ref
```

## 13. Event-to-Agent Routing

示例：

```yaml
rules:
  - event_type: supplier.news.detected
    agent: supplier-risk-agent
  - event_type: payment.anomaly
    agent: fraud-agent
  - event_type: service.alert
    agent: incident-agent
```

复杂语义路由可以使用模型，但外层仍需白名单和安全策略。

## 14. Proactive Agent 的通知原则

主动 Agent 最容易“骚扰用户”。

建议：

```text
事件重要吗？
是否新增信息？
是否已通知？
是否达到用户阈值？
是否在 Quiet Hours？
```

通知本身也是受控 Action。

## 15. 实训

扩展毕业项目：

- 每小时触发 `supplier-risk-watch`；
- 读取最近变化而不是全量重跑；
- 只有高风险才创建完整 Research Task；
- 同一个 supplier 10 分钟内事件聚合；
- 任务失败进入 DLQ；
- 支持 Replay；
- Notification 保存 `task_id + evidence_refs`。

## 16. 检查清单

- [ ] Event 是否有 Schema 和唯一 ID？
- [ ] 是否先做确定性 Filter？
- [ ] 是否支持 Dedup / Idempotency？
- [ ] 是否做高频 Event Aggregation？
- [ ] 外部 Webhook 是否验签？
- [ ] Event Task 是否走统一 Runtime？
- [ ] Retry 失败是否进入 DLQ？
- [ ] 是否可以安全 Replay？