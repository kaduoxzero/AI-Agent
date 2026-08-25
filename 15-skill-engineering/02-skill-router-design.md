# Skill Router Engineering

> 运行时规范与路由策略配置见 `../runtime/skill-router/`（含 `../runtime/skill-router/routing-policy.yaml`）；本文提供工程设计视角。

## 定位

Skill Router 是 Agent 能力选择层，根据任务目标、上下文、权限和成本策略选择最合适的 Skill。

## 核心流程

```text
User Task
   ↓
Intent Analysis
   ↓
Capability Matching
   ↓
Policy Check
   ↓
Skill Selection
   ↓
Skill Execution
   ↓
Evaluation
```

## Router 输入

- 用户任务
- Agent Manifest
- Skill Registry
- 当前 State
- 权限策略
- 成本预算

## 路由策略

- Rule Based Routing
- Semantic Routing
- LLM Routing
- Hybrid Routing

## 工程要求

- 可解释
- 可测试
- 可回放
- 可评估
- 支持版本管理

## 常见反模式

- 所有任务交给 LLM 自由决定
- Skill 无权限控制
- Skill 无版本约束
- 无失败降级方案
