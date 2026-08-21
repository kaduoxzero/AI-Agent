# LLM、Reasoning Model 与 Agent 所需模型能力

## 1. 为什么 Agent 工程师必须懂模型

Agent 的行为上限首先受模型能力限制。架构无法完全弥补模型在工具调用、指令遵循、规划或长上下文上的根本不足。

但大型 Agent 项目也绝不能“所有节点都用最强模型”。正确方法是理解不同节点需要什么模型能力。

## 2. LLM 的核心概念

### Token

模型处理文本的基本单位，不等于固定数量的汉字或单词。

Agent 中 Token 消耗来自：

```text
System Prompt
+ Conversation
+ Tool Schema
+ Tool Result
+ Retrieved Documents
+ Memory
+ Model Output
+ 多轮循环
```

因此 Agent 的 Token 成本通常明显高于单次聊天。

### Context Window

模型单次推理可接收的最大上下文范围。

**专业名词通义：Context Window**

可以理解为“一次模型调用能够同时读取的工作区大小”。它不是长期 Memory；超过窗口的信息如果没有压缩、检索或外部存储，就无法直接参与当前推理。

### Inference

模型已经训练完成之后，根据输入生成输出的过程。

### Sampling

模型从概率分布中选择下一 Token 的过程。

常见参数：

- Temperature；
- Top-P；
- Max Output Tokens。

生产 Agent 中不要简单把“Temperature 越低 = 越准确”当成定律。结构化任务、分类和 Tool 参数通常偏稳定；创意任务可以允许更高随机性。

## 3. 普通 LLM 与 Reasoning Model

### 普通 LLM

更适合：

- 分类；
- 改写；
- 摘要；
- 简单抽取；
- 简单 Router；
- 低延迟交互。

### Reasoning Model

更适合：

- 复杂 Planning；
- Coding；
- 数学 / 逻辑；
- 多约束任务；
- 工具选择困难的任务；
- 复杂 Agent 决策节点。

### 重要工程结论

不要设计：

```text
所有节点 → 最强 Reasoning Model
```

更推荐：

```text
Classifier → Fast Model
Router → Fast Model / Rule
Planner → Reasoning Model
Worker → Domain-appropriate Model
Evaluator → Strong Model or deterministic evaluator
```

## 4. Agent 对模型的特殊要求

### 4.1 Instruction Following

Agent 必须稳定遵守：

- Tool 使用规则；
- 输出 Schema；
- 权限边界；
- Delegation Policy；
- Stop Condition。

### 4.2 Tool Calling

模型需要：

1. 正确判断是否需要 Tool；
2. 选择正确 Tool；
3. 生成合法参数；
4. 正确利用 Tool Result；
5. 避免重复无意义调用。

### 4.3 Structured Output

Router、Planner、Evaluator 等节点通常应该输出结构化对象，而不是自由文本。

例如：

```json
{
  "route": "research",
  "confidence": 0.93,
  "reason": "需要外部最新信息"
}
```

### 4.4 Long Context

长 Context 不是越长越好。

常见问题：

- 无关信息干扰；
- Tool Result 堆积；
- 中间错误持续污染；
- 成本与延迟增加。

因此需要 Context Engineering，而不是单纯追求最大窗口。

### 4.5 Multimodal

大型 Agent 可能同时处理：

```text
Text
Image
Audio
PDF
Screenshot
Video Frame
```

Browser / Computer Agent 尤其依赖视觉能力。

## 5. Embedding 与 Reranker 不是 Chat Model

### Embedding Model

将文本、图片等映射为向量，用于相似度检索。

### Reranker

对第一阶段召回结果进行更精细的相关性重排。

企业 RAG 常见流程：

```text
Query
 ↓
Embedding / BM25 Retrieval
 ↓
Top 50
 ↓
Reranker
 ↓
Top 5
 ↓
LLM
```

## 6. 模型能力评估

不要只依据公开排行榜。

应该使用项目自己的任务集测试：

| 能力 | 测试内容 |
|---|---|
| Tool Selection | 是否选择正确 Tool |
| Arguments | 参数是否合法 |
| Routing | 路由准确率 |
| Planning | 计划是否可执行 |
| Coding | 测试通过率 |
| RAG | 基于 Evidence 回答能力 |
| Structured Output | Schema 成功率 |
| Safety | 是否遵守权限规则 |
| Latency | P50 / P95 |
| Cost | 每任务平均成本 |

## 7. Agent Model Layer 设计

大型项目不要在业务代码中到处直接调用厂商 SDK。

建议抽象：

```text
ModelGateway
├─ generate()
├─ generate_structured()
├─ stream()
├─ embed()
└─ health_check()
```

再通过配置：

```yaml
models:
  fast: ...
  reasoning: ...
  coding: ...
  vision: ...
  embedding: ...
```

这样 Router / Planner / Worker 不与具体供应商强耦合。

## 8. 常见反模式

### 所有 Agent 都用同一个模型

会造成成本、延迟和能力错配。

### 把 Embedding、Rerank 和 Generation 混为一谈

三者解决不同问题。

### 只看模型最大 Context

生产质量更依赖 Context 中“放了什么”，而不是理论上“能放多少”。

### 模型升级不重新做 Eval

模型版本变化可能导致 Prompt、Tool 参数和输出分布发生回归。

## 9. 检查清单

- [ ] 每个节点是否真的需要强推理模型？
- [ ] Router 是否可以用规则或小模型？
- [ ] 是否建立模型抽象层？
- [ ] 是否统计模型调用的 Token、Latency、Failure？
- [ ] 是否为模型升级准备回归测试？
- [ ] 是否为 Tool Calling 单独评估成功率？
