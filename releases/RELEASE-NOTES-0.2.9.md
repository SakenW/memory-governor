# Memory Governor 0.2.9

## Highlights

- added `references/dreaming-integration.md` to document how `memory-governor` should coexist with OpenClaw Dreaming
- clarified that Dreaming is an optional consolidation engine, not a new target class and not a replacement for `learning_candidates`
- defined `DREAMS.md` and `memory/.dreams/` as engine-owned artifacts rather than normal host memory targets
- made `daily_memory -> long_term_memory` Dreaming-preferred when Dreaming is enabled, while keeping candidate review and system-rule hardening manual-only
- updated startup and recovery read-order guidance so `DREAMS.md` stays out of the default recall path
- added Dreaming-aware capture guidance so explicit corrections continue to stage in `learning_candidates` instead of being dumped into daily memory

## Why This Release Exists

`0.2.8` introduced the candidate layer and staged correction flow.

That made one boundary much more important: how this governance kernel should relate to OpenClaw Dreaming.

Without a clear split, hosts can drift into duplicated authority:

- daily notes are manually promoted into long-term memory
- Dreaming also promotes from the same short-term signals
- explicit corrections get mixed into daily traces and hardened indirectly

`0.2.9` is a documentation and contract release that closes that gap.

## Core Decision

The recommended split is now explicit:

- `memory-governor` owns capture governance, routing, candidate staging, and manual hardening boundaries
- Dreaming owns background consolidation from short-term memory into long-term memory

In practical terms:

- Dreaming-preferred: `daily_memory -> long_term_memory`
- Manual-only: `learning_candidates -> reusable_lessons`
- Manual-only: `reusable_lessons -> system_rules / tool_rules / governance files`

## Scope Boundary

This release does not add:

- new target classes for Dreaming stages
- duplicated Dreaming scoring logic inside `memory-governor`
- automatic system-rule generation from Dreaming artifacts

It only makes the contract sharper.

## Functional Summary

`0.2.9` now gives hosts explicit guidance for Dreaming-aware operation:

- Dreaming is optional and host-owned
- Dreaming artifacts are not standard memory targets
- startup and recovery should not read `DREAMS.md` by default
- explicit corrections still enter `learning_candidates`
- same-day events and recurring short-term signals can stay in `daily_memory`
- manual governance remains the only path into system-level rule files
