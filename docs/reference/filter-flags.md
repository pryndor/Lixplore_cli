# Filtering & Processing Flags

> **Complete documentation for filtering and result processing flags**

## Table of Contents

- [Overview](#overview)
- [Date Filtering](#date-filtering)
- [Deduplication](#deduplication)
- [Sorting](#sorting)
- [Metadata Enrichment](#metadata-enrichment)
- [Best Practices](#best-practices)

---

## Overview

Filtering and processing flags allow you to refine, organize, and enhance search results after retrieval.

**Total Filter Flags:** 7

### Categories
- **Date Filtering** - Filter by publication date range
- **Deduplication** - Remove duplicate articles (5 strategies)
- **Sorting** - Order results (5 methods)
- **Enrichment** - Enhance metadata from external APIs

---

## Date Filtering

### `-d, --date`

**Description:** Filter results by publication date range.

**Syntax:**
```bash
lixplore [SOURCE] -q "QUERY" -d FROM_DATE TO_DATE [OPTIONS]
lixplore [SOURCE] -q "QUERY" --date FROM_DATE TO_DATE [OPTIONS]
```

**Type:** Two date values (FROM TO)

**Format:** YYYY-MM-DD

**Default:** No date filter

#### Examples

**Example 1: Recent Publications (Last 5 Years)**
```bash
lixplore -P -q "COVID-19" -d 2020-01-01 2024-12-31 -m 50
```

**Example 2: Historical Research**
```bash
lixplore -P -q "genetics" -d 1950-01-01 1970-12-31 -m 30 --sort oldest
```

**Example 3: Current Year Only**
```bash
lixplore -P -q "artificial intelligence" -d 2024-01-01 2024-12-31 -m 40
```

**Example 4: Decade Analysis**
```bash
lixplore -A -q "climate change" -d 2010-01-01 2019-12-31 -m 100 -D --stat
```

**Example 5: Pre-COVID Research**
```bash
lixplore -P -q "coronavirus" -d 2000-01-01 2019-12-31 -m 25
```

#### Tips
- Always use YYYY-MM-DD format
- Combine with `--sort newest` for latest-first order
- Use statistics flag to analyze publication trends
- Works best with PubMed and Crossref
- Date filtering happens after API retrieval (client-side)

#### Warnings
- Not all sources support date filtering equally
- Some older articles may lack proper date metadata
- Preprints (arXiv) may use submission date vs publication date
- DOAJ may have indexing delays

#### Related Flags
- [`--sort`](#sort) - Sort by date
- [`--stat`](display-flags.md#stat) - Publication trend analysis
- [`-m, --max_results`](search-flags.md#max-results) - Limit results

---

## Deduplication

### `-D, --deduplicate`

**Description:** Remove duplicate articles from multi-source searches using advanced matching algorithms.

**Syntax:**
```bash
lixplore [SOURCES] -q "QUERY" -D [STRATEGY] [OPTIONS]
lixplore [SOURCES] -q "QUERY" --deduplicate [STRATEGY] [OPTIONS]
```

**Type:** Optional string value

**Strategies:**
- `auto` (default) - Multi-level matching (DOI + title + author)
- `doi_only` - Match only by DOI
- `title_only` - Match only by title similarity
- `strict` - High similarity threshold (0.95)
- `loose` - Low similarity threshold (0.75)

**Default:** `auto` (when used without value)

#### Examples

**Example 1: Auto Deduplication (Recommended)**
```bash
lixplore -A -q "machine learning" -m 50 -D
```
Search all sources and remove duplicates automatically.

**Example 2: Strict Deduplication**
```bash
lixplore -s PCE -q "cancer" -m 100 -D strict
```
Very conservative matching (high threshold).

**Example 3: Loose Deduplication**
```bash
lixplore -A -q "COVID-19" -m 200 -D loose
```
Aggressive duplicate removal (catches more variants).

**Example 4: DOI-Only Matching**
```bash
lixplore -s PC -q "genetics" -m 80 -D doi_only
```
Only match articles with same DOI.

**Example 5: Title-Only Matching**
```bash
lixplore -A -q "neuroscience" -m 60 -D title_only
```
Match by title similarity only.

#### Advanced Deduplication Options

### `--dedup-threshold`

**Description:** Set title similarity threshold for deduplication.

**Syntax:**
```bash
lixplore -A -q "QUERY" -D --dedup-threshold FLOAT
```

**Type:** Float (0.0-1.0)

**Default:** 0.85

**Example:**
```bash
lixplore -A -q "cancer" -m 100 -D --dedup-threshold 0.9
```
Higher threshold = stricter matching (fewer false duplicates).

### `--dedup-keep`

**Description:** Choose which duplicate to keep when matches found.

**Syntax:**
```bash
lixplore -A -q "QUERY" -D --dedup-keep STRATEGY
```

**Type:** String choice

**Options:**
- `first` - Keep first occurrence (chronological order)
- `most_complete` - Keep entry with most metadata (default)
- `prefer_doi` - Prefer entries with DOI

**Example:**
```bash
lixplore -A -q "diabetes" -m 80 -D --dedup-keep prefer_doi
```
Keep DOI versions when duplicates found.

### `--dedup-merge`

**Description:** Merge metadata from duplicates instead of discarding.

**Syntax:**
```bash
lixplore -A -q "QUERY" -D --dedup-merge
```

**Type:** Boolean flag

**Example:**
```bash
lixplore -A -q "genetics" -m 100 -D --dedup-merge
```
Combine best metadata from all duplicate entries.

#### Deduplication Algorithms

**1. DOI Matching (Most Reliable):**
- Exact string match of DOI
- Normalized (lowercase, whitespace removed)
- If DOIs match → Duplicate confirmed

**2. Title Similarity:**
- SequenceMatcher algorithm
- Normalized strings (lowercase, extra spaces removed)
- Threshold comparison (default 0.85)
- Score ≥ threshold → Likely duplicate

**3. Author Matching:**
- Normalize author names (handle various formats)
- Count common authors
- Min 2 common authors → Confirmed
- Used as secondary validation for title matches

**4. Combined (Auto Strategy):**
```
IF both_have_doi:
    return doi_match()
ELSE IF titles_similar(threshold):
    IF have_author_data:
        return authors_match()
    ELSE:
        return True
ELSE IF many_authors_match AND titles_somewhat_similar(0.7):
    return True
ELSE:
    return False
```

#### Tips
- **ALWAYS use `-D`** when searching multiple sources
- `auto` strategy works well for most cases
- Use `strict` for important bibliographies
- Use `loose` when expecting many variants
- `--dedup-merge` provides most complete metadata
- Check deduplication stats in output

#### Warnings
- Deduplication is not perfect (may miss variants)
- Very different titles for same article may not match
- Author name variations can cause misses
- Processing time increases with result count
- Some false positives/negatives possible

#### Related Flags
- [`-A, --all`](source-flags.md#all) - Search all sources (needs dedup)
- [`-s, --sources`](source-flags.md#sources) - Multi-source search
- [`--enrich`](#enrich) - Fill missing metadata
- [`--sort`](#sort) - Organize results

---

## Sorting

### `--sort`

**Description:** Sort results by various criteria.

**Syntax:**
```bash
lixplore [SOURCE] -q "QUERY" --sort ORDER [OPTIONS]
```

**Type:** String choice

**Options:**
- `relevant` - Default API order (most relevant first)
- `newest` - Latest publications first (desc by year)
- `oldest` - Earliest publications first (asc by year)
- `journal` - Alphabetical by journal name
- `author` - Alphabetical by first author last name

**Default:** `relevant` (original API order)

#### Examples

**Example 1: Latest Research First**
```bash
lixplore -P -q "COVID-19" -m 100 --sort newest
```
Get most recent COVID-19 research.

**Example 2: Historical Perspective**
```bash
lixplore -P -q "genetics" -m 80 --sort oldest
```
Chronological order from earliest publications.

**Example 3: Journal Alphabetical**
```bash
lixplore -A -q "cancer" -m 150 -D --sort journal
```
Organize by journal name (A-Z).

**Example 4: Author Alphabetical**
```bash
lixplore -P -q "immunology" -m 60 --sort author
```
Organize by first author's last name.

**Example 5: Sort + Select + Export**
```bash
lixplore -A -q "machine learning" -m 200 -D --sort newest -S first:30 -X xlsx
```
Get latest 30 ML papers across all sources.

**Example 6: Sort for Statistics**
```bash
lixplore -P -q "neuroscience" -m 300 --sort newest --stat
```
Analyze recent publication trends.

**Example 7: Historical Analysis**
```bash
lixplore -P -q "quantum physics" -m 100 --sort oldest -S first:20
```
Get earliest 20 quantum physics papers.

**Example 8: Journal-Based Export**
```bash
lixplore -C -q "cardiology" -m 120 --sort journal -X csv
```
Export cardiology papers organized by journal.

**Example 9: Author Bibliography**
```bash
lixplore -P -au "Einstein A" -m 50 --sort oldest
```
Einstein's papers in chronological order.

**Example 10: Multi-Sort Workflow**
```bash
# Get latest papers
lixplore -P -q "CRISPR" -m 100 --sort newest -S first:20 -X xlsx -o latest_crispr.xlsx

# Get earliest papers
lixplore -P -q "CRISPR" -m 100 --sort oldest -S first:20 -X xlsx -o early_crispr.xlsx
```

#### Sorting Behavior

**By Year (newest/oldest):**
- Uses publication year field
- Missing years sorted to end
- Same year → maintains original order

**By Journal:**
- Alphabetical case-insensitive
- Missing journal → sorted to end
- Exact string match (not normalized)

**By Author:**
- Uses first author's last name
- Extracts last word as surname
- Missing authors → sorted to end
- Case-insensitive

**Relevant (Default):**
- Preserves API ranking
- Usually by relevance score
- Source-dependent algorithm

#### Tips
- Use `newest` for current research trends
- Use `oldest` for historical studies
- Combine with `-S first:N` to get top N after sorting
- Journal sort useful for journal-specific analysis
- Author sort good for alphabetical bibliographies
- Sorting happens client-side (after retrieval)

#### Warnings
- Some articles may lack year metadata
- Journal names not normalized (variants exist)
- Author extraction may fail for unusual formats
- Sorting large result sets can be slow
- Original relevance lost with custom sort

#### Related Flags
- [`-S, --select`](export-flags.md#select) - Select subset after sorting
- [`--stat`](display-flags.md#stat) - Analyze sorted trends
- [`-d, --date`](#date) - Filter before sorting
- [`-D, --deduplicate`](#deduplicate) - Dedupe before sorting

---

## Metadata Enrichment

### `--enrich`

**Description:** Enrich article metadata by querying external APIs for missing or additional information.

**Syntax:**
```bash
lixplore [SOURCE] -q "QUERY" --enrich [API...] [OPTIONS]
```

**Type:** Optional list of API names

**APIs:**
- `crossref` - Crossref API enrichment
- `pubmed` - PubMed API enrichment
- `arxiv` - arXiv API enrichment
- `all` - All available APIs (default if no args)

**Default:** `all` (when used without value)

#### Examples

**Example 1: Enrich from All APIs**
```bash
lixplore -P -q "cancer" -m 30 --enrich
```
Enrich metadata from all available sources.

**Example 2: Crossref Only**
```bash
lixplore -P -q "genetics" -m 50 --enrich crossref
```
Add DOI and citation data from Crossref.

**Example 3: PubMed Only**
```bash
lixplore -C -q "immunology" -m 40 --enrich pubmed
```
Add PubMed IDs and abstracts.

**Example 4: Multiple APIs**
```bash
lixplore -J -q "open access" -m 25 --enrich crossref pubmed
```
Enrich from Crossref and PubMed.

**Example 5: Enrich Before Export**
```bash
lixplore -A -q "neuroscience" -m 100 -D --enrich -X bibtex
```
Complete metadata before exporting citations.

**Example 6: Enrich + Statistics**
```bash
lixplore -P -q "COVID-19" -m 200 --enrich --stat
```
Enrich data for better statistics accuracy.

**Example 7: arXiv Enrichment**
```bash
lixplore -C -q "machine learning" -m 50 --enrich arxiv
```
Add arXiv links and preprint data.

#### What Gets Enriched

**Crossref Enrichment:**
- DOI validation and links
- Journal information (name, volume, issue, pages)
- Publication dates
- Publisher information
- Citation counts
- ISSN/ISBN
- License information

**PubMed Enrichment:**
- PubMed ID (PMID)
- PubMed Central ID (PMCID)
- Abstracts (if missing)
- MeSH terms
- Article types
- Grant information
- Author affiliations

**arXiv Enrichment:**
- arXiv ID
- Preprint links
- Categories
- PDF links
- Submission dates
- Updated versions

#### Enrichment Process

**1. DOI Discovery:**
```
For each article:
    IF no DOI:
        Query Crossref by title + author
        IF found → Add DOI
```

**2. Metadata Completion:**
```
For each article:
    For each enrichment API:
        IF has_identifier(doi/pmid/arxiv_id):
            Query API
            Merge results (keep best data)
```

**3. Field Priority:**
```
IF multiple_sources_have_field:
    Priority: PubMed > Crossref > arXiv > Original
    (Most reliable source wins)
```

#### Tips
- Use enrichment for incomplete search results
- Crossref best for DOI and citation data
- PubMed best for biomedical metadata
- Increases export quality (especially BibTeX)
- Adds 2-5 seconds per 10 articles
- Progress shown during enrichment

#### Warnings
- Slower search (additional API calls)
- API rate limits may apply
- Not all articles can be enriched
- Some APIs require internet connection
- May not find matches for very obscure articles
- Crossref rate limit: 50 requests/second

#### Related Flags
- [`-X, --export`](export-flags.md#export) - Export enriched data
- [`-D, --deduplicate`](#deduplicate) - Use before enrichment
- [`--stat`](display-flags.md#stat) - Statistics on enriched data

---

## Best Practices

### 1. Always Deduplicate Multi-Source Searches

```bash
# CORRECT
lixplore -A -q "query" -m 50 -D

# INCORRECT (will have many duplicates)
lixplore -A -q "query" -m 50
```

### 2. Combine Date + Sort + Select

```bash
# Get latest 20 papers from last 5 years
lixplore -P -q "CRISPR" -d 2020-01-01 2024-12-31 -m 100 --sort newest -S first:20 -X xlsx
```

### 3. Enrich Before Export

```bash
# Better export quality
lixplore -A -q "genetics" -m 50 -D --enrich -X bibtex
```

### 4. Use Appropriate Dedup Strategy

```bash
# For final bibliography (strict)
lixplore -A -q "query" -m 100 -D strict --dedup-keep most_complete

# For discovery (loose)
lixplore -A -q "query" -m 200 -D loose
```

### 5. Filter → Deduplicate → Sort → Select → Export

```bash
lixplore -A -q "machine learning" \
  -d 2020-01-01 2024-12-31 \  # 1. Filter by date
  -m 200 \                      # 2. Get results
  -D \                          # 3. Deduplicate
  --sort newest \               # 4. Sort
  -S first:50 \                 # 5. Select top 50
  -X xlsx                       # 6. Export
```

---

## Troubleshooting

### Problem: Too many duplicates remain

**Solution: Use stricter deduplication**
```bash
lixplore -A -q "query" -m 100 -D strict --dedup-threshold 0.9
```

### Problem: Missing some article variants

**Solution: Use looser deduplication**
```bash
lixplore -A -q "query" -m 100 -D loose --dedup-threshold 0.75
```

### Problem: Date filter not working

**Solution: Check date format and source compatibility**
```bash
# Correct format
lixplore -P -q "query" -d 2020-01-01 2024-12-31 -m 50

# Wrong format
lixplore -P -q "query" -d 2020 2024 -m 50  # Won't work
```

### Problem: Enrichment too slow

**Solution: Limit APIs or skip enrichment**
```bash
# Just Crossref (faster)
lixplore -P -q "query" -m 50 --enrich crossref

# Skip enrichment for speed
lixplore -P -q "query" -m 50
```

---

## Related Documentation

- [Source Flags](source-flags.md) - Multi-source searching
- [Search Flags](search-flags.md) - Query construction
- [Display Flags](display-flags.md) - View results
- [Export Flags](export-flags.md) - Export processed results

---

**Last Updated:** 2024-12-28
**Lixplore Version:** 2.0+
