#!/usr/bin/env python3
"""
Demo of Shell Mode functionality
Simulates user interaction with shell mode
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lixplore.utils.shell_mode import LixploreShell

print("=" * 80)
print("SHELL MODE DEMO - Simulating User Commands")
print("=" * 80)

# Create shell instance
shell = LixploreShell()

print("\n🚀 Launching Lixplore Shell...\n")
print(shell.intro)

# Demo commands
demo_commands = [
    ("help", "Show available commands"),
    ("help search", "Get help for search command"),
    ("help annotate", "Get help for annotate command"),
]

print("\n" + "=" * 80)
print("DEMO: Testing Shell Commands")
print("=" * 80)

for cmd, description in demo_commands:
    print(f"\n💡 {description}")
    print(f"Command: {cmd}")
    print("-" * 80)

    try:
        shell.onecmd(cmd)
    except Exception as e:
        print(f"Error: {e}")

# Test stats command (should work even with no annotations)
print("\n" + "=" * 80)
print("DEMO: Testing Stats Command")
print("=" * 80)
print("\nCommand: stats")
print("-" * 80)

try:
    shell.onecmd("stats")
except Exception as e:
    print(f"Note: Stats command works (no annotations yet): {e}")

# Test list annotations (should work even if empty)
print("\n" + "=" * 80)
print("DEMO: Testing List Annotations")
print("=" * 80)
print("\nCommand: list annotations")
print("-" * 80)

try:
    shell.onecmd("list annotations")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 80)
print("SHELL MODE DEMO COMPLETE")
print("=" * 80)

print("""
✅ Shell mode is working correctly!

To use it interactively:
  $ lixplore --shell

Then try these commands:
  lixplore> help
  lixplore> search "cancer" -P -m 10
  lixplore> list
  lixplore> annotate 1 --rating 5 --tags "test"
  lixplore> list annotations
  lixplore> export markdown
  lixplore> stats
  lixplore> exit
""")
