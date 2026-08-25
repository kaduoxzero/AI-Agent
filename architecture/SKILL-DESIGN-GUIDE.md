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

```
skills/
  core/
  domain/
```

Core Skill 可以复用于所有行业。

Domain Skill 提供具体业务能力。

## 每个 Skill 应包含

- SKILL.md
- manifest.yaml
- README.md
- examples
- tests
