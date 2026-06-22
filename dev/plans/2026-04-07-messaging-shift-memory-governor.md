# Messaging Shift for Official Outreach

## Goal

Change the narrative from:

- "here is my community skill"

to:

- "here is the problem we were already trying to solve"
- "the 4.5 Dreaming update solved an important part of it"
- "here is the smaller remaining gap that may still be worth absorbing upstream"

## Before the Dreaming Update

Before Dreaming, `memory-governor` was trying to solve a broad memory-hardening problem:

- what should count as memory
- where it should go
- what should stay short-term
- what should be allowed to harden into durable guidance

One especially painful gray zone was:

- explicit corrections
- one-off but suspiciously reusable lessons
- patterns worth watching, but not yet worth canonizing

That is why the project introduced:

- target classes
- routing rules
- promotion rules
- `learning_candidates`

## What Changed After 4.5

The 4.5 Dreaming update solved a meaningful part of the old problem space.

Dreaming now clearly covers:

- background consolidation from short-term memory
- multi-stage reflection and ranking
- promotion into long-term memory
- explainability around why something promoted or did not promote

That means one large category is now better handled by core:

- `daily_memory -> long_term_memory`

So the right story is no longer:

- "general memory governance is missing"

The better story is:

- "Dreaming covered the consolidation side"
- "a narrower hardening-boundary gap still remains"

## The Remaining Gap

What still feels open is narrower and more specific:

- a user corrected something once
- a pattern appeared once and looks promising
- a lesson might be reusable, but is not yet proven

These are not ordinary short-term traces.
And they are risky to harden too early.

This is where `memory-governor` still adds something distinctive.

## The Right Ask

The ask should now be:

- not "please absorb `memory-governor`"
- but "the Dreaming update made the remaining gap smaller and clearer"
- and "here are the two or three ideas that still look upstreamable"

## Most Upstreamable Ideas

1. explicit correction staging
2. Dreaming-vs-manual promotion authority split
3. explicit `DREAMS.md` / `memory/.dreams/` boundary guidance

## Tone Guidance

### Avoid

- "I built a better memory system"
- "please merge my skill into core"
- "Dreaming still does not solve memory"

### Prefer

- "we were already working on memory hardening boundaries"
- "the Dreaming update solved a meaningful part of that problem"
- "that changed the shape of what still feels missing"
- "the remaining gap is now smaller and more focused"
- "these ideas appear complementary to Dreaming, not competitive with it"

## One-Paragraph Version

Before Dreaming, `memory-governor` was trying to solve a broad memory-hardening problem: what should count as memory, where it should go, and when it should be allowed to become durable guidance. After the 4.5 Dreaming update, a major part of that problem is now covered much better by core, especially background consolidation from daily and short-term memory into long-term memory. That changes the pitch. The interesting remaining gap is no longer "general memory management," but a narrower one: how to handle explicit corrections and first-sighting lessons that are important enough to stage, but not yet safe to harden into durable rules. That is the part where some of the `memory-governor` ideas may still be useful upstream.
