"""
Full-screen Lixplore TUI built on Textual.

Needs the optional dependency: pip install "lixplore-cli[tui]" (Python 3.9+).
`launch()` falls back to the older Rich TUI when Textual is unavailable.
"""

from typing import Dict, List, Optional

# The app uses widgets and options added in Textual 4; older copies (such as
# the ones Debian and Ubuntu ship) import fine but crash when the app starts.
MIN_TEXTUAL = (4, 0)


def textual_version() -> Optional[str]:
    """Installed Textual version, or None when it is missing."""
    try:
        import textual  # noqa: F401
        from importlib.metadata import version
        return version("textual")
    except Exception:
        return None


def textual_available() -> bool:
    found = textual_version()
    if not found:
        return False
    try:
        parts = tuple(int(p) for p in found.split(".")[:2] if p.isdigit())
    except ValueError:
        return False
    return parts >= MIN_TEXTUAL


def launch(results: Optional[List[Dict]] = None, query: str = "") -> None:
    """Open the TUI, optionally showing results from a CLI search."""
    if textual_available():
        from .app import LixploreApp
        LixploreApp(results=results, query=query).run()
        return

    found = textual_version()
    if found:
        print(f"The full-screen TUI needs Textual 4 or newer (found {found}):  pip install \"lixplore-cli[tui]\"")
    else:
        print("The full-screen TUI needs Textual (Python 3.9+):  pip install \"lixplore-cli[tui]\"")
    print("Using the basic TUI instead.\n")
    if results:
        from lixplore.utils.interactive_tui import launch_interactive_mode
        launch_interactive_mode(results)
    else:
        from lixplore.utils.enhanced_tui import launch_enhanced_tui
        launch_enhanced_tui()
