---
name: archive
description: 将内容归档到 Library 知识库。无论在哪个目录下都可调用。支持智能内容识别、子目录分类、自动更新索引。
---

# Archive 知识归档

## 命令使用

`/archive <主题> [子目录] [内容标题]`

- **`<主题>`**: 必选参数，目标知识库主题（AI / Tech / Life）
- **`[子目录]`**: 可选参数，指定子目录（如：`/archive AI/工具与平台`）
- **`[内容标题]`**: 可选参数，指定要归档的内容标题

### 示例

```bash
/archive AI                           # 智能识别今日 Node 中可归档内容
/archive AI "Clawdbot 安装与配置"      # 归档指定标题内容到 AI/
/archive AI/工具与平台 "Clawdbot"       # 归档到 AI/05_工具与平台/ 子目录
```

## 执行步骤

1. **定位 Learning Journal 根目录**：无论当前在哪个项目，确保能找到 `/Users/eeo/learning-journal/`。

2. **识别 Node 文件**：读取今日或最近编辑的 Node 文件。

3. **智能内容识别**（若未指定内容标题）：
   - 扫描 Node 文件中的 `### ` 三级标题
   - 列出可归档的候选内容供用户选择：
     ```
     检测到以下可归档内容：
     1. Clawdbot/Moltbot 安装与配置
     2. Claude Code Skills 系统学习
     3. Moltbot 架构理解

     请输入编号或内容标题：
     ```

4. **确定目标路径**：
   - 基础目录：`src/02-Library/[主题]/`
   - 若指定子目录：`src/02-Library/[主题]/[子目录]/`
   - 文件名：`[序号]_[内容摘要].md`（如：`09_Clawdbot_安装配置指南.md`）
   - 目录不存在则自动创建

5. **创建 Library 文件**：
   - 添加 Front Matter（title, tags, public: false, source）
   - 添加来源链接：`> 📌 来源：[[原Node文件名]] | 日期：YYYY-MM-DD`
   - 写入提取的完整内容

6. **替换原内容为锚点**：
   - **删除**原 Node 文件中被归档的详细内容
   - **替换为**简洁的锚点链接：
     ```markdown
     ### Clawdbot/Moltbot 安装与配置
     → 已归档：[[09_Clawdbot_安装配置指南]] (AI 聊天机器人)
     ```

7. **自动更新 Library README**：
   - 在 `src/02-Library/[主题]/README.md` 的索引中添加新条目
   - 保持索引与内容同步

8. **反馈结果**：
   - 告知新文件路径
   - 显示锚点链接
   - 确认 README 已更新
