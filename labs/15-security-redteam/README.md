# Lab 15｜Agent Security Red Team：Injection、Tenant、Memory、Agency 与 Handoff

> 目标：把安全要求变成可自动回归的测试集，而不是只在 Prompt 里写“请注意安全”。

## 1. 学习目标

完成后应能够：

- 建立 Agent Security Golden Dataset；
- 测试 Direct / Indirect Prompt Injection；
- 测试 Tenant Leakage；
- 测试 Memory Poisoning；
- 测试 Excessive Agency；
- 测试 Unsafe Handoff；
- 为 Critical Case 建立 100% Pass Gate。

## 2. 专业名词通义

- **Red Team**：主动从攻击者角度设计输入，验证系统是否会越权或失控。
- **Indirect Prompt Injection**：恶意指令藏在网页、文档、邮件、Tool Result 等外部内容中。
- **Excessive Agency**：Agent 拥有超过完成任务所需的功能、权限或自主权。
- **Tenant Leakage**：跨租户读取或泄露数据。
- **Unsafe Handoff**：把任务移交给权限更高、职责不匹配的 Agent，导致权限升级。

## 3. 运行

```bash
cd labs/15-security-redteam
python run_redteam.py
```

Dataset：

```text
../../evals/security/redteam.jsonl
```

## 4. 安全测试思路

```text
Attack Case
 ↓
Agent / Policy System
 ↓
Action Decision
 ↓
Allowed / Blocked
 ↓
Assertion
```

Critical Case 不应该用平均分掩盖：

```text
100 个普通 Case 通过
+ 1 个跨租户泄漏失败
≠ 99% 很优秀
```

对于关键安全边界，应采用：

```text
Critical Security Pass Rate = 100%
```

## 5. 实验任务

1. 运行 baseline；
2. 故意删除一条 Policy，观察测试失败；
3. 增加 Tool Result Poisoning Case；
4. 增加 Credential Leak Case；
5. 增加 Browser Indirect Injection；
6. 将该脚本加入 CI。

## 6. 生产化原则

安全控制应该分层：

```text
Input Validation
Identity / Authorization
Tool Policy
Tenant Isolation
Memory Write Policy
HITL
Output Guardrail
Audit
```

不要把所有安全问题交给第二个 LLM Reviewer。

## 7. 验收标准

- [ ] Security Dataset 被版本控制；
- [ ] Direct / Indirect Injection 有测试；
- [ ] Tenant Leakage 有测试；
- [ ] Memory Poisoning 有测试；
- [ ] Excessive Agency 有测试；
- [ ] Unsafe Handoff 有测试；
- [ ] Critical Case 失败时退出码非零；
- [ ] 可以进入 CI Gate。
