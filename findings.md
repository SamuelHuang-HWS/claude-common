# Findings

- Existing proj-shared already has reference documents and reading principles; Phase 1 should avoid new authority layers.
- Existing default-contract has review_loop config; add protocol_evidence alongside it as declarative config.
- proj-start output schema lacks protocol evidence; add to clarify and complete forms.
- proj-qa is the right first consumer/checker of protocol evidence.

## Claude Code Review Follow-ups

- `skills/proj-start/SKILL.md` and `skills/proj-qa/SKILL.md` were already untracked before Phase 1 began, as shown in the initial git status. Phase 1 edited them in place but did not create their directories from scratch.
- `proj-shared/SKILL.md` reading-principle changes are split as follows: original rules 1-4 only gained `[MANDATORY]`; new rules 5-6 are Phase 1 behavioral additions; rule 18 adds explicit stateful-output routing guidance.
- Phase 2 optimization: make `verifier_sample_check_min` level-aware, e.g. L0=1, L1=2, L2=3.
- Phase 2 optimization: narrow the stateful-output-protocol trigger if it causes excessive loading.

## Final Review Scope Isolation

- Claude Code final review returned `FIX` only because the repository has many pre-existing out-of-scope tracked changes.
- Phase 1 in-scope files are strictly limited to:
  - `skills/proj-start/SKILL.md`
  - `skills/proj-qa/SKILL.md`
  - `skills/proj-shared/defaults/default-contract.yaml`
  - `skills/proj-shared/SKILL.md`
  - `task_plan.md`
  - `findings.md`
  - `progress.md`
- Out-of-scope dirty files, especially `skills/proj-shared/references/ai-team-workflow-model-v1.md`, must not be staged or committed as part of Phase 1.
- Required commit strategy for Phase 1: selective-stage only the in-scope files above. Do not run blanket `git add .`.

## Phase 2 Pre-review Findings

- Claude Code approved Phase 2 conditionally, requiring no parallel review format.
- `verifier-gate-protocol.md` must be an incremental policy layered on top of existing review-loop/gate/harness policies.
- `proj-exec` verifier handoff is declarative; `proj-qa` checks evidence and fails closed if required verification/owner resolution is missing.

## Phase 2 Final Review Follow-ups

- Claude Code final review accepted Phase 2 design as complete, with commit-boundary caution.
- Added `required_protocols: []` under `protocol_evidence.phase_requirements.proj_qa` to make the evidence-check-only role explicit.
- Clarified `recheck_required`: default true; false only when deferred and user explicitly accepts remaining risk.

## Phase 3 Plan Review Findings

- Claude Code approved Phase 3 conditionally with one P0 boundary: `proj-close` must only check evidence existence and status, not redo QA.
- `proj-docs` should output its own `protocol_evidence` and `docs_evidence`, but must not proxy/relay upstream QA evidence.
- `verifier_sample_check_min` should remain as a fallback scalar and gain `verifier_sample_check_min_by_level` for L0/L1/L2.
- `verifier-gate-protocol.md` needs a coverage statement update because Phase 3 adds close/docs evidence checks without expanding gate execution.

## Phase 3 Implementation Notes

- `proj-close` now explicitly checks only evidence existence and upstream status; it must not rerun tests, redo review, resample protocol rules, or execute Verifier Gate.
- `proj-docs` now produces its own `protocol_evidence` and `docs_evidence`; it does not proxy upstream QA/Verifier evidence.
- `verifier_sample_check_min` remains as fallback scalar and `verifier_sample_check_min_by_level` provides L0/L1/L2 overrides.
- Phase 3 intentionally did not modify `proj-qa`; later work should update proj-qa wording to prefer level-aware sampling.

## Phase 4 Consultation Findings

- Gemini and Claude Code agreed not to build a custom runtime; Sisyphus should own role contracts, handoff packets, evidence schemas, and platform adapter templates.
- Naming converged to `Role-Adapter Layer`; `Native Agent Adapter` remains a subtitle/alias for discoverability.
- v1 should focus on three independent professional roles: implementer, reviewer, qa-auditor. The main session remains orchestrator to avoid orchestration recursion.
- Handoff Packet is the shared state-bus. It must include enough context for isolated subagents but remain bounded to avoid context drift.
- Protocol Boot Sequence is the enforcement point for shared-protocol reading. It must require concrete protocol_evidence and fail closed if evidence is missing.
- Claude Code adapter should be concrete in v1; Codex should start as experimental skeleton; Gemini should remain documented until its extension/subagent mechanism is validated locally.
- Generator/sync automation is deferred until role contracts and templates stabilize.

## Phase 4 Review Findings

- Gemini review returned PASS and found no blocking P0/P1 issues.
- Claude Code review returned FIX with two P1 items:
  - Codex qa-auditor skeleton used `read-only` while QA role requires command execution; resolved by adding explicit `platform_gap` and keeping Codex skeleton non-production.
  - Role contract required_protocols and Claude Code adapter boot sequence were inconsistent; resolved by removing design-time `role-contract-schema.md` from role boot requirements and keeping adapter boot lists aligned. Reviewer retained operational gate protocol coverage.
- Addressed additional P2 improvements:
  - Added `spawn_subagent` / `bypass_orchestrator_routing` forbidden actions to v1 roles and adapter instructions.
  - Clarified v1 checksum canonicalization and `not_available` default.
  - Added Role-Adapter Layer protocol evidence to proj-exec example.

## Phase 4 Targeted Recheck

- Claude Code targeted recheck confirmed both P1 findings are resolved.
- Remaining note is P2 future maintenance: Codex qa-auditor skeleton still uses `sandbox_mode = "read-only"`, but this is acceptable because `platform_gap` and `experimental` explicitly mark it non-production.

## Phase 4 Codex Self-review Follow-ups

- Codex review found two actionable P1 issues after targeted recheck:
  - Reviewer adapters did not list `gate-artifact-policy-v1.md` even though reviewer role contract requires it.
  - QA auditor role required upstream `protocol_evidence_check` but did not require its own `protocol_evidence` output.
- Fixed both by updating Claude Code/Codex reviewer boot sequences and QA auditor role/adapter outputs.

## Phase 4 Post-fix Lightweight Review

- Consistency check found no remaining role/adaptor protocol alignment errors.
- Validated that reviewer adapters now include `gate-artifact-policy-v1.md` and qa-auditor role/adapters include its own `protocol_evidence` requirement/output.

## Workspace Junk Cleanup

- Removed only low-risk generated artifacts under `/Users/eeo/claude-common`: `.DS_Store` files and `__pycache__` directories.
- Did not remove unknown untracked configs, source files, skill directories, docs, or existing dirty tracked changes.

## Minimal Gitignore

- Added `.gitignore` limited to generated junk patterns: `.DS_Store`, Python bytecode/cache, and common test/type/lint caches.
- Did not ignore project configs, skill directories, docs, scripts, or planning files.

## Phase 4 Pilot Validation Assets

- Claude Code implementation attempts for this follow-up timed out twice with no output and no target-file changes.
- Implemented the minimal pilot assets directly after confirming no partial Claude Code output existed.
- Added a handoff packet template with checksum placeholder semantics for dry-run use.
- Added pilot validation protocol that explicitly forbids active config writes, generator/sync scripts, commit/push, and role-agent self-orchestration.
