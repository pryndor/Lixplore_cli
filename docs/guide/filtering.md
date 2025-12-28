# Filtering and Deduplication Guide

> **Master guide for filtering, deduplicating, and processing search results**

## Table of Contents

- [Date Filtering](#date-filtering)
- [Deduplication Strategies](#deduplication-strategies)
- [Result Sorting](#result-sorting)
- [Selection Patterns](#selection-patterns)
- [Complete Workflows](#complete-workflows)

---

## Date Filtering

### Basic Usage
```bash
lixplore -P -q "COVID-19" -d 2020-01-01 2024-12-31 -m 50
```

### Common Date Ranges

**Last Year:**
```bash
lixplore -P -q "query" -d 2024-01-01 2024-12-31 -m 50
```

**Last 5 Years:**
```bash
lixplore -P -q "query" -d 2020-01-01 2024-12-31 -m 100
```

**Historical Period:**
```bash
lixplore -P -q "genetics" -d 1950-01-01 1970-12-31 -m 50 --sort oldest
```

**Current Month:**
```bash
lixplore -P -q "latest research" -d 2024-12-01 2024-12-31 -m 20 --sort newest
```

### Best Practices

1. **Always use YYYY-MM-DD format**
2. **Combine with sorting** for better organization
3. **Use statistics** to analyze trends
4. **Remember:** Date filtering is client-side (fetches then filters)

---

## Deduplication Strategies

### Why Deduplicate?

Multi-source searches often return the same article multiple times:
- Same article indexed in PubMed and Crossref
- Preprint in arXiv, published version in journal
- Different metadata completeness

### Strategy Overview

| Strategy | Threshold | Use Case |
|----------|-----------|----------|
| `auto` | 0.85 | Balanced (recommended) |
| `strict` | 0.95 | Final bibliography |
| `loose` | 0.75 | Discovery, variant detection |
| `doi_only` | Exact | DOI-based only |
| `title_only` | 0.85 | When DOI unavailable |

### Auto Strategy (Recommended)

```bash
lixplore -A -q "query" -m 100 -D
```

**How it works:**
1. Match by DOI (if both have DOI)
2. Match by title similarity (≥0.85)
3. Verify with author overlap
4. Keep most complete metadata

### Strict Strategy (High Precision)

```bash
lixplore -A -q "systematic review topic" -m 200 -D strict
```

**Best for:**
- Final bibliographies
- Publication-ready references
- When false duplicates are costly

### Loose Strategy (High Recall)

```bash
lixplore -A -q "exploratory topic" -m 300 -D loose
```

**Best for:**
- Initial discovery
- Catching all variants
- Preliminary screening

### DOI-Only Strategy

```bash
lixplore -s PC -q "query" -m 100 -D doi_only
```

**Best for:**
- When metadata is unreliable
- High-quality journal articles
- Crossref + PubMed combinations

### Advanced Options

**Custom Threshold:**
```bash
lixplore -A -q "query" -m 150 -D --dedup-threshold 0.90
```

**Keep Preference:**
```bash
# Keep entry with most metadata
lixplore -A -q "query" -m 100 -D --dedup-keep most_complete

# Prefer entries with DOI
lixplore -A -q "query" -m 100 -D --dedup-keep prefer_doi

# Keep first found
lixplore -A -q "query" -m 100 -D --dedup-keep first
```

**Merge Metadata:**
```bash
lixplore -A -q "query" -m 100 -D --dedup-merge
```
Combines best data from all duplicates into single entry.

### Deduplication Examples

**Example 1: Comprehensive Lit Review**
```bash
lixplore -A -q "cancer immunotherapy" \
  -m 200 \
  -D strict \
  --dedup-keep most_complete \
  --dedup-merge \
  --enrich \
  -X bibtex
```

**Example 2: Quick Discovery**
```bash
lixplore -A -q "new topic" \
  -m 100 \
  -D loose \
  --sort newest \
  -S first:30
```

**Example 3: DOI-Based (Journal Articles Only)**
```bash
lixplore -s PC -q "published research" \
  -m 150 \
  -D doi_only \
  --dedup-keep prefer_doi
```

---

## Result Sorting

### Sort Methods

| Method | Description | Use Case |
|--------|-------------|----------|
| `relevant` | API default | Trust source ranking |
| `newest` | Latest first | Current research |
| `oldest` | Earliest first | Historical perspective |
| `journal` | Alphabetical | Journal-organized biblio |
| `author` | By first author | Author-organized biblio |

### Sort Examples

**Latest Research:**
```bash
lixplore -P -q "COVID-19 treatment" \
  -m 100 \
  --sort newest \
  -S first:20 \
  -X xlsx
```

**Historical Timeline:**
```bash
lixplore -P -q "genetics evolution" \
  -m 100 \
  --sort oldest \
  --stat
```

**Journal Organization:**
```bash
lixplore -C -q "neuroscience" \
  -m 200 \
  --sort journal \
  -X csv
```

**Author Bibliography:**
```bash
lixplore -P -au "Smith J" \
  -m 100 \
  --sort oldest \
  -X enw
```

### Sort + Select Combinations

**Top 10 Latest:**
```bash
lixplore -A -q "AI" -m 200 -D --sort newest -S first:10
```

**Last 5 Oldest:**
```bash
lixplore -P -q "classic papers" -m 100 --sort oldest -S last:5
```

**Even Newest:**
```bash
lixplore -P -q "research" -m 100 --sort newest -S even
```

---

## Selection Patterns

### Pattern Types

**Numbers:**
```bash
lixplore -P -q "query" -m 50 -S 1 3 5 7 9
```

**Ranges:**
```bash
lixplore -P -q "query" -m 100 -S 10-20
```

**Keywords:**
```bash
# Odd articles
lixplore -P -q "query" -m 100 -S odd

# Even articles
lixplore -P -q "query" -m 100 -S even

# First N
lixplore -P -q "query" -m 100 -S first:20

# Last N
lixplore -P -q "query" -m 100 -S last:10

# Top N (alias for first:N)
lixplore -P -q "query" -m 100 -S top:15
```

**Mixed Patterns:**
```bash
lixplore -P -q "query" -m 100 -S 1 3 5-10 15-20 odd
```

### Selection Strategies

**Sample Every Other:**
```bash
# 50% sample
lixplore -P -q "large dataset" -m 200 -S odd -X xlsx
```

**Top Results:**
```bash
# Best 30 after sorting
lixplore -A -q "query" -m 300 -D --sort newest -S first:30
```

**Quality Filter:**
```bash
# Top 25% after quality sort
lixplore -P -q "query" -m 100 --sort newest -S first:25
```

**Stratified Sample:**
```bash
# First 10, middle 10, last 10
lixplore -P -q "query" -m 100 -S first:10 45-55 last:10
```

---

## Complete Workflows

### Workflow 1: Systematic Literature Review

```bash
# Step 1: Comprehensive search across all sources
lixplore -A -q "(cancer OR tumor) AND (immunotherapy OR checkpoint inhibitor)" \
  -m 500 \
  -D strict \
  --dedup-keep most_complete \
  --dedup-merge

# Step 2: Filter to recent research
lixplore -A -q "..." \
  -m 500 \
  -d 2020-01-01 2024-12-31 \
  -D strict \
  --dedup-merge

# Step 3: Sort by newest and select top 100
lixplore -A -q "..." \
  -m 500 \
  -d 2020-01-01 2024-12-31 \
  -D strict \
  --sort newest \
  -S first:100

# Step 4: Enrich and export
lixplore -A -q "..." \
  -m 500 \
  -d 2020-01-01 2024-12-31 \
  -D strict \
  --dedup-merge \
  --sort newest \
  -S first:100 \
  --enrich \
  -X xlsx,bibtex \
  -o systematic_review
```

### Workflow 2: Current Awareness

```bash
# Weekly update: Latest 20 papers in field
lixplore -s PC -q "machine learning healthcare" \
  -d 2024-12-01 2024-12-31 \
  -m 100 \
  -D \
  --sort newest \
  -S first:20 \
  -X xlsx \
  -o weekly_update.xlsx
```

### Workflow 3: Historical Analysis

```bash
# Publication trends over decades
lixplore -P -q "diabetes treatment" \
  -d 1970-01-01 2024-12-31 \
  -m 1000 \
  --sort oldest \
  --stat \
  --stat-top 50
```

### Workflow 4: Quality Screening

```bash
# Step 1: Get large dataset
lixplore -A -q "research topic" -m 500 -D

# Step 2: Sort by newest (proxy for quality)
lixplore -A -q "research topic" -m 500 -D --sort newest

# Step 3: Manual review top 100 with abstracts
lixplore -A -q "research topic" -m 500 -D --sort newest -S first:100 -a

# Step 4: Annotate during review
lixplore --annotate 5 --rating 5 --tags "excellent,must-cite"
lixplore --annotate 8 --rating 4 --tags "relevant"

# Step 5: Export high-rated only
lixplore --filter-annotations "min_rating=4"
lixplore --export-annotations markdown
```

### Workflow 5: Multi-Stage Filtering

```bash
# Stage 1: Broad search
lixplore -A -q "broad topic" -m 1000 -D

# Stage 2: Date filter
lixplore -A -q "broad topic" \
  -m 1000 \
  -d 2020-01-01 2024-12-31 \
  -D

# Stage 3: Sort and select top tier
lixplore -A -q "broad topic" \
  -m 1000 \
  -d 2020-01-01 2024-12-31 \
  -D \
  --sort newest \
  -S first:200

# Stage 4: Manual screening with annotations
lixplore -A -q "broad topic" \
  -m 1000 \
  -d 2020-01-01 2024-12-31 \
  -D \
  --sort newest \
  -S first:200 \
  -a

# Stage 5: Second-round selection
lixplore -A -q "broad topic" \
  -m 1000 \
  -d 2020-01-01 2024-12-31 \
  -D \
  --sort newest \
  -S first:200 \
  -S odd  # 100 articles for deep review

# Stage 6: Final export after annotation
lixplore --filter-annotations "min_rating=4,priority=high"
lixplore --export-annotations markdown
```

---

## Best Practices

### 1. Always Deduplicate Multi-Source

```bash
# ✅ CORRECT
lixplore -A -q "query" -m 50 -D

# ❌ WRONG
lixplore -A -q "query" -m 50
```

### 2. Filter → Deduplicate → Sort → Select → Export

```bash
lixplore -A -q "query" \
  -d 2020-01-01 2024-12-31 \  # 1. Filter
  -m 200 \
  -D \                         # 2. Deduplicate
  --sort newest \              # 3. Sort
  -S first:50 \                # 4. Select
  -X xlsx                      # 5. Export
```

### 3. Use Appropriate Dedup Strategy

- **Final bibliography** → strict
- **Exploration** → loose
- **Balanced** → auto

### 4. Combine Date + Sort for Latest

```bash
lixplore -P -q "COVID-19" \
  -d 2024-01-01 2024-12-31 \
  -m 100 \
  --sort newest
```

### 5. Statistics for Large Sets

```bash
lixplore -A -q "field overview" \
  -m 500 \
  -D \
  --stat \
  --stat-top 25
```

---

## Troubleshooting

**Too many duplicates remain:**
```bash
# Use stricter strategy
lixplore -A -q "query" -m 100 -D strict --dedup-threshold 0.9
```

**Missing valid variants:**
```bash
# Use looser strategy
lixplore -A -q "query" -m 100 -D loose --dedup-threshold 0.75
```

**Date filter not working:**
```bash
# Check format (must be YYYY-MM-DD)
lixplore -P -q "query" -d 2020-01-01 2024-12-31 -m 50
```

**Sort not as expected:**
```bash
# Some articles may lack year/journal metadata
# Consider enrichment first
lixplore -A -q "query" -m 100 -D --enrich --sort newest
```

---

**Last Updated:** 2024-12-28
