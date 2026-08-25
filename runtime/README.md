# Agent Runtime

Agent Runtime 是 AI-Agent Framework 的运行时治理层。

## 模块

已实现（设计规范 + 配置）：

- skill-loader：Skill 发现与加载
- skill-router：任务路由
- skill-validator：Skill 质量检查
- policy-engine：安全策略
- state-manager：项目状态管理
- skill-lifecycle：生命周期状态模型
- skill-registry / registry：注册表与 Schema
- orchestrator：执行协议
- initialization：初始化协议
- compatibility：兼容性矩阵
- self-check：运行时自检
- domain-architecture：领域分层

规划中：

- skill-bootstrap：环境初始化（见 initialization/）
- resource-resolver：资源解析（见 skills/agent-engineering-master/resources/SKILL-RUNTIME-V2.md）

机器可读事实源：

```text
runtime/skill-registry.yaml
```

执行器：

```text
python scripts/validate_skills.py
```

Runtime 不承担具体业务能力，负责管理 Skills 生命周期。
