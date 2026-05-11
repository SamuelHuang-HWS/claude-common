# Role-Adapter Pilot Validation v1

> 状态：Draft v1  
> 作用：定义 Role-Adapter Layer 的 dry-run 验证流程。  
> 边界：不写入 active agent 配置，不安装平台扩展，不提交代码。

---

## 1. 目标

用最小风险验证以下闭环是否可执行：

```text
orchestrator 生成 handoff_packet
-> native role adapter 按 Protocol Boot Sequence 执行
-> role 返回 role_result
-> orchestrator / QA 验收 evidence
```

本验证只证明协议、模板和证据链可用，不证明平台原生 agent 已完成生产级安装。

---

## 2. 禁止事项

pilot validation 期间禁止：

- 修改 `~/.claude/agents`；
- 修改 `~/.codex/agents`；
- 安装 Gemini extension；
- 写入或运行 generator / sync 脚本；
- commit / push；
- 清理无关工作区脏改动；
- 绕过 orchestrator 直接让 role agent 互相调度。

---

## 3. 输入

必需输入：

- `skills/proj-shared/templates/handoff-packet-template.yaml` 的一份实例化副本；
- 目标 role contract：
  - `skills/proj-shared/agents/roles/implementer.role.yaml`
  - `skills/proj-shared/agents/roles/reviewer.role.yaml`
  - `skills/proj-shared/agents/roles/qa-auditor.role.yaml`
- 对应 adapter 模板：
  - `skills/proj-shared/agent-adapters/claude-code/*.md`
  - Codex adapter 仅可作为 experimental skeleton 参考。

---

## 4. Dry-run 流程

### Step 1：Orchestrator 生成 packet

1. 复制 `handoff-packet-template.yaml`；
2. 填写 `mission_id`、`packet_id`、`to_role`、`phase`、`task_summary`；
3. 明确 `context_scope.include/exclude`；
4. checksum 可保留 placeholder，但 role result 必须写 `checksum_verified: not_available` 或说明验证结果。

### Step 2：Role agent 执行 boot sequence

Role agent 必须读取：

1. 当前 role contract；
2. 当前 role 的 primary skill；
3. role contract 中的 required protocols；
4. handoff packet。

若任一输入缺失，必须返回 `status: BLOCKED`。

### Step 3：Role agent 返回 role_result

返回内容至少包含：

```yaml
role_result:
  role_id: "implementer | reviewer | qa-auditor"
  instance_id: "<platform/session/generated id>"
  status: PASS | FAIL | PARTIAL | BLOCKED
  protocol_evidence:
    loaded: []
    missing_evidence: []
  handoff_packet_check:
    packet_id: "..."
    checksum_verified: true | false | not_available
    impact: "..."
  outputs:
    summary: "..."
    evidence: []
  next_handoff:
    to_role: orchestrator
    reason: "..."
```

### Step 4：Orchestrator / QA 验收

验收者检查：

- role contract、primary skill、required protocols 是否被 evidence 覆盖；
- `protocol_evidence.missing_evidence` 是否为空；
- role 输出是否满足 `required_outputs`；
- 是否修改了 active agent 配置；
- 是否发生越权写入、commit、push 或 subagent 自行调度。

---

## 5. PASS / FAIL 标准

### PASS

全部满足时可 PASS：

- handoff packet 字段完整；
- role agent 返回 `role_result`；
- role agent 输出自身 `protocol_evidence`；
- `missing_evidence: []`；
- 未写 active config；
- 未 commit / push；
- 未越权修改文件；
- qa-auditor 与 implementer 的 role / instance 隔离可证明或明确记录为 warn。

### FAIL

任一情况必须 FAIL：

- 缺失 handoff packet；
- role agent 未读取 role contract 或 primary skill；
- `protocol_evidence` 缺失；
- `missing_evidence` 非空但仍声称 PASS；
- 修改了 active agent 配置；
- role agent 自行 spawn 下游 role 或绕过 orchestrator；
- P0/P1 reviewer finding 未进入 `adoption_log.owner_resolution`。

### CONDITIONAL

可 CONDITIONAL：

- checksum 未计算，但明确 `checksum_verified: not_available`；
- Codex adapter 仅以 experimental skeleton 参与文档级检查；
- Gemini adapter 仅作为 research note，不参与执行。

---

## 6. 一句话规则

> Pilot validation 只验证 Role-Adapter 协议和证据链，不安装、不同步、不提交；任何 role 缺 boot evidence 都必须 fail closed。
