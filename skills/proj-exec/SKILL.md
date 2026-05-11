---
name: proj-exec
description: 核心代码实施入口。接收 proj-tdd 给出的红色报错证明 (Red Proof) 或 proj-pm 给出的 L0 级 Bug Fix 契约。严格执行代码编写直至变绿 (Green Proof)。强制物理隔离。
version: 1.0.0
ssop_version: 1.1.0
created_at: 2026-05-06
---

# proj-exec — Sisyphus Stateful Output Protocol (SSOP)

## 1. 节点定位与强制物理隔离

```
proj-pm (product_definition)
  → proj-struct (architecture_definition)
    → proj-tdd (tdd_definition / Red Proof)
      → ★ proj-exec (execution_definition / Green Proof) ★
        → proj-qa  (review gate, strictly physically isolated)
        → proj-docs (documentation, fast-track for trivial patches)
```

**`proj-exec` 是整条流水线中唯一允许修改/编写业务逻辑代码的节点。**

**【红线约束：物理隔离】**
执行 `proj-exec` 的 Agent，绝对不可以是刚刚执行 `proj-tdd` 写测试的 Agent，也绝对不可以是后续执行 `proj-qa` 的 Agent。
这种隔离强制打破上下文连贯性，逼迫 Agent 只能通过上游的 `Red Proof`（终端报错日志）来理解验收标准，从而消除幻觉。

---

## 2. SSOP 状态机

```
┌──────────┐
│ initialize│ ← 解析输入契约
└─────┬─────┘
      │
      ▼
┌──────────┐     测试存在致命漏洞/歧义
│  clarify  │ ──────────────────────────► ┌──────────┐
│ (可选)    │ ◄── 修正后的测试或人类干预     │ executing │◄─── 变绿循环
└─────┬─────┘                             └─────┬─────┘────┘
      │                                       │
      │                                       ▼
      │                                  ┌──────────┐
      │                                  │  verify   │
      │                                  └─────┬─────┘
      │                                       │
      └──────────────────────────────────────►▼
                                          ┌──────────┐
                                          │ complete │ ← 终态
                                          └──────────┘
```

| 阶段 | 说明 |
|------|------|
| `initialize` | 校验上游契约。`mode: build` 必须有 `proj-tdd` 输出；`mode: patch` 允许直连 `proj-pm`。 |
| `executing` | 根据上游的 `Red Proof` 报错，编写/修改业务代码，并不断运行测试直到变绿。 |
| `clarify` | 如果发现 `proj-tdd` 给的测试在当前架构下根本不可实现（死锁），打回并暂停。 |
| `verify` | 严格比对 Diff，确保没有修改无关代码，没有残留 `console.log` 等。生成 `Green Proof`。 |
| `complete` | 生成 `execution_definition` YAML，流转给 `proj-qa`。 |

---

## 3. 输入契约

### 3.1 主输入 (Build Mode)

当接到完整需求时，必须有 `proj-tdd` 输出的失败测试证明：

```yaml
tdd_definition:
  _meta:
    pipeline_id: string
    source: proj-tdd
    pipeline_mode: build
    tdd_mode: strict | contract | mixed

  isolation_audit:
    producer_agent_id: string
    handoff_medium: artifact_only

  test_artifacts:
    - file: "src/utils/math.test.ts"
      tier: STRICT_TDD | CONTRACT_TDD
      target_component: string
      red_proof:
        status: valid
        cwd: string
        exit_code: 1
        harness_status: pass
        failure_class: assertion_failure | missing_symbol | contract_missing
        expected_failure_reason: string
        log_sha256: string
        error_excerpt: "ReferenceError: xxx is not defined" # 这个错就是你要修的目标
```

### 3.2 降级输入 (Patch Mode)

仅限于 L0-L1 级别的不涉及架构变动的 Bug 修复，允许跳过 TDD：

```yaml
_meta:
  pipeline_id: string
  source: proj-pm
  risk_level: L0
  mode: patch

target_files:
  - path: string
    change_type: patch
    description: "Fix: ..."
```

---

## 4. 核心执行规则 (Agent Behavioral Constraints)

### 4.1 变绿驱动 (Green Proof Drive)
在 `mode: build` 下，Agent 的唯一任务就是写代码消除 `red_proof` 里的错误。
你**无权自己补充测试逻辑**。你的目标是输出 `Green Proof`（测试全部 pass 的截图/日志）。如果测试写错了，把皮球踢回给 `proj-tdd` (`unhandled_gaps: test_unsatisfiable`)。

### 4.2 最小变更原则 (Diff Discipline)
- 不允许修改任何不在 `target_component` 和为了让测试变绿而必须修改的依赖文件之外的代码。
- 如果发现原代码有“可以优化的空间”，**强忍住，不要改**。记录在 `unhandled_gaps (info)` 里让下游决断。

### 4.3 死胡同打回机制 (Anti-Doom Loop)
如果连续 3 次尝试修改业务代码依然无法让测试变绿，大概率是测试的契约存在根本性谬误。必须停止盲目修改，退回给 `proj-tdd` 或 `proj-struct`重写测试/架构。
**必须提交证据确凿的 Unsatisfiable Report**，禁止无理由踢回。

---

## 5. 输出契约 (`execution_definition`)

```yaml
execution_definition:
  _meta:
    pipeline_id: string
    source: proj-exec
    pipeline_mode: build | patch
    phase: complete

  isolation_audit:
    producer_agent_id: string         # 当前执行写代码任务的 Agent 会话 ID
    producer_role: implementer        # 若来自 Role-Adapter Layer，必须声明为 implementer
    role_contract: "skills/proj-shared/agents/roles/implementer.role.yaml"
    handoff_packet_id: string | null
    forbidden_same_as: 
      - "proj-tdd 的 agent_id"
      - "后续 proj-qa / qa-auditor 的 agent_id 或 instance_id"

  protocol_evidence:
    loaded:
      - protocol_file: "skills/proj-exec/SKILL.md"
        key_rule_extracted: "proj-exec 负责输出 Green Proof，并默认交给 proj-qa 严格盲审。"
        compliance_action: "本轮完成实现后生成 execution_definition 并交给 proj-qa。"
      - protocol_file: "skills/proj-shared/references/verifier-gate-protocol.md"
        key_rule_extracted: "proj-exec 的 verifier_handoff 是声明式字段；proj-qa 只检查证据，不补做 Gate。"
        compliance_action: "声明是否需要 Verifier Gate 证据检查。"
      - protocol_file: "skills/proj-shared/references/role-adapter-layer-protocol.md"
        key_rule_extracted: "Role-Adapter Layer 中 implementer 是执行实现的专业角色，完成后必须通过 handoff 交给独立 QA。"
        compliance_action: "若本轮由 native implementer subagent 执行，则输出 producer_role、role_contract 与 handoff_packet_id。"
    missing_evidence: []

  summary:
    files_changed: int
    files_modified: list[string]

  verification_evidence:
    diff_self_check:
      status: pass | fail
      findings: ["只修改了目标文件，未引入无关变动"]
    green_proof:
      status: pass | warn | fail
      command: "npx jest src/utils/math.test.ts"
      output_summary: "1 pass, 0 fail"

  # 【仅在打回时提供】
  unsatisfiable_report:
    attempt: 1
    reason_type: architecture_mismatch | impossible_contract | missing_dependency | ambiguous_requirement
    evidence:
      commands_run:
        - command: string
          result: string
      changed_files_attempted:
        - path: string
      observed_blocker: string
    why_not_fixable_in_exec: string
    requested_action:
      target: proj-tdd | proj-struct | human_director

  unhandled_gaps:
    - id: string
      type: architectural | dependency
      severity: block | warn | info
      description: "..."
      requires: proj-struct | proj-qa

  verifier_handoff:
    required: true | false
    trigger_reason: "L1/L2 | high-risk | reviewer-requested | not-required"
    upstream_verifier_gate_status: not_required | pass | pending | blocked
    owner_resolution_status: not_required | closed | unresolved
    qa_must_fail_closed_if_unresolved: true

  handoff:
    target: "proj-qa | proj-tdd | proj-struct"
    reason: "Standard QA | Unsatisfiable test"
```

## 6. Handoff (交接路由)

- 默认情况：交给 **`proj-qa`** 进行严格盲审。
- 即使是 L0 极小修复，**默认也必须走 `proj-qa`**。只有当总监用户显式打上“特急特办跳过QA”的标签且零报错时，才允许直接交给 `proj-docs`。
- 如果测试不可满足，交给 **`proj-tdd`** (仅限1次) 或 **`proj-struct`**。
- 若上游 Verifier Gate 未完成或 P0/P1 owner_resolution 未闭环，`proj-exec` 只允许在 `verifier_handoff` 中声明，不得自行补做 reviewer；后续由 `proj-qa` fail-closed 检查。
