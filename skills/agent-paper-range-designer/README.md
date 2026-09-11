# agent-paper-range-designer

面向 **Paper Range / 纸上靶场 / Narrative Cyber Range** 的专项工程 Skill。

它负责把安全训练产品拆成稳定契约：

```text
Scenario
→ Typed Action Intent
→ Simulation Policy
→ WorldState
→ Story / Evidence
→ Learning Loop
→ Theme / UI Event
```

核心原则：**默认 Simulation-Only，场景外目标 Fail Closed。** 用户输入的 `nmap / curl / ssh` 等字符串不能直接进入系统 shell 或真实网络，而必须先归一化成模拟 Action。

## 适合

- 新增或改造纸上靶场场景；
- 设计虚构主机、服务、证据、Flag 和剧情分支；
- 设计 Action / WorldState / Story Graph；
- 设计 Hint / Score / 学习报告；
- 设计 Theme Pack Registry；
- 审查 Session Reset 和网络隔离边界。

## 不适合

- 对真实目标进行渗透测试；
- 普通 Agent 项目；
- 与模拟契约无关的纯样式调整。

执行协议见 `SKILL.md`，机器可读能力清单见 `skill.yaml`。
