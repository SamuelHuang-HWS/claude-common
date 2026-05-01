---
name: cross-review
description: 跨模型复核入口。用于 step/task 级双评审，通过 consult 能力层调用 Codex 做只读复核；不负责方案主评审或代码 QA 主门禁。
---

# Cross Review

> 用于步骤级或任务级的双模型复核。

`cross-review` 复用 `consult` 定义的调用约定、权限约束与输出规范，专注于定义复核协议（review_packet / review_result / adoption_log）。

## 1. 适用场景

- step 级复核（实现后验证某步是否达标）；
- task 级复核（全部步骤完成后的整体验收）；
- 用户说"找 codex 审一下"等单方只读复核。

不适用：
- 多方讨论（使用 `consult`）；
- PRD / MVP / 技术方案主评审（使用 `proj-review`）；
- 实现后 build/lint/test/code review 质量门禁（使用 `proj-qa`）。

## 2. 与 consult 的关系

`cross-review` 复用 `consult` 的：
- 调用约定（`codex exec` / `claude -p`，详见 `consult/SKILL.md` §2）
- 权限约束（外部 agent 只读，single writer）
- 失败处理（不静默跳过）

`cross-review` 自行定义：
- 复核协议（review_packet → review_result → adoption_log）
- 门禁语义（PASS / FIX / BLOCKED）
- 最多 2 轮复核循环

> cross-review 不经过 consult 的 orchestration 流程，而是**同级调用方**，共享同一底层调用机制。

## 3. 完整流程

See `references/flow.md`.
