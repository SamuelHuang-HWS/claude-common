---
name: start
description: 统一任务启动入口（自动分级）
arguments:
  - name: task
    description: 任务描述
    required: true
---

# 🚀 启动任务: {{task}}

## 0. 心智审计 [强制]
在开始前确认：
1. 是否在猜测接口？→ 先查文档/代码
2. 边界是否清晰？→ 不懂就问
3. 是否有现有实现？→ 优先复用

## 1. 环境侦查
- 分析项目结构、技术栈
- 检查 `docs/knowledge_base/` 相关经验
- 检查 `.agent/skills/` 可复用技能

## 2. 复杂度评估

| 级别 | 标准 | 行动 |
|------|------|------|
| **P0** | 架构变更、新模块 | 创建 Spec + Plan + Task，需确认 |
| **P1** | 常规功能 | 创建 Plan + Task，需确认 |
| **P2** | Bug 修复 | 创建 Plan（含复现步骤），需确认 |
| **P3** | 技术调研 | 创建调研笔记 |
| **Trivial** | ≤3 行修改 | 说明后直接执行 |

## 3. 创建任务文档
路径: `docs/archive/YYYY/MM/{{task-name}}.md`

使用 `docs/_scaffold/feature-template.md` 模板

## 4. 输出提案
- 评估级别
- 实现方案摘要
- 第一步行动

---
**提示**: 获取用户确认后方可进入实施阶段
