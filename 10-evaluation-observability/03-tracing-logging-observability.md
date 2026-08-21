# Agent Observability：Tracing、Logging、Metrics 与事件模型

## 1. 为什么普通日志不够

传统日志：

```text
2026-... request success
```

无法回答：

- 哪个 Agent 做的决定？
- 调了哪个 Tool？
- 为什么耗时 30 秒？
- Token 花在哪一步？
- Handoff 了几次？
- 哪个 Guardrail 拦截？

因此需要 Trace。

## 2. Trace / Span

### Trace

一次完整业务请求 / Agent Task 的全链路记录。

### Span

Trace 中的一段工作：

```text
Trace: task-123
├─ Span: router
├─ Span: planner
├─ Span: search tool
├─ Span: worker agent
└─ Span: evaluator
```

## 3. Agent Event Taxonomy

建议统一事件：

```text
run.start
run.end
model.start
model.end
tool.start
tool.end
handoff
state.update
checkpoint.save
approval.request
approval.resolve
guardrail.trip
error
```

OpenAI Agents SDK 当前默认 tracing 也覆盖 generation、tool call、handoff、guardrail 等 Agent 事件。

## 4. 必须记录的字段

```text
trace_id
task_id
session_id
tenant_id
agent_name
agent_version
model
prompt_version
tool_name
tool_version
latency_ms
input_tokens
output_tokens
cost
status
error_type
```

敏感内容不要默认全量记录。

## 5. Logging

日志更适合离散事件与诊断文本。

推荐结构化 JSON Log：

```json
{
  "level": "INFO",
  "event": "tool.completed",
  "trace_id": "...",
  "tool": "search",
  "latency_ms": 820
}
```

## 6. Metrics

### 业务指标

- Task Success；
- Human Escalation；
- Completion Time。

### Agent 指标

- Turns；
- Tool Calls；
- Handoffs；
- Guardrail Trips。

### LLM 指标

- Input / Output Tokens；
- TTFT；
- Model Error；
- Cost。

### Infrastructure

- Queue Lag；
- Worker Utilization；
- Sandbox Startup；
- Checkpoint latency。

## 7. Distributed Trace

A2A / Worker 系统要传播 Trace Context：

```text
API trace_id
 ↓
Queue message
 ↓
Worker
 ↓
A2A call
 ↓
Remote Agent
```

否则一个任务会碎成多个无法关联的日志。

## 8. Sensitive Data

Trace 可能包含：

- Prompt；
- Tool 参数；
- 用户数据；
- RAG 文档；
- Secret。

需要：

```text
redaction
data classification
retention
access control
tenant isolation
```

## 9. OpenTelemetry

可以将 Agent Trace 映射到 OpenTelemetry 的 Trace / Span / Event / Metric 体系，方便与现有微服务可观测平台统一。

但 GenAI / Agent 语义约定仍在快速演进，封装自己的 telemetry adapter，避免业务代码绑定具体字段版本。

## 10. Debug 页面

内部开发平台推荐展示：

```text
Graph timeline
State diff
Model call
Tool call
Artifacts
Cost
Errors
Checkpoint
```

比直接翻日志效率高得多。

## 11. 检查清单

- [ ] 每个 Task 是否有唯一 trace_id？
- [ ] Queue / A2A 是否传播 Trace Context？
- [ ] 是否能看到 Model / Tool / Handoff Span？
- [ ] 是否记录 Prompt / Tool / Model Version？
- [ ] 是否统计每一步 Token / Cost？
- [ ] 敏感数据是否脱敏？
- [ ] Trace 是否有保留期限？

## 12. 参考

- OpenAI Agents SDK Tracing：https://openai.github.io/openai-agents-python/tracing/
- OpenTelemetry：https://opentelemetry.io/
