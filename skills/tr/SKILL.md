---
name: tr
description: 已废弃。AutoFlow 步骤执行已迁移到 proj-exec。用户仍说"跑 /tr""继续执行"时，请使用 proj-exec。
---

# Deprecated: tr (AutoFlow Step Execution)

`/tr` 已废弃，不再维护。

请使用 `proj-exec` 执行已确认任务。

原因：
- `proj-*` 是唯一主框架；
- `.ccb` AutoFlow 状态机不再维护；
- 不再通过 tmux/ask 自动推进；
- autoloop 已删除。

迁移指引：
- 启动任务 → `proj-start`
- 执行实施 → `proj-exec`
- 质量验证 → `proj-qa`
- 跨模型复核 → `cross-review`
- 多方讨论 → `consult`
- 任务收尾 → `proj-close`
