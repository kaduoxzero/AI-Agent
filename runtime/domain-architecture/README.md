# Domain Architecture

AI-Agent 核心框架保持行业无关。

## Core Layer

负责：

- Agent 生命周期
- Skill 调度
- Workflow 编排
- Memory
- Evaluation
- Governance

## Domain Layer

行业能力通过扩展实现：

- healthcare
- finance
- ecommerce
- manufacturing
- education

Core 不允许依赖任何具体行业实现。
