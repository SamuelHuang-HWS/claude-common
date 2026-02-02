# 🎯 Skills 管理中心

> 遵循 CLAUDE.md 规范：**规范优先，效率兼顾，知识沉淀**

## 📊 评估维度

| 维度 | 说明 |
|------|------|
| 🎯 适用性 | 是否解决我的实际问题 |
| ⚡ 效率 | 是否真的提升了工作效率 |
| 🔧 维护性 | 是否需要频繁更新 |
| 💡 学习成本 | 上手难度 |

## ✅ 当前激活 Skills

### 1. frontend-design
- **来源**: anthropics/skills (官方)
- **用途**: 创建生产级前端界面，高设计质量
- **适用场景**: 构建 Web 组件、页面、应用 UI
- **评分**: ⭐⭐⭐⭐⭐
- **状态**: ✅ 激活中
- **备注**: 前端开发必备，帮助生成有设计感的界面

### 2. webapp-testing
- **来源**: anthropics/skills (官方)
- **用途**: Web 应用测试自动化
- **适用场景**: 前端/全栈测试
- **评分**: ⭐⭐⭐⭐⭐
- **状态**: ✅ 激活中
- **备注**: 全栈开发必备，保证代码质量

### 3. mcp-builder
- **来源**: anthropics/skills (官方)
- **用途**: 构建 Model Context Protocol 工具
- **适用场景**: AI 集成开发
- **评分**: ⭐⭐⭐⭐
- **状态**: ✅ 激活中
- **备注**: AI 全栈发展核心技能

### 4. skill-creator
- **来源**: anthropics/skills (官方)
- **用途**: 创建自定义 Skills
- **适用场景**: 扩展 Claude 能力
- **评分**: ⭐⭐⭐⭐
- **状态**: ✅ 激活中
- **备注**: 元能力，帮助定制化开发流程

### 5. planning-with-files
- **来源**: OthmanAdi/planning-with-files (社区)
- **用途**: Manus 风格的文件规划系统
- **适用场景**: 复杂多步骤任务、研究项目
- **评分**: ⭐⭐⭐⭐⭐
- **状态**: ✅ 激活中
- **备注**: 价值 20 亿的工作流模式，长期任务追踪神器

## 📦 技能库结构

```
~/.claude/skills/
├── _active/              # 当前激活的 skills (软链接)
│   ├── frontend-design@ → _library/anthropics/official/skills/frontend-design
│   ├── webapp-testing@ → _library/anthropics/official/skills/webapp-testing
│   ├── mcp-builder@ → _library/anthropics/official/skills/mcp-builder
│   ├── skill-creator@ → _library/anthropics/official/skills/skill-creator
│   └── planning-with-files@ → _library/community/planning-with-files/skills/planning-with-files
│
├── _library/             # Skills 仓库
│   ├── anthropics/
│   │   └── official/     # Anthropic 官方 skills
│   └── community/
│       ├── planning-with-files/
│       └── awesome-list/  # 精选列表（参考用）
│
└── SKILLS.md            # 本文件
```

## 🚀 待探索 Skills

### 来自 anthropics/skills
- [ ] pdf - PDF 处理
- [ ] docx - Word 文档处理
- [ ] xlsx - Excel 处理
- [ ] pptx - PowerPoint 处理
- [ ] canvas-design - Canvas 设计
- [ ] web-artifacts-builder - Web artifacts 构建

### 来自社区
- [ ] Agent-Skills-for-Context-Engineering (muratcankoylan)
  - 上下文工程和多 Agent 架构
- [ ] obsidian-skills (kepano)
  - Obsidian 集成
- [ ] Skill_Seekers (yusufkaraaslan)
  - 从文档/GitHub/PDF 自动生成 Skills

## 📝 使用原则

### P0 - 核心工作流
- frontend-design
- webapp-testing
- planning-with-files

### P1 - 提效工具
- mcp-builder
- skill-creator

### P2 - 探索性
- 文档处理类 (pdf/docx/xlsx)
- AI Agent 开发类

## 🎓 学习路径（前端 → 全栈 → AI）

### 阶段 1: 前端强化 (已完成)
✅ frontend-design
✅ webapp-testing

### 阶段 2: 全栈能力
- 学习后端 API 开发
- 数据库设计
- 部署流程

### 阶段 3: AI 集成
✅ mcp-builder (学习 AI 工具开发)
- 学习 LangChain/Vector DB
- RAG 架构实践

## 💡 快速命令

```bash
# 查看激活的 skills
ls -la ~/.claude/skills/_active/

# 激活新 skill
ln -s ~/.claude/skills/_library/path/to/skill ~/.claude/skills/_active/skill-name

# 停用 skill
rm ~/.claude/skills/_active/skill-name

# 更新官方 skills
cd ~/.claude/skills/_library/anthropics/official && git pull
```

## 📅 更新日志

### 2026-01-28
- ✅ 创建 Skills 管理体系
- ✅ 激活 5 个核心 Skills
- ✅ 下载官方和社区仓库
- 🎯 目标：前端 → 全栈 → AI

---

**记住**: 不贪多，用精品。每个 skill 都要有明确用途！
