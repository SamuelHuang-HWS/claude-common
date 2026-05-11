---
name: proj-shared
description: 项目开发共享协议与默认契约。供 proj-* skills 按需读取复杂度规则、文档生命周期、验证策略、提交策略、执行模式、状态机与默认配置，不作为直接执行入口。
---

# Proj Shared

这个 skill 不作为直接任务入口，主要提供 `proj-*` 技能族共用的引用文件。

## 目录约定

- `references/complexity-rubric.md`
  - 复杂度与最低交付协议
- `references/task-decomposition-protocol-v1.md`
  - 大任务拆分协议，定义 `Mission / Scope / Slice`、`Gap Check`、`Reslice`、XMind 融合与文档映射
- `references/ai-team-workflow-model-v1.md`
  - 总监视角的 AI 团队工作流模型，定义角色、主链、增强模式与审核 Gate
- `references/architecture-gate-rules-v1.md`
  - 架构决策与放行规则，定义架构级问题、ADR/checkpoint 触发与架构 Gate
- `references/doc-lifecycle.md`
  - 文档生命周期协议，定义工作区、归档区与知识区边界
- `references/verification-policy.md`
  - 验证与验收协议，统一 quick/full/pre-pr 门槛
- `references/commit-policy.md`
  - 提交与推送策略协议
- `references/execution-modes.md`
  - inspect / plan / apply 三态执行协议
- `references/state-machine.md`
  - 任务 / 文档状态机协议
- `references/stateful-output-protocol-v1.md`
  - Stateful Output Protocol 状态化 YAML 输出协议，定义 phase: clarify/complete 与鉴权红线
- `references/skill-mapping.md`
  - 旧 skill -> 新 skill 映射表
- `references/legacy-transition.md`
  - 旧 skill 兼容 / 退役策略
- `references/knowledge-layer-roadmap.md`
  - 知识层后续路线说明
- `references/migration-roadmap.md`
  - 新技能体系迁移路线图与验收清单
- `references/harness-model-v1.md`
  - Harness 分层架构、角色权限矩阵与 Single Writer / Multiple Reviewers 原则
- `references/review-loop-policy-v1.md`
  - Review Loop 闭环协议：review_packet → review_result → adoption_log、2 轮限制与 doom-loop 声明
- `references/verifier-gate-protocol.md`
  - Verifier Gate 增量协议：关键节点 cross-agent 核验、adoption_log.owner_resolution 与 fail-closed
- `references/role-adapter-layer-protocol.md`
  - Role-Adapter Layer 协议：把 Sisyphus 角色契约适配到平台原生自定义 agent，不自研 runtime
- `references/role-contract-schema.md`
  - Role Contract schema：定义 `agents/roles/*.role.yaml` 的角色身份、权限、隔离、handoff 与证据字段
- `references/handoff-packet-schema.md`
  - Handoff Packet schema：定义主会话 orchestrator 与 native role agents 之间的状态交接包
- `references/protocol-boot-sequence.md`
  - Protocol Boot Sequence：定义 native role agent 启动时必须读取协议并输出 protocol_evidence 的步骤
- `references/role-adapter-pilot-validation.md`
  - Role-Adapter Pilot Validation：定义不触碰 active agent 配置的 dry-run 验证流程和 PASS/FAIL 标准
- `agents/roles/`
  - 平台无关角色契约目录，v1 包含 `implementer`、`reviewer`、`qa-auditor`
- `agent-adapters/`
  - 平台 adapter 模板目录，v1 包含 Claude Code 模板、Codex experimental skeleton 与 Gemini 状态说明
- `references/skill-contract-rules-v1.md`
  - Skill Contract 格式规范：What+When+I/O+Forbidden 字段定义与校验规则
- `references/gate-artifact-policy-v1.md`
  - Gate 1-6 统一输出格式与按复杂度分级要求
- `references/trace-policy-v1.md`
  - 项目运行态 Trace JSONL 结构、存储位置与安全约束
- `references/eval-policy-v1.md`
  - Eval Case 格式、Runner 规范与回归策略
- `contracts/`
  - Skill 级 Contract 目录，含 schema + active proj-* / cross-review contract YAML
- `checks/`
  - 静态健康检查脚本目录
- `reports/`
  - Harness 自审计报告目录
- `templates/spec-template.md`
  - `spec` 最小模板，承载背景、Mission、边界与已知风险
- `templates/plan-template.md`
  - `plan` 最小模板，承载 Scope、Slice、依赖关系与 XMind 映射
- `templates/task-template.md`
  - `task` 最小模板，承载当前 Slice 执行态、Dynamic Tasks、阻塞与验证结果
- `templates/archive-task-dossier-template.md`
  - 最终归档单文件模板，L2 完整使用，L1 可按需裁剪使用
- `templates/handoff-packet-template.yaml`
  - Role-Adapter Layer 试运行 handoff packet 模板，供 orchestrator 复制后实例化
- `defaults/default-contract.yaml`
  - 全局默认契约，作为项目契约缺失时的兜底配置

## 读取原则

1. **[MANDATORY]** 先读与当前阶段直接相关的引用文件，避免全量加载。
2. **[MANDATORY]** 项目契约存在时，优先使用项目契约覆盖默认契约。
3. **[MANDATORY]** 用户显式指令、项目规则文件优先级高于默认契约。
4. **[MANDATORY]** 未命中项目契约时，走默认契约 + discovery fallback，但高风险动作优先退到 `plan`。
5. **[MANDATORY]** `proj-*` 关键输出应提供 `protocol_evidence`：列出读取的协议文件、摘录的关键规则、当前任务的执行动作，以及未满足的 `missing_evidence`。
6. **[MANDATORY]** 当必读协议缺失或 `missing_evidence` 非空时，必须 fail closed：入口类 skill 保持 `clarify`，QA/Close 类 skill 不得给出 `PASS` 或放行结论。
7. 涉及 L1/L2 任务拆分、`Mission / Scope / Slice`、XMind 映射或执行期 `Reslice` 时，优先读取 `references/task-decomposition-protocol-v1.md`。
8. 涉及角色分工、主链 / 增强模式、总监审核 Gate 或完整流程编排时，优先读取 `references/ai-team-workflow-model-v1.md`。
9. 涉及技术选型、系统边界、新依赖、协议变更、状态模型、ADR 或 checkpoint 门禁时，优先读取 `references/architecture-gate-rules-v1.md`。
10. 涉及工作文档初始化或结构补建时，可按需读取 `templates/spec-template.md`、`templates/plan-template.md`、`templates/task-template.md`，但不要机械套模板。
11. 涉及最终归档单文件档案时，可按需读取 `templates/archive-task-dossier-template.md`，作为 `proj-docs` 归档收敛的目标结构参考。
12. 涉及 Harness 分层、角色权限、Single Writer / Multiple Reviewers 或权限分级时，优先读取 `references/harness-model-v1.md`。
13. 涉及 Review Loop 闭环（review_packet / review_result / adoption_log）或审核轮次控制时，优先读取 `references/review-loop-policy-v1.md`。
14. 涉及关键节点 cross-agent 核验、Gate 3 实施放行或 `proj-exec -> proj-qa` handoff 证据检查时，优先读取 `references/verifier-gate-protocol.md`。
15. 涉及平台原生 subagent、自定义 agent、专业角色拆分、Role Contract、Handoff Packet、adapter 模板或 dry-run 试运行时，优先读取 `references/role-adapter-layer-protocol.md`、`references/role-contract-schema.md`、`references/handoff-packet-schema.md`、`references/protocol-boot-sequence.md` 与 `references/role-adapter-pilot-validation.md`。
16. 涉及 Skill Contract 格式定义或 Contract 校验时，优先读取 `references/skill-contract-rules-v1.md`。
17. 涉及 Gate 输出格式或 Gate 分级要求时，优先读取 `references/gate-artifact-policy-v1.md`。
18. 涉及运行轨迹或审计链路时，优先读取 `references/trace-policy-v1.md`。
19. 涉及回归用例、Eval Runner 或生产失败转测试时，优先读取 `references/eval-policy-v1.md`。
20. 涉及入口路由技能（如 proj-start/proj-pm）的输出结构、交互停顿或 pipeline 解析时，优先读取 `references/stateful-output-protocol-v1.md`。
