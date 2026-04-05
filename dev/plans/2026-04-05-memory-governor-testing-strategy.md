# Memory Governor Testing Strategy

## English Summary

This document defines a layered testing strategy for `memory-governor`.
It separates:

1. script correctness
2. host integration correctness
3. governance-quality evaluation

The goal is to avoid mixing runtime checks with policy evaluation.

In short:

- automate what is mechanical
- scenario-test what is judgment-heavy
- do not treat governance quality like a pure parser problem

Recommended layers:

- Layer 1: package smoke tests
- Layer 2: script correctness tests
- Layer 3: host integration tests
- Layer 4: governance evaluation tests

## 目标

为 `memory-governor` 设计一套分层测试方案，回答三个不同问题：

1. **脚本有没有坏**
2. **宿主接线有没有坏**
3. **治理判断是不是变好了**

这三类问题不能混在一起测。

## 核心原则

`memory-governor` 不是执行型 skill。  
它的价值来自：

- contract 是否清晰
- tooling 是否可靠
- host integration 是否稳定
- 治理判断是否真的更好

所以测试也要分层。

## 测试金字塔

建议分 4 层。

### Layer 1: Package Smoke Tests

目标：

- 包结构没坏
- 关键文件都在
- 脚本至少能启动

检查内容：

- `SKILL.md`
- `README.md`
- `VERSION`
- `references/`
- `assets/fallbacks/`
- `scripts/check-memory-host.py`
- `scripts/validate-memory-frontmatter.py`
- `scripts/bootstrap-generic-host.sh`

建议命令：

```sh
python3 -m py_compile scripts/check-memory-host.py scripts/validate-memory-frontmatter.py
sh -n scripts/bootstrap-generic-host.sh
```

这层回答：

- 包能不能被正常分发和读取

## Layer 2: Script Correctness Tests

目标：

- checker 和 validator 的基本逻辑正确
- manifest 解析和 fallback 行为不回归

这层最适合做成自动化。

### 2.1 Validator Tests

为 `validate-memory-frontmatter.py` 准备 fixture：

- valid `proactive_state`
- invalid `proactive_state`
- valid `working_buffer`
- invalid `working_buffer`
- valid `reusable_lessons`
- invalid `reusable_lessons`

断言：

- 有效 fixture 返回 `OK`
- 缺 key / heading / enum 值错误时返回非零

### 2.2 Checker Tests

准备 4 组宿主 fixture：

1. valid generic host
2. valid manifest host with primary adapter
3. valid manifest host with fallback adapter
4. invalid host with broken manifest

断言：

- valid host -> `PASS`
- fallback host -> `PASS` 或明确 `OK fallback`
- broken host -> `FAIL`

特别要测：

- `fallback_paths`
- `single / split / directory / pattern`
- `structured = true / false`
- Python 3.9 / 3.10 的 `tomli` fallback

这层回答：

- 工具到底有没有按 contract 工作

## Layer 3: Host Integration Tests

目标：

- reference host 和 generic host 真能被接起来

这层不追求细颗粒单元测试，而是偏集成测试。

### 3.1 Generic Host Fixture

直接使用：

- `examples/generic-host/`

断言：

```sh
python3 scripts/check-memory-host.py examples/generic-host
```

结果应为：

- `PROFILE: manifest`
- `STATUS: PASS`

### 3.2 Bootstrap Test

新建临时目录，运行：

```sh
scripts/bootstrap-generic-host.sh /tmp/some-host
python3 scripts/check-memory-host.py /tmp/some-host
```

断言：

- bootstrap 后骨架完整
- checker 通过

### 3.3 OpenClaw Reference Test

如果要验证 OpenClaw reference profile，不在发布仓库里直接耦合真实 home 路径。  
更好的做法是准备一个最小 OpenClaw fixture 目录。

建议后续新增：

- `examples/openclaw-host/`

这层回答：

- 这个包是不是真的能被宿主接起来

## Layer 4: Governance Evaluation Tests

目标：

- 新规则是否真的更好
- 而不是只是更多

这层不应该强行自动化。

它最适合用场景回放 + 评分模板。

当前已经有基础设施：

- `examples/eval-lab/`

建议用它来做 A/B 评估：

- A 组：当前正式内核
- B 组：实验性变体

比较维度：

- routing clarity
- promotion quality
- recovery usefulness
- noise control
- operational weight

这层回答：

- 新增概念值不值得存在

## What To Automate First

优先级建议：

1. Layer 1
2. Layer 2
3. Layer 3 generic host
4. Layer 4 保持人工评估

不要一开始就尝试把治理判断自动化。

## Minimal CI Gate

如果后面要加 CI，最小 gate 建议是：

1. Python scripts compile
2. validator fixture pass/fail as expected
3. generic-host checker pass
4. bootstrap -> checker pass

不建议把 eval-lab 打分塞进 CI。

## Suggested Directory Layout

建议后续新增一个测试目录：

- `tests/`

内部结构：

- `tests/fixtures/validator/`
- `tests/fixtures/hosts/generic-valid/`
- `tests/fixtures/hosts/manifest-fallback/`
- `tests/fixtures/hosts/broken-manifest/`
- `tests/test_validator.py`
- `tests/test_host_checker.py`
- `tests/test_bootstrap.py`

## Example Assertions

### Validator

- missing frontmatter -> fail
- wrong enum -> fail
- missing heading -> fail
- valid structured fallback -> pass

### Checker

- unknown manifest target -> warn
- broken fallback path -> fail
- fallback path present when primary missing -> pass
- pattern target declared correctly -> pass

## Release Gate Recommendation

发布前至少跑：

```sh
python3 -m py_compile scripts/check-memory-host.py scripts/validate-memory-frontmatter.py
sh -n scripts/bootstrap-generic-host.sh
python3 scripts/check-memory-host.py examples/generic-host
python3 scripts/validate-memory-frontmatter.py \
  examples/generic-host/memory/proactive-state.md \
  examples/generic-host/memory/reusable-lessons.md \
  examples/generic-host/memory/working-buffer.md
```

## 建议

最合理的测试设计不是“先造完整测试框架”，而是：

1. 先把 Layer 1-3 做成可重复脚本
2. 用 eval-lab 承接治理判断
3. 等 `learning_candidates` 真进入实验层，再给它加自己的 fixture 和回放场景

一句话：

**脚本正确性自动测，治理价值场景测。**
