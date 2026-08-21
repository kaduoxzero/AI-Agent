# Sandbox、Shell、Filesystem 与 Code Execution

## 1. 为什么需要 Sandbox

当 Agent 可以：

- 执行 Shell；
- 修改文件；
- 安装依赖；
- 运行代码；
- Clone Repo；

它就已经接近“远程代码执行系统”。

不能直接让模型在宿主机高权限执行。

## 2. Sandbox

Sandbox 是隔离执行环境，用来限制 Agent 对宿主系统的影响。

```text
Agent Runtime
 ↓
Sandbox Boundary
├─ Workspace
├─ Shell
├─ Files
├─ Processes
└─ Network Policy
```

### 专业名词通义：Isolation

通过进程、容器、VM 或托管环境，让 Agent 的文件、网络和系统权限与宿主系统分离。

## 3. Workspace

每个任务建议有独立 Workspace：

```text
/workspace/task-123/
├─ repo/
├─ input/
├─ output/
└─ .agent/
```

避免多个 Agent 修改同一目录造成污染。

## 4. Sandbox 类型

### Local Process

开发方便，隔离较弱。

### Container

Docker / container runtime，适合多数开发和生产场景。

### VM / MicroVM

隔离更强，成本更高。

### Hosted Sandbox

由第三方提供生命周期、镜像和隔离。

## 5. Shell Tool

Shell 不应设计成无限制：

```text
shell(command: str)
```

至少需要：

- timeout；
- working directory；
- environment allowlist；
- output size limit；
- command audit；
- network policy。

高风险命令应阻止或审批。

## 6. Filesystem Tool

常见能力：

```text
list
read
search
patch
write
move
```

Coding Agent 推荐 Patch，而不是每次整文件重写。

需要防：

- `../` path traversal；
- 绝对路径越界；
- symlink escape；
- Secret File 读取。

## 7. Manifest / Workspace Contract

现代 Sandbox Agent 常用 Manifest 定义任务开始时 Workspace 应包含什么：

```text
Repo
Input Files
Output Directory
Environment
Mounts
```

Manifest 描述“初始工作空间契约”，不等于运行中的实时文件状态。

## 8. Snapshot

长任务可以保存 Workspace Snapshot：

```text
Workspace at T1
 ↓ snapshot
Resume later
```

注意区分：

- Agent Checkpoint：控制流 / State；
- Sandbox Snapshot：文件和执行环境状态。

大型 Coding Agent 往往两者都需要。

## 9. Secret 管理

Secret 不应持久化到 Snapshot / Log。

使用：

```text
Secret Manager
 ↓ runtime injection
Ephemeral Env
```

## 10. Network Policy

Coding Agent 默认不一定需要访问整个互联网。

可以：

```text
Allow package registry
Allow Git provider
Block internal metadata endpoint
Block private network
```

防止 SSRF / 数据外泄。

## 11. Resource Limits

限制：

```text
CPU
Memory
Disk
Process Count
Execution Time
Output Size
```

否则 Agent 一条错误命令可能耗尽 Worker。

## 12. OpenAI Sandbox Agent 的工程启发

当前 Agents SDK Sandbox Agent 将 Agent Definition、Manifest、Sandbox Session、Run State / Snapshot 分层，这个设计值得借鉴：外层 Runtime 管理 approvals、tracing、handoffs 和 resume；Sandbox 管理命令、文件变化和环境隔离。

## 13. 检查清单

- [ ] 每个任务是否独立 Workspace？
- [ ] Shell 是否有 Timeout？
- [ ] 是否限制目录逃逸？
- [ ] Secret 是否 ephemeral？
- [ ] 是否有 Network Policy？
- [ ] 是否限制 CPU / RAM / Disk？
- [ ] Checkpoint 与 Workspace Snapshot 是否区分？
- [ ] 所有命令是否可审计？

## 14. 参考

- OpenAI Agents SDK Sandbox Concepts：https://openai.github.io/openai-agents-python/sandbox/guide/
