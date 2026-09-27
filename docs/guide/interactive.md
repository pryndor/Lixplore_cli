# Full-screen TUI

The TUI is a research cockpit: search several databases at once, read papers in a live preview, rate and annotate them, keep a library, check your alerts and export — all from one screen, with keyboard or mouse.

## Launching

```bash
pip install "lixplore-cli[tui]"          # adds Textual (Python 3.9+)

lixplore --tui                           # open the TUI
lixplore -P -q "CRISPR" -m 50 -i         # run a CLI search, then browse it in the TUI
```

Without Textual installed, these commands open the older Rich-based TUI instead. `lixplore --check-tui` reports what is installed and how to fix it.

## Layout

```
┌ ◆ Lixplore  [ search box ]   ● PubMed ● EuropePMC ● arXiv ○ Crossref ○ DOAJ │ ● Dedupe  20 [Search] ┐
├──────────────┬──────────────────────────────────────────────┬─────────────────────────────────────────┤
│ Search    ^F │ results table                                │ preview of the highlighted paper        │
│ Library   ^L │                                              │ title, authors, journal, links,         │
│ Alerts    ^N │                                              │ your rating / tags / notes, abstract    │
│ Stats     ^T │                                              │                                         │
│ RECENT       │ status: 36 results · 2 selected · sorted by… │                                         │
├──────────────┴──────────────────────────────────────────────┴─────────────────────────────────────────┤
│ footer: the keys available right now                                                                  │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

- **Top bar**: type a query and press Enter. Click a database chip (or focus it and press Space) to switch it on or off. The number is the maximum results per database.
- **Sidebar**: switch views (or `Ctrl+F` / `Ctrl+L` / `Ctrl+N` / `Ctrl+T`), or pick a recent search to run it again. `Esc` always takes you back.
- **Preview**: follows the cursor. It is hidden on narrow terminals (under 130 columns); press Enter to read a paper full-screen instead.

The footer always shows the keys that work in the current place.

## Searching

Queries go to each database as written, so boolean syntax works:

```
(semaglutide OR tirzepatide) AND obesity NOT diabetes
"graph neural network" AND drug
```

Results appear as each database answers. With **Dedupe** on, the same paper found in several databases is merged at the end. If a database fails to answer, a notification says which one.

## Working with results

| Key | Action |
|---|---|
| `↑` `↓`, mouse | Move; the preview updates |
| `Enter` | Read the paper full-screen (`Esc` to return) |
| `o` | Open the paper in your browser |
| `1`–`5` | Rate instantly |
| `a` | Annotate: rating, read status, priority, tags and a new note on one form (`Ctrl+S` saves) |
| `Space` | Select / unselect, then move down |
| `A` / `x` | Select all shown / clear selection |
| `e` | Export the selected, shown or all results (CSV, Excel, BibTeX, RIS, EndNote, JSON, XML) |
| `f` | Filter the table as you type (`Enter` keeps it, `Esc` leaves) |
| `s` | Sort: relevance → newest → oldest → title → source |
| `/` | Start a new search |

Rated papers show their stars in the first column; selected papers show `●`.

## Library (Ctrl+L)

Every paper you have rated, tagged or annotated, newest change first. Filter by *★ 4 and up*, *Unread*, *Reading*, *High priority* or *With notes*, or type to search titles, tags and notes. Rating, annotating, reading and opening work the same as in results.

Annotations are stored in `~/.lixplore_annotations.json` and are shared with the CLI annotation flags.

## Alerts (Ctrl+N)

Lists the searches from the `.env` in the folder you started Lixplore in (create one with `lixplore --alerts init`). Press Enter on an alert to see papers added in the last 7 days for it. See [Paper Alerts](alerts.md) for scheduled delivery by email, Telegram and more.

## Stats (Ctrl+T)

Charts for the current search (papers per database and per year) and for your library (ratings, read status, tags).

## Everywhere

| Key | Action |
|---|---|
| `Esc` | **Back** from anywhere: closes a pop-up, clears the filter, leaves a text box, or returns to the previous view |
| `Ctrl+F` `Ctrl+L` `Ctrl+N` `Ctrl+T` | Search · Library · Alerts · Stats |
| `F1`–`F4` | Same, if your terminal doesn't use these keys itself (xfce4-terminal opens its own help on `F1`) |
| `Ctrl+P` | Command palette, including theme switching (your choice is remembered) |
| `?` | Help |
| `q` | Quit |

## Troubleshooting

- **Colours look wrong or boxes appear**: use a terminal with true colour and a font with box-drawing characters (most modern terminals). On a raw Linux console (`TERM=linux`), use the CLI instead.
- **`lixplore --tui` opens the old menu**: Textual is missing or Python is older than 3.9. Run `lixplore --check-tui`.
- **Mouse doesn't work inside tmux**: enable it with `set -g mouse on`.
