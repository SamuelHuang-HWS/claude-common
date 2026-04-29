# Harness Audit Report — 2026-04-29

> **审计类型**: Harness Kernel 自审计
> **审计模式**: Phase 0a inspect → Phase 0b apply
> **审计范围**: proj-* skills + manifest + routing + boundaries

---

## 1. Frontmatter 审计

**总计**: 14 个 proj-* skill，全部含 SKILL.md

**ERROR (2)**:
- `proj-dev/SKILL.md`: frontmatter 缺少 name 字段
- `proj-uiux/SKILL.md`: frontmatter 缺少 name 字段

**修复**: Phase 0.5 补齐

---

## 2. Manifest 审计

```yaml
generated_at: "2026-04-14 21:02:16 +0800"
canonical_source: "/Users/eeo/claude-common/skills"

proj_review: "在 skipped_existing (codex/gemini)，不在 created"
cross_review: "在 skipped_existing (codex/gemini)，不在 created"
retired_qa_pro: "退役 QA 增强入口，Phase 3.5 已移除"

legacy_or_old_created_entries:
  codex: [review, autonew]
  gemini: [review, autonew, file-op, mounted, pend]

conclusion: "manifest 陈旧，但 proj-review / cross-review 并非完全缺失"
```

---

## 3. 路由矩阵覆盖度

`proj-start` 路由矩阵覆盖 10 个目标。

**WARN — 合理未覆盖 (2)**:
- `proj-close`: 非路由目标，由 proj-docs 后续进入
- `proj-dev`: 增强角色，由 proj-exec 内部按需调用

---

## 4. Skill 边界清晰度

| 边界 | 状态 |
|---|---|
| proj-review vs proj-qa | ✅ 清晰 |
| proj-qa vs cross-review | ✅ 清晰 |
| 退役 QA 增强入口 | ✅ Phase 3.5 已移除 |

---

## 5. 陈旧引用

**WARN (1)**:
- `proj-dev/SKILL.md:9` 引用 `/Users/eeo/.codex/skills/...` — 路径陈旧

**修复**: Phase 0.5 一并修正

---

## 6. 审计结论

```yaml
total_skills: 14
errors: 2
warnings: 4  # manifest 陈旧 + proj-dev 陈旧路径 + 2 个合理未覆盖
info: 0
verdict: "基线可用，Phase 0.5 修复后可继续 Phase 1"
```

---

## 7. Phase 0.5 Post-Fix 状态

```yaml
post_phase_0_5_status:
  errors_before: 2
  errors_after: 0
  warnings_before: 4
  warnings_after: 3  # manifest 陈旧 + 2 个合理未覆盖 (proj-close/proj-dev routing)
  fixes_applied:
    - "proj-dev/SKILL.md: 补齐 name: proj-dev"
    - "proj-uiux/SKILL.md: 补齐 name: proj-uiux"
    - "proj-dev/SKILL.md:9: 修正 .codex 陈旧路径 → 相对引用"
```

---

## 7. Phase 3.5 清理结果

```yaml
post_phase_3_5_status:
  metadata_errors: 0
  retired_qa_pro_entry: removed
  contract_coverage: active_proj_skills_plus_cross_review
  schema_validation: enabled_by_health_check
```
