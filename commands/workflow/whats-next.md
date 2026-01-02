---
description: Generate context handoff document for session continuity
allowed_tools:
  - Read
  - Glob
  - Grep
  - Bash(git:*)
---

# /whats-next

## Purpose
Create a handoff document capturing current state and next steps.

## Output Format

# whats-next.md

## Current State
- Last completed: [task description]
- Branch: [git branch]
- Tests passing: [yes/no]

## Next Steps
1. [Immediate next task]
2. [Following task]
3. [After that]

## Key Context
- Decision: [important architectural choice]
- Blocker: [any issues to resolve]
- Reference: [relevant file paths]

## Resume Command
@whats-next.md Continue from [specific point]

## Process
1. Check git status and branch
2. Review recent commits
3. Identify incomplete work
4. Document context for handoff
