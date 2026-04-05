# Eval Lab

This directory is a lightweight evaluation environment for `memory-governor`.

这个目录是给 `memory-governor` 准备的轻量评估环境。

Its purpose is to compare:

- the current core
- an experimental variant

它的目的，是对比：

- 当前正式内核
- 一个实验性变体

without pretending we already need a full automated test harness.

而不是假装我们现在已经需要一整套重型自动化评估系统。

## What It Tests

Each scenario is used to compare:

- routing clarity
- promotion quality
- recovery usefulness
- noise control
- operational weight

每个场景都用来比较：

- routing clarity
- promotion quality
- recovery usefulness
- noise control
- operational weight

## How To Use It

1. Pick a scenario from `scenarios/`
2. Evaluate it with the current core
3. Evaluate it with the experimental design
4. Record the result in `scorecard-template.md`

使用方式：

1. 从 `scenarios/` 里选一个场景
2. 用当前正式内核评估一次
3. 用实验性设计再评估一次
4. 把结果记录到 `scorecard-template.md`

## Important Constraint

This lab is intentionally judgment-oriented.

这个实验台是有意保持“判断导向”的。

It is not trying to prove:

- parser correctness
- script correctness
- filesystem wiring correctness

它不是为了证明：

- parser correctness
- script correctness
- filesystem wiring correctness

Those belong to validators and host checkers.

这些事情应该交给 validator 和 host checker。

This lab is for answering:

**does a proposed memory-layer change actually improve governance quality?**

这个实验台真正要回答的是：

**一个新的记忆层设计，是否真的改善了治理质量？**
