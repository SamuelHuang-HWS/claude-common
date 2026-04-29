# Skill Contract Rules v1

> 状态：v1.0
> 作用：定义 Skill Contract 的格式规范、必填字段与校验规则。
> 行业对标：CrewAI Contract-First, Agent Format (.agf.yaml)

---

## 1. Contract 定位

每个 active `proj-*` skill 与 `cross-review` 应有一个对应的 contract 文件，定义：
- **What**：这个 skill 做什么
- **When**：什么时候使用它
- **I/O**：输入/输出契约
- **Forbidden**：禁止动作

Contract 与 SKILL.md 互补：
- SKILL.md 提供完整操作说明（人类可读）
- Contract 提供结构化接口定义（机器可校验）

Contract 不复制 SKILL.md 的说明文本。

---

## 2. 文件位置

```text
proj-shared/contracts/
├── contract.schema.json     ← JSON Schema 校验定义
├── README.md                ← 格式说明
└── {skill-name}.contract.yaml
```

---

## 3. 必填字段

```yaml
name: string           # 必须与目录名一致
role: enum             # main_chain | enhancement | support | deprecated
entry_type: enum       # default | routed | direct | internal
what: string           # 做什么（简洁）
when: string           # 什么时候用（触发条件）
required_inputs: list  # 至少一个输入
required_outputs: list # 至少一个输出
forbidden_actions: list # 至少一个禁止动作
requires_user_gate: bool
next_skills: list      # 可路由的下一个 skill
```

---

## 4. 可选字段

```yaml
expected_output_format: enum  # structured | freeform
optional_inputs: list         # 可选输入
max_rounds: int               # 适用于 review 类 skill
triggers: list                # 自然语言触发短语
deprecated_by: string         # 若 role=deprecated，指向替代 skill
```

---

## 5. Role 分类

| Role | 含义 | 典型 Skill |
|---|---|---|
| main_chain | 主流程 skill，构成 PEV 主链 | proj-start, proj-exec, proj-qa, proj-docs, proj-close |
| enhancement | 增强角色，按需参与 | proj-pm, proj-review, proj-dev, cross-review |
| support | 支撑能力，被其他 skill 调用 | proj-struct, proj-adr, proj-checkpoint |
| deprecated | 已退役的兼容壳；若目录已移除则不保留 contract | legacy shell |

---

## 6. What+When 规则

描述必须同时包含 **What**（做什么）和 **When**（什么时候触发）。

✅ 正确示例：
```yaml
what: "项目任务实施主入口"
when: "任务已明确且用户已放行后"
```

❌ 错误示例：
```yaml
what: "帮助实施任务"
when: ""  # 缺失 When
```

---

## 7. 校验规则

Health Check 脚本应校验：
1. YAML 可解析
2. 所有必填字段存在且非空
3. `name` 与 contract 文件名一致（`proj-exec.contract.yaml` → `name: proj-exec`）
4. `name` 对应的 skill 目录存在
5. `role` 值在合法枚举中
6. `next_skills` 中引用的 skill 存在
7. `deprecated` role 必须有 `deprecated_by`
8. `required_inputs` 和 `required_outputs` 至少各一项
9. `forbidden_actions` 至少一项

---

## 8. 一句话规则

> Contract 定义 What+When+I/O+Forbidden，不复制 SKILL.md 文本；active skill 必须覆盖，已移除的退役入口不保留 contract。
