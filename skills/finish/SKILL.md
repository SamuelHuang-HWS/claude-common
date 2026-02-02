---
name: finish
description: 任务收尾与知识归档
---

# 🧹 任务收尾

## 0. 模式识别

| 模式 | 收尾流程 |
|:-----|:---------|
| **快速** | 仅执行步骤 1 + 6 |
| **常规** | 执行步骤 1 + 4 + 6 |
| **重大** | 执行全部步骤 |

---

## 1. 验证检查 [全模式]

- [ ] 相关测试通过
- [ ] 功能符合预期
- [ ] 无遗留 TODO 或 FIXME

## 2. Learnings 填写 [重大]

在任务文档的 **💡 Learnings** 区块填写：
- 可复用的经验
- 踩坑记录
- 关联知识

## 3. 知识提炼 [重大]

如果有项目内复用价值：
1. 提炼到 `docs/knowledge_base/`
2. 更新索引

## 4. CHANGELOG 更新 [常规/重大]

在 `docs/changelogs/YYYY-MM.md` 添加：

```markdown
## [YYYY-MM-DD] {{title}}
- **类型**: Feature | Fix | Refactor
- **摘要**: 一句话描述
```

## 5. 主索引检查 [重大]

确保 `docs/CHANGELOG.md` 包含当月链接

## 6. 代码提交 [全模式]

生成 Conventional Commits 格式的提交信息：

```
<type>(<scope>): <简述>

<详细说明>

Co-Authored-By: Claude <noreply@anthropic.com>
```

> ⚠️ AI 不会自动执行 git commit，需用户确认

---

## 💡 全局知识提示

> 问自己：**"这次学到的经验，下个项目还有用吗？"**
>
> 如果是，使用 `/remember` 沉淀到全局知识库

---

**完成后**：向用户确认任务圆满完成
