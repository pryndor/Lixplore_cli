# Export & Output Flags

> **Complete documentation for all export and output flags**

## Table of Contents

- [Export Formats](#export-formats)
- [Selection & Fields](#selection--fields)
- [Profiles & Templates](#profiles--templates)
- [PDF Downloads](#pdf-downloads)
- [Reference Managers](#reference-managers)

---

## Export Formats

### `-X, --export`

**Description:** Export results in specified format(s).

**Formats:** csv, xlsx, json, bibtex, ris, enw, endnote, xml

**Syntax:**
```bash
lixplore -q "QUERY" -X FORMAT [-o FILE]
lixplore -q "QUERY" -X FORMAT1,FORMAT2,FORMAT3  # Multiple
```

#### Examples

**Example 1: CSV Export**
```bash
lixplore -P -q "cancer" -m 30 -X csv
```

**Example 2: Excel with Custom Name**
```bash
lixplore -P -q "diabetes" -m 50 -X xlsx -o my_research.xlsx
```

**Example 3: BibTeX for LaTeX**
```bash
lixplore -C -q "quantum physics" -m 40 -X bibtex -o refs.bib
```

**Example 4: EndNote Tagged**
```bash
lixplore -P -q "neuroscience" -m 60 -X enw -o brain.enw
```

**Example 5: Multiple Formats**
```bash
lixplore -A -q "AI" -m 100 -D -X csv,ris,bibtex
```

**Export Locations:**
- CSV: `exports/csv/`
- Excel: `exports/excel/`
- JSON: `exports/json/`
- BibTeX: `exports/bibtex/`
- RIS: `exports/ris/`
- EndNote: `exports/endnote_tagged/`

---

### `-o, --output`

**Description:** Custom output filename.

**Syntax:**
```bash
lixplore -q "QUERY" -X FORMAT -o FILENAME
```

#### Examples

**Example 1: Named Export**
```bash
lixplore -P -q "COVID-19" -m 50 -X xlsx -o covid_research.xlsx
```

**Example 2: Multi-Format Base Name**
```bash
lixplore -A -q "genetics" -m 100 -D -X csv,ris -o genetics_papers
# Creates: genetics_papers.csv, genetics_papers.ris
```

---

### `--zip`

**Description:** Compress exported files to ZIP format.

**Syntax:**
```bash
lixplore -q "QUERY" -X FORMAT --zip
```

#### Examples

**Example 1: Compressed CSV**
```bash
lixplore -P -q "cancer" -m 200 -X csv --zip
```

**Example 2: Multi-Format ZIP**
```bash
lixplore -A -q "research" -m 300 -D -X csv,ris,bibtex --zip
```

---

## Selection & Fields

### `-S, --select`

**Description:** Select specific articles to export.

**Patterns:** numbers (1 3 5), ranges (1-10), keywords (odd, even, first:N, last:N)

**Syntax:**
```bash
lixplore -q "QUERY" -S SELECTION -X FORMAT
```

#### Examples

**Example 1: Specific Numbers**
```bash
lixplore -P -q "cancer" -m 50 -S 1 3 5 7 -X xlsx
```

**Example 2: Range**
```bash
lixplore -P -q "diabetes" -m 100 -S 10-20 -X csv
```

**Example 3: Odd Articles**
```bash
lixplore -P -q "genetics" -m 80 -S odd -X enw
```

**Example 4: Even Articles**
```bash
lixplore -A -q "AI" -m 100 -D -S even -X bibtex
```

**Example 5: First N**
```bash
lixplore -A -q "climate" -m 200 -D --sort newest -S first:30 -X xlsx
```

**Example 6: Last N**
```bash
lixplore -P -q "history" -m 100 --sort oldest -S last:10 -X csv
```

**Example 7: Top Results**
```bash
lixplore -P -q "COVID-19" -m 100 -S top:25 -X enw
```

**Example 8: Mixed Patterns**
```bash
lixplore -P -q "research" -m 100 -S 1 3 5-10 odd -X xlsx
```

---

### `--export-fields`

**Description:** Select specific metadata fields to export.

**Fields:** title, authors, abstract, journal, year, doi, url, source

**Syntax:**
```bash
lixplore -q "QUERY" -X FORMAT --export-fields FIELD1 FIELD2...
```

#### Examples

**Example 1: Essential Fields Only**
```bash
lixplore -P -q "cancer" -m 50 -X csv --export-fields title authors year doi
```

**Example 2: Citation Fields**
```bash
lixplore -C -q "research" -m 30 -X xlsx --export-fields title authors journal year
```

**Example 3: Minimal Export**
```bash
lixplore -P -q "diabetes" -m 100 -X csv --export-fields title doi
```

---

## Profiles & Templates

### `--save-profile`

**Description:** Save current export settings as reusable profile.

**Syntax:**
```bash
lixplore -q "QUERY" -X FORMAT [OPTIONS] --save-profile NAME
```

#### Examples

**Example 1: Save Export Profile**
```bash
lixplore -P -q "test" -m 10 -X xlsx --export-fields title authors year doi --save-profile my_workflow
```

**Example 2: Complex Profile**
```bash
lixplore -A -q "test" -m 50 -D --sort newest -X csv,ris --save-profile comprehensive_search
```

---

### `--load-profile`

**Description:** Load previously saved export profile.

**Syntax:**
```bash
lixplore -q "QUERY" --load-profile NAME
```

#### Examples

**Example 1: Use Saved Profile**
```bash
lixplore -P -q "new research" --load-profile my_workflow
```

---

### `--list-profiles`

**Description:** List all saved export profiles.

**Syntax:**
```bash
lixplore --list-profiles
```

---

### `--delete-profile`

**Description:** Delete saved export profile.

**Syntax:**
```bash
lixplore --delete-profile NAME
```

---

### `--template`

**Description:** Use predefined export template.

**Templates:** nature, science, ieee

**Syntax:**
```bash
lixplore -q "QUERY" --template NAME
```

#### Examples

**Example 1: Nature Format**
```bash
lixplore -P -q "biology" -m 30 --template nature
```

**Example 2: IEEE Format**
```bash
lixplore -x -q "engineering" -m 40 --template ieee
```

---

### `--list-templates`

**Description:** List available export templates.

**Syntax:**
```bash
lixplore --list-templates
```

---

## Citations

### `-c, --citations`

**Description:** Export as formatted citations.

**Styles:** apa, mla, chicago, ieee

**Syntax:**
```bash
lixplore -q "QUERY" -c STYLE
```

#### Examples

**Example 1: APA Style**
```bash
lixplore -P -q "psychology" -m 20 -c apa
```

**Example 2: MLA Style**
```bash
lixplore -P -q "literature" -m 15 -c mla
```

**Example 3: Chicago Style**
```bash
lixplore -C -q "history" -m 25 -c chicago
```

**Example 4: IEEE Style**
```bash
lixplore -x -q "engineering" -m 30 -c ieee
```

---

## PDF Downloads

### `--download-pdf`

**Description:** Download full-text PDFs for search results.

**Sources:** PMC, arXiv, DOI resolution, SciHub (optional)

**Syntax:**
```bash
lixplore -q "QUERY" --download-pdf [--use-scihub]
```

#### Examples

**Example 1: Download All PDFs**
```bash
lixplore -x -q "machine learning" -m 10 --download-pdf
```

**Example 2: Specific Articles**
```bash
lixplore -J -q "open access" -m 20 --download-pdf --pdf-numbers 1 3 5
```

**Example 3: With SciHub Fallback**
```bash
lixplore -P -q "cancer" -m 15 --download-pdf --use-scihub
```

**PDF Directory:** `~/Lixplore_PDFs/`

---

### `--pdf-numbers`

**Description:** Download PDFs only for specific article numbers.

**Syntax:**
```bash
lixplore -q "QUERY" --download-pdf --pdf-numbers N1 N2 N3...
```

#### Examples

**Example 1: Selected PDFs**
```bash
lixplore -P -q "genetics" -m 30 --download-pdf --pdf-numbers 1 5 10 15
```

---

### `--use-scihub`

**Description:** Use SciHub as fallback for PDF downloads.

**Syntax:**
```bash
lixplore -q "QUERY" --download-pdf --use-scihub
```

**Setup Required:**
```bash
lixplore --set-scihub-mirror https://sci-hub.se
```

---

### `--set-scihub-mirror`

**Description:** Configure SciHub mirror URL.

**Syntax:**
```bash
lixplore --set-scihub-mirror URL
```

#### Example

```bash
lixplore --set-scihub-mirror https://sci-hub.se
```

---

### `--show-pdf-dir`

**Description:** Show PDF download directory location.

**Syntax:**
```bash
lixplore --show-pdf-dir
```

---

## Reference Managers

### `--add-to-zotero`

**Description:** Add search results to Zotero library.

**Prerequisites:** Zotero API configuration

**Syntax:**
```bash
lixplore -q "QUERY" --add-to-zotero [--zotero-collection KEY]
```

#### Examples

**Example 1: Add to Library**
```bash
lixplore -P -q "genetics" -m 20 --add-to-zotero
```

**Example 2: Add to Collection**
```bash
lixplore -P -q "cancer" -m 30 --add-to-zotero --zotero-collection ABC123DEF
```

---

### `--configure-zotero`

**Description:** Configure Zotero API access.

**Syntax:**
```bash
lixplore --configure-zotero API_KEY USER_ID
```

#### Setup

**Step 1: Get API Key**
- Visit: https://www.zotero.org/settings/keys
- Create new private key

**Step 2: Configure**
```bash
lixplore --configure-zotero YOUR_API_KEY YOUR_USER_ID
```

---

### `--show-zotero-collections`

**Description:** List Zotero collections with their keys.

**Syntax:**
```bash
lixplore --show-zotero-collections
```

---

### `--export-for-mendeley`

**Description:** Export results as RIS for Mendeley import.

**Syntax:**
```bash
lixplore -q "QUERY" --export-for-mendeley
```

#### Example

```bash
lixplore -P -q "biology" -m 50 --export-for-mendeley
```

**Import to Mendeley:**
1. Open Mendeley Desktop
2. File → Import → RIS file
3. Select exported file

---

## Best Practices

### 1. Enrich Before Export
```bash
lixplore -A -q "research" -m 100 -D --enrich -X bibtex
```

### 2. Use Selection for Large Sets
```bash
lixplore -P -q "cancer" -m 500 --sort newest -S first:50 -X xlsx
```

### 3. Multi-Format for Flexibility
```bash
lixplore -A -q "genetics" -m 100 -D -X csv,ris,bibtex
```

### 4. Save Profiles for Repeated Workflows
```bash
# Save once
lixplore -P -q "test" -X xlsx --export-fields title authors year --save-profile quick_export

# Reuse many times
lixplore -P -q "different query" --load-profile quick_export
```

### 5. Organize with Output Names
```bash
lixplore -P -q "COVID-19" -m 100 --sort newest -S first:30 -X xlsx -o covid_latest_30.xlsx
```

---

**Last Updated:** 2024-12-28
