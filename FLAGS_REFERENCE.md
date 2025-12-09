# Lixplore CLI - Command Line Flags Reference

## Source Selection Flags

### Combined Source Selection (NEW)

| Short | Long | Description |
|-------|------|-------------|
| `-s` | `--sources` | Combined source selection using letters (e.g., `PX` for PubMed+arXiv) |

**Letter Codes:**
- `P` = PubMed
- `C` = Crossref
- `J` = DOAJ
- `E` = EuropePMC
- `X` = arXiv
- `A` = All sources

**Examples:**
- `lixplore -s PX -q "search term"` - Search PubMed and arXiv
- `lixplore -s PCE -q "search term"` - Search PubMed, Crossref, and EuropePMC
- `lixplore -s A -q "search term"` - Search all sources

### Individual Source Flags (Legacy)

| Short | Long | Description |
|-------|------|-------------|
| `-P` | `--pubmed` | Search PubMed |
| `-C` | `--crossref` | Search Crossref |
| `-J` | `--doaj` | Search DOAJ (Directory of Open Access Journals) |
| `-E` | `--europepmc` | Search EuropePMC |
| `-X` | `--arxiv` | Search arXiv |
| `-A` | `--all` | Search across all sources (PubMed, Crossref, DOAJ, EuropePMC, arXiv) |

**Note:** You can still use individual flags combined (e.g., `-P -C -E`) for backward compatibility

## Search Query Flags

| Short | Long | Description |
|-------|------|-------------|
| `-q` | `--query` | Query string to search |
| `-au` | `--author` | Search articles by author name |
| `-DOI` | `--doi` | Search article by DOI |

**Note:** You must provide one of these search parameters (-q, -au, or -DOI)

## Filter & Display Flags

| Short | Long | Description | Default |
|-------|------|-------------|---------|
| `-d` | `--date` | Filter with date range (FROM TO in YYYY-MM-DD format) | None |
| `-a` | `--abstract` | Show abstracts of results | False |
| `-m` | `--max_results` | Maximum number of results to fetch | 10 |
| `-N` | `--number` | Select article number(s) for detailed view (1-based index) | None |

## Post-Processing Flags

| Short | Long | Description |
|-------|------|-------------|
| `-D` | `--deduplicate` | Remove duplicate results using multi-level matching |
| `-Z` | `--zotero` | Export results to Zotero |
| `-H` | `--history` | Show search history |

### Deduplication Strategy

The `-D/--deduplicate` flag uses a sophisticated three-level matching approach:

1. **Primary (DOI Matching)**: If both articles have DOIs, they are compared directly. This is the most reliable method.

2. **Secondary (Title Similarity)**: For articles without DOIs, titles are compared using fuzzy matching (85% similarity threshold). If titles match:
   - Articles with author information require at least 1 common author
   - Articles without author information are deduplicated based on title alone

3. **Tertiary (Author Matching)**: For articles with slightly different titles (e.g., preprint vs. published version):
   - Requires significant author overlap (minimum 3 common authors)
   - Requires titles to be at least 70% similar
   - Handles various author name formats (e.g., "Smith J", "J Smith", "Smith, John")

This approach effectively catches:
- Exact duplicates (same article indexed in multiple databases)
- Preprint vs. published versions
- Articles with minor title variations
- Cross-database duplicates with different metadata formats

## Statistics Flag

| Short | Long | Description | Default |
|-------|------|-------------|---------|
| `-st` | `--stat` | Getting statistics for count of selected parameter | 50 |

---

## Usage Examples

### Basic Search
```bash
# Search PubMed for "machine learning" (new syntax)
lixplore -s P -q "machine learning"

# Search all sources for "CRISPR" (new syntax)
lixplore -s A -q "CRISPR"

# Old syntax still works
lixplore -P -q "machine learning"
lixplore -A -q "CRISPR"
```

### Multi-Source Search
```bash
# Search PubMed, Crossref, and EuropePMC (new syntax)
lixplore -s PCE -q "cancer immunotherapy" -m 20

# Search PubMed and arXiv (new syntax)
lixplore -s PX -q "quantum computing" -m 15

# Old syntax still works
lixplore -P -C -E -q "cancer immunotherapy" -m 20
```

### Author Search
```bash
# Search for articles by author
lixplore -P -au "Smith J" -m 15
```

### DOI Lookup
```bash
# Fetch article by DOI
lixplore -C -DOI "10.1038/nature12345"
```

### Advanced Filtering
```bash
# Search with date range and abstracts (new syntax)
lixplore -s P -q "COVID-19" -d 2020-01-01 2023-12-31 -a -m 50

# Old syntax
lixplore -P -q "COVID-19" -d 2020-01-01 2023-12-31 -a -m 50
```

### Deduplication and Export
```bash
# Search multiple sources, deduplicate, and export to Zotero (new syntax)
lixplore -s A -q "quantum computing" -D -Z -m 30

# Or combine specific sources
lixplore -s PCJE -q "quantum computing" -D -Z -m 30

# Old syntax
lixplore -A -q "quantum computing" -D -Z -m 30
```

### Detailed View
```bash
# Get detailed information for specific results
lixplore -P -q "neural networks" -N 1 3 5
```

### View History
```bash
# Show search history
lixplore -H
```

---

## Configuration

The tool uses `config.json` for API configuration:
- **PubMed**: Requires email, optional API key for higher rate limits
- **Crossref**: Requires mailto email address
