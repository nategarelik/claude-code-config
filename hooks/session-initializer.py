#!/usr/bin/env python3
"""
Session Initializer Hook for Claude Code.
Loads previous session context and recent git information on session start.
Runs on SessionStart event.
"""

import json
import sys
import logging
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

# Setup logging
LOG_DIR = Path.home() / ".claude" / "hooks" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=LOG_DIR / "session-initializer.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def get_memory_bank_path() -> Path:
    """Get path to memory bank directory."""
    return Path.home() / ".claude" / "memory-bank" / "main" / "sessions"


def load_previous_session() -> Optional[Dict[str, Any]]:
    """
    Load the most recent session from memory bank.

    Returns:
        Session data dict or None if not found
    """
    try:
        memory_path = get_memory_bank_path()
        if not memory_path.exists():
            return None

        # Find most recent session file
        session_files = sorted(memory_path.glob("session_*.json"), reverse=True)
        if not session_files:
            return None

        latest_session = session_files[0]
        with open(latest_session, 'r', encoding='utf-8') as f:
            data = json.load(f)
            logger.info(f"Loaded previous session from: {latest_session}")
            return data

    except Exception as e:
        logger.error(f"Error loading previous session: {type(e).__name__}: {e}")
        return None


def load_progress_file() -> Optional[str]:
    """
    Load claude-progress.txt if it exists, returning last 20 lines.

    Returns:
        Last 20 lines of progress file, or None if not found
    """
    try:
        progress_file = Path.home() / ".claude" / "claude-progress.txt"
        if not progress_file.exists():
            return None

        with open(progress_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Get last 20 lines
            recent_lines = lines[-20:] if len(lines) > 20 else lines
            progress_text = ''.join(recent_lines).strip()
            logger.info(f"Loaded progress file: {len(recent_lines)} recent lines")
            return progress_text

    except Exception as e:
        logger.error(f"Error loading progress file: {type(e).__name__}: {e}")
        return None


def get_git_branch() -> Optional[str]:
    """
    Get current git branch name.

    Returns:
        Branch name or None if not in git repo
    """
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            branch = result.stdout.strip()
            logger.info(f"Current git branch: {branch}")
            return branch
        return None
    except Exception as e:
        logger.debug(f"Error getting git branch: {type(e).__name__}: {e}")
        return None


def get_recent_commits(limit: int = 5) -> Optional[List[str]]:
    """
    Get recent git commits.

    Args:
        limit: Number of commits to retrieve

    Returns:
        List of commit messages, or None if error
    """
    try:
        result = subprocess.run(
            ['git', 'log', f'-{limit}', '--oneline'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            commits = result.stdout.strip().split('\n')
            commits = [c.strip() for c in commits if c.strip()]
            logger.info(f"Retrieved {len(commits)} recent commits")
            return commits
        return None
    except Exception as e:
        logger.debug(f"Error getting recent commits: {type(e).__name__}: {e}")
        return None


def build_context_summary() -> Dict[str, Any]:
    """
    Build comprehensive context summary from all sources.

    Returns:
        Dictionary with all available context
    """
    summary = {
        "timestamp": datetime.now().isoformat(),
        "git": {},
        "previous_session": None,
        "progress": None
    }

    # Add git context
    branch = get_git_branch()
    if branch:
        summary["git"]["current_branch"] = branch

    commits = get_recent_commits(5)
    if commits:
        summary["git"]["recent_commits"] = commits

    # Add previous session info
    previous = load_previous_session()
    if previous:
        summary["previous_session"] = {
            "session_id": previous.get("session_id"),
            "summary": previous.get("summary"),
            "timestamp": previous.get("timestamp"),
            "files_modified_count": len(previous.get("files_modified", [])),
            "tools_used": previous.get("tools_used", [])[:5],  # First 5 tools
        }

    # Add progress file
    progress = load_progress_file()
    if progress:
        summary["progress"] = progress

    return summary


def main() -> None:
    """Main hook entry point."""
    try:
        input_data = json.load(sys.stdin)

        context_summary = build_context_summary()

        # Format summary for readability
        summary_parts = []
        summary_parts.append("=== Session Context Loaded ===")

        if context_summary.get("git"):
            git_info = context_summary["git"]
            summary_parts.append(f"\nGit: {git_info.get('current_branch', 'unknown')}")
            if git_info.get("recent_commits"):
                summary_parts.append("Recent commits:")
                for commit in git_info["recent_commits"][:3]:
                    summary_parts.append(f"  {commit}")

        if context_summary.get("previous_session"):
            prev = context_summary["previous_session"]
            summary_parts.append(f"\nPrevious session: {prev.get('session_id')}")
            summary_parts.append(f"  Summary: {prev.get('summary', 'N/A')}")
            summary_parts.append(f"  Files modified: {prev.get('files_modified_count', 0)}")
            if prev.get("tools_used"):
                summary_parts.append(f"  Tools used: {', '.join(prev['tools_used'])}")

        if context_summary.get("progress"):
            summary_parts.append(f"\nRecent progress:")
            # Show first few lines of progress
            progress_lines = context_summary["progress"].split('\n')[:5]
            for line in progress_lines:
                summary_parts.append(f"  {line}")

        additional_context = "\n".join(summary_parts)

        # SessionStart only supports additionalContext (no custom fields)
        output = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": additional_context
            }
        }
        print(json.dumps(output))

        logger.info("Session context loaded successfully")
        sys.exit(0)

    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {type(e).__name__}: {e}")
        sys.exit(0)


if __name__ == "__main__":
    main()
