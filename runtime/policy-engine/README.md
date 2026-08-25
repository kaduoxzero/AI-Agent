# Policy Engine

负责 Agent 运行时策略治理。

## 管理范围

- Tool 权限
- 高风险操作确认
- 外部副作用控制
- 数据访问边界
- 人工审核节点

## 原则

```text
Capability != Permission

Agent 可以知道如何执行
但必须经过 Policy 判断是否允许执行
```
