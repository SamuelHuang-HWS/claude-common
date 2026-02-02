---
name: plan
description: 创建计划文件（年/月/周/日）。当用户说"创建计划"、"制定计划"、"/plan year"、"/plan month"、"/plan week"、"/plan day"时触发。支持四种类型：year（年度计划）、month（月度计划）、week（周计划）、day（日计划）。
---

# Plan 计划创建

## 使用方式

- `/plan year` 或 "创建年度计划" → 年计划
- `/plan month` 或 "创建月度计划" → 月计划
- `/plan week` 或 "创建周计划" → 周计划
- `/plan day` 或 "创建日计划" → 日计划

## 执行步骤

1. 获取当前日期（年、月、日、周数）
2. 根据类型确定文件路径：
   - 年计划：`src/01-Journal/{{YYYY}}/{{YYYY}}-Year-Plan.md`
   - 月计划：`src/01-Journal/{{YYYY}}/{{MM}}/{{YYYY}}-{{MM}}-Month-Plan.md`
   - 周计划：`src/01-Journal/{{YYYY}}/{{MM}}/{{YYYY}}-{{MM}}-W{{WW}}-Week-Plan.md`
   - 日计划：`src/01-Journal/{{YYYY}}/{{MM}}/{{YYYY}}-{{MM}}-{{DD}}-Day-Plan.md`
3. 确保目录存在
4. 检查文件是否已存在：
   - 已存在 → 询问用户是查看还是更新
   - 不存在 → 读取对应模板创建：
     - `src/01-Journal/templates/year-plan.md`
     - `src/01-Journal/templates/month-plan.md`
     - `src/01-Journal/templates/week-plan.md`
     - `src/01-Journal/templates/day-plan.md`
5. 替换模板中的日期占位符
6. 添加到上级计划的双向链接
7. 告知用户文件路径
