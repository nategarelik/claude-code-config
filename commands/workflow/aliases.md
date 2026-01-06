---
name: aliases
description: Setup terminal aliases for Claude Code velocity
allowed_tools:
  - Read
  - Write
  - Bash
---

# Terminal Aliases Configuration

Based on YK's claude-code-tips productivity patterns, this guide helps you set up velocity-enhancing aliases.

## Recommended Aliases

### PowerShell (Windows)

Add to `$PROFILE` (usually `C:\Users\<username>\Documents\PowerShell\Microsoft.PowerShell_profile.ps1`):

```powershell
# Claude Code aliases
function c { claude $args }
function ch { claude --chrome $args }
function cc { claude --compact $args }

# Development tool aliases
function gb { gh browse }
function co { code . }

# Quick navigation
function cdir { Set-Location "C:\Users\$env:USERNAME" }
function projects { Set-Location "C:\Users\$env:USERNAME\projects" }
```

### Bash/Zsh (WSL or Mac/Linux)

Add to `~/.bashrc` or `~/.zshrc`:

```bash
# Claude Code aliases
alias c='claude'
alias ch='claude --chrome'
alias cc='claude --compact'

# Development tool aliases
alias gb='gh browse'
alias co='code .'

# Quick navigation
alias cdir='cd ~'
alias projects='cd ~/projects'
```

## Usage Examples

```bash
# Instead of: claude
c                    # Start Claude Code

# Instead of: claude --chrome
ch                   # Start Claude Code with Chrome integration

# Instead of: claude --compact
cc                   # Start with context compaction

# Instead of: gh browse
gb                   # Open current repo in browser

# Instead of: code .
co                   # Open current directory in VS Code
```

## Productivity Impact

- **Reduced keystrokes**: 70%+ reduction (claude → c, 6→1 chars)
- **Cognitive load**: Less context switching thinking about command syntax
- **Velocity**: Faster iteration cycles, especially during rapid prototyping
- **Muscle memory**: Single-letter aliases become automatic

## Installation

### PowerShell

```powershell
# Check if profile exists
Test-Path $PROFILE

# If false, create it
New-Item -Path $PROFILE -Type File -Force

# Edit profile
notepad $PROFILE

# Reload profile
. $PROFILE
```

### Bash/Zsh

```bash
# Edit your shell config
nano ~/.bashrc    # or ~/.zshrc for zsh

# Reload config
source ~/.bashrc  # or source ~/.zshrc
```

## Advanced Patterns

### Context-Aware Aliases

```powershell
# PowerShell: Auto-detect if in git repo
function cg {
    if (git rev-parse --is-inside-work-tree 2>$null) {
        claude --chrome
    } else {
        claude
    }
}
```

```bash
# Bash: Auto-detect if in git repo
cg() {
    if git rev-parse --is-inside-work-tree &>/dev/null; then
        claude --chrome
    else
        claude
    fi
}
```

### Project-Specific Aliases

```bash
# Quick navigation to common projects
alias web='cd ~/projects/web-app && c'
alias api='cd ~/projects/api && c'
alias ml='cd ~/projects/ml-models && c'
```

## Maintenance

- **Keep it minimal**: Only alias commands you use daily
- **Mnemonic names**: Single letters for ultra-frequent, short words for occasional
- **Document intent**: Add comments explaining less obvious aliases
- **Review quarterly**: Remove unused aliases, add new patterns

## Integration with AGENTICSET

These aliases complement our configuration:
- Faster access to Claude Code sessions
- Reduced friction for autonomous/supervised mode switching
- Seamless integration with git-safety-net hooks
- Velocity boost for iterative workflows
