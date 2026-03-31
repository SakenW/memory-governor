# Adapter Manifest

## Goal

让 custom host 可以显式声明：

- 自己实现了哪些 target classes
- 每个 target class 映射到哪些路径
- 是 single 还是 split adapter
- 哪些 target 需要结构化 schema 校验

这样 host checker 就不必只靠 reference profile 猜目录。

## File Name

默认文件名：

- `memory-governor-host.toml`

推荐放在宿主根目录。

## Minimal Shape

```toml
version = "0.1"
profile = "generic"

[targets.reusable_lessons]
mode = "single"
paths = ["memory/reusable-lessons.md"]
structured = true
```

## Top-Level Keys

- `version`
  当前 manifest 版本。推荐先用 `"0.1"`。
- `profile`
  可选。宿主自我声明的 profile，比如 `"generic"`、`"openclaw"`、`"custom"`。
- `[targets.*]`
  每个 target class 一张表。

## Supported Target Classes

当前标准 target classes：

- `long_term_memory`
- `daily_memory`
- `reusable_lessons`
- `proactive_state`
- `working_buffer`
- `project_facts`
- `system_rules`
- `tool_rules`

## Per-Target Fields

### `mode`

支持：

- `single`
- `split`
- `directory`
- `pattern`

含义：

- `single` -> 一个文件实现一个 target
- `split` -> 多个文件联合实现一个 target
- `directory` -> 一个目录承接这个 target
- `pattern` -> 用路径模式描述，例如 daily note

### `paths`

必须是字符串数组。

示例：

```toml
paths = ["memory/proactive-state.md"]
paths = ["~/proactivity/memory.md", "~/proactivity/session-state.md"]
paths = ["memory"]
paths = ["notes/daily/YYYY-MM-DD.md"]
```

规则：

- 相对路径按宿主根目录解析
- `~` 会展开到当前用户 home
- `single` 必须只有一个路径
- `split` 至少两个路径

### `structured`

可选布尔值。

用于声明这个 target 是否应该走 schema 校验。

默认建议：

- `reusable_lessons` -> `true`
- `proactive_state` -> `true`
- `working_buffer` -> `true`

但如果宿主当前接的是 legacy external adapter，而且这些文件还不是 schema-frontmatter 格式，也可以先声明成 `false`。

这表示：

- target class 语义仍然成立
- checker 只做路径和模式检查
- 宿主暂时不承诺 machine-checkable structure

## Example

```toml
version = "0.1"
profile = "generic"

[targets.long_term_memory]
mode = "single"
paths = ["memory/long-term.md"]
structured = false

[targets.daily_memory]
mode = "pattern"
paths = ["notes/daily/YYYY-MM-DD.md"]
structured = false

[targets.reusable_lessons]
mode = "single"
paths = ["memory/reusable-lessons.md"]
structured = true

[targets.proactive_state]
mode = "single"
paths = ["memory/proactive-state.md"]
structured = true

[targets.working_buffer]
mode = "single"
paths = ["memory/working-buffer.md"]
structured = true
```

## Split Adapter Example

```toml
version = "0.1"
profile = "openclaw"

[targets.proactive_state]
mode = "split"
paths = ["~/proactivity/memory.md", "~/proactivity/session-state.md"]
structured = true
```

对于 `split` adapter，checker 会把“至少一个 canonical current-state slice 通过 schema 校验”视为通过条件。

## Checker Behavior

`check-memory-host.py` 的顺序是：

1. 先找 `memory-governor-host.toml`
2. 如果存在，就按 manifest 检查
3. 如果不存在，才回退到 reference profile auto-detect

这意味着 manifest 优先级高于目录猜测。

## Recommended Practice

- reference profile 宿主也可以写 manifest
- custom host 强烈建议写 manifest
- `adapter-map.md` 可以继续保留给人看
- `memory-governor-host.toml` 负责给工具读
