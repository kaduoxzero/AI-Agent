# Paper Range / 纸上靶场

Paper Range 是 AI-Agent 仓库中的叙事式安全推演实验场。用户输入的自然语言或“命令”只会被映射为 **Typed Action Contract → Simulated Runtime → WorldState → Story Graph → Narrative/Event → UI**。所有目标、服务、日志、资产关系、目录、凭据和结果都来自虚构场景，不会执行真实扫描器、系统 shell 或真实网络请求。

## 当前版本

当前后端 API：**0.6.0 / Investigation Engine v2**。

本版本在 v0.5 Live Story UI 上新增：

- Story Graph v2：第二层 `evidence-strategy` 条件分支；
- `direct`：直接验证候选证据；
- `correlate`：必须完成日志查询 + 资产关系映射，才能继续读取证据；
- `query_logs` simulation-only 动作；
- `trace_asset` simulation-only 动作；
- `evidence_strategy` / `investigation_checks` WorldState；
- 前端双层 Story Graph、条件检查清单和跳过节点显示；
- Playwright 浏览器 E2E smoke；
- CI 中启动真实 Docker Compose 栈并通过 Chromium 操作页面。

## 当前可玩链路

```text
创建临时 Session + 随机 Theme Pack
  ↓
端口侦察
  ↓
Web 初查
  ↓
第一层 Story Branch
  ├─ focused：定向、低噪声
  └─ broad：广覆盖、更多路径、-3 分
  ↓
路径枚举
  ↓
第二层 Evidence Strategy
  ├─ direct
  │    └─ 直接进入 evidence-review
  │
  └─ correlate
       ├─ SIMULATED LOG QUERY
       ├─ SIMULATED ASSET MAP
       └─ 两项都完成后才进入 evidence-review
  ↓
证据读取
  ↓
模拟 SSH 验证
  ↓
Flag + 学习报告
```

旧版五段式流程仍然兼容：如果玩家不显式选择第一层分支，Runtime 默认 `focused`；如果不显式选择第二层证据策略，读取证据时默认 `direct`。

## Typed Action Contract

```text
nmap -p- <scene-target>                 → scan_ports
curl http://<scene-target>              → inspect_web
approach focused                        → select_approach(focused)
approach broad                          → select_approach(broad)
dirsearch -u http://<scene-target>      → enumerate_paths
evidence direct                         → select_evidence_strategy(direct)
evidence correlate                      → select_evidence_strategy(correlate)
grep incident /var/log/paper-range/...  → query_logs
asset-map                               → trace_asset
cat /discovered/evidence                → inspect_file
ssh user@<scene-target>                  → ssh_access
```

自然语言也会归一化到相同 Contract，例如“关联证据”“查询日志”“追踪资产关系”“直接验证”。这些字符串从不交给系统 shell。

## Story Graph v2 / WorldState

每个 Session 现在维护：

- `story_node`：当前剧情节点；
- `story_branch`：`focused | broad`；
- `evidence_strategy`：`direct | correlate`；
- `investigation_checks`：例如 `log-query`、`asset-map`；
- `world_tags`：例如 `low-noise-recon`、`correlation-route`、`correlated-evidence`；
- `consequences`：当前局不可回滚的剧情后果。

核心节点：

```text
recon
  ↓
web-investigation
  ↓
approach-decision
  ↓
path-enumeration
  ↓
evidence-strategy
  ├─ direct ───────────────→ evidence-review
  └─ correlate → correlation-work
                    ├─ log-query
                    └─ asset-map
                         ↓ both complete
                    evidence-review
  ↓
access-validation
  ↓
complete
```

### direct

`direct` 更快，会写入 `direct-evidence-route`，并跳过 correlation-work。学习报告会建议下一局尝试 correlate。

### correlate

`correlate` 会写入 `correlation-route`。证据读取前必须满足：

```text
investigation_checks ⊇ {log-query, asset-map}
```

满足后写入 `correlated-evidence`，学习报告会记录玩家完成了日志时间线与资产关系的双重关联。

## Simulation-only 工具

### 模拟日志查询

```text
grep incident /var/log/paper-range/events.log
```

返回的是 Runtime 生成的训练事件，不读取容器真实日志，也不会执行 `grep`。输出会明确标记：

```text
network_io=none
```

### 模拟资产关系映射

```text
asset-map
```

只把当前 Scenario 已经公开给 Runtime 的虚构服务画像组织成关系信息。输出范围固定为：

```text
scope=current-fictional-scenario-only
network_io=none
```

场景外 IP 继续 fail-closed。

## SSE Live Event Stream

浏览器通过：

```text
GET /api/sessions/{session_id}/events?after=<event-seq>
```

消费 `GameEvent`。`GameEvent.seq` 也是 SSE `id`，支持 `Last-Event-ID` 重连续传。Action HTTP 响应负责同步 WorldState，SSE 负责 Agent / Narrative / Reward 演出。

SSE 只读取当前进程内 `SessionStore`，不会新增 Redis、数据库或持久化。

## 浏览器 E2E

前端使用 Playwright Chromium 做第一批真实浏览器 smoke test。CI 会：

```text
backend pytest
  ↓
frontend build
  ↓
docker compose config
  ↓
docker compose build
  ↓
docker compose up -d
  ↓
Chromium 打开 http://127.0.0.1:8080
  ↓
实际点击 scenario / focused / correlate / log-query / asset-map
  ↓
验证 Story Graph / SSE / WorldState UI
  ↓
docker compose down -v
```

本地运行：

```bash
cd projects/paper-range/frontend
npm install
npx playwright install chromium
npm run test:e2e
```

需要先确保 Paper Range 已运行在 `http://127.0.0.1:8080`，或通过 `PAPER_RANGE_BASE_URL` 指定地址。

## 场景与 Theme

当前包含 6 个虚构战役：废弃研究所、企业内网残影、地下交易市场、市政档案馆断电夜、轨道中继站静默协议、赤港夜班货运站。

当前有 12 套 Theme Pack：`inferno`、`blood-moon`、`black-site`、`ash-cathedral`、`neon-crypt`、`reactor-amber`、`plague-green`、`ice-vault`、`violet-null`、`rust-foundry`、`signal-blue`、`obsidian-gold`。最终目标仍是 40 套。

## 剧情秘密边界

`GET /api/scenarios` 不提前下发：

- 隐藏路径；
- Web 观察正文；
- 证据正文；
- 训练密码；
- Flag。

当前 UI 为 SSH 快捷提示仍会得到剧情用户名；密码和完成条件不会预泄露。

## Session 生命周期

```text
container start
  ↓
新的 SessionStore
  ↓
运行期间复用 WorldState / Story Graph / Event / Score / Theme
  ↓
container stop/remove
  ↓
全部游戏 Session 消失
```

不写 PostgreSQL、不写 Redis、不写宿主机游戏状态文件，Compose 不挂载游戏数据卷。

## 一键启动

```bash
cd projects/paper-range
docker compose up --build
```

打开：`http://127.0.0.1:8080`

健康检查：`http://127.0.0.1:8080/health`

## API

```text
GET    /health
GET    /api/scenarios
POST   /api/sessions
GET    /api/sessions/{session_id}
GET    /api/sessions/{session_id}/events
POST   /api/sessions/{session_id}/actions
POST   /api/sessions/{session_id}/hint
GET    /api/sessions/{session_id}/report
DELETE /api/sessions/{session_id}
```

## AI-Agent Skill 集成

仓库已注册 `agent-paper-range-designer`，用于维护 Paper Range 的 simulation-only Scenario / Action / WorldState / Story / Learning / Theme contracts。

## 下一阶段

1. 增加 HTTP 变体、结构化日志字段和更丰富的资产关系调查；
2. 将 Story Graph 条件与场景数据解耦，形成可配置 Graph Contract；
3. 扩充 Playwright E2E：完成整局、SSE 重连、移动端布局；
4. Theme Pack 从 12 扩展到 40，并加入场景/主题加权；
5. 场景生成器与难度/评分策略数据化。
