# Memory Governor Phase C Optimization Plan

## Decision

按 **C 档** 继续优化：

- 保持治理内核定位
- 吸收候选层 / 晋升阈值 / 错误采样
- 补 manifest / checker / fallback / example
- 不做 hook，不做自动晋升，不把它做成执行总线

这不是扩 scope，而是把已有治理内核补成“更可执行的治理流水线”。

## Goal

把 `memory-governor` 从：

- 规则完整

推进到：

- 候选层清晰
- 晋升门槛明确
- 错误采样边界明确
- manifest / checker 能承认新 target class
- generic host 示例也能跑通

## New Core Concept

新增 target class：

- `learning_candidates`

它的职责不是长期存储，而是 **观察期缓冲层**。

放这里的内容包括：

- 明确纠错
- 重复失败模式
- 反复暴露的能力缺口
- 暂时值得观察的规则候选

它和现有层的关系：

- `daily_memory`：事实和事件
- `learning_candidates`：待验证、待提炼的学习候选
- `reusable_lessons`：已经证明有复用价值
- `system_rules` / `tool_rules`：正式固化规则

## Updated Pipeline

新的推荐管道：

1. capture
2. `learning_candidates`
3. `reusable_lessons`
4. `system_rules` / `tool_rules`

其中：

- 不是所有 daily 内容都要进候选层
- 不是所有候选都要进 `reusable_lessons`
- 不是所有 lesson 都能升到宿主规则

## Promotion Thresholds

### `learning_candidates -> reusable_lessons`

建议满足任意两条才晋升：

- 同类问题重复出现 >= 2 次
- 跨不同任务出现
- 改正后明显改善执行质量
- 用户明确说这是可复用规则

### `reusable_lessons -> system_rules`

建议满足任意两条才晋升：

- 重复出现 >= 3 次
- 适用范围稳定
- 错了代价高
- 已有人类确认

### `reusable_lessons -> tool_rules`

建议满足任意两条才晋升：

- 工具误用反复出现
- 多任务重复成立
- 平台限制稳定存在
- 固化后能明显减少失败

## Error Sampling Rule

正式原则：

**失败可以自动采样，记忆不能自动晋升。**

值得采样到 `learning_candidates` 的失败：

- 同类失败重复出现
- 暴露稳定误区
- 是工具使用规则错误
- 改正后能减少未来损耗

不值得采样的失败：

- 一次性网络抖动
- 显而易见的权限拒绝
- 实验性命令失败
- 用户主动中断造成的失败

## Concrete Changes

### 1. Update `SKILL.md`

补充：

- `learning_candidates` 的角色
- 三段式管道
- 错误采样但不自动晋升

### 2. Update `references/memory-routing.md`

新增路由项：

- 明确纠错 -> `learning_candidates`
- 重复失败模式 -> `learning_candidates`
- 能力缺口候选 -> `learning_candidates`

并保留：

- 已经证明可复用的内容 -> `reusable_lessons`

### 3. Update `references/promotion-rules.md`

新增：

- `learning_candidates -> reusable_lessons`
- 建议阈值
- 不建议晋升的反例

### 4. Add `references/correction-pipeline.md`

定义：

- correction / error / gap 如何进候选层
- 候选层如何进入 `reusable_lessons`
- 什么情况下可以升到 `system_rules` / `tool_rules`

### 5. Add `references/error-sampling.md`

定义：

- 哪些错误值得采样
- 哪些错误是噪声
- 自动采样和人工晋升边界

### 6. Update `references/schema-conventions.md`

新增 `learning_candidates` schema：

- `target_class`
- `schema_version`
- `updated_at`
- `observed_issue`
- `context`
- `recurrence_count`
- `scope`
- `candidate_for`
- `status`

推荐 heading：

- `## Observations`
- `## Promotion Notes`

### 7. Update `references/adapter-manifest.md`

把 `learning_candidates` 加入标准 target classes。

同时给出：

- `single`
- `directory`
- `pattern`

三种 example。

### 8. Update `references/integration-checklist.md`

新增检查项：

- correction 是直接进入 `reusable_lessons`，还是先进入 `learning_candidates`
- 是否有自动错误采样
- 噪声过滤发生在哪一层
- 谁能决定候选被晋升

### 9. Add packaged fallback

新增：

- `assets/fallbacks/learning-candidates.md`

### 10. Add generic-host support

新增：

- `examples/generic-host/memory/learning-candidates.md`
- generic host manifest 声明

### 11. Extend checker + validator

更新：

- `scripts/check-memory-host.py`
- `scripts/validate-memory-frontmatter.py`

目标：

- checker 承认 `learning_candidates`
- validator 能校验其最小 frontmatter / heading

## Recommended Order

### Pass 1: Contract

- `SKILL.md`
- `memory-routing.md`
- `promotion-rules.md`
- `correction-pipeline.md`
- `error-sampling.md`

目标：

- 先把语言和规则定准

### Pass 2: Structured Support

- `schema-conventions.md`
- `adapter-manifest.md`
- `integration-checklist.md`
- fallback 模板

目标：

- 让新 target class 具备规范化写法

### Pass 3: Tooling + Example

- validator
- checker
- generic-host example

目标：

- 让这套升级不是纸面规则

## Acceptance Criteria

这版优化完成后，应满足：

- `learning_candidates` 成为正式 target class
- 文档里有清晰的三段式晋升路径
- promotion 不再只靠模糊主观判断
- 错误采样边界被明确写死
- fallback / example / manifest / checker 全部承认这个新 target
- 不引入自动晋升
- 不引入 hook 依赖

## Risks

### 风险 1：target class 变多，系统更重

控制方式：

- 把 `learning_candidates` 定义成“候选层”，不是强制所有宿主都必须重用
- 对简单宿主仍然允许跳过

### 风险 2：候选层和 `reusable_lessons` 重叠

控制方式：

- 用“是否已被证明可复用”作为硬边界

### 风险 3：错误采样引入噪声

控制方式：

- 只允许自动采样
- 不允许自动晋升
- 需要噪声过滤规则

## Recommendation

下一步直接执行：

- Pass 1
- Pass 2
- Pass 3

也就是按 C 档完整做完，但仍保持克制。
