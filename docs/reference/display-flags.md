# Display Option Flags

> **Complete documentation for result display and viewing flags**

## Table of Contents

- [Overview](#overview)
- [Abstract Display](#abstract-display)
- [Interactive Mode](#interactive-mode)
- [Article Details](#article-details)
- [Review Mode](#review-mode)
- [Statistics Dashboard](#statistics-dashboard)
- [Pagination](#pagination)
- [PDF Links](#pdf-links)

---

## Overview

Display flags control how search results are shown, viewed, and browsed in the terminal.

**Total Display Flags:** 9

---

## `-a, --abstract`

**Description:** Display article abstracts inline with search results.

**Syntax:**
```bash
lixplore [SOURCE] -q "QUERY" -a [OPTIONS]
```

**Type:** Boolean flag

#### Examples

**Example 1: View Abstracts**
```bash
lixplore -P -q "cancer treatment" -m 10 -a
```

**Example 2: Abstracts with PDF Links**
```bash
lixplore -J -q "open access" -m 15 -a --show-pdf-links
```

**Example 3: Export After Review**
```bash
lixplore -P -q "diabetes" -m 20 -a
# Review abstracts, then:
lixplore -P -q "diabetes" -m 20 -S 1 3 5 -X xlsx
```

---

## `-i, --interactive`

**Description:** Launch simple interactive TUI mode for searching and browsing.

**Syntax:**
```bash
lixplore -i  # Standalone
lixplore [SOURCE] -q "QUERY" -i  # After search
```

**Type:** Boolean flag

#### Examples

**Example 1: Standalone Interactive**
```bash
lixplore -i
```

**Example 2: Interactive After Search**
```bash
lixplore -P -q "neuroscience" -m 50 -i
```

**Example 3: Multi-Source Interactive**
```bash
lixplore -A -q "AI" -m 100 -D -i
```

**Tips:**
- Navigate with arrow keys
- Select articles with space
- Press 'q' to quit

---

## `-N, --number`

**Description:** View detailed JSON information for specific article(s).

**Syntax:**
```bash
lixplore [SOURCE] -q "QUERY" -N NUMBER [NUMBER...]
```

**Type:** List of integers

#### Examples

**Example 1: Single Article**
```bash
lixplore -P -q "cancer" -m 20 -N 5
```

**Example 2: Multiple Articles**
```bash
lixplore -P -q "genetics" -m 30 -N 1 5 10 15
```

**Example 3: Inspect Before Export**
```bash
lixplore -C -q "quantum physics" -m 25 -N 3
# Check metadata completeness, then export
```

---

## `-R, --review`

**Description:** Open article(s) in separate terminal window for detailed review.

**Syntax:**
```bash
lixplore -R NUMBER [NUMBER...]  # Standalone
lixplore [SOURCE] -q "QUERY" -R NUMBER [NUMBER...]  # With search
```

**Type:** List of integers

#### Examples

**Example 1: Review from Cache**
```bash
# Step 1: Search and cache
lixplore -P -q "diabetes" -m 20

# Step 2: Review specific articles
lixplore -R 3 7 12
```

**Example 2: Search and Review**
```bash
lixplore -P -q "cancer" -m 15 -R 1 2 3
```

**Example 3: Review Single Article**
```bash
lixplore -R 5  # Opens article #5 from last search
```

**Tips:**
- Press 'q' or Ctrl+C to close review window
- Works on Linux, macOS, Windows
- Caches results for later review

---

## `--stat`

**Description:** Show comprehensive statistics dashboard with visualizations.

**Syntax:**
```bash
lixplore [SOURCE] -q "QUERY" --stat [OPTIONS]
```

**Type:** Boolean flag

#### Examples

**Example 1: Publication Trends**
```bash
lixplore -A -q "COVID-19" -m 200 -D --stat
```

**Example 2: Author Analysis**
```bash
lixplore -P -au "Watson JD" -m 100 --stat --stat-top 20
```

**Example 3: Journal Distribution**
```bash
lixplore -C -q "neuroscience" -m 300 --stat
```

**Statistics Shown:**
- Publication trends by year
- Top journals (by article count)
- Top authors (by publication count)
- Source distribution
- Metadata completeness

---

## `--stat-top`

**Description:** Number of top items to show in statistics rankings.

**Syntax:**
```bash
lixplore [SOURCE] -q "QUERY" --stat --stat-top N
```

**Type:** Integer

**Default:** 10

#### Examples

**Example 1: Top 20 Journals**
```bash
lixplore -A -q "machine learning" -m 500 -D --stat --stat-top 20
```

**Example 2: Top 5 Authors**
```bash
lixplore -P -q "genetics" -m 200 --stat --stat-top 5
```

---

## `-p, --page`

**Description:** Page number to display when results exceed page size.

**Syntax:**
```bash
lixplore [SOURCE] -q "QUERY" -p PAGE_NUMBER
```

**Type:** Integer

**Default:** 1

#### Examples

**Example 1: View Second Page**
```bash
lixplore -P -q "cancer" -m 100 -p 2
```

**Example 2: Custom Page Size**
```bash
lixplore -P -q "diabetes" -m 200 -p 3 --page-size 50
```

---

## `--page-size`

**Description:** Number of results to display per page.

**Syntax:**
```bash
lixplore [SOURCE] -q "QUERY" --page-size N
```

**Type:** Integer

**Default:** 20

#### Examples

**Example 1: Show 50 Per Page**
```bash
lixplore -P -q "genetics" -m 200 --page-size 50
```

**Example 2: Small Pages**
```bash
lixplore -A -q "AI" -m 500 -D --page-size 10 -p 5
```

---

## `--show-pdf-links`

**Description:** Display clickable PDF links for open access articles.

**Syntax:**
```bash
lixplore [SOURCE] -q "QUERY" --show-pdf-links
```

**Type:** Boolean flag

#### Examples

**Example 1: arXiv PDF Links**
```bash
lixplore -x -q "neural networks" -m 15 --show-pdf-links
```

**Example 2: Open Access PDFs**
```bash
lixplore -J -q "public health" -m 20 --show-pdf-links
```

**Example 3: With Abstracts**
```bash
lixplore -P -q "COVID-19" -m 25 -a --show-pdf-links
```

**PDF Sources:**
- PubMed Central (PMC)
- arXiv
- Unpaywall
- DOAJ

**Tips:**
- Links are clickable in modern terminals
- Works in iTerm2, GNOME Terminal, Windows Terminal
- No download required - opens in browser

---

## Best Practices

### 1. Preview Before Export
```bash
lixplore -P -q "cancer" -m 50 -a
# Review abstracts
lixplore -P -q "cancer" -m 50 -S 1 3 5 8 -X xlsx
```

### 2. Use Review Mode for Detailed Inspection
```bash
lixplore -P -q "genetics" -m 30
lixplore -R 5 10 15  # Deep dive into specific articles
```

### 3. Statistics for Large Datasets
```bash
lixplore -A -q "machine learning" -m 500 -D --stat --stat-top 25
```

### 4. Pagination for Large Results
```bash
lixplore -P -q "cancer" -m 200 -p 1 --page-size 25
# Browse page by page
lixplore -P -q "cancer" -m 200 -p 2 --page-size 25
```

---

**Last Updated:** 2024-12-28
