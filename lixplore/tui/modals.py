"""Pop-up screens: annotate, export, help."""

from typing import Dict, List, Optional

from rich.text import Text
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Grid, Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Markdown, Select, Static, TextArea

# "No selection" marker: Select.NULL in Textual 6+, Select.BLANK before (now a False alias)
NO_SELECTION = getattr(Select, "NULL", Select.BLANK)

EXPORT_FORMATS = [
    ("CSV", "csv"), ("Excel (.xlsx)", "xlsx"), ("BibTeX", "bibtex"), ("RIS (Zotero, Mendeley)", "ris"),
    ("EndNote tagged (.enw)", "enw"), ("EndNote XML", "endnote"), ("JSON", "json"), ("XML", "xml"),
]


class AnnotateScreen(ModalScreen[Optional[Dict]]):
    """Rating, status, priority, tags and a new note on one screen."""

    BINDINGS = [
        Binding("escape", "cancel", "Back"),
        Binding("ctrl+s", "save", "Save", priority=True),
    ]

    def __init__(self, title: str, annotation: Optional[Dict]):
        super().__init__()
        self.article_title = title
        self.annotation = annotation or {}

    def compose(self) -> ComposeResult:
        ann = self.annotation
        with Vertical(id="dialog", classes="annotate"):
            yield Label("Annotate", classes="dialog-title")
            yield Static(Text(self.article_title, style="bold"), classes="dialog-subtitle")
            with Grid(id="annotate-grid"):
                yield Label("Rating")
                yield Select(
                    [("★" * n + "☆" * (5 - n) + f"  {n}", n) for n in range(5, 0, -1)],
                    value=ann.get("rating") or NO_SELECTION, prompt="Not rated", id="rating", compact=True)
                yield Label("Status")
                yield Select([("Unread", "unread"), ("Reading", "reading"), ("Read", "read")],
                             value=ann.get("read_status") or "unread", allow_blank=False, id="status", compact=True)
                yield Label("Priority")
                yield Select([("Low", "low"), ("Medium", "medium"), ("High", "high")],
                             value=ann.get("priority") or "medium", allow_blank=False, id="priority", compact=True)
                yield Label("Tags")
                yield Input(", ".join(ann.get("tags") or []), placeholder="comma-separated, e.g. cite, review",
                            id="tags", compact=True)
            notes = ann.get("comments") or []
            if notes:
                yield Label(f"Notes ({len(notes)})", classes="section")
                with VerticalScroll(id="old-notes"):
                    for c in notes:
                        yield Static(Text("• " + c.get("text", ""), style="italic"))
            yield Label("Add a note", classes="section")
            yield TextArea(id="note", soft_wrap=True, show_line_numbers=False)
            with Horizontal(classes="buttons"):
                yield Button("Cancel", id="cancel", compact=True)
                yield Button("Save  ^s", id="save", variant="primary", compact=True)

    def on_mount(self) -> None:
        self.query_one("#rating").focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            self.action_save()
        else:
            self.action_cancel()

    def action_save(self) -> None:
        rating = self.query_one("#rating", Select).value
        self.dismiss({
            "rating": int(rating) if isinstance(rating, int) and not isinstance(rating, bool) else None,
            "read_status": self.query_one("#status", Select).value,
            "priority": self.query_one("#priority", Select).value,
            "tags": [t.strip() for t in self.query_one("#tags", Input).value.split(",") if t.strip()],
            "comment": self.query_one("#note", TextArea).text.strip() or None,
        })

    def action_cancel(self) -> None:
        self.dismiss(None)


class ExportScreen(ModalScreen[Optional[Dict]]):
    BINDINGS = [Binding("escape", "cancel", "Back")]

    def __init__(self, counts: Dict[str, int]):
        super().__init__()
        self.counts = counts

    def compose(self) -> ComposeResult:
        scopes = [(f"{label} ({n})", key) for key, label, n in (
            ("selected", "Selected", self.counts.get("selected", 0)),
            ("visible", "Shown in table", self.counts.get("visible", 0)),
            ("all", "All results", self.counts.get("all", 0)),
        ) if n]
        with Vertical(id="dialog", classes="export"):
            yield Label("Export", classes="dialog-title")
            with Grid(id="export-grid"):
                yield Label("Papers")
                yield Select(scopes, value=scopes[0][1], allow_blank=False, id="scope", compact=True)
                yield Label("Format")
                yield Select(EXPORT_FORMATS, value="csv", allow_blank=False, id="format", compact=True)
                yield Label("File name")
                yield Input(placeholder="optional, saved under exports/<format>/", id="filename", compact=True)
            with Horizontal(classes="buttons"):
                yield Button("Cancel", id="cancel", compact=True)
                yield Button("Export", id="export", variant="primary", compact=True)

    def on_mount(self) -> None:
        self.query_one("#format").focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "export":
            self.dismiss({
                "scope": self.query_one("#scope", Select).value,
                "format": self.query_one("#format", Select).value,
                "filename": self.query_one("#filename", Input).value.strip() or None,
            })
        else:
            self.dismiss(None)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.query_one("#export", Button).press()

    def action_cancel(self) -> None:
        self.dismiss(None)


HELP = """\
## Searching
Type in the search bar and press **Enter**. Tick the databases to search.
Boolean queries work: `(semaglutide OR tirzepatide) AND obesity NOT diabetes`, `"exact phrase"`.
Results stream in as each database answers.

## Results
| Key | Action |
|---|---|
| `↑` `↓` / mouse | move, preview updates live |
| `Enter` | read the paper full-screen |
| `o` | open the paper in your browser |
| `1`–`5` | rate instantly |
| `a` | annotate: rating, status, priority, tags, notes |
| `space` | select / unselect |
| `A` / `x` | select all shown / clear selection |
| `e` | export (selected, shown or all) |
| `f` | filter the table as you type |
| `s` | sort: relevance → newest → oldest → title → source |
| `/` | new search |

## Everywhere
| Key | Action |
|---|---|
| `Esc` | **back**: close a pop-up, clear the filter, leave a text box, or return to the previous view |
| `Ctrl+F` `Ctrl+L` `Ctrl+N` `Ctrl+T` | Search · Library · Alerts · Stats (also `F1`–`F4` if your terminal allows) |
| `Ctrl+P` | command palette (also switches theme) |
| `?` | this help |
| `q` | quit |

**Library** lists every paper you've rated, tagged or noted. **Alerts** shows the searches in your
`.env` (see `lixplore --alerts init`); press Enter on one to see what's new in the last 7 days.
"""


class HelpScreen(ModalScreen[None]):
    BINDINGS = [Binding("escape,q,question_mark", "close", "Back")]

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="dialog", classes="help"):
            yield Markdown(HELP)
            with Horizontal(classes="buttons"):
                yield Button("Close", id="close", variant="primary", compact=True)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(None)

    def action_close(self) -> None:
        self.dismiss(None)
