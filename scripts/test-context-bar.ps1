# Test script for context-bar.ps1

# Create sample JSON input
$testData = @{
    model = "claude-sonnet-4-5-20250929"
    cwd = "C:\Users\Nate2\.claude"
    transcriptPath = ""
    contextWindow = 200000
} | ConvertTo-Json

Write-Host "`nTesting Context Bar with sample data:" -ForegroundColor Yellow
Write-Host "======================================`n" -ForegroundColor Yellow

# Test each color theme
$themes = @("orange", "blue", "teal", "green", "lavender", "rose", "gold", "slate", "cyan")

foreach ($theme in $themes) {
    Write-Host "$theme theme: " -NoNewline
    $testData | & "$PSScriptRoot\context-bar.ps1" -Color $theme
}

Write-Host "`n======================================" -ForegroundColor Yellow
Write-Host "If you see colored status bars above, context-bar.ps1 is working!" -ForegroundColor Green
Write-Host "`nTo use with actual Claude Code data, the script needs JSON input with:" -ForegroundColor Cyan
Write-Host "  - model: Claude model name" -ForegroundColor Cyan
Write-Host "  - cwd: Current working directory" -ForegroundColor Cyan
Write-Host "  - transcriptPath: Path to conversation transcript" -ForegroundColor Cyan
Write-Host "  - contextWindow: Token limit (default 200000)`n" -ForegroundColor Cyan
