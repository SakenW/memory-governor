# Memory Governor 0.2.7

## Highlights

- separated the ClawHub publish bundle from maintainer-only repository material
- added `publish/clawhub/` as a runtime-only publish target
- added `scripts/refresh-clawhub-package.sh` to rebuild the publish bundle
- cleaned up maintainer docs to use grouped bilingual sections
- converted `SKILL.md` to pure English for cleaner ClawHub rendering

## Why This Release Exists

This release improves packaging and presentation quality rather than changing the governance model itself.

It makes the public skill easier to publish and easier to read:

- ClawHub can now publish from a runtime-only directory
- maintainer material such as `tests/`, `dev/`, and `releases/` no longer needs to ship with the public skill
- the primary skill description now renders in English only

## Publishing Note

Recommended publish flow:

```sh
cd /Users/saken/Projects/OpenClaw/Skills/memory-governor
scripts/refresh-clawhub-package.sh
cd publish/clawhub
clawhub publish .
```

Do not publish from the repository root if you want to avoid shipping maintainer material.
