# Agent UX、任务进度、Artifact 与 Human Interaction

## 1. Agent UI 与聊天机器人 UI 的区别

普通 Chat UI：

```text
User message
Assistant message
```

大型 Agent UI 需要表达“任务正在执行”。

```text
Task
├─ Progress
├─ Tool Activity
├─ Subtasks
├─ Artifacts
├─ Citations
├─ Approval
└─ Final Result
```

## 2. Progressive Disclosure

不要把所有 Agent 内部细节直接倾倒给用户。

推荐三个层级：

### 默认层

```text
正在查询知识库…
正在比较 8 个候选方案…
报告生成完成。
```

### 展开层

显示 Tool、来源、耗时。

### Debug 层

开发人员可查看完整 Trace ID、Node、结构化 State 等。

## 3. 不展示私有 Chain-of-Thought

产品可以展示：

- 计划；
- 执行步骤；
- Tool 名称；
- 来源；
- 结果摘要；
- 状态。

不需要把模型私有推理过程作为“思考日志”展示。

## 4. Task UI

长任务应拥有独立 Task：

```text
Task ID
Title
Status
Progress
Started At
Current Step
Artifacts
Cancel
Retry
Resume
```

不要只把它绑在一个 WebSocket 连接上，否则刷新浏览器后任务“消失”。

## 5. Approval UI

高风险 Tool 审批不能只显示：

> 允许吗？

应该显示：

```text
Action: delete_repository
Target: repo-123
Reason: 用户明确要求清理旧测试仓库
Impact: 不可恢复删除
Arguments: {...}
```

用户才能做有效决定。

## 6. Artifact

Artifact 是 Agent 任务产生的稳定产物：

- Markdown；
- PDF；
- Spreadsheet；
- Code Patch；
- Image；
- JSON；
- Report。

与聊天消息分离。

```text
Conversation → explains
Artifact → deliverable
```

## 7. Citation UX

Citation 应让用户：

- 看到哪句话有来源；
- 点击来源；
- 查看文档 / 页码；
- 判断来源新旧。

不要只在末尾列几十个链接。

## 8. Error UX

错误分类展示：

```text
Tool temporary failure → retrying
Permission denied → request access
Need user input → ask user
Task failed → show recoverable checkpoint
```

不要统一显示“AI 出错了”。

## 9. Cancel / Retry / Resume

长任务必须提供：

- Cancel；
- Retry failed step；
- Resume from checkpoint；
- Edit and resume（适用时）。

## 10. Multi-Agent UX

用户通常不需要知道内部有 12 个 Agent。

只在有价值时展示：

```text
Research
Data Analysis
Review
```

架构复杂度不是产品卖点。

## 11. Human-Agent Trust

Agent 的语言越自信，人越容易过度信任。

高风险系统应该：

- 明示 Evidence；
- 明示不确定性；
- 区分建议与已执行 Action；
- 高风险 Action 二次确认。

## 12. 检查清单

- [ ] 长任务是否有 Task 页面？
- [ ] 页面刷新后是否能恢复进度？
- [ ] 是否展示计划 / Progress，而非私有推理？
- [ ] Approval 是否显示影响和参数？
- [ ] Artifact 是否与 Conversation 分离？
- [ ] Citation 是否可点击追溯？
- [ ] 用户是否能 Cancel / Retry / Resume？
