# Skill 设计规范

## 通用 Skill

Skill 必须描述能力，而不是行业。

正确：

- agent workflow design
- retrieval optimization
- security review
- evaluation

错误：

- 医疗问诊 Skill
- 电商订单 Skill

## Skill 分层

```text
skills/        core skills（行业无关，当前全部 13 个）
runtime/       运行时治理（行业无关）
domain/        领域扩展（未来按行业新增）
```

Core Skill 可以复用于所有行业；Domain Skill 提供具体业务能力，且不得修改 Core Runtime 文件。分层规范见 `CORE-DOMAIN-SEPARATION.md`。

## 每个 Skill 必须包含

```text
SKILL.md     执行协议（frontmatter: name / version / description）
skill.yaml   机器可读 manifest
```

推荐补充：README.md、examples、tests、resources。

manifest 模板与校验规则：

- 模板：`skills/SKILL-MANIFEST-TEMPLATE.yaml`
- 校验执行器：`scripts/validate_skills.py`
