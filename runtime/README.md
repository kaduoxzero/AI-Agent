# Agent Runtime

Agent Runtime 是 AI-Agent Framework 的运行时治理层。

## 模块

- skill-bootstrap：环境初始化
- skill-loader：Skill发现与加载
- skill-router：任务路由
- state-manager：项目状态管理
- skill-validator：Skill质量检查
- policy-engine：安全策略

Runtime 不承担具体业务能力，负责管理 Skills 生命周期。