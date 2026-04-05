# Memory Governor 0.2.6-beta

This beta focuses on repository organization and maintainer workflows.

## What Changed

- Added a maintainer-facing `tests/` suite for validator, host checker, and bootstrap flows
- Added more complex host fixtures for split adapters, directory/pattern targets, unknown targets, and missing fallbacks
- Reorganized maintainer material into `dev/`
- Moved per-version release notes into `releases/`
- Clarified in the README which directories are runtime package content vs maintainer-only material

## Why

The goal is to make the public repository easier to understand:

- installers can focus on the runtime package
- maintainers can find tests and planning material without confusing them with installation requirements
