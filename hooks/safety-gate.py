#!/usr/bin/env python3
"""
Safety Gate Hook - Blocks dangerous bash commands.
Minimal, focused, fast.
"""

import json
import sys
import re

# Dangerous patterns to block
BLOCK_PATTERNS = [
    r"rm\s+-rf\s+[/~]",           # rm -rf / or ~
    r"rm\s+-rf\s+\.\s*$",          # rm -rf .
    r":(){ :|:& };:",              # Fork bomb
    r"mkfs\.",                     # Format filesystem
    r"dd\s+if=.*of=/dev/",         # Overwrite disk
    r">\s*/dev/sd[a-z]",           # Redirect to disk
    r"chmod\s+-R\s+777\s+/",       # Dangerous permissions
    r"curl.*\|\s*(ba)?sh",         # Pipe curl to shell
    r"wget.*\|\s*(ba)?sh",         # Pipe wget to shell
]

def is_dangerous(command: str) -> tuple[bool, str]:
    """Check if command matches dangerous patterns."""
    for pattern in BLOCK_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return True, f"Blocked: matches dangerous pattern '{pattern}'"
    return False, ""

def main():
    try:
        data = json.loads(sys.stdin.read(5000))
        command = data.get("tool_input", {}).get("command", "")

        dangerous, reason = is_dangerous(command)
        if dangerous:
            # Use correct PreToolUse format with permissionDecision
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": f"BLOCKED: {reason}. This operation could cause irreversible damage."
                }
            }))
            sys.exit(0)  # Exit 0 when using JSON output

        sys.exit(0)  # Allow

    except Exception:
        sys.exit(0)  # Don't block on hook errors

if __name__ == "__main__":
    main()
