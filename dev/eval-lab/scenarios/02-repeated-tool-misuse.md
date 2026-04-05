# Scenario 02: Repeated Tool Misuse

## Setup

The agent repeatedly uses the wrong command pattern for the same tool across two tasks.

After correction, the failure clearly stops recurring.

## What To Evaluate

- Does the current design route this cleanly enough?
- Does an experimental candidate layer reduce premature jumps into `tool_rules`?
- At what point does this feel solid enough to become a tool rule?

## Desired Tension

This scenario tests whether repetition is handled as evidence rather than noise.
