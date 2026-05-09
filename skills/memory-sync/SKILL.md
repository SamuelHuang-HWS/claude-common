---
name: memory-sync
description: 共享记忆同步工具。写入/读取 knowledge-garden 决策记录。兼容 Hermes / Codex / Claude Code。
arguments:
  - name: action
    description: pull/push
    required: true
  - name: topic
    description: 主题关键词（如 auth、timezone）
    required: true
  - name: content
    description: (仅 push) 拟记录的内容摘要
    required: false
  - name: scope
    description: global/project
    default: global
  - name: project_id
    description: 项目标识
    required: false
---

# 🧠 Memory Sync: {{action}} {{topic}}

> 目标：将重要决策写入 knowledge-garden，作为跨 agent 共享的真相源。

## 💡 触发条件

- "把这个记到全局记忆" / "记住这个决策"
- "查一下之前关于 XXX 的决定"
- "记录项目决策到 XXX 项目"

## 🚀 执行流程

> **[红线]** 必须真实执行脚本。禁止伪造输出。脚本失败立即报告。

### Action: Pull

```bash
python3 ~/.gemini/antigravity/skills/memory-sync/scripts/harvest_memory.py pull "{{topic}}" --scope {{scope}}
```

输出结果后，标注来源文件路径和适用边界。

### Action: Push

1. 先向用户展示「拟写入摘要」并请求确认
2. 确认后执行：

```bash
python3 ~/.gemini/antigravity/skills/memory-sync/scripts/harvest_memory.py push "{{topic}}" "{{content}}" --scope {{scope}} --project {{project_id}}
```

3. 告知用户写入路径

### 存储规则

- 全局记忆 → `00-Meta/decisions/YYYY-MM-DD-主题.md`
- 项目记忆 → `03-Projects/<project>/docs/memory/decisions/`
- 所有文件含 YAML frontmatter (title, doc_type, scope, status, tags)