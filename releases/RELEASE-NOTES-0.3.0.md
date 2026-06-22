# Memory Governor 0.3.0

## Highlights

- added `references/compiled-surfaces.md` as the canonical inventory of official OpenClaw runtime / compiled surfaces that are NOT memory target classes
- aligned the kernel with the OpenClaw 2026.6.x memory stack instead of stopping at the April 2026 / 4.5 line
- covered People Wiki (2026.4.29), Memory Wiki Claim/Evidence, Memory Palace, Imported Insights, and Provenance Views as downstream compiled surfaces
- added governance rules for imported content (Imported Insights / cross-platform imports): stage through `learning_candidates`, do not jump to canonical truth
- added governance rules for entity memory: capture entity facts into `long_term_memory` / `project_facts` / `learning_candidates`, never directly into a `people/` surface or Person Card
- added a scope / privacy boundary that complements Active Memory Filters (`allowedChatIds` / `deniedChatIds`): record scope at capture time so compiled surfaces cannot widen it
- added a Multi-Agent Writer Rule covering coordinated agents on Workboard (2026.6.1+)
- added Skill Workshop (2026.6.1+) versioning guidance: a skill's `Memory Contract` should version and roll back with the skill
- cited official stale-REM filtering, partial-recall-on-timeout, and Memory Wiki SQLite migration as validation of the existing boundary

## Why This Release Exists

`0.2.10` aligned the kernel with Dreaming, Active Memory, and Memory Wiki.

That alignment was correct but incomplete. Between April 2026 and the 2026.6.x line, OpenClaw kept expanding the memory stack:

- 2026.4.29 added People Wiki, Person Cards, Relationship Graphs, Provenance Views, and Active Memory Filters
- later builds added Imported Insights and Memory Palace
- 2026.6.1 added Skill Workshop (governed skill lifecycle) and Workboard (multi-agent coordination)

Each of these is useful, but none of them is governed by the host's memory contract. Without an explicit boundary, two failure modes appear:

- skills start writing directly into `people/` pages, Claim artifacts, or Memory Palace tabs, treating compiled surfaces as capture layers
- imported or cross-chat content surfaces everywhere as canonical truth before it has been verified

`0.3.0` is a documentation and boundary release that closes those gaps.

## Core Decision

The 9 standard target classes are unchanged. No new target class was introduced.

Instead, every new official surface is declared a downstream compiled / runtime view, not a capture layer:

- capture into target classes first
- let official engines compile, recall, navigate, and index downstream
- canonical durable truth still lives in the target classes

This is the same stance the kernel already took for `DREAMS.md`, now extended consistently to all newer surfaces.

## Five Governance Gaps Closed

These are the dimensions OpenClaw does not govern for the host.

### 1. Imported content

Imported Insights are unverified by this host. They should stage through `learning_candidates`, not jump straight into `long_term_memory`, `reusable_lessons`, or system-level rules.

### 2. Entity memory capture

Entity facts are captured upstream into `long_term_memory` (stable facts), `project_facts` (project-scoped relationships), or `learning_candidates` (unverified inferences). People Wiki then compiles them. Skills must not write Person Cards or `people/` pages directly.

### 3. Scope / privacy boundary

Active Memory Filters control what may be recalled where. That is a recall-time control. Capture-time governance still records scope on the target class entry, otherwise a compiled surface can widen a scoped memory into a global view. A project-scoped fact compiled into a global People Wiki page is a leak, even if the target class was correct.

### 4. Multi-agent writers

Workboard lets multiple agents coordinate. Multi-writer governance now extends from skill-level to agent-level: coordinated agents should not each harden unconfirmed intermediate state, and shared layers (`long_term_memory`, `reusable_lessons`, `system_rules`) should keep a single canonical copy.

### 5. Skill Workshop versioning

A skill's `Memory Contract` should version and roll back with the skill. When a skill rolls back, rules it wrote into `system_rules` / `tool_rules` must be checked for consistency, otherwise orphan rules survive the rollback.

## Scope Boundary

This release does not add:

- a 10th target class (that would compete with official compiled surfaces)
- capture logic for People Wiki, Memory Palace, or Imported Insights
- automatic scope enforcement logic (scope is recorded at capture, enforcement remains the runtime's job)
- integration with Skill Workshop plumbing (only the contract-level guidance)

It only sharpens the boundary.

## Functional Summary

`0.3.0` now gives hosts explicit guidance for the 2026.6.x era:

- every official runtime / compiled surface is downstream of the memory contract
- imported and cross-platform content stages through `learning_candidates`
- entity facts are captured into target classes, then compiled by People Wiki
- scoped memories record scope at capture time
- coordinated agents on Workboard follow a Multi-Agent Writer Rule
- skills version and roll back their `Memory Contract` together with the skill
- the existing Dreaming, Active Memory, and Memory Wiki boundaries are unchanged

## Files

New:

- `references/compiled-surfaces.md`

Changed:

- `SKILL.md`
- `README.md`
- `VERSION`
- `CHANGELOG.md`
- `references/read-order.md`
- `references/exclusions.md`
- `references/stateful-targets.md`
- `references/skill-integration.md`
- `references/dreaming-integration.md`
- `references/host-profiles.md`
- `tests/test_contract_docs.py`

Publish bundle `publish/clawhub/` has been regenerated from source.

## Verification

- 44 tests pass
- `publish/clawhub/` is in sync with the source tree across all 23 reference files
