# Memory Governor Handoff

Date: 2026-04-05

## Current State

- Working repository:
  `/Users/saken/Projects/OpenClaw/Skills/memory-governor`
- Current local version:
  `0.2.7`
- Main goal of the latest work:
  clean up public presentation, split ClawHub publishing from maintainer material, and make the public `SKILL.md` English-only

## What Was Completed

### 1. ClawHub publish bundle was separated from the development repository

Added:

- `publish/clawhub/`
- `publish/README.md`
- `scripts/refresh-clawhub-package.sh`

Intent:

- publish from `publish/clawhub/`
- stop shipping `tests/`, `dev/`, and `releases/` to ClawHub

Recommended publish flow:

```sh
cd /Users/saken/Projects/OpenClaw/Skills/memory-governor
scripts/refresh-clawhub-package.sh
cd publish/clawhub
clawhub publish /Users/saken/Projects/OpenClaw/Skills/memory-governor/publish/clawhub --slug memory-governor --name "Memory Governor" --version 0.2.7
```

### 2. Public skill description was cleaned up

Completed:

- root `SKILL.md` converted to pure English
- `publish/clawhub/SKILL.md` refreshed and verified to be English-only

This was done because the mixed English/Chinese rendering looked awkward on ClawHub.

### 3. Maintainer docs were reformatted

These files were changed from line-by-line mixed language formatting to grouped sections:

- `dev/README.md`
- `dev/eval-lab/README.md`
- `dev/plans/2026-04-05-memory-governor-testing-strategy.md`
- `releases/README.md`

## What Is Still In Progress

The following local changes exist and are not yet committed:

- `CHANGELOG.md`
- `README.md`
- `SKILL.md`
- `VERSION`
- `publish/clawhub/CHANGELOG.md`
- `publish/clawhub/README.md`
- `publish/clawhub/SKILL.md`
- `publish/clawhub/VERSION`
- deletion of `releases/RELEASE-NOTES-0.2.6-beta.md`
- new file `releases/RELEASE-NOTES-0.2.7.md`

## ClawHub Publish Status

Important: GitHub and ClawHub are not currently in the same state.

### What happened

- The package was prepared correctly from `publish/clawhub/`
- `clawhub whoami` succeeded
- local path detection and `SKILL.md` validation issues were resolved
- explicit publish command reached the remote preparation stage:

```sh
clawhub publish /Users/saken/Projects/OpenClaw/Skills/memory-governor/publish/clawhub \
  --slug memory-governor \
  --name "Memory Governor" \
  --version 0.2.7
```

### Current blocker

ClawHub still failed with:

```text
- Preparing memory-governor@0.2.7
Timeout
```

So the current reading is:

- local package is ready
- publish command is correct
- remaining problem is probably ClawHub service-side timeout

Do not treat this as a local packaging bug unless the remote behavior changes.

## Product / Design Status

The current `0.2.7` work is a packaging and presentation upgrade, not a mechanism upgrade.

It includes:

- cleaner public presentation
- English-only `SKILL.md`
- publish-only directory
- clearer separation between runtime and maintainer material

It does **not** yet include the proposed candidate-layer improvements:

- no `learning_candidates` target class
- no `references/correction-pipeline.md`
- no promotion thresholds
- no correction staging layer
- no sampling-boundary integration guidance

## Strategic Decision

The latest decision was:

- do **not** build the full “extreme” candidate-layer system immediately
- do it later, in a lighter experimental form

Recommended next mechanism step:

### 0.2.8-lite

Add only the minimum experimental candidate-layer pieces:

1. add `learning_candidates` to `SKILL.md`
2. add `references/correction-pipeline.md`
3. update `references/memory-routing.md`
4. update `references/promotion-rules.md`
5. update `references/skill-integration.md`

Do **not** immediately require:

- checker support
- manifest enforcement
- generic-host mandatory adoption
- fully automated sampling logic

The current recommendation is:

**prove the candidate layer is useful before making the toolchain depend on it**

## Suggested Next Actions

Pick one of these two paths next:

### Path A: finish the release state

Use this if the priority is public packaging:

1. commit the current `0.2.7` local changes
2. push GitHub
3. retry ClawHub publish from `publish/clawhub/`
4. verify whether the ClawHub page updates despite prior timeout behavior

### Path B: start mechanism work

Use this if the priority is product evolution:

1. keep `0.2.7` as the packaging cleanup release
2. start `0.2.8-lite`
3. implement only the five contract-level changes listed above
4. do not expand into checker or manifest support yet

## Quick Resume Notes

- Repo is already separated into runtime vs maintainer material
- `SKILL.md` should stay English-only for ClawHub presentation
- `publish/clawhub/` is now the only correct publish root
- ClawHub timeout is still unresolved
- candidate-layer work is intentionally deferred into a lighter future release
