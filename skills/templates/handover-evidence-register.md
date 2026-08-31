# 交接证据台账模板

> 共享只读模板。用于证明交接结论，不用于保存 Secret。

## 证据等级

- `VERIFIED`：已通过代码、运行、测试、日志、配置、数据库或监控验证。
- `DOCUMENTED`：来自正式资料，尚未实际验证。
- `REPORTED`：来自交接人口述。
- `INFERRED`：由代码/上下文推断。
- `UNKNOWN`：无法确认。

## Evidence Register

| ID | Domain | Claim | Level | Source | Verification | Result | Owner |
|---|---|---|---|---|---|---|---|

## Critical Evidence

以下项目不能仅依赖 `REPORTED`：

- 项目可启动；
- 核心业务可用；
- 发布流程；
- 回滚流程；
- 备份恢复；
- 关键权限；
- 生产配置位置；
- 关键数据库关系；
- AI 高风险 Tool / HITL 边界。

## Verification Record

```text
Evidence ID:
Claim:
Precondition:
Command / Action:
Expected:
Actual:
Artifacts / Logs:
Verified By:
Date:
Result:
```

## Unknown Register

| ID | Unknown Item | Why Unknown | Impact | Required Action | Owner | Deadline |
|---|---|---|---|---|---|---|
