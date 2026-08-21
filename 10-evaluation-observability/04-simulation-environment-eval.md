# Agent Simulation、Scenario Test 与 Environment Eval

> 目标：从“给输入看最终答案”升级到“在可控环境中测试 Agent 面对真实故障、权限、恶意数据和长任务状态时的行为”。

## 1. 为什么静态 Eval 不够

Agent 是交互系统。真实运行会遇到：

- Tool timeout；
- API 429 / 500；
- 数据为空；
- Browser 页面变化；
- 恶意网页 Prompt Injection；
- 用户中途取消；
- HITL 长时间不响应；
- Budget 即将耗尽；
- Agent 间 Handoff 失败；
- Checkpoint 恢复；
- 部分依赖不可用。

这些都无法仅靠 `input -> output` 数据集验证。

## 2. 专业名词通义

- **Environment Eval（环境评估）**：让 Agent 在一个模拟或隔离环境中实际行动，并评价整个执行过程。
- **Scenario Test（场景测试）**：给定一套环境条件、事件和成功标准，验证 Agent 行为。
- **Fault Injection（故障注入）**：主动制造 timeout、500、脏数据等故障。
- **Simulation（仿真）**：用 Fake / Mock 服务构建可重复的真实世界替身。
- **Chaos Test（混沌测试）**：在系统运行中注入故障，测试韧性和降级能力。

## 3. Environment Harness

推荐：

```text
Agent Under Test
      ↓
Simulation Environment
 ├─ Fake MCP Server
 ├─ Fake Database
 ├─ Fake Browser
 ├─ Fake User
 ├─ Fake Approval
 ├─ Fault Injector
 └─ Event Recorder
```

测试目标不是让模拟服务“像真的一样复杂”，而是可以精确控制状态与故障。

## 4. Scenario Schema

```yaml
name: search-provider-timeout
initial_state:
  task: research
faults:
  - tool: web.search
    call: 1
    error: timeout
expected:
  must_retry: true
  max_retries: 2
  forbidden_tools:
    - admin.search
  final_status: completed
  max_cost_usd: 0.5
```

场景应可版本化并在 CI 中运行。

## 5. 测试维度

### 5.1 Functional

- 任务完成；
- Tool 参数正确；
- Artifact 正确；
- State Transition 正确。

### 5.2 Reliability

- Timeout 后是否正确 Retry；
- 是否触发 Fallback；
- 是否出现无限循环；
- Resume 是否从正确 Checkpoint 开始。

### 5.3 Security

- 恶意 Tool Result 是否能劫持 Agent；
- 外部网页是否能诱导调用内部 Tool；
- Tenant 数据是否越权；
- 高风险 Action 是否等待 Approval。

### 5.4 Cost / Budget

- 故障时 Token 是否爆炸；
- Retry 是否有上限；
- Budget 耗尽时是否优雅退出。

## 6. 必测场景库

建议至少维护：

```text
normal/
boundary/
tool-failure/
model-failure/
security/
permission/
cancellation/
resume/
long-context/
budget/
multi-agent/
browser-change/
```

## 7. Fake Tool 设计

Tool Fake 应支持：

```python
FakeTool(
    responses=[...],
    failures={2: TimeoutError()},
    latency_ms=100,
    record_calls=True,
)
```

然后可以断言：

```text
调用次数
参数
调用顺序
Retry 次数
是否调用 forbidden tool
```

## 8. Fake User / HITL

模拟：

```text
approve immediately
reject
edit result
never respond
respond after timeout
```

验证任务状态：

```text
RUNNING → WAITING_APPROVAL → RUNNING → COMPLETED
```

## 9. Browser / Computer Agent 仿真

不要依赖真实互联网做全部回归。

可以准备固定站点：

```text
v1 DOM
v2 DOM changed
login expired
popup appeared
malicious instruction embedded
button disabled
```

测试 Agent 是否验证动作结果，而不是盲目继续。

## 10. Trajectory Assertions

除了最终结果，还要断言路径：

```yaml
required_steps:
  - retrieve_kb
  - risk_check
forbidden_steps:
  - delete_record
max_tool_calls: 12
max_handoffs: 3
```

## 11. Replay

生产 Trace 可以脱敏后转换成 Scenario：

```text
Production failure
 ↓
Sanitize trace
 ↓
Create regression scenario
 ↓
Fix
 ↓
CI forever protects it
```

这是 Agent Regression 最重要的闭环之一。

## 12. CI 分层

```text
PR:
unit + deterministic scenarios

main:
full scenario suite + security

nightly:
large model matrix + browser + chaos

pre-release:
staging environment eval + canary eval
```

## 13. 成功标准

不要只用“回答看起来不错”。

```text
status == COMPLETED
forbidden_tool_calls == 0
cost <= budget
retries <= limit
citation_coverage >= threshold
critical_security_failures == 0
```

## 14. 实训

为毕业项目建立 20 个 Scenario：

1. 正常 Research；
2. RAG 无结果；
3. DB timeout；
4. Search 429；
5. Prompt Injection 页面；
6. Tenant 越权；
7. HITL reject；
8. HITL timeout；
9. 用户 cancel；
10. Checkpoint resume；
11. Planner 输出非法 DAG；
12. Worker 重复 Evidence；
13. Budget 只剩 10%；
14. Reviewer 要求局部重跑；
15. Agent Handoff 循环；
16. Model provider failure；
17. Citation 失效；
18. 恶意 Tool Result；
19. Queue 重复投递；
20. Worker crash 后恢复。

## 15. 检查清单

- [ ] 是否有 Environment Harness？
- [ ] Tool / DB / Browser 是否可以 Fake？
- [ ] 是否可以注入故障？
- [ ] 是否断言 Trajectory，而非只断言 Output？
- [ ] 生产故障是否会沉淀为 Regression Scenario？
- [ ] Security Scenario 是否进入 CI？