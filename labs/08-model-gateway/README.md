# Lab 08｜Model Gateway：能力路由、Fallback、Quota 与成本治理

> 目标：让业务代码依赖统一 Model Gateway，而不是到处直接调用不同厂商 SDK。

## 1. 学习目标

完成后应能够：

- 用统一 Request / Response Contract 调用不同 Provider；
- 根据任务能力选择模型；
- 在 429 / Timeout 时进行受控 Fallback；
- 禁止把 Tool-Calling 任务路由到不支持 Tool 的 Provider；
- 记录 Token / Cost / Provider / Model / Trace ID；
- 对 Tenant 实施调用额度。

## 2. 专业名词通义

- **Model Gateway**：Agent 与模型供应商之间的统一访问层。
- **Capability Routing**：根据模型是否支持 Tool Calling、Vision、Structured Output、Reasoning 等能力做路由。
- **Fallback**：主模型不可用时切换到满足同一能力要求的备用模型。
- **Quota**：租户、用户或 Agent 可消耗的调用预算。
- **Provider Adapter**：把不同厂商 API 统一成相同内部接口。

## 3. 运行

```bash
cd labs/08-model-gateway
python app.py
```

默认不调用真实模型，而使用两个 Fake Provider 注入：

- 正常响应；
- 429；
- 不支持 Tool Calling。

## 4. 核心架构

```text
Agent
 ↓
ModelRequest
 ↓
ModelGateway
 ├─ Capability Filter
 ├─ Quota
 ├─ Routing
 ├─ Fallback
 └─ Usage / Audit
 ↓
Provider Adapter
```

## 5. 实验任务

1. 普通文本任务走 cheap provider；
2. Tool 任务只能走 tool-capable provider；
3. 主 Provider 429 时 Fallback；
4. Tenant Quota 用尽后直接拒绝；
5. 在日志中查看 model、provider、estimated_cost。

## 6. 生产化要求

真实实现建议继续加入：

```text
Circuit Breaker
Provider Health
Rate Limit
Prompt Cache
Semantic Cache
Cost Budget
Model Version Pinning
Regional Routing
Data Residency
```

## 7. 验收标准

- [ ] 业务代码不知道具体 Provider SDK；
- [ ] Capability 不满足时不会错误 Fallback；
- [ ] 429 可以切换备用 Provider；
- [ ] Quota 由 Gateway 强制；
- [ ] 每次模型调用都有 Usage Record；
- [ ] 能解释为什么“所有 Agent 都直接 new OpenAI()”会导致平台治理困难。
