---
name: agent-debugger
version: 1.1.0
description: Diagnose and fix Agent systems that fail, hang, loop, call the wrong tool, lose state, retrieve bad evidence, produce invalid structured output, fail to resume, or behave inconsistently. Use for runtime bugs, orchestration bugs, tool bugs, RAG bugs, state bugs, provider failures, and Agent-specific regressions.
---

# Agent Debugger

## Objective

用可复现、可证伪的方式排查 Agent 故障，避免“改 Prompt 试试看”式调试。

## Core Rule

始终执行：

```text
Reproduce
→ Classify
→ Localize
→ Form Hypothesis
→ Minimal Fix
→ Regression Test
→ Root Cause Record
```

## 1. Reproduce First

优先收集：

- 输入；
- Agent / Prompt / Model 版本；
- State；
- Tool Call；
- Tool Result；
- Retrieval Evidence；
- Event / Trace；
- Error stack；
- Token / Step / Retry；
- 最小复现路径。

没有复现条件时，不要连续修改多个模块。

## 2. Classify Failure

分类到一个主故障域：

- Prompt / Structured Output
- Context / State
- Routing / Graph
- Tool Selection
- Tool Execution
- RAG Retrieval
- Memory
- Multi-Agent Handoff
- Model Provider
- Queue / Worker
- Checkpoint / Resume
- Permission / HITL
- Timeout / Retry
- Concurrency
- Deployment / Configuration

## 3. Agent Loop Debugging

如果出现死循环，检查：

- 是否有终止条件；
- `max_steps` 是否生效；
- Observation 是否真的改变 State；
- 相同 Tool 是否重复调用；
- 模型是否看不到已完成步骤；
- Planner 是否持续生成同一 Plan；
- Error 是否被吞掉后自动重试。

必须添加循环保护测试。

## 4. Tool Debugging

如果 Tool 没调用或调用错误：

检查：

```text
Tool registration
→ Tool description
→ Input schema
→ Model capability
→ Permission scope
→ Routing condition
→ Runtime adapter
→ Tool exception
```

不要只调整 Tool 描述。

## 5. Structured Output Debugging

检查：

- Schema 是否过于复杂；
- Provider 是否支持 Structured Output；
- Prompt 与 Schema 是否冲突；
- Optional / Required 是否正确；
- Validation Error 是否进入 Repair Loop；
- Repair 是否有次数上限。

## 6. RAG Debugging

拆分定位：

```text
Document missing?
Chunk bad?
Metadata bad?
Embedding bad?
Filter wrong?
TopK wrong?
Rerank wrong?
Context assembly wrong?
Generation ignores evidence?
```

必须查看实际召回 Evidence，不要仅看最终答案。

## 7. State / Checkpoint Debugging

检查：

- State 是否持久化；
- 更新是否覆盖旧字段；
- Reducer 是否正确；
- Checkpoint 保存时机；
- Resume 是否重复副作用操作；
- 旧 Schema 是否还能读取；
- Cancel / Approval 后状态是否一致。

## 8. Multi-Agent Debugging

检查：

- 谁拥有下一步控制权；
- Handoff 是否包含完整输入；
- 是否循环 Handoff；
- Shared State 是否被覆盖；
- Agent 输出 Artifact 是否符合下游契约；
- Supervisor 是否产生单点无限重试。

## 9. Provider Debugging

区分：

- 429 Rate Limit；
- Quota；
- Timeout；
- Context Length；
- Unsupported Tool Calling；
- Unsupported Structured Output；
- Safety refusal；
- Provider transport error。

Provider 故障应该由 Model Gateway 做标准化，不应该散落在业务代码里。

## 10. Minimal Fix Rule

一次修复优先只改变一个故障假设。

禁止同时：

- 换模型；
- 改 Prompt；
- 改 Tool；
- 改 State；
- 改框架。

否则无法知道真正原因。

## Regression Requirement

每个确认的 Bug 必须尽可能新增：

- 最小复现测试；
- 修复后通过测试；
- 相邻场景回归测试。

Agent Bug 优先记录：

```text
Input
State
Expected trajectory
Actual trajectory
Expected output
Actual output
```

## Failure Report

```text
Symptom:
Reproduction:
Failure domain:
Root cause:
Fix:
Regression test:
Residual risk:
```

## Report Back to Master

排查完成后，按 `../agent-engineering-master/SKILL-REGISTRY.md` 的 Return Contract 返回；Failure Report 中的 Root cause / Fix / Regression test 应映射到 Return Contract 对应项。

---

## Completion Criteria

- Bug 可解释，不只是“现在好了”；
- 修复范围最小；
- 有防止复发的测试或 Eval；
- 没有掩盖旧错误；
- Trace / Error 信息足够下次直接定位。
