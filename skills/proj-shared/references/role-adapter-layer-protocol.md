# Role-Adapter Layer Protocol v1

> 状态：Draft v1  
> 副标题：Native Agent Adapter  
> 作用：把 Sisyphus 角色契约适配到 Claude Code / Codex / Gemini 等平台原生自定义 agent 机制。  
> 定位：共享协议层，不是 agent runtime，不替代 `proj-*` skill、Verifier Gate 或 Review Loop。

---

## 1. 核心原则

### 1.1 不自研 Agent Runtime

Sisyphus 不负责创建新的 agent 执行引擎。Sisyphus 只负责：

- 角色契约（Role Contract）；
- 交接包（Handoff Packet）；
- 证据结构（Evidence Schema）；
- 平台适配模板（Adapter Template）。

Claude Code / Codex / Gemini / Copilot 等平台负责实际 subagent 执行。

### 1.2 Role Contract 是单一语义源

角色职责、权限边界、必读协议和必输出证据必须先写入平台无关的 `*.role.yaml`。
平台 adapter 只能翻译这些契约，不得引入更宽权限、更少证据或更弱 fail-closed 行为。

### 1.3 主会话是 Orchestrator，不注册为 v1 Subagent

v1 中主会话 agent 承担调度职责：

```text
orchestrator(main session)
  -> role-specific native agent
  -> handoff_packet / evidence
  -> orchestrator validates and routes
```

不要在 v1 注册独立 `orchestrator` subagent，避免调度权递归和 handoff 归属不清。

### 1.4 Handoff Packet 是 State-bus

跨 agent 状态传递必须通过 `handoff_packet` 完成。不得要求下游 subagent 依赖主会话隐式上下文。

### 1.5 Protocol Boot Sequence 是合规入口

每个 adapter 模板都必须包含 Protocol Boot Sequence：启动后先读取角色契约、对应 `proj-*` skill、默认/项目契约和 handoff packet，并在输出中给出 `protocol_evidence`。

缺失必读协议或 `protocol_evidence.missing_evidence` 非空时，必须 fail closed。

---

## 2. v1 角色

| Role | 专业身份 | 对应主 skill | 权限定位 |
|---|---|---|---|
| `implementer` | 实施者 / Builder | `proj-exec` | 可在授权范围内写业务代码 |
| `reviewer` | 评审者 / Verifier | `proj-review` | 只读评审、输出 findings 和 owner_resolution 要求 |
| `qa-auditor` | QA 审计者 / Auditor | `proj-qa` | 只读验证，必要时运行测试，不直接修业务代码 |

v1 不拆：

- `planner`：仍由 `proj-start` / planning-with-files / 主会话承担；
- `doc-writer`：仍由 `proj-docs` 承担；
- `closer`：仍由 `proj-close` 承担；
- `verifier`：并入 `reviewer`，避免与 Verifier Gate 建立第二套角色系统。

---

## 3. 与现有协议关系

| 现有协议 | 关系 |
|---|---|
| `harness-model-v1.md` | 本协议扩展 Execution Layer：从单一 thin agent 变为主 orchestrator + platform-native role agents。 |
| `review-loop-policy-v1.md` | `reviewer` 继续复用 `review_packet -> review_result -> adoption_log`。 |
| `verifier-gate-protocol.md` | Verifier Gate 的独立核验者由 `reviewer` role 承担，不创建新格式。 |
| `gate-artifact-policy-v1.md` | 所有 role 输出必须能被 Gate artifact 消费。 |
| `default-contract.yaml` | 声明 role_adapter 默认开关、v1 角色和平台适配状态。 |

---

## 4. Adapter 成熟度

| Platform | v1 状态 | 说明 |
|---|---|---|
| Claude Code | concrete_template | v1 首个可落地 adapter，使用 Markdown + frontmatter。 |
| Codex | experimental_skeleton | 提供 TOML 映射骨架，但未承诺端到端验证。 |
| Gemini | research_note | 仅记录 extension/subagent 适配方向，待本地验证后升级。 |

---

## 5. Fail-closed 规则

以下任一情况发生时，不得宣称 role 任务完成或放行下一 Gate：

- 未读取 role contract；
- 未读取本 role 对应的 `proj-*` skill；
- 未读取 handoff packet；
- `protocol_evidence.missing_evidence` 非空；
- 角色输出缺失其 `required_outputs`；
- `reviewer` 发现 P0/P1 且 `adoption_log.owner_resolution` 未闭环；
- `qa-auditor` 无法证明其与 `implementer` 为不同 role / instance。

---

## 6. 一句话规则

> Role-Adapter Layer 让 Sisyphus 角色通过平台原生 agent 执行；Sisyphus 只定义契约、交接和证据，不自研 runtime。所有 subagent 必须先 boot 协议、再做任务、最后产证据。
