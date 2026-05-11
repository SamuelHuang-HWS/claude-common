---
name: proj-qa
description: 项目质量验证入口。用于在实现之后做验证、审查或安全检查，并给出 QA 结论。
---

# Proj QA

> 先定范围，再验证与审查。

## 1. 何时使用

用于：
- 运行 build、typecheck、lint、test 等验证；
- 对当前改动做代码审查；
- 对高风险改动做安全审查；
- 给出是否可进入下一步的 QA 结论；
- 提交前做统一检查。

通常不用于：
- 启动任务；
- 真正实施改动；
- 只整理文档；
- 只提交代码；
- PRD / MVP / 技术方案 / 验收标准的开发前评审（转交 `proj-review`）。

## 2. QA 前先读什么

按最小上下文读取：
1. 用户显式指令；
2. 最近一次实施结果（若来自 `proj-exec`，优先复用）；
3. 项目规则文件（如 `AGENTS.md`、`.claude/CLAUDE.md`）；
4. 项目契约：`<project-root>/.proj/contract.yaml`；
5. 若项目契约不存在，则读取全局默认契约：`../proj-shared/defaults/default-contract.yaml`；
6. 上游输出中的 `protocol_evidence`（若存在）；
7. 当前改动范围（`git diff` / 已修改文件 / 用户指定范围）。

若用户未给范围，默认优先聚焦当前改动，而不是全仓扫描。

## 3. 只做这几件事

1. 确定 QA 范围与级别；
2. 运行可用验证命令；
3. 做代码审查；
4. 在需要时做安全审查；
5. 输出 QA 结论与下一步建议；
6. 在黑盒验证、Playwright 场景或复杂边界流需要增强时，直接执行增强验证并收集证据。

不做：修改代码、直接修复问题、归档、提交、静默吞掉问题。

## 4. 最小工作流

### Step 1：确定 QA 范围
明确：
- 本次是 `verify`、`review`、`security`，还是组合；
- 范围是当前 diff、指定文件，还是某个模块；
- 级别是 `quick / full / pre-pr`。
- 上游是否提供 `protocol_evidence`，以及 `missing_evidence` 是否为空。

默认规则：
- 普通验证 -> `full`
- 用户明确说“快速看一下” -> `quick`
- 用户明确说“pre-pr / 提交前 / 高风险检查” -> `pre-pr`

协议证据门禁：
- 若上游属于任何 `proj-*` skill 且未提供 `protocol_evidence`，标记 `protocol_evidence_check.status: fail`。
- 若 `protocol_evidence.missing_evidence` 非空，QA 结论不得为 `PASS`，`handoff.ready_for_next_step` 不得为 `YES`。
- 对 `key_rule_extracted` 至少抽查 1 条：确认其指向的协议文件真实存在，且规则摘录不是空泛的“已阅读”。
- 若上游声明 `verifier_gate.required: true` 或 `verifier_handoff.required: true`，必须检查 `adoption_log.owner_resolution` 是否闭环；未闭环时不得 `PASS`。
- L0 快速验证可使用轻量检查，但仍必须确认 `missing_evidence` 为空。

### Step 2：执行验证
按仓库可用性和级别运行：
- build
- typecheck
- lint
- test
- 必要时额外审计（如 console.log / hardcoded secret）

执行要求：
- 输出命令；
- 输出结果摘要；
- 不允许静默失败；
- 不可执行项标记 `SKIP` 并说明原因。

### Step 3：执行代码审查
重点看：
- 改动是否与目标一致；
- 是否夹带无关改动；
- 是否有边界条件 / 错误路径问题；
- 是否破坏接口契约或既有模式。

### Step 4：执行安全审查（如需要）
在以下场景补做安全审查：
- 用户明确要求；
- 命中 `安全` / `权限` / `核心链路`；
- 涉及对外入口、鉴权、注入、敏感数据等高风险改动；
- `pre-pr` 且改动确实涉及安全面。

按风险点做针对性审查，不机械全表扫描。

### Step 5：给出 QA 结论
统一输出：
- `PASS / FAIL / PARTIAL`
- `Ready for next step: YES / NO / CONDITIONAL`
- 若失败，明确交回 `proj-exec`
- 若通过，说明下一步是 `proj-docs` 还是 `proj-close`

### Step 6：黑盒增强验证（按需）
仅当常规 build / typecheck / lint / test / code review 不足以形成可信判断时，`proj-qa` 直接执行增强验证。

触发信号：
- 需要 Playwright / 浏览器自动化验证；
- 需要真实用户视角的黑盒链路验证；
- 需要复杂交互状态流、边界条件或异常流验证；
- 需要补充截图、日志、复现步骤等高价值证据；
- 需要展开测试细图来补齐放行判断缺口。

执行约束：
- 先明确本轮增强只验证什么、不验证什么；
- 不因“还能继续测”而扩大范围；
- 发现问题只报告并交回 `proj-exec`，不直接修代码；
- 输出“现象 + 复现方式 + 期望表现 + 证据”。

## 5. 标准输出

至少输出：

```yaml
qa_scope:
  - verify
  - review
  - security

level: quick | full | pre-pr
status: PASS | FAIL | PARTIAL

protocol_evidence_check:
  status: pass | fail | warn
  checked_files:
    - "<上游 protocol_evidence.loaded[].protocol_file>"
  missing_evidence: []
  sampled_rules:
    - protocol_file: "..."
      key_rule_extracted: "..."
      check_result: pass | fail | warn
  verifier_gate_check:
    status: pass | fail | warn | not_required
    upstream_required: true | false
    owner_resolution_closed: true | false
    unresolved_findings:
      - "VG-001"
  impact: "若 fail，则本轮 QA 不得 PASS。"

qa_isolation_check:
  status: pass | fail
  qa_agent_id: string                 # 当前执行审核任务的 Agent ID
  exec_agent_id_seen: string          # 从 execution_definition 读取的执行者 ID
  same_agent: true | false            # 动态比对 qa_agent_id 与 exec_agent_id_seen；必须判定为 false 才能 pass
  role_adapter_context:
    enabled: true | false
    qa_role: qa-auditor | null
    exec_role_seen: implementer | null
    qa_instance_id: string | null
    exec_instance_id_seen: string | null
    same_role: true | false | null
    same_instance: true | false | unknown | null
    role_contract_checked: "skills/proj-shared/agents/roles/qa-auditor.role.yaml"

verification:
  build: OK | FAIL | SKIP
  types: OK | FAIL | SKIP
  lint: OK | FAIL | SKIP
  tests: OK | FAIL | SKIP

findings:
  - severity: P0 | P1 | P2 | P3
    location: "..."
    issue: "..."
    suggestion: "..."

handoff:
  ready_for_next_step: YES | NO | CONDITIONAL
  next_skill: proj-exec | proj-docs | proj-close
  reason: "..."
```

## 6. 红线

- **强制物理隔离**：执行 `proj-qa` 的 Agent 实例，**绝对不能**与刚刚执行 `proj-exec` 写代码的 Agent 是同一个。必须强行打断上下文进行“盲审”。
- 若上游来自 Role-Adapter Layer，`proj-qa` 必须额外证明 `qa_role=qa-auditor` 且 `exec_role_seen=implementer`，并尽力比对 `qa_instance_id` 与 `exec_instance_id_seen`；同 role 或同 instance 均不得 PASS。
- 协议证据缺失或 `missing_evidence` 非空时，不得给出 `PASS` 或 `ready_for_next_step: YES`。
- 不把 `proj-qa` 做成边测边修的 skill。发现问题只报告并交回 `proj-exec`，不直接修代码。
- 不因用户未指定级别就默认跑最重检查。
- 不对不存在的命令瞎跑。
- 不对无关文件做大范围审查。
- 发现高风险问题时必须显式指出，不能轻描淡写。
