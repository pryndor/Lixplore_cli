# Lixplore New Features Guide

This document provides a comprehensive guide to all the new features added to Lixplore.

## Table of Contents

1. [Smart Caching with Expiration](#1-smart-caching-with-expiration)
2. [Pagination for Large Result Sets](#2-pagination-for-large-result-sets)
3. [Custom API Integration System](#3-custom-api-integration-system)
4. [Statistics Dashboard with Visualizations](#4-statistics-dashboard-with-visualizations)
5. [PDF Download Integration](#5-pdf-download-integration)
   - 5.5. [PDF Link Display (NEW!)](#55-pdf-link-display-new)
6. [Reference Manager Integration](#6-reference-manager-integration)
7. [Interactive TUI Mode](#7-interactive-tui-mode)

---

## 1. Smart Caching with Expiration

### Overview
Search results are now cached with timestamps and automatically expire after 7 days. Cache status is shown when using cached data.

### New Flags
- `--refresh` - Bypass cache and fetch fresh results

### How It Works
- First search: Results cached with timestamp
- Subsequent searches: Uses cache if < 7 days old
- Automatic messages: "Using cached results (2 days old)"
- Expiration warning: "Cache expired (older than 7 days)"

### Examples
```bash
# Normal search (uses cache if available)
lixplore -P -q "cancer research" -m 50

# Force fresh search
lixplore -P -q "cancer research" -m 50 --refresh

# Review cached results without new search
lixplore -R 1 2 3
```

### Technical Details
- Cache location: `~/.lixplore_cache.json`
- Format: JSON with metadata (timestamp, query, sources, results)
- Backwards compatible with old cache format

---

## 2. Pagination for Large Result Sets

### Overview
Automatic pagination when results exceed page size (default: 20). Makes browsing large result sets much easier.

### New Flags
- `-p, --page N` - View specific page number
- `--page-size N` - Set results per page (default: 20)

### How It Works
- Automatically activates when results > page_size
- Shows: "Page 1 of 5 | Showing 1-20 of 100 results"
- Helpful navigation hints
- Works with all other features (export, review, etc.)

### Examples
```bash
# Fetch 100 results, view page 1
lixplore -P -q "machine learning" -m 100

# View page 2
lixplore -P -q "machine learning" -m 100 -p 2

# Custom page size (50 per page)
lixplore -P -q "AI research" -m 200 --page-size 50

# Page 3 with custom size
lixplore -P -q "AI research" -m 200 --page-size 50 -p 3
```

### Technical Details
- Pagination logic in `lixplore/dispatcher.py`
- Smart page validation (clamps to valid range)
- All article numbers remain absolute (1-100, not 1-20 per page)

---

## 3. Custom API Integration System

### Overview
Plugin architecture allowing users to add ANY API source via simple JSON configuration. No code modification needed!

### New Flags
- `--custom-api NAME` - Search using custom API
- `--list-custom-apis` - List configured APIs
- `--create-api-examples` - Create example configs

### Supported by Default
- Springer Nature API
- BASE (Bielefeld Academic Search Engine)
- Any REST API with JSON responses

### How to Configure

#### Step 1: Create Example Configs
```bash
lixplore --create-api-examples
```

#### Step 2: Edit Configuration
Edit `~/.lixplore/apis/springer.json`:
```json
{
  "name": "Springer",
  "description": "Springer Nature API for scientific articles",
  "base_url": "http://api.springernature.com/meta/v2/json",
  "requires_auth": true,
  "api_key": "YOUR_API_KEY_HERE",
  "query_param": "q",
  "limit_param": "p",
  "response_path": "records",
  "field_mapping": {
    "title": "title",
    "authors": "creators[*].creator",
    "abstract": "abstract",
    "doi": "doi",
    "year": "publicationDate",
    "journal": "publicationName"
  }
}
```

#### Step 3: Use Custom API
```bash
# Search Springer
lixplore --custom-api springer -q "quantum physics" -m 20

# List configured APIs
lixplore --list-custom-apis

# Combine with standard sources
lixplore -P --custom-api springer -q "biology" -m 30 -D
```

### Configuration Options
- `name` - Display name
- `description` - Description (optional)
- `base_url` - API endpoint URL
- `requires_auth` - Whether API key required
- `api_key` - Your API key (if required)
- `query_param` - Query parameter name (e.g., "q")
- `limit_param` - Limit parameter name (e.g., "limit")
- `response_path` - JSON path to results array
- `field_mapping` - Map API fields to standard fields

### Technical Details
- Implementation: `lixplore/utils/custom_apis.py`
- Config location: `~/.lixplore/apis/` or `~/.lixplore/custom_apis.json`
- Automatic field extraction and normalization
- Error handling for missing/invalid configs

---

## 4. Statistics Dashboard with Visualizations

### Overview
Comprehensive statistical analysis with ASCII visualizations including publication trends, top journals, top authors, and source distribution.

### New Flags
- `--stat` - Show statistics dashboard
- `--stat-top N` - Number of top items to show (default: 10)

### What It Shows
- **Basic Statistics**: Total articles, abstract %, DOI %, year range
- **Publication Trends**: Bar chart by year
- **Top Journals**: Ranked bar chart
- **Top Authors**: Ranked bar chart
- **Source Distribution**: Where results came from

### Examples
```bash
# Basic statistics
lixplore -P -q "machine learning" -m 100 --stat

# Show top 20 items
lixplore -A -q "COVID-19" -m 200 --stat --stat-top 20

# With deduplication
lixplore -A -q "cancer research" -m 150 -D --stat

# Combined with export
lixplore -P -q "AI" -m 100 --stat -X xlsx
```

### Sample Output
```
📊 LITERATURE STATISTICS DASHBOARD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 Basic Statistics
Total Articles: 100
With Abstract: 85 (85.0%)
With DOI: 92 (92.0%)
Year Range: 2015-2024

📅 Publication Trends by Year
2024 │ ████████████████ 32
2023 │ ██████████████ 28
2022 │ ██████████ 20
...

📚 Top 10 Journals
Nature               │ ██████████████████ 15
Science              │ ████████████ 10
Cell                 │ ██████████ 8
...
```

### Technical Details
- Implementation: `lixplore/utils/statistics.py`
- Unicode detection for enhanced charts
- Automatic fallback to ASCII
- Handles missing data gracefully

---

## 5. PDF Download Integration

### Overview
Automatically downloads full-text PDFs from multiple sources with smart fallback chain.

### New Flags
- `--download-pdf` - Download PDFs for results
- `--pdf-numbers N [N...]` - Download specific articles only
- `--use-scihub` - Use SciHub as fallback
- `--set-scihub-mirror URL` - Configure SciHub mirror
- `--show-pdf-dir` - Show PDF directory info

### Download Priority
1. **PubMed Central (PMC)** - Open access articles
2. **arXiv** - Preprint repository
3. **DOI Resolution (Unpaywall)** - Legal open access
4. **SciHub** (optional) - User-configured fallback

### How to Use

#### Basic Download
```bash
# Download all results
lixplore -P -q "open access" -m 10 --download-pdf

# Download specific articles
lixplore -P -q "research" -m 50 --download-pdf --pdf-numbers 1 3 5 10
```

#### With SciHub (Optional)
```bash
# Configure SciHub mirror (one-time)
lixplore --set-scihub-mirror https://sci-hub.se

# Use SciHub as fallback
lixplore -P -q "article" -m 20 --download-pdf --use-scihub
```

#### Check Downloads
```bash
# Show PDF directory and count
lixplore --show-pdf-dir
```

### Output Format
```
📥 Downloading 10 PDF(s)...

[1/10] ✓ Downloaded from PMC: ~/Lixplore_PDFs/PubMed/article_title.pdf
[2/10] ✓ Downloaded from arXiv: ~/Lixplore_PDFs/arXiv/preprint.pdf
[3/10] ✗ PDF not available: Article title...
...

📊 Download Summary: 7 successful, 3 failed
📁 PDFs saved to: ~/Lixplore_PDFs/
```

### PDF Organization
```
~/Lixplore_PDFs/
├── PubMed/
│   ├── article1.pdf
│   └── article2.pdf
├── arXiv/
│   └── preprint.pdf
├── Crossref/
│   └── paper.pdf
└── ...
```

### Legal & Ethical Considerations
- **Prioritizes legal sources**: PMC, arXiv, Unpaywall
- **SciHub optional**: User must explicitly configure and enable
- **Respects copyright**: Users responsible for compliance
- **Use disclaimer**: "Use at your own discretion"

### Technical Details
- Implementation: `lixplore/utils/pdf_downloader.py`
- SciHub config: `~/.lixplore/scihub_mirror.txt`
- Automatic PDF validation (checks magic bytes)
- Cleanup on failed downloads
- Filename sanitization

---

## 5.5. PDF Link Display (NEW!)

### Overview
Display clickable PDF links for open access articles directly in search results without downloading. Perfect for quick access to PDFs without storing them locally.

### New Flag
- `--show-pdf-links` - Display PDF links for open access articles

### Features
- **No Download Required**: Links displayed directly in terminal
- **Clickable Links**: Works in modern terminals with OSC 8 support
- **Multiple Sources**: Checks PMC, arXiv, and Unpaywall
- **Fast**: Checks all articles in batch
- **Smart Detection**: Automatically extracts PDF URLs

### How to Use

#### Basic Usage
```bash
# Show PDF links in search results
lixplore -x -q "machine learning" -m 10 --show-pdf-links

# Combine with abstracts
lixplore -P -q "cancer" -m 20 -a --show-pdf-links

# Multi-source with deduplication
lixplore -A -q "COVID-19" -m 50 -D --show-pdf-links
```

#### Terminal Compatibility
Works with clickable links in:
- ✅ iTerm2 (macOS)
- ✅ GNOME Terminal 3.x+ (Linux)
- ✅ Konsole (KDE)
- ✅ Windows Terminal (Windows 10+)
- ✅ kitty, Alacritty, WezTerm

In terminals without OSC 8 support, the full URL is still displayed and can be copied.

### Output Format
```
🔍 Checking for open access PDFs...
✓ Found 3 PDF(s) available

[1] Neural Networks for Data Science
    📄 Open PDF → https://arxiv.org/pdf/2306.14753.pdf
[2] Machine Learning in Healthcare
    📄 Open PDF → https://arxiv.org/pdf/2307.05639.pdf
[3] Deep Learning Applications
    📄 Open PDF → https://arxiv.org/pdf/2901.06610.pdf
```

### How It Works
1. **PMC (PubMed Central)**: Checks for PMCID and generates PMC PDF link
2. **arXiv**: Extracts arXiv ID from URL and generates PDF link
3. **Unpaywall API**: For DOI-based articles, queries Unpaywall for open access PDFs

### Examples

#### arXiv Papers (Best for PDFs)
```bash
lixplore -x -q "neural networks" -m 10 --show-pdf-links
```

#### PubMed Open Access
```bash
lixplore -P -q "open access" -m 20 --show-pdf-links
```

#### Combined with Other Features
```bash
# With sorting and selection
lixplore -x -q "deep learning" -m 50 --sort newest --show-pdf-links -S first:10

# With pagination
lixplore -A -q "AI" -m 100 --show-pdf-links -p 1 --page-size 20

# Full workflow
lixplore -A -q "COVID-19 vaccine" -m 50 -D --show-pdf-links --sort newest -a
```

### Technical Details
- Implementation: `lixplore/utils/pdf_downloader.py` (functions: `get_pdf_link()`, `get_pdf_links_batch()`)
- Display: `lixplore/dispatcher.py` (function: `make_clickable_link()`, `show_results()`)
- OSC 8 escape sequences for terminal hyperlinks
- Timeout: 5 seconds per Unpaywall API request
- No rate limiting (batch processing)

### Advantages vs. Download
| Feature | PDF Links | PDF Download |
|---------|-----------|--------------|
| **Speed** | Instant | Slow (downloads files) |
| **Storage** | No disk space used | Requires disk space |
| **Access** | Click to open in browser | Local file access |
| **Updates** | Always latest version | Static snapshot |
| **Use Case** | Quick browsing | Offline reading |

### Tips
- Use with arXiv for guaranteed PDF availability
- Combine with `-a` to see abstracts before clicking PDFs
- Works great with `--sort newest` to find latest papers with PDFs
- Perfect for literature reviews - quickly scan titles and click interesting papers

---

## 6. Reference Manager Integration

### Overview
Direct integration with Zotero API and RIS export for Mendeley.

### New Flags
- `--add-to-zotero` - Add to Zotero library
- `--zotero-collection KEY` - Add to specific collection
- `--export-for-mendeley` - Export RIS for Mendeley
- `--configure-zotero API_KEY USER_ID` - Configure Zotero
- `--show-zotero-collections` - List collections

### Zotero Integration

#### Setup (One-Time Configuration)

**Step 1: Get API Key**
1. Go to https://www.zotero.org/settings/keys
2. Click **"Create new private key"**
3. Give it a name (e.g., "Lixplore CLI")
4. Enable permissions:
   - ✅ **Allow library access**
   - ✅ **Allow write access** (IMPORTANT!)
5. Click **"Save Key"**
6. **Copy the API key** (shown only once!)

**Step 2: Get User ID**
- Your **User ID** is displayed at the top of the same page (e.g., `1234567`)

**Step 3: Configure Lixplore**
```bash
lixplore --configure-zotero YOUR_API_KEY YOUR_USER_ID
```

**Example:**
```bash
lixplore --configure-zotero abc123XYZ789key 1234567
```

**Step 4: Get Collection Keys (Optional)**
```bash
# List all your Zotero collections with their keys
lixplore --show-zotero-collections
```

**Alternative ways to get Collection Key:**
- **Web**: Go to https://www.zotero.org → Click collection → Copy key from URL (e.g., `4FCVPNAP`)
- **Desktop**: Right-click collection → "Copy Collection Key"

#### Usage
```bash
# Add to main Zotero library
lixplore -P -q "machine learning" -m 10 --add-to-zotero

# Add to specific collection (using collection key)
lixplore -P -q "AI research" -m 20 --add-to-zotero --zotero-collection 4FCVPNAP

# Combined with deduplication and sorting
lixplore -A -q "COVID-19" -m 50 -D --sort newest --add-to-zotero --zotero-collection 4FCVPNAP

# Combined with search and export (add to Zotero AND export to BibTeX)
lixplore -A -q "machine learning" -m 50 -D --add-to-zotero -X bibtex
```

#### Troubleshooting

**Error: "Zotero API not configured"**
- Solution: Run `lixplore --configure-zotero YOUR_API_KEY YOUR_USER_ID`

**Error: "Invalid API key"**
- Check your API key is correct
- Ensure it has **write permissions** enabled
- Regenerate key if needed

**Error: "Collection not found"**
- Verify collection key is correct using `lixplore --show-zotero-collections`
- Collection key is case-sensitive (e.g., `4FCVPNAP`)

**Items not appearing in collection:**
- Check if items were added to main library
- Verify collection key is correct
- Ensure you have permission to add to that collection

### Mendeley Integration

```bash
# Export for Mendeley Desktop
lixplore -P -q "biology" -m 30 --export-for-mendeley

# Then in Mendeley: File → Import → RIS
```

### What Gets Sent to Zotero
- Title, abstract, journal
- Authors (properly formatted)
- DOI, URL
- Publication year
- Source tag (e.g., "source:PubMed")
- Collection assignment (if specified)

### Output Format
```
📚 Adding 10 article(s) to Zotero...

[1/10] ✓ Article Title One...
[2/10] ✓ Article Title Two...
[3/10] ✗ Article Title Three... (HTTP 400)
...

✓ Zotero import complete: 8 successful, 2 failed
```

### Technical Details
- Implementation: `lixplore/utils/reference_managers.py`
- Zotero API v3
- Config: `~/.lixplore/refman_config.json`
- Automatic author parsing
- Tag management
- Collection support

---

## 7. Interactive TUI Mode

### Overview
Full-featured interactive terminal UI for browsing, viewing, selecting, and exporting articles.

### New Flag
- `-i, --interactive` - Launch interactive mode

### Features
- **Navigation**: Next/prev pages, goto page
- **Article viewing**: Detailed information display
- **Selection**: Multi-select articles for export
- **Export**: Export selected to any format
- **Enhanced UI**: Rich library support (optional)

### Installation
```bash
# For enhanced UI (optional but recommended)
pip install rich

# Without rich, falls back to simple mode
```

### Usage
```bash
# Launch interactive mode
lixplore -P -q "machine learning" -m 50 -i
```

### Commands in Interactive Mode

#### Navigation
- `n` or `next` - Next page
- `p` or `prev` - Previous page
- `g<N>` - Go to page N (e.g., `g3`)

#### Article Operations
- `v` or `view` - View detailed article info
- `s` or `select` - Toggle article selection
- `e` or `export` - Export selected articles

#### Other
- `h` or `help` - Show help
- `q` or `quit` - Exit interactive mode

### Rich Mode Display
```
┌─────────────────────────────────────────────────────────────┐
│          Search Results (Page 1/5)                          │
├──┬──┬───────────────────────────────────────┬──────┬─────────┤
│ #│✓ │Title                                 │Year  │Source   │
├──┼──┼───────────────────────────────────────┼──────┼─────────┤
│ 1│✓ │Machine Learning Applications...      │2024  │PubMed   │
│ 2│  │Neural Networks for Data Science...   │2023  │arXiv    │
│ 3│✓ │Deep Learning in Healthcare...        │2024  │Crossref │
...
└──────────────────────────────────────────────────────────────┘

2 article(s) selected

Commands: [n]ext [p]rev [v]iew [s]elect [e]xport [q]uit [h]elp

>
```

### Simple Mode Display (Fallback)
```
Page 1/5
--------------------------------------------------------------------------------
  1 [✓] Machine Learning Applications in Healthcare          2024  PubMed
  2 [ ] Neural Networks for Data Science Analysis            2023  arXiv
  3 [✓] Deep Learning in Medical Imaging Applications        2024  Crossref
...

2 article(s) selected

Commands: [n]ext [p]rev [v]iew [s]elect [e]xport [q]uit [h]elp

>
```

### Technical Details
- Implementation: `lixplore/utils/interactive_tui.py`
- Rich library detection
- Automatic fallback to simple mode
- Persistent selection across pages
- Export integration with all formats

---

## Complete Flag Reference

### Display Options
| Flag | Description |
|------|-------------|
| `-i, --interactive` | Launch interactive TUI mode |
| `-p, --page N` | View page N of results |
| `--page-size N` | Results per page (default: 20) |
| `--stat` | Show statistics dashboard |
| `--stat-top N` | Top items in stats (default: 10) |

### Export & Output
| Flag | Description |
|------|-------------|
| `--download-pdf` | Download PDFs for results |
| `--pdf-numbers N [N...]` | Download specific PDFs |
| `--use-scihub` | Use SciHub as fallback |
| `--add-to-zotero` | Add to Zotero library |
| `--zotero-collection KEY` | Add to Zotero collection |
| `--export-for-mendeley` | Export RIS for Mendeley |

### Source Selection
| Flag | Description |
|------|-------------|
| `--custom-api NAME` | Search custom API |

### Utility
| Flag | Description |
|------|-------------|
| `--refresh` | Bypass cache |
| `--list-custom-apis` | List custom APIs |
| `--create-api-examples` | Create API config examples |
| `--set-scihub-mirror URL` | Configure SciHub |
| `--show-pdf-dir` | Show PDF directory |
| `--configure-zotero KEY ID` | Configure Zotero |
| `--show-zotero-collections` | List Zotero collections |

---

## Migration Guide

### For Existing Users

All existing commands continue to work exactly as before. New features are purely additive.

### Cache Format Update

Old cache format (array):
```json
[
  {"title": "Article 1", ...},
  {"title": "Article 2", ...}
]
```

New cache format (object with metadata):
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "query": "cancer research",
  "sources": ["pubmed", "crossref"],
  "count": 50,
  "results": [...]
}
```

**Automatic handling**: Tool detects old format and suggests refresh.

---

## Performance Considerations

### Caching
- **7-day cache**: Reduces API calls
- **Instant retrieval**: Cached results load instantly
- **Bandwidth savings**: Significant for large result sets

### Pagination
- **Memory efficient**: Only displays current page
- **Fast navigation**: No re-fetching needed
- **Works with cache**: Cached full results, paginated display

### PDF Downloads
- **Parallel potential**: Can be parallelized (future enhancement)
- **Partial downloads**: Can select specific articles
- **Automatic cleanup**: Failed downloads removed

### Statistics
- **In-memory**: Fast calculation on loaded results
- **No API calls**: Works on existing results
- **Lightweight**: ASCII charts, minimal overhead

---

## Troubleshooting

### Cache Issues
```bash
# Force refresh if cache seems stale
lixplore -P -q "query" --refresh

# Check cache location
ls -lh ~/.lixplore_cache.json
```

### PDF Download Issues
```bash
# Check PDF directory
lixplore --show-pdf-dir

# Verify SciHub configuration
cat ~/.lixplore/scihub_mirror.txt

# Try without SciHub first
lixplore -P -q "open access" -m 5 --download-pdf
```

### Zotero Issues
```bash
# Verify configuration
cat ~/.lixplore/refman_config.json

# List collections
lixplore --show-zotero-collections

# Test with small batch first
lixplore -P -q "test" -m 3 --add-to-zotero
```

### Custom API Issues
```bash
# List configured APIs
lixplore --list-custom-apis

# Check config file
cat ~/.lixplore/apis/springer.json

# Verify API key is set
grep "api_key" ~/.lixplore/apis/springer.json
```

---

## Future Enhancements

Potential future additions (not yet implemented):
- Parallel PDF downloads
- LLM integration (summarization, similarity search)
- More custom API templates
- Advanced filtering options
- Citation network visualization
- Collaboration features

---

## Support & Feedback

For issues, questions, or feature requests:
- GitHub Issues: https://github.com/yourusername/lixplore/issues
- Documentation: `man lixplore` or `lixplore --help`
- Quick examples: `lixplore --examples`

---

**Last Updated**: December 2024
**Version**: 2.0.0
**Compatibility**: Python 3.8+
