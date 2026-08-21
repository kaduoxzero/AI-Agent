---
name: agent-productionizer
description: Convert an Agent demo or prototype into a production-oriented service with durable task state, queue/worker execution, checkpoint/resume, cancellation, idempotency, event streaming, observability, deployment, release governance, reliability controls, and operational runbooks.
---

# Agent Productionizer

## Objective

把“本地能跑”升级为 **可长期运行、可恢复、可扩缩容、可回滚、可运维** 的 Agent 服务。

## Production Architecture Baseline

推荐最小边界：

```text
Client
→ API / Auth
→ Task Store
→ Queue
→ Worker
→ Agent Runtime
→ Tool / RAG / Model Gateway
→ Checkpoint
→ Artifact Store
→ Event / Trace / Metrics
```

## 1. Long-Running Task Model

Agent 长任务不要依赖单个同步 HTTP 请求生命周期。

至少定义：

- task_id；
- trace_id；
- status；
- created_at / updated_at；
- owner identity；
- Agent version；
- budget；
- result / artifact URI；
- error category。

## 2. Task State Machine

至少考虑：

```text
PENDING
RUNNING
WAITING_APPROVAL
CANCELLING
COMPLETED
FAILED
CANCELLED
```

状态转换必须受约束，避免任意跳转。

## 3. Queue & Worker

Worker 必须支持：

- at-least-once delivery；
- duplicate handling；
- graceful shutdown；
- retry；
- poison task isolation；
- crash recovery；
- bounded concurrency。

不能假设 Queue 消息只会消费一次。

## 4. Idempotency

对外任务创建和有副作用 Tool 都要考虑幂等。

典型：

```text
Tenant + Idempotency-Key
→ Existing Task or New Task
```

副作用 Tool 使用 operation_id / request_id 防重复执行。

## 5. Checkpoint / Resume

长任务至少在关键步骤后保存：

- plan；
- completed actions；
- evidence；
- state；
- side-effect markers。

Resume 不得重复已经完成的不可逆操作。

## 6. Cancellation

取消应是 Cooperative Cancellation：

```text
Cancel Request
→ CANCELLING
→ Worker checks boundary
→ Cleanup
→ CANCELLED
```

不要依赖粗暴杀线程作为唯一取消机制。

## 7. HITL

高风险 Action：

```text
Plan
→ Risk Policy
→ WAITING_APPROVAL
→ Human Approve / Reject
→ Resume / Cancel
```

审批记录必须审计 actor / reason / timestamp。

## 8. Model Gateway

生产环境不要让业务层散落 Provider SDK。

Gateway 负责：

- model routing；
- capability matching；
- timeout；
- fallback；
- 429 handling；
- quota；
- token accounting；
- cost accounting；
- tracing。

## 9. Tool Gateway

生产 Tool 层负责：

- schema validation；
- scope authorization；
- timeout；
- retries；
- circuit breaker；
- audit；
- idempotency；
- secret isolation。

## 10. Observability

最低要求：

### Trace

任务链路：API → Queue → Worker → Runtime → Model / Tool / RAG。

### Logs

结构化字段：

```text
trace_id
task_id
tenant_id
agent_id
agent_version
step
tool
error_category
```

### Metrics

至少：

- task success / failure；
- duration P50 / P95 / P99；
- queue lag；
- worker utilization；
- model calls；
- tokens；
- cost；
- tool error；
- approval count；
- retry count。

## 11. SLI / SLO

定义可操作指标：

- availability；
- task success；
- P95 completion latency；
- queue delay；
- recovery success；
- safety incidents；
- cost per task。

## 12. Deployment

至少支持：

- environment-based config；
- secret management；
- health / readiness；
- container image；
- persistent volumes / external services；
- migration job；
- graceful shutdown；
- rollback。

## 13. Release Governance

Agent 发布需要版本化：

- Agent definition；
- Prompt；
- Model route；
- Tool allowlist；
- RAG config；
- Eval dataset；
- release route。

推荐：

```text
Register
→ Eval Gate
→ Canary
→ Observe
→ Promote / Rollback
```

## 14. Failure Modes

必须演练：

- Worker crash；
- Redis / Queue unavailable；
- DB unavailable；
- Model 429；
- Model timeout；
- Tool timeout；
- RAG unavailable；
- corrupted checkpoint；
- duplicate message；
- process restart；
- partial deployment。

## 15. Runbook

至少建立：

```text
Symptom
Detection
Immediate mitigation
Diagnosis
Recovery
Rollback
Postmortem data
```

## Anti-Patterns

- FastAPI Handler 内同步跑 10 分钟 Agent；
- Task 只放内存；
- Queue 没有幂等；
- Worker 崩溃后任务永久 RUNNING；
- Prompt 修改直接全量上线；
- Tool 权限只写在 Prompt；
- 只有 Logs 没有 Metrics；
- 没有 Cancellation / Timeout / Cost Budget。

## Completion Criteria

生产化完成至少意味着：

- API 与长任务解耦；
- 状态耐久；
- Worker 可恢复；
- 重复投递安全；
- 可取消；
- 高风险可审批；
- 有 Trace / Log / Metric；
- 有 Eval Gate；
- 有 Canary / Rollback 路径；
- 核心故障有 Runbook。
