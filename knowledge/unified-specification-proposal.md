# Claude Code × Antigravity 统一规范方案

> **文档目的**: 团队头脑风暴讨论稿，整合两套工具的最佳实践
> **更新时间**: 2026-01-24
> **状态**: Draft - 待团队讨论确认

---

## 一、背景与目标

### 1.1 现状问题

| 问题 | 影响 |
|------|------|
| 两套工具目录结构不一致 | 团队成员切换工具时认知成本高 |
| 技能/工作流定义分散 | 无法共享，重复定义 |
| 存档规范不统一 | Claude Code 存全局，Antigravity 存项目 |
| 文件膨胀 | 每任务 3 文件，长期积累体积大 |
| 知识碎片化 | 过程文档与知识库割裂 |
| CHANGELOG 过长 | 单文件线性增长，难以维护 |

### 1.2 统一目标

1. **一套规范，两套工具都能用**
2. **项目级存档优先**（知识跟着代码走，可 Git 管理）
3. **单文件存档**（减少文件数量）
4. **强制知识提炼**（从过程中沉淀经验）
5. **分层索引**（CHANGELOG 保持轻量）

---

## 二、统一目录结构

### 2.1 项目级结构（核心）

```
<project>/
├── .agent/                          # Antigravity 专用
│   ├── skills/
│   │   └── <skill-name>/
│   │       └── SKILL.md
│   └── workflows/
│       └── *.md
│
├── .claude/                         # Claude Code 专用
│   ├── CLAUDE.md                    # 项目规范
│   └── skills/                      # 项目技能（或符号链接到 .agent/skills）
│
├── docs/                            # 📌 共享区域
│   ├── CHANGELOG.md                 # 轻量主索引
│   ├── changelogs/                  # 月度详情
│   │   └── YYYY-MM.md
│   ├── archive/                     # 任务存档（单文件）
│   │   └── YYYY/MM/
│   │       └── feature-name.md
│   ├── knowledge_base/              # 提炼后的知识
│   │   └── INDEX.md
│   ├── ADR/                         # 架构决策记录
│   │   └── ADR-NNN-title.md
│   └── _scaffold/                   # 模板
│       └── feature-template.md
│
└── src/
```

### 2.2 全局配置结构

```
~/.claude/
├── CLAUDE.md                        # 全局法则（精简版）
├── knowledge/                       # 全局知识库（跨项目通用）
│   └── INDEX.md
└── skills/                          # 全局技能
    ├── start.md
    ├── finish.md
    ├── fix.md
    ├── review.md
    ├── adr.md
    └── archive.md                   # 新增

~/.antigravity_tools/
├── gui_config.json                  # 模型调度配置
└── accounts.json                    # 多账户管理
```

### 2.3 目录共享策略

| 目录 | Antigravity | Claude Code | 共享方式 |
|------|-------------|-------------|----------|
| `docs/archive/` | ✅ 读写 | ✅ 读写 | 直接共享 |
| `docs/knowledge_base/` | ✅ 读写 | ✅ 读写 | 直接共享 |
| `docs/ADR/` | ✅ 读写 | ✅ 读写 | 直接共享 |
| `docs/CHANGELOG.md` | ✅ 读写 | ✅ 读写 | 直接共享 |
| `.agent/skills/` | ✅ 读写 | ✅ 只读 | Claude Code 识别 |
| `.claude/` | ❌ | ✅ 读写 | Claude Code 专用 |

---

## 三、单文件存档规范

### 3.1 问题回顾

**现状**: 每个任务创建一个目录，包含 3 个文件
```
archive/2026/01/new_profile_card/
├── spec.md      # 需求规格
├── plan.md      # 技术方案
└── task.md      # 施工清单
```

**问题**:
- 文件数量膨胀（5 个任务 = 15 个文件）
- 上下文分散，AI 需要读取多个文件
- 缺少 Learnings 区块

### 3.2 优化方案

**改为**: 单文件合并
```
archive/2026/01/new_profile_card.md
```

**文件结构**:
```markdown
---
title: 新版人物信息卡片
created: 2026-01-20
status: completed  # draft | in_progress | completed | abandoned
tags: [ui, profile, modeless]
figma: https://...
---

## 📋 Spec (需求)

### 背景
[为什么要做这个功能]

### 核心需求
[具体要实现什么]

### 验收标准
- [ ] 条件 1
- [ ] 条件 2

---

## 🏗️ Plan (方案)

### 架构变更
[需要修改哪些模块]

### 关键组件
[核心实现思路]

### 风险点
[可能的问题]

---

## ✅ Tasks (进度)

- [x] 任务 1
- [x] 任务 2
- [ ] 任务 3

---

## 💡 Learnings (知识提炼)

### 可复用的经验
[完成后必填，提炼出可复用的知识点]

### 踩坑记录
[遇到的问题和解决方案]

### 关联知识
- [相关知识条目](../knowledge_base/xxx.md)
```

### 3.3 收益

| 维度 | 改进 |
|------|------|
| 文件数量 | 减少 67% (3→1) |
| AI 上下文 | 一次读取全貌 |
| 知识沉淀 | Learnings 区块强制填写 |
| Git 历史 | 单文件变更更清晰 |

---

## 四、分层索引规范

### 4.1 问题回顾

**现状**: `CHANGELOG.md` 单文件线性增长，越来越难读

### 4.2 优化方案

**主索引** (`docs/CHANGELOG.md`):
```markdown
# Changelog

> 详细记录见各月度文件

## 2026
- [2026-01](./changelogs/2026-01.md) (12 条记录)
- [2026-02](./changelogs/2026-02.md) (进行中)

## 2025
- [2025-Q4 归档](./changelogs/2025-Q4.md)
```

**月度详情** (`docs/changelogs/2026-01.md`):
```markdown
# 2026年1月变更记录

## [2026-01-23] Profile Card 重构
- **类型**: Feature
- **摘要**: 非模态卡片 + 点击穿透
- **详情**: [查看完整记录](../archive/2026/01/new_profile_card.md)
- **知识**: [点击穿透实现](../knowledge_base/click-through.md)

## [2026-01-22] 移动端键盘崩溃修复
- **类型**: Fix
- **摘要**: WebGL resize 异常处理
- **详情**: [查看完整记录](../archive/2026/01/mobile_keyboard_crash.md)
```

### 4.3 收益

| 维度 | 改进 |
|------|------|
| 主索引 | 始终保持简洁 |
| 查找效率 | 按时间分层 |
| 历史归档 | 老记录自动"下沉" |

---

## 五、知识流转规范

### 5.1 流转路径

```
任务开始
    │
    ▼
┌─────────────────┐
│  archive/       │  ← 创建单文件存档
│  YYYY/MM/xxx.md │
└────────┬────────┘
         │
         ▼ 任务完成
┌─────────────────┐
│  填写 Learnings │  ← 强制提炼
│  区块           │
└────────┬────────┘
         │
         ▼ 有可复用价值
┌─────────────────┐
│  knowledge_base/│  ← 创建知识条目
│  xxx.md         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  更新 INDEX.md  │  ← 建立索引
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  更新 CHANGELOG │  ← 添加记录
└─────────────────┘
```

### 5.2 知识库索引

**文件**: `docs/knowledge_base/INDEX.md`

```markdown
# 知识库索引

## 按主题分类

### UI/交互
| 主题 | 描述 | 来源 | 更新时间 |
|------|------|------|----------|
| [点击穿透](./click-through.md) | 非模态弹窗点击穿透实现 | [new_profile_card](../archive/2026/01/new_profile_card.md) | 2026-01-23 |
| [1.68x 缩放](./ui-scaling.md) | Figma 812px 到代码的换算规则 | [study_buddy_ui](../archive/2026/01/study_buddy_ui.md) | 2026-01-21 |

### API/后端
| 主题 | 描述 | 来源 | 更新时间 |
|------|------|------|----------|
| [API Reference V3](./API_REFERENCE_V3.md) | 社交与组队模块接口 | 后端文档 | 2026-01-23 |

### 性能/稳定性
| 主题 | 描述 | 来源 | 更新时间 |
|------|------|------|----------|
| [WebGL Resize 修复](./webgl-resize.md) | 移动端键盘导致的崩溃处理 | [mobile_keyboard_crash](../archive/2026/01/mobile_keyboard_crash.md) | 2026-01-22 |
```

---

## 六、全局规则精简

### 6.1 设计原则

| 层级 | 放什么 | 特点 |
|------|--------|------|
| **全局** | 价值观、思维方式 | 跨项目不变，精简 |
| **项目** | 目录结构、存档规范、工具兼容 | 因项目而异 |

### 6.2 全局规则 (`~/.claude/CLAUDE.md`)

```markdown
# 🏛️ Claude Code 全局法则 (V4.0)

## 🎯 核心价值观
| 🚫 耻 | ✅ 荣 |
|-------|-------|
| 瞎猜接口 | 先查后写 |
| 模糊执行 | 确认再动 |
| 跳过验证 | 主动测试 |
| 静默失败 | 及时报告 |

## 🤝 协作分层
- **L1**: 读、搜、测试 → 直接做
- **L2**: 常规开发 → 告知后做
- **L3**: 架构/删除 → 必须确认

## 🐧 代码哲学
- 消除特例，让其成为通用逻辑
- 向后兼容是神圣规则
- 短函数，单一职责

## 🗣️ 语言
默认中文

---
**注**: 项目规范见 `<project>/.claude/CLAUDE.md`
```

### 6.3 项目规则 (`<project>/.claude/CLAUDE.md`)

```markdown
# 📁 [项目名] 开发规范

## 文档结构
```
docs/
├── CHANGELOG.md          # 轻量索引
├── changelogs/           # 月度详情
├── archive/              # 单文件存档
├── knowledge_base/       # 知识库
└── ADR/                  # 架构决策
```

## 存档规范
- 单文件包含: Spec + Plan + Tasks + Learnings
- 路径: `docs/archive/YYYY/MM/feature-name.md`
- 完成后必须填写 Learnings 区块

## 知识流转
1. 任务完成 → 填写 Learnings
2. 有复用价值 → 提炼到 knowledge_base/
3. 更新 INDEX.md 和 CHANGELOG

## Antigravity 兼容
- 共享 `docs/` 目录
- 识别 `.agent/skills/` 作为可用技能
- 识别 `.agent/workflows/` 作为工作流

## 项目特定约定
[根据项目情况填写，如 UI 缩放比例、API 规范等]
```

---

## 七、技能改造方案

### 7.1 技能对照表

| 技能 | 改动内容 |
|------|----------|
| `start.md` | 存档路径改为 `docs/archive/`，使用单文件模板 |
| `finish.md` | 添加 Learnings 填写检查、CHANGELOG 更新 |
| `fix.md` | 添加知识提炼步骤 |
| `review.md` | 添加文档完整性检查 |
| `adr.md` | 路径改为 `docs/ADR/` |
| `archive.md` | 🆕 新增：将旧目录结构合并为单文件 |

### 7.2 技能触发词统一

| 场景 | Claude Code | Antigravity | 统一建议 |
|------|-------------|-------------|----------|
| 启动任务 | `/start <task>` | 自然语言 | 保持各自方式 |
| 结束任务 | `/finish` | 自然语言 | 保持各自方式 |
| 代码审查 | `/review` | 自然语言 | 保持各自方式 |
| 调用项目技能 | 读取 `.agent/skills/` | 原生支持 | Claude Code 兼容 |

---

## 八、迁移执行计划

### Phase 1: 基础设施（立即执行）

| 序号 | 任务 | 文件 |
|------|------|------|
| 1.1 | 创建月度变更目录 | `docs/changelogs/` |
| 1.2 | 创建功能模板 | `docs/_scaffold/feature-template.md` |
| 1.3 | 创建知识库索引 | `docs/knowledge_base/INDEX.md` |
| 1.4 | 创建 Claude Code 项目配置 | `.claude/CLAUDE.md` |

### Phase 2: 规则更新

| 序号 | 任务 | 文件 |
|------|------|------|
| 2.1 | 精简全局规则 | `~/.claude/CLAUDE.md` |
| 2.2 | 更新 start 技能 | `~/.claude/skills/start.md` |
| 2.3 | 更新 finish 技能 | `~/.claude/skills/finish.md` |
| 2.4 | 更新 adr 技能 | `~/.claude/skills/adr.md` |
| 2.5 | 更新 fix 技能 | `~/.claude/skills/fix.md` |
| 2.6 | 更新 review 技能 | `~/.claude/skills/review.md` |
| 2.7 | 新增 archive 技能 | `~/.claude/skills/archive.md` |

### Phase 3: CHANGELOG 重构

| 序号 | 任务 | 文件 |
|------|------|------|
| 3.1 | 创建月度详情 | `docs/changelogs/2026-01.md` |
| 3.2 | 重构主索引 | `docs/CHANGELOG.md` |

### Phase 4: 存档迁移（可选/渐进）

| 序号 | 任务 | 说明 |
|------|------|------|
| 4.1 | 合并现有存档 | 将 5 组目录合并为 5 个单文件 |
| 4.2 | 删除旧目录 | 清理合并后的空目录 |
| 4.3 | 更新 CHANGELOG 链接 | 修正指向新文件的链接 |

---

## 九、决策点（待团队讨论）

### 9.1 存档位置

| 选项 | 优点 | 缺点 |
|------|------|------|
| **A: 项目级 `docs/`** | Git 管理、团队共享 | 每个项目都要维护 |
| B: 全局 `~/.claude/` | 集中管理 | 不随代码走、难共享 |

**建议**: 选项 A

### 9.2 旧存档是否迁移

| 选项 | 工作量 | 收益 |
|------|--------|------|
| **A: 立即全量迁移** | 高 | 统一规范 |
| B: 只迁移活跃项目 | 中 | 平衡成本 |
| C: 新任务用新规范，旧的不动 | 低 | 存在两套 |

**建议**: 选项 B

### 9.3 知识库层级

| 选项 | 结构 |
|------|------|
| **A: 项目级优先** | `<project>/docs/knowledge_base/` 为主，`~/.claude/knowledge/` 存跨项目通用 |
| B: 全局优先 | `~/.claude/knowledge/` 为主，项目只存特定知识 |

**建议**: 选项 A

---

## 十、预期收益

| 维度 | 改进前 | 改进后 |
|------|--------|--------|
| 文件数量 | 3 文件/任务 | 1 文件/任务 |
| CHANGELOG 可读性 | 线性增长 | 分层索引 |
| 知识复用 | 碎片化 | 结构化索引 |
| 工具兼容 | 各自为政 | 共享 docs/ |
| 全局规则 | 80+ 行 | 25 行 |
| 团队协作 | 切换成本高 | 统一规范 |

---

## 附录 A: 模板文件

### A.1 feature-template.md

```markdown
---
title: [功能名称]
created: YYYY-MM-DD
status: draft
tags: []
figma:
---

## 📋 Spec

### 背景

### 核心需求

### 验收标准
- [ ]

---

## 🏗️ Plan

### 架构变更

### 关键组件

### 风险点

---

## ✅ Tasks

- [ ]

---

## 💡 Learnings

### 可复用的经验

### 踩坑记录

### 关联知识
```

### A.2 ADR 模板

```markdown
# ADR-NNN: 标题

## Status
Proposed

## Context
[为什么需要这个决定]

## Decision
[最终方案]

## Consequences

### 优势

### 劣势/限制

### 风险

## References
- [相关任务](../archive/YYYY/MM/xxx.md)
```

---

*本文档由 Claude Code 自动生成，用于团队规范讨论*
*欢迎在团队会议中对"第九节：决策点"进行投票*
