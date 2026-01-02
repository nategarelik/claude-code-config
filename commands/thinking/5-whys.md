---
description: Root cause analysis via iterative questioning
arguments:
  - name: problem
    description: Problem to drill into
    required: true
allowed_tools:
  - Read
  - Glob
  - Grep
---

# /5-whys

## Purpose
Identify root cause by asking "why" iteratively until fundamental cause emerges.

## Process
1. State the problem clearly
2. Ask: Why did this happen? (Answer 1)
3. Ask: Why did [Answer 1] happen? (Answer 2)
4. Continue until root cause identified (typically 5 iterations)
5. Propose solution addressing root cause

## Output
Chain of causation leading to root cause, plus proposed solution.
