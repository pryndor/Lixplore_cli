# Source Selection Flags

> **Complete documentation for all source selection flags in Lixplore**

## Table of Contents

- [Overview](#overview)
- [Individual Source Flags](#individual-source-flags)
- [Combined Source Flags](#combined-source-flags)
- [Custom API Integration](#custom-api-integration)
- [Source Comparison](#source-comparison)
- [Best Practices](#best-practices)

---

## Overview

Lixplore supports searching across 5 major academic databases plus custom API integrations. You can search individual sources or combine multiple sources in a single query.

**Total Source Flags:** 8

### Available Sources
- **PubMed** - Biomedical and life sciences literature (MEDLINE)
- **Crossref** - Scholarly works with DOIs (70+ million records)
- **DOAJ** - Directory of Open Access Journals
- **EuropePMC** - Europe PubMed Central (biomedical + life sciences)
- **arXiv** - Preprint repository (physics, math, CS, etc.)
- **Custom APIs** - User-configured sources (Springer, BASE, etc.)

---

## Individual Source Flags

### `-P, --pubmed`

**Description:** Search PubMed (MEDLINE) database for biomedical and life sciences literature.

**Syntax:**
```bash
lixplore -P -q "QUERY" [OPTIONS]
lixplore --pubmed -q "QUERY" [OPTIONS]
```

**Type:** Boolean flag (no value required)

**Default:** Not enabled

**Database Info:**
- **Coverage:** 35+ million citations
- **Focus:** Biomedical, life sciences, clinical medicine
- **Provider:** U.S. National Library of Medicine (NLM)
- **Update Frequency:** Daily
- **Full Text:** Links to PMC when available

#### Examples

**Example 1: Basic PubMed Search**
```bash
lixplore -P -q "cancer treatment" -m 20
```
Search PubMed for cancer treatment articles, retrieve 20 results.

**Example 2: PubMed with Abstracts**
```bash
lixplore -P -q "diabetes type 2" -m 15 -a
```
Search diabetes articles and display abstracts inline.

**Example 3: PubMed with Date Filter**
```bash
lixplore -P -q "COVID-19 vaccine" -d 2020-01-01 2024-12-31 -m 30
```
Search COVID-19 vaccine articles published between 2020-2024.

**Example 4: PubMed Export to EndNote**
```bash
lixplore -P -q "neuroscience" -m 50 -X enw -o brain_research.enw
```
Search neuroscience articles and export to EndNote Tagged format.

**Example 5: PubMed with Boolean Operators**
```bash
lixplore -P -q "(cancer OR tumor) AND (treatment OR therapy)" -m 40
```
Advanced query using AND/OR operators for precise results.

#### Tips
- PubMed excels at biomedical and clinical research
- Use MeSH terms for better precision (e.g., "diabetes mellitus" instead of "diabetes")
- Author search format: `lixplore -P -au "Smith J" -m 10`
- Combine with `-a` flag to preview abstracts before exporting

#### Warnings
- PubMed API rate limit: 3 requests/second (handled automatically)
- Results may not include full text (check PMC availability)
- Date filters may not work for all queries (PubMed limitation)

#### Related Flags
- [`-au, --author`](search-flags.md#author) - Search by author name
- [`-d, --date`](filter-flags.md#date) - Date range filter
- [`--download-pdf`](export-flags.md#download-pdf) - Download PMC PDFs

---

### `-C, --crossref`

**Description:** Search Crossref database for scholarly works across all disciplines with DOI registration.

**Syntax:**
```bash
lixplore -C -q "QUERY" [OPTIONS]
lixplore --crossref -q "QUERY" [OPTIONS]
```

**Type:** Boolean flag

**Default:** Not enabled

**Database Info:**
- **Coverage:** 140+ million records
- **Focus:** All academic disciplines with DOIs
- **Provider:** Crossref (DOI registration agency)
- **Update Frequency:** Real-time
- **Full Text:** Links to publisher websites

#### Examples

**Example 1: Crossref Multi-Disciplinary Search**
```bash
lixplore -C -q "machine learning" -m 30
```
Search across all disciplines for machine learning papers.

**Example 2: Crossref with Sorting**
```bash
lixplore -C -q "climate change" -m 50 --sort newest
```
Get latest climate change research sorted by publication date.

**Example 3: Crossref DOI Lookup**
```bash
lixplore -C -DOI "10.1038/nature12345"
```
Retrieve article metadata using DOI.

**Example 4: Crossref Export to BibTeX**
```bash
lixplore -C -q "quantum computing" -m 25 -X bibtex
```
Export quantum computing papers for LaTeX citations.

**Example 5: Crossref with Enrichment**
```bash
lixplore -C -q "CRISPR" -m 20 --enrich crossref
```
Search and enrich metadata with additional Crossref data.

#### Tips
- Crossref has excellent coverage across ALL disciplines
- DOI lookup is extremely reliable and fast
- Metadata is generally very complete (journal, volume, pages, etc.)
- Best source for citation metadata and journal information

#### Warnings
- No full-text access (only metadata and DOI links)
- Some preprints may not be included
- Publisher paywalls may prevent access to full articles

#### Related Flags
- [`-DOI, --doi`](search-flags.md#doi) - Direct DOI lookup
- [`--enrich`](filter-flags.md#enrich) - Metadata enrichment
- [`--sort`](filter-flags.md#sort) - Sort by date/journal/author

---

### `-J, --doaj`

**Description:** Search Directory of Open Access Journals (DOAJ) for freely accessible peer-reviewed content.

**Syntax:**
```bash
lixplore -J -q "QUERY" [OPTIONS]
lixplore --doaj -q "QUERY" [OPTIONS]
```

**Type:** Boolean flag

**Default:** Not enabled

**Database Info:**
- **Coverage:** 19,000+ journals, 8+ million articles
- **Focus:** Open access peer-reviewed journals
- **Provider:** DOAJ (community-driven)
- **Update Frequency:** Weekly
- **Full Text:** Always freely available

#### Examples

**Example 1: DOAJ Open Access Search**
```bash
lixplore -J -q "renewable energy" -m 20
```
Search open access journals for renewable energy research.

**Example 2: DOAJ with PDF Links**
```bash
lixplore -J -q "public health" -m 15 --show-pdf-links
```
Display clickable PDF links for open access articles.

**Example 3: DOAJ PDF Download**
```bash
lixplore -J -q "education" -m 10 --download-pdf
```
Search and automatically download open access PDFs.

**Example 4: DOAJ Multi-Format Export**
```bash
lixplore -J -q "psychology" -m 30 -X csv,ris,bibtex
```
Export to multiple formats simultaneously.

**Example 5: DOAJ with Statistics**
```bash
lixplore -J -q "artificial intelligence" -m 100 --stat
```
Analyze publication trends in open access AI research.

#### Tips
- ALL results are open access (no paywalls!)
- Great source for freely downloadable PDFs
- Excellent for literature reviews requiring full-text access
- High-quality peer-reviewed content only

#### Warnings
- Smaller coverage compared to PubMed/Crossref
- May not have latest articles (indexing delay)
- Some disciplines better represented than others

#### Related Flags
- [`--show-pdf-links`](display-flags.md#show-pdf-links) - Display PDF links
- [`--download-pdf`](export-flags.md#download-pdf) - Download PDFs
- [`--stat`](display-flags.md#stat) - Statistics dashboard

---

### `-E, --europepmc`

**Description:** Search Europe PubMed Central for biomedical and life sciences literature in Europe.

**Syntax:**
```bash
lixplore -E -q "QUERY" [OPTIONS]
lixplore --europepmc -q "QUERY" [OPTIONS]
```

**Type:** Boolean flag

**Default:** Not enabled

**Database Info:**
- **Coverage:** 42+ million records
- **Focus:** Biomedical, life sciences (European focus)
- **Provider:** EMBL-EBI
- **Update Frequency:** Daily
- **Full Text:** Open access articles available

#### Examples

**Example 1: EuropePMC Search**
```bash
lixplore -E -q "malaria treatment" -m 20
```
Search European biomedical database for malaria research.

**Example 2: EuropePMC with Date Filter**
```bash
lixplore -E -q "gene therapy" -d 2022-01-01 2024-12-31 -m 25
```
Recent gene therapy articles from 2022-2024.

**Example 3: EuropePMC Author Search**
```bash
lixplore -E -au "Watson J" -m 15 -a
```
Find articles by author in EuropePMC.

**Example 4: EuropePMC Open Access**
```bash
lixplore -E -q "immunology" -m 30 --download-pdf
```
Search and download open access immunology papers.

**Example 5: EuropePMC Export**
```bash
lixplore -E -q "cardiology" -m 40 -X xlsx --export-fields title authors year doi
```
Export cardiology articles with selected fields.

#### Tips
- Good alternative/complement to PubMed
- Strong coverage of European research
- Excellent open access content availability
- Often includes grants and funding information

#### Warnings
- Some overlap with PubMed (use deduplication)
- European focus may miss some international research
- API can be slower during peak hours

#### Related Flags
- [`-P, --pubmed`](#pubmed) - Compare with PubMed
- [`-D, --deduplicate`](filter-flags.md#deduplicate) - Remove duplicates
- [`--download-pdf`](export-flags.md#download-pdf) - PDF download

---

### `-x, --arxiv`

**Description:** Search arXiv preprint repository for physics, mathematics, computer science, and related fields.

**Syntax:**
```bash
lixplore -x -q "QUERY" [OPTIONS]
lixplore --arxiv -q "QUERY" [OPTIONS]
```

**Type:** Boolean flag

**Default:** Not enabled

**Database Info:**
- **Coverage:** 2.3+ million preprints
- **Focus:** Physics, math, CS, quantitative fields
- **Provider:** Cornell University
- **Update Frequency:** Daily submissions
- **Full Text:** Always freely available (PDFs)

#### Examples

**Example 1: arXiv Computer Science Search**
```bash
lixplore -x -q "neural networks" -m 20
```
Search arXiv for neural network preprints.

**Example 2: arXiv with PDF Links**
```bash
lixplore -x -q "quantum physics" -m 15 --show-pdf-links
```
Display clickable PDF links for quantum physics papers.

**Example 3: arXiv Latest Research**
```bash
lixplore -x -q "transformers" -m 30 --sort newest
```
Get the latest transformer architecture papers.

**Example 4: arXiv PDF Download**
```bash
lixplore -x -q "deep learning" -m 10 --download-pdf
```
Search and download deep learning PDFs automatically.

**Example 5: arXiv with Statistics**
```bash
lixplore -x -q "machine learning" -m 200 --stat --stat-top 20
```
Analyze ML research trends with top 20 authors/topics.

#### Tips
- Best source for cutting-edge CS/physics research
- ALL articles have freely downloadable PDFs
- Often contains latest research before peer review
- Great for staying current in fast-moving fields

#### Warnings
- Preprints (not peer-reviewed)
- Quality varies (no editorial filtering)
- Limited to STEM fields (physics, math, CS, etc.)
- Author search may be less accurate than PubMed

#### Related Flags
- [`--show-pdf-links`](display-flags.md#show-pdf-links) - Display PDF links
- [`--download-pdf`](export-flags.md#download-pdf) - Automatic PDF download
- [`--sort`](filter-flags.md#sort) - Sort by date for latest papers

---

### `-A, --all`

**Description:** Search ALL sources simultaneously (PubMed, Crossref, DOAJ, EuropePMC, arXiv).

**Syntax:**
```bash
lixplore -A -q "QUERY" [OPTIONS]
lixplore --all -q "QUERY" [OPTIONS]
```

**Type:** Boolean flag

**Default:** Not enabled

**Coverage:** All 5 databases combined

#### Examples

**Example 1: Comprehensive Search**
```bash
lixplore -A -q "COVID-19" -m 50 -D
```
Search all sources and remove duplicates.

**Example 2: All Sources with Sorting**
```bash
lixplore -A -q "climate change" -m 100 -D --sort newest
```
Get latest research across all databases.

**Example 3: All Sources Export**
```bash
lixplore -A -q "artificial intelligence" -m 200 -D -X xlsx
```
Comprehensive AI literature review across all sources.

**Example 4: All Sources with Statistics**
```bash
lixplore -A -q "cancer immunotherapy" -m 150 -D --stat
```
Analyze publication patterns across all databases.

**Example 5: All Sources with Selection**
```bash
lixplore -A -q "genetics" -m 300 -D --sort newest -S first:50 -X enw
```
Get top 50 latest genetics papers from all sources.

#### Tips
- **ALWAYS use `-D` flag** to remove duplicates!
- Best for comprehensive literature reviews
- Provides broader coverage than any single source
- Good for discovering research across disciplines

#### Warnings
- Much slower than single source (5x API calls)
- Will have many duplicates without `-D` flag
- Results can be overwhelming without sorting/selection
- API rate limits may apply

#### Related Flags
- [`-D, --deduplicate`](filter-flags.md#deduplicate) - **ESSENTIAL** with `-A`
- [`--sort`](filter-flags.md#sort) - Organize combined results
- [`-S, --select`](export-flags.md#select) - Export subset

---

### `-s, --sources`

**Description:** Search specific combination of sources using shorthand codes.

**Syntax:**
```bash
lixplore -s CODES -q "QUERY" [OPTIONS]
lixplore --sources CODES -q "QUERY" [OPTIONS]
```

**Type:** String value

**Default:** None

**Source Codes:**
- `P` = PubMed
- `C` = Crossref
- `J` = DOAJ
- `E` = EuropePMC
- `X` = arXiv
- `A` = All sources

#### Examples

**Example 1: PubMed + arXiv**
```bash
lixplore -s PX -q "machine learning healthcare" -m 30 -D
```
Search biomedical and CS sources for ML in healthcare.

**Example 2: PubMed + Crossref + EuropePMC**
```bash
lixplore -s PCE -q "gene therapy" -m 40 -D --sort newest
```
Comprehensive biomedical search across three databases.

**Example 3: DOAJ + arXiv**
```bash
lixplore -s JX -q "open source software" -m 25 --download-pdf
```
Search open access sources and download PDFs.

**Example 4: All Except arXiv**
```bash
lixplore -s PCJE -q "clinical trials" -m 50 -D
```
Search all sources except preprints.

**Example 5: Single Source (Alternative Syntax)**
```bash
lixplore -s P -q "diabetes" -m 20
# Same as: lixplore -P -q "diabetes" -m 20
```

#### Tips
- More concise than multiple individual flags
- Easy to remember shorthand codes
- Can combine any sources you need
- Order doesn't matter (PX = XP)

#### Warnings
- **Always use `-D`** when combining sources
- Invalid codes are silently ignored
- `A` code overrides other codes (searches all)

#### Related Flags
- [`-D, --deduplicate`](filter-flags.md#deduplicate) - Remove duplicates
- [`--sort`](filter-flags.md#sort) - Organize results
- All individual source flags above

---

### `--custom-api`

**Description:** Use custom-configured API source (Springer, BASE, IEEE, etc.).

**Syntax:**
```bash
lixplore --custom-api NAME -q "QUERY" [OPTIONS]
```

**Type:** String value

**Default:** None

**Prerequisites:** API must be configured in `~/.lixplore/custom_apis.json`

#### Examples

**Example 1: Springer API Search**
```bash
lixplore --custom-api springer -q "nanotechnology" -m 20
```
Search Springer database (requires API key).

**Example 2: BASE (Bielefeld Academic Search Engine)**
```bash
lixplore --custom-api base -q "open access" -m 30
```
Search BASE repository for open access content.

**Example 3: Custom API with Export**
```bash
lixplore --custom-api ieee -q "robotics" -m 25 -X bibtex
```
Search IEEE and export to BibTeX.

**Example 4: Combined Custom + Standard Sources**
```bash
# Note: Cannot combine with -s flag, use separately
lixplore -P -q "query" -m 20 -X csv
lixplore --custom-api springer -q "query" -m 20 -X csv
```

**Example 5: List Available Custom APIs**
```bash
lixplore --list-custom-apis
```

#### Setup Instructions

**1. Create API Examples:**
```bash
lixplore --create-api-examples
```

**2. Configure API (edit `~/.lixplore/custom_apis.json`):**
```json
{
  "springer": {
    "name": "Springer",
    "base_url": "https://api.springernature.com/meta/v2/json",
    "api_key_param": "api_key",
    "query_param": "q",
    "limit_param": "p",
    "requires_auth": true
  }
}
```

**3. Add API Key:**
```json
{
  "springer": {
    ...
    "api_key": "YOUR_API_KEY_HERE"
  }
}
```

#### Tips
- Extend Lixplore to ANY REST API
- No code modification needed
- Great for institutional subscriptions
- Can combine with standard sources (separate searches)

#### Warnings
- Requires valid API key for most services
- Configuration format must match spec
- Cannot use with `-s` or `-A` flags in same command
- API rate limits may apply

#### Related Flags
- [`--list-custom-apis`](utility-flags.md#list-custom-apis) - Show configured APIs
- [`--create-api-examples`](utility-flags.md#create-api-examples) - Setup templates

---

## Source Comparison

### Coverage by Discipline

| Source | Biomedical | Physical Sciences | Social Sciences | Computer Science | Open Access |
|--------|------------|-------------------|-----------------|------------------|-------------|
| PubMed | ★★★★★ | ★☆☆☆☆ | ★★☆☆☆ | ★☆☆☆☆ | ★★★☆☆ |
| Crossref | ★★★★☆ | ★★★★★ | ★★★★★ | ★★★★★ | ★★★☆☆ |
| DOAJ | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | ★★★★★ |
| EuropePMC | ★★★★★ | ★☆☆☆☆ | ★★☆☆☆ | ★☆☆☆☆ | ★★★★☆ |
| arXiv | ★☆☆☆☆ | ★★★★★ | ★☆☆☆☆ | ★★★★★ | ★★★★★ |

### Feature Comparison

| Feature | PubMed | Crossref | DOAJ | EuropePMC | arXiv |
|---------|--------|----------|------|-----------|-------|
| **Size** | 35M+ | 140M+ | 8M+ | 42M+ | 2.3M+ |
| **Full Text** | Some | No | Yes | Some | Yes |
| **Peer Review** | Yes | Yes | Yes | Yes | No |
| **Latest Research** | Medium | High | Medium | Medium | Highest |
| **Metadata Quality** | High | Highest | Medium | High | Medium |
| **API Speed** | Fast | Fast | Medium | Medium | Fast |

### Recommended Combinations

**Biomedical Research:**
```bash
lixplore -s PE -q "query" -m 50 -D
# PubMed + EuropePMC
```

**Computer Science:**
```bash
lixplore -s XC -q "query" -m 50 -D
# arXiv + Crossref
```

**Open Access Only:**
```bash
lixplore -s JX -q "query" -m 50 -D
# DOAJ + arXiv
```

**Comprehensive Review:**
```bash
lixplore -A -q "query" -m 100 -D
# All sources
```

**Latest Peer-Reviewed:**
```bash
lixplore -s PC -q "query" -m 50 -D --sort newest
# PubMed + Crossref
```

---

## Best Practices

### 1. Choose Sources Based on Discipline

**Biomedical/Health:**
```bash
lixplore -P -q "clinical trial diabetes" -m 30
```

**Physics/Math:**
```bash
lixplore -x -q "quantum entanglement" -m 30
```

**Computer Science:**
```bash
lixplore -x -q "neural networks" -m 30
```

**Multi-Disciplinary:**
```bash
lixplore -C -q "artificial intelligence" -m 30
```

### 2. Always Deduplicate Multi-Source Searches

```bash
# CORRECT
lixplore -A -q "query" -m 50 -D

# WRONG (will have many duplicates)
lixplore -A -q "query" -m 50
```

### 3. Use Specific Combinations

```bash
# Instead of -A (all sources)
lixplore -A -q "query" -m 50 -D

# Use targeted combination
lixplore -s PE -q "query" -m 50 -D  # Just biomedical
```

### 4. Combine with Sorting

```bash
lixplore -A -q "COVID-19" -m 100 -D --sort newest
```

### 5. Export Source Information

```bash
lixplore -A -q "query" -m 50 -D -X csv --export-fields title authors year source
```

---

## Troubleshooting

### Problem: No results from specific source

**Solution 1: Try different query format**
```bash
# Instead of exact phrase
lixplore -P -q "machine learning"

# Try individual terms
lixplore -P -q "machine OR learning"
```

**Solution 2: Check source availability**
```bash
# Test with known query
lixplore -P -q "cancer" -m 5
```

### Problem: Too many duplicates

**Solution: Use deduplication**
```bash
lixplore -A -q "query" -m 50 -D strict
```

### Problem: Custom API not working

**Solution: Verify configuration**
```bash
# List configured APIs
lixplore --list-custom-apis

# Check configuration file
cat ~/.lixplore/custom_apis.json
```

### Problem: Slow search across all sources

**Solution: Use targeted combination**
```bash
# Instead of all sources
lixplore -A -q "query" -m 100

# Use specific sources
lixplore -s PC -q "query" -m 50
```

---

## Related Documentation

- [Search Flags](search-flags.md) - Query syntax and search parameters
- [Filter Flags](filter-flags.md) - Deduplication and sorting
- [Export Flags](export-flags.md) - Export and download options
- [Utility Flags](utility-flags.md) - API configuration and management

---

**Last Updated:** 2024-12-28
**Lixplore Version:** 2.0+
