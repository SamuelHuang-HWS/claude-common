# Review Loop Policy v1

> 状态：v1.0
> 作用：定义 Antigravity ↔ Codex/Opus 的 Review Loop 闭环协议。
> 行业对标：Ask → Action → Audit, Producer-Reviewer Pattern

---

## 1. 适用场景

Review Loop 适用于：
- `proj-review`：开发前方案评审
- `proj-qa`：实现后质量验证
- `cross-review`：step/task 级双模型复核

不适用于：
- L0 简单任务（除非用户显式要求）
- 纯文档整理（proj-docs）

---

## 2. 三段式闭环

```text
Antigravity 执行
→ 生成 review_packet
→ 发送给 Codex/Opus
→ Codex/Opus 返回 review_result
→ Antigravity 生成 adoption_log
→ Antigravity 按 adoption_log 修正
→ 必要时进入第 2 轮
→ User Gate 放行
```

---

## 3. Review Packet 格式

```yaml
review_packet:
  task_summary: "..."
  phase: "proj-review | proj-qa | cross-review"
  changed_files:
    - "..."
  relevant_rules:
    - "Sisyphus V3.0"
    - "proj-shared"
  acceptance_criteria:
    - "..."
  verification_evidence:
    - command: "..."
      result: "..."
  questions:
    - "是否存在 P0/P1/P2 风险？"
    - "是否可以进入下一 Gate？"
```

---

## 4. Review Result 格式

```yaml
review_result:
  status: PASS | FIX | BLOCKED
  confidence: 0.0-1.0
  findings:
    - priority: P0 | P1 | P2 | P3
      file: "..."
      issue: "..."
      recommendation: "..."
  gate_decision:
    ready_for_next_step: YES | NO | CONDITIONAL
  required_actions:
    - "..."
```

---

## 5. Adoption Log 格式

```yaml
adoption_log:
  accepted:
    - finding_id: "..."
      action: "..."
  rejected:
    - finding_id: "..."
      reason: "..."
  deferred:
    - finding_id: "..."
      reason: "..."
```

---

## 6. 循环控制

### 6.1 最大轮次

```yaml
max_rounds: 2
```

默认最多 2 轮 review loop。超过 2 轮时：
- Antigravity 必须停止自动循环
- 将未解决的 findings 汇总提交给用户
- 由用户决定是否继续、接受当前状态或重新规划

### 6.2 Doom-Loop Detection（声明）

> 本 policy 声明 doom-loop detection 规则。运行时实现属于 Phase 4。

检测条件：
- 连续 2 轮 review 的 findings 实质相同（相同文件 + 相同类别）
- Antigravity 的修正未实质改变 review_result.status
- adoption_log 中 rejected 的 finding 在下一轮被重新提出

检测到 doom-loop 时：
- 强制终止 review loop
- 生成 doom-loop 报告提交用户
- 用户决定下一步

---

## 7. Reviewer 权限约束

所有 Reviewer（Codex / Claude Opus / 其他模型）在 review loop 中：

```yaml
reviewer_permissions:
  can_read: true
  can_suggest_patch: true
  can_write_files: false
  can_commit: false
  can_push: false
  can_override_user_gate: false
```

---

## 8. CLI 调用约定

### 8.1 Provider 调用

通过 `codex exec` 无状态调用 Codex：

```bash
codex exec "<review_packet prompt>" 2>&1
```

规则：
- 不指定 `-m` 模型参数，用默认值；
- 不做预检（不 ping、不 which、不读 config）；
- cwd 设为目标项目目录；
- Codex 只读，不修改文件。

多方讨论时可同时调用 Claude Code：

```bash
echo "<review_packet prompt>" | claude -p --add-dir $PROJECT_DIR --output-format json --no-session-persistence 2>&1
```

### 8.2 Provider 不可用处理

若 Codex 不可用（超时、连接失败等）：
- 按 Sisyphus 红线"禁止静默失败"处理
- 报告"现象 + 影响 + 建议处理"
- 建议：降级为当前 agent 单侧评审 + 用户 Gate 确认

---

## 9. 与其他协议的关系

- Review Loop 的触发时机由 `ai-team-workflow-model-v1.md` 的 Gate 定义
- Review Loop 的角色权限由 `harness-model-v1.md` 定义
- Review Loop 的具体操作由各 skill（proj-review / proj-qa / cross-review）实现
- Review Packet 模板：`proj-shared/templates/review-packet-template.yaml`
- Cross-review 完整流程：`cross-review/references/flow.md`
- 多智能体讨论能力层：`consult/SKILL.md`

---

## 10. 一句话规则

> Review Loop 最多 2 轮，超出交给用户；Reviewer 只读不写；adoption_log 记录所有采纳/拒绝/延迟决策；Codex 通过 `codex exec` 调用。

