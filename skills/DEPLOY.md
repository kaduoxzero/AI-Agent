# 一键部署 / 更新 Skills

本文件提供把本仓库 Agent Engineering Skills 部署到任意开发环境的提示词。

> Skill 版本记录在各自 SKILL.md frontmatter 的 `version` 字段（MAJOR.MINOR.PATCH）。更新前比较版本即可判断差异；结构一致性由仓库根目录 `scripts/validate_skills.py` 与 GitHub Actions 保证。

## 首次部署

下面这段提示词可以直接复制给 **Codex、Coding Agent 或其他支持 Skills 的工程 Agent**，让它把本仓库的 Agent Engineering Skills 部署到当前开发环境。

```text
请帮我部署 AI-Agent 仓库中的 Agent Engineering Skills。

来源仓库：
https://github.com/kaduoxzero/AI-Agent

目标内容：
仓库根目录下的 skills/ 目录。

部署要求：

1. 先检查当前 Agent / Coding Agent 环境支持的 Skills 机制、Skill 搜索路径、项目级 Skill 目录和用户级 Skill 目录。
2. 如果当前项目已经存在 Skills 目录或已有 Skill 约定，优先遵循现有项目规范，不要擅自创造新的非标准目录。
3. 如果平台同时支持“项目级 Skills”和“全局 / 用户级 Skills”，默认优先安装为项目级 Skills；只有我明确要求全局安装时才安装到用户级目录。
4. 将 AI-Agent 仓库中的完整 skills/ 能力体系部署到目标 Skills 目录，而不是只复制单个 SKILL.md。
5. 必须保留各 Skill 的目录层级、SKILL.md、skill.yaml、SKILL-REGISTRY.md、PROJECT-STATE-POLICY.md、resources/ 和 templates/，确保 Skill 之间的相对引用关系可用。
6. 将以下 Skill 设置为唯一推荐主入口：
   agent-engineering-master
7. 其他 Skill 不需要我手动调用，它们作为 agent-engineering-master 的内部能力模块，由 Master Skill 在任务执行期间按需加载、组合和切换。
8. 部署时不要覆盖、删除或重命名我已有的无关 Skills。
9. 如果目标位置已经存在同名 AI-Agent Skills：
   - 先比较各 SKILL.md frontmatter 中的 version 与文件差异；
   - 只更新本套 Skills 自己管理的文件；
   - 保留用户自行新增的无关文件；
   - 不要因为更新本 Skill 集而清空整个 Skills 目录。
10. 检查所有 SKILL.md 的 YAML Frontmatter（name / version / description）与同目录 skill.yaml 的元数据一致，相对路径有效。
11. 检查 agent-engineering-master 是否能够发现并引用以下能力：
   - agent-grill-me
   - agent-guided-builder
   - agent-greenfield-builder
   - agent-existing-project-modifier
   - agent-architecture-reviewer
   - agent-debugger
   - agent-rag-engineer
   - agent-multi-agent-designer
   - agent-eval-hardening
   - agent-productionizer
   - agent-security-reviewer
   - agent-performance-cost-optimizer
   - agent-project-orchestrator
12. 检查 templates/ 中的 Boundary Canvas、Decision Ledger、Session State、Project Intake、Architecture Summary、Change Impact、Verification Report 是否完整。
13. 不要修改我的业务代码、Agent 实现、Prompt、依赖或配置；这一步只负责部署 Skills。
14. 不要因为你熟悉某个平台就猜测 Skill 安装路径。优先检查当前环境真实支持的位置和现有约定。
15. 如果当前平台无法原生安装 Skills，则保留原目录结构部署到项目中，并明确告诉我该平台应该如何引用 agent-engineering-master/SKILL.md；不要擅自改写 Skill 内容来适配。

部署完成后执行验证：

A. 能找到 agent-engineering-master/SKILL.md；
B. Master Skill 能读取 SKILL-REGISTRY.md 和 PROJECT-STATE-POLICY.md；
C. Master Skill 能按需定位其他专项 Skill；
D. templates/ 可被读取；
E. 原有 Skills 未被破坏；
F. 不存在重复嵌套目录，例如 skills/skills/...；
G. 不存在只复制 Master Skill、却丢失被调用专项 Skill 的情况。

最后只需要给我输出：

- 实际部署位置；
- 部署 / 更新了哪些 Skill 及其 version；
- 主入口路径；
- 是否通过上述验证；
- 如果当前 Agent 平台存在 Skills 加载限制，说明具体限制。

部署成功后的默认使用规则：
后续涉及 Agent 的设计、开发、修改、调试、RAG、Multi-Agent、Eval、安全、性能优化和生产化任务，优先从 agent-engineering-master 开始，由它自主调度其他 Skill，不需要再次让我选择专项 Skill。
```

## 更新已有部署

如果之前已经部署过，可以直接使用下面的简化提示词：

```text
请从 https://github.com/kaduoxzero/AI-Agent 更新我当前环境中已部署的 Agent Engineering Skills。

只同步仓库 skills/ 下属于本套 Skill 系统的内容，不要删除我的其他 Skills，也不要修改业务代码。

更新前先比较每个 SKILL.md frontmatter 的 version，跳过版本相同的文件。

更新后确保：
1. agent-engineering-master 仍然是唯一推荐主入口；
2. Master 能动态调用其他专项 Skill；
3. PROJECT-STATE-POLICY.md、SKILL-REGISTRY.md 与 templates/ 同步更新；
4. 所有 SKILL.md Frontmatter（name / version / description）有效；
5. 不产生 skills/skills/ 这类重复目录；
6. 输出实际更新文件、版本变化和验证结果。
```
