# Protocol Boot Sequence v1

> 状态：Draft v1  
> 作用：定义 native role agent 每次启动时必须执行的协议读取与证据输出步骤。

---

## 1. 适用范围

适用于 Role-Adapter Layer 下所有平台 adapter：

- Claude Code agent markdown；
- Codex agent TOML；
- Gemini extension/subagent；
- 未来其他平台自定义 agent。

---

## 2. 启动步骤

每个 role agent 接到任务后必须按顺序执行：

1. 读取本 role 的 `*.role.yaml`；
2. 读取 `role_contract.source_of_truth.primary_skill`；
3. 读取 `role_contract.source_of_truth.required_protocols`；
4. 读取本轮 `handoff_packet`；
5. 校验 `handoff_packet.to_role` 是否等于当前 role；
6. 校验权限边界：只做 role contract 与 handoff packet 允许的事；
7. 执行角色任务；
8. 输出 `role_result`，其中必须包含 `protocol_evidence` 与 handoff packet 检查结果。

---

## 3. Fail-closed 条件

任一条件命中时，role agent 必须停止并输出 `status: BLOCKED` 或 `FAIL`：

- role contract 缺失；
- primary skill 缺失；
- required protocol 缺失；
- handoff packet 缺失；
- handoff packet 指向的 `to_role` 不是当前 role；
- 当前任务要求突破 role 权限；
- `protocol_evidence.missing_evidence` 非空；
- 输出无法满足 role contract 的 `required_outputs`。

---

## 4. 标准输出片段

```yaml
protocol_evidence:
  loaded:
    - protocol_file: "skills/proj-shared/agents/roles/<role>.role.yaml"
      key_rule_extracted: "本角色权限、必读协议和必输出证据由 role contract 定义。"
      compliance_action: "按 role contract 限定执行范围。"
    - protocol_file: "skills/proj-shared/references/protocol-boot-sequence.md"
      key_rule_extracted: "role agent 必须先读取 role contract、primary skill、required protocols 和 handoff packet。"
      compliance_action: "已完成 boot sequence 后再执行角色任务。"
  missing_evidence: []
```

---

## 5. Adapter 编写规则

平台 adapter 必须把本文件的启动步骤写入原生 agent 的系统指令 / developer instructions / markdown body。

若平台无法强制某步骤，只能写入 `platform_gap`，不得删除该步骤。

本协议是声明式约束，不提供自研 runtime 级强制执行。补偿控制来自：

- `protocol_evidence.loaded[].key_rule_extracted` 必须给出具体规则摘录；
- QA / reviewer 按 `default-contract.yaml` 抽查协议文件与规则摘录；
- 缺失或空泛证据必须 fail closed。

---

## 6. 一句话规则

> Native role agent 不是靠“自觉读协议”运行；它每次启动都必须执行 Protocol Boot Sequence，并把读到的协议转化为可审计的 protocol_evidence。
