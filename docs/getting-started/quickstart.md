# Quick Start Guide

Get started with Lixplore in 5 minutes!

---

## Installation

```bash
pip install lixplore
```

Verify installation:
```bash
lixplore --help
```

---

## Your First Search

### 1. Basic PubMed Search

```bash
lixplore -P -q "cancer treatment" -m 10
```

This searches PubMed for "cancer treatment" and returns 10 results.

**Output:**
```
Searching for query: cancer treatment
Sources: PubMed
  Searching PubMed...

Found 10 results:
[1] Novel approaches to cancer treatment...
[2] Immunotherapy in cancer treatment...
[3] Precision medicine for cancer...
...
```

### 2. Search Multiple Sources

```bash
lixplore -A -q "machine learning" -m 20 -D
```

- `-A`: Search ALL sources (PubMed, arXiv, Crossref, DOAJ, EuropePMC)
- `-m 20`: Get 20 results per source
- `-D`: Deduplicate results

### 3. Interactive Browsing

```bash
lixplore -P -q "CRISPR" -m 50 -i
```

Browse results interactively with a simple menu interface.

---

## Common Commands

### Export to Excel

```bash
lixplore -P -q "diabetes" -m 100 -X xlsx -o results.xlsx
```

### Export to BibTeX

```bash
lixplore -P -q "neuroscience" -m 100 -X bibtex -o references.bib
```

### Find Open Access PDFs

```bash
lixplore -x -q "neural networks" -m 20 --show-pdf-links
```

### Search by Date Range

```bash
lixplore -P -q "COVID-19" -d 2023-01-01 2024-12-31 -m 50
```

### Search by Author

```bash
lixplore -P -au "Smith J" -m 30
```

---

## Quick Examples by Use Case

### For Literature Reviews

```bash
# Comprehensive search across all sources
lixplore -A -q "systematic review cancer treatment" \
  -m 100 -D --sort newest -X xlsx -o review.xlsx
```

### For Citation Management

```bash
# Export to BibTeX for LaTeX
lixplore -P -q "quantum computing" -m 200 -X bibtex -o refs.bib

# Export to RIS for EndNote/Mendeley
lixplore -P -q "genetics" -m 150 -X ris -o refs.ris
```

### For Data Analysis

```bash
# Export to JSON for processing
lixplore -A -q "climate change" -m 500 -D -X json -o data.json

# Export to CSV for spreadsheets
lixplore -P -q "public health" -m 200 -X csv -o data.csv
```

### For Finding Free PDFs

```bash
# arXiv papers with PDF links
lixplore -x -q "deep learning" -m 50 --show-pdf-links

# Download PDFs automatically
lixplore -x -q "machine learning" -m 30 --download-pdf
```

---

## Annotations

### Annotate Important Articles

```bash
# First, search
lixplore -P -q "stem cells" -m 50

# Then annotate article #5
lixplore --annotate 5 --rating 5 --tags "important,cite" \
  --comment "Groundbreaking research"

# View all annotations
lixplore --list-annotations

# Export annotations
lixplore --export-annotations markdown
```

---

## Automation

### Daily Monitoring (Cron Job)

```bash
# Add to crontab (crontab -e)
0 9 * * * lixplore -P -q "your topic" -m 50 -X csv -o ~/daily_$(date +\%Y\%m\%d).csv
```

### Save and Reuse Configurations

```bash
# Save a profile
lixplore -P -q "test" -m 100 -D --sort newest \
  --save-profile my_search

# Reuse the profile
lixplore -q "new topic" --load-profile my_search
```

---

## Command Structure

Lixplore commands follow this pattern:

```bash
lixplore [SOURCE] [SEARCH] [FILTERS] [DISPLAY] [EXPORT]
```

### Examples:

```bash
# Source + Search + Export
lixplore -P -q "cancer" -X csv

# Source + Search + Filters + Export
lixplore -A -q "AI" -D --sort newest -X xlsx

# Source + Search + Display
lixplore -P -q "research" -m 50 -i

# Source + Search + Filters + Display + Export
lixplore -A -q "topic" -d 2023-01-01 2024-12-31 -D -i -X bibtex
```

---

## Cheat Sheet

| Task | Command |
|------|---------|
| **Basic search** | `lixplore -P -q "topic" -m 20` |
| **All sources** | `lixplore -A -q "topic" -m 50 -D` |
| **Export Excel** | `lixplore -P -q "topic" -m 100 -X xlsx` |
| **Export BibTeX** | `lixplore -P -q "topic" -m 100 -X bibtex` |
| **Interactive** | `lixplore -P -q "topic" -m 50 -i` |
| **PDF links** | `lixplore -x -q "topic" -m 20 --show-pdf-links` |
| **Date filter** | `lixplore -P -q "topic" -d 2023-01-01 2024-12-31` |
| **Author search** | `lixplore -P -au "Author Name" -m 30` |
| **Statistics** | `lixplore -A -q "topic" -m 100 --stat` |
| **Annotate** | `lixplore --annotate 5 --rating 5 --tags "cite"` |
| **View history** | `lixplore -H` |
| **Show examples** | `lixplore --examples` |

---

## Next Steps

- [Basic Usage Guide](basic-usage.md) - Learn fundamental concepts
- [First Search Tutorial](first-search.md) - Step-by-step walkthrough
- [Complete Flag Reference](../reference/flags-overview.md) - All commands
- [Examples & Use Cases](../examples/workflows.md) - Real-world scenarios

---

## Getting Help

```bash
# Show help
lixplore --help

# Show quick examples
lixplore --examples

# View search history
lixplore -H
```

**Questions?** Check the [FAQ](../about/faq.md) or open an [issue on GitHub](https://github.com/pryndor/Lixplore_cli/issues).

---

**Ready to dive deeper?** Continue to [Basic Usage](basic-usage.md) →
