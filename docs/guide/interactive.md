# Interactive TUI Mode

Lixplore includes a full-screen split-pane TUI (Text User Interface) that lets you search, browse, annotate, and export without typing any CLI flags. Navigation is driven entirely by the keyboard — no numbered prompts, no pressing Enter to move between items.

## Launching the TUI

```bash
lixplore --tui
```

> **Note:** Running `lixplore` with no arguments does **not** launch the TUI — it shows a "no source selected" error. The `--tui` flag is always required.

---

## Layout

The TUI uses a **split-pane** design:

```
┌─────────────────────┬──────────────────────────────┐
│  Left panel         │  Right panel                 │
│  Menu / Article list│  Description / Article detail│
└─────────────────────┴──────────────────────────────┘
```

Both panels update live as you move the cursor.

---

## Main Menu Navigation

When you launch `--tui` you land on the main menu with six items:

| Item | Action |
|------|--------|
| Search Articles | Search PubMed, arXiv, Crossref, EuropePMC |
| My Annotations | Browse all your saved notes |
| Statistics | Rating, status, and tag overview |
| Export | Save annotations to file |
| Help | Keyboard shortcut guide |
| Exit | Quit Lixplore |

### Main menu keys

| Key | Action |
|-----|--------|
| `↑` / `↓` (arrow keys) | Move highlight up / down |
| `k` / `j` | Move highlight up / down (vim-style) |
| `Enter`, `Space`, or `→` | Select highlighted item |
| `1` – `6` | Jump to and select that item directly |
| `q` or `Esc` | Quit |

The right panel automatically shows a description of the highlighted item as you navigate.

---

## Searching for Articles

Select **Search Articles** from the main menu. You will be prompted (with normal text input) for:

1. **Search query** — e.g. `cancer AND treatment`
2. **Database** — choose from PubMed, arXiv, Crossref, EuropePMC, or All
3. **Max results** — number of articles to fetch
4. **Deduplicate?** — shown only when "All databases" is selected

After the search completes you are offered the **split-pane results browser**.

---

## Article Browser

The article browser shows the result list on the left and the currently highlighted article's details on the right.

### Navigation keys

| Key | Action |
|-----|--------|
| `↑` / `↓` (arrow keys) | Move cursor up / down through articles |
| `k` / `j` | Move cursor up / down (vim-style) |
| `n` | Next page |
| `p` | Previous page |
| `g` | Jump to article by number (shows a prompt) |

### Article actions

| Key | Action |
|-----|--------|
| `Enter` or `v` | View full article detail (fullscreen) |
| `a` | Annotate current article (rating, tags, notes) |
| `s` | Toggle selection of current article |
| `e` | Export all selected articles (prompted for format) |
| `f` | Toggle fullscreen for the right panel |
| `b`, `q`, or `Esc` | Go back / exit browser |

### Selection and export

- Press `s` on any article to mark it (shown with `●`).
- Press `e` to export your selection — you will be prompted to choose CSV, JSON, BibTeX, RIS, Excel, or EndNote.
- The selection count is displayed at the top of the left panel.

---

## Annotations

Open **My Annotations** from the main menu to browse previously saved annotations. Filter by:

- All annotations
- High-rated (4–5 ★)
- Unread articles
- High priority
- Keyword search

To add or update an annotation for an article, navigate to it in the article browser and press `a`. You can set:

- **Rating** (1–5 stars)
- **Tags** (comma-separated, e.g. `cite, review-later`)
- **Notes / comments**
- **Priority** (low / medium / high)
- **Read status** (unread / reading / read)

Annotations are stored locally in `~/.lixplore_annotations.json` and persist across sessions.

---

## Statistics

Select **Statistics** from the main menu to see:

- Total annotated articles
- Rating distribution chart
- Read-status breakdown
- Priority breakdown
- Unique tags and frequency
- Total comments written

---

## Export Annotations

Select **Export** from the main menu to dump all saved annotations to a file. Available formats:

| Format | Use case |
|--------|----------|
| Markdown | Human-readable notes |
| JSON | Machine-readable backup |
| CSV | Spreadsheet import |

---

## Keyboard Reference (Summary)

### Main menu

| Key | Action |
|-----|--------|
| `↑` / `↓` | Navigate items |
| `j` / `k` | Navigate items (vim) |
| `Enter` / `Space` / `→` | Select |
| `1`–`6` | Direct select |
| `q` / `Esc` | Quit |

### Article browser

| Key | Action |
|-----|--------|
| `↑` / `↓` | Move cursor |
| `j` / `k` | Move cursor (vim) |
| `n` / `p` | Next / previous page |
| `g` | Jump to # (prompted) |
| `Enter` / `v` | View article |
| `a` | Annotate |
| `s` | Toggle select |
| `e` | Export selected |
| `f` | Fullscreen toggle |
| `b` / `q` / `Esc` | Back |

---

## Requirements

The enhanced TUI requires the **Rich** library (≥ 13):

```bash
pip install "rich>=13"
```

To diagnose Rich installation issues:

```bash
lixplore --check-tui
```

If Rich is unavailable, Lixplore falls back to a minimal text menu.
