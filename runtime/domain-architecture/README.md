# Domain Architecture

> 本主题的权威文档：`../../architecture/CORE-DOMAIN-SEPARATION.md`

## 摘要

AI-Agent 核心框架保持行业无关。

Core Layer 负责：

- Agent 生命周期
- Skill 调度
- Workflow 编排
- Memory
- Evaluation
- Governance

Domain Layer 承载行业扩展（healthcare / finance / ecommerce 等）。

原则：Core 不依赖 Domain；Domain 可以依赖 Core；领域能力以插件形式接入，不得修改 Core Runtime 文件。
