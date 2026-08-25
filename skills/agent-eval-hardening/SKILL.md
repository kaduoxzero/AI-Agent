---
name: agent-eval-hardening
version: 1.1.0
description: Build evaluation, regression, and release gates for Agent systems. Use when an Agent works but is unstable, when prompts/models/tools/RAG are changing, before production release, after bugs, or when quality must be measured across final output, trajectory, tool calls, retrieval, safety, latency, and cost.
---

# Agent Eval Hardening

## Objective

把“看起来能用”变成 **有数据证明的稳定可发布**。

## Core Principle

Agent 评测不能只看最终回答。

必须至少覆盖：

```text
Input
→ Trajectory
→ Tool / Retrieval
→ State Transition
→ Output
→ Cost / Latency
→ Safety
```

## 1. Define Evaluation Layers

### Output Eval

评估最终结果：

- correctness；
- completeness；
- relevance；
- groundedness；
- citation；
- style / schema compliance。

### Trajectory Eval

评估过程：

- 是否选择正确 Tool；
- Tool 参数是否正确；
- 是否走了不必要步骤；
- 是否出现重复调用；
- 是否正确终止；
- 是否遵守权限。

### Retrieval Eval

评估：

- Recall@K；
- correct source hit；
- rerank quality；
- tenant leakage；
- citation mapping。

### Safety Eval

覆盖：

- Prompt Injection；
- Tool 越权；
- 数据泄露；
- 高风险 Action；
- HITL bypass；
- Secret handling。

### Reliability Eval

覆盖：

- timeout；
- 429；
- provider failure；
- tool failure；
- worker restart；
- resume；
- cancellation；
- duplicate delivery。

## 2. Golden Dataset

Golden Case 至少包含：

```text
case_id
input
setup
expected_output_constraints
expected_tools
forbidden_tools
expected_evidence
expected_status
max_steps
max_cost
risk_level
```

不要只存自然语言问题 + 标准答案。

## 3. Dataset Categories

至少覆盖：

- Happy Path；
- Boundary；
- Ambiguous；
- No Evidence；
- Conflicting Evidence；
- Tool Failure；
- Provider Failure；
- Security Attack；
- Multi-Tenant；
- Long Context；
- High Risk；
- Cancellation / Resume。

## 4. Baseline First

任何优化前先跑 Baseline。

记录：

```text
Version:
Model:
Prompt:
Dataset:
Success Rate:
Latency P50/P95:
Avg Tokens:
Avg Cost:
Safety Violations:
```

没有 Baseline 就无法证明修改真的更好。

## 5. Deterministic vs LLM Judge

优先确定性检查：

- JSON Schema；
- Tool sequence；
- status；
- source_id；
- forbidden action；
- numeric threshold。

只有无法用规则判断的质量维度才使用 LLM-as-Judge。

LLM Judge 必须：

- 使用固定 rubric；
- 输出结构化 score + reason；
- 尽量盲评版本；
- 校验与人工判断的一致性。

## 6. Regression Gate

每次修改 Agent / Prompt / Model / Tool / RAG 后至少比较：

```text
New vs Baseline
```

Release Gate 示例：

- task_success 不下降；
- critical safety violations = 0；
- tenant leakage = 0；
- P95 latency 不超过阈值；
- 平均成本不超过预算；
- 关键 Golden Cases 100% 通过。

## 7. Bug-to-Eval Rule

每次生产 Bug 或高价值 Bug 修复后：

```text
Bug reproduction
→ Add to regression dataset
→ Fix
→ Run full relevant suite
```

不允许只修代码不留下回归资产。

## 8. Prompt / Model Experiment

一次实验尽量只改变一个变量：

- Prompt；
- Model；
- Temperature；
- Retriever；
- Reranker；
- Tool Description。

否则无法归因。

## 9. Multi-Agent Eval

必须比较：

```text
Single Agent Baseline
vs
Multi-Agent Candidate
```

评价：

- quality gain；
- latency increase；
- token increase；
- routing errors；
- handoff errors；
- failure amplification。

## 10. Release Report

输出：

```text
Candidate version:
Baseline version:
Dataset version:
Passed cases:
Failed cases:
Quality delta:
Latency delta:
Cost delta:
Safety result:
Release decision:
Known risk:
```

## Anti-Patterns

禁止：

- 用 3 个示例判断 Prompt 已优化；
- 只测最终文字；
- 用同一个模型生成答案又给自己打分且没有校准；
- Dataset 随代码一起偷偷改到全部通过；
- 忽略失败 Case，只看平均分；
- 发布时没有记录 Prompt / Model / Agent Version。

## Report Back to Master

完成后，按 `../agent-engineering-master/SKILL-REGISTRY.md` 的 Return Contract 返回；Release Report 的 Quality / Latency / Cost delta 与 Release decision 应映射到 Verification Performed 与 Recommended Next Capability。Eval 资产位置写入当前项目 `.agent-engineering/verification-report.md`。

---

## Completion Criteria

- 有版本化 Dataset；
- 有 Baseline；
- 有 Output + Trajectory Eval；
- 安全关键项有确定性 Gate；
- Agent 变更可以自动回归；
- Release Decision 可以被数据解释；
- 生产 Bug 能沉淀成新测试资产。
