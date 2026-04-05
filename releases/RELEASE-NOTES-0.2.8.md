# Memory Governor 0.2.8

## Highlights

- added `learning_candidates` as a staged capture layer for corrections and emerging lessons
- added `references/correction-pipeline.md` to define the correction-to-candidate-to-rule flow
- updated routing, promotion, read-order, and skill integration docs to treat candidate capture as a first-class contract
- taught the checker and validator to recognize `learning_candidates` as a standard validated target
- added a lightweight review helper for keep / promote / discard passes on `learning_candidates`
- added stronger candidate lifecycle guidance with structured entry fields such as `lifecycle_stage`, `evidence_count`, and `next_review`
- tightened host integration validation so declared host-entry and writer-contract files must contain real `memory-governor` / `Memory Contract` markers, not just exist
- added OpenClaw-style simulation tests to exercise fallback-only, external-adapter, partial-adapter, and invalid-schema environments

## Why This Release Exists

`0.2.7` cleaned up packaging and public presentation.

`0.2.8` is the minimal mechanism follow-up:

- it adds a candidate layer
- it avoids hardening single corrections too early
- it defines a lightweight promotion path and review helper without introducing automation-first behavior
- it starts turning readiness checks into something closer to real host wiring validation

## Scope Boundary

This release does not yet require:

- mandatory host adoption of automated sampling
- a full candidate-layer orchestration system
- automatic promotion into durable memory or rule files

The goal is smaller:

- prove that staged correction capture is useful before the toolchain depends on it
- make host integration validation strong enough that `Validated` means more than “files happen to exist”

## Functional Summary

`0.2.8` now ships a fairly complete governance package for staged memory handling:

- target-class contract for long-term memory, daily memory, candidate lessons, reusable lessons, stateful working context, project facts, and system/tool rules
- staged correction pipeline with a default route into `learning_candidates`
- candidate review workflow for keep / promote / discard
- candidate reviewer that can report stale entries, unstructured entries, lifecycle-stage distribution, and promotion-ready candidates
- structured frontmatter validation for key fallback targets
- manifest-driven host validation for generic hosts and OpenClaw-style hosts
- generic host bootstrap and example package
- OpenClaw-style environment tests that simulate how the checker behaves with local fallbacks and external adapters
