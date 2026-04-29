# Gate Artifact Policy v1

> 状态：v1.0
> 作用：统一 Gate 1-6 的输出格式，确保每个 Gate 产物可机器解析、可追溯。
> 行业对标：Harness.io Approval Gates, LangGraph interrupt()

---

## 1. Gate 定义

| Gate | 名称 | 阶段 | Owner |
|---|---|---|---|
| Gate 1 | 启动理解确认 | proj-start 后 | 用户 |
| Gate 2 | 需求加工确认 | proj-pm / proj-uiux 后 | 用户 |
| Gate 3 | 实施放行 | proj-review 后 | 用户 |
| Gate 4 | 实施中途确认 | proj-exec 中 | 用户 |
| Gate 5 | QA 放行 | proj-qa 后 | 用户 |
| Gate 6 | 最终完成 | proj-close 后 | 用户 |

---

## 2. Gate Artifact 格式

```yaml
gate:
  id: gate_3
  name: implementation_release
  status: PASS | FAIL | CONDITIONAL
  owner: user
  reviewer: antigravity | codex | claude_opus
  phase: proj-review | proj-qa | proj-close

  decision:
    ready_for_next_step: YES | NO | CONDITIONAL
    next_skill: proj-exec
    conditions:
      - "..."

  risks:
    - priority: P0 | P1 | P2 | P3
      description: "..."

  evidence:
    - type: command | manual | review
      detail: "..."
      result: "..."

  user_confirmation_required: true
```

---

## 3. 按复杂度分级

| 级别 | Gate 要求 |
|---|---|
| L0 | Gate 1 + Gate 5 可最小化；若进入 close/commit，Gate 6 也必须有轻量输出 |
| L1 | Gate 1 + Gate 3 + Gate 5 建议输出 |
| L2 | Gate 1-6 完整输出，强制 |

---

## 4. Gate 与 Skill 的映射

| Skill 完成后 | 产出 Gate |
|---|---|
| proj-start | Gate 1 |
| proj-pm / proj-uiux / proj-struct | Gate 2 |
| proj-review | Gate 3 |
| proj-exec (中途) | Gate 4 |
| proj-qa | Gate 5 |
| proj-close | Gate 6 |

---

## 5. 一句话规则

> 每个 Gate 产物必须包含 status + decision + evidence + user_confirmation_required；L0 轻量、L1 建议、L2 强制。
