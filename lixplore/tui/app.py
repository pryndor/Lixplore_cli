"""
Lixplore research cockpit: sidebar, results table and live preview.

    ┌ search bar · source toggles ─────────────────────────────┐
    │ sidebar │ results / library / alerts / stats │ preview  │
    └ footer: key hints ───────────────────────────────────────┘
"""

import json
import os
import webbrowser
from datetime import date, timedelta
from typing import Dict, List, Optional, Set

from rich.align import Align
from rich.console import Group
from rich.rule import Rule
from rich.text import Text
from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import (Button, ContentSwitcher, DataTable, Footer, Input, Label,
                             OptionList, Select, Static)
from textual.widgets.option_list import Option

from .modals import AnnotateScreen, ExportScreen, HelpScreen

SOURCES = [  # (key, label, colour, on by default)
    ("pubmed", "PubMed", "#4ea1ff", True),
    ("europepmc", "EuropePMC", "#3ddc97", True),
    ("arxiv", "arXiv", "#ff6b6b", True),
    ("crossref", "Crossref", "#ffb454", False),
    ("doaj", "DOAJ", "#c792ea", False),
]
SOURCE_LABEL = {k: label for k, label, _, _ in SOURCES}
SOURCE_COLOUR = {k: colour for k, _, colour, _ in SOURCES}
SORTS = ["relevance", "newest", "oldest", "title", "source"]
SETTINGS_FILE = os.path.expanduser("~/.lixplore/tui.json")
HISTORY_FILE = os.path.expanduser("~/.lixplore_history.json")
DEFAULT_THEME = "tokyo-night"

LOGO = r"""
 _     _            _
| |   (_)_  ___ __ | | ___  _ __ ___
| |   | \ \/ / '_ \| |/ _ \| '__/ _ \
| |___| |>  <| |_) | | (_) | | |  __/
|_____|_/_/\_\ .__/|_|\___/|_|  \___|
             |_|
"""


# ---------------------------------------------------------------- rendering helpers

def _authors(article: Dict, limit: int = 2) -> str:
    authors = article.get("authors") or []
    if isinstance(authors, str):
        authors = [a.strip() for a in authors.split(",") if a.strip()]
    if not authors:
        return ""
    return ", ".join(authors[:limit]) + (f" +{len(authors) - limit}" if len(authors) > limit else "")


def _source_badge(source: str) -> Text:
    return Text(SOURCE_LABEL.get(source, source or "?"), style=f"bold {SOURCE_COLOUR.get(source, 'white')}")


def _link(article: Dict) -> str:
    if article.get("url"):
        return article["url"]
    if article.get("doi"):
        return f"https://doi.org/{article['doi']}"
    return ""


def render_article(article: Dict, annotation: Optional[Dict]) -> Group:
    """The preview / reader view of one paper."""
    parts = [Text(article.get("title") or "Untitled", style="bold"), Text("")]
    if article.get("authors"):
        authors = article["authors"]
        parts.append(Text(", ".join(authors) if isinstance(authors, list) else str(authors), style="italic"))
    meta = Text()
    for bit in (article.get("journal"), str(article.get("year") or "")):
        if bit:
            meta.append(bit + "  ·  ", style="dim")
    meta.append_text(_source_badge(article.get("source", "")))
    parts.append(meta)

    link = _link(article)
    if article.get("doi"):
        parts.append(Text(f"doi:{article['doi']}", style=f"dim link https://doi.org/{article['doi']}"))
    if link:
        parts.append(Text("↗ " + link, style=f"underline link {link}"))

    if annotation:
        parts += [Text(""), Rule("Your notes", style="dim", align="left")]
        line = Text()
        if annotation.get("rating"):
            line.append("★" * annotation["rating"] + "☆" * (5 - annotation["rating"]) + "   ", style="bold yellow")
        status = annotation.get("read_status") or "unread"
        line.append({"unread": "○ unread", "reading": "◐ reading", "read": "● read"}.get(status, status) + "   ")
        priority = annotation.get("priority") or "medium"
        line.append(f"▲ {priority}", style={"high": "bold red", "medium": "yellow", "low": "dim"}.get(priority, ""))
        parts.append(line)
        if annotation.get("tags"):
            tags = Text()
            for tag in annotation["tags"]:
                tags.append(f" {tag} ", style="reverse")
                tags.append(" ")
            parts.append(tags)
        for c in annotation.get("comments") or []:
            parts.append(Text("❝ " + c.get("text", ""), style="italic"))

    parts += [Text(""), Rule("Abstract", style="dim", align="left")]
    abstract = (article.get("abstract") or "").strip()
    if abstract:
        parts.append(Text(abstract))
    elif "abstract" not in article:  # a Library entry: annotations don't store abstracts
        parts.append(Text("Not stored in your library. Press o to open the paper.", style="dim italic"))
    else:
        parts.append(Text("No abstract available.", style="dim italic"))
    return Group(*parts)


# ---------------------------------------------------------------- widgets

class Chip(Static, can_focus=True):
    """A clickable on/off chip, used for the database and dedupe toggles."""

    BINDINGS = [Binding("space,enter", "toggle", "Toggle", show=False)]
    value: reactive = reactive(True)

    def __init__(self, label: str, colour: str, value: bool, id: str):
        super().__init__(id=id, classes="chip")
        self.label, self.colour = label, colour
        self.set_reactive(Chip.value, value)

    def render(self) -> Text:
        if self.value:
            return Text(f"● {self.label}", style=f"bold {self.colour}")
        return Text(f"○ {self.label}", style="dim")

    def action_toggle(self) -> None:
        self.value = not self.value

    def on_click(self) -> None:
        self.action_toggle()


# ---------------------------------------------------------------- tables

class ResultsTable(DataTable):
    """Search results. Its bindings show in the footer while it has focus."""

    BINDINGS = [
        Binding("enter", "app.read", "Read"),
        Binding("o", "app.open", "Browser"),
        Binding("a", "app.annotate_current", "Annotate"),
        Binding("space", "app.toggle_select", "Select"),
        Binding("e", "app.export", "Export"),
        Binding("f", "app.filter", "Filter"),
        Binding("s", "app.sort", "Sort"),
        Binding("A", "app.select_all", "Select all", show=False),
        Binding("x", "app.clear_selection", "Clear selection", show=False),
    ] + [Binding(str(n), f"app.rate({n})", "Rate 1-5" if n == 1 else f"Rate {n}", show=n == 1)
         for n in range(1, 6)]


class LibraryTable(DataTable):
    BINDINGS = [
        Binding("enter", "app.read", "Read"),
        Binding("o", "app.open", "Browser"),
        Binding("a", "app.annotate_current", "Annotate"),
    ] + [Binding(str(n), f"app.rate({n})", "Rate 1-5" if n == 1 else f"Rate {n}", show=n == 1)
         for n in range(1, 6)]


# ---------------------------------------------------------------- reader

class ReaderScreen(ModalScreen[None]):
    """Full-screen reading view for one paper."""

    BINDINGS = [
        Binding("escape,q,enter", "close", "Back"),
        Binding("o", "open", "Open in browser"),
        Binding("a", "annotate", "Annotate"),
    ]

    def __init__(self, article: Dict, annotation_manager):
        super().__init__()
        self.article = article
        self.manager = annotation_manager

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="reader"):
            yield Static(id="reader-body")
        yield Footer()

    def on_mount(self) -> None:
        self._refresh()
        self.query_one("#reader").focus()

    def _refresh(self) -> None:
        ann = self.manager.get_annotation_for_article(self.article) if self.manager else None
        self.query_one("#reader-body", Static).update(render_article(self.article, ann))

    def action_close(self) -> None:
        self.dismiss(None)

    def action_open(self) -> None:
        self.app.open_article(self.article)

    def action_annotate(self) -> None:
        self.app.annotate(self.article, after=self._refresh)


# ---------------------------------------------------------------- app

class LixploreApp(App):
    TITLE = "Lixplore"
    CSS = """
    Screen { layout: vertical; }

    #topbar { height: 3; padding: 1 1; background: $panel; }
    #logo { width: auto; padding: 0 2 0 1; color: $accent; text-style: bold; }
    #query { width: 1fr; margin-right: 2; background: $surface; padding: 0 1; }
    #query:focus { background: $background; }
    #sources { width: auto; height: 1; margin-right: 1; }
    .chip { width: auto; padding: 0 1; }
    .chip:hover { background: $boost; }
    .chip:focus { background: $boost; text-style: underline; }
    .sep { width: auto; color: $text-muted; padding: 0 1; }
    #max { width: 6; margin-right: 1; background: $surface; }
    #go { min-width: 10; }

    #body { height: 1fr; }
    #sidebar { width: 24; background: $panel; padding: 1 1; }
    #nav { height: auto; border: none; background: $panel; padding: 0; }
    #nav > .option-list--option { padding: 0 0; }
    #nav { padding-left: 0; }
    #recent-title { color: $text-muted; margin: 1 0 0 1; text-style: bold; }
    #recent > .option-list--option { padding: 0 1; }
    #recent { height: 1fr; border: none; background: $panel; }

    #main { width: 1fr; }
    #main > Vertical { height: 1fr; }
    .status { height: 1; padding: 0 1; color: $text-muted; background: $boost; }
    #filter { display: none; margin: 0 1; }
    #filter.visible { display: block; }
    DataTable { height: 1fr; overflow-x: hidden; }
    #empty { height: 1fr; content-align: center middle; color: $text-muted; }
    #lib-bar { height: 1; margin: 0 1; }
    #lib-filter { width: 26; }
    #lib-search { width: 1fr; }
    #stats-view { padding: 1 2; }

    #preview { width: 38%; max-width: 76; border-left: tall $panel; padding: 1 2; }
    .narrow #preview, .no-preview #preview { display: none; }
    .tiny #sidebar { display: none; }
    .narrow #logo, .narrow .sep { display: none; }
    .narrow #query { min-width: 24; }

    #reader { padding: 1 4; max-width: 110; }
    ReaderScreen { align: center top; }

    AnnotateScreen, ExportScreen, HelpScreen { align: center middle; }
    #dialog { width: 72; height: auto; max-height: 90%; background: $surface;
              border: round $accent; padding: 1 2; }
    #dialog.help { width: 90; height: 90%; }
    .dialog-title { text-style: bold; color: $accent; margin-bottom: 1; }
    .dialog-subtitle { margin-bottom: 1; }
    #annotate-grid, #export-grid { grid-size: 2; grid-columns: 12 1fr; grid-rows: 1; grid-gutter: 1 1;
                                   height: auto; }
    .section { margin-top: 1; color: $text-muted; text-style: bold; }
    #old-notes { height: auto; max-height: 6; }
    #note { height: 5; }
    .buttons { height: auto; align-horizontal: right; margin-top: 1; }
    .buttons Button { margin-left: 2; }
    """

    BINDINGS = [
        # Ctrl keys first: many terminals grab F-keys (xfce4-terminal opens its help on F1)
        Binding("ctrl+f,f1", "view('results')", "Search", show=False),
        Binding("ctrl+l,f2", "view('library')", "Library", show=False),
        Binding("ctrl+n,f3", "view('alerts')", "Alerts", show=False),
        Binding("ctrl+t,f4", "view('stats')", "Stats", show=False),
        Binding("escape", "back", "Back"),
        Binding("slash", "focus_search", "New search"),
        Binding("question_mark", "help", "Help"),
        Binding("q", "quit", "Quit"),
    ]

    def __init__(self, results: Optional[List[Dict]] = None, query: str = ""):
        super().__init__()
        self.results: List[Dict] = list(results or [])
        self.shown: List[int] = []
        self.selected: Set[int] = set()
        self.sort_mode = "relevance"
        self.initial_query = query
        self.library_items: List[Dict] = []
        self.alerts: List = []
        self._recent_queries: Dict[str, str] = {}
        self._view_history: List[str] = []  # for Esc = back
        self._manager = None

    # -------------------------------------------------- layout

    def compose(self) -> ComposeResult:
        with Horizontal(id="topbar"):
            yield Static("◆ Lixplore", id="logo")
            yield Input(placeholder='Search papers…  AND · OR · NOT · "phrases" · (groups)', id="query",
                        compact=True)
            with Horizontal(id="sources"):
                for key, label, colour, on_default in SOURCES:
                    yield Chip(label, colour, on_default, id=f"src-{key}")
                yield Static("│", classes="sep")
                yield Chip("Dedupe", "white", True, id="dedupe")
            yield Input("20", id="max", type="integer", compact=True)
            yield Button("Search", id="go", variant="primary", compact=True)
        with Horizontal(id="body"):
            with Vertical(id="sidebar"):
                yield OptionList(
                    *[Option(Text.assemble((f" {name:<14}", "bold"), (key, "dim")), id=view)
                      for view, name, key in (("results", "Search", "^F"), ("library", "Library", "^L"),
                                              ("alerts", "Alerts", "^N"), ("stats", "Stats", "^T"))],
                    id="nav",
                )
                yield Label("RECENT", id="recent-title")
                yield OptionList(id="recent")
            with ContentSwitcher(initial="results", id="main"):
                with Vertical(id="results"):
                    yield Input(placeholder="Filter shown results…  (Esc to clear)", id="filter", compact=True)
                    yield Static(Align.center(Group(
                        Text(LOGO, style="bold #7aa2f7"),
                        Text("Search PubMed, Europe PMC, arXiv, Crossref and DOAJ at once.\n"),
                        Text.assemble(("Enter", "bold"), " search   ", ("?", "bold"), " keys   ",
                                      ("Ctrl+P", "bold"), " commands   ", ("Ctrl+L", "bold"), " your library",
                                      style="dim"),
                    ), vertical="middle"), id="empty")
                    yield ResultsTable(id="table", cursor_type="row", zebra_stripes=True)
                    yield Static("", id="results-status", classes="status")
                with Vertical(id="library"):
                    with Horizontal(id="lib-bar"):
                        yield Select([("All annotated", "all"), ("★ 4 and up", "top"), ("Unread", "unread"),
                                      ("Reading", "reading"), ("High priority", "high"), ("With notes", "notes")],
                                     value="all", allow_blank=False, id="lib-filter", compact=True)
                        yield Input(placeholder="Search titles, tags and notes…", id="lib-search", compact=True)
                    yield LibraryTable(id="lib-table", cursor_type="row", zebra_stripes=True)
                    yield Static("", id="lib-status", classes="status")
                with Vertical(id="alerts"):
                    yield DataTable(id="alert-table", cursor_type="row", zebra_stripes=True)
                    yield Static("", id="alert-status", classes="status")
                with VerticalScroll(id="stats"):
                    yield Static(id="stats-view")
            with VerticalScroll(id="preview"):
                yield Static(Text("Select a paper to preview it here.", style="dim"), id="preview-body")
        yield Footer()

    def on_mount(self) -> None:
        try:
            self.theme = self._load_settings().get("theme", DEFAULT_THEME)
        except Exception:
            self.theme = DEFAULT_THEME
        self.query_one("#max", Input).tooltip = "Max results per database"
        table = self.query_one("#table", DataTable)
        table.add_column("", key="mark", width=4)
        table.add_column("Title", key="title", width=40)
        table.add_column("First author", key="authors", width=16)
        table.add_column("Year", key="year", width=4)
        table.add_column("Source", key="source", width=9)
        lib = self.query_one("#lib-table", DataTable)
        for key, label, width in (("rating", "★", 5), ("title", "Title", 50), ("tags", "Tags", 14),
                                  ("status", "Status", 8), ("priority", "Priority", 8)):
            lib.add_column(label, key=key, width=width)
        alerts = self.query_one("#alert-table", DataTable)
        alerts.add_column("Alert", key="name", width=20)
        alerts.add_column("Query", key="query", width=50)
        alerts.add_column("Sources", key="sources", width=28)

        self._load_recent()
        if self.results:
            self._rebuild_table()
            table.focus()
            if self.initial_query:
                self.query_one("#query", Input).value = self.initial_query
        else:
            self.query_one("#query", Input).focus()
        self._update_empty()
        self.call_after_refresh(self._fit_columns)

    def watch_theme(self, theme: str) -> None:
        settings = self._load_settings()
        if settings.get("theme") != theme:
            settings["theme"] = theme
            try:
                os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
                with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                    json.dump(settings, f)
            except OSError:
                pass

    @staticmethod
    def _load_settings() -> Dict:
        try:
            with open(SETTINGS_FILE, encoding="utf-8") as f:
                return json.load(f)
        except (OSError, ValueError):
            return {}

    def on_resize(self) -> None:
        self.screen.set_class(self.size.width < 130, "narrow")
        self.screen.set_class(self.size.width < 90, "tiny")
        self.call_after_refresh(self._fit_columns)

    def _fit_columns(self) -> None:
        """Give the title (or query) column whatever width the table has left."""
        for table_id in ("#table", "#lib-table", "#alert-table"):
            table = self.query_one(table_id, DataTable)
            columns = list(table.columns.values())
            flexible = columns[1]
            fixed = sum(c.width for c in columns if c is not flexible)
            width = max(20, table.scrollable_content_region.width - fixed - 2 * len(columns) - 1)
            if flexible.width != width:
                flexible.width = width
                flexible.auto_width = False
                # DataTable caches rendered rows and has no public way to drop
                # them after a column resize, so reset its caches if possible
                if hasattr(table, "_clear_caches"):
                    table._clear_caches()
                    table._require_update_dimensions = True
                table.refresh(layout=True)

    # -------------------------------------------------- annotations

    @property
    def manager(self):
        if self._manager is None:
            try:
                from lixplore.utils.annotations import AnnotationManager
                self._manager = AnnotationManager()
            except Exception as e:
                self.notify(f"Annotations unavailable: {e}", severity="error")
        return self._manager

    def annotation_for(self, article: Dict) -> Optional[Dict]:
        return self.manager.get_annotation_for_article(article) if self.manager else None

    def annotate(self, article: Dict, after=None) -> None:
        def save(result: Optional[Dict]) -> None:
            if not result or not self.manager:
                return
            self.manager.annotate(article, comment=result["comment"], rating=result["rating"],
                                  read_status=result["read_status"], priority=result["priority"])
            self.manager.set_tags(article, result["tags"])
            self.notify("Annotation saved", title=(article.get("title") or "")[:60])
            self._after_annotation_change()
            if after:
                after()

        self.push_screen(AnnotateScreen(article.get("title") or "Untitled", self.annotation_for(article)), save)

    def _after_annotation_change(self) -> None:
        self._refresh_current_row()
        self._show_preview(self._current_article())
        if self.query_one("#main", ContentSwitcher).current == "library":
            self._load_library(keep_cursor=True)

    # -------------------------------------------------- search

    @on(Input.Submitted, "#query")
    @on(Button.Pressed, "#go")
    def start_search(self) -> None:
        query = self.query_one("#query", Input).value.strip()
        if not query:
            self.notify("Type something to search for", severity="warning")
            return
        sources = [k for k, *_ in SOURCES if self.query_one(f"#src-{k}", Chip).value]
        if not sources:
            self.notify("Tick at least one database", severity="warning")
            return
        try:
            limit = max(1, min(500, int(self.query_one("#max", Input).value or 20)))
        except ValueError:
            limit = 20
        self.run_search(query, sources, limit, self.query_one("#dedupe", Chip).value)

    @work(thread=True, exclusive=True, group="search")
    def run_search(self, query: str, sources: List[str], limit: int, dedupe: bool,
                   since: Optional[date] = None) -> None:
        # Source modules report problems with print(); keep that off the screen
        # and use it to tell the user which database failed
        import contextlib
        import io
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
            self._search(query, sources, limit, dedupe, since, buffer)

    def _search(self, query, sources, limit, dedupe, since, buffer) -> None:
        import importlib
        self.call_from_thread(self._search_started, query, sources, since)
        found: List[Dict] = []
        failed: List[str] = []
        for i, source in enumerate(sources, 1):
            self.call_from_thread(self._set_status, f"⏳ Searching {SOURCE_LABEL[source]}…  ({i}/{len(sources)})")
            mark = buffer.tell()
            try:
                module = importlib.import_module(f"lixplore.sources.{source}")
                batch = module.search(query, limit, since=since) if since else module.search(query, limit)
            except Exception:
                batch = None
            if batch is None or (not batch and "Error]" in buffer.getvalue()[mark:]):
                failed.append(SOURCE_LABEL[source])
                continue
            found.extend(batch)
            self.call_from_thread(self._append_results, batch)

        removed = 0
        if dedupe and len(sources) > 1 and found:
            from lixplore import dispatcher
            unique = dispatcher.deduplicate_advanced(found, strategy="auto", keep_preference="most_complete")
            removed = len(found) - len(unique)
            found = unique
            self.call_from_thread(self._replace_results, found)
        try:
            from lixplore import dispatcher
            dispatcher.save_to_history(query, sources, len(found))
        except Exception:
            pass
        self.call_from_thread(self._search_finished, len(found), removed, failed, since)

    def _search_started(self, query: str, sources: List[str], since: Optional[date]) -> None:
        self.action_view("results")
        self.results, self.shown, self.selected = [], [], set()
        self.sort_mode = "relevance"
        self.query_one("#table", DataTable).clear()
        self.query_one("#empty").display = False
        self.query_one("#table").display = True
        self.screen.remove_class("no-preview")
        self.query_one("#table", DataTable).loading = True
        self.call_after_refresh(self._fit_columns)
        self.query_one("#go", Button).disabled = True

    def _append_results(self, batch: List[Dict]) -> None:
        table = self.query_one("#table", DataTable)
        table.loading = False
        start = len(self.results)
        self.results.extend(batch)
        for idx in range(start, len(self.results)):
            if self._matches_filter(self.results[idx]):
                self.shown.append(idx)
                table.add_row(*self._row(idx), key=str(idx))
        if start == 0 and batch:
            table.focus()
            self._show_preview(self._current_article())

    def _replace_results(self, results: List[Dict]) -> None:
        self.results = results
        self._rebuild_table()

    def _search_finished(self, total: int, removed: int, failed: List[str], since: Optional[date]) -> None:
        self.query_one("#table", DataTable).loading = False
        self.query_one("#go", Button).disabled = False
        self._update_empty()
        self._load_recent()
        msg = f"{total} papers" + (f" added since {since:%d %b}" if since else "")
        if removed:
            msg += f" · {removed} duplicates merged"
        if failed:
            self.notify("No response from " + ", ".join(failed), severity="warning")
        self.notify(msg, title="Search complete")
        self._update_status()

    def _set_status(self, text: str) -> None:
        self.query_one("#results-status", Static).update(text)

    # -------------------------------------------------- results table

    def _row(self, idx: int):
        article = self.results[idx]
        ann = self.annotation_for(article)
        mark = Text()
        if idx in self.selected:
            mark.append("● ", style="bold green")
        if ann and ann.get("rating"):
            mark.append(f"{ann['rating']}★", style="yellow")
        return (mark, article.get("title") or "Untitled", _authors(article, 1), str(article.get("year") or ""),
                _source_badge(article.get("source", "")))

    def _matches_filter(self, article: Dict) -> bool:
        text = self.query_one("#filter", Input).value.strip().lower()
        if not text:
            return True
        hay = " ".join(str(article.get(k) or "") for k in ("title", "journal", "year", "source"))
        hay += " " + _authors(article, 50)
        return all(word in hay.lower() for word in text.split())

    def _sorted_indices(self) -> List[int]:
        idx = [i for i in range(len(self.results)) if self._matches_filter(self.results[i])]
        year = lambda i: str(self.results[i].get("year") or "0000")  # noqa: E731
        if self.sort_mode == "newest":
            idx.sort(key=year, reverse=True)
        elif self.sort_mode == "oldest":
            idx.sort(key=year)
        elif self.sort_mode == "title":
            idx.sort(key=lambda i: (self.results[i].get("title") or "").lower())
        elif self.sort_mode == "source":
            idx.sort(key=lambda i: self.results[i].get("source") or "")
        return idx

    def _rebuild_table(self, keep: Optional[int] = None) -> None:
        table = self.query_one("#table", DataTable)
        table.clear()
        self.shown = self._sorted_indices()
        for idx in self.shown:
            table.add_row(*self._row(idx), key=str(idx))
        if keep is not None and keep in self.shown:
            table.move_cursor(row=self.shown.index(keep))
        self._update_empty()
        self._update_status()
        self._show_preview(self._current_article())

    def _update_empty(self) -> None:
        has = bool(self.results)
        self.query_one("#empty").display = not has
        self.query_one("#table").display = has
        if self.query_one("#main", ContentSwitcher).current == "results":
            self.screen.set_class(not has, "no-preview")
        self.call_after_refresh(self._fit_columns)

    def _update_status(self) -> None:
        text = f"{len(self.results)} results"
        if len(self.shown) != len(self.results):
            text += f" · {len(self.shown)} shown"
        if self.selected:
            text += f" · {len(self.selected)} selected"
        text += f" · sorted by {self.sort_mode}"
        self._set_status(text)

    def _current_index(self) -> Optional[int]:
        table = self.query_one("#table", DataTable)
        if not self.shown or table.cursor_row is None or table.cursor_row >= len(self.shown):
            return None
        return self.shown[table.cursor_row]

    def _current_article(self) -> Optional[Dict]:
        view = self.query_one("#main", ContentSwitcher).current
        if view == "library":
            row = self.query_one("#lib-table", DataTable).cursor_row
            if self.library_items and row is not None and row < len(self.library_items):
                return self.library_items[row]["annotation"].get("article_info", {})
            return None
        idx = self._current_index()
        return self.results[idx] if idx is not None else None

    def _refresh_current_row(self) -> None:
        idx = self._current_index()
        if idx is None:
            return
        table = self.query_one("#table", DataTable)
        for col, value in zip(("mark", "title", "authors", "year", "source"), self._row(idx)):
            table.update_cell(str(idx), col, value)

    def _show_preview(self, article: Optional[Dict]) -> None:
        body = self.query_one("#preview-body", Static)
        if not article:
            body.update(Text("Select a paper to preview it here.", style="dim"))
            return
        body.update(render_article(article, self.annotation_for(article)))
        self.query_one("#preview").scroll_home(animate=False)

    @on(DataTable.RowHighlighted)
    def _row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        if event.data_table.id in ("table", "lib-table"):
            self._show_preview(self._current_article())

    @on(DataTable.RowSelected, "#alert-table")
    def _alert_chosen(self, event: DataTable.RowSelected) -> None:
        self.action_run_alert()

    # -------------------------------------------------- actions on the current paper

    def action_read(self) -> None:
        article = self._current_article()
        if article:
            self.push_screen(ReaderScreen(article, self.manager))

    def open_article(self, article: Dict) -> None:
        link = _link(article)
        if link:
            webbrowser.open(link)
            self.notify("Opened in browser", title=link[:60])
        else:
            self.notify("This paper has no link", severity="warning")

    def action_open(self) -> None:
        article = self._current_article()
        if article:
            self.open_article(article)

    def action_annotate_current(self) -> None:
        article = self._current_article()
        if article:
            self.annotate(article)

    def action_rate(self, stars: int) -> None:
        article = self._current_article()
        if article and self.manager:
            self.manager.annotate(article, rating=stars)
            self.notify("★" * stars + "☆" * (5 - stars), title="Rated")
            self._after_annotation_change()

    def action_toggle_select(self) -> None:
        idx = self._current_index()
        if idx is None:
            return
        self.selected.symmetric_difference_update({idx})
        self._refresh_current_row()
        self._update_status()
        table = self.query_one("#table", DataTable)
        if table.cursor_row < len(self.shown) - 1:
            table.move_cursor(row=table.cursor_row + 1)

    def action_select_all(self) -> None:
        self.selected.update(self.shown)
        self._rebuild_table(keep=self._current_index())

    def action_clear_selection(self) -> None:
        self.selected.clear()
        self._rebuild_table(keep=self._current_index())

    def action_sort(self) -> None:
        self.sort_mode = SORTS[(SORTS.index(self.sort_mode) + 1) % len(SORTS)]
        self._rebuild_table(keep=self._current_index())
        self.notify(f"Sorted by {self.sort_mode}", timeout=1.5)

    def action_filter(self) -> None:
        box = self.query_one("#filter", Input)
        box.add_class("visible")
        box.focus()

    @on(Input.Changed, "#filter")
    def _filter_changed(self) -> None:
        self._rebuild_table(keep=self._current_index())

    @on(Input.Submitted, "#filter")
    def _filter_done(self) -> None:
        self.query_one("#table").focus()

    def on_input_blurred(self, event) -> None:  # hide an empty filter box
        box = self.query_one("#filter", Input)
        if event.input is box and not box.value:
            box.remove_class("visible")

    def action_export(self) -> None:
        if not self.results:
            self.notify("Nothing to export yet", severity="warning")
            return

        def do_export(choice: Optional[Dict]) -> None:
            if not choice:
                return
            idx = {"selected": sorted(self.selected), "visible": self.shown,
                   "all": list(range(len(self.results)))}[choice["scope"]]
            papers = [self.results[i] for i in idx]
            import contextlib
            import io
            try:
                from lixplore.utils.export import export_results
                with contextlib.redirect_stdout(io.StringIO()):
                    path = export_results(papers, choice["format"], choice["filename"])
            except Exception as e:
                self.notify(str(e), title="Export failed", severity="error")
                return
            if path:
                self.notify(os.path.abspath(path), title=f"Exported {len(papers)} papers", timeout=8)
            else:
                self.notify("Export failed", severity="error")

        self.push_screen(ExportScreen({"selected": len(self.selected), "visible": len(self.shown),
                                       "all": len(self.results)}), do_export)

    # -------------------------------------------------- navigation

    def action_view(self, view: str, remember: bool = True) -> None:
        if isinstance(self.screen, ModalScreen):
            return  # a pop-up is open; Esc closes it first
        switcher = self.query_one("#main", ContentSwitcher)
        if remember and switcher.current and switcher.current != view:
            self._view_history = [v for v in self._view_history if v != switcher.current][-9:]
            self._view_history.append(switcher.current)
        switcher.current = view
        self.screen.set_class(view in ("alerts", "stats") or (view == "results" and not self.results),
                              "no-preview")
        nav = self.query_one("#nav", OptionList)
        nav.highlighted = nav.get_option_index(view)
        if view == "library":
            self._load_library()
            self.query_one("#lib-table").focus()
        elif view == "alerts":
            self._load_alerts()
            self.query_one("#alert-table").focus()
        elif view == "stats":
            self._load_stats()
        else:
            self.query_one("#table" if self.results else "#query").focus()
            self._show_preview(self._current_article())
        self.call_after_refresh(self._fit_columns)

    def action_back(self) -> None:
        """Esc: step back one level from wherever you are."""
        box = self.query_one("#filter", Input)
        if box.has_class("visible"):
            box.value = ""
            box.remove_class("visible")
            self.query_one("#table").focus()
            return
        view = self.query_one("#main", ContentSwitcher).current
        focused = self.focused
        home = {"results": "#table", "library": "#lib-table", "alerts": "#alert-table"}.get(view)
        if isinstance(focused, Input) and home and (view != "results" or self.results):
            self.query_one(home).focus()
            return
        if self._view_history:
            self.action_view(self._view_history.pop(), remember=False)
        elif view != "results":
            self.action_view("results", remember=False)
        else:
            self.notify("You're at the start. Press q to quit.", timeout=2)

    @on(OptionList.OptionSelected, "#nav")
    def _nav_chosen(self, event: OptionList.OptionSelected) -> None:
        self.action_view(event.option.id)

    def action_focus_search(self) -> None:
        self.action_view("results")
        box = self.query_one("#query", Input)
        box.focus()
        box.select_all()

    def action_help(self) -> None:
        self.push_screen(HelpScreen())

    # -------------------------------------------------- recent searches

    def _load_recent(self) -> None:
        recent = self.query_one("#recent", OptionList)
        recent.clear_options()
        try:
            with open(HISTORY_FILE, encoding="utf-8") as f:
                history = json.load(f)
        except (OSError, ValueError):
            history = []
        seen = set()
        for entry in history:
            q = (entry.get("query") or "").strip()
            if q and q not in seen:
                seen.add(q)
                label = Text(q if len(q) <= 17 else q[:16] + "…", no_wrap=True, overflow="ellipsis")
                recent.add_option(Option(label, id=f"q{len(seen)}"))
                self._recent_queries[f"q{len(seen)}"] = q
            if len(seen) >= 12:
                break

    @on(OptionList.OptionSelected, "#recent")
    def _recent_chosen(self, event: OptionList.OptionSelected) -> None:
        q = self._recent_queries.get(event.option.id)
        if q:
            self.query_one("#query", Input).value = q
            self.start_search()

    # -------------------------------------------------- library

    @on(Select.Changed, "#lib-filter")
    @on(Input.Changed, "#lib-search")
    def _library_filter_changed(self) -> None:
        if self.query_one("#main", ContentSwitcher).current == "library":
            self._load_library()

    def _load_library(self, keep_cursor: bool = False) -> None:
        table = self.query_one("#lib-table", DataTable)
        row = table.cursor_row
        table.clear()
        if not self.manager:
            return
        mode = self.query_one("#lib-filter", Select).value
        filters = {"top": {"min_rating": 4}, "unread": {"read_status": "unread"},
                   "reading": {"read_status": "reading"}, "high": {"priority": "high"},
                   "notes": {"has_comments": True}}.get(mode)
        items = self.manager.list_all(filters)
        text = self.query_one("#lib-search", Input).value.strip().lower()
        if text:
            items = [it for it in items if text in json.dumps(it["annotation"], ensure_ascii=False).lower()]
        items.sort(key=lambda it: it["annotation"].get("updated_at", ""), reverse=True)
        self.library_items = items
        for it in items:
            ann = it["annotation"]
            info = ann.get("article_info", {})
            table.add_row(
                Text("★" * ann["rating"], style="yellow") if ann.get("rating") else "",
                info.get("title") or "Untitled",
                ", ".join(ann.get("tags") or []),
                ann.get("read_status") or "",
                Text(ann.get("priority") or "", style={"high": "bold red", "low": "dim"}.get(ann.get("priority"), "")),
            )
        if keep_cursor and row is not None and items:
            table.move_cursor(row=min(row, len(items) - 1))
        total = len(self.manager.list_all())
        self.query_one("#lib-status", Static).update(
            f"{len(items)} of {total} annotated papers" if total else
            "No annotations yet. Rate a paper with 1–5 or press a in search results.")
        self._show_preview(self._current_article())

    # -------------------------------------------------- alerts

    def _load_alerts(self) -> None:
        table = self.query_one("#alert-table", DataTable)
        table.clear()
        status = self.query_one("#alert-status", Static)
        try:
            from lixplore.alerts.config import ConfigError, load_config, load_dotenv
            load_dotenv(".env")
            self.alerts = load_config().alerts
        except ConfigError:
            self.alerts = []
        except Exception as e:
            self.alerts = []
            status.update(f"Could not read alerts: {e}")
            return
        for a in self.alerts:
            table.add_row(a.name, a.query, ", ".join(SOURCE_LABEL.get(s, s) for s in a.sources))
        if self.alerts:
            status.update("Enter: show papers added in the last 7 days  ·  settings come from .env in this folder")
        else:
            status.update("No alerts here. Run `lixplore --alerts init` in this folder, add LIXPLORE_QUERIES "
                          "to .env, then reopen.")

    def action_run_alert(self) -> None:
        row = self.query_one("#alert-table", DataTable).cursor_row
        if not self.alerts or row is None or row >= len(self.alerts):
            return
        alert = self.alerts[row]
        self.query_one("#query", Input).value = alert.query
        for key, *_ in SOURCES:
            self.query_one(f"#src-{key}", Chip).value = key in alert.sources
        limit = int(self.query_one("#max", Input).value or 20)
        self.run_search(alert.query, alert.sources, limit, True, since=date.today() - timedelta(days=7))

    # -------------------------------------------------- stats

    def _load_stats(self) -> None:
        out: List = [Text("This search", style="bold underline"), Text("")]
        if self.results:
            by_source: Dict[str, int] = {}
            by_year: Dict[str, int] = {}
            for a in self.results:
                by_source[a.get("source", "?")] = by_source.get(a.get("source", "?"), 0) + 1
                y = str(a.get("year") or "?")
                by_year[y] = by_year.get(y, 0) + 1
            out += self._bars({SOURCE_LABEL.get(k, k): v for k, v in by_source.items()},
                              colours={SOURCE_LABEL.get(k, k): SOURCE_COLOUR.get(k, "white") for k in by_source})
            out.append(Text(""))
            years = dict(sorted(by_year.items(), reverse=True)[:10])
            out += self._bars(years, colours={}, default="cyan")
        else:
            out.append(Text("No search yet.", style="dim"))

        out += [Text(""), Text("Your library", style="bold underline"), Text("")]
        stats = self.manager.get_statistics() if self.manager else None
        if stats and stats.get("total"):
            out.append(Text(f"{stats['total']} annotated papers · {stats.get('total_comments', 0)} notes · "
                            f"{stats.get('total_tags', 0)} tags"))
            out.append(Text(""))
            if stats.get("by_rating"):
                out += self._bars({"★" * int(k): v for k, v in sorted(stats["by_rating"].items(), reverse=True)},
                                  colours={}, default="yellow")
                out.append(Text(""))
            if stats.get("by_status"):
                out += self._bars({k.title(): v for k, v in stats["by_status"].items()}, colours={}, default="green")
            if stats.get("unique_tags"):
                tags = Text("\n")
                for t in stats["unique_tags"][:30]:
                    tags.append(f" {t} ", style="reverse")
                    tags.append(" ")
                out.append(tags)
        else:
            out.append(Text("Nothing annotated yet.", style="dim"))
        self.query_one("#stats-view", Static).update(Group(*out))

    @staticmethod
    def _bars(data: Dict[str, int], colours: Dict[str, str], default: str = "cyan") -> List[Text]:
        if not data:
            return []
        peak = max(data.values()) or 1
        width = max(len(k) for k in data)
        rows = []
        for label, value in data.items():
            line = Text(f"{label:>{width}} ")
            line.append("█" * max(1, round(value / peak * 40)), style=colours.get(label, default))
            line.append(f" {value}", style="dim")
            rows.append(line)
        return rows
