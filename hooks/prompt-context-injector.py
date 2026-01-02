#!/usr/bin/env python3
"""
Prompt Context Injector Hook for Claude Code.
Adds relevant context to user prompts based on keywords and patterns.
Runs on UserPromptSubmit event.
"""

import json
import sys
import logging
import re
from pathlib import Path
from datetime import datetime

# Setup logging
LOG_DIR = Path.home() / ".claude" / "hooks" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=LOG_DIR / "prompt-context-injector.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def detect_thinking_trigger(prompt: str) -> str | None:
    """Detect extended thinking triggers in prompt."""
    triggers = {
        "ultrathink": "Enable extended thinking with maximum depth.",
        "think hard": "Enable extended thinking for this complex problem.",
        "think": "Apply careful reasoning to this question.",
    }
    prompt_lower = prompt.lower()
    for trigger, instruction in triggers.items():
        if trigger in prompt_lower:
            return instruction
    return None


def detect_autonomy_mode(prompt: str) -> str | None:
    """Detect autonomy mode triggers."""
    prompt_lower = prompt.lower()
    if "autonomous" in prompt_lower or "handle it" in prompt_lower:
        return "Mode: AUTONOMOUS - Execute end-to-end without checkpoints."
    if "step by step" in prompt_lower or "supervise" in prompt_lower:
        return "Mode: SUPERVISED - Explain each action before executing."
    return None


def get_current_time() -> str:
    """Get formatted current time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main() -> None:
    """Main hook entry point."""
    try:
        input_data = json.load(sys.stdin)
        prompt = input_data.get("prompt", "")

        context_parts = []

        # Add timestamp
        context_parts.append(f"Current time: {get_current_time()}")

        # Check for thinking triggers
        thinking = detect_thinking_trigger(prompt)
        if thinking:
            context_parts.append(thinking)
            logger.info(f"Detected thinking trigger: {thinking}")

        # Check for autonomy mode
        autonomy = detect_autonomy_mode(prompt)
        if autonomy:
            context_parts.append(autonomy)
            logger.info(f"Detected autonomy mode: {autonomy}")

        if context_parts:
            additional_context = "\n".join(context_parts)
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": additional_context
                }
            }
            print(json.dumps(output))
            logger.info("Context injected successfully")

        sys.exit(0)

    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {type(e).__name__}: {e}")
        sys.exit(0)


if __name__ == "__main__":
    main()
