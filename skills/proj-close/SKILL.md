---
name: proj-close
description: 项目任务收尾与提交入口。用于做最终健康检查、确认暂存范围、生成 Conventional Commit 提交信息，并在用户明确确认后执行 commit；默认不自动 push。用户说“收尾一下”“准备提交”“生成 commit message”“提交这些改动”“提交并推送”时使用。
---

# Proj Close

> 项目主链的最终收尾与提交入口。位于 `proj-docs` 之后，是进入最终完成前的最后一道提交门禁。

## 1. 适用范围

在以下场景使用本 skill：
- 任务已经完成实施与必要验证；
- 需要做最终健康检查；
- 需要确认暂存范围是否正确；
- 需要生成 Conventional Commit 提交信息；
- 用户要求提交，或提交并推送。

以下场景通常不使用：
- 任务还在启动或实施阶段；
- 只想做文档归档；
- 只想跑测试 / review；
- 只想写全局知识库。

## 2. 启动前读取顺序

按以下顺序读取：
1. 用户显式指令；
2. 最近一次 `proj-exec` / `proj-qa` / `proj-docs` 输出；
3. 项目规则文件（如 `AGENTS.md`、`.claude/CLAUDE.md`）；
4. 项目契约：`<project-root>/.proj/contract.yaml`（如果存在）；
5. 默认契约：`../proj-shared/defaults/default-contract.yaml`；
6. 上游 `protocol_evidence`、`protocol_evidence_check`、`verifier_gate` / `verifier_handoff`、`adoption_log.owner_resolution` 与 `docs_evidence`；
7. 当前 git 状态（`git status`、暂存区 diff、工作区 diff）。

## 3. 本 skill 负责什么

本 skill 负责：
1. 作为主链最终收尾入口，承接 `proj-docs` 之后的提交准备；
2. 做最终健康检查；
3. 确认本次提交范围；
4. 生成或改写 Conventional Commit 提交信息；
5. 在用户明确确认后执行 `git commit`；
6. 若用户明确要求推送，再执行 `git push`。

## 4. 本 skill 不负责什么

不要在本 skill 中做以下事情：
- 不修改业务代码；
- 不代替 `proj-docs` 做文档归档；
- 不代替 `proj-qa` 做完整验证；
- 不静默提交；
- 不默认自动 push；
- 不把无关文件混进本次提交。

## 4.1 在主流程中的位置

在总流程中，`proj-close` 的位置是：

```text
proj-qa -> proj-docs -> proj-close
```

进入 `proj-close` 的前提通常是：
- 已完成必要实施；
- 已完成必要 QA；
- 文档已由 `proj-docs` 收敛到可归档/可提交状态；
- 总监已同意进入最终提交阶段。

本 skill 不替代前置 QA 与文档整理，只负责最终提交与收尾门禁。

## 5. 收尾工作流

### Step 1：做最终健康检查
至少检查：
- 当前 `git status`；
- 暂存区是否只包含预期文件；
- 修改文件中是否存在 `TODO` / `FIXME`；
- 是否存在 hardcoded secret / token；
- 是否存在残留 `console.log`（项目相关语言）；
- 是否已有足够验证证据；
- 是否已有上游协议证据与 Verifier Gate 闭环状态；
- 若经过 `proj-docs`，是否已有 `docs_evidence`；
- 若本次应经过 `proj-docs` 但尚未整理，先提醒而不是直接跳过。

发现问题时：
- 报告“现象 + 影响 + 建议动作”；
- 不要静默继续提交。

边界：
- `proj-close` 只检查证据存在性与上游放行状态；
- 不重跑测试、不重做 code review、不重新抽样协议规则、不执行 Verifier Gate；
- 若上游证据缺失或状态为 `pending/blocked/fail`，只报告并阻塞提交准备。

### Step 2：确认提交范围
优先使用：
- `git diff --cached --name-only`
- `git diff --cached`

若暂存区为空，再结合用户意图判断：
- 是提示用户先暂存；
- 还是在用户明确要求下帮助确认应暂存哪些文件。

原则：
- 默认不自动 stage；
- 若发现无关文件混入，必须显式指出；
- 混有代码改动与无关文档改动时，要提醒 scope 风险。

### Step 3：生成提交信息
提交信息遵循 Conventional Commits：
- `feat`
- `fix`
- `docs`
- `style`
- `refactor`
- `perf`
- `test`
- `build`
- `ci`
- `chore`

生成规则：
- 优先基于暂存区内容；
- 若未暂存且用户只想“先看 commit message”，可基于工作区草拟；
- scope 尽量来自主模块 / 主目录；
- 标题中文简洁，不超过 50 字符；
- 正文说明“为什么改 + 改了什么”；
- 如有单据可追加引用。

### Step 4：先给预览，再决定 commit
必须先展示：
- 健康检查结论；
- 本次提交范围；
- commit message 预览；

然后再明确：
- 若用户确认 -> 执行 `git commit`；
- 若用户未确认 -> 停在预览阶段。

### Step 5：push 门禁
只有在用户明确表达以下意图时，才允许 push：
- “提交并推送”
- “commit 后 push”
- “直接推上去”

默认规则：
- commit 后**不自动 push**；
- 若涉及 amend / rebase / 历史改写，提醒并使用 `--force-with-lease`；
- 若用户只说“提交”，默认只做本地 commit。

## 6. 标准输出

输出时优先给结论，再给依据。建议至少包含以下结构：

```yaml
health_checks:
  git_status: OK | WARN | FAIL
  todos: OK | FAIL
  secrets: OK | FAIL
  console_logs: OK | FAIL
  verification: OK | WARN | FAIL
  evidence_gate: OK | WARN | FAIL

evidence_gate:
  protocol_evidence: OK | WARN | FAIL
  verifier_gate: OK | WARN | FAIL | SKIP
  owner_resolution: OK | WARN | FAIL | SKIP
  qa_evidence: OK | WARN | FAIL
  docs_evidence: OK | WARN | FAIL | SKIP
  note: "只检查上游证据存在性与状态，不重验内容。"

staging_scope:
  staged_files:
    - ...
  unexpected_files:
    - ...
  advice: ...

commit_message:
  type: feat | fix | docs | style | refactor | perf | test | build | ci | chore
  scope: ...
  subject: ...
  body:
    - ...

commit_action:
  commit_ready: YES | NO
  push_requested: YES | NO
  push_allowed: YES | NO

next_handoff:
  - none
  - proj-exec
  - proj-docs
  - proj-qa

risks:
  - ...
```

面向用户表达时，可压缩为：
- 健康检查结论；
- 本次提交范围；
- commit 预览；
- 是否准备提交；
- 是否需要推送。

## 7. 关键策略

### 7.1 提交前必须预览
无论用户是否要求 commit，都先给：
- 提交范围预览；
- commit message 预览。

### 7.2 默认不自动 push
这是一条硬规则。
只有用户明确要求，才允许 push。

### 7.3 提交与推送分离
- “提交” ≠ “提交并推送”；
- 不要把这两个动作混成一步默认执行。

### 7.4 问题先暴露，不要硬提
如果发现：
- 暂存区为空；
- 无关文件混入；
- 高风险问题未解决；
- 验证证据不足；
应先报告，再决定是否允许提交。

## 8. 边界提醒

- 不要把 `proj-close` 做成“自动提交机器人”；
- 不要把 `proj-close` 做成第二个 `proj-qa`：不得重跑测试、重做 review、重抽样协议规则或补做 Verifier Gate；
- 不要继承旧 `git-commit-convention` 的默认 auto push 逻辑；
- 不要把 `proj-docs` 尚未完成的事情偷偷吞掉；
- 不要基于工作区草率提交无关改动；
- 用户只要求“生成提交信息”时，不要擅自 commit。
