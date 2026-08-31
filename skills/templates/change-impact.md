# Agent 修改影响分析

> 用于已有项目修改前。先完成影响分析，再开始改代码。项目实例文件：`.agent-engineering/影响分析.md`。

## 修改目标

```text
请求的修改：
为什么需要：
预期用户可见行为：
非目标：
```

## 当前基线

```text
当前入口：
当前 Agent / Graph：
当前 Model / Prompt：
当前 Tools：
当前 RAG / Memory：
当前 State / Checkpoint：
当前 Tests / Evals：
当前已知失败：
```

## 必须保持的不变量

- [ ] Public API
- [ ] Request / Response Schema
- [ ] Task Status 行为
- [ ] Tool 名称 / Schema
- [ ] State Key
- [ ] Event Type
- [ ] 数据库兼容性
- [ ] 租户隔离
- [ ] 现有 Prompt 输出契约
- [ ] 现有用户可见行为

补充：

```text
其他不变量：
```

## 影响范围（Blast Radius）

| 区域 | 影响程度 | 风险 | 必须验证的内容 |
|---|---|---|---|
| API | 无 / 低 / 中 / 高 | | |
| Agent Runtime | | | |
| Prompt | | | |
| Tool | | | |
| State / Checkpoint | | | |
| RAG / Memory | | | |
| 数据库 | | | |
| Queue / Worker | | | |
| 安全 | | | |
| Eval | | | |
| Deployment | | | |

## 拟采用策略

优先选择：

```text
Adapter
新增隔离模块
扩展接口
局部重构
兼容层
Migration
重大重写
```

选择：

```text
策略：
为什么这是最小且安全的方案：
```

## 预计修改文件

```text
直接修改文件：
可能受影响文件：
明确不在范围内的文件：
```

## 兼容性

```text
是否向后兼容：是 / 否
是否需要 Migration：是 / 否
旧数据是否可读：是 / 否
是否支持旧客户端：是 / 否
Checkpoint 是否兼容：是 / 否
```

## 回滚

```text
回滚触发条件：
回滚步骤：
数据回滚：
配置回滚：
发布回滚：
```

## 测试计划

```text
静态检查：
单元测试：
回归测试：
功能测试：
Eval Suite：
安全测试：
集成测试：
冒烟测试：
```

## 停止条件

出现以下情况立即停止扩大修改：

- 影响面明显超过需求；
- 必须破坏核心公开契约；
- 旧数据无法安全迁移；
- 大量旧测试在改动前已失败；
- 发现更高优先级 P0 / P1 风险。

## 最终批准检查清单

- [ ] 基线已记录
- [ ] 不变量已识别
- [ ] Blast Radius 已分析
- [ ] 最小修改策略已选择
- [ ] 回滚路径存在
- [ ] 测试范围明确
