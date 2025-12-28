# Basic Usage

Learn the fundamentals of Lixplore.

---

## Core Concepts

### 1. Sources

Lixplore searches 5 academic databases:

- **PubMed** (`-P`): Biomedical and life sciences
- **arXiv** (`-x`): Preprints in physics, math, CS, etc.
- **Crossref** (`-C`): DOI database (130M+ records)
- **DOAJ** (`-J`): Directory of Open Access Journals
- **EuropePMC** (`-E`): Europe PubMed Central

### 2. Results Per Source

The `-m` flag specifies results **per source**:

```bash
# Single source: 50 results total
lixplore -P -q "cancer" -m 50

# All sources: 250 results total (5 sources × 50)
lixplore -A -q "cancer" -m 50
```

Use `-D` to deduplicate when using multiple sources.

### 3. Export Formats

Lixplore supports 10+ export formats:

- **Data**: CSV, Excel (XLSX), JSON, XML
- **Citations**: BibTeX, RIS, EndNote (Tagged & XML)
- **Formatted**: APA, MLA, Chicago, Harvard, Vancouver, IEEE

---

## Common Workflows

### Literature Review

```bash
#1. Comprehensive search
lixplore -A -q "your research topic" -m 100 -D --sort newest

# 2. Review interactively
lixplore -i

# 3. Export top 50
lixplore -S first:50 -X xlsx -o review.xlsx
```

### Citation Management

```bash
# Search and export for LaTeX
lixplore -P -q "topic" -m 200 -X bibtex -o references.bib

# For EndNote/Mendeley
lixplore -P -q "topic" -m 200 -X ris -o references.ris
```

### PDF Collection

```bash
# Find open access PDFs
lixplore -x -q "machine learning" -m 50 --show-pdf-links

# Download automatically
lixplore -x -q "neural networks" -m 30 --download-pdf
```

---

## File Organization

Lixplore automatically organizes files:

```
~/
├── Lixplore_PDFs/              # Downloaded PDFs
│   ├── pubmed/
│   ├── arxiv/
│   └── scihub/
├── .lixplore_cache.json        # 7-day cache
├── .lixplore_annotations.json  # Your annotations
└── .lixplore/
    ├── profiles.json           # Saved profiles
    ├── templates/              # Export templates
    └── apis/                   # Custom APIs
```

---

## Next: [First Search Tutorial](first-search.md) →
