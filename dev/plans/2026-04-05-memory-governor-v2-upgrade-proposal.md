# Memory Governor v2 Upgrade Proposal

## Conclusion

`memory-governor` 值得继续升级，但不应该吸收 `self-improving-agent` 的整套机制。

应该吸收的是 4 个局部工程优点：

1. 把修正 / 错误 / 缺口从泛化记忆里单独拎出来
2. 给 promotion 增加更机械的晋升阈值
3. 增加候选层，避免内容直接冲进长期规则
4. 支持工具失败采样，但不允许自动晋升

一句话：

`memory-governor` 下一阶段该补的是“候选层和门槛机制”，不是“更重的自动化系统”。

## Current State

当前内核已经具备：

- target classes
- adapter / fallback
- routing
- promotion rules
- exclusions
- read-order
- retention rules
- stateful target semantics
- host profiles / manifest / checker

它的问题不是骨架不对，而是：

- correction / learning 还缺一个观察期缓冲层
- promotion 还偏原则型，门槛不够工程化
- error sampling 还没有正式入口

## Recommended Upgrade Level

推荐走 **B 档升级**：

- 比最小升级更完整
- 但仍然保持 `memory-governor` 是治理内核
- 不把 hook、本地自动化、执行逻辑塞进内核

## New Target Class

建议新增：

- `learning_candidates`

不建议叫 `correction_memory`，因为 scope 太窄。

`learning_candidates` 应覆盖：

- 明确被纠正的内容
- 重复失败模式
- 暴露出来的能力缺口
- 待观察的可复用规则
- 值得进入 `reusable_lessons`，但还不该直接晋升的材料

## New Pipeline

建议把当前升级路径明确成三段：

1. `learning_candidates`
2. `reusable_lessons`
3. `system_rules` / `tool_rules`

解释：

- `learning_candidates`
  观察期缓冲层，允许原始修正和初步提炼
- `reusable_lessons`
  已经证明可复用，但还不是宿主硬规则
- `system_rules` / `tool_rules`
  正式固化到宿主治理规则

## Promotion Thresholds

建议给 promotion 增加“建议性阈值”，而不是自动化阈值。

### `learning_candidates -> reusable_lessons`

满足任意两条，才建议晋升：

- 同类问题重复出现 >= 2 次
- 跨不同任务出现
- 明确改善了后续判断 / 执行质量
- 用户明确指出这是一个可复用规则

### `reusable_lessons -> system_rules`

满足任意两条，才建议晋升：

- 重复出现 >= 3 次
- 适用范围稳定，不是项目临时特例
- 错了代价高
- 已有人类确认值得固化

### `reusable_lessons -> tool_rules`

满足任意两条，才建议晋升：

- 工具误用重复出现
- 规则在多个任务里都成立
- 平台 / 工具限制稳定存在
- 固化后能明显减少未来失败

## Error Sampling Principle

建议新增正式原则：

**失败可以自动采样，记忆不能自动晋升。**

值得进入 `learning_candidates` 的失败：

- 同类失败重复出现
- 暴露稳定误区
- 是工具使用规则错误，不是随机外部波动
- 改正后可显著减少未来损耗

不值得进入 `learning_candidates` 的失败：

- 一次性网络抖动
- 权限拒绝但原因显然
- 实验性命令失败
- 用户中断导致的失败

## Schema Proposal

建议给 `learning_candidates` 增加轻量 schema。

推荐字段：

- `target_class = "learning_candidates"`
- `schema_version`
- `updated_at`
- `observed_issue`
- `context`
- `recurrence_count`
- `scope = "global" | "domain" | "project"`
- `candidate_for = "reusable_lessons" | "system_rules" | "tool_rules"`
- `status = "open" | "observing" | "promoted" | "discarded"`

推荐 heading：

- `## Observations`
- `## Promotion Notes`

## File-Level Changes

### Add

- `references/correction-pipeline.md`
- `references/error-sampling.md`

### Update

- `SKILL.md`
  增加 `learning_candidates` 说明
- `references/memory-routing.md`
  增加新的 target class 和路由表项
- `references/promotion-rules.md`
  增加门槛和三段式升级路径
- `references/schema-conventions.md`
  增加 `learning_candidates` schema
- `references/integration-checklist.md`
  增加 correction / sampling 接入检查项
- `references/adapter-manifest.md`
  把 `learning_candidates` 加入标准 target class

### Optional Later

- `assets/fallbacks/learning-candidates.md`
- `examples/generic-host/memory/learning-candidates.md`
- manifest / checker support for this new target

## Minimal Diff Strategy

最小且不破坏现有结构的顺序：

1. 先补文档层 target class 和 routing
2. 再补 promotion thresholds
3. 再补 schema 和 fallback 模板
4. 最后再考虑 manifest / checker 扩展

这样做的好处：

- 先把 contract 说清楚
- 不会因为工具层还没支持，就把治理层卡死
- 宿主可以先手工采用，再逐步获得 machine-checkable support

## What Not to Absorb

不建议吸收：

- `.learnings/` 这种具体目录结构
- shell hook / prompt hook 逻辑
- 自动晋升机制
- 把错误采样直接塞进治理内核执行

这些都应属于：

- host integration
- optional companion skill
- future automation layer

而不是 `memory-governor` 本身。

## Recommended Execution Order

### Phase A

- `learning_candidates`
- `correction-pipeline.md`
- promotion thresholds

### Phase B

- `error-sampling.md`
- `learning_candidates` schema
- integration checklist updates

### Phase C

- packaged fallback
- generic-host example
- manifest / checker support

## Recommendation

下一步建议直接做 **Phase A + Phase B 的文档层升级**，先不做 hook，不做自动晋升。

这会让 `memory-governor` 从：

- 规则完整

升级到：

- 规则更可执行
- 候选层更清晰
- 晋升更有门槛
- 错误采样边界更明确
