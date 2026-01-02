#!/usr/bin/env python3
"""
Context Compression Guard Hook for Claude Code.
Warns about important context that may be lost during compression.
Suggests archiving critical decisions and context.
Runs on PreCompact event.
"""

import json
import sys
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

# Setup logging
LOG_DIR = Path.home() / ".claude" / "hooks" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=LOG_DIR / "context-compression-guard.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def get_memory_bank_path() -> Path:
    """Get path to memory bank directory."""
    return Path.home() / ".claude" / "memory-bank" / "main"


def extract_important_elements(context: str) -> Dict[str, List[str]]:
    """
    Extract potentially important elements from context.

    Args:
        context: The context string being compressed

    Returns:
        Dictionary with lists of important elements
    """
    important = {
        "decisions": [],
        "critical_items": [],
        "file_paths": [],
        "commands": []
    }

    try:
        lines = context.split('\n')

        for line in lines:
            line_lower = line.lower()

            # Look for decision markers
            if any(marker in line_lower for marker in
                   ['decision:', 'decided:', 'approved:', 'confirmed:', 'agreed:']):
                important["decisions"].append(line.strip())

            # Look for critical markers
            if any(marker in line_lower for marker in
                   ['critical:', 'important:', 'must:', 'never:', 'always:',
                    'security:', 'permission:', 'error:', 'bug:', 'issue:']):
                important["critical_items"].append(line.strip())

            # Look for file paths (approximate)
            if any(path_indicator in line for path_indicator in
                   ['/', '\\', '.py', '.js', '.ts', '.json', '.md']):
                if len(line.strip()) < 200:  # Reasonable length for a path reference
                    important["file_paths"].append(line.strip())

            # Look for commands (git, bash, etc)
            if any(cmd in line_lower for cmd in
                   ['git ', 'bash ', 'npm ', 'python ', 'docker ', 'commit']):
                important["commands"].append(line.strip())

    except Exception as e:
        logger.error(f"Error extracting important elements: {type(e).__name__}: {e}")

    return important


def calculate_compression_impact(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate what will be lost during compression.

    Args:
        input_data: Hook input data with context info

    Returns:
        Dictionary with compression impact analysis
    """
    impact = {
        "original_tokens": input_data.get("original_token_count", 0),
        "target_tokens": input_data.get("target_token_count", 0),
        "reduction_percent": 0,
        "elements_at_risk": []
    }

    if impact["original_tokens"] > 0:
        reduction = (1 - impact["target_tokens"] / impact["original_tokens"]) * 100
        impact["reduction_percent"] = round(reduction, 1)

    return impact


def archive_critical_context(important_elements: Dict[str, List[str]]) -> Optional[str]:
    """
    Archive critical context to memory bank before compression.

    Args:
        important_elements: Dictionary of important elements extracted from context

    Returns:
        Path to archive file, or None if error
    """
    try:
        memory_path = get_memory_bank_path()
        memory_path.mkdir(parents=True, exist_ok=True)

        archive_dir = memory_path / "compression-archives"
        archive_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_file = archive_dir / f"context-archive_{timestamp}.json"

        archive_data = {
            "timestamp": datetime.now().isoformat(),
            "archive_type": "pre-compression",
            "critical_decisions": important_elements.get("decisions", [])[:10],
            "critical_items": important_elements.get("critical_items", [])[:10],
            "referenced_files": important_elements.get("file_paths", [])[:10],
            "commands_used": important_elements.get("commands", [])[:10],
            "note": "This context was archived before compression to preserve important decisions and context"
        }

        with open(archive_file, 'w', encoding='utf-8') as f:
            json.dump(archive_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Critical context archived to: {archive_file}")
        return str(archive_file)

    except Exception as e:
        logger.error(f"Error archiving critical context: {type(e).__name__}: {e}")
        return None


def build_warning_message(context: str, impact: Dict[str, Any],
                         important_elements: Dict[str, List[str]]) -> str:
    """
    Build a warning message about compression.

    Args:
        context: The context being compressed
        impact: Compression impact analysis
        important_elements: Extracted important elements

    Returns:
        Warning message string
    """
    message_parts = []
    message_parts.append("=== Context Compression Warning ===\n")

    # Compression stats
    message_parts.append(f"Compression: {impact['original_tokens']:,} -> "
                        f"{impact['target_tokens']:,} tokens "
                        f"({impact['reduction_percent']:.1f}% reduction)\n")

    # Important elements being compressed
    message_parts.append("Elements at risk of being compressed away:\n")

    if important_elements.get("decisions"):
        message_parts.append(
            f"  - {len(important_elements['decisions'])} decisions/approvals\n")

    if important_elements.get("critical_items"):
        message_parts.append(
            f"  - {len(important_elements['critical_items'])} critical items\n")

    if important_elements.get("file_paths"):
        message_parts.append(
            f"  - {len(important_elements['file_paths'])} file references\n")

    if important_elements.get("commands"):
        message_parts.append(
            f"  - {len(important_elements['commands'])} executed commands\n")

    message_parts.append("\nRecommendations:\n")
    message_parts.append("1. Review critical decisions above\n")
    message_parts.append("2. Archive context before compression if needed\n")
    message_parts.append("3. Consider documenting key findings in memory-bank\n")
    message_parts.append("4. This compression is informational only - no action required\n")

    return "".join(message_parts)


def main() -> None:
    """Main hook entry point."""
    try:
        input_data = json.load(sys.stdin)

        # Extract context that will be compressed
        context = input_data.get("context", "")
        if not context or len(context) < 100:
            # Not much context to worry about
            sys.exit(0)

        # Analyze what's important in the context
        important_elements = extract_important_elements(context)

        # Calculate compression impact
        impact = calculate_compression_impact(input_data)

        # Archive critical context if there's anything important
        has_important = any(important_elements.get(key) for key in important_elements)
        if has_important:
            archive_path = archive_critical_context(important_elements)
            if archive_path:
                logger.info(f"Context archived before compression to {archive_path}")

        # Build warning message
        warning_message = build_warning_message(context, impact, important_elements)

        # PreCompact: stdout is shown in transcript mode (Ctrl-R)
        # No hookSpecificOutput needed - just print informational message
        print(warning_message)

        logger.info(f"Compression event logged - {impact['reduction_percent']:.1f}% reduction")
        sys.exit(0)

    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {type(e).__name__}: {e}")
        sys.exit(0)


if __name__ == "__main__":
    main()
