# Scenario 05: Interrupted Recovery

## Setup

A task is interrupted after:

- current state was updated
- several breadcrumbs were written
- one recurring mistake pattern has just been noticed but not yet proven

## What To Evaluate

- Does the extra candidate layer improve later recovery?
- Or does it add another layer to read without helping the next move?
- Can the system still preserve the rule that `proactive_state` remains canonical current truth?

## Desired Tension

This scenario tests whether the proposed layer helps the actual workflow instead of only making the model look cleaner.
