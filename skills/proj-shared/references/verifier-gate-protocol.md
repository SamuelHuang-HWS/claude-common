# Verifier Gate Protocol v1

> 状态：v1.0
> 作用：定义关键节点的独立智能体核验门禁。
> 定位：本协议只定义 `review-loop-policy-v1.md` 的增量约束，不替代 Gate / Review Loop / Harness 协议。

---

## 1. 继承关系

Verifier Gate 必须复用现有协议：

- Gate 结构沿用 `gate-artifact-policy-v1.md`。
- Review Loop 沿用 `review-loop-policy-v1.md` 的 `review_packet -> review_result -> adoption_log`。
- Reviewer 权限沿用 `harness-model-v1.md`：只读、不写文件、不 commit、不 push。

禁止另起一套并行格式。若需要记录主 agent 对 reviewer finding 的处理，必须写入 `adoption_log.owner_resolution`，而不是创建独立的 review 系统。

---

## 2. Phase 2–3 适用范围

Phase 2 仅覆盖：

| 位置 | Gate / Handoff | 要求 |
|---|---|---|
| `proj-review` | Gate 3：实施放行 | `pre-exec` 或 L1/L2 时触发 Verifier Gate |
| `proj-exec` | `proj-exec -> proj-qa` handoff | 只声明是否需要 Verifier Gate，不直接执行 |
| `proj-qa` | 上游证据检查 | 只检查证据，不补做 Verifier Gate |
| `proj-docs` | Phase 3 文档证据 | 只输出自身 `docs_evidence`，不透传 QA / Verifier 证据 |
| `proj-close` | Phase 3 最终证据门禁 | 只检查证据存在性与状态，不重做 QA / Verifier Gate |

暂不覆盖：
- Gate 4：实施中途确认；
- Gate 5：QA 放行时再次执行 Verifier Gate；
- `proj-close` / `proj-docs` 的 Gate 执行逻辑（Phase 3 只做证据输出/检查）。

---

## 3. 触发条件

满足任一条件时，必须触发或声明 Verifier Gate：

- 任务复杂度为 L1/L2；
- `proj-review.level == pre-exec`；
- 涉及权限、安全、迁移、新依赖、核心链路；
- Reviewer / QA 发现 P0/P1 风险；
- 用户显式要求 cross-review / consult / Claude Code 审核。

L0 默认不强制，除非命中高风险关键词或用户显式要求。

---

## 4. Review Packet 增量字段

Verifier Gate 使用 `review-loop-policy-v1.md` 的 `review_packet`，并允许增加以下字段：

```yaml
review_packet:
  verifier_gate:
    gate_id: gate_3
    trigger_reason: "L1 pre-exec review"
    blocking_threshold: P1
    must_check:
      - protocol_evidence
      - acceptance_criteria
      - risk_control
      - ready_for_next_step
```

---

## 5. Adoption Log 增量字段

主 agent 必须对 reviewer findings 逐条处理，并写入 `adoption_log.owner_resolution`：

```yaml
adoption_log:
  accepted:
    - finding_id: "VG-001"
      action: "..."
  rejected:
    - finding_id: "VG-002"
      reason: "..."
  deferred:
    - finding_id: "VG-003"
      reason: "..."
  owner_resolution:
    - finding_id: "VG-001"
      decision: accepted | rejected | deferred | needs_user
      action_taken: "..."
      evidence: "命令、文件、手测结果或明确理由"
      remaining_risk: "..."
      recheck_required: true
```

`recheck_required` 默认应为 `true`。仅当 finding 被 `deferred` 且用户明确接受剩余风险时，才可设为 `false`。

---

## 6. Fail-closed 规则

- 存在未处理的 P0/P1 reviewer finding 时，不得进入下一 Gate。
- `owner_resolution` 缺失时，不得声明 `ready_for_dev: YES` 或 `ready_for_next_step: YES`。
- `proj-exec` 只输出 `verifier_handoff` 声明；若声明需要 Verifier Gate 但未完成，`proj-qa` 必须 fail closed。
- Review Loop 最多 2 轮。超过 2 轮或出现稳定分歧时，必须交给用户裁决。

---

## 7. 用户裁决条件

以下情况必须停止自动推进并交给用户：

- P0 finding 被主 agent 拒绝；
- P1 finding 连续两轮未收敛；
- reviewer 与主 agent 对范围、风险或验收标准存在稳定分歧；
- 需要破坏性操作、历史改写、批量迁移或安全权限变更；
- 继续推进会突破用户授权范围。

---

## 8. 一句话规则

> Verifier Gate 不是第二套 review 系统；它是 Gate 3 与 exec→qa handoff 上的强制 `review_packet -> review_result -> adoption_log.owner_resolution` 闭环。P0/P1 未闭环，不得放行。
