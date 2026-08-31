# Agent 项目调研模板

> 用于从 0 到 1、新项目接手或重大改造前快速建立工程上下文。能从仓库直接推断的信息优先自动填写，不要反复询问用户。项目实例文件：`.agent-engineering/项目调研.md`。

## 1. 项目身份

```text
项目名称：
代码仓库：
当前阶段：想法 / 原型 / MVP / 生产
主要开发语言：
框架：
模型提供方：
部署目标：
```

## 2. 业务目标

```text
主要参与者：
主要目标：
触发方式：
输入：
预期输出：
业务价值：
```

## 3. 执行模型

```text
当前架构：函数 / Workflow / Single Agent / Multi-Agent
谁决定下一步：
是否存在长任务：是 / 否
是否有异步 Worker：是 / 否
是否需要人工审批：是 / 否
```

## 4. Agent 能力

```text
Prompt：
Structured Output：
Tools：
RAG：
Memory：
State：
Checkpoint：
Multi-Agent：
Browser / Computer Use：
Code / Shell execution：
```

## 5. 数据与知识

```text
主要数据源：
向量存储：
关系型存储：
缓存：
Artifact 存储：
租户隔离：
知识新鲜度要求：
```

## 6. 契约

记录当前已有或计划中的：

```text
TaskRequest：
TaskRecord：
AgentState：
ToolInput / ToolOutput：
Evidence：
Artifact：
Event：
Error Model：
```

## 7. 可靠性

```text
超时：
重试：
降级：
最大步骤：
最大模型调用：
最大 Tool 调用：
最大成本：
取消：
恢复：
幂等性：
```

## 8. 安全

```text
身份来源：
权限模型：
Tool Scope：
敏感操作：
Prompt Injection 边界：
Secrets：
HITL：
审计：
```

## 9. 质量与评估

```text
已有测试：
已有 Eval：
Golden Dataset：
已知失败案例：
质量目标：
延迟目标：
成本目标：
安全目标：
```

## 10. 约束

```text
必须保留：
不可修改：
兼容性要求：
基础设施约束：
截止时间 / 范围约束：
```

## 11. 当前风险

| 风险 | 严重程度 | 证据 | 缓解措施 |
|---|---|---|---|
| | | | |

## 12. 完成定义

- [ ] 核心业务闭环可端到端运行
- [ ] Public Contract 已定义
- [ ] 测试通过
- [ ] 相关 Eval 通过
- [ ] 权限边界已执行
- [ ] 失败行为有明确边界
- [ ] 可观测性满足要求
- [ ] Deployment / Rollback 路径明确
