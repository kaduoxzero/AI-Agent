# Agent Orchestrator

负责运行时任务编排。

职责：

- 分析用户目标
- 创建任务计划
- 调用 Skill Router
- 分配 Supporting Skills
- 汇总结果
- 执行最终验证

流程：

User Task

↓

Planner

↓

Skill Router

↓

Skill Loader

↓

Execution

↓

Validator

↓

Final Report
