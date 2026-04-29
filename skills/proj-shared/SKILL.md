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
- `defaults/default-contract.yaml`
  - 全局默认契约，作为项目契约缺失时的兜底配置

## 读取原则

1. 先读与当前阶段直接相关的引用文件，避免全量加载。
2. 项目契约存在时，优先使用项目契约覆盖默认契约。
3. 用户显式指令、项目规则文件优先级高于默认契约。
4. 未命中项目契约时，走默认契约 + discovery fallback，但高风险动作优先退到 `plan`。
5. 涉及 L1/L2 任务拆分、`Mission / Scope / Slice`、XMind 映射或执行期 `Reslice` 时，优先读取 `references/task-decomposition-protocol-v1.md`。
6. 涉及角色分工、主链 / 增强模式、总监审核 Gate 或完整流程编排时，优先读取 `references/ai-team-workflow-model-v1.md`。
7. 涉及技术选型、系统边界、新依赖、协议变更、状态模型、ADR 或 checkpoint 门禁时，优先读取 `references/architecture-gate-rules-v1.md`。
8. 涉及工作文档初始化或结构补建时，可按需读取 `templates/spec-template.md`、`templates/plan-template.md`、`templates/task-template.md`，但不要机械套模板。
9. 涉及最终归档单文件档案时，可按需读取 `templates/archive-task-dossier-template.md`，作为 `proj-docs` 归档收敛的目标结构参考。
10. 涉及 Harness 分层、角色权限、Single Writer / Multiple Reviewers 或权限分级时，优先读取 `references/harness-model-v1.md`。
11. 涉及 Review Loop 闭环（review_packet / review_result / adoption_log）或审核轮次控制时，优先读取 `references/review-loop-policy-v1.md`。
12. 涉及 Skill Contract 格式定义或 Contract 校验时，优先读取 `references/skill-contract-rules-v1.md`。
13. 涉及 Gate 输出格式或 Gate 分级要求时，优先读取 `references/gate-artifact-policy-v1.md`。
14. 涉及运行轨迹或审计链路时，优先读取 `references/trace-policy-v1.md`。
15. 涉及回归用例、Eval Runner 或生产失败转测试时，优先读取 `references/eval-policy-v1.md`。
