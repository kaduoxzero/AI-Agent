# Agent Change Impact Template

> 用于已有项目修改前。先填这个，再开始改代码。

## Change Goal

```text
Requested change:
Why it is needed:
Expected user-visible behavior:
Non-goals:
```

## Current Baseline

```text
Current entry point:
Current Agent / Graph:
Current model / prompt:
Current tools:
Current RAG / memory:
Current state / checkpoint:
Current tests / evals:
Current known failures:
```

## Invariants To Preserve

- [ ] Public API
- [ ] Request / response schema
- [ ] Task status behavior
- [ ] Tool names / schema
- [ ] State keys
- [ ] Event types
- [ ] Database compatibility
- [ ] Tenant isolation
- [ ] Existing prompt output contract
- [ ] Existing user-visible behavior

补充：

```text
Other invariants:
```

## Blast Radius

| Area | Impact | Risk | Required Verification |
|---|---|---|---|
| API | none / low / medium / high | | |
| Agent runtime | | | |
| Prompt | | | |
| Tool | | | |
| State / checkpoint | | | |
| RAG / memory | | | |
| Database | | | |
| Queue / worker | | | |
| Security | | | |
| Eval | | | |
| Deployment | | | |

## Proposed Strategy

优先选择：

```text
Adapter
New isolated module
Extend interface
Local refactor
Compatibility layer
Migration
Major rewrite
```

选择：

```text
Strategy:
Why this is the smallest safe option:
```

## Files Expected To Change

```text
Direct files:
Possible dependent files:
Files explicitly out of scope:
```

## Compatibility

```text
Backward compatible: yes / no
Migration required: yes / no
Old data readable: yes / no
Old clients supported: yes / no
Checkpoint compatibility: yes / no
```

## Rollback

```text
Rollback trigger:
Rollback steps:
Data rollback:
Config rollback:
Release rollback:
```

## Test Plan

```text
Static checks:
Unit tests:
Regression tests:
Feature tests:
Eval suite:
Security tests:
Integration tests:
Smoke tests:
```

## Stop Conditions

立即停止扩大修改，如果出现：

- 影响面明显超过需求；
- 必须破坏核心公开契约；
- 旧数据无法安全迁移；
- 大量旧测试在改动前已失败；
- 发现更高优先级 P0 / P1 风险。

## Final Approval Checklist

- [ ] Baseline 已记录
- [ ] Invariants 已识别
- [ ] Blast Radius 已分析
- [ ] 最小修改策略已选择
- [ ] 回滚路径存在
- [ ] 测试范围明确
