# Search Parameter Flags

> **Complete documentation for all search parameter flags in Lixplore**

## Table of Contents

- [Overview](#overview)
- [Query Search](#query-search)
- [Author Search](#author-search)
- [DOI Search](#doi-search)
- [Result Limiting](#result-limiting)
- [Boolean Operators Guide](#boolean-operators-guide)
- [Best Practices](#best-practices)

---

## Overview

Search parameter flags define what to search for and how many results to retrieve. Lixplore supports three types of searches: query search with Boolean operators, author search, and DOI lookup.

**Total Search Flags:** 4

### Search Types
- **Query Search** - Text search with Boolean operators (AND, OR, NOT)
- **Author Search** - Search by author name
- **DOI Search** - Direct DOI lookup
- **Result Limiting** - Control number of results per source

---

## Query Search

### `-q, --query`

**Description:** Search query string with support for Boolean operators and advanced syntax.

**Syntax:**
```bash
lixplore [SOURCE] -q "QUERY" [OPTIONS]
lixplore [SOURCE] --query "QUERY" [OPTIONS]
```

**Type:** String value (required for search)

**Default:** None

**Boolean Operators:**
- `AND` - Both terms must be present
- `OR` - Either term must be present
- `NOT` - Exclude term
- `()` - Group terms for complex queries

#### Examples

**Example 1: Simple Query**
```bash
lixplore -P -q "cancer treatment" -m 20
```
Search for articles containing "cancer treatment" phrase.

**Example 2: AND Operator**
```bash
lixplore -P -q "diabetes AND obesity" -m 30
```
Find articles that mention both diabetes AND obesity.

**Example 3: OR Operator**
```bash
lixplore -P -q "cancer OR tumor" -m 25
```
Find articles mentioning either cancer OR tumor.

**Example 4: NOT Operator**
```bash
lixplore -P -q "diabetes NOT type1" -m 20
```
Find diabetes articles excluding type 1 diabetes.

**Example 5: Complex Query with Parentheses**
```bash
lixplore -P -q "(cancer OR tumor) AND (treatment OR therapy)" -m 40
```
Advanced query: (cancer OR tumor) combined with (treatment OR therapy).

**Example 6: Multi-Source with Boolean**
```bash
lixplore -A -q "COVID-19 AND (vaccine OR treatment)" -m 100 -D --sort newest
```
Search all sources for COVID-19 vaccines or treatments, deduplicate, sort by newest.

**Example 7: Field-Specific Search (PubMed)**
```bash
lixplore -P -q "Smith J[Author] AND cancer[Title]" -m 15
```
PubMed-specific: Author Smith J with cancer in title.

**Example 8: Date-Filtered Query**
```bash
lixplore -P -q "machine learning" -d 2020-01-01 2024-12-31 -m 50
```
Search with date range filter for recent ML papers.

**Example 9: Query with Export**
```bash
lixplore -C -q "quantum computing" -m 30 -X bibtex -o quantum_papers.bib
```
Search and export quantum computing papers to BibTeX.

**Example 10: Multi-Term Complex Query**
```bash
lixplore -P -q "((breast OR ovarian) AND cancer) AND (BRCA1 OR BRCA2)" -m 50
```
Highly specific query for BRCA-related breast/ovarian cancer.

#### Query Syntax Tips

**1. Phrase Matching:**
```bash
# Exact phrase (use quotes in your query string)
lixplore -P -q "machine learning" -m 10

# Individual words
lixplore -P -q "machine OR learning" -m 10
```

**2. Boolean Logic:**
```bash
# AND (both required)
lixplore -P -q "cancer AND treatment" -m 10

# OR (either acceptable)
lixplore -P -q "cancer OR tumor" -m 10

# NOT (exclude)
lixplore -P -q "diabetes NOT type2" -m 10
```

**3. Grouping with Parentheses:**
```bash
# Group related terms
lixplore -P -q "(lung OR breast) AND cancer" -m 10

# Nested groups
lixplore -P -q "((A OR B) AND C) NOT D" -m 10
```

**4. PubMed Field Tags:**
```bash
# Author field
lixplore -P -q "Smith J[Author]" -m 10

# Title field
lixplore -P -q "diabetes[Title]" -m 10

# Title/Abstract
lixplore -P -q "CRISPR[Title/Abstract]" -m 10
```

#### Tips
- Use quotes around entire query: `-q "your query here"`
- Boolean operators must be UPPERCASE (AND, OR, NOT)
- Parentheses allow complex logic
- Field tags work best with PubMed
- Combine with date filters for recent research

#### Warnings
- Complex queries may return fewer results
- Some sources don't support all Boolean operators
- Field tags (e.g., [Author]) are source-specific
- Special characters may need escaping in terminal

#### Related Flags
- [`-d, --date`](filter-flags.md#date) - Date range filter
- [`--sort`](filter-flags.md#sort) - Sort results
- [`-m, --max_results`](#max-results) - Limit results
- [`-S, --select`](export-flags.md#select) - Select subset

---

## Author Search

### `-au, --author`

**Description:** Search for articles by specific author name.

**Syntax:**
```bash
lixplore [SOURCE] -au "AUTHOR NAME" [OPTIONS]
lixplore [SOURCE] --author "AUTHOR NAME" [OPTIONS]
```

**Type:** String value

**Default:** None

**Name Formats:**
- "Smith J" (Last name + Initial)
- "John Smith" (First + Last)
- "Smith, John" (Last, First)
- "Einstein A" (Famous scientists)

#### Examples

**Example 1: Basic Author Search**
```bash
lixplore -P -au "Smith J" -m 15
```
Find articles by author Smith J in PubMed.

**Example 2: Full Name Search**
```bash
lixplore -C -au "John Smith" -m 20
```
Search Crossref for articles by John Smith.

**Example 3: Author with Abstracts**
```bash
lixplore -P -au "Watson JD" -m 10 -a
```
Find Watson's articles and display abstracts.

**Example 4: Author with Date Filter**
```bash
lixplore -P -au "Einstein A" -d 1900-01-01 1955-12-31 -m 25
```
Find Einstein's papers from his lifetime.

**Example 5: Author Export to EndNote**
```bash
lixplore -P -au "Darwin C" -m 30 -X enw -o darwin_papers.enw
```
Export Darwin's work to EndNote format.

**Example 6: Multi-Source Author Search**
```bash
lixplore -A -au "Hawking S" -m 50 -D
```
Find Hawking's papers across all sources, deduplicate.

**Example 7: Author with Sorting**
```bash
lixplore -P -au "Curie M" -m 40 --sort oldest
```
Get Curie's papers sorted chronologically.

**Example 8: Author Statistics**
```bash
lixplore -P -au "Feynman R" -m 100 --stat
```
Analyze Feynman's publication patterns.

**Example 9: Recent Author Publications**
```bash
lixplore -x -au "LeCun Y" -m 20 --sort newest
```
Get Yann LeCun's latest arXiv preprints.

**Example 10: Author Co-Publication Analysis**
```bash
lixplore -P -au "Watson JD" -m 50 --stat --stat-top 20
```
Analyze Watson's collaborations (top 20 co-authors).

#### Author Name Format Tips

**PubMed Format:**
```bash
# Last name + First initial
lixplore -P -au "Smith J" -m 10

# Full last name + Full first name
lixplore -P -au "Smith John" -m 10

# Formal format
lixplore -P -au "Smith, John" -m 10
```

**Crossref/Other Sources:**
```bash
# First + Last (more common)
lixplore -C -au "John Smith" -m 10
```

**Handling Common Names:**
```bash
# Add date filter to narrow results
lixplore -P -au "Smith J" -d 2015-01-01 2024-12-31 -m 20

# Use query instead for more specificity
lixplore -P -q "Smith J[Author] AND genetics[Title]" -m 10
```

#### Tips
- Try multiple name formats if no results
- Use initials for PubMed (more reliable)
- Combine with date filter for recent work
- Some sources better support author search than others
- Statistics flag useful for author publication analysis

#### Warnings
- Common names may return many irrelevant results
- Name format varies by source (try both formats)
- Some databases may not support author search
- Middle initials often not indexed

#### Related Flags
- [`-q, --query`](#query) - Alternative with author field tags
- [`-d, --date`](filter-flags.md#date) - Filter by publication date
- [`--sort`](filter-flags.md#sort) - Sort chronologically
- [`--stat`](display-flags.md#stat) - Author statistics

---

## DOI Search

### `-DOI, --doi`

**Description:** Search for a specific article by its Digital Object Identifier (DOI).

**Syntax:**
```bash
lixplore [SOURCE] -DOI "DOI STRING" [OPTIONS]
lixplore [SOURCE] --doi "DOI STRING" [OPTIONS]
```

**Type:** String value

**Default:** None

**DOI Format:** `10.XXXX/YYYYY`

#### Examples

**Example 1: Basic DOI Lookup**
```bash
lixplore -C -DOI "10.1038/nature12345"
```
Retrieve article metadata using DOI from Crossref.

**Example 2: DOI with Details**
```bash
lixplore -C -DOI "10.1126/science.1234567" -N 1
```
Get full article details for DOI.

**Example 3: DOI Export to BibTeX**
```bash
lixplore -C -DOI "10.1038/nature12345" -X bibtex
```
Get BibTeX citation for specific DOI.

**Example 4: DOI Export to EndNote**
```bash
lixplore -C -DOI "10.1126/science.1234567" -X enw
```
Export DOI article to EndNote format.

**Example 5: Multiple DOIs (using multiple commands)**
```bash
lixplore -C -DOI "10.1038/nature12345" -X csv -o results.csv
lixplore -C -DOI "10.1126/science.1234567" -X csv -o results.csv
```
Look up multiple DOIs (append mode).

**Example 6: DOI with Enrichment**
```bash
lixplore -C -DOI "10.1038/nature12345" --enrich crossref
```
Get enriched metadata for DOI.

**Example 7: DOI PDF Download**
```bash
lixplore -C -DOI "10.1371/journal.pone.0123456" --download-pdf
```
Download PDF for open access DOI (e.g., PLOS).

**Example 8: DOI to Zotero**
```bash
lixplore -C -DOI "10.1038/nature12345" --add-to-zotero
```
Add DOI article directly to Zotero library.

**Example 9: DOI Citation Format**
```bash
lixplore -C -DOI "10.1038/nature12345" -c apa
```
Get APA-formatted citation for DOI.

**Example 10: DOI with Annotation**
```bash
lixplore -C -DOI "10.1038/nature12345"
lixplore --annotate 1 --rating 5 --tags "important,methodology"
```
Look up and annotate a specific DOI article.

#### DOI Format Examples

**Valid DOI Formats:**
```bash
# Standard format
10.1038/nature12345

# With URL prefix (works too)
https://doi.org/10.1038/nature12345

# arXiv DOI
10.48550/arXiv.2103.14030

# PubMed Central DOI
10.1371/journal.pone.0123456
```

#### Tips
- Crossref is best source for DOI lookup
- DOI lookup is extremely fast (single record)
- Most reliable way to get specific article
- Automatically validates DOI format
- Great for citation management

#### Warnings
- DOI must exist in database
- Some very old articles may not have DOIs
- Invalid DOI format will return no results
- Not all sources support DOI search equally well

#### Related Flags
- [`--enrich`](filter-flags.md#enrich) - Get complete metadata
- [`-X, --export`](export-flags.md#export) - Export citation
- [`-c, --citations`](export-flags.md#citations) - Formatted citations
- [`--add-to-zotero`](export-flags.md#add-to-zotero) - Import to Zotero

---

## Result Limiting

### `-m, --max_results`

**Description:** Maximum number of results to retrieve per source.

**Syntax:**
```bash
lixplore [SOURCE] -q "QUERY" -m NUMBER [OPTIONS]
lixplore [SOURCE] -q "QUERY" --max_results NUMBER [OPTIONS]
```

**Type:** Integer value

**Default:** 10

**Range:** 1-1000 (recommended: 10-200)

#### Examples

**Example 1: Small Sample**
```bash
lixplore -P -q "cancer" -m 5
```
Quick preview with just 5 results.

**Example 2: Medium Search**
```bash
lixplore -P -q "diabetes" -m 50
```
Comprehensive search with 50 results.

**Example 3: Large Literature Review**
```bash
lixplore -A -q "machine learning" -m 200 -D
```
Extensive search across all sources (200 per source).

**Example 4: Pagination Example**
```bash
lixplore -P -q "COVID-19" -m 100 -p 1 --page-size 20
```
Retrieve 100 results, display 20 per page.

**Example 5: Export Top Results**
```bash
lixplore -P -q "genetics" -m 100 --sort newest -S first:20 -X xlsx
```
Get 100 results, sort, export top 20.

**Example 6: Statistics on Large Set**
```bash
lixplore -A -q "climate change" -m 500 -D --stat
```
Analyze 500 articles per source for comprehensive statistics.

**Example 7: Author Publication Count**
```bash
lixplore -P -au "Smith J" -m 200 --stat
```
Get all author publications for analysis.

**Example 8: Multi-Source Balanced**
```bash
lixplore -s PCE -q "neuroscience" -m 30 -D
```
30 results per source (90 total before dedup).

**Example 9: Selective Export**
```bash
lixplore -P -q "immunology" -m 100 -S odd -X csv
```
Retrieve 100, export every other one (50 articles).

**Example 10: Performance Optimization**
```bash
lixplore -P -q "quick check" -m 3
```
Ultra-fast search for quick verification.

#### Result Limiting Tips

**Performance vs Coverage:**
```bash
# Fast (single source, few results)
lixplore -P -q "query" -m 10

# Balanced
lixplore -s PC -q "query" -m 50 -D

# Comprehensive (slow)
lixplore -A -q "query" -m 200 -D
```

**Per-Source Behavior:**
```bash
# With -A flag: 50 results PER source
lixplore -A -q "query" -m 50
# Total: up to 250 results (5 sources × 50)

# After deduplication:
lixplore -A -q "query" -m 50 -D
# Total: ~150-200 (depends on overlap)
```

**Pagination Strategy:**
```bash
# Instead of loading all at once
lixplore -P -q "query" -m 500

# Use pagination
lixplore -P -q "query" -m 500 -p 1 --page-size 50
lixplore -P -q "query" -m 500 -p 2 --page-size 50
```

#### Tips
- Start small (10-20) for exploratory searches
- Use 50-100 for literature reviews
- Use 200+ for comprehensive analysis
- Results are cached (can review later)
- Combine with selection for subset export

#### Warnings
- Higher limits = slower search
- API rate limits may apply
- Very large results may cause memory issues
- Some sources have maximum limits

#### Related Flags
- [`-S, --select`](export-flags.md#select) - Export subset
- [`--sort`](filter-flags.md#sort) - Organize before selection
- [`-p, --page`](display-flags.md#page) - Pagination
- [`--page-size`](display-flags.md#page-size) - Results per page

---

## Boolean Operators Guide

### Operator Reference

| Operator | Symbol | Purpose | Example |
|----------|--------|---------|---------|
| **AND** | `AND` | Both terms required | `cancer AND treatment` |
| **OR** | `OR` | Either term accepted | `cancer OR tumor` |
| **NOT** | `NOT` | Exclude term | `diabetes NOT type1` |
| **Grouping** | `()` | Group operations | `(A OR B) AND C` |

### Logic Examples

**1. Simple AND:**
```bash
lixplore -P -q "diabetes AND obesity" -m 20
```
Articles must mention BOTH diabetes and obesity.

**2. Simple OR:**
```bash
lixplore -P -q "cancer OR tumor" -m 20
```
Articles can mention cancer, tumor, or both.

**3. Simple NOT:**
```bash
lixplore -P -q "diabetes NOT type1" -m 20
```
Articles about diabetes but NOT type 1.

**4. AND + OR:**
```bash
lixplore -P -q "cancer AND (treatment OR therapy)" -m 20
```
Cancer articles that mention treatment OR therapy.

**5. Complex Nested:**
```bash
lixplore -P -q "((lung OR breast) AND cancer) NOT metastatic" -m 30
```
Lung or breast cancer articles, excluding metastatic.

**6. Multiple AND:**
```bash
lixplore -P -q "COVID-19 AND vaccine AND efficacy" -m 20
```
All three terms must be present.

**7. Multiple OR:**
```bash
lixplore -P -q "cancer OR tumor OR neoplasm OR malignancy" -m 30
```
Any of these synonyms acceptable.

### Truth Tables

**AND Operator:**
| Term A | Term B | Result |
|--------|--------|--------|
| Present | Present | ✓ Match |
| Present | Absent | ✗ No match |
| Absent | Present | ✗ No match |
| Absent | Absent | ✗ No match |

**OR Operator:**
| Term A | Term B | Result |
|--------|--------|--------|
| Present | Present | ✓ Match |
| Present | Absent | ✓ Match |
| Absent | Present | ✓ Match |
| Absent | Absent | ✗ No match |

**NOT Operator:**
| Term A | NOT Term B | Result |
|--------|------------|--------|
| Present | Present | ✗ No match |
| Present | Absent | ✓ Match |
| Absent | Present | ✗ No match |
| Absent | Absent | ✗ No match |

---

## Best Practices

### 1. Start Broad, Then Refine

```bash
# Step 1: Broad search
lixplore -P -q "cancer" -m 10

# Step 2: Add specificity
lixplore -P -q "breast cancer" -m 20

# Step 3: Add more terms
lixplore -P -q "breast cancer AND treatment" -m 30
```

### 2. Use Boolean Operators for Precision

```bash
# Less precise (phrase search)
lixplore -P -q "cancer treatment" -m 20

# More precise (both terms required)
lixplore -P -q "cancer AND treatment" -m 20

# Most precise (specific combination)
lixplore -P -q "(breast OR ovarian) AND cancer AND BRCA1" -m 30
```

### 3. Combine Search Types

```bash
# Query search for broad results
lixplore -P -q "genetics" -m 50

# Author search for specific researcher
lixplore -P -au "Watson JD" -m 30

# DOI for specific article
lixplore -C -DOI "10.1038/nature12345"
```

### 4. Use Appropriate Result Limits

```bash
# Quick check (5-10)
lixplore -P -q "test query" -m 5

# Standard search (20-50)
lixplore -P -q "research topic" -m 30

# Literature review (100-200)
lixplore -A -q "comprehensive topic" -m 150 -D

# Statistical analysis (200+)
lixplore -A -q "analysis topic" -m 300 -D --stat
```

### 5. Leverage Date Filters

```bash
# Recent research only
lixplore -P -q "COVID-19" -d 2020-01-01 2024-12-31 -m 50

# Historical perspective
lixplore -P -q "genetics" -d 1950-01-01 1970-12-31 -m 30 --sort oldest
```

---

## Troubleshooting

### Problem: No results found

**Solution 1: Simplify query**
```bash
# Instead of complex query
lixplore -P -q "((A AND B) OR C) NOT D" -m 20

# Try simpler
lixplore -P -q "A OR B" -m 20
```

**Solution 2: Remove Boolean operators**
```bash
# Instead of
lixplore -P -q "cancer AND treatment" -m 20

# Try
lixplore -P -q "cancer treatment" -m 20
```

**Solution 3: Try different source**
```bash
# If PubMed returns nothing
lixplore -P -q "query" -m 20

# Try Crossref or all sources
lixplore -A -q "query" -m 20
```

### Problem: Too many irrelevant results

**Solution: Add more specific terms**
```bash
# Too broad
lixplore -P -q "cancer" -m 100

# More specific
lixplore -P -q "breast cancer AND BRCA1 AND treatment" -m 50
```

### Problem: Author search returns wrong person

**Solution: Add date filter or query combination**
```bash
# Generic author search
lixplore -P -au "Smith J" -m 50

# With date filter
lixplore -P -au "Smith J" -d 2015-01-01 2024-12-31 -m 30

# With topic filter (use query instead)
lixplore -P -q "Smith J[Author] AND genetics[Title]" -m 20
```

---

## Related Documentation

- [Source Flags](source-flags.md) - Choose databases to search
- [Filter Flags](filter-flags.md) - Process search results
- [Display Flags](display-flags.md) - View and browse results
- [Export Flags](export-flags.md) - Export and save results

---

**Last Updated:** 2024-12-28
**Lixplore Version:** 2.0+
