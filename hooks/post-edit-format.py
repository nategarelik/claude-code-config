#!/usr/bin/env python3
"""
Post-Edit Format Hook for Claude Code.
Auto-formats files after edit operations based on file type.
Runs on PostToolUse for Write|Edit|MultiEdit operations.
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
    filename=LOG_DIR / "post-edit-format.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Formatters by file extension
FORMATTERS = {
    ".py": ["python", "-m", "black", "--quiet"],
    ".js": ["npx", "prettier", "--write"],
    ".ts": ["npx", "prettier", "--write"],
    ".tsx": ["npx", "prettier", "--write"],
    ".jsx": ["npx", "prettier", "--write"],
    ".json": ["npx", "prettier", "--write"],
    ".md": ["npx", "prettier", "--write"],
    ".yaml": ["npx", "prettier", "--write"],
    ".yml": ["npx", "prettier", "--write"],
}


def format_file(file_path: str) -> bool:
    """
    Format file using appropriate formatter.

    Returns:
        True if formatted successfully, False otherwise
    """
    path = Path(file_path)
    if not path.exists():
        return False

    ext = path.suffix.lower()
    formatter = FORMATTERS.get(ext)

    if not formatter:
        logger.debug(f"No formatter configured for {ext}")
        return True  # Not an error, just no formatter

    try:
        cmd = formatter + [str(path)]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            logger.info(f"Formatted {file_path}")
            return True
        else:
            logger.warning(f"Formatter failed for {file_path}: {result.stderr}")
            return False
    except FileNotFoundError:
        logger.debug(f"Formatter not found for {ext}")
        return True  # Formatter not installed, not an error
    except subprocess.TimeoutExpired:
        logger.warning(f"Formatter timeout for {file_path}")
        return False
    except Exception as e:
        logger.error(f"Error formatting {file_path}: {e}")
        return False


def main() -> None:
    """Main hook entry point."""
    try:
        input_data = json.load(sys.stdin)
        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})
        tool_response = input_data.get("tool_response", {})

        # Get file path from input
        file_path = tool_input.get("file_path", "")

        # Check if operation was successful
        if not tool_response.get("success", True):
            logger.debug("Tool operation was not successful, skipping format")
            sys.exit(0)

        if file_path:
            format_file(file_path)

        sys.exit(0)

    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {type(e).__name__}: {e}")
        sys.exit(0)


if __name__ == "__main__":
    main()
