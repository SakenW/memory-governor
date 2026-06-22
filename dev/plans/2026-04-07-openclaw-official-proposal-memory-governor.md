# Proposal: explicit correction staging for OpenClaw memory

## Summary

OpenClaw Dreaming already improves background consolidation from short-term memory into long-term memory.

What still feels missing is a lightweight layer for explicit corrections and first-sighting emerging lessons:

- things the user corrected once
- things that look reusable, but are not yet proven
- things that should not harden directly into durable rules

This proposal does **not** ask OpenClaw to adopt the whole `memory-governor` skill.
It proposes three focused ideas that seem upstreamable:

1. an explicit correction staging layer such as `learning_candidates`
2. a clear promotion-authority split between Dreaming and manual rule hardening
3. an explicit boundary that `DREAMS.md` and `memory/.dreams/` are engine-owned artifacts, not target classes

## Problem

Today there is still a gap between:

- same-day memory and short-term traces
- reusable durable lessons
- system-level rules

Without a staging layer, explicit corrections tend to become either:

- over-hardened too early
- or lost inside daily notes

Dreaming is strong at background consolidation and promotion from short-term memory, but it is solving a different problem from explicit correction hardening.

## Proposal

### 1. Add an explicit correction staging concept

Introduce a low-commitment staging concept, such as `learning_candidates`, with these default rules:

- explicit corrections go here first
- first-sighting emerging lessons go here first
- promotion into reusable lessons stays manual or review-gated

This makes it easier to distinguish:

- "the user corrected this once"
- from
- "this should now be treated as a durable reusable rule"

### 2. Split promotion authority clearly

Recommended default split:

- Dreaming-preferred:
  `daily_memory -> long_term_memory`
- Manual-only:
  `learning_candidates -> reusable_lessons`
  `reusable_lessons -> system/tool/system-style rules`

This keeps Dreaming focused on background consolidation and prevents duplicate promotion authority.

### 3. Make Dreaming artifacts explicit engine-owned boundaries

Clarify in docs and integration guidance that:

- `DREAMS.md` is a Dreaming artifact
- `memory/.dreams/` is Dreaming engine state
- neither should be treated as a standard memory target class

This reduces confusion for advanced users building plugins, skills, or host-specific memory workflows.

## Why This Complements Dreaming

Dreaming is already good at:

- background consolidation
- multi-stage ranking
- explainable promotion from short-term memory

This proposal targets a different gap:

- explicit correction staging
- manual review before hardening
- keeping one-off corrections from becoming durable truth too early

In short:

- Dreaming handles background memory consolidation
- correction staging handles explicit correction hardening

These two ideas fit together rather than compete.

## What This Proposal Does Not Ask For

This proposal does **not** ask OpenClaw to:

- absorb the entire `memory-governor` skill into core
- replace Dreaming with a manual review system
- model `DREAMS.md` as a user-facing target class
- let background consolidation write directly into system-governance files

## Why It May Be Worth Considering

Potential benefits:

- lower false hardening from one-off corrections
- cleaner separation between observed correction and durable rule
- clearer promotion authority for advanced hosts
- better explanation for users who want both Dreaming and explicit rule governance

## Community Implementation

I have a working community implementation in `memory-governor` that currently tests these ideas as a governance layer:

- explicit correction staging
- candidate review workflow
- Dreaming boundary rules
- promotion-authority split

The intent is not to upstream the whole skill as-is, but to share a tested community pattern that may help shape core memory behavior.

## Most Upstreamable Pieces

If OpenClaw only wanted to absorb the smallest useful parts, the best candidates appear to be:

1. explicit correction staging
2. Dreaming-vs-manual promotion authority split
3. explicit `DREAMS.md` / `memory/.dreams/` boundary guidance

## Suggested Ask

The most realistic ask is probably:

- discuss whether explicit correction staging belongs in memory-core docs or behavior
- clarify Dreaming artifact boundaries in official docs
- consider whether manual hardening should remain the default path for system-rule promotion
