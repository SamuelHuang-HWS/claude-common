---
name: review
description: 兼容路由壳。旧 review 入口已软废弃：方案评审转 proj-review，代码验收转 proj-qa，双模型 step/task 复核转 cross-review。
---

# Deprecated Compatibility Router: review

`review` 旧入口已软废弃，不再承载主职责。请按意图选择新入口：

- **方案 / PRD / MVP / 技术方案 / 验收标准评审** → `proj-review`
- **实现完成后的代码验收 / 测试 / 安全检查 / 黑盒验证** → `proj-qa`
- **`/tr` step/task 的 Claude + Codex/Gemini 双模型复核** → `cross-review`

若用户只说“review 一下”且对象是文档或方案，优先使用 `proj-review`；若对象是已实现代码或 diff，优先使用 `proj-qa`；若明确是 step/task cross-review，使用 `cross-review`。
