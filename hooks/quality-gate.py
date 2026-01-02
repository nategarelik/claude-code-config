#!/usr/bin/env python3
"""
Quality Gate Hook - Validates subagent output completeness.
Checks for evidence of actual work, not just claims.
"""

import json
import sys
import re

# Minimum indicators of quality output
QUALITY_INDICATORS = [
    r"```",                        # Code block present
    r"(?:error|success|pass|fail)", # Result indicators
    r"(?:created|modified|updated|fixed)", # Action words
    r"\d+\s*(?:test|file|line)",   # Quantified results
]

# Red flags - claims without evidence
RED_FLAGS = [
    r"(?:should|would|could)\s+work",  # Hypothetical language
    r"I (?:think|believe|assume)",     # Uncertainty
    r"done[.!]?\s*$",                  # Just "done" with nothing else
]

def check_quality(output: str) -> tuple[bool, str]:
    """Check if output meets quality standards."""
    if len(output) < 50:
        return False, "Output too brief - provide more detail"

    # Check for red flags
    for flag in RED_FLAGS:
        if re.search(flag, output, re.IGNORECASE):
            return False, f"Contains uncertain language - provide evidence"

    # Check for quality indicators
    indicator_count = sum(1 for ind in QUALITY_INDICATORS
                         if re.search(ind, output, re.IGNORECASE))

    if indicator_count < 1:
        return False, "Missing evidence of work - show output/results"

    return True, ""

def main():
    try:
        data = json.loads(sys.stdin.read(50000))
        output = data.get("output", "")

        if not output:
            sys.exit(0)

        passed, reason = check_quality(output)

        if not passed:
            # SubagentStop uses decision/reason at top level, not hookSpecificOutput
            # Use decision: "block" to prevent subagent from stopping and prompt improvement
            print(json.dumps({
                "decision": "block",
                "reason": f"Quality check failed: {reason}. Please provide more detail with evidence of work."
            }))

        sys.exit(0)

    except Exception:
        sys.exit(0)

if __name__ == "__main__":
    main()
