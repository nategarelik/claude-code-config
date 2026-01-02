#!/usr/bin/env python3
"""
Session Archiver Hook for Claude Code.
Archives session context to memory-bank when session stops.
Runs on Stop event.

Parses the transcript file to extract:
- Tools used during the session
- Files modified (Edit/Write operations)
- Session summary from first user message
"""

import json
import sys
import os
import logging
import tempfile
import shutil
import uuid
import re
from datetime import datetime
from pathlib import Path
from typing import Any, List, Dict, Set, Optional

# Setup logging
LOG_DIR = Path.home() / ".claude" / "hooks" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=LOG_DIR / "session-archiver.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def get_memory_bank_path() -> Path:
    """Get path to memory bank directory."""
    return Path.home() / ".claude" / "memory-bank" / "main" / "sessions"


def sanitize_filename(filename: str) -> str:
    """
    Remove dangerous characters from filename.

    Args:
        filename: Raw filename string

    Returns:
        Sanitized filename safe for filesystem
    """
    # Remove path separators and special chars
    safe = re.sub(r'[^\w\-_.]', '_', str(filename))
    # Prevent directory traversal
    safe = safe.replace('..', '_')
    # Limit length
    return safe[:100]


def safe_get_string(data: dict, key: str, default: str = "") -> str:
    """Safely extract string value from dict."""
    value = data.get(key, default)
    if value is None:
        return default
    return str(value)[:10000]  # Limit length


def safe_get_list(data: dict, key: str) -> List[Any]:
    """Safely extract list value from dict."""
    value = data.get(key, [])
    if isinstance(value, list):
        return value[:1000]  # Limit items
    return []


def check_disk_space(path: Path, required_mb: int = 5) -> bool:
    """
    Check if sufficient disk space available.

    Args:
        path: Path to check
        required_mb: Minimum required MB

    Returns:
        True if sufficient space available
    """
    try:
        stat = shutil.disk_usage(path)
        available_mb = stat.free / (1024 * 1024)
        return available_mb >= required_mb
    except (OSError, AttributeError):
        return True  # Assume OK if can't check


def parse_transcript(transcript_path: str) -> Dict[str, Any]:
    """
    Parse transcript JSONL file to extract session information.

    Args:
        transcript_path: Path to the transcript .jsonl file

    Returns:
        Dict with tools_used, files_modified, and summary
    """
    tools_used: Set[str] = set()
    files_modified: Set[str] = set()
    first_user_message: Optional[str] = None

    try:
        transcript_file = Path(transcript_path)
        if not transcript_file.exists():
            logger.warning(f"Transcript file not found: {transcript_path}")
            return {
                "tools_used": [],
                "files_modified": [],
                "summary": "Session ended"
            }

        with open(transcript_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue

                entry_type = entry.get("type", "")

                # Extract first user message for summary
                if entry_type == "user" and first_user_message is None:
                    message = entry.get("message", {})
                    content = message.get("content", "")
                    if isinstance(content, str) and content:
                        # Truncate long messages
                        first_user_message = content[:200]
                        if len(content) > 200:
                            first_user_message += "..."

                # Extract tool usage from assistant messages
                if entry_type == "assistant":
                    message = entry.get("message", {})
                    content_list = message.get("content", [])

                    if isinstance(content_list, list):
                        for content_item in content_list:
                            if not isinstance(content_item, dict):
                                continue

                            if content_item.get("type") == "tool_use":
                                tool_name = content_item.get("name", "")
                                if tool_name:
                                    tools_used.add(tool_name)

                                # Extract file paths from file-modifying tools
                                tool_input = content_item.get("input", {})
                                if isinstance(tool_input, dict):
                                    file_path = tool_input.get("file_path", "")
                                    if file_path and tool_name in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
                                        files_modified.add(file_path)

    except Exception as e:
        logger.error(f"Error parsing transcript: {e}")

    # Generate summary
    if first_user_message:
        summary = f"Task: {first_user_message}"
    else:
        summary = "Session ended"

    return {
        "tools_used": sorted(list(tools_used)),
        "files_modified": sorted(list(files_modified)),
        "summary": summary
    }


def archive_session(session_data: dict) -> str:
    """
    Archive session data to memory bank with atomic write.

    Args:
        session_data: Session information to archive

    Returns:
        Path to archive file

    Raises:
        IOError: If disk space insufficient
        OSError: If write fails
    """
    memory_path = get_memory_bank_path()
    memory_path.mkdir(parents=True, exist_ok=True)

    # Check disk space
    if not check_disk_space(memory_path):
        raise IOError("Insufficient disk space for session archive")

    # Generate unique filename (prevent collision)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    archive_file = memory_path / f"session_{timestamp}_{unique_id}.json"

    archive_data = {
        "timestamp": datetime.now().isoformat(),
        "session_id": sanitize_filename(session_data.get("session_id", "unknown")),
        "summary": safe_get_string(session_data, "summary", "Session ended"),
        "tools_used": safe_get_list(session_data, "tools_used"),
        "files_modified": safe_get_list(session_data, "files_modified"),
        "key_decisions": safe_get_list(session_data, "key_decisions"),
    }

    # Atomic write via temp file
    temp_fd = None
    temp_path = None
    try:
        temp_fd, temp_path = tempfile.mkstemp(
            dir=memory_path,
            prefix=".session_",
            suffix=".tmp"
        )

        with os.fdopen(temp_fd, "w", encoding="utf-8") as f:
            json.dump(archive_data, f, indent=2, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())

        temp_fd = None  # Prevent double-close

        # Atomic rename
        shutil.move(temp_path, archive_file)
        logger.info(f"Session archived to: {archive_file}")
        return str(archive_file)

    except Exception as e:
        # Clean up temp file on failure
        if temp_path and Path(temp_path).exists():
            try:
                os.unlink(temp_path)
            except OSError:
                pass
        raise


def main() -> None:
    """Main hook entry point."""
    try:
        input_data = json.load(sys.stdin)
        logger.debug(f"Received input: {json.dumps(input_data)}")

        # Claude Code Stop hook provides:
        # - session_id: Unique session identifier
        # - transcript_path: Path to the conversation JSONL file
        # - cwd: Current working directory
        # - permission_mode: Current permission mode
        # - hook_event_name: "Stop"
        # - stop_hook_active: Boolean to prevent infinite loops

        session_id = safe_get_string(input_data, "session_id", "unknown")
        transcript_path = input_data.get("transcript_path", "")

        # Parse transcript to extract actual session data
        if transcript_path:
            logger.info(f"Parsing transcript: {transcript_path}")
            transcript_data = parse_transcript(transcript_path)
        else:
            logger.warning("No transcript_path provided")
            transcript_data = {
                "tools_used": [],
                "files_modified": [],
                "summary": "Session ended"
            }

        session_data = {
            "session_id": session_id,
            "summary": transcript_data["summary"],
            "tools_used": transcript_data["tools_used"],
            "files_modified": transcript_data["files_modified"],
            "key_decisions": [],  # Could be extracted from transcript in future
        }

        archive_file = archive_session(session_data)

        # Stop hooks don't support hookSpecificOutput.additionalContext
        # For informational output, just print to stdout (shown in transcript mode)
        # Exit 0 = success, don't block stopping
        print(f"Session archived to: {archive_file}")

        sys.exit(0)

    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        sys.exit(0)
    except IOError as e:
        logger.error(f"IO error: {e}")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {type(e).__name__}: {e}")
        sys.exit(0)


if __name__ == "__main__":
    main()
