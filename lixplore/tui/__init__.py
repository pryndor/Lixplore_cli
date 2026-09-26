"""
Full-screen Lixplore TUI built on Textual.

Needs the optional dependency: pip install "lixplore-cli[tui]" (Python 3.9+).
`launch()` falls back to the older Rich TUI when Textual is unavailable.
"""

from typing import Dict, List, Optional


def textual_available() -> bool:
    try:
        import textual  # noqa: F401
        return True
    except Exception:
        return False


def launch(results: Optional[List[Dict]] = None, query: str = "") -> None:
    """Open the TUI, optionally showing results from a CLI search."""
    if textual_available():
        from .app import LixploreApp
        LixploreApp(results=results, query=query).run()
        return

    print("The full-screen TUI needs Textual (Python 3.9+):  pip install \"lixplore-cli[tui]\"")
    print("Using the basic TUI instead.\n")
    if results:
        from lixplore.utils.interactive_tui import launch_interactive_mode
        launch_interactive_mode(results)
    else:
        from lixplore.utils.enhanced_tui import launch_enhanced_tui
        launch_enhanced_tui()
