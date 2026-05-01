---
name: tp
description: 已废弃。AutoFlow 计划创建已迁移到 proj-start。用户仍说"跑 /tp""创建计划"时，请使用 proj-start。
---

# Deprecated: tp (AutoFlow Plan Creation)

`/tp` 已废弃，不再维护。

请使用 `proj-start` 启动任务。

原因：
- `proj-*` 是唯一主框架；
- `.ccb` AutoFlow 状态机不再维护；
- `proj-start` 已具备启动、分级、路由、计划能力。

迁移指引：
- 启动任务 → `proj-start`
- 复杂任务计划 → `proj-start` → `planning-with-files`
- 执行实施 → `proj-exec`
