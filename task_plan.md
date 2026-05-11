# Task Plan: Phase 1 Protocol Evidence Loop

## Goal
Make shared protocol reading enforceable for the proj skill chain by adding minimal protocol evidence output/checks without broad rewrites.

## Scope
Modify only:
- skills/proj-start/SKILL.md
- skills/proj-qa/SKILL.md
- skills/proj-shared/defaults/default-contract.yaml
- optionally skills/proj-shared/SKILL.md for [MANDATORY] reading rule notes

## Non-goals
- No PROTOCOL_KERNEL.md in Phase 1
- No standalone verifier-gate-protocol.md in Phase 1
- No changes to proj-exec/proj-review/proj-close in Phase 1
- No cleanup of existing dirty git status
- No commit/push

## Phases
1. [complete] Read planning and target context
2. [complete] Apply minimal protocol_evidence edits
3. [complete] Validate YAML/text consistency and diff scope
4. [complete] Summarize evidence, risks, rollback

## Decisions
- Follow Claude Code review: reduce scope; enforce via evidence fields and QA check.
- Prefer existing proj-shared authority over new PROTOCOL_KERNEL.

## Errors Encountered
| Error | Attempt | Resolution |
|---|---|---|

## Review Follow-up
- Claude Code returned FIX; P1/P2 required actions were applied in proj-qa/default-contract and recorded in findings.md.

## Phase 1 Commit Boundary

Claude Code final review found no blocking issue in the in-scope Phase 1 protocol-evidence design, but warned that the repository contains many unrelated dirty tracked changes.

Phase 1 commit/staging boundary:
- Include only the four skill/config files changed for protocol evidence plus the three planning files.
- Exclude all pre-existing dirty files, especially `skills/proj-shared/references/ai-team-workflow-model-v1.md`.
- Never use `git add .` for this Phase 1 work.

# Phase 2: Verifier Gate Protocol

## Goal
Institutionalize cross-agent verification at key proj gates without creating a second review system.

## Scope
Phase 2 in-scope files:
- `skills/proj-shared/references/verifier-gate-protocol.md` (new)
- `skills/proj-shared/SKILL.md`
- `skills/proj-shared/defaults/default-contract.yaml`
- `skills/proj-review/SKILL.md`
- `skills/proj-exec/SKILL.md`
- `skills/proj-qa/SKILL.md`
- `task_plan.md`, `findings.md`, `progress.md`

## Non-goals
- Do not modify `review-loop-policy-v1.md`, `gate-artifact-policy-v1.md`, or `harness-model-v1.md`; only reference them.
- Do not modify `proj-close` / `proj-docs` in Phase 2.
- Do not touch pre-existing dirty files such as `ai-team-workflow-model-v1.md`.
- Do not use `git add .`.

## Design Decisions from Claude Code Pre-review
- Verifier Gate must inherit `review_packet -> review_result -> adoption_log`; no parallel `review_card` format.
- `owner_resolution` lives inside/alongside `adoption_log`, not as a separate review system.
- Phase 2 applies to Gate 3 and `proj-exec -> proj-qa` handoff only.
- `proj-qa` performs evidence checks only; it does not execute Verifier Gate.

# Phase 3: Close/Docs Evidence Gate

## Goal
Connect protocol evidence and verifier evidence to final documentation and close gates without turning proj-close into a second QA.

## Scope
- `skills/proj-close/SKILL.md`
- `skills/proj-docs/SKILL.md`
- `skills/proj-shared/defaults/default-contract.yaml`
- `skills/proj-shared/references/verifier-gate-protocol.md` (coverage statement only)
- planning files

## Non-goals
- Do not modify proj-qa in Phase 3.
- Do not rerun or redefine QA from proj-close.
- Do not modify review-loop/gate/harness references.
- Do not touch pre-existing dirty files.

## Key Boundary
`proj-close` checks evidence existence and upstream pass/closed status only. It must not re-sample protocol rules, rerun tests, redo code review, or execute Verifier Gate.

# Phase 4: Role-Adapter Layer (Native Agent Adapter)

## Goal
Introduce platform-native subagent support without building a custom agent runtime. Sisyphus owns role contracts, handoff packets, evidence schemas, and adapter templates; Claude Code / Codex / Gemini execute through their native mechanisms.

## Scope
Phase 4 v1 in-scope files:
- `skills/proj-shared/references/role-adapter-layer-protocol.md` (new)
- `skills/proj-shared/references/role-contract-schema.md` (new)
- `skills/proj-shared/references/handoff-packet-schema.md` (new)
- `skills/proj-shared/references/protocol-boot-sequence.md` (new)
- `skills/proj-shared/agents/roles/implementer.role.yaml` (new)
- `skills/proj-shared/agents/roles/reviewer.role.yaml` (new)
- `skills/proj-shared/agents/roles/qa-auditor.role.yaml` (new)
- `skills/proj-shared/agent-adapters/claude-code/*.md` (new templates)
- `skills/proj-shared/agent-adapters/codex/*.toml` (experimental skeleton templates)
- `skills/proj-shared/agent-adapters/gemini/README.md` (adapter status note)
- `skills/proj-shared/SKILL.md`
- `skills/proj-shared/defaults/default-contract.yaml`
- planning files

## Non-goals
- Do not modify active `~/.claude/agents`, `~/.codex/agents`, or Gemini extension directories.
- Do not create a custom agent runtime.
- Do not add generator/sync automation in v1.
- Do not alter unrelated dirty files or archive old skills.
- Do not commit/push.

## Phases
1. [complete] Define Phase 4 protocol and schema documents
2. [complete] Define v1 role contracts: implementer, reviewer, qa-auditor
3. [complete] Add Claude Code adapter templates and Codex/Gemini placeholders
4. [complete] Register references in proj-shared/default contract
5. [complete] Validate YAML/TOML/text consistency and run review gate

## Decisions
- Formal name: Role-Adapter Layer; Native Agent Adapter is a search-friendly subtitle only.
- v1 roles: implementer, reviewer, qa-auditor. Main session remains orchestrator and is not registered as a subagent.
- v1 implementation: Claude Code templates are concrete; Codex templates are experimental skeletons; Gemini is documented as pending/stabilizing.
- Handoff Packet is the state-bus between roles.
- Protocol Boot Sequence is mandatory in every adapter template.

## Errors Encountered
| Error | Attempt | Resolution |
|---|---|---|

## Phase 4 Follow-up: Pilot Validation Assets

### Goal
Add non-invasive dry-run assets for Role-Adapter Layer so future validation can exercise handoff packets and role_result evidence without installing native agents or touching active config.

### Scope
- `skills/proj-shared/templates/handoff-packet-template.yaml`
- `skills/proj-shared/references/role-adapter-pilot-validation.md`
- `skills/proj-shared/SKILL.md`
- `skills/proj-shared/defaults/default-contract.yaml`
- planning files

### Non-goals
- Do not modify `~/.claude/agents`, `~/.codex/agents`, or Gemini extension directories.
- Do not write generator/sync automation.
- Do not commit/push.

### Status
- [complete] Added handoff packet template.
- [complete] Added pilot validation protocol.
- [complete] Registered template/protocol in proj-shared and default contract.
