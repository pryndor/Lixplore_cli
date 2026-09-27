# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Python 3.9 or newer is required (3.8 reached end of life in October 2024; source builds on it
  already failed). CI now tests 3.9 to 3.13

### Fixed
- Alerts `.env`: when a variable appears twice, the later line now wins (as in other `.env` tools).
  Before, a `LIXPLORE_QUERIES` line added below the `init` template's example was silently ignored
- Alerts `test` and `check` work before any search is set, so channels can be tested first
  (before, both stopped with "LIXPLORE_QUERIES is empty"). `run` and `dry-run` still require it
- PubMed: DOIs were missing for many older papers (the DOI was read only from `ELocationID`,
  not from the article ID list), which weakened deduplication, enrichment and PDF lookup
- PubMed: year was empty when the record only has a date range such as "2001 May 1-15"
- PubMed: when NCBI's search backend is temporarily down, requests are retried and a clear
  "temporarily unavailable" message is shown instead of the raw server error

## [1.2.1] - 2026-09-27

### Fixed
- Journal export templates (`--template`, `--list-templates`) were missing when the package was
  built straight from source, as the AUR and Homebrew packages do
- Exports were written inside the installed package (`site-packages/exports/`), which fails with a
  permission error for AUR and Homebrew installs. They now go to `exports/` in the current folder
- `--install-man` could not find the man page in pip, AUR and Homebrew installs

## [1.2.0] - 2026-09-27

### Added
- **New full-screen TUI** (`lixplore --tui`, and `-i` after a search), built on Textual
  - Research-cockpit layout: search bar with database chips, sidebar, results table and live preview
  - Results stream in per database; failed databases are reported
  - Instant rating with `1`–`5`, one-screen annotation form, full-screen reader, open in browser
  - Library view of annotated papers with filters and search; Alerts view; Stats charts
  - Filter-as-you-type, sort, multi-select and export in 8 formats
  - Mouse support, command palette, remembered theme, adapts to narrow terminals
  - `Esc` goes back from anywhere; views switch with `Ctrl+F/L/N/T` (F1–F4 also work where the terminal allows)
  - Falls back to the Rich TUI on Python 3.8 or without Textual
- `--check-tui` also reports Textual status
- Homebrew tap for macOS and Linux: `brew install pryndor/lixplore/lixplore-cli` (includes the TUI)

### Changed
- The `tui` / `all` extras now install Textual (Python 3.9+)

### Fixed
- Annotations on papers without a DOI were lost between sessions: their IDs used Python's
  per-process `hash()`. They now use a stable hash (older entries for such papers can't be matched)

## [1.1.0] - 2026-09-26

### Added
- **Paper alerts** - scheduled digests of newly published papers for your searches
  - Runs free on GitHub Actions: fork the repo, set `LIXPLORE_QUERIES` and a channel's secrets under
    Settings → Secrets and variables → Actions. No file edits needed
  - Also runs on your own computer: `lixplore --alerts init | check | test | dry-run | run | schedule`
    (or the `lixplore-alerts` command), configured with a `.env` file
  - 17 delivery channels: Email, Telegram, Discord, Slack, Microsoft Teams, Google Chat, Matrix, WeCom,
    Feishu, DingTalk, ntfy, Gotify, Pushover, PushPlus, ServerChan3, AstrBot and custom webhooks
  - Per search, each source's count of new papers with titles, plus a CSV/BibTeX/RIS attachment
  - Boolean queries (`AND`, `OR`, `NOT`, parentheses, quoted phrases) passed to each source
  - Only papers not sent before; history kept on a `lixplore-state` branch (GitHub) or `.lixplore-state/` (local)
  - Schedule by `LIXPLORE_SEND_DAYS` and `LIXPLORE_SEND_HOUR_UTC`
  - Guide: `docs/guide/alerts.md`
- Source modules accept an optional `since` date to fetch only recently added records
- `--check-tui` diagnoses Rich / TUI installation problems
- `--install-man` installs the `lixplore` man page
- Arch Linux `PKGBUILD` and Homebrew formula

### Changed
- TUI reworked; Rich detection centralised in `utils/rich_check.py`
- Rich moved to the optional `tui` / `all` extras
- arXiv requests use HTTPS

### Removed
- Unused `litstudy` dependency

### Fixed
- README no longer claims that running `lixplore` with no arguments opens the TUI

## [1.0.1] - 2026-01-04

### Fixed
- **TUI Mode Deduplication Error** - Fixed TypeError when using deduplication in TUI mode
  - Changed incorrect parameter names in `enhanced_tui.py`:
    - `threshold` → `title_threshold`
    - `keep` → `keep_preference`
    - `merge_data` → `merge_metadata`
  - TUI mode now properly calls `deduplicate_advanced()` with correct parameters
  - Resolves: "deduplicate_advanced() got an unexpected keyword argument 'threshold'"

### Changed
- Improved error handling and parameter validation in TUI search workflow

## [1.0.0] - 2025-12-28

### Added - Major Export Enhancement Update

**New Export Features:**
- **Citation Style Export** - Export formatted citations in APA, MLA, Chicago, IEEE styles (`-C`)
- **Batch Export** - Export to multiple formats simultaneously (`-X csv,ris,bibtex`)
- **Export Field Filtering** - Select specific fields to export (`--export-fields title authors year doi`)
- **Metadata Enrichment** - Enrich results using CrossRef, PubMed, arXiv APIs (`--enrich`)
- **DOI Resolution** - Automatically validate and find missing DOIs (integrated with enrichment)
- **Export Templates** - Use predefined templates for journals (`--template nature`)
- **Export Compression** - Auto-compress exports to ZIP (`--zip`)
- **Export Profiles** - Save and reuse export configurations (`--save-profile`, `--load-profile`)
- **Enhanced Deduplication** - Advanced strategies with metadata merging (`-D strict --dedup-merge`)

**New CLI Flags:**
- `-C, --citation STYLE` - Export as formatted citations (apa|mla|chicago|ieee)
- `-X FORMAT[,FORMAT...]` - Batch export to multiple formats (comma-separated)
- `--export-fields FIELD [FIELD ...]` - Select specific fields to export
- `--enrich [API ...]` - Enrich metadata (crossref|pubmed|arxiv|all)
- `--template NAME` - Use predefined export template (nature|science|ieee)
- `--zip` - Compress exported files to ZIP
- `--save-profile NAME` - Save current export settings as profile
- `--load-profile NAME` - Load saved export profile
- `--list-profiles` - List all saved profiles
- `--delete-profile NAME` - Delete saved profile
- `--list-templates` - List all available templates
- `-D [STRATEGY]` - Enhanced deduplication (auto|strict|loose|doi_only|title_only)
- `--dedup-threshold FLOAT` - Title similarity threshold (0.0-1.0, default: 0.85)
- `--dedup-keep STRATEGY` - Which duplicate to keep (first|most_complete|prefer_doi)
- `--dedup-merge` - Merge metadata from duplicates

**New Modules:**
- `lixplore/utils/citations.py` - Citation formatting engine
- `lixplore/utils/enrichment.py` - Metadata enrichment and DOI resolution
- `lixplore/utils/profiles.py` - Profile management
- `lixplore/utils/template_engine.py` - Template processing
- `lixplore/templates/` - Built-in templates (nature, science, ieee)

**New Export Features:**
- `exports/citations/` - Citation format exports folder
- `~/.lixplore/profiles.json` - User profiles storage
- `~/.lixplore/templates/` - User custom templates folder

### Changed
- `-D, --deduplicate` now accepts optional strategy parameter
- `-X, --export` now supports comma-separated format list for batch export
- Enhanced deduplication with configurable strategies and metadata merging
- Improved field filtering across all export formats

### Removed
- `-Z, --zotero` flag (replaced by RIS export which works with Zotero)
- Stub Zotero integration function (use `-X ris` instead)

### Fixed
- Deduplication now properly handles metadata completeness scoring
- Export field filtering now validates field names
- Better handling of missing metadata fields

### Added
- Multi-source search across 5 academic databases (PubMed, arXiv, Crossref, DOAJ, EuropePMC)
- Boolean operator support (AND, OR, NOT, parentheses)
- 8 export formats (CSV, Excel, JSON, BibTeX, RIS, EndNote XML, EndNote Tagged, XML)
- Smart selection patterns (odd, even, ranges, first:N, last:N, top:N)
- Sorting options (relevant, newest, oldest, journal, author)
- Review feature - view articles in separate terminal windows
- Deduplication across multiple sources
- Organized export folders by format type
- Date range filtering
- Author and DOI search
- Complete documentation (man page, help, examples, TLDR)
- Cross-platform support (Linux, macOS, Windows)

### Features
- `-P, --pubmed` - Search PubMed
- `-C, --crossref` - Search Crossref
- `-J, --doaj` - Search DOAJ
- `-E, --europepmc` - Search EuropePMC
- `-x, --arxiv` - Search arXiv
- `-A, --all` - Search all sources
- `-s, --sources` - Combined source selection
- `-q, --query` - Search query with Boolean operators
- `-au, --author` - Search by author
- `-DOI, --doi` - Search by DOI
- `-m, --max_results` - Maximum results (default: 10)
- `-d, --date` - Date range filter
- `-D, --deduplicate` - Remove duplicates
- `--sort` - Sort results (relevant, newest, oldest, journal, author)
- `-a, --abstract` - Show abstracts
- `-N, --number` - View details in console
- `-R, --review` - Review in separate terminal
- `-st, --stat` - Get statistics
- `-X, --export` - Export format
- `-o, --output` - Custom output filename
- `-S, --select` - Smart selection
- `-H, --history` - Show search history
- `--examples` - Show quick examples
- `-h, --help` - Show help message

### Documentation
- Comprehensive README with examples
- Professional Unix man page
- Quick examples (TLDR-style)
- Complete help system
- API documentation

### Package Distribution
- PyPI package support
- Cross-platform compatibility (Linux, macOS, Windows)
- Python 3.7+ support
- Modern packaging with pyproject.toml
- GitHub Actions for CI/CD
- Automated testing across platforms

## Planned Features

- Citation network visualization
- Bookmarking system
- Web interface
- Batch processing from file

---

For more details, see the [README](https://github.com/pryndor/Lixplore_cli#readme).
