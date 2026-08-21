# Agent Deployment、CI/CD 与 Agent DevOps

## 1. Agent 部署比普通 API 多了什么

普通服务重点：

```text
Code + Config + DB
```

Agent 还包含：

```text
Prompt
Model Config
Workflow
Tool Schema
Skill
RAG Index
Eval Dataset
Policy
```

这些都可能改变行为。

## 2. 推荐服务拆分

```text
API Service
Task Service
Agent Workers
Tool Services
MCP Gateway
Retrieval Service
Memory Service
Sandbox Service
Evaluation Service
Observability Stack
```

小项目可以合并，但逻辑职责应明确。

## 3. Container

Agent Worker 推荐容器化：

- 环境一致；
- 依赖可控；
- 易扩缩容。

注意：运行 Coding Sandbox 时不要默认把 Docker Socket 暴露给 Agent Worker，否则等于给宿主高权限。

## 4. Kubernetes / Worker Scaling

扩缩容信号可以是：

```text
queue lag
running tasks
CPU
memory
provider rate limit headroom
```

不是只看 CPU，因为 Agent Worker 可能主要等待网络。

## 5. Stateless API, Stateful Backend

API 层尽量 Stateless。

真正状态存储在：

```text
PostgreSQL
Checkpoint Store
Redis
Object Storage
Vector DB
```

这样 API / Worker 可以水平扩展。

## 6. CI Pipeline

```text
Lint
 ↓
Unit Test
 ↓
Tool / Workflow Test
 ↓
Agent Eval
 ↓
Security Test
 ↓
Build Image
 ↓
Deploy Staging
 ↓
Smoke Eval
```

## 7. Prompt / Model Change 也走 CI

不要允许生产 Prompt 在后台随便改而没有版本。

```text
Prompt PR
 ↓
Eval
 ↓
Review
 ↓
Release
```

Model Version 更新同理。

## 8. Eval Gate

示例：

```yaml
quality:
  task_success: ">= 0.92"
safety:
  critical_cases: "= 1.0"
cost:
  avg_task_usd: "<= 0.30"
latency:
  p95_seconds: "<= 20"
```

不达标阻止上线。

## 9. Canary

新 Prompt / Model / Workflow 先给小比例流量：

```text
95% stable
5% candidate
```

比较：

- quality；
- error；
- cost；
- human escalation。

## 10. Feature Flag

用于快速关闭：

- 新 Agent；
- 高风险 Tool；
- 新 MCP Server；
- 新 Memory Feature；
- 新 Model Route。

## 11. Rollback

必须能回滚：

```text
Code Version
Prompt Version
Model Config
Workflow Version
Tool Schema
Skill Version
```

RAG Index 也建议版本化。

## 12. Secret

使用 Secret Manager，不进入：

- Git；
- Prompt；
- Trace；
- Sandbox Snapshot。

## 13. Environment

```text
local
integration
staging
production
```

Staging Tool 应连接测试业务系统，避免 Eval 误操作生产数据。

## 14. Observability Gate

新版本上线后自动观察：

```text
Task Success
Cost
Latency
Tool Error
Guardrail Trip
Queue Lag
```

异常自动降级 / 回滚。

## 15. Agent DevOps 核心理念

> Agent 的“代码”不只在 `.py/.java` 文件里。Prompt、模型、Tool、Knowledge、Skill 和 Policy 都是运行行为的一部分，都需要版本、测试和发布治理。

## 16. 检查清单

- [ ] Agent Worker 是否容器化？
- [ ] API 是否可水平扩展？
- [ ] Prompt / Model 是否版本化？
- [ ] CI 是否包含 Agent Eval？
- [ ] 是否有 Safety Gate？
- [ ] 是否 Canary？
- [ ] 是否能快速禁用 Tool / Agent？
- [ ] 是否能回滚 Knowledge Index？
