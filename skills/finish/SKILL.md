---
name: finish
description: 任务收尾与知识归档
---

# 🧹 任务收尾与归档

## 1. 验证检查
- [ ] 相关测试全部通过
- [ ] 功能符合验收标准
- [ ] 无遗留 TODO 或 FIXME

## 2. Learnings 填写 [强制]
在任务文档的 **💡 Learnings** 区块填写：
- 可复用的经验
- 踩坑记录
- 关联知识

## 3. 知识提炼（项目级）
如果有项目内复用价值：
1. 提炼到 `docs/knowledge_base/xxx.md`
2. 更新 `docs/knowledge_base/INDEX.md`

## 4. CHANGELOG 更新
在 `docs/changelogs/YYYY-MM.md` 添加记录：

```markdown
## [YYYY-MM-DD] {{title}}
- **类型**: Feature | Fix | Refactor
- **摘要**: 一句话描述
- **详情**: [查看完整记录](../archive/YYYY/MM/xxx.md)
```

## 5. 主索引检查
确保 `docs/CHANGELOG.md` 包含当月链接

## 6. 提交代码
生成 Conventional Commits 格式提交

---

## 💡 全局知识提示

> 问自己：**"如果我明天开一个新项目，这次学到的经验还有用吗？"**
>
> 如果是，使用 `/remember` 命令将经验沉淀到全局知识库 `~/.claude/knowledge/`

---

**完成后**: 向用户确认任务圆满完成
