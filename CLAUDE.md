# CLAUDE.md - Global Configuration

## Project Context
- Name: Global User Config
- Type: Multi-domain development environment
- Stack: Python, TypeScript, Unity (C#), various frameworks

## Core Principles
1. Test-Driven Development (RED-GREEN-REFACTOR)
2. YAGNI (You Aren't Gonna Need It)
3. DRY (Don't Repeat Yourself)
4. Minimal viable implementation first

## Development Workflow
1. **Brainstorming** - Refine requirements through questions
2. **Design Approval** - Validate before implementation
3. **Implementation Planning** - Bite-sized tasks (2-5 min each)
4. **Subagent Execution** - Fresh context per task
5. **Code Review** - Two-stage (spec compliance, then quality)
6. **Verification** - Ensure actual fixes

## File Conventions
- Tests: `*_test.py` or `*.test.ts`
- Configs: `config/` directory
- Documentation: `docs/` directory

## Tool Restrictions
- Prefer built-in tools over external dependencies
- Document any required MCP servers
- Specify allowed/blocked operations

## Memory Hints
- Key decisions: Log in `docs/decisions/` or `~/.claude/memory-bank/`
- Architecture patterns: Reference documents in project root
- Known issues: Track in GitHub Issues or local `KNOWN_ISSUES.md`

## Autonomy Modes
- **Autonomous** (triggers: "autonomous", "handle it"): Execute end-to-end
- **Collaborative** (default): Check in at decision points
- **Supervised** (triggers: "step by step", "supervise"): Explain before executing

## Extended Thinking
Triggers: "think", "think hard", "ultrathink"
