# 项目交接总览模板

> 共享只读模板。实例化后写入业务项目 `.agent-engineering/交接/00-交接总览.md`，不得把项目数据直接写回本模板。

## 1. 交接信息

| 字段 | 内容 |
|---|---|
| 项目 | |
| 交接类型 | |
| 交接原因 | |
| 原 Owner | |
| 新 Owner | |
| 业务 Owner | |
| 技术 Owner | |
| 交接范围 | |
| 不在范围 | |
| Based on Commit / Version | |
| 目标完成时间 | |
| 当前状态 | |

## 2. Executive Snapshot

### 当前项目阶段

### 当前运行状态

### 当前开发状态

### 当前测试状态

### 当前发布状态

### 重大风险

### Critical Gaps

## 3. 证据等级

| 结论 | Evidence Level | 来源 | 备注 |
|---|---|---|---|

Evidence Level：`VERIFIED / DOCUMENTED / REPORTED / INFERRED / UNKNOWN`。

## 4. Scope Matrix

| Domain | In Scope | Current Owner | New Owner | Status |
|---|---|---|---|---|
| Business | | | | |
| Product | | | | |
| Backend | | | | |
| Frontend | | | | |
| Database | | | | |
| AI / Agent | | | | |
| Infrastructure | | | | |
| Operations | | | | |
| Security | | | | |
| Third-party | | | | |

## 5. 核心业务流程

### Normal Flow

### Exception Flow

### Compensation Flow

### Manual Flow

## 6. 架构摘要

### 系统边界

### 核心组件

### 关键调用链

### 数据流

### 外部依赖

## 7. Git / Repository Snapshot

```text
Repository:
Remote:
Default Branch:
Current Branch:
Latest Commit:
Latest Tag:
Working Tree:
Ahead / Behind:
Stash:
Untracked Files:
```

## 8. 当前工作状态

### DONE

### PARTIAL

### IN_PROGRESS

### BLOCKED

### TODO

### VERIFY

## 9. 核心运行入口

| 类型 | 位置/命令 | 验证方式 | Evidence |
|---|---|---|---|
| Build | | | |
| Startup | | | |
| Health Check | | | |
| Smoke Test | | | |
| Logs | | | |
| Monitoring | | | |
| Release | | | |
| Rollback | | | |

## 10. 已知问题与技术债

| ID | Type | Priority | Impact | Owner | Status |
|---|---|---|---|---|---|

## 11. 关键风险

| Risk | Probability | Impact | Level | Mitigation | Owner |
|---|---|---|---|---|---|

## 12. Ownership / RACI

| Activity | R | A | C | I |
|---|---|---|---|---|
| Requirement | | | | |
| Code Change | | | | |
| Release | | | | |
| DB Migration | | | | |
| Production Incident | | | | |

## 13. KT / Shadow / Reverse Shadow

| Scenario | Shadow | Reverse Shadow | Result | Evidence |
|---|---|---|---|---|
| Build & Run | | | | |
| Core Smoke Test | | | | |
| Small Change | | | | |
| Test | | | | |
| Log Diagnosis | | | | |
| Release | | | | |
| Rollback | | | | |

## 14. Acceptance Gates

| Gate | Result | Evidence | Gap |
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

## 15. 最终结论

```text
交接状态：COMPLETE / CONDITIONAL / INCOMPLETE / BLOCKED
交接评分：__/200
Critical Blocker：
Remaining Dependency：
New Owner：
接手后的第一项实际动作：
```
