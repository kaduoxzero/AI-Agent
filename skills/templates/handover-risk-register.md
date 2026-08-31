# 交接风险与 SPOF 台账模板

> 共享只读模板。项目实例应放入业务项目交接目录。

## 1. Risk Register

| Risk ID | Category | Description | Probability | Impact | Level | Trigger | Mitigation | Contingency | Owner |
|---|---|---|---|---|---|---|---|---|---|

风险分类至少检查：

- Business
- Architecture
- Code
- Data
- Database
- Security
- Operations
- External Service
- Permission
- People
- Cost
- AI
- Compliance
- Schedule

## 2. SPOF Register

| SPOF ID | Type | Description | Current Dependency | Impact | Remediation | Owner |
|---|---|---|---|---|---|---|

重点识别：

- `Knowledge SPOF`：只有一个人知道；
- `Access SPOF`：只有一个管理员/个人账号；
- `Runtime SPOF`：单机、单实例、单节点；
- `Data SPOF`：只有一份数据/未验证恢复；
- `Provider SPOF`：只有一个模型/API/供应商；
- `Process SPOF`：关键步骤完全依赖人工记忆。

## 3. Tribal Knowledge Register

| ID | Hidden Knowledge | Current Source | Why It Matters | Documentation Action | Owner |
|---|---|---|---|---|---|

## 4. Technical Debt Register

| Debt ID | Description | Reason | Impact | Risk | Priority | Suggested Solution | Owner |
|---|---|---|---|---|---|---|---|

## 5. Known Issue Register

| Issue ID | Severity | Impact | Trigger | Root Cause | Workaround | Permanent Fix | Verification | Owner |
|---|---|---|---|---|---|---|---|---|
