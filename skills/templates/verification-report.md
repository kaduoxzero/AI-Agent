# Agent 验证报告

> 用于功能完成、Bug 修复、迁移、重构或上线前，记录“到底验证了什么”。项目实例文件：`.agent-engineering/验证报告.md`。

## 1. 修改摘要

```text
任务：
版本 / Commit：
使用的主 Skill：
修改模块：
用户可见行为是否变化：
```

## 2. 基线对比

```text
修改前行为：
修改后行为：
保持不变的行为：
```

## 3. 静态验证

- [ ] Import / Build 成功
- [ ] Type Check 成功
- [ ] 与本次范围相关的 Lint / Format 检查成功
- [ ] 配置可正确解析
- [ ] Schema Validation 成功

备注：

```text

```

## 4. 单元 / 组件测试

| 测试 | 结果 | 备注 |
|---|---|---|
| | 通过 / 失败 / 未运行 | |

## 5. 回归测试

| 既有行为 | 结果 | 证据 |
|---|---|---|
| | | |

## 6. Agent 执行轨迹验证

检查：

- [ ] 正确选择 Agent / Workflow
- [ ] 正确选择 Tool
- [ ] Tool 参数正确
- [ ] 没有不必要的重复调用
- [ ] State 更新正确
- [ ] 终止条件正确
- [ ] Handoff / Routing 正确（如适用）
- [ ] Checkpoint / Resume 正确（如适用）

## 7. RAG 验证

如适用：

- [ ] 正确召回目标文档
- [ ] Metadata Filter 正确
- [ ] Tenant Isolation 正确
- [ ] Citation / source_id 正确
- [ ] 无命中时行为正确
- [ ] 恶意文档不能覆盖系统策略

## 8. 安全验证

- [ ] Identity Boundary 正确
- [ ] Tool Allowlist 正确
- [ ] Permission Scope 正确
- [ ] Cross-Tenant Access 被拒绝
- [ ] High-Risk Action 进入 HITL
- [ ] Secret 未进入 Prompt / Log / Artifact
- [ ] Side Effect 具备幂等或恢复策略

## 9. 可靠性验证

- [ ] Timeout 有界
- [ ] Retry 有界
- [ ] Max Steps 生效
- [ ] Max Model Calls 生效
- [ ] Max Tool Calls 生效
- [ ] Cost Budget 生效
- [ ] Cancellation 正确
- [ ] Worker Failure 可恢复
- [ ] Duplicate Delivery 安全

## 10. Eval 结果

```text
Dataset 版本：
Baseline 版本：
Candidate 版本：
Baseline Task Success：
Candidate Task Success：
质量变化：
安全违规数：
Latency P95：
平均 Token：
平均成本：
Release Gate：通过 / 失败 / 未运行
```

## 11. 性能

```text
P50 延迟：
P95 延迟：
P99 延迟：
每任务模型调用数：
每任务 Tool 调用数：
每任务 Input Token：
每任务 Output Token：
每任务估算成本：
```

## 12. 兼容性

- [ ] Public API 兼容
- [ ] 数据库兼容
- [ ] Event Schema 兼容
- [ ] State / Checkpoint 兼容
- [ ] 现有客户端兼容
- [ ] 不兼容项已有 Migration 文档

## 13. 已知限制

```text

```

## 14. 剩余风险

| 风险 | 严重程度 | 缓解措施 | 负责人 / 后续动作 |
|---|---|---|---|
| | | | |

## 15. 回滚

```text
回滚触发条件：
回滚步骤：
数据恢复：
预计回滚时间 / 步骤：
```

## 16. 最终结论

```text
可发布 / 不可发布 / 可发布但存在已知风险

原因：
```
