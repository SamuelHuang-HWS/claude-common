# Eval Policy v1

> 状态：v1.0
> 作用：定义 Eval Case 格式、Runner 规范和回归策略。
> 行业对标：SWE-bench PEV, Arize Production→Test

---

## 1. Eval 定位

Eval 用于验证 Harness 自身的正确性：
- 路由是否正确（PRD → proj-pm、bug → proj-exec）
- Skill 元数据是否健康
- Gate Artifact 格式是否合规
- Review Loop 规则是否被遵守

Eval 不验证业务代码。

---

## 2. 文件位置

```text
proj-shared/evals/
├── routing-prd.yaml
├── routing-bugfix.yaml
├── routing-review-vs-qa.yaml
├── routing-cross-review.yaml
├── metadata-health.yaml
├── gate-artifact.yaml
└── review-loop.yaml
```

---

## 3. Eval Case 格式

```yaml
name: routing-prd
category: routing
description: "PRD 类请求应路由到 proj-pm"

input:
  user_intent: "整理 PRD"
  context: {}

expected:
  route_to: proj-pm
  should_not_route_to:
    - proj-exec
    - proj-qa

assertions:
  - type: route_match
    field: next_skill
    value: proj-pm
```

---

## 4. Eval 类别

| 类别 | 验证内容 |
|---|---|
| routing | proj-start 路由正确性 |
| metadata | skill frontmatter 健康度 |
| gate | Gate artifact 格式合规性 |
| review_loop | review loop 规则遵守 |

---

## 5. Runner 规范

Runner 脚本读取 evals/ 下所有 YAML，执行断言，输出结果：

```bash
python3 proj-shared/checks/run-skill-evals.py \
  --evals proj-shared/evals \
  --contracts proj-shared/contracts
```

输出格式：
```json
{
  "total": 7,
  "passed": 6,
  "failed": 1,
  "results": [
    {"name": "routing-prd", "status": "PASS"},
    {"name": "metadata-health", "status": "FAIL", "reason": "..."}
  ]
}
```

通过条件：全部 PASS 时 exit 0，任一 FAIL 时 exit 1。

---

## 6. 生产失败转测试

> 后续阶段可增加：从真实执行失败中生成新 eval case。

流程：
1. 在实际执行中发现路由错误或 Gate 异常
2. 将该场景抽象为 eval case
3. 加入 evals/ 目录作为回归用例

---

## 7. 一句话规则

> Eval 验证 Harness 自身而非业务代码；YAML 声明式 case + 脚本 runner；生产失败可转化为回归用例。
