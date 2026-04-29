# Trace Policy v1

> 状态：v1.0
> 作用：定义项目运行态 Trace 的结构、存储位置和生命周期。
> 行业对标：Arize OpenTelemetry, SWE-bench Trace Fingerprinting

---

## 1. Trace 定位

Trace 记录任务执行的关键事件，用于：
- 事后审计（出了什么、谁做的、什么证据）
- 故障分析（哪步出错、为什么）
- 后续 Eval（从真实执行生成回归用例）

Trace 不替代 Gate Artifact 或 Adoption Log，而是补充运行态视角。

---

## 2. 存储位置

```text
<project-root>/.proj/runs/{task_id}.jsonl
```

不放在 `proj-shared`，避免污染协议层。

---

## 3. Trace 事件格式

每行一个 JSON 对象：

```json
{
  "timestamp": "2026-04-29T12:00:00+08:00",
  "task_id": "harness-v1",
  "skill": "proj-exec",
  "phase": "execution",
  "event": "review_requested",
  "span": {
    "parent": "proj-exec",
    "name": "codex-review-round-1",
    "depth": 1
  },
  "input_summary": "...",
  "output_summary": "...",
  "gate": "gate_5",
  "next_skill": "proj-qa",
  "evidence": [],
  "risks": []
}
```

---

## 4. 事件类型

| event | 含义 |
|---|---|
| skill_entered | 进入某 skill |
| skill_exited | 退出某 skill |
| gate_proposed | 提出 Gate 决策 |
| gate_approved | 用户放行 |
| gate_rejected | 用户拒绝 |
| review_requested | 发起 review loop |
| review_received | 收到 review result |
| adoption_decided | 记录采纳决策 |
| error_reported | 异常报告 |

---

## 5. 按复杂度分级

| 级别 | Trace 要求 |
|---|---|
| L0 | 不强制写 trace |
| L1 | 建议记录 Gate 和 Review 事件 |
| L2 | 强制记录完整执行链 |

---

## 6. 安全约束

- Trace 默认存储摘要，不存完整敏感内容
- 文件路径、API key、密码等敏感信息必须脱敏
- Trace 文件不提交到远程仓库（应在 .gitignore 中）

---

## 7. 一句话规则

> Trace 存项目目录不存协议层；L0 不强制、L2 强制；摘要为主、脱敏为先。
