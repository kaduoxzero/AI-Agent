# Lab 14｜Sandbox Coding Agent：Workspace、Path Boundary、Command Policy 与 Timeout

> 目标：理解 Coding Agent 不能直接拿宿主机 Shell 权限。先实现一个教学用受限 Workspace，再理解为什么生产环境需要 Container / MicroVM 级隔离。

## 1. 学习目标

完成后应能够：

- 为每个任务创建独立 Workspace；
- 防止路径逃逸（`../`）；
- 使用 Command Allowlist；
- 禁止 `shell=True`；
- 为进程设置 Timeout；
- 输出 Diff / Artifact，而不是直接覆盖真实仓库；
- 理解应用层限制与真正 OS Sandbox 的区别。

## 2. 专业名词通义

- **Workspace**：Agent 当前任务能读写的隔离工作目录。
- **Path Traversal**：通过 `../` 等路径访问 Workspace 外文件。
- **Command Allowlist**：只允许预先批准的命令形态。
- **Sandbox**：限制代码、文件、网络、进程和资源访问的隔离执行环境。
- **MicroVM**：比普通进程隔离更强的轻量虚拟机执行环境。

## 3. 重要边界

本实验是**应用层教学 Sandbox**，用于演示：

```text
Path Boundary
Command Policy
Timeout
Workspace Lifecycle
```

它不是强安全隔离。真实不可信代码执行应使用：

```text
Container / gVisor / Firecracker / MicroVM / Remote Sandbox
```

并限制：

```text
CPU
Memory
Disk
Network
Syscall
Credential
Execution Time
```

## 4. 运行

```bash
cd labs/14-sandbox-coding-agent
python app.py
```

## 5. 实验行为

程序会：

1. 创建临时 Workspace；
2. 写入一个 Python 文件；
3. 运行 `python -m py_compile`；
4. 尝试 `../secret.txt` 路径逃逸并确认被拒绝；
5. 尝试未授权命令并确认被拒绝。

## 6. 生产 Coding Agent

真正 Coding Agent 的执行链通常是：

```text
Task
 ↓
Create Sandbox
 ↓
Clone / Mount Repo
 ↓
Read / Search
 ↓
Patch
 ↓
Test
 ↓
Diff
 ↓
Review
 ↓
Destroy Sandbox
```

Agent 不应直接获得宿主机长期 Secret。

## 7. 验收标准

- [ ] 无法访问 Workspace 外路径；
- [ ] 不使用 `shell=True`；
- [ ] Command 必须经过 Policy；
- [ ] Process 有 Timeout；
- [ ] Workspace 生命周期明确；
- [ ] 能解释为什么这仍然不等于强 Sandbox；
- [ ] 能描述生产 MicroVM / Container 隔离需要增加什么。
