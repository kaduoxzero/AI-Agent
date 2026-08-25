# Project Document Naming Convention

## Rule

Agent Engineering 内部 Skill 使用英文协议名。

生成到项目中的文档使用中文文件名。

## Mapping

| Internal ID | Project File |
|---|---|
| project.yaml | 项目状态.yaml |
| boundary-canvas.md | 边界画布.md |
| decision-ledger.md | 决策记录.md |
| current-session.md | 当前会话.md |
| project-intake.md | 项目调研.md |
| architecture.md | 架构设计.md |
| change-impact.md | 影响分析.md |
| verification-report.md | 验证报告.md |

## Restrictions

禁止：

- 将项目状态写入 skills/templates；
- 使用英文文件名生成用户项目文档；
- 多项目共享同一个 .agent-engineering 状态目录。

允许：

- Skill 内部使用英文 ID；
- Registry 使用英文 key；
- Runtime 使用英文协议。
