"""Terminal-based review gate for video scripts."""

import json
import os
import subprocess
import sys
import tempfile


def print_script_preview(script: dict):
    """Pretty-print the script for terminal review."""
    print("\n" + "=" * 60)
    print(f"  CHAPTER PULSE: {script['chapter'].upper()}")
    print(f"  {script['month']}")
    print("=" * 60)

    print(f"\n  BEAT 1: {script['chapter'].upper()}")

    stat = script["stat_hook"]
    print(f"\n  BEAT 2: {stat['number']} {stat['descriptor']}")

    print(f"\n  BEAT 3: Quotes")
    for i, m in enumerate(script["moments"], 1):
        print(f"    {i}. \"{m['quote']}\"")
        print(f"       — {m['first_name']}, {m['title']}")

    b4 = script["beat_4_stat"]
    print(f"\n  BEAT 4: {b4['number']} {b4['descriptor']}")

    print(f"\n  BEAT 5: {script['cta_line']}")
    print("=" * 60)


def review_script(script: dict, script_path: str) -> str:
    """Present script for review. Returns 'approve' or 'reject'.

    If user chooses 'edit', opens the JSON file in the default editor,
    reloads, shows the updated preview, and asks again.
    """
    print_script_preview(script)

    while True:
        print("\n  Options: [a]pprove  [e]dit  [r]eject")
        choice = input("  > ").strip().lower()

        if choice in ("a", "approve"):
            print("  ✓ Script approved. Moving to render.")
            return "approve"

        elif choice in ("r", "reject"):
            print("  ✗ Script rejected. Exiting.")
            return "reject"

        elif choice in ("e", "edit"):
            # Open in default editor (macOS: 'open' opens in default app)
            editor = os.environ.get("EDITOR", "open")
            subprocess.call([editor, script_path])

            input("  Press Enter after saving your edits...")

            # Reload and show updated preview
            with open(script_path) as f:
                script = json.load(f)

            print("\n  Updated script:")
            print_script_preview(script)
            # Loop continues — user must approve or reject

        else:
            print("  Please enter 'a', 'e', or 'r'.")
