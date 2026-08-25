# Agent Engineering Skill Runtime v2

## 目标

升级 Agent Engineering Master 的运行机制，同时保持 Master Skill 作为唯一入口不变。

## 核心原则

Master 负责：

- 用户目标理解
- 项目状态初始化
- Skill 路由
- 生命周期控制
- 最终验收

专项 Skill 负责具体领域执行。

## Runtime Bootstrap

Skill 加载后必须先确定：

```text
SKILL_ROOT
PROJECT_ROOT
PROJECT_STATE_ROOT
```

解析规则：

1. SKILL_ROOT 为当前 Skill 所在目录；
2. 所有 Skill 内部资源必须相对 SKILL_ROOT 解析；
3. 不允许从当前工作目录猜测 Skill 文件位置；
4. 不允许把 skills 目录作为业务项目状态目录。

## Resource Resolver

资源加载顺序：

```text
1. 当前 Skill resources/
2. 当前 Skill 根目录
3. 注册中心定义位置
4. 安全降级规则
```

找不到非关键资源时继续运行。

找不到核心策略文件时进入安全降级模式，并明确记录。

## Project Artifact Language

Skill 内部协议保持英文。

所有生成到业务项目的文档默认使用中文：

- 项目状态.yaml
- 边界画布.md
- 决策记录.md
- 当前会话.md
- 项目调研.md
- 架构设计.md
- 影响分析.md
- 验证报告.md

除非用户明确要求英文。

## State Isolation

模板只读：

```text
skills/templates
```

项目状态独立：

```text
<project>/.agent-engineering
```

多个项目禁止共享状态。

## Future Runtime Modules

规划模块：

```text
skill-bootstrap
skill-loader
skill-router
resource-resolver
state-manager
skill-validator
```
