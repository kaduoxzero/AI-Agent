# Lab 02｜Tool Runtime：权限、超时、幂等与审计

> 目标：理解生产级 Tool 不是“一个 Python 函数加描述”，而是一套受 Runtime 管理的执行边界。

## 1. 学习目标

完成实验后应能够：

- 定义 Tool Schema 与权限等级；
- 区分 read / write Tool；
- 对 Tool 设置 Timeout；
- 对写操作使用 Idempotency Key；
- 记录 ToolStarted / ToolCompleted / ToolFailed 审计事件；
- 理解为什么模型不能直接掌握数据库事务、权限和重试策略。

## 2. 专业名词通义

- **Tool Runtime**：统一执行 Tool 的运行层，负责校验、授权、超时、审计和错误转换。
- **Idempotency Key**：幂等键。同一个写请求重复提交时，用它识别“这其实是同一次操作”。
- **Side Effect**：副作用，指调用会修改外部世界，如写数据库、发邮件、创建订单。
- **Audit Event**：审计事件，用于回答“谁在什么时间以什么权限调用了什么能力”。

## 3. 运行

```bash
cd labs/02-tool-runtime
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
python app.py
```

## 4. 代码结构

```text
ToolDefinition
  ├─ name
  ├─ args_model
  ├─ side_effect
  ├─ required_scope
  └─ timeout_seconds

ToolRuntime
  ├─ validate args
  ├─ authorize
  ├─ idempotency
  ├─ timeout
  ├─ execute
  └─ audit
```

## 5. 实验任务

运行后观察：

1. `get_supplier` 只读 Tool 正常执行；
2. 没有 `supplier:write` Scope 时，`update_supplier_status` 被拒绝；
3. 有权限后写操作成功；
4. 使用同一 Idempotency Key 重试，第二次不重复写入；
5. `slow_tool` 被 Runtime 超时终止等待。

## 6. 生产设计原则

```text
LLM decides intent
      ↓
Runtime validates
      ↓
Policy authorizes
      ↓
Tool executes deterministic business logic
      ↓
Audit + typed result
```

不要把这些责任写进 Prompt：

> “你一定不要调用危险工具。”

Prompt 可以辅助决策，但真正边界必须由代码和权限系统保证。

## 7. 验收标准

- [ ] 无权限无法执行 Write Tool；
- [ ] Tool 参数经过 Pydantic 校验；
- [ ] 写 Tool 支持 Idempotency Key；
- [ ] 有超时控制；
- [ ] 每次调用都有 Audit Event；
- [ ] 能解释 Tool Error 与 Model Error 为什么要分开。
