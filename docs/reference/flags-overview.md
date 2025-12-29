# Lixplore Command-Line Flags - Complete Reference

> **Comprehensive overview of all 95+ command-line flags organized by category**

## Table of Contents

- [Quick Index](#quick-index)
- [Summary Table](#summary-table)
- [Flag Categories](#flag-categories)
- [Common Flag Combinations](#common-flag-combinations)
- [Best Practices](#best-practices)

---

## Quick Index

### Source Selection (8 flags)
- [`-P, --pubmed`](#source-flags) - Search PubMed
- [`-C, --crossref`](#source-flags) - Search Crossref
- [`-J, --doaj`](#source-flags) - Search DOAJ
- [`-E, --europepmc`](#source-flags) - Search EuropePMC
- [`-x, --arxiv`](#source-flags) - Search arXiv
- [`-A, --all`](#source-flags) - Search all sources
- [`-s, --sources`](#source-flags) - Combined source codes
- [`--custom-api`](#source-flags) - Custom API integration

### Search Parameters (4 flags)
- [`-q, --query`](#search-flags) - Search query with Boolean operators
- [`-au, --author`](#search-flags) - Search by author name
- [`-DOI, --doi`](#search-flags) - Search by DOI
- [`-m, --max_results`](#search-flags) - Maximum results per source

### Filtering & Processing (7 flags)
- [`-d, --date`](#filter-flags) - Date range filter
- [`-D, --deduplicate`](#filter-flags) - Remove duplicates
- [`--dedup-threshold`](#filter-flags) - Similarity threshold
- [`--dedup-keep`](#filter-flags) - Which duplicate to keep
- [`--dedup-merge`](#filter-flags) - Merge duplicate metadata
- [`--sort`](#filter-flags) - Sort results
- [`--enrich`](#filter-flags) - Enrich metadata

### Display Options (9 flags)
- [`-a, --abstract`](#display-flags) - Show abstracts
- [`-i, --interactive`](#display-flags) - Simple TUI mode
- [`-N, --number`](#display-flags) - View article details
- [`-R, --review`](#display-flags) - Review in terminal
- [`--stat`](#display-flags) - Statistics dashboard
- [`--stat-top`](#display-flags) - Top N in stats
- [`-p, --page`](#display-flags) - Page number
- [`--page-size`](#display-flags) - Results per page
- [`--show-pdf-links`](#display-flags) - Display PDF links

### Export & Output (15 flags)
- [`-X, --export`](#export-flags) - Export format(s)
- [`-o, --output`](#export-flags) - Output filename
- [`-S, --select`](#export-flags) - Select articles
- [`--export-fields`](#export-flags) - Select fields
- [`--zip`](#export-flags) - Compress exports
- [`-c, --citations`](#export-flags) - Citation style
- [`--save-profile`](#export-flags) - Save settings
- [`--load-profile`](#export-flags) - Load settings
- [`--template`](#export-flags) - Use template
- [`--download-pdf`](#export-flags) - Download PDFs
- [`--pdf-numbers`](#export-flags) - PDF article numbers
- [`--use-scihub`](#export-flags) - Use SciHub
- [`--add-to-zotero`](#export-flags) - Add to Zotero
- [`--zotero-collection`](#export-flags) - Zotero collection
- [`--export-for-mendeley`](#export-flags) - Mendeley export

### Annotations (13 flags)
- [`--annotate`](#annotation-flags) - Annotate article
- [`--comment`](#annotation-flags) - Add comment
- [`--rating`](#annotation-flags) - Rate article
- [`--tags`](#annotation-flags) - Add tags
- [`--read-status`](#annotation-flags) - Set read status
- [`--priority`](#annotation-flags) - Set priority
- [`--show-annotation`](#annotation-flags) - Show annotation
- [`--list-annotations`](#annotation-flags) - List all
- [`--filter-annotations`](#annotation-flags) - Filter annotations
- [`--search-annotations`](#annotation-flags) - Search annotations
- [`--export-annotations`](#annotation-flags) - Export annotations
- [`--annotation-stats`](#annotation-flags) - Annotation statistics
- [`--delete-annotation`](#annotation-flags) - Delete annotation

### Interactive Modes (3 flags)
- [`--tui`](#interactive-flags) - Enhanced TUI mode
- [`--shell`](#interactive-flags) - Shell mode (deprecated)
- [`--wizard`](#interactive-flags) - Wizard mode (deprecated)

### Utility (12 flags)
- [`-H, --history`](#utility-flags) - Search history
- [`--refresh`](#utility-flags) - Bypass cache
- [`--examples`](#utility-flags) - Show examples
- [`--list-profiles`](#utility-flags) - List profiles
- [`--delete-profile`](#utility-flags) - Delete profile
- [`--list-templates`](#utility-flags) - List templates
- [`--list-custom-apis`](#utility-flags) - List custom APIs
- [`--create-api-examples`](#utility-flags) - Create API examples
- [`--set-scihub-mirror`](#utility-flags) - Configure SciHub
- [`--show-pdf-dir`](#utility-flags) - Show PDF directory
- [`--configure-zotero`](#utility-flags) - Configure Zotero
- [`--show-zotero-collections`](#utility-flags) - Show collections

---

## Summary Table

| Category | Flags | Purpose |
|----------|-------|---------|
| **Source Selection** | 8 | Choose databases to search |
| **Search Parameters** | 4 | Define search criteria |
| **Filtering** | 7 | Filter and process results |
| **Display** | 9 | Control result display |
| **Export** | 15 | Export and save results |
| **Annotations** | 13 | Organize and rate articles |
| **Interactive** | 3 | Interactive modes |
| **Utility** | 12 | Configuration and helpers |
| **TOTAL** | **71** | All available flags |

---

## Flag Categories

### 1. Source Selection Flags
Choose which academic databases to search. Multiple sources can be combined.

**Available Sources:**
- PubMed (biomedical literature)
- Crossref (scholarly works with DOIs)
- DOAJ (open access journals)
- EuropePMC (European literature)
- arXiv (preprints)
- Custom APIs (user-configured)

**See:** [source-flags.md](source-flags.md) for complete documentation

### 2. Search Parameter Flags
Define what to search for and how many results to retrieve.

**Search Types:**
- Query search with Boolean operators
- Author search
- DOI lookup

**See:** [search-flags.md](search-flags.md) for complete documentation

### 3. Filtering & Processing Flags
Process and refine search results after retrieval.

**Features:**
- Date range filtering
- Duplicate removal (5 strategies)
- Result sorting (5 methods)
- Metadata enrichment

**See:** [filter-flags.md](filter-flags.md) for complete documentation

### 4. Display Option Flags
Control how results are displayed in the terminal.

**Features:**
- Abstract display
- Interactive browsing
- Pagination
- Statistics dashboard
- PDF link display

**See:** [display-flags.md](display-flags.md) for complete documentation

### 5. Export & Output Flags
Export results in various formats and manage output.

**Export Formats:** CSV, Excel, JSON, BibTeX, RIS, EndNote, XML
**Citations:** APA, MLA, Chicago, IEEE

**See:** [export-flags.md](export-flags.md) for complete documentation

### 6. Annotation Flags
Rate, tag, comment, and organize your research library.

**Features:**
- 5-star rating system
- Comments and notes
- Tag organization
- Read status tracking
- Priority levels

**See:** [annotation-flags.md](annotation-flags.md) for complete documentation

### 7. Interactive Mode Flags
Launch interactive interfaces for easier usage.

**Modes:**
- **Enhanced TUI** (primary interface - recommended)
- Shell mode (persistent session - deprecated)
- Wizard mode (guided workflows - deprecated)

**Note:** Shell and wizard modes are deprecated in favor of the enhanced TUI.

**See:** [interactive-flags.md](interactive-flags.md) for complete documentation

### 8. Utility Flags
Configuration, management, and helper commands.

**Features:**
- Search history
- Profile management
- Template management
- API configuration

**See:** [utility-flags.md](utility-flags.md) for complete documentation

---

## Common Flag Combinations

### Basic Search + Export
```bash
lixplore -P -q "cancer" -m 20 -X xlsx
```
**Flags:** `-P` (PubMed), `-q` (query), `-m` (max results), `-X` (export)

### Multi-Source with Deduplication
```bash
lixplore -A -q "COVID-19" -m 50 -D --sort newest -X csv
```
**Flags:** `-A` (all sources), `-q`, `-m`, `-D` (deduplicate), `--sort`, `-X`

### Advanced Search with Filters
```bash
lixplore -s PX -q "machine learning" -d 2020-01-01 2024-12-31 -m 30 -D strict --enrich -X xlsx
```
**Flags:** `-s` (sources), `-q`, `-d` (date), `-m`, `-D`, `--enrich`, `-X`

### Review Workflow
```bash
# Step 1: Search
lixplore -P -q "diabetes" -m 20 -a

# Step 2: Review specific articles
lixplore -R 3 5 8

# Step 3: Annotate
lixplore --annotate 3 --rating 5 --tags "important,methodology"
```

### Smart Selection + Export
```bash
lixplore -P -q "research" -m 100 --sort newest -S first:20 -X enw,csv
```
**Flags:** `-P`, `-q`, `-m`, `--sort`, `-S` (select), `-X` (multi-format)

### Statistics Dashboard
```bash
lixplore -A -q "artificial intelligence" -m 200 -D --stat --stat-top 15
```
**Flags:** `-A`, `-q`, `-m`, `-D`, `--stat`, `--stat-top`

### PDF Download Workflow
```bash
lixplore -x -q "neural networks" -m 10 --download-pdf --pdf-numbers 1 3 5
```
**Flags:** `-x` (arXiv), `-q`, `-m`, `--download-pdf`, `--pdf-numbers`

### Reference Manager Integration
```bash
lixplore -P -q "genetics" -m 30 -D --add-to-zotero --zotero-collection ABC123
```
**Flags:** `-P`, `-q`, `-m`, `-D`, `--add-to-zotero`, `--zotero-collection`

---

## Best Practices

### 1. Always Use Deduplication with Multiple Sources
```bash
# Good
lixplore -A -q "query" -m 50 -D

# Not recommended (will have duplicates)
lixplore -A -q "query" -m 50
```

### 2. Specify Max Results Per Source
```bash
# Clear and efficient
lixplore -s PCE -q "query" -m 30  # 30 per source

# Unclear (uses default 10)
lixplore -s PCE -q "query"
```

### 3. Use Sorting for Better Organization
```bash
# Latest research first
lixplore -P -q "COVID-19" -m 100 --sort newest

# Historical perspective
lixplore -P -q "diabetes" -m 100 --sort oldest
```

### 4. Combine Selection with Export
```bash
# Export only top results
lixplore -P -q "AI" -m 100 --sort newest -S first:20 -X xlsx
```

### 5. Save Profiles for Repeated Workflows
```bash
# Save settings
lixplore -P -q "query" -m 50 -X xlsx --export-fields title authors year doi --save-profile my_workflow

# Reuse later
lixplore -P -q "different query" --load-profile my_workflow
```

### 6. Use Enrichment for Complete Metadata
```bash
# Enrich from all APIs
lixplore -A -q "query" -m 50 -D --enrich -X bibtex
```

### 7. Cache Management
```bash
# Bypass cache for fresh results
lixplore -P -q "breaking news" -m 10 --refresh

# Use cached results (faster)
lixplore -R 1 2 3  # Review from cache
```

### 8. Annotation Workflow
```bash
# Search and review
lixplore -P -q "topic" -m 20 -a

# Annotate important articles
lixplore --annotate 5 --rating 5 --tags "important,cite" --comment "Excellent methodology"

# Filter and export annotations
lixplore --filter-annotations "min_rating=4,priority=high"
lixplore --export-annotations markdown
```

---

## Flag Syntax Rules

### Boolean Flags (no value needed)
```bash
-P, -A, -D, -a, --stat, --zip, --refresh
```
**Usage:** Just add the flag
```bash
lixplore -P -q "query" -D
```

### Value Flags (require value)
```bash
-q TEXT, -m NUMBER, -X FORMAT, -o FILE
```
**Usage:** Flag followed by value
```bash
lixplore -P -q "cancer" -m 20 -X xlsx
```

### Multi-Value Flags (accept multiple values)
```bash
-d FROM TO, -N 1 2 3, -S odd even 1-10, --export-fields title authors year
```
**Usage:** Flag followed by multiple values
```bash
lixplore -P -q "query" -N 1 2 3 -S first:10 last:5
```

### Optional Value Flags (work with or without value)
```bash
-D [STRATEGY], --enrich [API...]
```
**Usage:**
```bash
lixplore -A -q "query" -D           # Uses default strategy
lixplore -A -q "query" -D strict    # Uses strict strategy
```

---

## Performance Tips

### 1. Optimize Search Scope
```bash
# Faster (single source)
lixplore -P -q "query" -m 20

# Slower (all sources)
lixplore -A -q "query" -m 20
```

### 2. Use Pagination for Large Results
```bash
# View first page
lixplore -P -q "query" -m 100 -p 1

# View next page
lixplore -P -q "query" -m 100 -p 2
```

### 3. Limit Enrichment Scope
```bash
# Enrich from specific API only
lixplore -P -q "query" -m 50 --enrich crossref

# Enrich from all (slower)
lixplore -P -q "query" -m 50 --enrich
```

### 4. Export Selected Articles Only
```bash
# Export all (slow for large sets)
lixplore -P -q "query" -m 500 -X xlsx

# Export selection (faster)
lixplore -P -q "query" -m 500 -S first:50 -X xlsx
```

---

## Troubleshooting

### Common Issues

**Problem:** No results found
```bash
# Solution: Try broader query or different source
lixplore -A -q "cancer"  # Search all sources
```

**Problem:** Too many duplicates
```bash
# Solution: Use deduplication
lixplore -A -q "query" -m 50 -D
```

**Problem:** Missing metadata
```bash
# Solution: Use enrichment
lixplore -P -q "query" -m 20 --enrich
```

**Problem:** Export file not found
```bash
# Solution: Check exports/ folder organization
# CSV files: exports/csv/
# Excel: exports/excel/
# etc.
```

---

## Getting Help

### Built-in Help
```bash
# Quick examples
lixplore --examples

# Complete help
lixplore --help

# Man page
man lixplore
```

### Detailed Documentation
- [Source Flags](source-flags.md)
- [Search Flags](search-flags.md)
- [Filter Flags](filter-flags.md)
- [Display Flags](display-flags.md)
- [Export Flags](export-flags.md)
- [Annotation Flags](annotation-flags.md)
- [Interactive Flags](interactive-flags.md)
- [Utility Flags](utility-flags.md)

---

## Version Information

**Lixplore Version:** 2.0+
**Total Flags:** 71
**Documentation Updated:** 2024-12-28

For updates and more information, visit the [GitHub repository](https://github.com/yourusername/lixplore).
