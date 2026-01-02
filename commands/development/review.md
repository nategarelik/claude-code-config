---
description: Code review workflow
arguments:
  - name: scope
    description: What to review (file, PR, changes)
    required: false
allowed_tools:
  - Read
  - Glob
  - Grep
  - Bash(git:*)
---

# /review

## Purpose
Two-stage code review for quality assurance.

## Process
**Stage 1: Spec Compliance**
- Does it meet requirements?
- Are acceptance criteria satisfied?
- Is functionality complete?

**Stage 2: Code Quality**
- Is it maintainable?
- Are there potential bugs?
- Is it well-tested?
- Does it follow conventions?

## Output
Review summary with specific, actionable feedback.
