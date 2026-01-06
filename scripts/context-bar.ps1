# Claude Code Context Bar for PowerShell
# Adapted from YK's claude-code-tips context-bar.sh for Windows

param(
    [string]$InputJson = "",
    [string]$Color = "teal"
)

# Color theme definitions (PowerShell console colors)
$ColorThemes = @{
    "orange"   = "DarkYellow"
    "blue"     = "Blue"
    "teal"     = "Cyan"
    "green"    = "Green"
    "lavender" = "Magenta"
    "rose"     = "Red"
    "gold"     = "Yellow"
    "slate"    = "Gray"
    "cyan"     = "Cyan"
}

$AccentColor = $ColorThemes[$Color]
if (-not $AccentColor) { $AccentColor = "Cyan" }

# Parse input JSON (from stdin if not provided)
if (-not $InputJson) {
    $InputJson = [Console]::In.ReadToEnd()
}

try {
    $data = $InputJson | ConvertFrom-Json
} catch {
    Write-Error "Failed to parse JSON input"
    exit 1
}

# Extract core information
$model = if ($data.model) { $data.model -replace '^claude-', '' -replace '-\d{8}$', '' } else { "sonnet" }
$cwd = if ($data.cwd) { Split-Path -Leaf $data.cwd } else { "unknown" }
$transcriptPath = $data.transcriptPath
$contextWindow = if ($data.contextWindow) { $data.contextWindow } else { 200000 }

# Initialize output components
$statusParts = @()

# Add model
$statusParts += $model

# Add current directory
$statusParts += "DIR:$cwd"

# Git information (if in git repo)
try {
    $gitBranch = git branch --show-current 2>$null
    if ($LASTEXITCODE -eq 0 -and $gitBranch) {
        $gitInfo = "GIT:$gitBranch"

        # Count uncommitted files
        $uncommitted = (git status --porcelain 2>$null | Measure-Object -Line).Lines
        if ($uncommitted -eq 1) {
            $filename = (git status --porcelain 2>$null) -replace '^\s*\S+\s+', ''
            $gitInfo += " ($filename)"
        } elseif ($uncommitted -gt 0) {
            $gitInfo += " ($uncommitted)"
        }

        # Check upstream status
        $ahead = (git rev-list --count '@{u}..HEAD' 2>$null)
        $behind = (git rev-list --count 'HEAD..@{u}' 2>$null)

        if ($ahead -and $ahead -gt 0) {
            $gitInfo += " ^$ahead"
        }
        if ($behind -and $behind -gt 0) {
            $gitInfo += " v$behind"
        }

        $statusParts += $gitInfo
    }
} catch {
    # Not in a git repo or git not available
}

# Token usage calculation
$tokens = 20000  # Default baseline
if ($transcriptPath -and (Test-Path $transcriptPath)) {
    try {
        # Read transcript and find last message with token usage
        $transcript = Get-Content $transcriptPath -Raw | ConvertFrom-Json
        foreach ($msg in $transcript.messages) {
            if ($msg.metadata -and $msg.metadata.inputTokens) {
                $tokens = $msg.metadata.inputTokens
            }
        }
    } catch {
        # Use baseline if transcript parsing fails
    }
}

# Calculate token percentage and progress bar
$tokenPercent = [math]::Min(100, [math]::Round(($tokens / $contextWindow) * 100))
$barWidth = 10
$filled = [math]::Floor($barWidth * $tokens / $contextWindow)
$empty = $barWidth - $filled

$progressBar = ""
for ($i = 0; $i -lt $filled; $i++) { $progressBar += "#" }
for ($i = 0; $i -lt $empty; $i++) { $progressBar += "-" }

$statusParts += "[$progressBar] $tokenPercent%"

# Conversation preview (last user message)
if ($transcriptPath -and (Test-Path $transcriptPath)) {
    try {
        $transcript = Get-Content $transcriptPath -Raw | ConvertFrom-Json
        $lastUserMsg = ""

        for ($i = $transcript.messages.Count - 1; $i -ge 0; $i--) {
            $msg = $transcript.messages[$i]
            if ($msg.role -eq "user" -and $msg.text -and $msg.text.Length -gt 0) {
                $lastUserMsg = $msg.text -replace '\n', ' ' -replace '\s+', ' '
                break
            }
        }

        if ($lastUserMsg) {
            $maxWidth = $Host.UI.RawUI.WindowSize.Width - ($statusParts -join " | ").Length - 10
            if ($lastUserMsg.Length -gt $maxWidth -and $maxWidth -gt 0) {
                $lastUserMsg = $lastUserMsg.Substring(0, $maxWidth) + "..."
            }
            $statusParts += "MSG:$lastUserMsg"
        }
    } catch {
        # Skip preview if transcript parsing fails
    }
}

# Output with color
$output = $statusParts -join " | "
Write-Host $output -ForegroundColor $AccentColor
