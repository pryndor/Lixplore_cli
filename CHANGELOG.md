# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
- `-Z, --zotero` - Export to Zotero
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
