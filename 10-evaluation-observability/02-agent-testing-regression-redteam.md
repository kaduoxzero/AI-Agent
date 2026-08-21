# Agent Testing、Regression 与 Red Team

## 1. Agent 测试金字塔

```text
        End-to-End Agent Test
       Integration Workflow Test
      Component / Tool / Node Test
          Unit / Pure Function
```

不要所有测试都通过真实模型端到端执行，成本高且不稳定。

## 2. Unit Test

普通确定性逻辑照常测试：

- State reducer；
- permission policy；
- parser；
- budget calculator；
- routing rule。

Agent 项目仍然首先是软件工程项目。

## 3. Tool Test

每个 Tool 测试：

```text
valid input
invalid input
timeout
permission denied
network failure
idempotent retry
large response
```

Tool 是 Agent 最常产生真实副作用的位置，测试优先级很高。

## 4. Model Mock

Workflow Control Flow 测试可以 Mock Model：

```text
when input=A → output route=B
```

这样能够稳定验证 Graph 路径，而不是依赖模型每次随机输出。

## 5. Integration Test

组合：

```text
real model + fake tool
fake model + real DB test env
real graph + sandbox service
```

根据测试目标选择边界。

## 6. End-to-End

使用真实模型、真实 Retriever、测试环境 Tool 完成业务任务。

重点关注：

- Task Success；
- Trajectory；
- Side Effect；
- Checkpoint；
- Trace。

## 7. Regression

模型 / Prompt 非确定性不意味着不能 Regression Test。

可以定义容忍阈值：

```text
Task Success >= 90%
Invalid Tool Call <= 1%
P95 Cost <= budget
Safety Pass = 100% for critical cases
```

## 8. Security Red Team

Agent Red Team 应覆盖：

- Prompt Injection；
- Indirect Injection；
- Tool misuse；
- privilege escalation；
- data exfiltration；
- malicious MCP Server；
- poisoned memory；
- malicious handoff；
- shell escape；
- browser injection。

## 9. Chaos / Failure Test

主动制造：

```text
LLM 429
Tool timeout
DB unavailable
Worker crash
Queue duplicate
Checkpoint failure
A2A remote agent down
```

检查系统是否安全失败。

## 10. Long-Running Test

长任务专门测试：

- Context compaction 后质量；
- resume；
- cancellation；
- stale checkpoint；
- budget exhaustion；
- memory growth。

## 11. Test Artifact

每次失败保留：

```text
input
model version
prompt version
trace id
trajectory
state snapshot
tool results
final output
```

否则很难复现。

## 12. 检查清单

- [ ] 普通代码是否仍有 Unit Test？
- [ ] Tool 是否做异常 / 幂等测试？
- [ ] Workflow 是否可用 Mock Model 测路径？
- [ ] 是否有 E2E Golden Cases？
- [ ] 是否 Red Team Prompt / Tool / Memory？
- [ ] 是否测试 Worker Crash 后 Resume？
- [ ] 测试失败是否保留 Trace Artifact？
