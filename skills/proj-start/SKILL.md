---
name: proj-start
description: 项目任务启动入口。用于先理解需求、判定 feature/bug、tracker、L0/L1/L2，识别缺口，并决定下一步是 proj-pm、proj-struct、proj-uiux、planning-with-files、proj-exec 或 proj-qa。适合“先分析一下怎么做”“先定级”“这个需求/bug 怎么起手”。
---

# Proj Start

> 先判题，再分流。

## 1. 何时使用

用于：
- 新需求、新功能、重构、迁移、治理；
- 缺陷修复；
- 带 TAPD / Jira / Issue 约束的任务；
- 用户想先定级、定范围、定第一步。

通常可跳过：
- 明确且低风险的 L0 小改，且用户已明确要求直接实施；
- 只要求测试、归档、提交；
- 已完成启动，仅需继续执行。

## 2. 启动时先读什么

按最小上下文读取：
1. 用户显式指令；
2. 项目规则文件（如 `AGENTS.md`、`.claude/CLAUDE.md`）；
3. 项目契约：`<project-root>/.proj/contract.yaml`；
4. 若项目契约不存在，则读取全局默认契约：`../proj-shared/defaults/default-contract.yaml`；
5. 读取并输出协议证据：至少包含本 skill 自身输出协议、项目/默认契约中的 `protocol_evidence` 配置，以及本轮实际应用的关键规则。

按需补读：
- 复杂度：`../proj-shared/references/complexity-rubric.md`
- 文档策略：`../proj-shared/references/doc-lifecycle.md`
- 大任务拆分：`../proj-shared/references/task-decomposition-protocol-v1.md`

## 3. 只做这几件事

1. 回述需求理解并请求确认；
2. 判定 `feature|bug`、`tracker=yes|no`、`L0|L1|L2`；
3. 识别前置缺口；
4. 给出最低交付物；
5. 决定下一步路由；
6. 若进入实施，要求用户明确放行。

不做：写代码、跑测试、归档、提交、未授权放行实施。

## 4. 最小工作流

### Step 0：沟通确认与双态输出 (Stateful Output)
在开始正式定级或实施前，必须进行回述理解。
由于大模型在执行单次问答时无法“停顿”，`proj-start` 必须且仅能通过 **双态输出协议 (Stateful Output Protocol)** 来保证交互的完整性。

**当处于“等待用户确认”或“信息不全”状态时（哪怕是 mode: pipeline 模式）：**
- 必须强制输出 `phase: clarify` 的 YAML 结构。
- 必须将 `classification` 和 `route` 设为 `null`，严禁填入 `TBD`、`未知` 等占位符。
- 在 `gaps` 字段中以结构化形式列出缺失信息。
- 在 `required_user_input` 中总结出需要用户回答的具体问题。
- 必须输出 `protocol_evidence`；若必读协议缺失，写入 `missing_evidence`，并保持 `phase: clarify`。
- 输出完 YAML 后，附加自然语言询问，等待用户输入。

**当用户已明确表示“理解无误 / 开始实施”，且所有关键信息收集完毕时：**
- 必须强制输出 `phase: complete` 的 YAML 结构。
- `protocol_evidence.missing_evidence` 必须为空；否则禁止进入 `phase: complete`。
- 正式执行后续的 Step 1 - Step 6 定级和路由逻辑。

### Step 1：判定分类
- `feature`：功能、优化、重构、治理、迁移、架构演进；
- `bug`：错误行为、回归问题、故障修复、异常表现。

同时判断 `tracker=true|false`：是否受 TAPD / Jira / Issue / 工单约束。

### Step 2：判定复杂度
按复杂度协议判定 `L0 / L1 / L2`。

遇到以下关键词，不得停留在 `L0`：
- `权限`
- `安全`
- `重构`
- `迁移`
- `新依赖`
- `核心链路`

### Step 3：识别缺口
- 产品定义缺口 -> `proj-pm`
- 结构表达缺口 -> `proj-struct`
- 设计语义缺口 -> `proj-uiux`
- 无显著缺口 -> 继续判断执行路径

### Step 4：决定执行路径
- 需求未收敛 -> `proj-pm`
- 结构仍混乱 -> `proj-struct`
- 设计语义不足 -> `proj-uiux`
- 任务明确但执行复杂 -> `planning-with-files`
- 方案 / PRD / 计划 / 验收标准需要开发前评审 -> `proj-review`
- 任务明确且可直接实施 -> 用户放行后进 `proj-exec`
- 当前诉求是实现后验证 / 代码验收 / QA -> `proj-qa`

优先路由到 `planning-with-files` 的条件：
- `L1` 或 `L2`
- 多阶段推进
- 工具调用较多或执行链较长
- 需要持续记录计划、发现、进度、错误
- 会跨多轮 / 跨会话推进

### Step 5：形成启动结论
至少明确：
- 需求目标；
- 范围与非目标；
- 当前缺口；
- 最低交付物；
- 下一步建议交给谁。

### Step 6：请求放行
若下一步是 `proj-exec`，必须显式请求用户许可。

只有当用户明确表示“可以开始实施 / 放行 / 继续开发”时，才进入实施。

## 5. 路由矩阵

- `proj-pm`：需求目标 / MVP / 成功标准不清
- `proj-struct`：模块、流程、依赖关系混乱
- `proj-uiux`：状态、交互反馈、视觉约束不清
- `planning-with-files`：任务明确但复杂，需详细计划与持续记录
- `proj-review`：当前主要诉求是方案 / PRD / 计划 / 验收标准的开发前评审
- `proj-exec`：信息足够且用户已放行
- `proj-qa`：当前主要诉求是实现后验证 / 代码验收 / QA
- `proj-checkpoint`：高风险改动前需建检查点
- `proj-adr`：涉及架构 / 协议 / 边界决策
- `proj-docs`：纯文档生命周期整理任务

## 6. 标准输出 (Sisyphus Stateful Protocol [P0])

每次调用必须且仅能输出以下两块内容（自然语言对话 + 机器解析 YAML）。严禁丢弃 YAML 或伪造不符合协议的结构。

### 情况 A：仍在收集信息，需要用户确认时 (`phase: clarify`)

```yaml
--- # sisyphus-routing-output
kind: sisyphus.routing_output
schema_version: 1
skill: proj-start
phase: clarify
mode: interactive
task_understanding:
  summary: "..."
  scope: "..."
  non_goals: "..."

classification: null

protocol_evidence:
  loaded:
    - protocol_file: "skills/proj-start/SKILL.md"
      key_rule_extracted: "phase: clarify 时 classification 和 route 必须为 null，并在 gaps/required_user_input 中列出缺失信息。"
      compliance_action: "本轮仍需用户确认或信息补齐，因此保持 phase: clarify，不做正式路由。"
  missing_evidence: []

gaps:
  - id: "gap_01"
    description: "<系统层面的具体缺失描述>"
    critical: true

required_user_input:
  - "<给用户的最终白话提示语>"

route: null
...
```

### 情况 B：信息已确认，可安全向下游转移时 (`phase: complete`)

```yaml
--- # sisyphus-routing-output
kind: sisyphus.routing_output
schema_version: 1
skill: proj-start
phase: complete
mode: pipeline
task_understanding:
  summary: "..."
  scope: "..."
  non_goals: "..."

classification:
  work_type: feature  # [feature, bug]
  tracker: true       # [true, false]
  level: L1           # [L0, L1, L2]

protocol_evidence:
  loaded:
    - protocol_file: "skills/proj-start/SKILL.md"
      key_rule_extracted: "phase: complete 仅在用户已确认理解且关键信息收集完毕后输出。"
      compliance_action: "本轮已完成定级、缺口识别和路由判断。"
    - protocol_file: "skills/proj-shared/defaults/default-contract.yaml"
      key_rule_extracted: "protocol_evidence.fail_closed_on_missing: true"
      compliance_action: "确认 missing_evidence 为空后才输出 phase: complete。"
  missing_evidence: []

gaps: []

route:
  next_skill: proj-exec  # [proj-pm, proj-struct, proj-uiux, planning-with-files, proj-review, proj-exec, proj-qa, proj-checkpoint, proj-adr, proj-docs]
  user_permission_required: true
  reason: "..."
...
```

## 7. 红线

- 不把 `tracker` 当独立主模式；它只是附加约束。
- 不把“资料齐全”直接等同于“理解无误”或“可以实施”。
- **绝对禁止在信息不全的情况下，为了走完流程而跳过 `phase: clarify` 直接输出 `phase: complete`。** 哪怕在 `mode: pipeline` 下，只要有 Critical Gap，也必须老实输出 `clarify`。
- 绝对禁止在 `phase: clarify` 下，为 classification 或 route 填充 `TBD`、`未知` 或胡乱猜测的值（必须使用 `null`）。
- 绝对禁止在 `protocol_evidence.missing_evidence` 非空时输出 `phase: complete`；缺协议证据必须 fail closed 到 `phase: clarify`。
- 不在用户未明确许可时静默放行给 `proj-exec`。
- 对复杂任务，优先分流到 `planning-with-files`，不要在 `proj-start` 主流程里展开完整执行编排。
