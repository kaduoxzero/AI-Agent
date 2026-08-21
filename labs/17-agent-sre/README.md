# Lab 17｜Agent SRE：Circuit Breaker、Degraded Mode、SLI/SLO 与 Failure Drill

> 目标：把 Agent 服务当成真正需要 SLO、故障隔离和降级策略的生产系统，而不是“模型 API 能返回就算可用”。

## 1. 学习目标

完成后应能够：

- 定义 Agent SLI / SLO；
- 对不稳定依赖实现 Circuit Breaker；
- 在外部 Search 不可用时进入 Degraded Mode；
- 记录成功率、Fallback 次数和依赖失败；
- 设计 Failure Drill；
- 理解 Error Budget 与发布速度之间的关系。

## 2. 专业名词通义

- **SLI**：实际测量的可靠性指标，例如 task_success_rate、p95_latency。
- **SLO**：对 SLI 的目标，例如月度任务成功率 ≥ 99.5%。
- **Circuit Breaker**：依赖连续失败后暂时停止继续请求，避免故障放大。
- **Degraded Mode**：部分依赖不可用时保留受限但可工作的服务能力。
- **Failure Drill**：主动注入故障验证恢复策略，而不是等生产事故第一次验证。

## 3. 运行

```bash
cd labs/17-agent-sre
python app.py
```

## 4. 场景

Research Agent 同时可以使用：

```text
Public Search
Internal RAG
```

当 Public Search 连续失败：

```text
failure
 ↓
failure
 ↓ threshold
Circuit OPEN
 ↓
Degraded Mode
 ↓
只使用 Internal RAG
```

最终答案必须标明证据范围已降低，不能假装系统仍然是 Full Mode。

## 5. 推荐 SLI

```text
task_success_rate
p95_task_duration
model_error_rate
tool_error_rate
fallback_rate
checkpoint_recovery_rate
human_intervention_rate
cost_per_successful_task
```

## 6. 实验任务

1. 正常运行；
2. 注入连续 Search Failure；
3. 观察 Circuit OPEN；
4. 观察 Degraded Mode；
5. 清除故障并模拟 Half-Open Recovery；
6. 输出 Metrics。

## 7. 验收标准

- [ ] 连续失败不会无限打依赖；
- [ ] 有 Circuit Breaker；
- [ ] 有 Degraded Mode；
- [ ] 降级结果向调用者显式标识；
- [ ] 有 SLI 统计；
- [ ] 能设计至少 5 个 Failure Drill；
- [ ] 能写出一次 Agent Incident 的 Runbook / Postmortem 结构。
