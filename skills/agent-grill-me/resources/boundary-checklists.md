# Boundary Checklists — 边界与领域检查单库

> `agent-grill-me` 的战术检查单。每次进入执行前，按任务涉及的技术栈选用对应检查单快速扫描。
>
> 原则：技术型边界自动采用标准做法；业务型边界弹选择框询问用户。

## 1. 通用边界维度（13 类）

### 1.1 Input Boundary / 输入边界

- null / 空字符串 / 空数组 / 空对象
- 0 / 负数 / 最大值 / 最小值
- 超长文本 / 特殊字符 / Unicode / Emoji
- 非法格式 / 非预期类型
- 重复字段 / 缺少必填字段

示例：用户创建接口不要只考虑 `{"username": "kaduox"}`，还要考虑 username 为 null、空串、超长、已存在、含特殊字符。

### 1.2 Data Boundary / 数据边界

- 数据不存在 / 已删除
- 数据重复 / 状态已变化
- 关联数据不存在 / 数据过期
- 软删除 / 脏数据
- 历史数据格式不同 / 迁移兼容

### 1.3 Concurrency Boundary / 并发边界

- 两请求同时修改 / 重复点击 / 重复消费
- 并发扣减 / 分布式锁 / 乐观锁 / 悲观锁
- 幂等 / 请求重试 / 超时重试

库存、支付、下单、状态流转、MQ、定时任务、余额场景必须特别关注并发。

### 1.4 Transaction Boundary / 事务边界

检查组合：

```text
数据库成功 + 消息失败
数据库失败 + 消息成功
部分表成功 + 部分表失败
远程调用成功 + 本地事务失败
```

考虑：本地事务 / 分布式事务 / Outbox / 最终一致性 / 补偿机制 / 重试 / 死信队列。

### 1.5 Failure Boundary / 异常边界

- DB / Redis / MQ 挂了
- 第三方 API / AI API 超时
- 模型返回非法 JSON
- 网络中断 / 磁盘满 / 服务重启 / 请求超时 / 下游限流

不要默认所有依赖永远成功。

### 1.6 Permission Boundary / 权限边界

- 未登录 / Token 过期 / Token 伪造
- 普通用户访问管理员接口 / 用户访问他人数据
- 租户隔离 / 越权 / 数据权限 / API 权限 / 操作权限

### 1.7 Security Boundary / 安全边界

通用：

- SQL Injection / XSS / CSRF / SSRF
- Path Traversal / Command Injection / 文件上传风险
- 敏感信息泄露 / API Key 泄露 / 日志打印密码
- 任意文件读取 / 非法 URL / Webhook 伪造

AI 项目额外：

- Prompt Injection / Tool Injection
- RAG 污染 / 越权调用 Tool
- Agent 误执行危险命令 / 模型幻觉导致错误写操作

### 1.8 Performance Boundary / 性能边界

- 1 条 / 100 条 / 1 万条 / 100 万条数据
- 高并发 / 慢 SQL / N+1 Query
- 大对象 / 大文件 / 大模型上下文 / Token 爆炸
- 无限递归 / Agent 无限循环

方案只在小数据量下可行时必须指出。

### 1.9 API Boundary / 接口边界

- HTTP 状态码 / 错误码 / 参数校验
- 分页 / 排序 / 批量接口大小
- 幂等 / 超时 / 重试
- API 版本 / 向后兼容 / Response Schema / 空数据响应

### 1.10 State Machine Boundary / 状态机边界

有状态业务必须先画：状态 + 允许迁移 + 禁止迁移。

```text
待支付 → 已支付 → 已完成
待支付 → 已取消
禁止：已退款 → 已支付；已取消 → 已支付
```

状态规则属于业务决策时用选择框询问。

### 1.11 Time Boundary / 时间边界

- 时区 / 夏令时 / 零点 / 月末 / 年末 / 闰年
- 过期时间 / 定时任务重复执行 / 延迟任务
- 时间精度 / 数据库时间 vs 应用时间

### 1.12 Deployment Boundary / 部署边界

- 单机 / 多实例 / Docker / Kubernetes
- Windows / Linux 发行版差异
- 环境变量 / 配置中心 / Secret
- 服务发现 / 端口冲突 / 优雅停机

### 1.13 Compatibility Boundary / 兼容边界

- 老 API / 老数据库 / 老客户端 / 老数据
- Java / Python / 中间件 / PostgreSQL / Redis / SDK 版本

修改可能破坏旧功能时必须显式指出。

---

## 2. 领域专项检查单

### 2.1 API Checklist

```text
参数为空 / 参数非法 / 参数超长
资源不存在 / 重复请求 / 权限不足 / Token 过期
并发更新 / 数据库异常 / 第三方异常 / 超时
分页边界 / 排序字段非法 / 批量请求大小
返回值为空 / 错误码一致性
```

### 2.2 Database Checklist

```text
唯一约束 / NOT NULL / 索引 / 外键
软删除 / 时间字段 / 数据类型 / 超长字段
大表 / 分页 / 并发更新 / 事务 / 死锁
慢 SQL / 迁移 / 历史数据兼容
```

### 2.3 MQ Checklist（RabbitMQ / Kafka / RocketMQ 等）

```text
消息重复 / 消息丢失 / 消费者异常
重试 / 死信队列 / 幂等 / 乱序
消息积压 / 消费超时 / 事务一致性
```

### 2.4 Cache Checklist（Redis 等）

```text
缓存穿透 / 缓存击穿 / 缓存雪崩
热点 Key / 大 Key / 缓存一致性 / 过期时间
Redis 故障 / 并发写
分布式锁 / 锁过期 / 锁误删
```

### 2.5 AI Agent Checklist

```text
Prompt Injection / Tool Injection / 模型幻觉
Tool 调用失败 / Tool 返回异常
无限循环 / Agent 递归 / 上下文过长 / Token 成本
模型超时 / 模型限流 / JSON 输出非法
Memory 污染 / RAG 错误召回 / 知识库数据过期
Agent 权限越界 / 危险操作确认 / 人工兜底
```

### 2.6 RAG Checklist

```text
文档重复 / 文档版本 / 文档过期
切片过短 / 切片过长
召回为空 / 错误召回 / Embedding 失败 / 向量库不可用
权限隔离 / 知识库污染 / 来源追踪 / 引用
更新策略 / 删除策略
```

### 2.7 File Upload Checklist

```text
空文件 / 超大文件 / 非法扩展名 / 伪造 MIME
恶意脚本 / 重复文件 / 文件名特殊字符 / 路径穿越
文件损坏 / 解析失败 / 病毒风险 / 存储失败
```

---

## 3. 使用方式

1. 按任务技术栈挑选相关检查单；
2. 快速过一遍，标记命中项；
3. 技术型边界直接采用标准做法并记录默认值；
4. 业务型边界按 SKILL.md 第 5–8 节的决策分类与选项设计处理；
5. 高风险项走 Risk Escalation 清单强制确认。
