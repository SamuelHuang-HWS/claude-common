# Antigravity 核心能力与架构梳理 (修订版)

> **文档目的**: 团队规范分享，梳理 Antigravity 的完整能力图谱
> **更新时间**: 2026-01-24
> **修订说明**: 聚焦开发规范体系，忽略代理层能力

---

## 一、系统定位

Antigravity 是 Google 推出的 **Agent-First 开发平台**，核心理念是将 IDE 演进为"任务控制中心"，让 AI 作为自主执行者完成规划、编码、验证的完整闭环。

**核心特点**：
- **Agent-First**: AI 不是辅助工具，而是自主执行者
- **三层定制体系**: Rules + Workflows + Skills
- **双层作用域**: 全局 + 工作区
- **Artifacts 验证**: 通过可交付物（任务列表、截图、录屏）而非日志验证

---

## 二、目录结构

### 2.1 全局配置 (~/.gemini/)

```
~/.gemini/
├── GEMINI.md                      # 📌 全局规则（核心）
├── settings.json                  # 设置
├── antigravity/
│   ├── global_workflows/          # 📌 全局工作流
│   │   ├── start-feature.md       # P0: 重大需求
│   │   ├── start-minor.md         # P1: 小型任务
│   │   ├── fix-bug.md             # P2: 故障修复
│   │   ├── start-research.md      # P3: 技术调研
│   │   ├── finish-task.md         # 任务收尾
│   │   ├── new-adr.md             # 架构决策
│   │   ├── git-commit.md          # Git 提交
│   │   ├── design-ui.md           # UI 设计
│   │   ├── figma-code.md          # Figma 转码
│   │   ├── product-design.md      # 产品设计
│   │   ├── image-aigc.md          # AI 生图
│   │   └── image-slice.md         # 图片切片
│   ├── global_skills/             # 📌 全局技能
│   ├── brain/                     # AI 知识/上下文
│   ├── knowledge/                 # 知识库
│   ├── conversations/             # 对话历史
│   ├── browser_recordings/        # 浏览器录制
│   ├── annotations/               # 标注
│   └── mcp_config.json            # MCP 服务器配置
└── tmp/
```

### 2.2 项目级配置 (<project>/.agent/)

```
<project>/
├── .agent/
│   ├── rules/                     # 项目专属规则
│   │   └── *.md
│   ├── skills/                    # 项目专属技能
│   │   └── <skill-name>/
│   │       └── SKILL.md
│   └── workflows/                 # 项目专属工作流
│       └── *.md
└── docs/
    ├── _scaffold/                 # 活跃任务文档
    │   └── <task-name>/
    │       ├── spec.md
    │       ├── plan.md
    │       └── task.md
    ├── archive/                   # 已完成任务归档
    │   └── YYYY/MM/<task-name>/
    ├── knowledge_base/            # 知识库
    ├── ADR/                       # 架构决策记录
    └── CHANGELOG.md               # 变更日志索引
```

---

## 三、三层定制体系

### 3.1 Rules (规则)

**定位**: 被动约束，始终生效的行为准则

**特点**:
- 始终注入到系统提示
- 按文件类型触发或全局生效
- 类似"护栏"，确保 AI 遵循规范

**存储位置**:
- 全局: `~/.gemini/GEMINI.md`
- 工作区: `<project>/.agent/rules/*.md`

**当前全局规则 (GEMINI.md V2.0) 结构**:

```
Part 0: 核心价值观 (八荣八耻)
Part 1: 握手协议与物理拦截
Part 2: 架构宪法 (九条)
Part 3: P0 级生存红线
Part 4: 集成约束
Part 5: 知识资产与分流
Part 6: 响应封锁协议
Part 7: 豁免条款
Part 8: 惩罚与熔断模式
Appendix: Linus Torvalds 哲学
```

---

### 3.2 Workflows (工作流)

**定位**: 主动触发的多步骤流程

**特点**:
- 通过斜杠命令触发 (如 `/start-feature`)
- 定义结构化的执行步骤
- 可调用其他工作流

**存储位置**:
- 全局: `~/.gemini/antigravity/global_workflows/*.md`
- 工作区: `<project>/.agent/workflows/*.md`

**当前全局工作流 (12个)**:

| 工作流 | 触发命令 | 用途 | 优先级 |
|--------|----------|------|--------|
| `start-feature.md` | `/start-feature` | 重大需求/重构 | P0 |
| `start-minor.md` | `/start-minor` | 小型任务 | P1 |
| `fix-bug.md` | `/fix-bug` | 故障修复 | P2 |
| `start-research.md` | `/start-research` | 技术调研 | P3 |
| `finish-task.md` | `/finish-task` | 任务收尾归档 | - |
| `new-adr.md` | `/new-adr` | 架构决策记录 | - |
| `git-commit.md` | `/git-commit` | Git 提交 | - |
| `design-ui.md` | `/design-ui` | UI 设计 | - |
| `figma-code.md` | `/figma-code` | Figma 转代码 | - |
| `product-design.md` | `/product-design` | 产品设计 | - |
| `image-aigc.md` | `/image-aigc` | AI 生成图片 | - |
| `image-slice.md` | `/image-slice` | 图片切片 | - |

---

### 3.3 Skills (技能)

**定位**: 按需加载的专业知识包

**特点**:
- 渐进式披露：先看名称描述，相关时才加载完整内容
- 包含指令、最佳实践、可选脚本
- 模块化、可发现、可复用

**存储位置**:
- 全局: `~/.gemini/antigravity/global_skills/<skill-name>/SKILL.md`
- 工作区: `<project>/.agent/skills/<skill-name>/SKILL.md`

**技能定义格式**:
```markdown
---
name: skill-name
description: 技能描述（供 Agent 发现）
created_at: YYYY-MM-DD
version: x.x.x
---

# 技能标题

## 触发条件
[何时应该使用此技能]

## 执行流程
[具体步骤]

## 关键规则
[必须遵守的约束]
```

**项目示例 (NBLab-Game)**:
```
.agent/skills/
└── ui-perfect-replica/
    └── SKILL.md          # Figma 一键复刻技能
```

---

## 四、核心设计模式

### 4.1 零信任准则 (Zero-Trust)

```
用户未发送 `/xxx` 指令前：
├── AI 处于"观察者"模式
├── 禁止调用任何写入工具
├── 禁止输出具体业务代码
└── 仅允许提供【任务分级建议】和【工作流命令列表】
```

### 4.2 三步走死令 (Strict Three-Step)

```
Step 1: 拦截
    └── 用户提出需求 → AI 拦截并引导发送 `/start-xxx`

Step 2: 规划
    └── 调用工作流生成 plan.md 和 task.md
    └── 展示并获取用户确认

Step 3: 实现
    └── 获取用户对 Plan 的显式确认后
    └── 方可操作业务文件
```

### 4.3 任务分级锁

| 级别 | 命令 | 要求 | 场景 |
|------|------|------|------|
| **P0** | `/start-feature` | Spec + Plan + Task + ADR | 重大需求 |
| **P1** | `/start-minor` | Plan + Task | 小型任务 |
| **P2** | `/fix-bug` | 复现用例 + 预期 + 实际 | 故障修复 |
| **P3** | `/start-research` | 调研笔记 + POC | 技术调研 |

### 4.4 中场偏移处理

```
实施中触发非预期 Bug 或样式偏移时：
├── 必须先在 task.md 登记子项
├── 报备方案
├── 申请修复
└── 严禁静默修复
```

### 4.5 图书馆模式

```
CHANGELOG.md
    └── 仅做简要索引
    └── 详情必须链接至 _scaffold/ 或 archive/

_scaffold/
    └── 活跃任务的 spec/plan/task

archive/
    └── 已完成任务的归档
```

### 4.6 惩罚与熔断

```
违规熔断 1:
    └── AI 发现自己未初始化阶段输出代码
    └── 必须主动认错
    └── 征求用户意见执行 /finish-task 清理

违规熔断 2:
    └── 发现静默修复或任务进度漏登
    └── 视为 P0 级流程违规
    └── 须主动认错并申请重整
```

---

## 五、文档存档流程

### 5.1 完整流程

```
┌─────────────────────────────────────────────────────────────┐
│                    Antigravity 任务流程                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐  │
│  │ 需求    │───▶│ /start  │───▶│ 创建    │───▶│ 用户    │  │
│  │ 输入    │    │ -xxx    │    │ scaffold│    │ 确认    │  │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘  │
│                                      │              │       │
│                               spec.md│       确认 Plan      │
│                               plan.md│              │       │
│                               task.md│              ▼       │
│                                      │        ┌─────────┐  │
│                                      │        │  实施   │  │
│                                      │        │ (TDD)   │  │
│                                      │        └────┬────┘  │
│                                      │             │       │
│                                      ▼             ▼       │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐  │
│  │ 知识库  │◀───│ archive │◀───│/finish  │◀───│  验证   │  │
│  │ 沉淀    │    │ 归档    │    │ -task   │    │ 通过    │  │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘  │
│       │                              │                      │
│       ▼                              ▼                      │
│  knowledge_base/              CHANGELOG 更新                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 文件流转

| 阶段 | 位置 | 文件 |
|------|------|------|
| 活跃 | `docs/_scaffold/<task>/` | spec.md, plan.md, task.md |
| 归档 | `docs/archive/YYYY/MM/<task>/` | 同上（移动） |
| 索引 | `docs/CHANGELOG.md` | 链接到 archive |
| 永久 | `docs/ADR/` | 架构决策记录（不归档） |

---

## 六、MCP 集成

**配置位置**: `~/.gemini/antigravity/mcp_config.json`

**当前配置**:
```json
{
  "mcpServers": {
    "figma-dev-mode-mcp-server": {
      "command": "npx",
      "args": ["mcp-remote", "http://127.0.0.1:3845/sse"]
    }
  }
}
```

**用途**: 扩展 Agent 的工具调用能力（如 Figma 设计稿读取）

---

## 七、与 Claude Code 对比

| 维度 | Antigravity | Claude Code |
|------|-------------|-------------|
| **定位** | Agent-First 开发平台 | 官方 CLI 工具 |
| **厂商** | Google | Anthropic |
| **定制体系** | Rules + Workflows + Skills（三层） | CLAUDE.md + Skills（两层） |
| **作用域** | 全局 + 工作区（双层） | 全局 + 项目（双层） |
| **触发方式** | 斜杠命令 `/xxx` | 斜杠命令 `/xxx` |
| **任务分级** | P0/P1/P2/P3 四级 | Trivial/Minor/Standard/Major 四级 |
| **零信任模式** | ✅ 有（物理拦截） | ❌ 无 |
| **熔断机制** | ✅ 有（自动认错） | ❌ 无 |
| **存档位置** | 项目内 `docs/archive/` | 全局 `~/.claude/knowledge/` |
| **活跃文档** | `docs/_scaffold/` | 无专用目录 |
| **文档结构** | spec + plan + task（三件套） | 无强制结构 |
| **CHANGELOG** | 图书馆模式（索引+链接） | 无强制规范 |
| **MCP** | ✅ 支持 | ✅ 支持 |
| **浏览器能力** | ✅ 内置 | ❌ 无 |
| **Artifacts** | ✅ 截图/录屏验证 | ❌ 无 |

---

## 八、优势总结

| 维度 | 优势 |
|------|------|
| **流程严谨** | 三步走死令 + 零信任 + 熔断机制，防止 AI 失控 |
| **任务分级** | P0-P3 四级，不同级别不同流程要求 |
| **文档规范** | spec/plan/task 三件套 + 图书馆模式 |
| **三层定制** | Rules/Workflows/Skills 职责分明 |
| **双层作用域** | 全局 + 工作区，灵活覆盖 |
| **自我纠错** | 熔断机制，AI 主动认错 |
| **知识沉淀** | archive + knowledge_base + ADR |
| **MCP 扩展** | 支持外部工具集成 |
| **验证能力** | 内置浏览器、截图、录屏 |

---

## 九、不足与改进空间

| 维度 | 不足 | 改进建议 |
|------|------|----------|
| **文件膨胀** | 每任务 3 文件 + 1 目录 | 合并为单文件 |
| **知识碎片** | archive 与 knowledge_base 割裂 | 强制 Learnings 提炼 |
| **CHANGELOG 过长** | 单文件线性增长 | 按月拆分 |
| **全局 Skills** | 当前为空 | 沉淀通用技能 |
| **规则冗长** | GEMINI.md 约 150 行 | 考虑精简或模块化 |

---

## 附录：全局规则详情 (GEMINI.md V2.0)

### Part 0: 核心价值观 (八荣八耻)

| 🚫 以此为耻 | ✅ 以此为荣 |
|------------|------------|
| 瞎猜接口 | 认真查询 |
| 模糊执行 | 寻求确认 |
| 臆想业务 | 人类确认 |
| 创造接口 | 复用现有 |
| 跳过验证 | 主动测试 |
| 破坏架构 | 遵循规范 |
| 文档堆砌 | 提炼精华 |
| 用此即弃 | 测试转正 |

### Part 2: 架构宪法 (九条)

| 条款 | 原则 | 强制要求 |
|------|------|----------|
| I | Library-First | 所有功能先抽象为可复用模块 |
| II | CLI Interface | 核心库必须暴露文本接口 |
| III | Test-First | 先写测试确认失败再写实现 |
| IV | Asset-Permanence | 测试即交付物，Bug 修复必须产出永久测试 |
| V | Minimal Surface | 暴露最小必要功能 |
| VI | Error-First | 错误路径与正常路径同等重要 |
| VII | Simplicity Gate | 最多 3 个子项目 |
| VIII | Anti-Abstraction | 宁可重复，不要错误抽象 |
| IX | Integration-First | 优先真实环境测试 |

---

*本文档基于 [Antigravity 官方文档](https://antigravity.google) 和本地配置整理*
*用于团队规范讨论*
