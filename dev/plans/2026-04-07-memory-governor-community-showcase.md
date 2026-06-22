# Showcase: a memory-governance layer that complements Dreaming

## Short Version

I built a community skill called `memory-governor` to solve a gap I kept feeling in advanced OpenClaw hosts.

Originally, that gap was broader:

- memory routing
- memory hardening
- correction handling
- durable-rule boundaries

But the 4.5 Dreaming update changed the shape of that problem in a good way.

Dreaming now covers a major part of the old gap:

- background consolidation from short-term memory into long-term memory

So `memory-governor` now feels less like "general memory governance" and more like a complement:

- Dreaming handles consolidation
- `memory-governor` focuses on explicit corrections, routing discipline, and safe hardening boundaries

The goal was not to replace Dreaming.
The goal was to complement it.

## What `memory-governor` Is

`memory-governor` is a governance kernel for memory-heavy agent systems.

It answers questions like:

- what should count as memory at all
- which target class something belongs to
- whether something should remain short-term
- whether it should first become a candidate lesson
- whether it is ready to harden into reusable guidance

It is not:

- a second-brain app
- a sync bus
- a universal knowledge manager
- a replacement for Dreaming

## The Main Idea

The core split looks like this:

- Dreaming:
  background consolidation from short-term signals into long-term memory
- `memory-governor`:
  capture rules, routing rules, explicit correction staging, and hardening boundaries

That led to a simple but useful division of labor:

- `daily_memory -> long_term_memory`
  Dreaming-preferred
- `learning_candidates -> reusable_lessons`
  manual review
- `reusable_lessons -> AGENTS / TOOLS / SOUL`
  manual hardening

## Why I Built It

The missing piece that still feels open after Dreaming is this:

some things are important enough to remember,
but not yet important enough to become durable truth.

Examples:

- the user corrected one reply
- a pattern appeared once and might repeat
- a workflow lesson looks promising but is still under evidence collection

Without a staging layer, these tend to become either:

- over-hardened too early
- or lost inside daily notes

## What It Adds

The most important concept is:

- `learning_candidates`

This is a low-commitment layer for:

- explicit corrections
- first-sighting emerging lessons
- not-yet-proven reusable guidance

It also adds:

- `memory type -> target class -> adapter / fallback`
- candidate review workflow (`keep / promote / discard`)
- host manifest guidance
- host checker and validator tools
- Dreaming boundary rules so `DREAMS.md` is not mistaken for a normal memory layer

## What I Think Could Be Useful to OpenClaw

I do **not** think the whole skill should simply be absorbed into core.

But I do think three ideas are promising:

1. explicit correction staging
2. Dreaming-vs-manual promotion authority split
3. clearer official boundary for `DREAMS.md` and `memory/.dreams/`

## Who This Is For

This skill is probably useful if your host already has:

- multiple memory layers
- multiple skills that write memory
- optional adapters that are starting to drift
- a need for one shared memory contract

It is probably overkill for a tiny single-agent setup.

## Current Status

The project currently exists as a community skill and reference implementation.

I am interested in:

- feedback from advanced OpenClaw users
- discussion about whether explicit correction staging should exist in official memory docs or behavior
- learning whether this governance split feels useful in real hosts that already use Dreaming

## One-Line Pitch

`memory-governor` is a community memory-governance layer for OpenClaw-style hosts: it does not replace Dreaming, it complements Dreaming by making correction staging, routing, and hardening boundaries explicit.
