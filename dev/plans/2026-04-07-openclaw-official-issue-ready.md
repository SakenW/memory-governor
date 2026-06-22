# GitHub Discussion / Issue Draft

## Title

Proposal: explicit correction staging for OpenClaw memory after Dreaming

## Body

Before Dreaming, I was using `memory-governor` to explore a broader memory-hardening problem:

- what should count as memory
- where it should go
- what should remain short-term
- what should be allowed to harden into durable rules

The 4.5 Dreaming update changes that picture in a good way.

OpenClaw Dreaming already improves background consolidation from short-term memory into long-term memory.
That means a meaningful part of the original problem is now better handled by core, especially `daily_memory -> long_term_memory`.

What still feels missing is a lightweight layer for explicit corrections and first-sighting emerging lessons:

- things the user corrected once
- things that look reusable, but are not yet proven
- things that should not harden directly into durable rules

Because of that, I do **not** think the whole `memory-governor` skill should be absorbed into core as-is.
Instead, I think the Dreaming update makes the upstream ask smaller and clearer:

- keep Dreaming as the consolidation engine
- consider whether a few explicit correction-staging ideas are still worth absorbing upstream

I built `memory-governor` as a community skill to explore that remaining gap.

So this proposal is not "please replace Dreaming."
It is:

- Dreaming solved a meaningful part of the old problem
- the remaining gap is now narrower
- explicit correction staging may still be a useful missing piece

## The Gap

There is still an awkward space between:

- same-day memory / short-term traces
- reusable durable lessons
- system-level rules

Without an explicit staging layer, explicit corrections tend to become either:

- over-hardened too early
- or buried inside daily notes

Dreaming is already strong at background consolidation and promotion from short-term memory. That is a different job from explicit correction hardening.

## Proposal

### 1. Add an explicit correction staging concept

Something like `learning_candidates`:

- explicit corrections go here first
- first-sighting emerging lessons go here first
- promotion into reusable lessons stays manual or review-gated

This helps distinguish:

- "the user corrected this once"
- from
- "this should now be treated as durable reusable guidance"

### 2. Split promotion authority clearly

Recommended split:

- Dreaming-preferred:
  `daily_memory -> long_term_memory`
- Manual-only:
  `learning_candidates -> reusable_lessons`
  `reusable_lessons -> system/tool/system-style rules`

This avoids duplicate promotion authority and keeps Dreaming focused on consolidation.

### 3. Clarify Dreaming artifact boundaries

It would help to make the following explicit in docs or integration guidance:

- `DREAMS.md` is a Dreaming artifact
- `memory/.dreams/` is Dreaming engine state
- neither should be treated as a standard memory target class

That would reduce confusion for advanced users building host-specific memory workflows, plugins, and skills.

## Why This Complements Dreaming

Dreaming is already good at:

- background consolidation
- multi-stage ranking
- explainable promotion from short-term memory

This proposal targets a different gap:

- explicit correction staging
- manual hardening boundaries
- preventing one-off corrections from becoming durable truth too early

In short:

- Dreaming handles background memory consolidation
- explicit correction staging handles manual hardening

## What This Proposal Does Not Ask For

This is **not** asking OpenClaw to:

- absorb the entire `memory-governor` skill into core
- replace Dreaming with a manual review system
- model `DREAMS.md` as a user-facing target class
- let background consolidation write directly into system-governance files

## Community Reference

I have a working community implementation in `memory-governor` that currently tests:

- explicit correction staging
- candidate review workflow
- Dreaming-vs-manual promotion authority split
- explicit `DREAMS.md` / `memory/.dreams/` boundary guidance

Happy to share a minimal contract-level diff if that is useful.

## Smallest Potential Upstream Pieces

If only the smallest parts are worth considering, the best candidates seem to be:

1. explicit correction staging
2. clearer Dreaming vs manual promotion authority
3. clearer Dreaming artifact boundary guidance
