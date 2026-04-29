# Harness Model v1

> 状态：v1.0
> 作用：定义 Sisyphus Harness 的完整分层架构、角色权限与协作原则。
> 定位：`ai-team-workflow-model-v1.md` 的上层补充，聚焦 Harness 工程化视角。
> 行业对标：Thin Agent / Fat Platform, Single Writer / Multiple Reviewers

---

## 1. 核心原则

### 1.1 Single Writer, Multiple Reviewers

> 唯一写入者，多审核者。

- **Antigravity** 是唯一拥有写权限的执行者（Single Writer）。
- **Codex / Claude Opus / 其他模型** 是审核者（Reviewers），默认只读。
- **用户** 是所有关键 Gate 的最终 Owner。

在 Antigravity-led Review Loop 中，Codex / Gemini / Claude Opus 默认作为 Reviewer，不直接写文件、commit 或 push。

### 1.2 Harness > Model

> 可靠性来自 Harness 工程，不来自更换更大的模型。

本体系采纳的行业实践判断：Agent 可靠性的主要提升来自更好的编排、工具设计和验证循环，而非单纯更换模型。

### 1.3 Thin Agent / Fat Platform

> Agent 保持轻量，平台承载智能。

- **Thin Agent（Antigravity）**：每轮读取最小上下文，避免上下文窗口污染。
- **Fat Platform（proj-shared）**：承载协议、契约、检查规则，按需加载（JIT）。

### 1.4 Permission 分级

参考 Anthropic 权限模型，权限按 **deny → ask → allow** 优先级处理：

| 优先级 | 类型 | 含义 |
|---|---|---|
| 最高 | deny | 禁止执行，无论其他规则 |
| 中 | ask | 需用户确认后执行 |
| 最低 | allow | 可直接执行 |

---

## 2. 分层架构

```text
┌─────────────────────────────────────┐
│         Policy Layer                │
│  AGENTS.md + Sisyphus V3.0          │
│  deny → ask → allow                │
├─────────────────────────────────────┤
│    Shared Contract Layer            │
│    proj-shared (Fat Platform)       │
│    references / contracts / checks  │
├─────────────────────────────────────┤
│       Workflow Layer (PEV)          │
│  Plan → Execute → Verify           │
├─────────────────────────────────────┤
│       Review Layer                  │
│  Ask → Action → Audit              │
├─────────────────────────────────────┤
│      Execution Layer                │
│  Antigravity (Thin Agent)           │
├─────────────────────────────────────┤
│       Evidence Layer                │
│  Gate artifacts / Traces / Evals    │
└─────────────────────────────────────┘
```

### 2.1 Policy Layer

- 用户全局规则（Sisyphus V3.0）
- 项目规则文件（AGENTS.md / CLAUDE.md）
- 权限分级（deny → ask → allow）

### 2.2 Shared Contract Layer (Fat Platform)

- `proj-shared/references/`：协议文档，按需读取
- `proj-shared/contracts/`：Skill 级 Contract（What+When+I/O+Forbidden）
- `proj-shared/checks/`：静态健康检查
- `proj-shared/evals/`：回归测试用例（后续阶段）

### 2.3 Workflow Layer (PEV Pattern)

Plan-Execute-Verify 三段式，映射到 skill 主链：

| 阶段 | Skill | 职责 |
|---|---|---|
| Plan | proj-start → proj-pm → proj-review | 理解、分流、加工、评审 |
| Execute | proj-exec → proj-dev | 实施、增强 |
| Verify | proj-qa → proj-docs → proj-close | 验证、归档、提交 |

### 2.4 Review Layer (Ask → Action → Audit)

- **Ask**：Antigravity 生成 review_packet，提交审核
- **Action**：Codex/Opus 返回 review_result
- **Audit**：Antigravity 生成 adoption_log，记录采纳/拒绝/延迟

详见 `review-loop-policy-v1.md`。

### 2.5 Execution Layer (Thin Agent)

Antigravity 作为 Single Writer：
- 每轮启动时读取最小上下文
- 按需加载 proj-shared references
- 执行后输出验证证据

### 2.6 Evidence Layer

- Gate artifacts：每个 Gate 的结构化输出
- Traces：项目运行态记录
- Eval reports：回归测试结果

---

## 3. 角色权限矩阵

| 角色 | 读文件 | 写文件 | Commit | Push | 建议补丁 | Gate 决策 |
|---|---|---|---|---|---|---|
| User / 总监 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ 最终 |
| Antigravity | ✅ | ✅ | ✅(需确认) | ✅(需确认) | ✅ | 建议 |
| Codex | ✅ | ❌ | ❌ | ❌ | ✅ | 建议 |
| Claude Opus | ✅ | ❌ | ❌ | ❌ | ✅ | 建议 |

### Codex 权限约束

```yaml
codex_role:
  mode: review_only
  can_read: true
  can_suggest_patch: true
  can_write_files: false
  can_commit: false
  can_push: false
```

---

## 4. 与现有文档的关系

| 文档 | 定位 | 本文件补充 |
|---|---|---|
| `ai-team-workflow-model-v1.md` | 角色 + 流程 + Gate | Harness 分层 + 权限矩阵 + 行业对标 |
| `architecture-gate-rules-v1.md` | 架构决策规则 | 无冲突，互补 |
| `task-decomposition-protocol-v1.md` | 拆分规则 | 无冲突，互补 |

本文件不替代上述文档，而是从 Harness 工程化视角补充分层、权限和协作原则。

---

## 5. 一句话规则

> Antigravity 是唯一 Writer，Codex 是默认 Reviewer，用户是最终 Gate Owner；可靠性来自 Harness 而非 Model，协议按需加载而非全量灌入。
