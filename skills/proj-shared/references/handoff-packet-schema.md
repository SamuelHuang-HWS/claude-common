# Handoff Packet Schema v1

> 状态：Draft v1  
> 作用：定义主会话与 native role agents 之间的状态交接包。

---

## 1. Envelope

```yaml
handoff_packet:
  schema_version: 1
  mission_id: "2026-05-11-role-adapter-layer"
  packet_id: "hp-001"
  created_at: "2026-05-11T12:00:00+08:00"

  from_role: "orchestrator"
  to_role: "implementer | reviewer | qa-auditor"
  expected_return_role: "orchestrator"

  phase: "plan | execute | review | qa | close"
  task_summary: "..."

  context_scope:
    mode: "contract_only | diff_plus_contract | full_project"
    include:
      - "..."
    exclude:
      - "..."

  required_protocols:
    - "skills/proj-shared/references/protocol-boot-sequence.md"

  acceptance_criteria:
    - id: "AC-001"
      description: "..."
      verification: "command | manual | review"

  input_evidence:
    - type: "protocol_evidence | review_result | execution_definition | qa_result | command"
      ref: "..."
      summary: "..."

  role_instructions:
    allowed_actions:
      - "..."
    forbidden_actions:
      - "..."
    output_requirements:
      - "protocol_evidence"
      - "role_execution_result"

  integrity:
    checksum_algorithm: "sha256"
    checksum_payload: "canonical_yaml_without_integrity.checksum"
    checksum: "..."

  return_packet:
    required: true
    expected_outputs:
      - "protocol_evidence"
      - "role_execution_result"
```

---

## 2. Required Return Fields

任何 role agent 完成后必须返回：

```yaml
role_result:
  role_id: "implementer | reviewer | qa-auditor"
  instance_id: "platform/session specific id or explicit generated id"
  status: PASS | FAIL | PARTIAL | BLOCKED

  protocol_evidence:
    loaded:
      - protocol_file: "..."
        key_rule_extracted: "..."
        compliance_action: "..."
    missing_evidence: []

  handoff_packet_check:
    packet_id: "..."
    checksum_verified: true | false | not_available
    impact: "..."

  outputs:
    summary: "..."
    evidence:
      - type: command | manual | review | diff | artifact
        detail: "..."
        result: "..."

  next_handoff:
    to_role: "orchestrator | reviewer | qa-auditor | implementer"
    reason: "..."
```

---

## 3. Checksum Rule

v1 的 checksum 是完整性提示，不是安全签名。

- 创建 packet 时，orchestrator 应对去掉 `integrity.checksum` 后的 canonical YAML 计算 sha256。
- v1 canonical YAML 约定：key 按字母序排序；不使用 anchors / aliases；不使用多行 folding；列表顺序保持语义顺序；字符串仅在 YAML 需要时加引号。
- role agent 若无法计算 checksum，必须写 `checksum_verified: not_available` 并说明原因。
- QA / reviewer 不得把 `not_available` 当成安全证明；只能作为 warn 或 fail 的依据。
- 若 orchestrator 未提供 canonical payload，`checksum_verified: not_available` 是默认安全输出；只有 canonical form 受控时才应声明 `true`。

---

## 4. Context Scope

| mode | 含义 | 默认使用场景 |
|---|---|---|
| `contract_only` | 只看 handoff + 指定协议 | reviewer / qa-auditor |
| `diff_plus_contract` | 可看指定 diff 和协议 | qa-auditor / reviewer |
| `full_project` | 可读较多项目上下文 | implementer，但仍受 scope 限制 |

---

## 5. 一句话规则

> Handoff Packet 是跨角色唯一可信状态载体；没有 packet 或 packet 证据不完整时，role agent 必须 fail closed。
