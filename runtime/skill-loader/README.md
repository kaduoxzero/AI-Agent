# Skill Loader

Skill Loader 是 Runtime 的能力加载层。

## 职责

- 发现 Skill
- 读取 skill.yaml
- 校验 Skill 元数据
- 解析依赖关系
- 加载目标 SKILL.md
- 控制加载范围

## 加载流程

```text
Skill Router
    ↓
Skill Registry
    ↓
Skill Loader
    ↓
Manifest Validation
    ↓
Load Skill
```

原则：

- 按需加载
- 禁止全量加载
- 禁止绕过 Registry
- 失败时进入安全降级模式
