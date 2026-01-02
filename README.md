# Claude Code Global Configuration

My personal Claude Code configuration implementing the AGENTICSET methodology - a comprehensive agentic system setup synthesized from best practices across multiple repositories.

## Overview

This configuration provides:
- **Streamlined workflows** via commands and skills
- **Progressive disclosure** through skill hierarchy
- **Enhanced automation** via intelligent hooks
- **Safety guardrails** for git operations and sensitive files
- **Context injection** for thinking modes and autonomy levels

## Structure

```
.claude/
├── CLAUDE.md              # Project context and core principles
├── settings.json          # Permissions, hooks, and environment
├── commands/              # Executable command files
│   ├── workflow/          # Session and prompt management
│   ├── thinking/          # Problem-solving frameworks
│   ├── development/       # Debugging and review
│   └── meta/              # Self-improvement
├── hooks/                 # Event-driven automation
│   ├── session-initializer.py
│   ├── prompt-context-injector.py
│   ├── git-safety-net.py
│   ├── post-edit-format.py
│   └── ...
└── skills/                # Knowledge base (progressive disclosure)
    ├── core/              # Foundational workflows
    ├── language/          # Language-specific patterns
    ├── infrastructure/    # DevOps and deployment
    └── expertise/         # Advanced specializations
```

## Features

### Autonomy Modes
Trigger different interaction styles:
- `autonomous` / `handle it` → End-to-end execution
- `step by step` / `supervise` → Explain before executing
- Default → Collaborative with decision checkpoints

### Extended Thinking
Request deeper reasoning:
- `ultrathink` → Maximum depth analysis
- `think hard` → Complex problem solving
- `think` → Careful reasoning

### Automated Hooks
- **Session initialization** - Loads previous context
- **Context injection** - Detects thinking/autonomy triggers
- **Git safety** - Protects sensitive files and branches
- **Auto-formatting** - Runs Black, Prettier on edits
- **Quality gates** - Validates subagent outputs

### Progressive Skill Loading
Skills organized in 4 tiers for efficient context usage:
1. **Core** - Essential workflows (git, testing)
2. **Language** - Stack-specific patterns (Python, TypeScript, PowerShell)
3. **Infrastructure** - DevOps expertise (Docker, Kubernetes)
4. **Expertise** - Advanced topics (API design)

## Setup

1. Clone this repo to `~/.claude/`
2. Install dependencies: Python 3.x, Black (optional), Prettier (optional)
3. Ensure gh CLI is authenticated for GitHub operations
4. Restart Claude Code to load new configuration

## References

Based on AGENTICSET methodology synthesizing:
- TÂCHES CC Resources
- Superpowers plugin suite
- DAIR.AI Prompt Engineering Guide
- wshobson/agents patterns
- Claude-Flow architecture

## License

Personal configuration - use and adapt as needed.
