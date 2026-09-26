#!/usr/bin/env python3
"""
Rich Library Detection and Diagnostics

Provides centralized Rich detection with better error reporting
to help users diagnose TUI issues.
"""

import sys
from typing import Tuple, Optional

# Minimum required Rich version
MIN_RICH_VERSION = "13.0.0"

# Global state
RICH_AVAILABLE = False
RICH_VERSION = None
RICH_ERROR = None


def _parse_version(version_str: str) -> Tuple[int, ...]:
    """Parse version string to tuple for comparison."""
    try:
        return tuple(int(x) for x in version_str.split('.')[:3])
    except (ValueError, AttributeError):
        return (0, 0, 0)


def check_rich() -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Check if Rich is available and meets version requirements.

    Returns:
        Tuple of (is_available, version, error_message)
    """
    global RICH_AVAILABLE, RICH_VERSION, RICH_ERROR

    try:
        import rich
        # Try multiple ways to get version
        RICH_VERSION = getattr(rich, '__version__', None)
        if RICH_VERSION is None:
            try:
                from importlib.metadata import version
                RICH_VERSION = version('rich')
            except Exception:
                RICH_VERSION = 'unknown'

        # Check version
        if RICH_VERSION != 'unknown':
            current = _parse_version(RICH_VERSION)
            required = _parse_version(MIN_RICH_VERSION)

            if current < required:
                RICH_ERROR = f"Rich version {RICH_VERSION} is too old. Required: >={MIN_RICH_VERSION}"
                RICH_AVAILABLE = False
                return False, RICH_VERSION, RICH_ERROR

        # Try importing key components
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel
        from rich.prompt import Prompt, Confirm, IntPrompt
        from rich.text import Text
        from rich import box

        # Test basic functionality
        console = Console(force_terminal=False, no_color=True)

        RICH_AVAILABLE = True
        RICH_ERROR = None
        return True, RICH_VERSION, None

    except ImportError as e:
        RICH_AVAILABLE = False
        RICH_ERROR = f"Import error: {e}"
        return False, None, RICH_ERROR

    except Exception as e:
        RICH_AVAILABLE = False
        RICH_ERROR = f"Unexpected error: {e}"
        return False, RICH_VERSION, RICH_ERROR


def get_rich_imports():
    """
    Get Rich imports if available, otherwise return None placeholders.

    Returns:
        Tuple of (Console, Table, Panel, Prompt, Confirm, IntPrompt, Text, box, Layout)
        or tuple of Nones if Rich is not available.
    """
    if not RICH_AVAILABLE:
        check_rich()

    if RICH_AVAILABLE:
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel
        from rich.prompt import Prompt, Confirm, IntPrompt
        from rich.text import Text
        from rich import box
        from rich.layout import Layout
        return Console, Table, Panel, Prompt, Confirm, IntPrompt, Text, box, Layout
    else:
        return None, None, None, None, None, None, None, None, None


def print_diagnostics():
    """Print detailed Rich diagnostics for troubleshooting."""
    print("\n" + "=" * 60)
    print("LIXPLORE TUI DIAGNOSTICS")
    print("=" * 60)

    # Python info
    print(f"\nPython Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")

    # Check if in virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    print(f"Virtual Environment: {'Yes' if in_venv else 'No'}")
    if in_venv:
        print(f"  Venv Path: {sys.prefix}")

    # Rich check
    print("\n" + "-" * 60)
    print("RICH LIBRARY STATUS")
    print("-" * 60)

    available, version, error = check_rich()

    if available:
        print(f"Status: AVAILABLE")
        print(f"Version: {version}")
        print(f"Required: >={MIN_RICH_VERSION}")
        print("\nTUI Mode: Should work correctly!")
    else:
        print(f"Status: NOT AVAILABLE")
        if version:
            print(f"Version Found: {version}")
        print(f"Required: >={MIN_RICH_VERSION}")
        print(f"Error: {error}")

        print("\n" + "-" * 60)
        print("HOW TO FIX")
        print("-" * 60)

        # Check installation method
        if 'pipx' in sys.executable.lower() or '.local/pipx' in sys.prefix:
            print("\nYou installed lixplore with pipx.")
            print("Rich needs to be in the same environment.")
            print("\nSolution (choose one):")
            print("  1. pipx inject lixplore-cli rich")
            print("  2. pipx uninstall lixplore-cli && pipx install 'lixplore-cli[tui]'")
        else:
            print("\nSolution:")
            print("  pip install 'lixplore-cli[tui]'")
            print("  # or just:")
            print("  pip install rich")

    # Show installed packages in current environment
    print("\n" + "-" * 60)
    print("INSTALLED PACKAGES (relevant)")
    print("-" * 60)

    try:
        from importlib.metadata import version, PackageNotFoundError
        relevant = ['rich', 'lixplore-cli', 'biopython', 'requests']
        for pkg in relevant:
            try:
                pkg_version = version(pkg)
                print(f"  {pkg}: {pkg_version}")
            except PackageNotFoundError:
                print(f"  {pkg}: NOT INSTALLED")
    except ImportError:
        # Fallback for older Python
        try:
            import pkg_resources
            relevant = ['rich', 'lixplore-cli', 'biopython', 'requests']
            for pkg in relevant:
                try:
                    pkg_version = pkg_resources.get_distribution(pkg).version
                    print(f"  {pkg}: {pkg_version}")
                except pkg_resources.DistributionNotFound:
                    print(f"  {pkg}: NOT INSTALLED")
        except ImportError:
            print("  (package info not available)")

    print("\n" + "=" * 60 + "\n")

    return available


# Run check on module import
check_rich()
