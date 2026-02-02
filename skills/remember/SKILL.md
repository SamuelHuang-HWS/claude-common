---
name: remember
description: 将经验沉淀到全局知识库
arguments:
  - name: topic
    description: 知识主题（如：webgl-resize-crash）
    required: true
---

# 💾 沉淀到全局知识库: {{topic}}

## 判断标准
> **"如果我明天开一个新项目，这个知识还有用吗？"**

| 答案 | 动作 |
|------|------|
| **是** | 继续执行，沉淀到全局 |
| **否** | 建议留在项目 `docs/knowledge_base/` |

## 1. 创建知识文件

**路径**: `~/.claude/knowledge/YYYY-MM-DD-{{topic}}.md`

**模板**:
```markdown
# {{topic}}

## 场景
[什么情况下会遇到这个问题/需要这个技巧？]

## 方案
[具体怎么解决/怎么做？]

## 代码示例
```
[如有必要，附上代码片段]
```

## 来源
- 项目: {{project}}
- 任务: [{{task}}]({{link_to_archive}})
- 日期: {{date}}
```

## 2. 更新索引

在 `~/.claude/knowledge/INDEX.md` 对应分类下添加链接：

```markdown
| [{{topic}}](./YYYY-MM-DD-{{topic}}.md) | 简短描述 | YYYY-MM-DD |
```

**常见分类**：
- 🎨 前端
- 📱 移动端
- 🗄️ 数据库
- ⚡ 缓存
- 🔧 后端/服务端
- 🔌 Git
- 🐛 调试技巧
- 🛠️ 工具/配置

**没有合适分类？** 直接在 INDEX.md 新增一个表格

## 3. 确认

- 文件已创建
- 索引已更新
- 告知用户完成

---

**注意**:
- 文件扁平存放，分类通过 INDEX.md 管理
- 一个知识可以出现在多个分类下
- 全局知识库与 Antigravity 共享（`~/.gemini/antigravity/knowledge_shared/`）
