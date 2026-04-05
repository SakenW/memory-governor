# Memory Governor Eval Lab Design

## Goal

设计一个足够轻、但能真实比较差异的评估环境，用来测试：

- 当前 `memory-governor`
- 加入 `learning_candidates` 后的候选方案

重点不是“跑自动化 benchmark”，而是回答：

**这个新层到底有没有减少混乱、提高提炼质量，并且没有把系统搞重。**

## Core Question

我们不是要证明 `learning_candidates` “听起来合理”，而是要验证：

1. 它是否减少了“过早晋升”
2. 它是否减少了“纠错散落在 daily / reusable_lessons / system_rules 之间”
3. 它是否提高了恢复和提炼质量
4. 它带来的认知负担是否值得

## Evaluation Shape

建议用 **A/B 对照 + 场景回放**。

### A 组：Current

当前正式内核：

- `daily_memory`
- `reusable_lessons`
- `proactive_state`
- `working_buffer`
- `project_facts`
- `system_rules`
- `tool_rules`

没有 `learning_candidates`。

### B 组：Candidate

实验内核：

- 保留现有 target classes
- 增加 `learning_candidates`
- 增加候选层晋升规则

## What To Compare

每个场景都比较这 5 个维度：

1. **Routing clarity**
   是否容易判断写到哪
2. **Promotion quality**
   是否减少过早晋升 / 漏晋升
3. **Recovery usefulness**
   后续恢复时是否更有帮助
4. **Noise control**
   是否把一次性噪声挡在外面
5. **Operational weight**
   是否明显增加宿主和接入者负担

## Success Metrics

建议用人工打分，不先追求伪精确：

- `better`
- `same`
- `worse`

同时补一句理由。

如果想更细一点，可用 1-5 分：

- 1 = 明显更差
- 3 = 差不多
- 5 = 明显更好

## Test Scenarios

至少测这 5 类：

### 1. Direct Correction

例：

- 用户明确纠正表达方式
- 这条纠正可能可复用，但一次还不够稳

想验证：

- A 组会不会过早直接写进 `reusable_lessons`
- B 组会不会更自然地先进候选层

### 2. Repeated Tool Misuse

例：

- 连续两次用错命令或平台格式
- 修正后明显减少失败

想验证：

- A 组是否容易直接跳到 `tool_rules`
- B 组是否更适合先候选，再晋升

### 3. One-Off External Failure

例：

- 一次性网络超时
- 第三方 API 抖动

想验证：

- B 组会不会因为引入候选层，反而把噪声也吸进来

### 4. Project-Only Exception

例：

- 某项目里有一个临时约束
- 这条约束不该污染全局 reusable lessons

想验证：

- A / B 两组是否都能稳定拦在 `project_facts`
- `learning_candidates` 会不会误吸项目局部特例

### 5. Interrupted Recovery

例：

- 任务被中断
- 有当前状态、有临时 breadcrumb、有一个刚刚暴露出来的待观察误区

想验证：

- 候选层是否真的帮助恢复
- 还是只是多了一个要读的层，反而更乱

## Test Method

每个场景按同样流程：

1. 给出场景描述
2. 分别让 A 组和 B 组决定：
   - 路由到哪
   - 是否升格
   - 是否进入规则层
3. 再给一个“过一段时间后的后续事件”
4. 观察哪组更容易：
   - 避免噪声污染
   - 提炼出正确规则
   - 维持清晰恢复路径

## Environment Layout

建议新增一个轻量评估目录：

- `skills/memory-governor/examples/eval-lab/`

里面放：

- `README.md`
- `scorecard-template.md`
- `scenarios/`

这个目录不需要一开始就接入 checker。  
它的职责是：

- 提供统一场景
- 提供统一评分方式
- 让以后不同版本的 `memory-governor` 可比较

## Why Not Start With Full Automation

因为这里评估的是：

- 路由质量
- 晋升判断
- 噪声边界

这些很多是治理判断，不是纯程序正确性。

如果一开始就做重自动化，很容易变成：

- 指标很精致
- 但判断仍然是空的

所以建议：

- 先做场景回放 + 人工评分
- 等 `learning_candidates` 真进入实验层后，再考虑更自动的 replay harness

## Decision Rule

只有在下面 3 条至少满足 2 条时，才建议把 `learning_candidates` 从实验层推进到正式层：

1. 多数场景里 promotion quality 明显更好
2. 噪声控制没有明显变差
3. 宿主负担没有显著上升

如果达不到，就说明：

- 它也许只是一个“看起来合理”的层
- 还不值得进入标准 target class

## Recommendation

下一步最值钱的不是继续抽象，而是：

1. 搭这个 eval lab 骨架
2. 写 5 个场景
3. 用当前内核先跑一遍基线
4. 再拿实验版去对照

这样我们评估的是“它到底值不值得存在”，而不是“概念是否漂亮”。
