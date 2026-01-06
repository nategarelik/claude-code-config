# System Prompt Patching for Claude Code

## Overview

YK's claude-code-tips demonstrates a 52.5% reduction in system prompt overhead (~11k tokens saved) through strategic patching of Claude Code's internal system prompt. This is a high-value optimization for context efficiency.

## Challenge on Windows

**Claude Code on Windows is distributed as a PE32+ executable** (`C:\Users\Nate2\.local\bin\claude.exe`), not as a Node.js application with accessible JavaScript bundles.

### YK's Implementation (Unix/Mac)

YK's approach works on Unix/Mac systems where:
- Claude Code runs as Node.js source or accessible bundles
- `patch-cli.js` can find and modify system prompt text
- Files are located in predictable paths (e.g., `~/.local/share/claude-code/`)
- Regex patterns match minified variable names (e.g., `${n3}`)

### Windows Constraints

On Windows:
- Binary executable (cannot directly edit bundled JS)
- System prompt embedded in compiled binary
- No accessible JavaScript source to patch
- Requires different approach (decompilation, hex editing, or runtime interception)

## Alternative Approaches for Windows

### Option 1: Runtime Interception (Recommended)

Create a Python hook that intercepts and modifies the system prompt at runtime:

**Pros:**
- No binary modification required
- Survives Claude Code updates
- Can be version-controlled
- Follows AGENTICSET hook architecture

**Cons:**
- Requires hooking at the right interception point
- May not be exposed via current hook system
- Needs investigation of hook capabilities

**Implementation Path:**
1. Investigate if `SessionStart` or similar hooks receive system prompt
2. Create `system-prompt-optimizer.py` hook
3. Strip verbose examples, redundant instructions
4. Inject optimized version

### Option 2: Environment Variable Injection

If Claude Code supports environment-based prompt customization:

```powershell
# In PowerShell profile or settings.json
$env:CLAUDE_SYSTEM_PROMPT_OVERRIDE = "path/to/optimized-prompt.txt"
```

**Pros:**
- Clean, declarative approach
- Easy to version control
- No binary modification

**Cons:**
- Only works if Claude Code exposes this capability
- Needs API documentation verification

### Option 3: MCP Server Wrapper

Create an MCP (Model Context Protocol) server that:
1. Intercepts Claude API calls
2. Modifies system prompt before sending to API
3. Returns responses unchanged

**Pros:**
- Works at API layer (platform-independent)
- Can be shared across systems
- Follows Claude ecosystem patterns

**Cons:**
- Complex implementation
- May introduce latency
- Requires MCP server development expertise

### Option 4: WSL Bridge

Run YK's Unix-based patching tools in WSL:

**Pros:**
- Use YK's proven tooling
- Community support and updates

**Cons:**
- Requires WSL setup
- Cross-filesystem complexity
- Must patch WSL version of Claude Code separately

### Option 5: Request Official Feature

File feature request with Anthropic for:
- Documented system prompt customization API
- Environment variable support
- Hook exposure for system prompt modification

**Pros:**
- Official, supported approach
- Benefits entire community
- No workarounds needed

**Cons:**
- Timeline uncertain
- May not align with product roadmap
- Depends on Anthropic priorities

## Workaround: Context Optimization Without Patching

While waiting for a Windows-compatible patching solution, achieve similar goals through:

### 1. Aggressive CLAUDE.md Minimization
- Keep CLAUDE.md under 500 tokens (currently 43 lines ≈ 300 tokens)
- Remove all redundant instructions
- Use skills instead of inline documentation

### 2. Skill-Based Knowledge Loading
- Progressive disclosure (already implemented)
- Load-on-demand vs. always-present
- Four-tier hierarchy reduces baseline overhead

### 3. Clone/Half-Clone Patterns
- Install and use dx plugin commands (✅ already done)
- `/half-clone` preserves recent context, sheds old baggage
- Strategic conversation branching

### 4. Manual Compaction Strategy
- Use `/compact` proactively (not reactively)
- Create handoff documents at 50-60% context usage
- Fresh sessions for new topics

### 5. Model Selection Optimization
- Haiku for simple operations (smaller prompts accepted)
- Sonnet for standard work (current default)
- Opus only for complex architectural decisions

## Estimated Impact

**With Patching (YK's approach):**
- System prompt: ~20k → ~9k tokens (-55%)
- Effective context: 180k → 191k (+6%)
- ROI: High (one-time setup, permanent gains)

**Without Patching (Optimization strategies):**
- CLAUDE.md: Minimal (already optimized at ~300 tokens)
- Skills: Progressive disclosure saves ~2-5k tokens/conversation
- Half-clone: 30-50% context reduction per branch
- Manual compaction: Prevents 80%+ context usage scenarios
- Combined ROI: Medium (requires discipline, smaller gains)

## Recommendation

**Phase 1 (Immediate):**
1. ✅ Install dx plugin for `/half-clone`, `/clone`, `/handoff`
2. ✅ Maintain minimal CLAUDE.md (43 lines)
3. ✅ Use progressive disclosure skill hierarchy
4. 📋 Document handoff patterns in workflows

**Phase 2 (Investigation - 1-2 weeks):**
1. Research Claude Code hook capabilities for system prompt access
2. Test MCP server interception feasibility
3. Check for official environment variable support
4. Engage with Anthropic community on Windows patching

**Phase 3 (Implementation - if feasible):**
1. Build runtime interception hook if API available
2. OR create MCP server if hooks insufficient
3. OR file feature request if no current path exists
4. Document solution for community sharing

## Tracking

- **Estimated savings**: 11k tokens (55% of system prompt)
- **Complexity**: High (Windows binary limitations)
- **Priority**: Medium (workarounds provide 60-70% of benefit)
- **Status**: Documented, pending investigation

## References

- YK's system-prompt README: https://github.com/ykdojo/claude-code-tips/tree/main/system-prompt
- UPGRADING.md guide: Maintaining patches across versions
- patch-cli.js: Regex-based bundle modification tool
- Our issue: Windows PE executable vs. Unix Node.js source

## Next Steps

1. Test dx plugin `/handoff` command effectiveness
2. Experiment with `/half-clone` at different context percentages
3. Monitor context usage patterns with new aliases (c, ch, cc)
4. Investigate Claude Code extension API documentation
5. Engage with superpowers-developing-for-claude-code plugin for hook insights
