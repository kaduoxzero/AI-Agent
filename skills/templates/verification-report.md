# Agent Verification Report Template

> 用于功能完成、Bug 修复、迁移、重构或上线前，记录“到底验证了什么”。

## 1. Change Summary

```text
Task:
Version / commit:
Primary skill used:
Changed modules:
User-visible behavior changed:
```

## 2. Baseline Comparison

```text
Previous behavior:
New behavior:
Preserved behavior:
```

## 3. Static Verification

- [ ] Imports / build succeed
- [ ] Type checks succeed
- [ ] Lint / format checks relevant to scope succeed
- [ ] Config parses correctly
- [ ] Schema validation succeeds

Notes:

```text

```

## 4. Unit / Component Tests

| Test | Result | Notes |
|---|---|---|
| | PASS / FAIL / NOT RUN | |

## 5. Regression Tests

| Existing behavior | Result | Evidence |
|---|---|---|
| | | |

## 6. Agent Trajectory Verification

检查：

- [ ] 正确选择 Agent / Workflow
- [ ] 正确选择 Tool
- [ ] Tool 参数正确
- [ ] 没有不必要重复调用
- [ ] State 更新正确
- [ ] 终止条件正确
- [ ] Handoff / Routing 正确（如适用）
- [ ] Checkpoint / Resume 正确（如适用）

## 7. RAG Verification

如适用：

- [ ] 正确召回目标文档
- [ ] Metadata Filter 正确
- [ ] Tenant Isolation 正确
- [ ] Citation / source_id 正确
- [ ] 无命中时行为正确
- [ ] 恶意文档不能覆盖系统策略

## 8. Security Verification

- [ ] Identity boundary 正确
- [ ] Tool allowlist 正确
- [ ] Permission scope 正确
- [ ] Cross-tenant access 被拒绝
- [ ] High-risk action 进入 HITL
- [ ] Secret 未进入 Prompt / Log / Artifact
- [ ] Side effect 具备幂等或恢复策略

## 9. Reliability Verification

- [ ] Timeout 有界
- [ ] Retry 有界
- [ ] Max steps 生效
- [ ] Max model calls 生效
- [ ] Max tool calls 生效
- [ ] Cost budget 生效
- [ ] Cancellation 正确
- [ ] Worker failure 可恢复
- [ ] Duplicate delivery 安全

## 10. Eval Result

```text
Dataset version:
Baseline version:
Candidate version:
Task success baseline:
Task success candidate:
Quality delta:
Safety violations:
Latency P95:
Average tokens:
Average cost:
Release gate: PASS / FAIL / NOT RUN
```

## 11. Performance

```text
P50 latency:
P95 latency:
P99 latency:
Model calls / task:
Tool calls / task:
Input tokens / task:
Output tokens / task:
Estimated cost / task:
```

## 12. Compatibility

- [ ] Public API compatible
- [ ] Database compatible
- [ ] Event schema compatible
- [ ] State / checkpoint compatible
- [ ] Existing clients compatible
- [ ] Migration documented if not compatible

## 13. Known Limitations

```text

```

## 14. Residual Risks

| Risk | Severity | Mitigation | Owner / Follow-up |
|---|---|---|---|
| | | | |

## 15. Rollback

```text
Rollback trigger:
Rollback procedure:
Data recovery:
Expected rollback time / steps:
```

## 16. Final Decision

```text
READY / NOT READY / READY WITH KNOWN RISK

Reason:
```
