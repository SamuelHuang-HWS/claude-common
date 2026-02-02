---
name: adr
description: 新增架构决策记录
---

# 🏛️ 新增架构决策记录 (ADR)

## 触发条件
满足以下任意一条即需创建 ADR：

**通用触发**:
- 引入新依赖 (DB, Middleware, 3rd-party Lib)
- 核心数据模型变更
- 关键协议变更 (API, Auth, Socket)

**前端专属触发**:
- Store 结构重构
- 全局样式/组件变更
- 路由逻辑变更
- 工程化配置变更

## 1. 文件创建
路径: `docs/ADR/ADR-NNN-标题.md`

编号规则: 查找现有最大编号 +1

## 2. 内容模板

```markdown
# ADR-NNN: 标题

## Status
Proposed | Accepted | Deprecated | Superseded by ADR-XXX

## Context
为什么需要这个决定？背景是什么？

## Decision
最终选型和方案是什么？

## Consequences

### 优势
-

### 劣势/限制
-

### 风险
-

## References
- [相关任务文档](../archive/YYYY/MM/xxx.md)
```

## 3. 关联
在当前任务文档中添加此 ADR 的链接

---
**注意**: ADR 是永久资产，不随任务归档，始终留在 `docs/ADR/`
