# Agent Prompt Engineering 与 Structured Output

## 1. Agent Prompt 与普通 Prompt 的区别

普通 Prompt 往往只需要描述一次性任务；Agent Prompt 必须约束一个会持续运行、会调用工具、可能委派任务的执行主体。

一个可维护的 Agent Prompt 至少应该包含：

```text
Role
Goal
Responsibilities
Constraints
Tool Policy
Decision Policy
Delegation Policy
Failure Policy
Output Contract
Stop Condition
```

### 专业名词通义

- **Tool Policy**：什么情况下允许调用什么 Tool，以及哪些 Tool 需要审批。
- **Delegation Policy**：什么时候把任务交给其他 Agent，禁止什么样的无限转交。
- **Output Contract**：对输出字段、类型和语义的约定。
- **Stop Condition**：达到什么条件必须结束本轮执行。

## 2. 推荐 Prompt 分层

大型系统不要把所有规则塞入一个数千行 System Prompt。

推荐：

```text
System Policy
  ↓
Agent Role Prompt
  ↓
Task Prompt
  ↓
Dynamic Context
  ↓
Tool / Skill Instructions
```

其中：

- System Policy：跨 Agent 的安全、权限、行为底线；
- Role Prompt：本 Agent 的职责；
- Task Prompt：当前任务；
- Dynamic Context：检索结果、State 摘要等；
- Skill Instructions：仅在相关任务时加载。

## 3. Prompt 中必须明确的边界

例如 Research Agent：

```text
你负责检索和整理证据，不负责执行写操作。
如果信息不足，应继续检索或报告证据不足，不得编造。
不得调用带副作用的 Tool。
输出必须包含来源、关键事实和不确定性。
```

比只写“你是一名资深研究专家”有效得多。

## 4. Structured Output

Agent 间通信、Routing、Tool 参数和 Evaluator 结果应优先使用结构化输出。

例如 Router：

```json
{
  "route": "research",
  "confidence": 0.91,
  "requires_human": false
}
```

而不是：

```text
我认为应该交给研究模块，因为……
```

### 为什么结构化输出重要

- 可以做类型校验；
- 可以减少解析歧义；
- 可以驱动 Conditional Edge；
- 可以记录稳定的 Trace；
- 可以做自动 Eval。

## 5. Schema 设计原则

### 使用 Enum 约束有限集合

```python
from typing import Literal
from pydantic import BaseModel

class RouteDecision(BaseModel):
    route: Literal["research", "data", "direct"]
    confidence: float
```

### 字段要表达业务语义

不推荐：

```json
{"result": "A"}
```

推荐：

```json
{
  "risk_level": "high",
  "reasons": ["..."],
  "requires_review": true
}
```

### 不要把自由文本 JSON 当 Structured Output

真正的 Structured Output 应由模型接口 / Schema 约束并在程序端验证。

## 6. Prompt Versioning

生产系统需要版本化 Prompt：

```text
prompt_id: risk-agent
version: 2026-08-01-v3
```

Trace 至少记录：

```text
Prompt Version
Model Version
Tool Version
Knowledge Version
```

否则出现质量回归时无法定位。

## 7. Prompt 与代码的职责边界

不要用 Prompt 实现：

- 权限控制；
- 金额校验；
- 数据库约束；
- 硬风险阈值；
- 幂等；
- 事务。

Prompt 负责语义判断，代码负责确定性规则。

## 8. Prompt Injection 基础意识

System Prompt 不能被视为真正的安全边界。外部文档、网页、Tool Result 都可能包含恶意指令。

因此：

```text
Prompt Rule
+ Tool Permission
+ Data Isolation
+ Guardrail
+ Approval
```

需要共同工作。

## 9. 常见反模式

### Prompt 超长

规则越多不一定越稳定，反而可能造成冲突和注意力稀释。

### 同一条规则重复十次

应通过 Schema、权限和程序约束增强，而不是文字重复。

### 输出完全自由文本

后续节点需要解析时会非常脆弱。

### Agent Prompt 直接包含所有领域知识

领域知识更适合 RAG / Skill 按需加载。

## 10. 检查清单

- [ ] Role 是否明确？
- [ ] Agent 不应该做什么是否明确？
- [ ] Tool Policy 是否明确？
- [ ] Delegation 是否有边界？
- [ ] 是否定义停止条件？
- [ ] 机器处理结果是否使用 Schema？
- [ ] Prompt 是否有版本？
- [ ] 确定性业务规则是否仍由代码控制？
