# Search Sources Guide

> **Comprehensive guide to searching each academic database**

## Table of Contents

- [PubMed](#pubmed)
- [Crossref](#crossref)
- [DOAJ](#doaj)
- [EuropePMC](#europepmc)
- [arXiv](#arxiv)
- [Multi-Source Strategies](#multi-source-strategies)

---

## PubMed

### Overview
- **Coverage:** 35+ million citations
- **Focus:** Biomedical and life sciences
- **Provider:** U.S. National Library of Medicine
- **Best For:** Clinical medicine, biology, health sciences

### Basic Search
```bash
lixplore -P -q "diabetes treatment" -m 20
```

### Advanced Search Techniques

**1. MeSH Terms (Medical Subject Headings)**
```bash
lixplore -P -q "diabetes mellitus[MeSH]" -m 30
```

**2. Field-Specific Search**
```bash
# Title field
lixplore -P -q "CRISPR[Title]" -m 20

# Title/Abstract
lixplore -P -q "gene therapy[Title/Abstract]" -m 30

# Author field
lixplore -P -q "Smith J[Author] AND cancer[Title]" -m 15
```

**3. Publication Type Filters**
```bash
lixplore -P -q "diabetes AND systematic review[pt]" -m 20
lixplore -P -q "COVID-19 AND randomized controlled trial[pt]" -m 30
```

### Best Practices

**DO:**
- Use MeSH terms for precision
- Combine with date filters for recent research
- Search author publications
- Use field tags [Title], [Author], [Journal]

**DON'T:**
- Expect full-text availability for all articles
- Use for non-biomedical topics
- Ignore publication type filters

### Common Workflows

**Clinical Research:**
```bash
lixplore -P -q "hypertension AND treatment[Title/Abstract]" \
  -d 2020-01-01 2024-12-31 \
  -m 50 \
  --sort newest \
  -X enw
```

**Author Publications:**
```bash
lixplore -P -au "Smith J" -m 100 --sort newest --stat
```

**Systematic Review Preparation:**
```bash
lixplore -P -q "cancer immunotherapy" \
  -m 200 \
  --enrich \
  -X xlsx \
  -o systematic_review.xlsx
```

---

## Crossref

### Overview
- **Coverage:** 140+ million records
- **Focus:** All academic disciplines with DOIs
- **Provider:** Crossref (DOI registration agency)
- **Best For:** Multi-disciplinary research, citation metadata

### Basic Search
```bash
lixplore -C -q "machine learning" -m 30
```

### Advanced Techniques

**1. DOI Lookup**
```bash
lixplore -C -DOI "10.1038/nature12345"
```

**2. Journal-Focused Search**
```bash
lixplore -C -q "artificial intelligence" -m 100 --sort journal
```

**3. Citation Metadata**
```bash
lixplore -C -q "quantum computing" -m 50 --enrich crossref -X bibtex
```

### Best Practices

**DO:**
- Use for DOI lookup
- Combine with enrichment for complete metadata
- Search across all disciplines
- Export to BibTeX for LaTeX

**DON'T:**
- Expect full-text access
- Use for preprint-only searches
- Rely on abstract availability

### Common Workflows

**Bibliography Building:**
```bash
lixplore -C -q "topic" -m 100 --enrich crossref -X bibtex -o refs.bib
```

**Multi-Disciplinary Review:**
```bash
lixplore -C -q "artificial intelligence healthcare" \
  -m 200 \
  --sort newest \
  -S first:50 \
  -X xlsx
```

---

## DOAJ

### Overview
- **Coverage:** 19,000+ journals, 8+ million articles
- **Focus:** Open access peer-reviewed content
- **Provider:** DOAJ (community-driven)
- **Best For:** Free full-text access, open science

### Basic Search
```bash
lixplore -J -q "renewable energy" -m 20
```

### Advanced Techniques

**1. Open Access PDFs**
```bash
lixplore -J -q "public health" -m 15 --download-pdf
```

**2. PDF Link Display**
```bash
lixplore -J -q "education" -m 20 --show-pdf-links
```

**3. Multi-Format Export**
```bash
lixplore -J -q "psychology" -m 30 -X csv,ris,bibtex
```

### Best Practices

**DO:**
- Use for freely accessible articles
- Download PDFs directly
- Combine with other sources (deduplicate)
- Check for open access versions

**DON'T:**
- Expect comprehensive coverage
- Use as only source for lit reviews
- Assume latest articles indexed immediately

### Common Workflows

**Open Access Literature Review:**
```bash
lixplore -J -q "machine learning" \
  -m 50 \
  --download-pdf \
  -X xlsx \
  -o open_access_ml.xlsx
```

**PDF Collection:**
```bash
lixplore -J -q "climate change" -m 30 --show-pdf-links
# Click links or:
lixplore -J -q "climate change" -m 30 --download-pdf
```

---

## EuropePMC

### Overview
- **Coverage:** 42+ million records
- **Focus:** Biomedical, life sciences (European)
- **Provider:** EMBL-EBI
- **Best For:** European research, open access content

### Basic Search
```bash
lixplore -E -q "malaria treatment" -m 20
```

### Advanced Techniques

**1. Grant-Funded Research**
```bash
lixplore -E -q "gene therapy" -m 30 --enrich
```

**2. Open Access Filter**
```bash
lixplore -E -q "immunology" -m 25 --download-pdf
```

### Best Practices

**DO:**
- Use alongside PubMed for biomedical
- Check for open access content
- Use deduplication with PubMed

**DON'T:**
- Use for non-biomedical topics
- Expect different results from PubMed always
- Skip deduplication

### Common Workflows

**Biomedical Research (EU Focus):**
```bash
lixplore -s PE -q "cancer therapy" \
  -m 100 \
  -D \
  --sort newest \
  -X enw
```

---

## arXiv

### Overview
- **Coverage:** 2.3+ million preprints
- **Focus:** Physics, math, CS, quantitative fields
- **Provider:** Cornell University
- **Best For:** Latest research, preprints, open access PDFs

### Basic Search
```bash
lixplore -x -q "neural networks" -m 20
```

### Advanced Techniques

**1. Latest Research**
```bash
lixplore -x -q "transformers" -m 30 --sort newest
```

**2. PDF Downloads**
```bash
lixplore -x -q "deep learning" -m 10 --download-pdf
```

**3. Clickable PDF Links**
```bash
lixplore -x -q "quantum physics" -m 15 --show-pdf-links
```

**4. Author Tracking**
```bash
lixplore -x -au "LeCun Y" -m 20 --sort newest
```

### Best Practices

**DO:**
- Use for cutting-edge CS/physics research
- Download PDFs (always available)
- Track specific authors
- Sort by newest for latest papers

**DON'T:**
- Expect peer review
- Use for medical/clinical research
- Trust all methodologies blindly

### Common Workflows

**Stay Current in CS:**
```bash
lixplore -x -q "machine learning" \
  -d 2024-01-01 2024-12-31 \
  -m 100 \
  --sort newest \
  --stat
```

**Author Monitoring:**
```bash
lixplore -x -au "Hinton G" -m 50 --sort newest -X xlsx
```

**PDF Collection:**
```bash
lixplore -x -q "deep learning" -m 20 --download-pdf
```

---

## Multi-Source Strategies

### All Sources Search
```bash
lixplore -A -q "query" -m 50 -D --sort newest
```

**Advantages:**
- Comprehensive coverage
- Cross-disciplinary results
- Maximum recall

**Disadvantages:**
- Slower (5x API calls)
- Many duplicates (use -D!)
- Can be overwhelming

### Custom Combinations

**Biomedical (PubMed + EuropePMC):**
```bash
lixplore -s PE -q "cancer treatment" -m 50 -D
```

**Computer Science (arXiv + Crossref):**
```bash
lixplore -s XC -q "machine learning" -m 50 -D
```

**Open Access Only (DOAJ + arXiv):**
```bash
lixplore -s JX -q "research" -m 50 -D --download-pdf
```

**Peer-Reviewed Recent (PubMed + Crossref):**
```bash
lixplore -s PC -q "AI" -m 100 -D --sort newest -S first:30
```

### Deduplication Strategy

**Essential for Multi-Source:**
```bash
# ALWAYS use -D flag
lixplore -A -q "query" -m 50 -D
```

**Choose Strategy:**
```bash
# Strict (bibliography)
lixplore -A -q "query" -m 100 -D strict

# Loose (discovery)
lixplore -A -q "query" -m 200 -D loose

# Auto (balanced)
lixplore -A -q "query" -m 150 -D
```

---

## Source Selection Decision Tree

```
Need biomedical/clinical research?
  ├─ Yes → PubMed or EuropePMC
  └─ No → Continue

Need latest CS/physics preprints?
  ├─ Yes → arXiv
  └─ No → Continue

Need open access PDFs?
  ├─ Yes → DOAJ or arXiv
  └─ No → Continue

Need multi-disciplinary?
  ├─ Yes → Crossref or All sources
  └─ No → Continue

Need comprehensive coverage?
  └─ Use All sources (-A) with deduplication (-D)
```

---

## Performance Comparison

| Aspect | PubMed | Crossref | DOAJ | EuropePMC | arXiv |
|--------|--------|----------|------|-----------|-------|
| **Speed** | Fast | Fast | Medium | Medium | Fast |
| **Coverage** | ★★★★☆ | ★★★★★ | ★★★☆☆ | ★★★★☆ | ★★★☆☆ |
| **Full Text** | Some | No | Yes | Some | Yes |
| **Metadata** | ★★★★★ | ★★★★★ | ★★★☆☆ | ★★★★☆ | ★★★☆☆ |

---

**Last Updated:** 2024-12-28
