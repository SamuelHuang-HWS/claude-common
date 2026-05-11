---
name: proj-review
description: 开发前方案评审入口。用于审查 PRD、MVP 范围、技术方案、验收标准、风险与 Ready for Dev 状态；不负责代码验收、构建测试或发布放行。
---

# Proj Review

> 开发前先评审方案是否清楚、可落地、可验证。

`proj-review` 是开发前质量门禁，用于审查需求、PRD、MVP 计划、技术方案、任务拆分与验收标准是否已经 Ready for Dev。它与 `proj-qa` 正交：

- `proj-review`：开发前，判断方案能不能开工；
- `proj-qa`：开发后，判断代码能不能交付。

## 1. 何时使用

用于：
- PRD / 产品规格审核；
- MVP / P1 / P2 范围审查；
- 技术方案 / 实施计划评审；
- 验收标准可测试性审查；
- 风险登记与缓解方案审查；
- 判断是否可以进入 `proj-exec`。

通常不用于：
- 跑 build / typecheck / lint / test；
- 对已实现代码做最终验收；
- Playwright / 浏览器黑盒验证；
- 提交、归档、发布放行；
- 替代 `proj-adr` 做正式架构决策。

## 2. 评审前先读什么

按最小上下文读取：
1. 用户显式指令；
2. 待评审材料：PRD、spec、plan、task、ADR 草案或用户粘贴内容；
3. 项目规则文件（如 `AGENTS.md`、`.claude/CLAUDE.md`）；
4. 项目契约：`<project-root>/.proj/contract.yaml`；
5. 若项目契约不存在，则读取全局默认契约：`../proj-shared/defaults/default-contract.yaml`；
6. 当评审级别为 `pre-exec` 或任务为 L1/L2 时，读取 `../proj-shared/references/verifier-gate-protocol.md` 与 `../proj-shared/references/review-loop-policy-v1.md`。

按需补读：
- 相关源码结构，用于判断技术可行性；
- 竞品/官方文档，仅当方案依赖外部事实或用户要求调研时；
- `proj-adr`，仅当评审对象涉及已存在架构决策。

## 3. 只做这几件事

1. 明确评审对象与评审级别；
2. 按 8 个维度审查方案质量；
3. 检查验收标准是否清晰、可测、可观察；
4. 输出 findings 与 risk register；
5. 给出 Ready for Dev 结论与下一步路由。

不做：修改业务代码、跑实现后测试、直接替代产品决策、无边界扩展调研。

## 4. 评审维度

```yaml
review_dimensions:
  product_value: "是否有明确用户价值与成功目标"
  scope_control: "MVP/P1/P2 是否拆分合理，是否过度膨胀"
  user_flow: "核心用户路径、交互状态与异常反馈是否闭环"
  data_model: "数据结构、接口契约与状态模型是否支撑需求"
  technical_feasibility: "技术路径是否可落地，依赖和集成点是否清楚"
  acceptance_criteria: "验收标准是否清晰、可测试、可观察"
  risk_control: "关键风险是否暴露，并有缓解或回滚方案"
  implementation_readiness: "是否足以进入 proj-exec，仍缺什么"
```

## 5. 最小工作流

### Step 1：确定评审范围

明确：
- 本次评审对象：PRD / spec / plan / task / 技术方案 / ADR 草案；
- 评审级别：`quick / full / pre-exec`；
- 本轮只评审什么、不评审什么。

默认规则：
- 用户说“审核方案 / 评审计划 / 看看能不能做” -> `full`；
- 用户说“快速看一下” -> `quick`；
- 用户说“开工前 / 进入实现前 / Ready for Dev” -> `pre-exec`。

### Step 2：逐维度审查

对 8 个维度给出 `PASS / PARTIAL / FAIL`。优先发现会影响开工的阻塞项：
- 范围不收敛；
- 验收标准不可测；
- 关键交互或数据模型缺失；
- 技术依赖或集成点不清；
- 风险无缓解方案。

### Step 3：验收标准质量检查

每条关键 AC 应尽量满足：
- clear：描述无歧义；
- testable：可通过命令或手测验证；
- observable：有可观察结果；
- bounded：有边界与禁用规则；
- automatable：必要时可转成自动化测试。

### Step 4：风险登记

对高价值风险输出：
- risk；
- probability：low / medium / high；
- impact：low / medium / high；
- mitigation。

### Step 5：给出 Ready for Dev 结论

统一输出：
- `PASS / FAIL / PARTIAL`；
- `ready_for_dev: YES / NO / CONDITIONAL`；
- 若未就绪，明确 blockers；
- 若就绪，说明下一步进入 `proj-exec`；
- 若需要补产品、结构、UI 或架构，分别路由到 `proj-pm`、`proj-struct`、`proj-uiux`、`proj-adr`。

### Step 6：Verifier Gate（pre-exec / L1+）

当评审级别为 `pre-exec`、任务为 L1/L2，或命中安全/权限/迁移/新依赖/核心链路时：
- 必须按 `verifier-gate-protocol.md` 发起或声明 Verifier Gate；
- 复用 `review-loop-policy-v1.md` 的 `review_packet -> review_result -> adoption_log`；
- reviewer 只读，不写文件、不 commit、不 push；
- 若通过 Role-Adapter Layer 调用 native subagent，reviewer 必须使用 `skills/proj-shared/agents/roles/reviewer.role.yaml` 并执行 Protocol Boot Sequence；
- P0/P1 reviewer findings 必须写入 `adoption_log.owner_resolution` 并闭环；
- 未闭环时不得输出 `ready_for_dev: YES`。

## 6. 标准输出

至少输出：

```yaml
mode: project_review
level: quick | full | pre-exec
status: PASS | FAIL | PARTIAL

protocol_evidence:
  loaded:
    - protocol_file: "skills/proj-review/SKILL.md"
      key_rule_extracted: "pre-exec 或 L1/L2 评审时必须执行 Verifier Gate。"
      compliance_action: "本轮根据评审级别决定是否触发 Verifier Gate。"
    - protocol_file: "skills/proj-shared/references/verifier-gate-protocol.md"
      key_rule_extracted: "Verifier Gate 复用 review_packet -> review_result -> adoption_log.owner_resolution。"
      compliance_action: "P0/P1 findings 未闭环时不放行 ready_for_dev。"
    - protocol_file: "skills/proj-shared/references/role-adapter-layer-protocol.md"
      key_rule_extracted: "Role-Adapter Layer 通过 reviewer role 承担 Verifier Gate，不创建第二套 verifier 角色。"
      compliance_action: "若本轮使用 native reviewer subagent，则要求其输出 role_result 与 protocol_evidence。"
  missing_evidence: []

readiness:
  ready_for_dev: YES | NO | CONDITIONAL
  blockers:
    - "..."

review_dimensions:
  product_value: PASS | PARTIAL | FAIL
  scope_control: PASS | PARTIAL | FAIL
  user_flow: PASS | PARTIAL | FAIL
  data_model: PASS | PARTIAL | FAIL
  technical_feasibility: PASS | PARTIAL | FAIL
  acceptance_criteria: PASS | PARTIAL | FAIL
  risk_control: PASS | PARTIAL | FAIL
  implementation_readiness: PASS | PARTIAL | FAIL

findings:
  - severity: P0 | P1 | P2 | P3
    dimension: product_value | scope_control | user_flow | data_model | technical_feasibility | acceptance_criteria | risk_control | implementation_readiness
    issue: "..."
    suggestion: "..."

risk_register:
  - risk: "..."
    probability: low | medium | high
    impact: low | medium | high
    mitigation: "..."

verifier_gate:
  required: true | false
  trigger_reason: "pre-exec | L1/L2 | high-risk | user-requested | not-required"
  review_loop:
    status: not_required | pending | pass | fix | blocked
    rounds_used: 0
    reviewer: codex | claude_code | other

adoption_log:
  accepted: []
  rejected: []
  deferred: []
  owner_resolution:
    - finding_id: "VG-001"
      decision: accepted | rejected | deferred | needs_user
      action_taken: "..."
      evidence: "..."
      remaining_risk: "..."
      recheck_required: true

handoff:
  next_skill: proj-pm | proj-struct | proj-uiux | proj-adr | proj-exec | proj-docs
  reason: "..."
```

## 7. 红线

- 不把 `proj-review` 用成代码验收；实现后验证必须交给 `proj-qa`。
- 不把方案评审变成无限调研；外部调研必须服务于具体评审缺口。
- 不替用户做不可逆产品决策；高争议范围裁剪要明确标注为建议。
- 不静默放过不可测试 AC；不可测就是开发前风险。
- 不绕过 `proj-adr`；发现架构决策缺口时应转交 `proj-adr`。
- pre-exec / L1+ 的 Verifier Gate 若存在未闭环 P0/P1 finding，不得输出 `ready_for_dev: YES`。
