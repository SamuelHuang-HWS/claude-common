---
name: fix
description: 故障修复模式
arguments:
  - name: bug
    description: Bug 描述或错误日志
    required: true
---

# 🛡️ 故障修复: {{bug}}

## 1. 诊断 (Diagnose)
- 预期行为 vs 实际现象
- 寻找最小复现路径
- 检索 `docs/knowledge_base/` 类似问题

## 2. 创建修复文档
路径: `docs/archive/YYYY/MM/fix-{{bug-name}}.md`

**必须包含**:
- 预期行为 (Expected)
- 实际现象 (Actual)
- 复现步骤 (Reproduction)
- 根因分析 (Root Cause)

## 3. 复现 (Reproduce) [强制]
编写一个能复现该 Bug 的失败测试用例

## 4. 修复 (Fix)
- 实施修复直到测试通过
- 检查周边逻辑是否存在类似隐患

## 5. 中场偏移处理
修复过程中若引入新问题：
1. 在文档中登记
2. 报备方案
3. 申请修复

## 6. 验证 (Verify)
运行全量相关测试

## 7. 知识沉淀
如果是有价值的修复经验：
- 填写 Learnings 区块
- 考虑提炼到 `knowledge_base/`

---
**完成后**: 调用 `/finish` 归档
