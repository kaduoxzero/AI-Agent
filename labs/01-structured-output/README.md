# Lab 01｜Structured Output：把模型输出变成可验证契约

> 目标：不要把 Agent 的核心状态建立在“模型大概会返回这个 JSON”上，而是把输出当成真正的数据契约进行解析、校验和失败处理。

## 1. 学习目标

完成本实验后应能够：

- 使用 Pydantic 定义 Agent 输出 Schema；
- 区分“JSON 可解析”和“业务合法”两个层次；
- 对未知字段、非法 Enum、越界置信度进行拒绝；
- 将模型输出失败转换成显式错误，而不是静默补默认值；
- 理解 Structured Output 为什么是 Router、Planner、Evaluator、Tool Arguments 的基础。

## 2. 专业名词通义

- **Schema**：数据结构契约，规定字段、类型、是否必填以及约束。
- **Validation**：验证输入是否满足契约。
- **Strict Model**：不接受 Schema 中未声明字段的数据模型。
- **Fail Closed**：无法确认结果合法时拒绝继续，而不是猜一个默认值。

## 3. 运行

```bash
cd labs/01-structured-output
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
# source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

## 4. 实验任务

`app.py` 内置 4 组模拟模型输出：

1. 合法输出；
2. `risk_level` 不在允许枚举中；
3. `confidence` 超出 0~1；
4. 模型偷偷增加未声明字段。

观察 Pydantic 如何拒绝错误结果。

## 5. 工程延伸

将 `parse_model_output()` 替换为真实模型 SDK 时，应尽量使用 Provider 原生 JSON Schema / Structured Output 能力，而不是只提示“请输出 JSON”。即使 Provider 保证 JSON 格式，业务层仍然建议进行一次本地 Schema 校验。

典型生产链路：

```text
Model
  ↓
Structured Output / JSON Schema
  ↓
Local Validation
  ↓
Business Rule Validation
  ↓
State Update
```

## 6. 验收标准

- [ ] 合法样例能成功解析；
- [ ] 非法 Enum 被拒绝；
- [ ] 越界 confidence 被拒绝；
- [ ] 未声明字段被拒绝；
- [ ] 代码中没有 `except: pass`；
- [ ] 能解释为什么 Router 输出必须结构化。

## 7. 进一步挑战

增加：

- `reasons: list[str]` 数量限制；
- `evidence_ids: list[str]`；
- `requires_human_approval: bool`；
- 二次业务校验：`risk_level == high` 时必须存在 Evidence。
