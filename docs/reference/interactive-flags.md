# Interactive Mode Flags

> **Documentation for interactive mode flags**

## Overview

Lixplore offers three interactive modes for easier usage without memorizing command-line flags.

**Total Interactive Flags:** 3

---

## `--tui`

**Description:** Launch enhanced TUI (Text User Interface) mode - the primary interactive interface.

**Syntax:**
```bash
lixplore --tui
```

> **Note:** Running `lixplore` with no arguments does **not** launch the TUI — it shows a "no source selected" error. The `--tui` flag is always required.

**Type:** Boolean flag

### Features
- Split-pane visual interface (article list + detail preview)
- Real-time arrow-key navigation — no numbered prompts
- Search across multiple academic databases
- Browse and annotate articles
- Statistics dashboard
- Export to CSV, JSON, BibTeX, RIS, Excel, and EndNote

### Examples

**Launch TUI:**
```bash
lixplore --tui
```

### Main menu navigation

| Key | Action |
|-----|--------|
| `↑` / `↓` (arrow keys) | Move highlight |
| `k` / `j` | Move highlight (vim-style) |
| `Enter`, `Space`, or `→` | Select highlighted item |
| `1`–`6` | Jump to and select item directly |
| `q` / `Esc` | Quit |

### Article browser navigation

| Key | Action |
|-----|--------|
| `↑` / `↓` (arrow keys) | Move cursor through articles |
| `k` / `j` | Move cursor (vim-style) |
| `n` / `p` | Next / previous page |
| `g` | Jump to article by number (prompted) |
| `Enter` or `v` | View full article detail |
| `a` | Annotate current article |
| `s` | Toggle selection |
| `e` | Export selected articles |
| `f` | Toggle fullscreen preview |
| `b` / `q` / `Esc` | Back |

See [Interactive TUI Mode](../guide/interactive.md) for the full guide.

### TUI Screens
1. **Search:** Enter query and select sources
2. **Results:** Browse and select articles
3. **Annotations:** Manage annotations
4. **Statistics:** View analytics
5. **Export:** Export selected items

---

## `--shell`

**Description:** Launch interactive shell mode (persistent session).

**Status:** Deprecated - use `--tui` instead

**Syntax:**
```bash
lixplore --shell
```

**Type:** Boolean flag

### Features
- Persistent session
- Command history
- No need to type 'lixplore' repeatedly
- Tab completion

### Examples

**Example 1: Shell Mode**
```bash
lixplore --shell

lixplore> search "cancer" -P -m 20
lixplore> annotate 5 --rating 5
lixplore> list annotations
lixplore> export markdown
lixplore> exit
```

**Note:** This mode is deprecated. Use `--tui` for better experience.

---

## `--wizard`

**Description:** Launch wizard mode with guided workflows.

**Status:** Deprecated - use `--tui` instead

**Syntax:**
```bash
lixplore --wizard
```

**Type:** Boolean flag

### Features
- Step-by-step guided workflows
- No flags to memorize
- Interactive prompts
- Beginner-friendly

### Examples

**Example 1: Wizard Mode**
```bash
lixplore --wizard

What do you want to do?
  1. Search for articles
  2. Annotate an article
  3. View annotations
  4. Export results

Select option: 1

Which sources do you want to search?
  [ ] PubMed
  [ ] Crossref
  [x] arXiv
  ...
```

**Note:** This mode is deprecated. Use `--tui` for better experience.

---

## Best Practices

### When to Use Interactive Modes

**Use TUI Mode When:**
- Learning Lixplore for the first time
- You prefer visual interfaces
- Complex multi-step workflows
- Exploring features

**Use Command Line When:**
- Scripting and automation
- Quick one-off searches
- Integrating with other tools
- CI/CD pipelines

---

**Last Updated:** 2024-12-28
