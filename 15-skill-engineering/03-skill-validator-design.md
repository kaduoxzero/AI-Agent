# Skill Validator Engineering

## 目标

Skill Validator 用于保证 Agent Skill 的质量、安全和兼容性。

## 校验维度

### Manifest

- name
- version
- description
- input schema
- output schema

### Engineering

- 文档完整性
- 示例可运行
- 依赖声明
- 测试覆盖

### Security

- Tool 权限
- 数据访问范围
- Secret 使用
- Prompt Injection 风险

## Validation Pipeline

```text
Skill Package
    ↓
Schema Validate
    ↓
Static Check
    ↓
Security Scan
    ↓
Runtime Test
    ↓
Publish
```

## 发布规则

未通过 Validator 的 Skill 不允许进入生产 Registry。
