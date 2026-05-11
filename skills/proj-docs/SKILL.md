---
name: proj-docs
description: "项目文档生命周期管理入口。用于在实施和 QA 之后整理项目内工作文档、归档文档和 changelog 入口，并给出 inspect、plan 或 apply 级别的文档收尾结论。用户说\"整理文档\"\"归档\"\"changelog 收尾\"\"文档收尾\"\"项目内文档清理\"时使用。"
---

# Proj Docs

> 先识别文档角色，再决定归档动作。

## 1. 何时使用

用于：
- 识别项目工作区文档与归档文档；
- 归档未归档文档；
- 合并重复归档；
- 修正 changelog 指向最终归档入口；
- 收尾项目内文档生命周期。

通常不用于：
- 写全局知识库；
- 回写 memory；
- 改业务代码；
- 跑测试；
- 直接提交代码。

## 2. 文档整理前先读什么

按最小上下文读取：
1. 用户显式指令；
2. 项目规则文件（如 `AGENTS.md`、`.claude/CLAUDE.md`）；
3. 项目契约：`<project-root>/.proj/contract.yaml`；
4. 若项目契约不存在，则读取全局默认契约：`../proj-shared/defaults/default-contract.yaml`；
5. 文档生命周期协议：`../proj-shared/references/doc-lifecycle.md`；
6. 相关 docs 目录结构与目标文件内容。

若没有项目契约，不阻塞，但默认更保守：优先 `inspect / plan`，不要直接 `apply`。

## 3. 只做这几件事

1. 识别项目内文档角色与状态；
2. 生成“源 -> 目标 -> 动作”的归档映射；
3. 执行归档与合并；
4. 更新 changelog / 索引到最终归档入口；
5. 输出知识候选建议，但不直接写知识层。

不做：改业务代码、跑测试、提交代码、直接写知识库、未读源文件就删改文档。

## 4. 最小工作流

### Step 1：确定模式
支持三种模式：
- `inspect`：只盘点，不改动；
- `plan`：输出归档方案，不落盘；
- `apply`：真正执行归档、合并与 changelog 更新。

默认模式：
- `plan`
- 若上下文不清或目录规则不明，则退到 `inspect`

### Step 2：识别文档角色与状态
至少识别：
- 工作区文档（如 `structured` / `issue`）；
- 归档文档；
- changelog / 索引入口；
- 项目内 knowledge 文档（仅识别，不写入）。

并判断文档状态，如：
- `active`
- `completed`
- `archived`
- `merged`

### Step 3：建立归档映射
对每个候选文档建立最小映射单元：
- 源路径；
- 角色；
- 当前状态；
- 目标路径；
- 动作（`archive / merge / keep`）；
- 是否删除源文件；
- 原因。

对于本次明确不处理的文件，也要列出 kept 清单和原因。

### Step 4：执行归档与合并
执行时遵守：
- 先读源文件，再决定是否写；
- 按角色归档，不按文件名归档；
- 重复归档只保留一个最终入口；
- 默认不自动删除源文件；
- `L2` 复杂任务的最终归档应收敛为单文件最终档案。

### Step 5：更新 changelog / 索引
确保：
- changelog 不指向工作区文档；
- changelog 只指向最终归档入口；
- 合并旧归档后，同步修正入口；
- changelog 仅记录用户可感知变化，不堆工作日志。

### Step 6：输出知识候选
若发现可复用经验，可输出：
- 候选主题；
- 建议理由；
- 建议交给 `remember` / `archive` / `memory-sync`。

但不要直接执行知识写入。

### Step 7：输出文档证据
`proj-docs` 只产出自身文档证据，不透传上游 QA / Verifier 证据。

必须输出：
- `protocol_evidence`：本轮读取的文档生命周期、默认契约和本 skill 规则；
- `docs_evidence`：归档映射、changelog 更新、kept 清单和 apply/plan/inspect 结果。

若 `docs_evidence` 缺失，`proj-close` 不得把本轮视为文档已收尾。

## 5. 标准输出

至少输出：

```yaml
mode: inspect | plan | apply

protocol_evidence:
  loaded:
    - protocol_file: "skills/proj-docs/SKILL.md"
      key_rule_extracted: "proj-docs 只整理项目文档，不改业务代码、不提交代码。"
      compliance_action: "本轮只输出或执行文档生命周期动作。"
    - protocol_file: "skills/proj-shared/references/doc-lifecycle.md"
      key_rule_extracted: "按工作区、归档区和知识区边界处理文档。"
      compliance_action: "本轮按文档角色建立归档映射。"
  missing_evidence: []

discovery:
  workspace_docs:
    - path: "..."
      role: structured | issue
      status: active | completed
  archive_docs:
    - path: "..."
      status: archived | merged
  changelog:
    - path: "..."

mappings:
  - source: "..."
    target: "..."
    action: archive | merge | keep
    delete_source: true | false
    reason: "..."

kept:
  - path: "..."
    reason: "..."

changelog_updates:
  - from: "..."
    to: "..."
    reason: "..."

knowledge_suggestions:
  - topic: "..."
    reason: "..."

docs_evidence:
  status: pass | warn | fail
  mode: inspect | plan | apply
  mappings_count: 0
  changelog_updates_count: 0
  source_delete_performed: false
  close_consumable: true
```

## 6. 红线

- 不把 `proj-docs` 做成顺手整理一切的大杂烩。
- 不因为看到工作区文档就默认清空。
- 不把项目 docs 归档和全局知识归档混为一谈。
- 没有项目契约时，优先 `inspect / plan`。
- 删除文档前必须能解释为什么删、删了什么、如何回溯。
- 不透传上游 QA / Verifier 证据；`proj-docs` 只对自身文档动作产证据。
