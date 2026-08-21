# Examples：最小可运行示例规划

> `examples/` 用于存放“一个概念一个最小运行例子”。它和 `labs/` 不同：Examples 追求小而清晰，Labs 追求完整工程能力和故障验证。

## 1. 目录规划

```text
examples/
├─ 01-structured-output/
├─ 02-tool-calling/
├─ 03-mcp-server/
├─ 04-rag/
├─ 05-agentic-rag/
├─ 06-react/
├─ 07-plan-execute/
├─ 08-langgraph-state/
├─ 09-langgraph-hitl/
├─ 10-multi-agent-handoff/
├─ 11-a2a/
├─ 12-ag-ui/
├─ 13-sandbox/
├─ 14-agent-eval/
└─ 15-event-driven-agent/
```

## 2. 每个 Example 的规范

每个目录只解决一个问题，并包含：

```text
README.md
requirements / pyproject
.env.example
src/
tests/
```

README 至少说明：

```text
解决什么问题
运行命令
预期结果
关键代码
生产环境不能直接照搬的部分
```

## 3. Example 不应该做什么

不要：

- 引入完整微服务；
- 一次展示 8 种 Pattern；
- 为了“高级”强行 Multi-Agent；
- 隐藏错误处理；
- 使用真实生产 Secret；
- 把教学示例包装成生产最佳实践。

## 4. 与 Labs 的关系

例如：

```text
examples/02-tool-calling
    ↓ 看懂基本机制
labs/L03-tool-runtime
    ↓ 加入 Registry / Retry / Permission / Audit
13-projects/
    ↓ 进入完整生产项目
```

学习路径是：

```text
Example → Lab → Project
```

## 5. 后续代码实现优先级

P0：

```text
Structured Output
Tool Calling
MCP Server
RAG
ReAct
LangGraph State / HITL
Eval Harness
```

P1：

```text
A2A
AG-UI
Sandbox
Event-Driven Agent
Agent Identity
```

完成 P0 后，仓库就从纯知识库升级为可以直接跟练的课程。