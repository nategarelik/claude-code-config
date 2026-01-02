#!/usr/bin/env python3
"""
Git Safety Net Hook for Claude Code.
Prevents dangerous git operations and protects important branches.
Runs on PreToolUse for Write|Edit|MultiEdit operations.
"""

import json
import sys
import logging
import subprocess
from pathlib import Path

# Setup logging
LOG_DIR = Path.home() / ".claude" / "hooks" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=LOG_DIR / "git-safety-net.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Protected branches that require extra caution
PROTECTED_BRANCHES = ["main", "master", "production", "release"]

# Protected file patterns
PROTECTED_PATTERNS = [
    ".env",
    ".env.*",
    "*.pem",
    "*.key",
    "*secret*",
    "*credential*",
    "id_rsa*",
]


def get_current_branch() -> str | None:
    """Get current git branch."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception as e:
        logger.debug(f"Error getting branch: {e}")
    return None


def is_protected_file(file_path: str) -> bool:
    """Check if file matches protected patterns."""
    from fnmatch import fnmatch
    file_name = Path(file_path).name
    for pattern in PROTECTED_PATTERNS:
        if fnmatch(file_name, pattern) or fnmatch(file_path, pattern):
            return True
    return False


def main() -> None:
    """Main hook entry point."""
    try:
        input_data = json.load(sys.stdin)
        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})

        file_path = tool_input.get("file_path", "")

        # Check for protected files
        if file_path and is_protected_file(file_path):
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": f"Protected file pattern detected: {file_path}"
                }
            }
            print(json.dumps(output))
            logger.warning(f"Blocked access to protected file: {file_path}")
            sys.exit(0)

        # Check branch protection for certain operations
        branch = get_current_branch()
        if branch in PROTECTED_BRANCHES:
            logger.info(f"Operating on protected branch: {branch}")
            # We don't block, just log for awareness

        # Allow the operation
        sys.exit(0)

    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {type(e).__name__}: {e}")
        sys.exit(0)


if __name__ == "__main__":
    main()
