#!/usr/bin/env python3
"""
Enhanced TUI (Text User Interface) for Lixplore

Split-pane interface:
  Left panel  — navigation menu / article list
  Right panel — article preview / detail review
  [f]          toggle fullscreen review mode
"""

from __future__ import annotations
import sys
import time
from typing import List, Dict, Optional, Set

try:
    import tty as _tty
    import termios as _termios
    import select as _select
    _RAW_KEY_AVAILABLE = True
except ImportError:
    _RAW_KEY_AVAILABLE = False

from lixplore.utils.rich_check import check_rich, RICH_AVAILABLE as _RICH_CHECK

RICH_AVAILABLE = _RICH_CHECK

if RICH_AVAILABLE:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm, IntPrompt
    from rich.text import Text
    from rich import box
    from rich.align import Align


# ── colour palette ──────────────────────────────────────────────────────────
_ACCENT   = "cyan"
_DIM      = "dim"
_SUCCESS  = "green"
_WARN     = "yellow"
_ERROR    = "red"
_BORDER   = "cyan"


class EnhancedTUI:
    """Enhanced TUI with beautiful split-pane layout."""

    PAGE_SIZE = 10          # articles per page in the left panel

    def __init__(self):
        if not RICH_AVAILABLE:
            from lixplore.utils.rich_check import RICH_ERROR
            print("\nWARNING: Enhanced TUI not available.")
            if RICH_ERROR:
                print(f"  Reason: {RICH_ERROR}")
            print("\nRun: lixplore --check-tui  for diagnostics.")
            print("Falling back to basic mode...\n")
            self.console = None
        else:
            self.console = Console()

        self.current_results: List[Dict] = []
        self.selected_articles: Set[int] = set()   # 1-indexed
        self.annotation_manager = None
        self.cursor: int = 0        # 0-indexed position in current_results
        self.page: int = 0          # current page index

    # ── helpers ─────────────────────────────────────────────────────────────

    def _get_annotation_manager(self):
        if self.annotation_manager is None:
            try:
                from lixplore.utils.annotations import AnnotationManager
                self.annotation_manager = AnnotationManager()
            except Exception as e:
                if self.console:
                    self.console.print(f"[{_ERROR}]Cannot load annotations: {e}[/{_ERROR}]")
                return None
        return self.annotation_manager

    def _clamp_cursor(self):
        """Keep cursor inside current_results bounds."""
        total = len(self.current_results)
        if total == 0:
            self.cursor = 0
            return
        self.cursor = max(0, min(self.cursor, total - 1))
        # sync page
        self.page = self.cursor // self.PAGE_SIZE

    def _read_key(self) -> str:
        """Read one keypress without requiring Enter. Returns a normalised string."""
        if not _RAW_KEY_AVAILABLE:
            try:
                line = input().strip().lower()
                return line[0] if line else ""
            except (EOFError, KeyboardInterrupt):
                raise KeyboardInterrupt

        import os
        fd = sys.stdin.fileno()
        old = _termios.tcgetattr(fd)
        try:
            _tty.setraw(fd)
            # Use os.read to bypass Python's buffered IO — critical for arrow keys,
            # because sys.stdin.read() can silently consume extra bytes into its
            # internal buffer, making the follow-up select() see nothing.
            ch = os.read(fd, 1)
            if ch == b"\x03":       # Ctrl-C
                raise KeyboardInterrupt
            if ch == b"\x1b":
                if _select.select([fd], [], [], 0.05)[0]:
                    ch2 = os.read(fd, 1)
                    if ch2 == b"[":
                        ch3 = os.read(fd, 1)
                        return {b"A": "up", b"B": "down", b"C": "right", b"D": "left"}.get(ch3, "esc")
                return "esc"
            return ch.decode("utf-8", errors="replace")
        finally:
            _termios.tcsetattr(fd, _termios.TCSADRAIN, old)

    # ── article list renderer ────────────────────────────────────────────────

    def _render_article_list(self):
        """Full-width article list — no split pane."""
        self.console.clear()
        total   = len(self.current_results)
        n_pages = max(1, (total + self.PAGE_SIZE - 1) // self.PAGE_SIZE)
        start   = self.page * self.PAGE_SIZE
        end     = min(start + self.PAGE_SIZE, total)
        manager = self._get_annotation_manager()

        table = Table(
            box=box.SIMPLE_HEAD,
            expand=True,
            show_header=True,
            header_style=f"bold {_ACCENT}",
            show_edge=False,
            padding=(0, 1),
        )
        table.add_column("",        width=2,  no_wrap=True)
        table.add_column("#",       width=3,  justify="right", style=_DIM)
        table.add_column("Title",   ratio=5)
        table.add_column("Authors", ratio=2,  no_wrap=True)
        table.add_column("Year",    width=5,  justify="right")
        table.add_column("Source",  width=10, no_wrap=True)
        table.add_column("",        width=5,  justify="right")   # badge

        for abs_idx in range(start, end):
            article = self.current_results[abs_idx]
            num     = abs_idx + 1
            is_cur  = abs_idx == self.cursor
            is_sel  = num in self.selected_articles

            marker = "▶" if is_cur else ("●" if is_sel else "")

            title   = article.get("title", "No title")
            authors = article.get("authors", [])
            if isinstance(authors, list):
                a_str = ", ".join(authors[:2])
                if len(authors) > 2:
                    a_str += f" +{len(authors) - 2}"
            else:
                a_str = str(authors)

            year   = str(article.get("year",   ""))
            source = str(article.get("source", ""))

            badge = ""
            if manager:
                ann = manager.get_annotation_for_article(article)
                if ann and ann.get("rating"):
                    badge = f"★{ann['rating']}"
            if is_sel:
                badge = ("✓ " + badge).strip()

            if is_cur:
                row_style = "bold cyan"
            elif is_sel:
                row_style = _SUCCESS
            else:
                row_style = "white"

            table.add_row(
                marker, str(num), title, a_str, year, source, badge,
                style=row_style,
            )

        sel_hint = f" · {len(self.selected_articles)} selected" if self.selected_articles else ""
        panel_title = (
            f"[bold cyan]Results[/bold cyan]  "
            f"[dim]{total} articles · page {self.page + 1}/{n_pages}{sel_hint}[/dim]"
        )
        self.console.print(Panel(table, title=panel_title, border_style=_BORDER, box=box.ROUNDED))
        self.console.print(
            "[dim]  ↑/↓ j/k  navigate  ·  Enter/v  view article  ·  "
            "a  annotate  ·  s  select  ·  e  export  ·  n/p  pages  ·  g  jump  ·  b  back[/dim]"
        )

    # ── main menu helpers ────────────────────────────────────────────────────

    _MENU_ITEMS = [
        ("1", "Search Articles",  "Search PubMed, arXiv, Crossref …"),
        ("2", "My Annotations",   "Browse & filter saved notes"),
        ("3", "Statistics",       "Rating, status & tag overview"),
        ("4", "Export",           "Save annotations to file"),
        ("5", "Help",             "Guide & shortcuts"),
        ("6", "Exit",             "Quit Lixplore"),
    ]

    _MENU_DESCRIPTIONS: Dict[int, tuple] = {
        1: ("Search for Articles",
            "Search across multiple academic databases:\n\n"
            "  • PubMed    — Biomedical & life sciences\n"
            "  • arXiv     — Physics, math, CS & more\n"
            "  • Crossref  — DOI-indexed publications\n"
            "  • EuropePMC — European biomedical lit.\n\n"
            "Browse results, annotate papers with ratings,\n"
            "tags, and comments. Export to CSV / BibTeX / RIS."),
        2: ("Browse Annotations",
            "View all your annotated papers in one place.\n\n"
            "Filter by:\n"
            "  • Rating  (e.g. 4-5 stars)\n"
            "  • Status  (unread / reading / read)\n"
            "  • Priority (low / medium / high)\n"
            "  • Keyword search across all notes\n\n"
            "Annotations are stored locally and persist\n"
            "across sessions."),
        3: ("Statistics",
            "Get an overview of your reading activity:\n\n"
            "  • Total annotated articles\n"
            "  • Rating distribution chart\n"
            "  • Read-status breakdown\n"
            "  • Priority breakdown\n"
            "  • Unique tags & frequency\n"
            "  • Total comments written"),
        4: ("Export Annotations",
            "Export saved annotations to a file:\n\n"
            "  • Markdown — Human-readable notes\n"
            "  • JSON     — Machine-readable backup\n"
            "  • CSV      — Spreadsheet compatible\n\n"
            "Export regularly to back up your research\n"
            "notes and share with collaborators."),
        5: ("Help & Guide",
            "Quick reference for using Lixplore:\n\n"
            "  • How to search effectively\n"
            "  • Annotation best practices\n"
            "  • Keyboard shortcuts\n"
            "  • CLI usage examples\n\n"
            "Tip: lixplore --help  lists all CLI flags.\n"
            "     lixplore --check-tui  diagnoses issues."),
        6: ("Exit",
            "Quit Lixplore.\n\n"
            "Your annotations are automatically saved.\n"
            "See you next time!"),
    }

    def _left_main_menu(self, active: int) -> Panel:
        t = Text()
        t.append("\n")
        for num, name, desc in self._MENU_ITEMS:
            n = int(num)
            if n == active:
                t.append(f"  ▶ {num}. ", style="bold cyan")
                t.append(name + "\n",   style="bold white")
                t.append(f"       {desc}\n\n", style="dim cyan")
            else:
                t.append(f"    {num}. ", style=_ACCENT)
                t.append(name + "\n",   style="white")
                t.append("\n")
        return Panel(t, title="[bold cyan]Menu[/bold cyan]", border_style=_BORDER, box=box.ROUNDED)

    def _right_main_menu(self, active: int) -> Panel:
        name, body = self._MENU_DESCRIPTIONS.get(active, ("", ""))
        t = Text()
        t.append(f"\n{name}\n", style="bold white")
        t.append("  " + "─" * 38 + "\n\n", style=_DIM)
        t.append(body + "\n\n", style="white")
        t.append("\n  ↑/↓ navigate  ·  Enter select  ·  q quit\n", style=_DIM)
        return Panel(t, title="[bold cyan]About[/bold cyan]", border_style=_BORDER, box=box.ROUNDED)

    def _render_main_menu(self, active: int):
        self.console.clear()
        grid = Table.grid(expand=True)
        grid.add_column(ratio=2)
        grid.add_column(ratio=3)
        grid.add_row(self._left_main_menu(active), self._right_main_menu(active))
        self.console.print(grid)

    # ── public entry point ───────────────────────────────────────────────────

    def launch(self):
        """Launch the enhanced TUI."""
        if not RICH_AVAILABLE:
            self._launch_simple()
            return

        self._show_welcome()
        active = 1

        while True:
            try:
                self._render_main_menu(active)
                key = self._read_key()

                if key in ("j", "down", "+"):
                    active = min(6, active + 1)
                    continue
                if key in ("k", "up", "-"):
                    active = max(1, active - 1)
                    continue
                if key in ("\r", "\n", " ", "l", "right"):
                    choice = active
                elif key.isdigit() and key != "0":
                    active = int(key)
                    choice = active
                elif key in ("q", "esc"):
                    self.console.print("\n\n[yellow]Exiting Lixplore…[/yellow]\n")
                    break
                else:
                    continue

                if choice == 1:
                    self._search_workflow()
                elif choice == 2:
                    self._browse_annotations()
                elif choice == 3:
                    self._show_statistics()
                elif choice == 4:
                    self._export_annotations()
                elif choice == 5:
                    self._show_help_guide()
                elif choice == 6:
                    self.console.print("\n[yellow]Thanks for using Lixplore! Goodbye![/yellow]\n")
                    break

            except KeyboardInterrupt:
                self.console.print("\n\n[yellow]Exiting Lixplore…[/yellow]\n")
                break
            except Exception as e:
                self.console.print(f"[{_ERROR}]Error: {e}[/{_ERROR}]")

    def _show_welcome(self):
        self.console.clear()
        self.console.print(Panel(
            Align.center(Text.assemble(
                ("LIXPLORE\n",                  "bold cyan"),
                ("Academic Literature Explorer\n\n", "dim white"),
                ("Search  ·  Annotate  ·  Discover", _ACCENT),
            ), vertical="middle"),
            border_style=_ACCENT,
            box=box.DOUBLE,
            padding=(2, 4),
        ))
        time.sleep(0.6)

    # ── search workflow ──────────────────────────────────────────────────────

    def _search_workflow(self):
        self.console.clear()
        self.console.print(Panel(
            "[bold cyan]SEARCH FOR ARTICLES[/bold cyan]\n"
            "[dim]Enter your parameters below.[/dim]",
            border_style=_BORDER, box=box.ROUNDED,
        ))

        query = Prompt.ask("\n[cyan]Search query[/cyan]")
        if not query:
            return

        self.console.print("\n[bold]Database:[/bold]")
        databases = [
            ("1", "PubMed",       "Biomedical & life sciences"),
            ("2", "arXiv",        "Physics, math, CS"),
            ("3", "Crossref",     "Scholarly DOI works"),
            ("4", "EuropePMC",    "European biomedical"),
            ("5", "All databases","Comprehensive (slower)"),
        ]
        for num, name, desc in databases:
            marker = "[cyan]▶[/cyan]" if num == "1" else " "
            self.console.print(f"  {marker} {num}. [bold]{name}[/bold]  [dim]{desc}[/dim]")

        db_choice   = Prompt.ask("\n[cyan]Database[/cyan]", default="1")
        db_map      = {"1": "P", "2": "x", "3": "C", "4": "E", "5": "A"}
        source_flag = db_map.get(db_choice, "P")
        max_results = IntPrompt.ask("[cyan]Max results[/cyan]", default=20)

        dedup = False
        if db_choice == "5":
            dedup = Confirm.ask("Remove duplicates?", default=True)

        self.console.print(f"\n[cyan]Searching…[/cyan]\n")

        try:
            from lixplore import dispatcher

            source_names = {
                "pubmed": "PubMed", "crossref": "Crossref",
                "doaj": "DOAJ", "europepmc": "EuropePMC", "arxiv": "arXiv",
            }
            if source_flag == "A":
                sources = ["pubmed", "crossref", "doaj", "europepmc", "arxiv"]
            else:
                sources = [{"P": "pubmed", "x": "arxiv", "C": "crossref", "E": "europepmc"}[source_flag]]

            all_results: List[Dict] = []
            for source in sources:
                self.console.print(f"  Searching [cyan]{source_names[source]}[/cyan]…")
                try:
                    res = dispatcher.search(source=source, query=query, limit=max_results)
                    if res:
                        all_results.extend(res)
                        self.console.print(f"    [{_SUCCESS}]✓[/{_SUCCESS}] {len(res)} articles")
                except Exception as e:
                    self.console.print(f"    [{_WARN}]⚠[/{_WARN}] {e}")

            if dedup and len(sources) > 1 and all_results:
                self.console.print(f"\n  [cyan]Removing duplicates…[/cyan]")
                all_results = dispatcher.deduplicate_advanced(
                    all_results, strategy="auto",
                    title_threshold=0.85, keep_preference="first", merge_metadata=False,
                )

            if all_results:
                self.current_results = all_results
                self.cursor = 0
                self.page   = 0
                self.selected_articles.clear()
                self.console.print(f"\n[{_SUCCESS}]✓ Found {len(all_results)} articles[/{_SUCCESS}]")
                if Confirm.ask("Browse results in split-pane view?", default=True):
                    self._browse_results()
            else:
                self.console.print(f"\n[{_WARN}]No results found[/{_WARN}]")
                Prompt.ask("\nPress Enter")

        except Exception as e:
            self.console.print(f"\n[{_ERROR}]Search failed: {e}[/{_ERROR}]")
            import traceback
            self.console.print(f"[{_DIM}]{traceback.format_exc()}[/{_DIM}]")
            Prompt.ask("\nPress Enter")

    # ── results browser ───────────────────────────────────────────────────────

    def _browse_results(self):
        """Full-width article browser with arrow-key navigation."""
        if not self.current_results:
            return

        self._clamp_cursor()
        total   = len(self.current_results)
        n_pages = max(1, (total + self.PAGE_SIZE - 1) // self.PAGE_SIZE)

        while True:
            self._render_article_list()
            key = self._read_key()

            # ── navigation ──
            if key in ("j", "down"):
                if self.cursor < total - 1:
                    self.cursor += 1
                    self._clamp_cursor()

            elif key in ("k", "up"):
                if self.cursor > 0:
                    self.cursor -= 1
                    self._clamp_cursor()

            elif key == "n":
                if self.page < n_pages - 1:
                    self.page += 1
                    self.cursor = self.page * self.PAGE_SIZE
                    self._clamp_cursor()

            elif key == "p":
                if self.page > 0:
                    self.page -= 1
                    self.cursor = self.page * self.PAGE_SIZE
                    self._clamp_cursor()

            elif key == "g":
                num_str = Prompt.ask("[cyan]Jump to #[/cyan]").strip()
                try:
                    num = int(num_str)
                    if 1 <= num <= total:
                        self.cursor = num - 1
                        self._clamp_cursor()
                    else:
                        self.console.print(f"[{_ERROR}]Enter 1–{total}[/{_ERROR}]")
                        time.sleep(0.8)
                except ValueError:
                    pass

            # ── article actions ──
            elif key in ("v", "\r", "\n"):
                self._view_article_fullscreen(self.current_results[self.cursor], self.cursor + 1)

            elif key == "a":
                self._annotate_article(self.current_results[self.cursor], self.cursor + 1)

            elif key == "s":
                num = self.cursor + 1
                if num in self.selected_articles:
                    self.selected_articles.remove(num)
                else:
                    self.selected_articles.add(num)

            elif key == "e":
                if self.selected_articles:
                    self._export_selected_results()
                else:
                    self.console.print(f"[{_WARN}]No articles selected — press 's' first[/{_WARN}]")
                    time.sleep(1.0)

            elif key in ("b", "q", "esc"):
                break

    # ── fullscreen article view ───────────────────────────────────────────────

    def _view_article_fullscreen(self, article: Dict, number: int):
        """Show a single article full-width with complete details."""
        self.console.clear()

        t = Text()

        # ── title ──
        title = article.get("title", "No title")
        t.append(f"\n{title}\n", style="bold white")
        t.append("  " + "─" * 60 + "\n\n", style=_DIM)

        def row(label, value, vstyle="white"):
            t.append(f"  {label:<12}", style=f"bold {_ACCENT}")
            t.append(value + "\n",     style=vstyle)

        # ── authors (all of them) ──
        authors = article.get("authors", [])
        if authors:
            a_str = (", ".join(authors) if isinstance(authors, list) else str(authors))
            row("Authors", a_str)

        if article.get("journal"):  row("Journal", article["journal"])
        if article.get("year"):     row("Year",    str(article["year"]),   _WARN)
        if article.get("source"):   row("Source",  article["source"],      "magenta")
        if article.get("doi"):      row("DOI",     article["doi"],         _DIM)
        if article.get("url"):      row("URL",     article["url"],         f"{_DIM} blue")

        # ── annotation block ──
        manager = self._get_annotation_manager()
        if manager:
            ann = manager.get_annotation_for_article(article)
            if ann:
                t.append(f"\n  ── Annotation {'─' * 48}\n", style=f"{_WARN} dim")
                if ann.get("rating"):
                    stars = "★" * ann["rating"] + "☆" * (5 - ann["rating"])
                    t.append(f"  {'Rating':<12}", style=f"bold {_WARN}")
                    t.append(f"{stars}  ({ann['rating']}/5)\n", style=_WARN)
                if ann.get("tags"):
                    row("Tags",     ", ".join(ann["tags"]), _SUCCESS)
                if ann.get("read_status"):
                    row("Status",   ann["read_status"].title())
                if ann.get("priority"):
                    row("Priority", ann["priority"].title())
                if ann.get("comments"):
                    t.append(f"  {'Notes':<12}\n", style=f"bold {_WARN}")
                    for c in ann["comments"]:
                        t.append(f"    • {c['text']}\n", style="white")

        # ── full abstract (no truncation) ──
        abstract = article.get("abstract", "")
        if abstract:
            t.append(f"\n  ── Abstract {'─' * 48}\n\n", style=f"{_ACCENT} dim")
            t.append("  " + abstract.replace("\n", "\n  ") + "\n", style="white")
        else:
            t.append(f"\n  [dim]No abstract available.[/dim]\n")

        self.console.print(Panel(
            t,
            title=f"[bold cyan]Article #{number}[/bold cyan]",
            border_style=_BORDER,
            box=box.ROUNDED,
        ))
        self.console.print("[dim]  Press Enter to return to results list[/dim]")
        Prompt.ask("")

    # ── annotation dialog ────────────────────────────────────────────────────

    def _annotate_article(self, article: Dict, number: int):
        self.console.clear()
        title_short = (article.get("title", "No title")[:70] + "…"
                       if len(article.get("title", "")) > 70
                       else article.get("title", "No title"))

        self.console.print(Panel(
            f"[bold cyan]ANNOTATE  #  {number}[/bold cyan]\n"
            f"[dim]{title_short}[/dim]",
            border_style=_BORDER, box=box.ROUNDED,
        ))

        manager = self._get_annotation_manager()
        if not manager:
            self.console.print(f"[{_ERROR}]Annotation system not available[/{_ERROR}]")
            Prompt.ask("Press Enter")
            return

        existing = manager.get_annotation_for_article(article)
        if existing:
            self.console.print(f"\n[{_WARN}]Existing annotation:[/{_WARN}]")
            if existing.get("rating"):
                self.console.print(f"  Rating: {existing['rating']}/5")
            if existing.get("tags"):
                self.console.print(f"  Tags:   {', '.join(existing['tags'])}")
            self.console.print()

        rating = None
        if Confirm.ask("Add / update rating?", default=True):
            try:
                r = IntPrompt.ask("Rating (1–5)", default=5)
                rating = max(1, min(5, r))
            except Exception:
                pass

        tags = None
        if Confirm.ask("Add / update tags?", default=True):
            raw = Prompt.ask("Tags (comma-separated)  [dim]e.g. important, cite[/dim]")
            if raw:
                tags = [t.strip() for t in raw.split(",") if t.strip()]

        comment = None
        if Confirm.ask("Add a note / comment?", default=True):
            comment = Prompt.ask("Your note")

        priority = None
        if Confirm.ask("Set priority?", default=False):
            self.console.print("  1. Low   2. Medium   3. High")
            p = IntPrompt.ask("Priority", default=2)
            priority = {1: "low", 2: "medium", 3: "high"}.get(p, "medium")

        read_status = None
        if Confirm.ask("Set read status?", default=False):
            self.console.print("  1. Unread   2. Reading   3. Read")
            s = IntPrompt.ask("Status", default=1)
            read_status = {1: "unread", 2: "reading", 3: "read"}.get(s, "unread")

        try:
            manager.annotate(
                article, comment=comment, rating=rating,
                tags=tags, read_status=read_status, priority=priority,
            )
            self.console.print(f"\n[{_SUCCESS}]✓ Annotation saved![/{_SUCCESS}]")
        except Exception as e:
            self.console.print(f"\n[{_ERROR}]Failed to save: {e}[/{_ERROR}]")

        Prompt.ask("\nPress Enter")

    # ── export selected ──────────────────────────────────────────────────────

    def _export_selected_results(self):
        selected = [self.current_results[n - 1] for n in sorted(self.selected_articles)]
        formats  = ["CSV", "JSON", "BibTeX", "RIS", "Excel", "EndNote"]

        self.console.print("\n[bold]Export Format:[/bold]")
        for i, f in enumerate(formats, 1):
            self.console.print(f"  {i}. {f}")

        try:
            choice = IntPrompt.ask("\nFormat (1–6)", default=1)
            if 1 <= choice <= len(formats):
                from lixplore.utils.export import export_results
                fmt = formats[choice - 1].lower()
                self.console.print(f"\n[cyan]Exporting {len(selected)} article(s)…[/cyan]")
                out = export_results(selected, fmt)
                if out:
                    self.console.print(f"[{_SUCCESS}]✓ Saved to: {out}[/{_SUCCESS}]")
                else:
                    self.console.print(f"[{_ERROR}]Export failed[/{_ERROR}]")
            else:
                self.console.print(f"[{_ERROR}]Invalid choice[/{_ERROR}]")
        except Exception as e:
            self.console.print(f"[{_ERROR}]Export error: {e}[/{_ERROR}]")

        Prompt.ask("\nPress Enter")

    # ── annotations browser ──────────────────────────────────────────────────

    def _browse_annotations(self):
        self.console.clear()
        manager = self._get_annotation_manager()
        if not manager:
            self.console.print(f"[{_ERROR}]Annotation system not available[/{_ERROR}]")
            Prompt.ask("Press Enter")
            return

        while True:
            self.console.clear()
            self.console.print(Panel(
                "[bold cyan]MY ANNOTATIONS[/bold cyan]",
                border_style=_BORDER, box=box.ROUNDED,
            ))
            self.console.print("  1. All annotations")
            self.console.print("  2. High-rated (4-5 ★)")
            self.console.print("  3. Unread articles")
            self.console.print("  4. High priority")
            self.console.print("  5. Search by keyword")
            self.console.print("  6. Back")

            try:
                choice = IntPrompt.ask("\nChoice", default=1)
            except Exception:
                break

            if choice == 6:
                break

            try:
                if   choice == 1: annotations = manager.list_all()
                elif choice == 2: annotations = manager.list_all({"min_rating": 4})
                elif choice == 3: annotations = manager.list_all({"read_status": "unread"})
                elif choice == 4: annotations = manager.list_all({"priority": "high"})
                elif choice == 5:
                    kw = Prompt.ask("Keyword")
                    res = manager.search_annotations(kw)
                    annotations = [{"article_id": r["article_id"], "annotation": r["annotation"]} for r in res]
                else:
                    continue
            except Exception as e:
                self.console.print(f"[{_ERROR}]{e}[/{_ERROR}]")
                Prompt.ask("Press Enter")
                continue

            if not annotations:
                self.console.print(f"\n[{_WARN}]No annotations found[/{_WARN}]")
                Prompt.ask("Press Enter")
                continue

            self._display_annotation_list(annotations)
            Prompt.ask("\nPress Enter")

    def _display_annotation_list(self, annotations: List[Dict]):
        self.console.print(f"\n[bold]Found {len(annotations)} annotation(s):[/bold]\n")
        table = Table(show_header=True, box=box.ROUNDED)
        table.add_column("#",      style=_ACCENT,   width=4)
        table.add_column("Rating", style=_WARN,     width=8)
        table.add_column("Title",  style="white")
        table.add_column("Tags",   style=_SUCCESS,  width=20)
        table.add_column("Status", style="magenta", width=10)

        for i, item in enumerate(annotations, 1):
            ann  = item["annotation"]
            info = ann.get("article_info", {})
            rating = f"{ann['rating']}/5" if ann.get("rating") else ""
            title  = (info.get("title", "No title")[:38] + "…"
                      if len(info.get("title", "")) > 38
                      else info.get("title", "No title"))
            tags   = ", ".join(ann.get("tags", [])[:3])
            if len(ann.get("tags", [])) > 3:
                tags += "…"
            status = ann.get("read_status", "unread").title()
            table.add_row(str(i), rating, title, tags, status)

        self.console.print(table)

    # ── statistics ───────────────────────────────────────────────────────────

    def _show_statistics(self):
        self.console.clear()
        manager = self._get_annotation_manager()
        if not manager:
            self.console.print(f"[{_ERROR}]Annotation system not available[/{_ERROR}]")
            Prompt.ask("Press Enter")
            return

        stats = manager.get_statistics()
        t = Text()
        t.append(f"\n  Total annotated: ", style="bold cyan")
        t.append(f"{stats['total']}\n\n", style="bold white")

        if stats.get("by_rating"):
            t.append("  Rating distribution\n", style="bold cyan")
            for rating in sorted(stats["by_rating"].keys(), reverse=True):
                count = stats["by_rating"][rating]
                bar   = "█" * min(count, 40)
                t.append(f"  {'★' * rating:<5}", style=_WARN)
                t.append(f" {bar} {count}\n",    style=_WARN)
            t.append("\n")

        if stats.get("by_status"):
            t.append("  Read status\n", style="bold cyan")
            for status, count in stats["by_status"].items():
                t.append(f"  {status.title():<12}", style="white")
                t.append(f"{count}\n",              style=_WARN)
            t.append("\n")

        if stats.get("by_priority"):
            t.append("  Priority\n", style="bold cyan")
            for pri, count in stats["by_priority"].items():
                t.append(f"  {pri.title():<12}", style="white")
                t.append(f"{count}\n",           style=_WARN)
            t.append("\n")

        t.append("  Comments\n", style="bold cyan")
        t.append(f"  With comments    {stats['with_comments']}\n", style="white")
        t.append(f"  Total comments   {stats['total_comments']}\n\n", style="white")

        t.append("  Tags\n", style="bold cyan")
        t.append(f"  Unique tags      {stats['total_tags']}\n", style="white")
        if stats.get("unique_tags"):
            preview = ", ".join(stats["unique_tags"][:12])
            if len(stats["unique_tags"]) > 12:
                preview += "…"
            t.append(f"  {preview}\n", style=_DIM)

        self.console.print(Panel(t, title="[bold cyan]Statistics[/bold cyan]", border_style=_BORDER, box=box.ROUNDED))
        Prompt.ask("\nPress Enter")

    # ── export annotations ───────────────────────────────────────────────────

    def _export_annotations(self):
        self.console.clear()
        manager = self._get_annotation_manager()
        if not manager:
            self.console.print(f"[{_ERROR}]Annotation system not available[/{_ERROR}]")
            Prompt.ask("Press Enter")
            return

        self.console.print(Panel(
            "[bold cyan]EXPORT ANNOTATIONS[/bold cyan]",
            border_style=_BORDER, box=box.ROUNDED,
        ))
        formats = ["Markdown", "JSON", "CSV"]
        for i, f in enumerate(formats, 1):
            self.console.print(f"  {i}. {f}")

        try:
            choice = IntPrompt.ask("\nFormat (1–3)", default=1)
            if 1 <= choice <= 3:
                fmt = {1: "markdown", 2: "json", 3: "csv"}[choice]
                out = manager.export_annotations(format=fmt)
                self.console.print(f"[{_SUCCESS}]✓ Exported to: {out}[/{_SUCCESS}]")
            else:
                self.console.print(f"[{_ERROR}]Invalid choice[/{_ERROR}]")
        except Exception as e:
            self.console.print(f"[{_ERROR}]Export error: {e}[/{_ERROR}]")

        Prompt.ask("\nPress Enter")

    # ── help guide ───────────────────────────────────────────────────────────

    def _show_help_guide(self):
        self.console.clear()
        help_text = """
[bold cyan]Split-Pane TUI[/bold cyan]

  The TUI shows a [bold]left panel[/bold] (article list / menu) and a
  [bold]right panel[/bold] (article preview / detail).

  Press [bold cyan]f[/bold cyan] at any time to toggle [bold]fullscreen[/bold] for the right panel.

[bold yellow]Browse Commands[/bold yellow]

  [cyan]↑ / ↓[/cyan]        move cursor (arrow keys)
  [cyan]j / k[/cyan]        move cursor down / up (vim-style)
  [cyan]n / p[/cyan]        next / previous page
  [cyan]g[/cyan]            jump to article number (prompted)
  [cyan]Enter / v[/cyan]    view article in fullscreen detail
  [cyan]a[/cyan]            annotate current article
  [cyan]s[/cyan]            toggle selection of current article
  [cyan]e[/cyan]            export selected articles
  [cyan]f[/cyan]            toggle fullscreen review panel
  [cyan]b / q / Esc[/cyan]  back / quit

[bold yellow]Annotations[/bold yellow]

  • Rate articles 1–5 ★ to track quality
  • Tag for easy organisation (e.g. cite, review-later)
  • Add notes while reading
  • Set read status & priority
  • Export to Markdown / JSON / CSV regularly

[bold yellow]CLI Quick Reference[/bold yellow]

  lixplore -P -q "topic" -m 20          search PubMed
  lixplore -A -q "topic" -D -X xlsx     all sources, dedup, export Excel
  lixplore --tui                         launch this TUI
  lixplore --check-tui                   diagnose Rich installation
"""
        self.console.print(Panel(help_text, title="[bold yellow]Help & Guide[/bold yellow]",
                                 border_style="yellow", box=box.ROUNDED))
        Prompt.ask("\nPress Enter")

    # ── simple fallback ──────────────────────────────────────────────────────

    def _launch_simple(self):
        print("\n" + "=" * 70)
        print("LIXPLORE — ENHANCED MODE (Basic)")
        print("=" * 70)
        print("\nFor the full split-pane TUI, install Rich:")
        if "pipx" in sys.executable.lower() or ".local/pipx" in getattr(sys, "prefix", ""):
            print("  pipx inject lixplore-cli rich")
        else:
            print("  pip install rich")
        print("\nRun 'lixplore --check-tui' for diagnostics.")
        print("=" * 70)

        while True:
            print("\nMain Menu:")
            print("  1. Search for articles")
            print("  2. Browse annotations")
            print("  3. View statistics")
            print("  4. Export annotations")
            print("  5. Exit")
            try:
                choice = input("\nYour choice [1]: ").strip() or "1"
                if choice == "5":
                    print("\nGoodbye!")
                    break
                elif choice in ("1", "2", "3", "4"):
                    print(f"\n[Feature {choice} — Rich library required for full TUI]")
                    input("Press Enter to continue…")
                else:
                    print("Invalid choice")
            except KeyboardInterrupt:
                print("\n\nExiting…")
                break


# ── public API ───────────────────────────────────────────────────────────────

def launch_enhanced_tui(results=None):
    """
    Launch the enhanced split-pane TUI.

    Args:
        results: Optional pre-loaded search results to browse immediately.
    """
    tui = EnhancedTUI()

    if results:
        tui.current_results = results
        tui.cursor = 0
        tui.page   = 0
        if RICH_AVAILABLE and tui.console:
            if Confirm.ask("\nBrowse results in split-pane view?", default=True):
                tui._browse_results()
        else:
            print("Results available. Launch TUI with: lixplore --tui")
    else:
        tui.launch()


if __name__ == "__main__":
    launch_enhanced_tui()
