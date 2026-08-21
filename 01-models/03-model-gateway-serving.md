# Model Gateway、Serving 与 Inference Infrastructure

> 目标：让 Agent 系统摆脱“业务代码里到处散落模型 SDK”的状态，建立统一模型访问、路由、治理、成本与可用性层。

## 1. 为什么需要 Model Gateway

真实 Agent 系统通常同时使用：

```text
Fast Model
Reasoning Model
Vision Model
Embedding Model
Reranker
Local Model
Fallback Model
```

如果每个 Agent 直接调用不同厂商 SDK：

- 配置分散；
- 重试策略不一致；
- Trace 不统一；
- 模型替换成本高；
- 成本无法集中治理；
- Rate Limit 无法全局协调；
- Secret 暴露面增加。

## 2. 专业名词通义

- **Model Gateway（模型网关）**：统一封装多个模型 Provider 的访问、路由、鉴权、预算、Trace 和 Fallback。
- **Serving（模型服务）**：把模型作为可调用服务运行，包括 GPU 调度、Batch、KV Cache 等。
- **Inference（推理）**：使用训练完成的模型产生输出的过程。
- **Provider Adapter（供应商适配器）**：把不同模型厂商 API 转成内部统一接口。
- **Model Tiering（模型分层）**：按能力、延迟、成本把模型划分不同等级。

## 3. 参考架构

```text
Agent Runtime
      ↓
Model Gateway
 ├─ Policy
 ├─ Router
 ├─ Budget
 ├─ Retry / Fallback
 ├─ Cache
 ├─ Trace
 └─ Provider Adapter
      ├─ Provider A
      ├─ Provider B
      └─ Local Serving
```

## 4. 统一请求契约

推荐业务层只依赖内部抽象：

```python
class ModelRequest(BaseModel):
    task_type: str
    messages: list[Message]
    output_schema: dict | None
    tool_schema: list[dict] | None
    latency_class: str
    quality_class: str
    max_cost: float | None
    tenant_id: str
    trace_id: str
```

业务层不要知道某个 Provider 的私有字段。

## 5. Model Routing

路由应基于任务属性：

```text
classification → fast / cheap
planner → reasoning
coding → code-capable
vision → multimodal
embedding → embedding model
```

不要只按“最强模型优先”。

### Routing Input

```text
task_type
required_capabilities
latency_slo
cost_budget
context_size
availability
region / data policy
```

## 6. Fallback Policy

Fallback 不能只写：

```text
失败就换另一个模型
```

必须考虑能力兼容：

```text
Tool Calling 是否兼容？
Structured Output 是否兼容？
Context Window 是否够？
Vision 是否支持？
Data Residency 是否允许？
```

## 7. Model Version Pinning

生产 Agent 应记录：

```text
logical_model_policy
resolved_provider
resolved_model
model_version
```

否则线上结果变化时无法复现。

## 8. Budget

Model Gateway 应支持：

```text
max_input_tokens
max_output_tokens
max_cost_per_call
max_cost_per_task
max_calls_per_tenant
```

Budget 超限时：

```text
reject
route cheaper model
reduce context
require approval
```

而不是继续无限调用。

## 9. Rate Limit 与 Quota

不同 Provider 有不同限额。

Gateway 统一管理：

```text
RPM
TPM
Concurrent Requests
Tenant Quota
Priority Queue
```

关键任务可以拥有更高优先级。

## 10. Cache

### Prompt Cache

适合重复 System Prompt / 固定上下文。

### Response Cache

仅适合确定性较高、时效性可控场景。

### Semantic Cache

按语义近似命中结果，但必须特别注意：

- 用户权限；
- Tenant；
- 数据新鲜度；
- 上下文差异；
- 安全敏感场景。

## 11. Observability

每次 Model Call 至少记录：

```text
trace_id
task_id
agent_id
model_policy
resolved_model
latency
input_tokens
output_tokens
cost
cache_hit
retry_count
error_code
```

## 12. Local / Self-hosted Serving

Agent 工程师不一定训练模型，但应理解：

```text
GPU
Model Server
Batching
KV Cache
Quantization
Tensor Parallelism
Autoscaling
```

### 什么时候考虑自托管

- 强数据隔离；
- 稳定高吞吐；
- 特定模型；
- 成本结构合适；
- 离线环境。

### 不要低估的成本

```text
GPU 利用率
容量规划
模型更新
故障恢复
监控
弹性
驱动 / CUDA
```

## 13. Provider Abstraction 的边界

不要为了统一接口抹掉所有能力差异。

错误：

> 所有模型必须被压成完全一样的最低公共能力。

推荐：

```text
Common Interface
+
Capability Flags
+
Provider-specific escape hatch
```

例如：

```json
{
  "tool_calling": true,
  "vision": true,
  "structured_output": true,
  "reasoning_effort": true
}
```

## 14. Model Eval

路由策略必须通过 Eval 决定，而不是主观判断。

```text
Model A / B / C
 ↓ same dataset
Quality
Latency
Cost
Tool Accuracy
Structured Output Validity
 ↓
Routing Policy
```

## 15. 安全

Gateway 负责：

- Secret 集中管理；
- Provider allowlist；
- Data classification；
- 禁止某类敏感数据发送到不允许的 Provider；
- 请求 / 响应审计策略；
- Tenant 隔离。

## 16. 实训

实现一个最小 Model Gateway：

```text
POST /v1/generate
```

支持：

1. `task_type` 路由；
2. 两个 Provider Adapter；
3. Fallback；
4. Token / Cost 统计；
5. Tenant Quota；
6. Trace；
7. Model Eval 对比脚本。

然后让所有毕业项目 Agent 不再直接初始化厂商 SDK。

## 17. 检查清单

- [ ] 业务代码是否与 Provider SDK 解耦？
- [ ] 是否支持 Capability-aware Routing？
- [ ] Fallback 是否验证能力兼容？
- [ ] 是否记录最终 Model Version？
- [ ] 是否有 Cost / Tenant Budget？
- [ ] 是否统一 Trace / Rate Limit？
- [ ] 模型选型是否由 Eval 驱动？