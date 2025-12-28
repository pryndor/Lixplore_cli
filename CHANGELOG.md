# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-12-24

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

## [1.0.0] - 2024-12-19

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

## [Unreleased]

### Planned Features
- PDF download support
- Citation network visualization
- Bookmarking system
- Search profiles
- Web interface
- Batch processing from file

---

For more details, see the [README](README.md).
