# Lixplore-cli

> **A Unix-inspired command-line tool for searching scientific literature**, built for terminal users who want speed, automation and minimal interfaces.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://pryndor.github.io/Lixplore_cli/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github)](https://github.com/pryndor/Lixplore_cli)
[![PyPI version](https://badge.fury.io/py/lixplore-cli.svg)](https://pypi.org/project/lixplore-cli/)
[![Downloads](https://static.pepy.tech/badge/lixplore-cli)](https://pepy.tech/project/lixplore-cli)
[![Issues](https://img.shields.io/github/issues/pryndor/Lixplore_cli)](https://github.com/pryndor/Lixplore_cli/issues)
<a href="https://www.buymeacoffee.com/lixplore" target="_blank" rel="noopener noreferrer"><img src="https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Support-40DCA5?style=flat&logo=buy-me-a-coffee" alt="Buy Me A Coffee"></a>

Search PubMed, arXiv, Crossref, DOAJ and Europe PMC in one command with Boolean queries, deduplicate the results, and export to 8 formats including BibTeX, RIS, EndNote and Excel. Browse and annotate papers in a full-screen TUI, and get **new-paper alerts** on email, Telegram, Slack and 14 other channels.

**📚 [Complete Documentation](https://pryndor.github.io/Lixplore_cli/)** | **🐛 [Report Issues](https://github.com/pryndor/Lixplore_cli/issues)**

---

## ✨ Features

### Core Features
- 🔍 **Multi-Source Search** - Search 5 academic databases simultaneously (PubMed, arXiv, Crossref, DOAJ, EuropePMC)
- 🔤 **Boolean Operators** - Advanced queries with AND, OR, NOT, parentheses
- 📊 **Smart Sorting** - Sort by relevance, newest, oldest, journal, or author
- 🔢 **Smart Selection** - Export odd/even, ranges, first/last N articles
- 💾 **8 Export Formats** - CSV, Excel, JSON, BibTeX, RIS, EndNote, XML
- 📖 **Review Mode** - View articles in separate terminal windows
- 🎯 **Deduplication** - Advanced duplicate removal with multiple strategies
- 📁 **Organized Exports** - Auto-organized folders by format type in `./exports/`
- 📬 **Paper Alerts** - Scheduled digests of new papers on 17 channels, via GitHub Actions or cron

### Advanced Features
- 📥 **PDF Downloads** - Automatic PDF downloads from PMC, arXiv, Unpaywall, and SciHub (optional)
- 🔗 **PDF Link Display** - Show clickable PDF links for open access articles in terminal (NEW!)
- 📚 **Reference Manager Integration** - Direct Zotero API integration and Mendeley RIS export
- 📊 **Statistics Dashboard** - Comprehensive analytics with visualizations (publication trends, top journals, top authors)
- 🎨 **Full-screen TUI** - Search, read, rate, annotate and export in a Textual interface (`--tui`)
- 📝 **Citation Export** - Format citations in APA, MLA, Chicago, IEEE styles
- 🔧 **Custom API Integration** - Plugin architecture for any REST API (Springer, BASE, etc.)
- 💡 **Metadata Enrichment** - Auto-enrich results from multiple APIs (Crossref, PubMed, arXiv)
- 💾 **Smart Caching** - 7-day cache with automatic expiration
- 📄 **Pagination** - Browse large result sets with automatic pagination
- 🎯 **Export Profiles** - Save and reuse export configurations
- 📋 **Export Templates** - Predefined templates (Nature, Science, IEEE)
- 🗜️ **Export Compression** - ZIP compression for batch exports

### Documentation
- 📚 **[Complete Documentation Site](https://pryndor.github.io/Lixplore_cli/)** - Comprehensive online documentation
- 📖 **32+ Documentation Pages** - Getting started, user guides, command reference, examples
- 🔍 **All 75 Flags Documented** - Detailed examples for every command-line flag
- 🎓 **Step-by-Step Tutorials** - From installation to advanced workflows
- 💡 **Quick Examples** - Built-in examples with `--examples` flag
- 📄 **Man Page** - Traditional Unix man page included

### 🚀 Interactive Interface
- 🎨 **Enhanced TUI Mode** - Beautiful text-based interface with search, browse, annotate, and export
- 📝 **Annotation System** - Rate, tag, comment, and organize your research library
- 📊 **Statistics Dashboard** - Visualize publication trends and analytics
- 💾 **Smart Export** - Export to 8 formats with intelligent deduplication

---

## 🎯 Two Ways to Use Lixplore

### 1️⃣ Full-screen TUI - Research Cockpit

**Perfect for exploring, reading and curating papers**

```bash
pip install "lixplore-cli[tui]"   # adds Textual (Python 3.9+)
lixplore --tui
```

```
┌ ◆ Lixplore  (semaglutide OR tirzepatide) AND obesity   ● PubMed ● EuropePMC ○ arXiv  [Search] ┐
├──────────────┬──────────────────────────────────────────────┬─────────────────────────────────┤
│ Search    ^F │     Title                    Author  Year Src│ GLP-1 Receptor Agonists in      │
│ Library   ^L │ 4★  GLP-1 Receptor Agonists  Yuan Y  2026 PM │ Heart Failure: A Systematic …   │
│ Alerts    ^N │ ●   An RNA thermogenic ther… Thorne  2026 PM │ Yuan Y, Chen C, Li X +2         │
│ Stats     ^T │     Patient characteristics… Tewksb… 2026 EP │ Drugs · 2026 · PubMed           │
│              │                                              │ ── Your notes ──────────        │
│ RECENT       │                                              │ ★★★★☆  ○ unread  ▲ medium       │
│ semaglutide… │ 36 results · 1 selected · sorted by newest   │ ── Abstract ────────────        │
├──────────────┴──────────────────────────────────────────────┴─────────────────────────────────┤
│ ⏎ Read  o Browser  a Annotate  space Select  e Export  f Filter  1-5 Rate  esc Back  ? Help   │
└───────────────────────────────────────────────────────────────────────────────────────────────┘
```

- ✅ Results stream in per database, with a live preview of the highlighted paper
- ✅ Rate with `1`–`5`, annotate (status, priority, tags, notes) on one form
- ✅ Library of everything you've annotated, filterable and searchable
- ✅ Alerts view: see what's new for your saved alert searches
- ✅ Export selected / shown / all results in 8 formats
- ✅ Mouse support, command palette (`Ctrl+P`), themes, works on Linux, macOS and Windows
- ℹ️ Enrichment, citation styles and PDF download are CLI flags for now

### 2️⃣ Command Line Mode - Direct Commands ✅ (Fully Production-Ready)

**Perfect for scripting, automation, and quick searches**

**All 75 flags fully functional and tested!**

```bash
# Quick search and export
lixplore -P -q "machine learning" -m 20 -X xlsx

# Advanced workflow with deduplication
lixplore -A -q "COVID-19" -m 50 -D --sort newest -X csv

# Citation export with enrichment
lixplore -P -q "CRISPR" -m 30 --enrich crossref -C apa

# Batch export to multiple formats
lixplore -x -q "quantum computing" -m 25 -X csv,bibtex,ris --zip
```

**All Features Available:**
- ✅ 75 command-line flags
- ✅ Multi-source search (PubMed, arXiv, Crossref, DOAJ, EuropePMC)
- ✅ Boolean operators and advanced queries
- ✅ 8 export formats (CSV, Excel, JSON, BibTeX, RIS, EndNote, XML)
- ✅ Citation formatting (APA, MLA, Chicago, IEEE)
- ✅ Metadata enrichment and PDF downloads
- ✅ Deduplication with multiple strategies
- ✅ Export profiles and templates
- ✅ Complete annotation system

**Note:** Legacy shell (`--shell`) and wizard (`--wizard`) modes are still available but deprecated in favor of the enhanced TUI mode.

---

## 🆕 Feature Highlights

### 📥 PDF Download & Link Display
**Download PDFs** automatically with smart fallback chain:
- PubMed Central (open access)
- arXiv (preprints)
- DOI Resolution via Unpaywall
- SciHub fallback (optional, user-configured)

```bash
lixplore -P -q "open access" -m 10 --download-pdf
```

**Show PDF Links** directly in search results (NEW!):
- Display clickable PDF links for open access articles
- Works in modern terminals (iTerm2, GNOME Terminal, Windows Terminal)
- No download required - click to open in browser

```bash
lixplore -x -q "machine learning" -m 10 --show-pdf-links
```

### 📚 Reference Manager Integration
Direct integration with your favorite reference managers:
- **Zotero**: API integration with collection support
- **Mendeley**: RIS export for easy import

**Setup Zotero (one-time):**
1. Get API key: https://www.zotero.org/settings/keys
2. Configure: `lixplore --configure-zotero YOUR_API_KEY YOUR_USER_ID`

**Usage:**
```bash
# Add to Zotero library
lixplore -P -q "research" -m 10 --add-to-zotero

# Add to specific collection
lixplore -P -q "AI" -m 20 --add-to-zotero --zotero-collection 4FCVPNAP
```

### 📊 Statistics Dashboard
Comprehensive analytics with beautiful ASCII visualizations:
- Publication trends by year
- Top journals and authors
- Source distribution
- Metadata completeness

```bash
lixplore -P -q "AI" -m 100 --stat
```

### 🎨 Full-screen TUI
Open any CLI search in the TUI to read, rate, select and export:

```bash
lixplore -P -q "machine learning" -m 50 -i
```

### 🔧 Custom API Integration
Add ANY API source via simple JSON configuration:
- No code modification needed
- Supports Springer, BASE, and more
- Plugin architecture for extensibility

```bash
lixplore --custom-api springer -q "quantum physics" -m 20
```

### 💡 Smart Enhancements
- **Metadata Enrichment**: Auto-fill missing data from multiple APIs
- **Export Profiles**: Save and reuse export configurations
- **Citation Formatting**: Export as APA, MLA, Chicago, IEEE
- **Batch Export**: Export to multiple formats simultaneously
- **Deduplication Strategies**: Multiple algorithms with customization

---

## 📬 Paper Alerts by Email, Telegram, Discord, Slack & more

Get new papers for your searches delivered on a schedule, run free by GitHub Actions. No server, no file edits:

1. **Fork** this repo and enable workflows in the **Actions** tab.
2. In **Settings → Secrets and variables → Actions**, add the variable `LIXPLORE_QUERIES` (one search per line), plus secrets for any channel: Email, Telegram, Discord, Slack, Microsoft Teams, Google Chat, Matrix, WeCom, Feishu, DingTalk, ntfy, Gotify, Pushover, PushPlus, ServerChan3, AstrBot or a custom webhook (n8n/Zapier for WhatsApp, SMS and more).
3. Run **Actions → Lixplore Alerts → Run workflow → test**.

Each digest lists only papers new since the last one, with a CSV/BibTeX attachment. Full guide: [docs/guide/alerts.md](docs/guide/alerts.md).

Prefer your own computer? `pip install -U lixplore-cli`, then `lixplore --alerts init` creates the settings file and `lixplore --alerts schedule` prints the cron / Task Scheduler line.

---

## 🚀 Quick Start

### ⚠️ Prerequisites

Before installing Lixplore, ensure you have:

**Python 3.8 or higher:**
```bash
python3 --version
```

---

### Installation

#### Method 1: pipx (Recommended)

**Best for most users.** Installs in an isolated environment, no virtual env needed.

```bash
# Install pipx if you don't have it
# Arch: sudo pacman -S python-pipx
# Ubuntu/Debian: sudo apt install pipx
# Fedora: sudo dnf install pipx
# macOS: brew install pipx

# Then install lixplore
pipx install lixplore-cli

# Upgrade
pipx upgrade lixplore-cli
```

> **Why pipx?** Modern Linux distros (Arch, Fedora 38+, Ubuntu 23.04+, Debian 12+) block system-wide `pip install` (PEP 668). `pipx` handles this automatically by creating isolated environments per tool while keeping the `lixplore` command available globally.

#### Method 2: pip (in virtual environment)

```bash
# Create and activate a virtual environment
python3 -m venv ~/.venvs/lixplore
source ~/.venvs/lixplore/bin/activate

# Install
pip install lixplore-cli

# Upgrade
pip install --upgrade lixplore-cli
```

#### Method 3: Arch Linux (AUR)

```bash
# Using yay
yay -S lixplore-cli

# Using paru
paru -S lixplore-cli
```

#### Method 4: Homebrew (macOS & Linux)

```bash
brew install pryndor/lixplore/lixplore-cli

# Upgrade
brew update && brew upgrade lixplore-cli
```

Works on Apple Silicon and Intel Macs. Includes the full-screen TUI (`lixplore --tui`).

#### Method 5: From source

```bash
git clone https://github.com/pryndor/Lixplore_cli.git
cd Lixplore_cli
pip install -e .
```

### Optional: Full-screen TUI

For `lixplore --tui` (Textual, Python 3.9+; older Pythons get a simpler Rich TUI):

```bash
# With pipx (inject into existing install)
pipx inject lixplore-cli rich textual

# With pip
pip install "lixplore-cli[tui]"

# Arch Linux
sudo pacman -S python-textual
```

### ✅ Verify Installation

```bash
lixplore --version
lixplore --help
```

### 🐛 Troubleshooting

#### ❌ Error: "externally-managed-environment" (Linux)

This means your distro blocks system-wide pip installs. Use **pipx** (Method 1) instead.

#### ❌ Error: "command 'pip' not found"

```bash
# Use pip3 or python module syntax
pip3 install lixplore-cli
python -m pip install lixplore-cli
```

#### ❌ Error: Permission denied (Linux/macOS)

```bash
# Use pipx (recommended) or install for current user
pipx install lixplore-cli
# or
pip install --user lixplore-cli
```

---

### 🖥️ TUI Mode Troubleshooting (Linux)

`lixplore --tui` uses [Textual](https://textual.textualize.io/) (≥ 4.0, Python 3.9+). Without Textual it falls back to a simpler TUI built on `rich` (≥ 13.0). If it fails to launch, follow these steps:

#### Step 1 — Run the built-in diagnostics

```bash
lixplore --check-tui
```

This prints your Python version, Textual and Rich status, and exact fix instructions.

#### Step 2 — Install / inject Textual

| Installation method | Fix command |
|---------------------|-------------|
| **pipx** (most common) | `pipx inject lixplore-cli textual rich` |
| **pip + venv** | `pip install "lixplore-cli[tui]"` (activate venv first) |
| **Arch Linux (AUR)** | `sudo pacman -S python-textual` |
| **Homebrew** | included, nothing to install |

> **pipx users — common gotcha:** pipx creates an isolated environment per tool. Installing `textual` with plain `pip` or `pacman` puts it in a *different* Python environment that lixplore cannot see. Always use `pipx inject lixplore-cli textual rich` so it lands inside the same isolated env.

#### Step 3 — Check terminal compatibility

Rich needs a terminal that supports ANSI escape codes and Unicode. Verify yours:

```bash
# Should print "xterm-256color" or similar (not "dumb")
echo $TERM

# Quick Unicode/color test
python3 -c "from rich.console import Console; Console().print('[bold cyan]OK[/bold cyan]')"
```

Known-working terminals on Linux: **GNOME Terminal, Konsole, Alacritty, Kitty, Tilix, Xfce4-terminal, WezTerm**.

#### Step 4 — SSH / remote sessions

When connecting over SSH the `TERM` variable is sometimes lost, disabling Rich:

```bash
# On your local machine, connect with terminal forwarding
ssh -t user@host

# Or force 256-color on the remote side
export TERM=xterm-256color
lixplore --tui
```

#### Step 5 — Headless / container environments

Rich will not render correctly in Docker containers, CI runners, or terminals with `NO_COLOR=1` set. In these environments, unset the variable if it was set unintentionally:

```bash
unset NO_COLOR
lixplore --tui
```

#### Step 6 — tmux / screen sessions

Multiplexers like `tmux` and `screen` sometimes set `TERM=screen`, which limits color support. Inside a tmux session:

```bash
# Quick fix for current session
export TERM=xterm-256color
lixplore --tui

# Permanent fix — add to ~/.tmux.conf
# set -g default-terminal "screen-256color"
```

For `screen`, launch it with: `screen -T xterm-256color`

#### Step 7 — Linux virtual console (tty without a desktop)

If you are logged in directly on a raw Linux console (not inside GNOME Terminal, Konsole, etc.) your `TERM` will be `linux`, which does not support 256 colors. The TUI will look broken or fail to render.

**Solution:** Log in via SSH from a color-capable terminal, or start a desktop session and use a terminal emulator listed in Step 3 above. Alternatively, use CLI mode (all features work without a terminal emulator).

#### ✅ If TUI still doesn't work — use CLI mode

All flags work in CLI mode without any extra dependencies. CLI mode is fully production-ready and is what we recommend for scripting, automation, and SSH sessions:

```bash
# CLI equivalents for common TUI workflows
lixplore -P -q "your topic" -m 20          # search PubMed
lixplore -A -q "your topic" -m 50 -D       # search all + deduplication
lixplore -P -q "topic" -m 20 -X xlsx       # export to Excel
lixplore -P -q "topic" -m 20 -i            # open the results in the TUI
```

### Basic Usage

```bash
# Search PubMed
lixplore -P -q "cancer treatment" -m 10

# Search all sources with deduplication
lixplore -A -q "COVID-19" -m 50 -D

# Export to Excel
lixplore -P -q "diabetes" -m 20 -X xlsx -o results.xlsx
```

---

## 📚 Documentation

### 📖 [Complete Online Documentation](https://pryndor.github.io/Lixplore_cli/)

Visit our comprehensive documentation site for:
- **Getting Started Guides** - Installation and first search tutorial
- **User Guides** - Search, filtering, export, annotations, PDF management
- **Command Reference** - All 75 flags with detailed examples
- **Advanced Features** - Automation, AI integration, Zotero, custom APIs
- **Examples** - Common workflows, use cases, tool integrations

### Quick Help

```bash
# Show quick examples
lixplore --examples

# Show complete help
lixplore --help

# View man page (after installing)
man lixplore

# Browse online documentation
# https://pryndor.github.io/Lixplore_cli/
```

### Key Commands

#### Search Sources
```bash
-P, --pubmed       # Search PubMed
-C, --crossref     # Search Crossref
-J, --doaj         # Search DOAJ
-E, --europepmc    # Search EuropePMC
-x, --arxiv        # Search arXiv
-A, --all          # Search all sources
-s PX              # Combined (PubMed + arXiv)
```

#### Boolean Operators
```bash
# AND - both terms required
lixplore -P -q "cancer AND treatment" -m 10

# OR - either term
lixplore -P -q "cancer OR tumor" -m 10

# NOT - exclude term
lixplore -P -q "diabetes NOT type1" -m 10

# Complex queries
lixplore -P -q "(cancer OR tumor) AND treatment" -m 20
```

#### Export Formats
```bash
-X csv      # CSV format
-X xlsx     # Excel with formatting
-X json     # JSON structured data
-X bibtex   # BibTeX for LaTeX
-X ris      # RIS for reference managers
-X enw      # EndNote Tagged (recommended)
-X endnote  # EndNote XML
-X xml      # Generic XML
```

#### Smart Selection
```bash
# Export odd-numbered articles
lixplore -P -q "research" -m 50 -S odd -X csv

# Export first 10 articles
lixplore -P -q "cancer" -m 50 -S first:10 -X xlsx

# Export range
lixplore -P -q "study" -m 50 -S 10-20 -X enw

# Mixed patterns
lixplore -P -q "science" -m 50 -S 1 3 5-10 odd -X csv
```

#### Sorting
```bash
--sort newest   # Latest publications first
--sort oldest   # Earliest publications first
--sort journal  # Alphabetical by journal
--sort author   # Alphabetical by author
```

#### Review Mode
```bash
# Step 1: Search
lixplore -P -q "aspirin" -m 10

# Step 2: Review in separate terminal
lixplore -R 2

# Close review window: Press 'q' or Ctrl+C
```

#### PDF Links
```bash
# Show clickable PDF links in results
lixplore -x -q "neural networks" -m 10 --show-pdf-links

# Combine with abstracts
lixplore -P -q "cancer" -m 20 -a --show-pdf-links

# Multi-source with PDF links
lixplore -A -q "COVID-19" -m 50 -D --show-pdf-links
```

---

## 🎯 Use Cases

### 1. Literature Review
```bash
# Search all sources, deduplicate, sort newest, export top 20
lixplore -A -q "machine learning healthcare" -m 100 -D \
  --sort newest -S first:20 -X xlsx -o ml_healthcare.xlsx
```

### 2. Boolean Search with Export
```bash
# Advanced query with multiple conditions
lixplore -P -q "(COVID-19 OR coronavirus) AND (vaccine OR treatment)" \
  -m 50 --sort newest -X enw -o covid_papers.enw
```

### 3. Quick Sample Review
```bash
# Search 50, export odd-numbered (25 articles)
lixplore -A -q "cancer immunotherapy" -m 50 -D \
  -S odd -X csv -o cancer_sample.csv
```

### 4. Historical Research
```bash
# Sort by oldest to study evolution
lixplore -P -q "diabetes" -m 100 --sort oldest \
  -X xlsx -o diabetes_history.xlsx
```

### 5. Multi-Step Workflow
```bash
# 1. Search
lixplore -P -q "neuroscience" -m 20

# 2. Review specific articles
lixplore -R 2 5 8

# 3. Export selected
lixplore -P -q "neuroscience" -m 20 -S 2 5 8 -X enw
```

---

## 📊 Export Formats

All exports are automatically organized into folders under `exports/` in the folder you run `lixplore` from (use `-o FILE` to choose a path yourself):

```
exports/
├── csv/              # CSV files
├── excel/            # Excel files (.xlsx)
├── json/             # JSON files
├── bibtex/           # BibTeX files
├── ris/              # RIS files
├── endnote_tagged/   # EndNote Tagged (.enw)
├── endnote_xml/      # EndNote XML files
└── xml/              # Generic XML files
```

---

## 🔧 Advanced Features

### Smart Selection Patterns

| Pattern | Syntax | Example | Result |
|---------|--------|---------|--------|
| Specific | `1 3 5` | `-S 1 3 5` | Articles #1, #3, #5 |
| Range | `1-10` | `-S 1-10` | Articles #1 through #10 |
| Odd | `odd` | `-S odd` | Odd-numbered articles |
| Even | `even` | `-S even` | Even-numbered articles |
| First N | `first:10` | `-S first:10` | First 10 articles |
| Last N | `last:5` | `-S last:5` | Last 5 articles |
| Mixed | `1 3 5-10` | `-S 1 3 5-10` | Combined patterns |

### Sort Options

- `relevant` - Default API order (most relevant first)
- `newest` - Latest publications (2025 → 2020)
- `oldest` - Earliest publications (1990 → 2000)
- `journal` - Alphabetical by journal name
- `author` - Alphabetical by first author

---

## 🖥️ Platform Support

Lixplore works on all major platforms:

- ✅ **Linux** (all distributions)
- ✅ **macOS** (10.14+)
- ✅ **Windows** (10+)

### Platform-Specific Notes

#### Linux
Review feature works with: xfce4-terminal, gnome-terminal, konsole, xterm, alacritty, kitty

#### macOS
Review feature uses Terminal.app

#### Windows
Review feature uses cmd.exe

---

## 📦 Installation Methods

| Method | Command | Best for |
|--------|---------|----------|
| **pipx** (recommended) | `pipx install lixplore-cli` | All Linux/macOS users |
| **pip + venv** | `pip install lixplore-cli` | Virtual environments |
| **AUR** | `yay -S lixplore-cli` | Arch Linux users |
| **Homebrew** | `brew install pryndor/lixplore/lixplore-cli` | macOS & Homebrew users |
| **From source** | `pip install -e .` | Development |

See [Quick Start](#-quick-start) above for detailed instructions.

---

## 🔍 Requirements

- Python 3.8 or higher (3.9+ for the full-screen TUI)
- Internet connection for API access
- Terminal emulator (for review feature)

### Dependencies

- `biopython` - PubMed/NCBI API access
- `requests` - HTTP requests
- `openpyxl` - Excel export support
- `textual` + `rich` (optional) - Full-screen TUI

All core dependencies are automatically installed. For the TUI, install with `pip install "lixplore-cli[tui]"` or `pipx inject lixplore-cli textual rich`.

---

## 📖 Man Page

After installation, install the man page using whichever method suits you:

**Option 1 — built-in command (any install method):**
```bash
lixplore --install-man
man lixplore
```

**Option 2 — from a cloned repo:**
```bash
bash docs/install_man_page.sh
man lixplore
```

The installer automatically finds the right directory, handles sudo when needed, and refreshes the man database. If `man lixplore` still fails after a user-local install, add this to your shell profile:
```bash
export MANPATH=$HOME/.local/share/man:$MANPATH
```

---

## ☕ Support the Project

If you find Lixplore useful for your research, consider supporting its development!

<a href="https://www.buymeacoffee.com/lixplore" target="_blank" rel="noopener noreferrer">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;">
</a>

**Why support?**
- ✨ Keeps the project actively maintained and updated
- 🚀 Helps add new features and integrations
- 📚 Supports free, open-source academic tools
- 🌍 Makes research more accessible to everyone

> *"If you value independent research tools and open access to literature, consider buying me a coffee ☕—it helps keep development and research going!"*

Your support enables:
- Regular updates and bug fixes
- New API integrations (IEEE Xplore, Scopus, Web of Science)
- Advanced features (LLM integration, citation networks, collaboration tools)
- Better documentation and tutorials
- Faster response to issues and feature requests

**Other ways to support:**
- ⭐ Star the repository on GitHub
- 🐛 Report bugs and issues
- 💡 Suggest new features
- 📖 Improve documentation
- 🔀 Contribute code via pull requests
- 📢 Share Lixplore with your research community

---

## 🚀 Development Roadmap

### TUI Mode Enhancement (Active Development)
We're actively working to bring all CLI features into the TUI mode. Upcoming updates will include:

- 🔄 **All CLI Flags in TUI** - Full integration of all command-line features
- 📊 **Advanced Filtering** - Date ranges, author search, DOI lookup in TUI
- 📥 **PDF Integration** - Direct PDF download and viewing from TUI
- 🔧 **Custom API Support** - GUI for adding custom data sources
- 📋 **Profile Management** - Visual interface for export profiles
- 🎯 **Citation Formatting** - Interactive citation style selection
- 📈 **Advanced Statistics** - More visualization options

**Current Status:** The Textual TUI covers search, reading, rating, annotation, library, alerts, stats and export. Enrichment, citation styles and PDF download are CLI flags for now.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📰 Reviews

Community write-ups, tutorials, and independent reviews of Lixplore:

- **[Lixplore-cli: The Ultimate Command Line Tool Revolutionizing Academic Research](https://www.scribddownload.online/2026/01/lixplore-cli-ultimate-command-line-tool.html)**
  A detailed overview of Lixplore's strengths as a Python-based CLI for researchers — covering multi-source search, export formats, scripting potential, and why the command-line approach outperforms graphical alternatives for academic workflows.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- PubMed/NCBI for providing free API access
- arXiv for open preprint access
- Crossref for DOI metadata
- DOAJ for open access journal data
- EuropePMC for European literature access

---

## Reviews

- **OSTechNix:** [https://ostechnix.com/lixplore-cli-command-line-academic-research-tool/](https://ostechnix.com/lixplore-cli-command-line-academic-research-tool/)
- **Ardreyex:**  [https://andreyex.ru/linux/lixplore-cli-instrument-komandnoj-stroki-dlya-nauchnyh-issledovanij/](https://andreyex.ru/linux/lixplore-cli-instrument-komandnoj-stroki-dlya-nauchnyh-issledovanij/)
- **Mylinux:**   [https://muylinux.xyz/lixplore-cli-una-herramienta-de-linea-de-comandos-para-investigacion-academica/](https://muylinux.xyz/lixplore-cli-una-herramienta-de-linea-de-comandos-para-investigacion-academica/)

---

## 📧 Support & Community

- **📚 Documentation:** [https://pryndor.github.io/Lixplore_cli/](https://pryndor.github.io/Lixplore_cli/)
- **🐛 Issues:** [GitHub Issues](https://github.com/pryndor/Lixplore_cli/issues)
- **❓ FAQ:** [Documentation FAQ](https://pryndor.github.io/Lixplore_cli/about/faq/)

---

## 🔗 Quick Links

- **📦 PyPI Package:** [https://pypi.org/project/lixplore-cli/](https://pypi.org/project/lixplore-cli/)
- **💻 GitHub Repository:** [https://github.com/pryndor/Lixplore_cli](https://github.com/pryndor/Lixplore_cli)
- **📚 Documentation:** [https://pryndor.github.io/Lixplore_cli/](https://pryndor.github.io/Lixplore_cli/)
- **🐛 Issue Tracker:** [https://github.com/pryndor/Lixplore_cli/issues](https://github.com/pryndor/Lixplore_cli/issues)
- **🚀 Changelog:** [https://pryndor.github.io/Lixplore_cli/about/changelog/](https://pryndor.github.io/Lixplore_cli/about/changelog/)
- **🤝 Contributing Guide:** [https://pryndor.github.io/Lixplore_cli/about/contributing/](https://pryndor.github.io/Lixplore_cli/about/contributing/)

---

**Made with ❤️ for the research community**
