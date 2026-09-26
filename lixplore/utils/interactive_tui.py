#!/usr/bin/env python3
"""
Interactive TUI Mode — delegates to the enhanced split-pane TUI.

Keeping this module for backwards compatibility; all display logic now
lives in enhanced_tui.py.
"""

from __future__ import annotations
import sys
from typing import List, Dict

from lixplore.utils.rich_check import RICH_AVAILABLE as _RICH_CHECK

RICH_AVAILABLE = _RICH_CHECK

if RICH_AVAILABLE:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich import box


def launch_interactive_mode(results: List[Dict]):
    """
    Launch interactive TUI mode for browsing results.

    Delegates to the enhanced split-pane TUI when Rich is available,
    otherwise falls back to a simple text browser.

    Args:
        results: List of article dictionaries.
    """
    if not results:
        print("No results to display in interactive mode.")
        return

    if RICH_AVAILABLE:
        # Use the enhanced split-pane TUI
        from lixplore.utils.enhanced_tui import EnhancedTUI
        tui = EnhancedTUI()
        tui.current_results = results
        tui.cursor = 0
        tui.page   = 0
        tui._browse_results()
    else:
        launch_simple_tui(results)


def launch_simple_tui(results: List[Dict]):
    """
    Simple text-based fallback browser (no Rich required).

    Args:
        results: List of article dictionaries.
    """
    print("\n" + "=" * 80)
    print("LIXPLORE INTERACTIVE MODE (Basic)")
    print("=" * 80)
    print("For the full split-pane TUI, install Rich:")
    if "pipx" in sys.executable.lower() or ".local/pipx" in getattr(sys, "prefix", ""):
        print("  pipx inject lixplore-cli rich")
    else:
        print("  pip install rich")
    print("Run 'lixplore --check-tui' for diagnostics.")
    print("=" * 80 + "\n")

    page_size  = 10
    total      = len(results)
    n_pages    = max(1, (total + page_size - 1) // page_size)
    cur_page   = 0
    selected   = set()

    while True:
        start = cur_page * page_size
        end   = min(start + page_size, total)

        print(f"\nPage {cur_page + 1}/{n_pages}  ({total} articles)")
        print("-" * 80)
        for i in range(start, end):
            art   = results[i]
            num   = i + 1
            check = "[X]" if num in selected else "[ ]"
            title  = (art.get("title", "No title") or "")[:55]
            year   = str(art.get("year", "N/A"))
            source = str(art.get("source", ""))[:10]
            print(f"{num:3d} {check} {title:55s} {year:6s} {source}")

        if selected:
            print(f"\n{len(selected)} article(s) selected")

        print("\nCommands: (n)ext (p)rev (v)iew (s)elect (e)xport (q)uit (h)elp")
        cmd = input("\n> ").lower().strip()

        if cmd in ("q", "quit", "exit"):
            print("\nExiting interactive mode…")
            break

        elif cmd in ("n", "next"):
            if cur_page < n_pages - 1:
                cur_page += 1
            else:
                print("Already on last page")

        elif cmd in ("p", "prev", "previous"):
            if cur_page > 0:
                cur_page -= 1
            else:
                print("Already on first page")

        elif cmd in ("h", "help"):
            print("\n" + "=" * 80)
            print("  n / next   — next page")
            print("  p / prev   — previous page")
            print("  v <num>    — view article details")
            print("  s <num>    — toggle selection")
            print("  e          — export selected")
            print("  q          — quit")
            print("=" * 80)
            input("\nPress Enter to continue…")

        elif cmd.startswith("v"):
            raw = cmd[1:].strip() or input("Article number: ").strip()
            try:
                num = int(raw)
                if 1 <= num <= total:
                    art = results[num - 1]
                    print("\n" + "=" * 80)
                    print(f"ARTICLE #{num}")
                    print("=" * 80)
                    print(f"Title:   {art.get('title', 'No title')}")
                    authors = art.get("authors", [])
                    if isinstance(authors, list):
                        print(f"Authors: {', '.join(authors[:5])}")
                    print(f"Year:    {art.get('year', 'N/A')}")
                    print(f"Journal: {art.get('journal', 'N/A')}")
                    print(f"DOI:     {art.get('doi', 'N/A')}")
                    print(f"Source:  {art.get('source', 'N/A')}")
                    if art.get("abstract"):
                        print(f"\nAbstract:\n{art['abstract'][:600]}…")
                    print("=" * 80)
                    input("\nPress Enter to return…")
                else:
                    print(f"Must be 1–{total}")
            except ValueError:
                print("Invalid number")

        elif cmd.startswith("s"):
            raw = cmd[1:].strip() or input("Article number: ").strip()
            try:
                num = int(raw)
                if 1 <= num <= total:
                    if num in selected:
                        selected.remove(num)
                        print(f"Article #{num} deselected")
                    else:
                        selected.add(num)
                        print(f"Article #{num} selected")
                else:
                    print(f"Must be 1–{total}")
            except ValueError:
                print("Invalid number")

        elif cmd in ("e", "export"):
            if not selected:
                print("No articles selected")
                continue
            print("\nFormats: 1. CSV  2. JSON  3. BibTeX  4. RIS")
            try:
                choice = int(input("Format (1-4): "))
                fmts   = ["csv", "json", "bibtex", "ris"]
                if 1 <= choice <= 4:
                    sel_arts = [results[n - 1] for n in selected]
                    from lixplore.utils.export import export_results
                    out = export_results(sel_arts, fmts[choice - 1])
                    print(f"Exported to: {out}" if out else "Export failed")
                else:
                    print("Invalid choice")
            except (ValueError, Exception) as e:
                print(f"Error: {e}")

        else:
            print(f"Unknown command: {cmd}.  Type 'h' for help.")


if __name__ == "__main__":
    test = [
        {"title": f"Article {i}", "authors": ["Author A"], "year": 2020 + i,
         "source": "PubMed", "doi": f"10.1234/test{i}"}
        for i in range(25)
    ]
    launch_interactive_mode(test)
