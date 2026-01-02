---
description: Generate optimized prompts for sub-agent execution
arguments:
  - name: task
    description: Task description to create prompt for
    required: true
allowed_tools:
  - Read
  - Glob
  - Grep
---

# /create-prompt

## Purpose
Generate a detailed, context-rich prompt for executing a task in a fresh sub-agent context.

## Process
1. Analyze the task requirements
2. Gather relevant file paths and context
3. Structure a clear, actionable prompt
4. Include necessary constraints and success criteria

## Output
A prompt ready to be passed to a sub-agent for execution.

## Example
/create-prompt "implement user authentication with JWT"
