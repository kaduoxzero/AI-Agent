# LangGraph 核心：State、Node、Edge 与 Graph Runtime

> LangGraph 是低层 Agent Orchestration Framework / Runtime，重点不是替你写 Prompt，而是提供长时间、有状态工作流所需的执行控制。

## 1. LangGraph 的定位

当前官方将 LangGraph 定位为用于 long-running、stateful agent 的低层 orchestration framework 与 runtime，核心能力包括 durable execution、streaming、human-in-the-loop 和 persistence。

所以正确理解是：

```text
LangChain / your model layer → Agent abstraction
LangGraph → orchestration runtime
LangSmith → tracing / evaluation / deployment platform
```

你可以不用 LangChain 组件而直接使用 LangGraph。

## 2. State

State 是整个 Graph 运行时共享的数据契约。

```python
from typing import TypedDict

class State(TypedDict):
    query: str
    documents: list
    answer: str
    retry_count: int
```

### 专业名词通义：State

不是“模型记忆”本身，而是 Workflow 运行时可读写的结构化状态。

### 设计原则

保存原始数据，而不是到处存格式化 Prompt 字符串。

好：

```python
{"documents": [...], "risk_score": 0.82}
```

差：

```python
{"prompt_text": "以下是我们之前所有结果......"}
```

## 3. Node

Node 是一个执行步骤。

**Node 不等于 Agent。**

Node 可以是：

- 普通函数；
- LLM Call；
- Agent；
- Tool 调用；
- 数据库查询；
- Rule Engine；
- Human Approval；
- SubGraph。

典型函数：

```python
def retrieve(state: State):
    docs = retriever.search(state["query"])
    return {"documents": docs}
```

节点接收 State，返回对 State 的更新。

## 4. Edge

Edge 描述 Node 之间的执行关系。

```text
START → retrieve → generate → END
```

## 5. Conditional Edge

根据 State 动态选择下一节点：

```text
            ┌→ approved → END
review ─────┤
            └→ rejected → rewrite
```

小白速记：就是 Graph 层的 `if / else`，但路由结果最好结构化并可追踪。

## 6. Reducer

多个 Node 同时更新同一 State Key 时，需要定义如何合并。

例如消息通常是 append，而普通字段可能是 overwrite。

### 专业名词通义：Reducer

定义“旧 State 和新 Update 怎样合并”的函数。

在并行 MapReduce 中非常重要。

## 7. Graph Build / Compile / Invoke

概念流程：

```python
builder = StateGraph(State)
builder.add_node("retrieve", retrieve)
builder.add_node("generate", generate)
builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", END)
graph = builder.compile()
```

执行：

```python
result = graph.invoke({"query": "..."})
```

生产环境通常还会加入 checkpointer、store、streaming 等。

## 8. Error 是控制流的一部分

不要统一写：

```python
try:
    ...
except Exception:
    retry()
```

应该区分：

```text
Transient Error → retry policy
LLM-recoverable → loop with error context
User-fixable → interrupt
Unexpected → fail and trace
```

## 9. SubGraph

大型 Graph 可以把一组节点封装为 SubGraph：

```text
Main Graph
├─ Research SubGraph
├─ Review SubGraph
└─ Approval SubGraph
```

适合：

- 模块复用；
- 独立团队开发；
- 不同 State Scope；
- Multi-Agent。

## 10. LangGraph 适合什么

适合：

- 显式 Workflow；
- 有循环；
- 需要持久化；
- 需要 HITL；
- 长任务；
- Multi-Agent；
- 对控制流要求高。

不一定适合：

- 一个简单 ReAct Agent；
- 单次 Tool Calling；
- 简单聊天。

更高层 Agent SDK 可能更省代码。

## 11. 架构建议

不要把业务层写成一个 80 Node 巨图。

推荐：

```text
Main Orchestration Graph
├─ deterministic nodes
├─ Agent nodes
└─ domain subgraphs
```

Node 只做一件核心事情。

## 12. 检查清单

- [ ] State 是否有明确 Schema？
- [ ] Node 是否职责单一？
- [ ] 是否把普通函数误拆成 Agent？
- [ ] 并行更新是否定义 Reducer？
- [ ] Error 是否按类型进入不同控制流？
- [ ] 大型流程是否使用 SubGraph？

## 13. 参考

- LangGraph Overview：https://docs.langchain.com/oss/python/langgraph/overview
