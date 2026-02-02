# Claude Code 核心能力与架构梳理

> **文档目的**: 团队规范分享，梳理 Claude Code 的完整能力图谱
> **更新时间**: 2026-01-24

---

## 一、系统定位

Claude Code 是 Anthropic 官方推出的 CLI 开发助手，定位为**开发者操作系统**，而非简单的聊天接口。其核心特点是：

- **高度模块化**: 通过插件、技能、钩子实现功能扩展
- **深度项目感知**: 按项目隔离配置和会话上下文
- **规则驱动**: 通过 CLAUDE.md 定义 AI 行为准则

---

## 二、目录结构

```
~/.claude/
├── CLAUDE.md                 # 全局行为规范
├── settings.json             # 主配置（API、模型等）
├── history.jsonl             # 交互历史
├── knowledge/                # 知识库（经验沉淀）
│   └── INDEX.md
├── skills/                   # 全局技能定义
│   ├── start.md
│   ├── finish.md
│   ├── fix.md
│   ├── review.md
│   └── adr.md
├── plugins/                  # 插件系统
│   ├── marketplaces/
│   └── known_marketplaces.json
├── projects/                 # 项目隔离配置
│   └── -Users-eeo-xxx/
│       ├── sessions-index.json
│       ├── *.jsonl           # 会话记录
│       └── subagents/        # 子智能体状态
├── session-env/              # 会话环境隔离
├── shell-snapshots/          # Shell 状态快照
├── todos/                    # 任务跟踪
├── debug/                    # 调试日志
├── cache/                    # 缓存
├── statsig/                  # 功能标志
└── telemetry/                # 遥测数据
```

---

## 三、核心能力模块

### 3.1 全局规范 (CLAUDE.md)

**位置**: `~/.claude/CLAUDE.md`（全局）+ `<project>/.claude/CLAUDE.md`（项目级）

**当前内容**:
```markdown
# 核心价值观（八荣八耻）
- 瞎猜接口 vs 认真查询
- 模糊执行 vs 寻求确认
- 跳过验证 vs 主动测试
- 静默失败 vs 及时报告

# 信任协作分层
- L1: 读、搜、测试 → 直接执行
- L2: 常规开发 → 告知后执行
- L3: 架构变更 → 必须确认

# 架构哲学（Linus 风格）
- Good Taste: 消除特例
- Never Break Userspace: 向后兼容
- Simplicity: 短函数，单一职责
```

**优势**:
- 统一 AI 行为准则，减少不可预测输出
- 分层授权，平衡效率和安全

**不足**:
- 当前全局规范偏"心法"，缺少具体的文档结构规范
- 项目级规范需要手动创建

---

### 3.2 技能系统 (Skills)

**位置**: `~/.claude/skills/*.md`

**当前定义的技能**:

| 技能 | 触发命令 | 功能 |
|------|----------|------|
| `start` | `/start <task>` | 任务启动，自动分级（Trivial/Minor/Standard/Major） |
| `finish` | `/finish` | 任务收尾，知识归档，提交代码 |
| `fix` | `/fix <bug>` | 故障修复流程（诊断→复现→修复→验证） |
| `review` | `/review` | 架构师级代码审查 |
| `adr` | `/adr` | 创建架构决策记录 |

**技能定义格式**:
```markdown
---
name: skill-name
description: 技能描述
arguments:
  - name: arg1
    description: 参数说明
    required: true
---

# 技能标题

执行步骤...
```

**优势**:
- 将常见开发流程标准化
- 支持参数传递
- 可以全局或项目级定义

**不足**:
- 当前技能较少（5个）
- 缺少存档、部署等技能
- 路径配置与 Antigravity 不一致

---

### 3.3 插件系统 (Plugins)

**位置**: `~/.claude/plugins/`

**发现的插件类型**:

| 类别 | 插件示例 | 功能 |
|------|----------|------|
| **LSP 语言支持** | typescript-lsp, pyright-lsp, rust-analyzer-lsp, gopls-lsp | 代码智能感知 |
| **开发辅助** | commit-commands, feature-dev, pr-review-toolkit | Git 工作流 |
| **外部集成** | github, gitlab, slack, linear, asana | 第三方服务 |
| **云服务** | stripe, supabase, firebase | 后端服务集成 |

**优势**:
- 官方市场提供丰富插件
- 支持 LSP 协议，代码分析能力强

**不足**:
- 插件配置分散，管理成本高
- 缺少可视化管理界面

---

### 3.4 钩子系统 (Hooks)

**位置**: 分布在各插件中

**发现的钩子类型**:

| 钩子 | 触发时机 | 用途 |
|------|----------|------|
| `pretooluse` | 工具调用前 | 拦截、修改、审计 |
| `posttooluse` | 工具调用后 | 结果处理、日志 |
| `userpromptsubmit` | 用户输入提交 | 输入预处理 |
| `session-start` | 会话开始 | 初始化设置 |
| `stop-hook` | 任务停止 | 清理、归档 |

**示例插件**:
- `hookify`: 通用钩子管理
- `security-guidance/hooks`: 安全审计
- `explanatory-output-style/hooks`: 输出风格定制

**优势**:
- 可在 AI 执行过程中插入自定义逻辑
- 支持 Python 和 Shell 脚本

**不足**:
- 钩子分散在插件中，缺少统一管理
- 文档不够完善

---

### 3.5 MCP 服务器 (Model Context Protocol)

**位置**: 插件中的配置示例

**支持的传输方式**:
- `stdio`: 标准输入输出
- `http`: HTTP 服务
- `sse`: Server-Sent Events

**配置示例**:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-filesystem"]
    }
  }
}
```

**优势**:
- 标准化的工具扩展协议
- 可集成外部服务（数据库、API 等）

**不足**:
- 当前项目中 MCP 配置为空
- 需要手动配置

---

### 3.6 项目隔离 (Projects)

**位置**: `~/.claude/projects/<path-encoded>/`

**每个项目包含**:
- `sessions-index.json`: 会话索引
- `*.jsonl`: 会话对话记录
- `subagents/`: 子智能体状态

**优势**:
- 不同项目完全隔离
- 会话可持久化和恢复

---

### 3.7 任务跟踪 (Todos)

**位置**: `~/.claude/todos/`

**文件格式**: `[SessionID]-agent-[AgentID].json`

**内容结构**:
```json
{
  "tasks": [
    {
      "id": "1",
      "subject": "任务标题",
      "description": "详细描述",
      "status": "pending|in_progress|completed"
    }
  ]
}
```

**优势**:
- 内置任务管理
- 与会话关联

---

### 3.8 知识库 (Knowledge)

**位置**: `~/.claude/knowledge/`

**当前状态**: 刚初始化，仅有 `INDEX.md`

**设计用途**:
- 沉淀开发经验
- 跨会话知识复用
- 错误解决方案积累

---

## 四、工作流程

```
┌─────────────────────────────────────────────────────────────┐
│                      Claude Code 工作流                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐  │
│  │ /start  │───▶│  分析   │───▶│  规划   │───▶│  执行   │  │
│  │  任务   │    │ 复杂度  │    │ 方案    │    │ 代码    │  │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘  │
│                                                     │       │
│                                                     ▼       │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐  │
│  │ 提交    │◀───│ /review │◀───│  测试   │◀───│ 验证    │  │
│  │ 代码    │    │  审查   │    │ 通过    │    │ 结果    │  │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘  │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────┐    ┌─────────┐                                │
│  │ /finish │───▶│ 知识    │                                │
│  │  归档   │    │ 沉淀    │                                │
│  └─────────┘    └─────────┘                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 五、配置文件详解

### 5.1 settings.json

```json
{
  "env": {
    "ANTHROPIC_API_KEY": "sk-xxx",
    "ANTHROPIC_BASE_URL": "http://127.0.0.1:8045"
  },
  "model": "opus"
}
```

### 5.2 项目级配置

**位置**: `<project>/.claude/CLAUDE.md`

**用途**: 覆盖或扩展全局规范

---

## 六、优势总结

| 维度 | 优势 |
|------|------|
| **模块化** | 插件、技能、钩子分离，易于扩展 |
| **项目隔离** | 不同项目配置和会话完全独立 |
| **规则驱动** | CLAUDE.md 统一 AI 行为 |
| **生态丰富** | 官方市场提供大量插件 |
| **知识沉淀** | 内置知识库机制 |
| **任务跟踪** | 内置 Todo 系统 |

---

## 七、不足与改进空间

| 维度 | 不足 | 改进建议 |
|------|------|----------|
| **技能数量** | 仅 5 个基础技能 | 添加 archive、deploy、test 等 |
| **文档规范** | 缺少统一的存档结构 | 定义 spec/plan/task 模板 |
| **MCP 配置** | 当前为空 | 集成常用工具 |
| **路径一致性** | 与 Antigravity 路径不一致 | 统一目录结构 |
| **可视化** | 纯 CLI，无 GUI | 考虑集成 Web UI |

---

## 八、与 Antigravity 的差异

| 维度 | Claude Code | Antigravity |
|------|-------------|-------------|
| **定位** | 官方 CLI 工具 | 第三方代理层 + IDE |
| **配置位置** | `~/.claude/` | `~/.antigravity/` + `.agent/` |
| **技能定义** | `skills/*.md` | `.agent/skills/*/SKILL.md` |
| **工作流** | 无专用目录 | `.agent/workflows/*.md` |
| **存档位置** | `~/.claude/knowledge/` | `docs/archive/` |
| **模型调度** | 单一模型 | 多模型映射 |
| **插件来源** | 官方市场 | VSCode 生态 |

---
