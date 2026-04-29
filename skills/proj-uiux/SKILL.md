---
name: proj-uiux
description: UI/UX 设计语义补全入口。用于在已有 PRD、spec、交互稿或 Figma 基础上补齐状态、交互和视觉约束，供开发与 QA 消费；不替代 proj-start，也不直接实施代码。
---

# proj-uiux

> 将设计输入转译为开发与验证可消费的交互语义。

## 何时使用
- 已有 PRD / spec / 交互稿 / UI 稿 / Figma
- 缺少页面状态、交互反馈、视觉强约束或组件映射说明
- 当前重点是补设计语义，而不是重新定义产品或直接写代码

若任务仍在“先定级 / 怎么起手 / 开始做”的语境，默认回到 `proj-start`。

## 先读什么
1. 当前需求输入：PRD / spec / 交互稿 / UI 稿 / Figma
2. 已有设计系统、组件库或既有页面规则
3. 与实现和验证直接相关的状态说明

## 只做这几件事
1. 提炼关键页面或组件的语义
2. 枚举必须实现和必须验证的状态
3. 说明关键交互反馈与视觉约束
4. 标出与现有组件库或设计系统的映射

## 最小工作流
1. **识别缺口**：确认缺的是状态、反馈、视觉规则还是组件映射
2. **补齐语义**：整理默认态、hover、focus、disabled、loading、empty、error、选中/切换态
3. **约束落点**：区分必须保真与可灵活处理的设计点
4. **交棒建议**：
   - 已可实施 → `proj-start` / `proj-exec`
   - 仍缺产品边界 → `proj-pm`
   - 仍缺结构梳理 → `proj-struct`

## 标准输出
```yaml
design_semantics:
  surfaces:
    - "..."
  states:
    - "..."
  interactions:
    - "..."
  visual_constraints:
    must_keep:
      - "..."
    flexible:
      - "..."
  component_mapping:
    - "..."

route:
  next_skill: proj-start | proj-exec | proj-pm | proj-struct
  reason: "..."
```

## 红线
- 不重做产品定义，这属于 `proj-pm`
- 不承担高层结构梳理，这属于 `proj-struct`
- 不直接输出最终业务代码，这属于 `proj-exec` / `proj-dev`
- 不抢 `proj-start` 的主入口职责
