# Agent SRE：Reliability Engineering 与故障治理

> 目标：把 Agent 当成长期运行的生产服务，而不是“能跑起来就算成功”的 Demo。

## 1. 为什么 Agent 需要自己的 SRE 思维

Agent 系统的故障面比普通 CRUD 更大：

```text
Model Provider
Tool / MCP
Retriever
Vector DB
Queue
Checkpoint Store
Browser
Sandbox
Identity Provider
Human Approval
Multi-Agent Communication
```

任何一个依赖变慢或失败，都可能导致整个 Task 延迟、重复执行、成本失控或产生错误动作。

## 2. 专业名词通义

- **SRE（Site Reliability Engineering）**：用软件工程方法管理服务可靠性。
- **SLI（Service Level Indicator）**：实际测量指标，例如任务成功率、P95 延迟。
- **SLO（Service Level Objective）**：对 SLI 的目标，例如月任务成功率 >= 99%。
- **Error Budget（错误预算）**：SLO 允许的失败空间，用于平衡发布速度和稳定性。
- **Degraded Mode（降级模式）**：部分依赖不可用时，以受限能力继续服务。
- **Load Shedding（负载丢弃）**：过载时主动拒绝低优先级任务，保护核心服务。

## 3. Agent SLI

普通 API 只看 HTTP 200 不够。

推荐分层：

### Task SLI

```text
task_success_rate
task_completion_latency
cancel_success_rate
resume_success_rate
```

### Agent Quality SLI

```text
eval_pass_rate
citation_valid_rate
unsafe_action_rate
human_override_rate
```

### Dependency SLI

```text
model_error_rate
tool_error_rate
retrieval_error_rate
queue_lag
checkpoint_failure_rate
```

### Cost SLI

```text
cost_per_successful_task
tokens_per_task
wasted_tokens_on_failed_tasks
```

## 4. SLO 示例

```yaml
monthly:
  task_success_rate: ">= 99%"
  p95_task_latency: "<= 120s"
  critical_unsafe_action_rate: "0"
  checkpoint_resume_success: ">= 99.9%"
  p95_queue_wait: "<= 10s"
```

不同 Task Class 应有不同 SLO。

实时客服 Agent 和 30 分钟 Deep Research 不能用同一延迟目标。

## 5. Dependency Failure Matrix

设计前明确：

| 依赖失败 | 系统行为 |
|---|---|
| 强模型不可用 | Fallback 到备用模型或暂停高风险任务 |
| Search 不可用 | 仅使用内部 KB，并标记 Evidence 范围降低 |
| Vector DB 不可用 | 禁止生成声称基于内部知识的结论 |
| Approval Service 不可用 | 高风险 Action 保持 WAITING，不绕过审批 |
| Trace Backend 不可用 | 本地 Buffer / 异步补传，不阻塞核心任务 |
| Queue 过载 | Admission Control / Load Shedding |

## 6. Circuit Breaker

如果某 Tool 连续失败：

```text
CLOSED
 ↓ failures exceed threshold
OPEN
 ↓ cooldown
HALF_OPEN
 ↓ success
CLOSED
```

Agent Runtime 不应该每一轮都重新撞一个已知故障依赖。

## 7. Fallback

Fallback 必须事先定义，而不是让 LLM临场发挥。

例如：

```text
primary model → secondary model
primary search → backup search
web + kb → kb only degraded mode
realtime result → cached result with freshness warning
```

Fallback 后输出必须标记能力降低。

## 8. Graceful Degradation

降级不是静默“假装一切正常”。

Artifact 可以记录：

```json
{
  "degraded": true,
  "missing_capabilities": ["public_web_search"],
  "quality_warning": "External evidence unavailable"
}
```

## 9. Admission Control

长 Agent Task 成本高，不能无限入队。

入口应检查：

```text
queue depth
worker capacity
tenant quota
cost budget
priority
current provider health
```

然后决定：

```text
accept
queue
throttle
reject
```

## 10. Backpressure

如果 Worker 消费速度低于生产速度：

```text
Producer
 ↓ too fast
Queue grows
 ↓
Backpressure
 ↓
throttle upstream
```

不要依靠无限扩容解决所有问题。

## 11. Runbook

每个关键故障应有 Runbook：

```text
症状
告警
可能原因
诊断步骤
临时恢复
长期修复
回滚方式
验证方式
```

例如：

```text
Runbook: MODEL_PROVIDER_OUTAGE
1. Verify provider status
2. Check circuit breaker
3. Enable fallback policy
4. Disable high-risk autonomous actions
5. Watch quality eval
6. Restore gradually
```

## 12. Incident Management

Agent 事故不仅是“服务挂了”。

还包括：

- Agent 错误发送大量通知；
- Tool 越权；
- Memory 污染；
- 成本突然上升 10 倍；
- 某版本开始 Citation 大量失效；
- Multi-Agent 出现委派循环。

事件处理必须能通过 `trace_id / task_id / agent_version` 定位。

## 13. Postmortem

事故后必须沉淀：

```text
Timeline
Impact
Root Cause
Why safeguards failed
Detection gap
Corrective actions
Regression scenario
Owner / due date
```

最重要的一步：

> 把事故转换成 Eval / Simulation Scenario，避免重复发生。

## 14. Chaos / Failure Drill

定期验证：

- Kill Worker；
- DB connection loss；
- Tool 500；
- Model 429；
- Queue backlog；
- Checkpoint storage latency；
- Approval timeout；
- Network partition。

确认 Task 不会丢、不会重复危险 Action。

## 15. Agent Cost Incident

成本也要有告警：

```text
cost/task > baseline * 2
mean_steps spike
retry_rate spike
context_tokens spike
```

常见原因：

- Prompt 变长；
- Reflection 死循环；
- Tool failure；
- Model Routing 失效；
- Memory 过度注入 Context。

## 16. 实训

给毕业项目增加 SRE Dashboard：

```text
Task Success
P95 Duration
Queue Lag
Model Error
Tool Error
Cost / Task
Retry Rate
HITL Wait Time
Eval Pass Rate
```

再完成 5 个故障演练：

1. Search Provider outage；
2. Worker crash；
3. Model 429；
4. Queue backlog；
5. Checkpoint latency。

## 17. 检查清单

- [ ] 是否定义 Task / Quality / Dependency SLI？
- [ ] 是否有 SLO？
- [ ] 是否有 Dependency Failure Matrix？
- [ ] 是否有 Circuit Breaker / Fallback？
- [ ] 是否支持显式 Degraded Mode？
- [ ] 是否有 Admission Control / Backpressure？
- [ ] 事故是否会转化为 Regression Scenario？
- [ ] Cost 是否作为可靠性指标监控？