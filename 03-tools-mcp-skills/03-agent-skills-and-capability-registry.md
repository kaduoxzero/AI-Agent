# Agent Skills、Capability Registry 与渐进式能力加载

## 1. Skill 解决什么问题

当 Agent 的 Prompt、Tool 和领域规则越来越多时，全部常驻 Context 会造成：

- Prompt 膨胀；
- Tool 选择困难；
- 无关知识干扰；
- 维护困难。

Skill 的思路是：

> 将特定领域的工作方法、规则、资源和脚本封装成按需加载的能力包。

## 2. Skill 与 Tool 的区别

| 概念 | 作用 |
|---|---|
| Prompt | 告诉 Agent 如何行动 |
| Tool | 执行具体外部操作 |
| Skill | 某一类任务的完整工作方法 / 资源包 |
| MCP | 标准化连接外部能力 |

例如 Code Review Skill 可以包含：

```text
SKILL.md
rules/
examples/
scripts/
checklists/
```

而 `run_tests` 是 Tool。

## 3. Progressive Loading

**专业名词通义：Progressive Loading**

只在任务需要时加载 Skill 的详细内容。

```text
Agent sees skill index
 ↓ selects code-review
Load skill instructions
 ↓
Execute task
```

这样可以减小 Context。

## 4. Skill Metadata

建议至少维护：

```yaml
name: java-code-review
description: Java/Spring 代码规范、逻辑、安全审查
version: 1.3.0
owner: platform-ai
risk_level: low
required_tools:
  - repo_search
  - run_tests
```

## 5. Capability Registry

大型 Agent 平台不仅需要 Tool Registry，还需要 Capability Registry：

```text
Capability
├─ Agent
├─ Skill
├─ Tool
├─ MCP Server
└─ Model Requirement
```

Orchestrator 可以根据任务选择“能力”，而不是硬编码具体实现。

## 6. Skill 与 Multi-Agent

不是每个专业领域都需要拆 Agent。

例如：

```text
General Coding Agent
+ Java Skill
+ Python Skill
+ SQL Skill
```

可能比：

```text
Java Agent
Python Agent
SQL Agent
```

更简单。

只有当职责、权限或 Context 真正独立时才拆 Agent。

## 7. Skill 的版本与测试

Skill 更新也可能导致 Agent 行为回归，因此应：

```text
Skill Change
 ↓
Eval Dataset
 ↓
Regression Test
 ↓
Release Version
```

Trace 记录 Skill Version。

## 8. Skill 安全

Skill 可能包含脚本和工具说明，因此需要：

- 来源可信；
- 代码审查；
- 权限限制；
- 禁止未经审核的自动下载执行；
- 版本锁定。

## 9. 检查清单

- [ ] 能力是否应该是 Skill 而不是新 Agent？
- [ ] Skill 是否按需加载？
- [ ] 是否记录版本和 Owner？
- [ ] 是否声明依赖 Tool？
- [ ] 是否有 Eval？
- [ ] Skill 中脚本是否经过安全审查？
