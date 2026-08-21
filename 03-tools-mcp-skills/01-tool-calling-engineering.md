# Tool Calling 与 Function Calling 工程实践

## 1. Tool 是 Agent 与真实世界的接口

没有 Tool 的模型主要只能生成内容；Tool 让 Agent 可以：

- 查询数据库；
- 搜索网页；
- 调用 API；
- 写文件；
- 执行代码；
- 操作浏览器；
- 创建业务对象。

```text
Agent
 ↓ decide
Tool Call
 ↓ execute
External System
 ↓
Tool Result
 ↓
Agent
```

## 2. Tool Calling 与 Function Calling

工程上常被混用。

- **Function Calling**：模型按照函数 Schema 生成调用参数；
- **Tool Calling**：更宽泛，Tool 可以是函数、MCP Tool、Agent、Browser、Shell 等。

## 3. 好 Tool 的设计原则

### 3.1 单一职责

不推荐：

```text
do_everything(query)
```

推荐：

```text
search_patient()
get_blood_pressure_records()
create_followup_task()
```

### 3.2 Description 要说明使用条件

Tool Description 不只是函数注释，它直接影响模型选择。

应该说明：

- 做什么；
- 不做什么；
- 什么场景使用；
- 关键限制。

### 3.3 输入 Schema 严格

```python
class PatientQuery(BaseModel):
    patient_id: str
    start_date: date
    end_date: date
```

优先类型化字段，少用一个万能 `query: str`。

### 3.4 输出结构化

```json
{
  "status": "success",
  "data": [],
  "source": "patient-service",
  "trace_id": "..."
}
```

## 4. Tool 分类

### Read Tool

无副作用：查询、读取。

### Write Tool

创建或修改业务数据。

### Destructive Tool

删除、转账、发布、覆盖、执行高权限操作。

### 专业名词通义：Side Effect

Tool 调用改变外部世界状态，例如创建订单、发送消息、删除文件，称为副作用。

## 5. Tool Permission

推荐：

```text
Agent Identity
 ↓
Authorization Layer
 ↓
Tool Policy
 ↓
Tool Execution
```

不要仅依赖 Prompt：

> “你没有权限时不要调用 delete_user。”

真正的 Tool 层必须再次校验权限。

## 6. Tool Approval

高风险操作：

```text
Agent proposes action
 ↓
Permission Check
 ↓
Human Approval
 ↓
Execute
```

审批前应显示：

- Tool 名称；
- 参数；
- 影响范围；
- Agent 理由；
- 风险等级。

## 7. Retry 与 Idempotency

网络 Tool 可能失败。

但 Write Tool 不能简单自动重试。

例如：

```text
create_payment()
```

如果超时，不知道服务端是否已成功，再次调用可能重复扣款。

因此需要 Idempotency Key：

```text
X-Idempotency-Key: task-123-step-5
```

## 8. Timeout / Circuit Breaker

Tool 应定义：

```text
connect_timeout
read_timeout
max_retries
circuit_breaker
```

Agent 不应该无限等待一个坏掉的服务。

## 9. Parallel Tool Calling

无依赖 Tool：

```text
search_news(A) ─┐
search_news(B) ─┼→ Join
search_news(C) ─┘
```

应并行。

有依赖 Tool：

```text
get_user()
 ↓ user_id
get_orders(user_id)
```

必须保留依赖顺序。

## 10. Tool Registry

大型平台推荐建立 Tool Registry：

```text
Tool Name
Version
Schema
Owner
Risk Level
Required Scopes
Timeout
Idempotent
Enabled Tenants
```

Agent 只拿到当前任务需要的 Tool 子集。

## 11. Tool Result 防污染

Tool Result 是“不可信输入”。

特别是：

- 网页内容；
- 邮件；
- 外部文档；
- 第三方 MCP Server。

不要允许 Tool Result 中的文字直接提升权限或修改 System Policy。

## 12. 检查清单

- [ ] Tool 是否单一职责？
- [ ] 参数是否 Schema 化？
- [ ] 输出是否结构化？
- [ ] 是否标注 Read / Write / Destructive？
- [ ] 权限是否在 Tool 层强制执行？
- [ ] Write Tool 是否有幂等设计？
- [ ] 是否有 Timeout / Retry？
- [ ] 是否记录 Tool Call Trace？
- [ ] 外部 Tool Result 是否按不可信输入处理？
