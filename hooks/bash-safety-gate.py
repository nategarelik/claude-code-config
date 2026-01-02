#!/usr/bin/env python3
"""
Combined Bash Safety Gate - Merges safety-gate.py + git-safety-net.py
Single hook = faster execution, no duplication risk.
"""

import json
import sys
import re
import logging
from pathlib import Path

# Setup logging
LOG_DIR = Path.home() / ".claude" / "hooks" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=LOG_DIR / "bash-safety-gate.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# === DANGEROUS COMMAND PATTERNS ===
BLOCK_PATTERNS = [
    (r"rm\s+-rf\s+[/~]", "Recursive delete of root/home"),
    (r"rm\s+-rf\s+\.\s*$", "Recursive delete of current dir"),
    (r":(){ :|:& };:", "Fork bomb"),
    (r"mkfs\.", "Format filesystem"),
    (r"dd\s+if=.*of=/dev/", "Overwrite disk"),
    (r">\s*/dev/sd[a-z]", "Redirect to disk device"),
    (r"chmod\s+-R\s+777\s+/", "Dangerous permissions on root"),
    (r"curl.*\|\s*(ba)?sh", "Pipe curl to shell"),
    (r"wget.*\|\s*(ba)?sh", "Pipe wget to shell"),
]

# === GIT SAFETY PATTERNS ===
GIT_DANGEROUS = [
    (r"git\s+push\s+.*--force\s+.*(?:main|master)", "Force push to main/master"),
    (r"git\s+push\s+-f\s+.*(?:main|master)", "Force push to main/master"),
    (r"git\s+reset\s+--hard\s+HEAD~?\d*\s*$", "Hard reset (may lose work)"),
    (r"git\s+clean\s+-fd", "Clean untracked files"),
    (r"git\s+checkout\s+--\s+\.", "Discard all changes"),
]

GIT_WARN_PATTERNS = [
    (r"git\s+rebase\s+-i", "Interactive rebase"),
    (r"git\s+commit\s+--amend", "Amend commit"),
]


def check_command(command: str) -> tuple[str, str, str]:
    """
    Check command for safety issues.
    Returns: (decision, reason, context)
    - decision: "allow", "deny", or "warn"
    """
    cmd_lower = command.lower()

    # Check dangerous patterns (BLOCK)
    for pattern, desc in BLOCK_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return "deny", f"Blocked dangerous command: {desc}", ""

    # Check git dangerous patterns (BLOCK)
    for pattern, desc in GIT_DANGEROUS:
        if re.search(pattern, command, re.IGNORECASE):
            return "deny", f"Blocked git operation: {desc}", ""

    # Check git warning patterns (ALLOW with context)
    for pattern, desc in GIT_WARN_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return "allow", "", f"⚠️ Caution: {desc} - ensure this is intentional"

    return "allow", "", ""


def main():
    try:
        data = json.loads(sys.stdin.read(10000))
        command = data.get("tool_input", {}).get("command", "")

        if not command:
            sys.exit(0)

        logger.info(f"Checking: {command[:100]}...")

        decision, reason, context = check_command(command)

        if decision == "deny":
            logger.warning(f"BLOCKED: {reason}")
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": f"🛑 {reason}"
                }
            }))
        elif context:
            # Allow but add warning context
            logger.info(f"Warning: {context}")
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "additionalContext": context
                }
            }))

        sys.exit(0)

    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(0)


if __name__ == "__main__":
    main()
