# 交接验收模板

> 共享只读模板。用于接手人验收，不以“文档已发送”作为通过标准。

## 1. Day 0 — Access Ready

- [ ] Repository 可访问
- [ ] 文档可访问
- [ ] Dev/Test 环境可访问
- [ ] Database 权限可用
- [ ] Monitoring/Logging 可访问
- [ ] 必要 Third-party 权限可用

## 2. Day 1 — Runtime Ready

- [ ] Clone / Checkout 成功
- [ ] Dependency 安装成功
- [ ] Build 成功
- [ ] 项目启动成功
- [ ] Health Check 通过
- [ ] Core Smoke Test 通过
- [ ] 能查询关键日志

## 3. Day 3 — Development Ready

- [ ] 能解释核心架构
- [ ] 能定位核心代码入口
- [ ] 能完成一个小修改
- [ ] 能运行测试
- [ ] 能定位一个普通 Bug
- [ ] 能解释关键配置来源

## 4. Day 7 — Ownership Ready

- [ ] 能独立完成常规开发
- [ ] 能独立完成常规发布
- [ ] 能说明回滚条件和步骤
- [ ] 能处理普通 Incident
- [ ] 能正确使用 Escalation Path
- [ ] 不依赖原负责人完成日常工作

## 5. Reverse Shadow

| Scenario | Operator | Observer | Result | Evidence | Gap |
|---|---|---|---|---|---|
| Build & Run | | | | | |
| Core Smoke | | | | | |
| Small Change | | | | | |
| Test | | | | | |
| Log Diagnosis | | | | | |
| Release | | | | | |
| Rollback | | | | | |
| Backup Restore（如适用） | | | | | |

## 6. Acceptance Gates

| Gate | PASS/FAIL | Evidence | Critical Gap |
|---|---|---|---|
| Scope Ready | | | |
| Asset Ready | | | |
| Knowledge Ready | | | |
| Runtime Ready | | | |
| Development Ready | | | |
| Operations Ready | | | |
| Security & Permission Ready | | | |
| Ownership Ready | | | |
| Reverse Shadow Passed | | | |

## 7. Critical Blocker Override

出现以下任一项时不得判定 COMPLETE：

- [ ] 核心仓库无法访问
- [ ] 接手人无法启动项目
- [ ] 关键代码仅存在原负责人本地
- [ ] 生产 Owner 不明确
- [ ] 关键数据库关系未知
- [ ] 发布流程不可执行
- [ ] 核心回滚方案不明确
- [ ] 关键权限未移交
- [ ] 关键 Secret 仅存在个人设备
- [ ] 核心未提交修改未处置
- [ ] 关键数据恢复策略缺失
- [ ] Reverse Shadow 关键项失败

## 8. Score

```text
Business & Product              __ / 15
Architecture & Decisions        __ / 20
Code & Repository               __ / 20
Data & API                      __ / 20
Environment / Build / Run       __ / 20
Test & Verification             __ / 15
Release / Rollback / Operations __ / 20
Security & Permission           __ / 10
Risk / Debt / Hidden Knowledge  __ / 15
Ownership / RACI                __ / 10
Knowledge Transfer              __ / 10
Reverse Shadow                  __ / 15
Documentation Consistency       __ / 10
---------------------------------------
Total                           __ / 200
```

## 9. Final Status

- `COMPLETE`
- `CONDITIONAL`
- `INCOMPLETE`
- `BLOCKED`

```text
Status:
Score:
Critical Gaps:
Remaining Dependencies:
New Owner:
Accepted By:
Next Exact Action:
```
