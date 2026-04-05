# Scenario 04: Project-Only Exception

## Setup

A project has a local exception rule:

- one specific repo needs a non-default release step

The rule should not become a global reusable lesson.

## What To Evaluate

- Does the system keep this in `project_facts`?
- Does a candidate layer incorrectly absorb it as a general lesson candidate?
- Is scope control still obvious to the operator?

## Desired Tension

This scenario tests whether "interesting" gets confused with "global".
