# Role Contract Schema v1

> 状态：Draft v1  
> 作用：定义 `skills/proj-shared/agents/roles/*.role.yaml` 的最小结构。

---

## 1. 最小结构

```yaml
role_id: implementer
schema_version: 1
status: draft | active | experimental

identity:
  name: "Implementer"
  description: "负责在授权范围内实现代码并输出 Green Proof。"
  professional_frame: "Senior implementation engineer"

source_of_truth:
  primary_skill: "skills/proj-exec/SKILL.md"
  required_protocols:
    - "skills/proj-shared/defaults/default-contract.yaml"
    - "skills/proj-shared/references/role-adapter-layer-protocol.md"
    - "skills/proj-shared/references/protocol-boot-sequence.md"
    - "skills/proj-shared/references/handoff-packet-schema.md"

permissions:
  can_read: true
  can_write_files: true
  can_modify_business_code: true
  can_run_commands: true
  can_commit: false
  can_push: false
  allowed_write_scopes:
    - "handoff_packet.scope.include"
  forbidden_actions:
    - "commit"
    - "push"

isolation:
  must_differ_from_roles:
    - "qa-auditor"
  must_emit_instance_id: true
  handoff_medium: "handoff_packet_only"

handoff:
  receives_from:
    - "orchestrator"
    - "reviewer"
  outputs_to:
    - "qa-auditor"
  input_schema: "skills/proj-shared/references/handoff-packet-schema.md"
  output_schema: "skills/proj-shared/references/handoff-packet-schema.md"

required_inputs:
  - "handoff_packet"
  - "acceptance_criteria"

required_outputs:
  - "protocol_evidence"
  - "role_execution_result"
  - "handoff_packet"

evidence_contract:
  protocol_evidence_required: true
  missing_evidence_must_fail_closed: true
  command_evidence_required_when_commands_run: true
```

---

## 2. 字段语义

| 字段 | 必填 | 说明 |
|---|---:|---|
| `role_id` | 是 | 平台无关角色 ID。 |
| `schema_version` | 是 | Role Contract schema 版本。 |
| `status` | 是 | `active` 可用于生产；`experimental` 只能试用。 |
| `identity` | 是 | 专业身份与职责边界。 |
| `source_of_truth.primary_skill` | 是 | 本角色对应的主 skill。 |
| `source_of_truth.required_protocols` | 是 | Protocol Boot Sequence 必读文件。 |
| `permissions` | 是 | 角色允许/禁止动作。平台 adapter 不得放宽。 |
| `isolation` | 是 | 与其他角色/实例的隔离要求。 |
| `handoff` | 是 | 上下游关系和 packet schema。 |
| `required_inputs` | 是 | 启动 role 所需输入。 |
| `required_outputs` | 是 | 完成 role 必须输出的证据。 |
| `evidence_contract` | 是 | 证据与 fail-closed 要求。 |

---

## 3. 权限映射原则

- Role Contract 权限是上限，不是建议。
- 平台 adapter 可以比 Role Contract 更严格，不得更宽松。
- 若平台不支持某个权限字段，必须在 adapter 中写明 `platform_gap`，并用指令层约束补足。

---

## 4. 一句话规则

> `*.role.yaml` 是角色语义源；adapter 只能翻译，不得扩权，不得删减必读协议和必输出证据。
