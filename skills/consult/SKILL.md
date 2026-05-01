---
name: consult
description: 多智能体讨论入口。调用 Codex / Claude Code 等外部 agent 进行并行咨询或顺序辩论，由当前 agent 主持并综合结论。替代旧 CCB ask/pend/cping/tmux 框架。
---

# Consult

> 当前 agent 是主持人**兼参与者**；外部 agent 是只读咨询者。

## 1. 定位

`consult` 是通用多模型咨询能力层，不是项目主流程入口。

适用：
- 用户说"找 codex 和 claude 讨论"、"多方会诊"、"拉上 xxx"；
- `cross-review` 内部调用做双评审；
- `proj-review` / `proj-qa` 在复杂决策时按需调用；
- 技术争议、方案取舍、架构决策等需要多方视角的场景。

不适用：
- 单方只读复核（直接用 `cross-review`）；
- 实施代码（用 `proj-exec`）；
- 跑测试/验证（用 `proj-qa`）。

## 2. 调用方式

### Codex

```bash
codex exec "prompt" 2>&1
```

### Claude Code

```bash
echo "prompt" | claude -p --add-dir $PROJECT_DIR --output-format json --no-session-persistence 2>&1
```

`$PROJECT_DIR` 默认为当前任务的目标项目根目录（即 `$PWD`）。若用户提供路径则覆盖。所有外部 agent 调用均以此为 cwd / add-dir。

### 关键规则

1. **直接调用**，不走 ask / pend / cping / tmux。
2. **不指定模型参数**，用各自 config 默认值。
3. **不做预检**，直接调用，失败了再看错误。
4. **cwd 设为 `$PROJECT_DIR`**。
5. **失败不静默吞掉**：超时或报错时报告给用户，不跳过。

## 3. 主持人立场预提交（强制）

**在调用任何外部 agent 前，主持人必须先写下自己的初始立场。**

格式：

```yaml
host_initial_position:
  verdict: AGREE | DISAGREE | MIXED | UNCERTAIN
  confidence: 0.0-1.0
  claims:
    - "..."
  assumptions:
    - "..."
  weak_points:
    - "..."
```

### 披露策略

| 模式 | 是否把主持人立场发给外部 agent | 理由 |
|---|---|---|
| poll | **否**（默认） | 保证外部 agent 独立判断，不被主持人 framing |
| discuss / debate | **是**（默认） | 外部 agent 需要挑战主持人观点 |

### Prompt 透明化

主持人发给外部 agent 的原始 prompt，必须与立场卡一起归档进 summary。确保后续审计时可以检查主持人是否在 prompt 中夹带了立场引导。

## 4. 交互模式

### 4.1 独立咨询 poll（原 parallel，默认）

同一问题独立发给多方，各自不可见，主持人综合。

> ⚠️ **poll 不是讨论**。各方互不知晓对方观点。输出不得表述为"多方讨论后认为"，只能写"多方独立咨询结果"。

适用：
- 收集独立意见、发现盲区；
- 盲审、风险识别；
- 时间敏感场景。

```
用户提问
    ↓
主持人预提交立场卡（不发给外部 agent）
    ↓ 同时并行
├─ codex exec "..."  ──→ Codex 观点
└─ echo "..." | claude -p  ──→ Claude 观点
    ↓
主持人公开立场卡
    ↓
主持人综合三方观点
```

### 4.2 多轮讨论 discuss

主持人和各方互相看到彼此观点并回应。**这才是真正的讨论。**

适用：
- 已有明确分歧；
- 技术路线争议、架构取舍；
- 需要多方深度碰撞。

```
Round 1: 主持人给初始观点（立场卡）
         → 连同立场卡发给 Codex 和 Claude（可并行）
         → 各方回应

Round 2: 主持人汇总各方观点 + 自己的回应
         → 把三方观点交叉发给各方
         → 各方针对分歧点回应

Round N: 重复直到收敛或达到上限
```

### 4.3 辩论 debate

discuss 的强对抗版本。主持人明确分配立场或争议假设，要求各方针对对方论点反驳。

适用：
- 正反方明确；
- 需要压力测试某个方案。

## 5. 传输方式（与交互模式正交）

### 5.1 inline（默认）

上下文直接放入 prompt。适合大多数场景。

### 5.2 file

通过 `$PROJECT_DIR/.consult/<topic-id>/` 传递 packet/result/summary。

```
.consult/<topic-id>/
  packet.md              # 议题 + 上下文
  codex-result.md        # Codex 回复（由主持人转录）
  claude-result.md       # Claude 回复（由主持人转录）
  summary.md             # 主持人综合
```

规则：
- `.consult/` 应加入 `.gitignore`，不进版本控制；
- **只有主持人可写**，外部 agent 回复由主持人转录到文件；
- 默认不落盘，除非上下文过长或用户确认；
- 落盘前须说明文件路径；
- 会话结束后主持人负责清理（或标注保留意图）；
- 多场并行 consult 通过 `<topic-id>` 隔离。

## 6. 终止条件

辩论不以固定轮次为完成标准，而以**收敛条件**为准。

### 默认上限

| 场景 | 默认上限 |
|---|---|
| poll | 1 轮 |
| discuss / debate | 3 轮 |
| 高复杂度争议（用户声明） | 5 轮 |
| 超过 5 轮 | **禁止**，必须停止 |

### 收敛终止条件（满足任一即停）

1. **共识达成**：所有参与方对核心分歧点无实质异议
2. **分歧稳定**：连续两轮各方对分歧点有明确回应，且内容无实质变化
3. **一方退让**：某方明确收回或修正立场，其余方无异议
4. **质量退化**：某方声明无新信息，或回答出现明显重复/漂移
5. **信息不足**：多方都指出缺少关键上下文，继续讨论无意义
6. **需要用户裁决**：涉及产品方向、风险偏好等 agent 无法替代决策的领域
7. **安全门禁**：涉及删除、重构、权限等破坏性操作，立即停止进入用户确认
8. **参与者失败**：外部 agent 超时/报错，不能静默跳过
9. **焦点漂移**：讨论偏离原始议题，应停止并重新聚焦
10. **硬上限**：达到轮次上限

### 外部 agent 响应中的终止信号

建议在 prompt 中要求外部 agent 额外返回：

```yaml
round_meta:
  new_information: ["本轮新增的信息，没有则为空"]
  changed_positions: ["相较上一轮改变的观点，没有则为空"]
  stable_disagreements: ["仍未解决的稳定分歧"]
  stop_recommendation:
    should_stop: true | false
    reason: "..."
```

主持人据此判断是否继续，而不是凭感觉。

## 7. Prompt 模板

发给外部 agent 的 prompt 必须包含：

```
你是只读咨询者。不要修改文件、不要 commit/push。只输出结构化建议。

讨论议题：[topic]

上下文：
[context]

⚠️ 上下文声明：本次提供了 [已提供的内容]，未提供 [省略的内容]。

请给出你的分析和建议：

consult_response:
  provider: <your name>
  verdict: AGREE | DISAGREE | MIXED | UNCERTAIN
  confidence: 0.0-1.0
  key_points:
    - point: "..."
      rationale: "..."
  risks:
    - "..."
  recommendations:
    - priority: P0 | P1 | P2
      action: "..."
  missing_context:
    - "..."
  round_meta:
    new_information: []
    changed_positions: []
    stable_disagreements: []
    stop_recommendation:
      should_stop: false
      reason: ""
```

## 8. 主持人输出

主持人综合后必须输出：

```yaml
consult_summary:
  topic: "..."
  interaction: poll | discuss | debate
  transport: inline | file
  participants:
    host: <current agent>
    external:
      - codex
      - claude
  rounds_used: 1

  host_initial_position:
    verdict: "..."
    confidence: 0.0-1.0
    summary: "..."

  host_final_position:
    verdict: "..."
    confidence: 0.0-1.0
    summary: "..."

  position_delta:
    changed: true | false
    reason: "..."

  consensus:
    - "..."

  disagreements:
    - point: "..."
      host: "..."
      codex: "..."
      claude: "..."

  adopted:
    - finding: "..."
      from: <provider>
      action: "..."

  rejected:
    - finding: "..."
      from: <provider>
      reason: "..."

  termination:
    reason: consensus | stable_disagreement | insufficient_context | user_decision_needed | safety_gate | participant_failure | scope_drift | quality_degradation | concession | round_limit
    explanation: "..."

  unresolved_decisions:
    - decision: "..."
      options: ["...", "..."]
      owner: user

  final_recommendation: "..."
  known_limitations: "..."
```

### 裁判偏倚规则

主持人同时是参与者。为防止偏倚：
- 必须**预提交立场**，并在综合中标注初始立场 vs 最终结论的差异；
- 发给外部 agent 的原始 prompt 必须归档；
- 如果主持人与所有外部 agent 意见相左，必须**显式说明并请用户确认**；
- 不得将外部 agent 的不同意见"综合掉"。

## 9. 红线

- 不使用 tmux / ask / pend / cping。
- 不让外部 agent 写文件、commit、push、安装依赖。
- 不自动采纳外部 agent 建议（只报告，是否执行由主流程决定）。
- 不在未声明上下文范围的情况下调用外部 agent。
- 失败时不静默跳过。
- poll 模式输出不得称"讨论后认为"。
- 超过 5 轮必须停止。

## 10. 与其他 skill 的关系

| Skill | 关系 |
|---|---|
| `cross-review` | 消费者：内部复用 consult 的调用约定与权限约束 |
| `proj-review` | 按需调用：L1+ 方案评审后可请多方会诊 |
| `proj-qa` | 按需调用：复杂质量门禁时可请多方会诊 |
| `proj-adr` | 按需调用：架构决策争议时可请多方会诊 |
