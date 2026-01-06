# Claude Code Context Bar for Windows

A PowerShell adaptation of YK's context-bar.sh providing real-time visibility into Claude Code session state.

## Features

- **Model Display**: Shows current Claude model (simplified name)
- **Directory Context**: Current working directory
- **Git Integration**: Branch, uncommitted files, ahead/behind status
- **Token Usage**: Visual progress bar and percentage of context window
- **Conversation Preview**: Last user message (truncated to fit)
- **Color Themes**: 9 themes (orange, blue, teal, green, lavender, rose, gold, slate, cyan)

## Installation

### Automatic (via Hook)

The context bar can be automatically displayed at session start by enabling the SessionStart hook.

1. Create or edit `C:\Users\<username>\.claude\hooks\session-start-context-bar.py`
2. Configure hook in `settings.json` under `hooks.SessionStart`
3. Restart Claude Code

### Manual Usage

```powershell
# Basic usage (reads from stdin)
echo '{"model":"claude-sonnet-4-5-20250929","cwd":"C:\\Projects\\myapp","transcriptPath":"C:\\Users\\...\\transcript.json"}' | powershell C:\Users\Nate2\.claude\scripts\context-bar.ps1

# With color theme
echo '{"model":"..."}' | powershell C:\Users\Nate2\.claude\scripts\context-bar.ps1 -Color "lavender"

# Direct JSON parameter
powershell C:\Users\Nate2\.claude\scripts\context-bar.ps1 -InputJson '{"model":"..."}'
```

## Color Themes

| Theme    | Color      | Use Case                           |
|----------|------------|------------------------------------|
| orange   | DarkYellow | Warm, high-visibility              |
| blue     | Blue       | Cool, professional                 |
| teal     | Cyan       | Balanced, modern (default)         |
| green    | Green      | Success-oriented, calm             |
| lavender | Magenta    | Creative, distinctive              |
| rose     | Red        | Urgent, attention-grabbing         |
| gold     | Yellow     | Premium, bright                    |
| slate    | Gray       | Minimal, subdued                   |
| cyan     | Cyan       | Technical, clear                   |

## Status Bar Format

```
Model | 📁Directory | 🔀Branch (uncommitted) ↑ahead ↓behind | [██████░░░░] 60% | 💬Last message...
```

### Components

1. **Model**: `sonnet-4-5` (version stripped)
2. **Directory**: `📁myapp` (basename only)
3. **Git** (if in repo):
   - `🔀main` - branch name
   - `(3)` - 3 uncommitted files
   - `(file.txt)` - single uncommitted file (shows name)
   - `↑2` - 2 commits ahead of upstream
   - `↓1` - 1 commit behind upstream
4. **Tokens**:
   - `[████████░░]` - visual progress (10 chars)
   - `80%` - percentage of context window used
5. **Preview**: `💬Last user message truncated to fit...`

## Token Calculation

- **Baseline**: 20,000 tokens (system prompt, tools, memory, dynamic context)
- **Reading**: Parses transcript JSON for last `metadata.inputTokens`
- **Progress**: Visualizes against context window (default 200k)

## Integration with AGENTICSET

The context bar complements our configuration by:
- **Visual feedback** on context consumption (aligns with token efficiency goals)
- **Git awareness** (works with git-safety-net.py hook)
- **Session context** (shows what you're working on at a glance)
- **Autonomy support** (quickly see if you're approaching context limits)

## Customization

### Change Default Theme

Edit the script's default:
```powershell
[string]$Color = "lavender"  # Change from "teal"
```

### Adjust Progress Bar Width

```powershell
$barWidth = 20  # Change from 10 for more granular visualization
```

### Modify Baseline Tokens

```powershell
$tokens = 15000  # Adjust if your setup has lower overhead
```

## Troubleshooting

**Q: Status bar shows wrong tokens**
A: Baseline is 20k. Token count comes from transcript's last API message metadata.

**Q: Git info not showing**
A: Ensure git is in PATH and you're in a git repository. Check `git branch --show-current` works in PowerShell.

**Q: Colors not displaying**
A: PowerShell console colors are limited. Windows Terminal provides better color support.

**Q: Conversation preview empty**
A: Transcript must contain user messages with text content. Early in conversation, this may be empty.

## Performance

- **Startup time**: ~100-300ms depending on transcript size
- **Dependencies**: PowerShell 5.1+, git (optional)
- **File I/O**: Reads transcript JSON once per invocation

## Future Enhancements

- [ ] RGB/True color support for Windows Terminal
- [ ] Caching transcript parsing for faster updates
- [ ] Integration with Windows notifications
- [ ] Real-time updates via file watching
- [ ] Export to Starship prompt format
