# Memory Governor 0.2.8

## Highlights

- added `learning_candidates` as a staged capture layer for corrections and emerging lessons
- added `references/correction-pipeline.md` to define the correction-to-candidate-to-rule flow
- updated routing, promotion, read-order, and skill integration docs to treat candidate capture as a first-class contract
- taught the checker and validator to recognize `learning_candidates` as a standard validated target
- added a lightweight review helper for keep / promote / discard passes on `learning_candidates`

## Why This Release Exists

`0.2.7` cleaned up packaging and public presentation.

`0.2.8` is the minimal mechanism follow-up:

- it adds a candidate layer
- it avoids hardening single corrections too early
- it defines a lightweight promotion path and review helper without introducing automation-first behavior

## Scope Boundary

This release does not yet require:

- mandatory host adoption of automated sampling
- a full candidate-layer orchestration system

The goal is smaller:

- prove that staged correction capture is useful before the toolchain depends on it
