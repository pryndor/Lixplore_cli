# Lixplore_cli - Academic Literature Explorer

**Fast, lightweight, multi-source academic literature search and export tool for researchers.**

---

## Overview

Lixplore is a powerful command-line tool designed for researchers, students, and academics who need to search, filter, export, and manage academic literature from multiple sources.

### Key Features

**Multi-Source Search**  
Search across 5 major academic databases simultaneously:

- PubMed (biomedical literature)
- arXiv (preprints in physics, math, CS, etc.)
- Crossref (DOI database with 130M+ records)
- DOAJ (Directory of Open Access Journals)
- EuropePMC (life sciences literature)

**10+ Export Formats**  
Export your results in any format you need:

- Citation formats: BibTeX, RIS, EndNote (Tagged & XML)
- Data formats: CSV, Excel (XLSX), JSON, XML
- Citations: APA, MLA, Chicago, Harvard, Vancouver, IEEE

**Powerful Annotation System**  
Organize your research with:

- 5-star ratings
- Custom tags
- Comments and notes
- Priority levels
- Read status tracking
- Full-text search across annotations

**Interactive Modes**  
Browse results interactively with:

- Simple TUI for quick browsing
- Enhanced TUI with advanced features
- Wizard mode for guided searches
- Shell mode for multiple commands

**PDF Management**  
Access open access literature:

- Automatic detection of open access PDFs
- Clickable PDF links in terminal
- Bulk PDF download
- SciHub integration (optional)
- Organized file storage

---

## Quick Start

### Installation

```bash
pip install lixplore
```

### Basic Search

```bash
# Search PubMed for cancer research
lixplore -P -q "cancer treatment" -m 50

# Search all sources with deduplication
lixplore -A -q "machine learning" -m 50 -D

# Interactive browsing
lixplore -P -q "CRISPR" -m 50 -i
```

### Export Results

```bash
# Export to Excel
lixplore -P -q "research topic" -m 100 -X xlsx -o results.xlsx

# Export to BibTeX
lixplore -P -q "neuroscience" -m 100 -X bibtex -o references.bib

# Export to JSON
lixplore -A -q "climate change" -m 200 -D -X json -o data.json
```

---

## Why Lixplore?

**For Researchers**: Search multiple databases in one command, stay organized with annotations, automate daily monitoring

**For Students**: Quick literature reviews, citation management, find open access PDFs

**For Data Scientists**: API access via JSON export, AI integration, batch processing

---

## Documentation

- [Installation Guide](getting-started/installation.md)
- [Quick Start](getting-started/quickstart.md)
- [Complete Flag Reference](reference/flags-overview.md)
- [Examples & Use Cases](examples/workflows.md)

---

**Ready to Get Started?**

Install now: `pip install lixplore`

View all documentation in the menu above.
