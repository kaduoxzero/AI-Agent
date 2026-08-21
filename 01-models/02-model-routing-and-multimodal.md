# 模型路由、Fallback、多模态与成本优化

## 1. 为什么需要 Model Routing

大型 Agent 系统通常包含不同类型任务：

```text
Intent Classification
Planning
Coding
Vision
Summary
Evaluation
Embedding
```

这些任务对模型要求不同。如果全部使用同一种模型，通常会出现“简单任务过贵、复杂任务能力不足”的问题。

## 2. Model Routing

**专业名词通义：Model Routing**

根据任务类型、难度、延迟要求、成本预算或输入模态，动态选择最合适模型。

```text
Request
  ↓
Task Analyzer
  ↓
┌────────────┬───────────────┬────────────┐
Fast Model   Reasoning Model  Vision Model
```

### 路由信号

可以使用：

- intent；
- token length；
- 是否需要 Tool；
- 是否包含图片；
- 风险等级；
- 用户套餐；
- 任务复杂度；
- 当前预算；
- 供应商可用性。

## 3. Model Tiering

推荐将模型按能力层级配置，而不是把业务逻辑绑定模型名：

```yaml
model_tiers:
  fast:
    purpose: routing, classify, summarize
  standard:
    purpose: normal agent work
  reasoning:
    purpose: planning, difficult analysis
  vision:
    purpose: screenshot/image
```

业务代码引用 `reasoning`，基础设施层再解析到具体模型。

## 4. Fallback

Fallback 用于主模型不可用或输出失败时切换备用模型。

```text
Primary Model
 ↓ error / timeout
Fallback Model
```

但需要注意：

> Fallback 模型不是简单替换接口地址。

不同模型可能存在：

- Tool Calling Schema 差异；
- Structured Output 行为差异；
- System Prompt 敏感度差异；
- Context 限制差异。

因此必须对 Fallback 路径单独 Eval。

## 5. Complexity Routing

可以先由轻量 Router 判断复杂度：

```json
{
  "complexity": "high",
  "needs_reasoning": true,
  "needs_tools": true
}
```

然后选择强模型。

但 Router 本身也可能错，因此关键业务建议增加保守策略：

```text
低置信度 → 升级模型
高风险任务 → 强模型
普通任务 → 快模型
```

## 6. 多模态 Agent

### 6.1 Vision Agent

典型任务：

- UI 分析；
- Screenshot 理解；
- 图表读取；
- 票据 / 医学图片辅助分析；
- Browser / Computer Use。

### 6.2 Audio / Voice

Voice Agent 常见两种方案：

#### Pipeline

```text
Audio
 ↓ STT
Text
 ↓ Agent
Text
 ↓ TTS
Audio
```

#### Speech-to-Speech Realtime

```text
Audio ↔ Realtime Model ↔ Tools
```

后者延迟更低，但对会话状态、中断、音频安全与成本控制要求更高。

### 专业名词通义

- **STT**：Speech-to-Text，语音转文字。
- **TTS**：Text-to-Speech，文字转语音。
- **VAD**：Voice Activity Detection，判断用户是否开始/停止说话。
- **Barge-in**：用户在 Agent 讲话时插话并中断当前输出。

## 7. Model Gateway

生产系统推荐：

```text
Agent
 ↓
Model Gateway
├─ Provider A
├─ Provider B
└─ Local Model
```

Model Gateway 统一处理：

- API Key；
- Retry；
- Timeout；
- Provider Routing；
- Token Metrics；
- Rate Limit；
- Fallback；
- Cache。

## 8. Prompt / Context Caching

对于重复出现的大 System Prompt、Tool Schema、固定知识，可以利用模型厂商提供的 Prompt / Context Cache 能力降低成本和首 Token 延迟。

但缓存键必须考虑：

- Prompt Version；
- Tool Version；
- Tenant；
- Permission；
- Model Version。

不要因为缓存造成跨租户数据泄漏。

## 9. 成本预算

生产 Agent 应为每个任务定义 Budget：

```yaml
budget:
  max_steps: 20
  max_model_calls: 25
  max_tool_calls: 30
  max_input_tokens: 200000
  max_cost_usd: 1.0
  timeout_seconds: 180
```

Budget 不只是财务控制，也可以阻止 Agent 死循环。

## 10. 检查清单

- [ ] 是否按能力 Tier 而非模型名写业务代码？
- [ ] 是否定义 Fallback？
- [ ] Fallback 是否跑过 Eval？
- [ ] 是否区分文本、视觉、语音任务？
- [ ] 是否统计每个 Node 的模型成本？
- [ ] 是否定义单任务 Token / Step / Cost Budget？
- [ ] 多租户缓存是否隔离？
