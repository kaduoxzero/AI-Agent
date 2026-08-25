# Core 与 Domain 分层规范

## 定位

AI-Agent Framework 必须保持行业无关。

Core 负责智能体工程基础能力：

- Agent Runtime
- Skill 调度
- Workflow 编排
- Memory 管理
- Evaluation
- Governance

Domain 负责行业扩展：

- 医疗
- 金融
- 电商
- 制造
- 教育

## 原则

Core 不允许依赖 Domain。

Domain 可以依赖 Core。

结构：

```
Core Runtime
      ↑
Domain Extension
```

## 禁止

禁止在核心 Skill 中出现：

- 患者
- 订单
- 金融交易
- 企业流程

这些属于 Domain 示例。
