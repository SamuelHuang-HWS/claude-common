# Cross Review — Flow

用于 step/task 级只读交叉复核。
唯一外部调用方式：`codex exec`（通过 `consult` 能力层）。

## 1. Modes

- `mode=step`: Review single step execution
- `mode=task`: Review entire task completion

## 2. Input

| Field | step mode | task mode |
|-------|-----------|-----------|
| target | Step title | Task name |
| doneConditions | Step done conditions | Acceptance criteria |
| changedFiles | Files changed in step | All files changed |
| proof | Execution output | All step summaries |

## 3. Execution Flow

### 3.1 Local Initial Assessment

当前 agent 先做本地初评：

- 完成了什么；
- 是否满足 done conditions；
- 已知风险；
- 初步结论：**PASS** / **FIX** / **UNCERTAIN**。

### 3.2 Generate review_packet

```yaml
review_packet:
  mode: step | task
  target: "<step title or task name>"
  task_summary: "<what was done>"
  phase: cross-review
  changed_files:
    - "<file path>"
  acceptance_criteria:
    - "<criterion>"
  local_assessment:
    verdict: PASS | FIX | UNCERTAIN
    reason: "<reason>"
  verification_evidence:
    - command: "<command>"
      result: "<output>"
  context_declaration: "<what context was provided, what was omitted>"
  questions:
    - "是否同意本地评估？"
    - "是否发现遗漏问题？"
    - "最终建议 PASS / FIX / BLOCKED？"
```

### 3.3 Codex Read-only Review

调用方式：

```bash
codex exec "你是只读 Reviewer。不要修改文件、不要 commit/push。
请根据以下 review_packet 检查当前目录中的相关文件。

<review_packet YAML>

请只输出 review_result YAML：

review_result:
  status: PASS | FIX | BLOCKED
  confidence: 0.0-1.0
  findings:
    - priority: P0 | P1 | P2 | P3
      file: '<file>'
      issue: '<issue>'
      recommendation: '<recommendation>'
  gate_decision:
    ready_for_next_step: YES | NO | CONDITIONAL
  required_actions:
    - '<action>'" 2>&1
```

规则：
- 不指定 `-m` 模型参数；
- 不 ping、不预检；
- cwd 必须为目标项目目录；
- Codex 只读，不修改文件。

### 3.4 Parse review_result

期望返回：

```yaml
review_result:
  status: PASS | FIX | BLOCKED
  confidence: 0.0-1.0
  findings:
    - priority: P0 | P1 | P2 | P3
      file: "<file>"
      issue: "<issue>"
      recommendation: "<recommendation>"
  gate_decision:
    ready_for_next_step: YES | NO | CONDITIONAL
  required_actions:
    - "<action>"
```

如果结构化解析失败：
- 不静默跳过；
- 手动提取核心结论；
- 在 adoption_log 中记录 WARN。

### 3.5 Adoption Processing

对每个 finding 分类为 `accepted` / `rejected` / `deferred`：

```yaml
adoption_log:
  round: 1
  accepted:
    - finding: "<finding summary>"
      action: "<what will be done>"
  rejected:
    - finding: "<finding summary>"
      reason: "<why not adopted>"
  deferred:
    - finding: "<finding summary>"
      reason: "<why deferred>"
```

规则：
- `rejected` 必须说明理由；
- P0/P1 不能无理由 deferred；
- 如果 accepted findings 存在 → 执行修正。

### 3.6 Max 2 Rounds

- Round 1 发现问题 → 处理后可进入 Round 2；
- Round 2 后仍有 unresolved findings → 停止，提交用户 Gate；
- 禁止无限辩论。

### 3.7 Final Decision

合并 local_assessment + review_result + adoption_log：

| Local | Codex | Result |
|-------|-------|--------|
| PASS | PASS | → PASS |
| PASS | FIX | → FIX (via adoption) |
| FIX | PASS | → FIX (merge items) |
| FIX | FIX | → FIX (merge items) |
| UNCERTAIN | * | → 当前 agent 做最终判断 |
| * (round 2 unresolved) | * | → ESCALATE to user Gate |

## 4. Mode-Specific Checklist

### step mode
- Done conditions satisfied?
- Code changes correct?
- No regressions introduced?

### task mode
- All acceptance criteria met?
- Gaps or missing pieces?
- Code quality issues?
- Documentation complete?
- Tests passing?

## 5. Principles

1. **Single Writer**: 只有当前 agent 写文件；Codex 只读。
2. **Structured I/O**: review_packet in, review_result out, adoption_log recorded.
3. **Max 2 rounds**: 防止无限辩论；unresolved → user Gate.
4. **Traceable**: 完整评审链可审计。
5. **No tmux**: 不使用 ask / pend / cping / CCB_CALLER。
