# Scenario 03: One-Off External Failure

## Setup

A third-party service times out once.

The next retry works without any workflow change.

## What To Evaluate

- Does the system correctly keep this out of durable memory?
- Would a candidate layer accidentally become a trash bucket for random failures?
- Is the exclusion boundary still clear after adding more memory structure?

## Desired Tension

This scenario is mainly about noise control.
