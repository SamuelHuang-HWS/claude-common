# Cross Review — Flow

Dual review by Antigravity (initial assessment) and a configurable cross-review provider (Codex by default).

Protocol reference: `proj-shared/references/review-loop-policy-v1.md`

## Modes

- `mode=step`: Review single step execution (used by /tr Step 7)
- `mode=task`: Review entire task completion (used by /tr Step 9.1)

## Input

| Field | step mode | task mode |
|-------|-----------|-----------| 
| target | Step title | Task name |
| doneConditions | Step done conditions | Acceptance criteria |
| changedFiles | Files changed in step | All files changed |
| proof | Execution output | All step summaries |

## Execution Flow

### 0. Resolve Cross-Review Provider

Resolve the `reviewer` role using a two-layer lookup:

1. **CLAUDE.md Role Assignment table** (primary): Read the Role Assignment table in CLAUDE.md. The `reviewer` role maps to a provider (e.g., `codex`, `gemini`).
2. **`.autoflow/roles.json`** (override): If this file exists in the repo, and `enabled == true` and `schemaVersion == 1`, use its `reviewer` field to override.

Default: `codex`

### 1. Antigravity Initial Assessment

Evaluate against done conditions / acceptance criteria:
- What was accomplished?
- Are all conditions met?
- Any issues or risks?

Preliminary verdict: **PASS** / **FIX** / **UNCERTAIN**

### 2. Generate Review Packet

Antigravity generates a structured `review_packet` for the cross-review provider.

Template: `proj-shared/templates/review-packet-template.yaml`

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
  antigravity_assessment:
    verdict: PASS | FIX | UNCERTAIN
    reason: "<reason>"
  verification_evidence:
    - command: "<command>"
      result: "<output>"
  questions:
    - "是否同意 Antigravity 的评估？"
    - "是否发现 Antigravity 遗漏的问题？"
    - "最终建议：PASS 还是 FIX？"
```

### 3. Cross-Review (Provider)

Send the review_packet to the resolved provider.

**Invocation:**

```bash
# Background mode (default for routine review)
CCB_CALLER=manual ask codex --background "Cross-review:

<review_packet YAML content>

Instructions:
- You are a read-only Reviewer. Do NOT write files, commit, or push.
- Evaluate the changes against the acceptance criteria.
- Return a structured review_result in YAML format.
- If FIX, list specific actionable items (max 5).
- Respond ONLY with the YAML block below:

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
    - '<action>'"
```

```bash
# Retrieve result
pend codex
```

```bash
# Foreground mode (debug only)
CCB_CALLER=manual ask codex --foreground "<prompt>"
```

### 4. Parse Review Result

Expected `review_result` format from Codex:

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

If Codex response cannot be parsed as structured `review_result`:
- Extract key points manually.
- Log a WARN in the adoption_log.
- Do NOT silently skip the review.

### 5. Adoption Processing (Antigravity)

Antigravity processes each finding from the `review_result`:

1. **Classify** each finding as `accepted`, `rejected`, or `deferred`.
2. **rejected** findings MUST include a reason.
3. **Generate** `adoption_log`:

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

4. If `accepted` findings exist → execute corrections.
5. If corrections warrant re-review → generate new `review_packet` for round 2.
6. **Max 2 rounds.** If unresolved findings remain after round 2 → stop and submit to user Gate.

### 6. Final Decision

Combine Antigravity assessment + Codex review_result + adoption_log:

| Antigravity | Codex | Result |
|-------------|-------|--------|
| PASS | PASS | → PASS (continue) |
| PASS | FIX | → FIX (Antigravity decides via adoption) |
| FIX | PASS | → FIX (merge items) |
| FIX | FIX | → FIX (merge items) |
| UNCERTAIN | * | → Antigravity makes final call |
| * (round 2 unresolved) | * | → Escalate to user Gate |

## Mode-Specific Checklist

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

## Principles

1. **Single Writer**: Only Antigravity writes files; Codex is read-only.
2. **Structured I/O**: review_packet in, review_result out, adoption_log recorded.
3. **Max 2 rounds**: Prevents runaway debate; unresolved → user Gate.
4. **Traceable**: Full assessment chain captured for audit trail.
5. **Unified schema**: Same output format for both step and task modes.
