# Tool Integration Examples

> **Integrate Lixplore with other research tools**

## Table of Contents

- [Command-Line Tools](#command-line-tools)
- [Reference Managers](#reference-managers)
- [Spreadsheet Tools](#spreadsheet-tools)
- [LaTeX Integration](#latex-integration)
- [Cloud Services](#cloud-services)
- [Programming Languages](#programming-languages)

---

## Command-Line Tools

### jq (JSON Processing)

**Extract specific fields from JSON export:**

```bash
# Export to JSON
lixplore -P -q "cancer" -m 50 -X json -o results.json

# Extract titles only
jq '.[] | .title' exports/json/results.json

# Extract titles and DOIs
jq '.[] | {title: .title, doi: .doi}' exports/json/results.json

# Filter by year
jq '.[] | select(.year >= 2020)' exports/json/results.json

# Count by source
jq 'group_by(.source) | map({source: .[0].source, count: length})' exports/json/results.json
```

### csvkit (CSV Processing)

**Advanced CSV manipulation:**

```bash
# Export to CSV
lixplore -P -q "diabetes" -m 100 -X csv -o results.csv

# View first 10 rows
csvlook exports/csv/results.csv | head -20

# Filter by year
csvgrep -c year -r "202[0-4]" exports/csv/results.csv

# Sort by year
csvsort -c year -r exports/csv/results.csv > sorted_results.csv

# Get statistics
csvstat exports/csv/results.csv

# Convert to JSON
csvjson exports/csv/results.csv > results.json

# Merge multiple CSV files
csvstack file1.csv file2.csv file3.csv > merged.csv
```

### grep/awk/sed (Text Processing)

**Search and filter results:**

```bash
# Export to CSV
lixplore -P -q "research" -m 200 -X csv -o results.csv

# Find articles mentioning "methodology"
grep -i "methodology" exports/csv/results.csv

# Extract DOIs only
awk -F',' '{print $5}' exports/csv/results.csv | tail -n +2

# Replace text in CSV
sed 's/old_text/new_text/g' exports/csv/results.csv > modified.csv

# Count articles per year
awk -F',' '{print $4}' exports/csv/results.csv | tail -n +2 | sort | uniq -c
```

### pandoc (Document Conversion)

**Convert between formats:**

```bash
# Export annotations to Markdown
lixplore --export-annotations markdown

# Convert Markdown to PDF
pandoc lixplore_annotations_*.md -o annotations.pdf

# Convert to Word
pandoc lixplore_annotations_*.md -o annotations.docx

# Convert to HTML
pandoc lixplore_annotations_*.md -o annotations.html

# Custom styling
pandoc lixplore_annotations_*.md --css=style.css -o annotations.html
```

---

## Reference Managers

### Zotero Integration

**Direct API integration:**

```bash
# Setup (one-time)
lixplore --configure-zotero YOUR_API_KEY YOUR_USER_ID

# View collections
lixplore --show-zotero-collections

# Add to library
lixplore -P -q "research topic" -m 50 --add-to-zotero

# Add to specific collection
lixplore -P -q "chapter 2 topic" -m 30 --add-to-zotero --zotero-collection ABC123

# Workflow: Search → Annotate → Add to Zotero
lixplore -P -q "important topic" -m 20 -a
lixplore --annotate 3 --rating 5 --tags "important"
lixplore --filter-annotations "min_rating=4"
lixplore -P -q "important topic" -m 20 -S 3 --add-to-zotero
```

### Mendeley Integration

**Export RIS format:**

```bash
# Export for Mendeley
lixplore -P -q "research" -m 50 --export-for-mendeley

# Or manual RIS export
lixplore -P -q "research" -m 50 -X ris -o mendeley_import.ris

# Import to Mendeley Desktop:
# File → Import → RIS → Select file
```

### EndNote Integration

**EndNote Tagged format:**

```bash
# Export to EndNote Tagged (.enw) - RECOMMENDED
lixplore -P -q "neuroscience" -m 100 -X enw -o endnote_refs.enw

# Import to EndNote:
# File → Import → File → Select .enw file → Import Option: EndNote Tagged Import

# Or EndNote XML
lixplore -P -q "neuroscience" -m 100 -X endnote -o endnote_refs.xml

# Batch export by topic
lixplore -P -q "topic1" -m 50 -X enw -o topic1.enw
lixplore -P -q "topic2" -m 50 -X enw -o topic2.enw
lixplore -P -q "topic3" -m 50 -X enw -o topic3.enw
```

---

## Spreadsheet Tools

### Excel Integration

**Advanced Excel workflows:**

```bash
# Export with all fields
lixplore -P -q "research" -m 100 -X xlsx -o results.xlsx

# Open in Excel and use:
# - Filters (Data → Filter)
# - Pivot tables (Insert → PivotTable)
# - Conditional formatting
# - Charts/graphs

# Export multiple formats for Excel analysis
lixplore -P -q "topic" -m 200 -X xlsx,csv -o analysis

# In Excel:
# 1. Open analysis.xlsx
# 2. Create pivot table by year/journal
# 3. Generate charts
# 4. Apply conditional formatting for ratings
```

### Google Sheets Integration

**Cloud-based collaboration:**

```bash
# Export to CSV
lixplore -P -q "collaboration topic" -m 150 -X csv -o team_refs.csv

# Upload to Google Sheets:
# 1. Open Google Sheets
# 2. File → Import → Upload → Select team_refs.csv
# 3. Share with team

# Or use Google Drive CLI (gdrive)
lixplore -P -q "topic" -m 100 -X csv -o results.csv
gdrive upload exports/csv/results.csv
```

### LibreOffice Calc Integration

**Open-source spreadsheet:**

```bash
# Export to CSV or Excel
lixplore -P -q "research" -m 100 -X xlsx -o results.xlsx

# Open in LibreOffice Calc:
libreoffice --calc exports/excel/results.xlsx

# Or from command line
lixplore -P -q "topic" -m 50 -X csv | libreoffice --calc
```

---

## LaTeX Integration

### BibTeX Workflow

**Complete LaTeX bibliography:**

```bash
# Create BibTeX file
lixplore -C -q "machine learning" -m 100 --enrich -X bibtex -o ml_refs.bib

# In LaTeX document:
\bibliography{ml_refs}
\bibliographystyle{plain}

# Compile
pdflatex document.tex
bibtex document
pdflatex document.tex
pdflatex document.tex
```

### Multiple Bibliography Files

**Organize by chapter:**

```bash
# Chapter-specific bibliographies
lixplore -P -q "chapter 1 topic" -m 50 --enrich -X bibtex -o chapter1.bib
lixplore -P -q "chapter 2 topic" -m 50 --enrich -X bibtex -o chapter2.bib
lixplore -P -q "chapter 3 topic" -m 50 --enrich -X bibtex -o chapter3.bib

# In LaTeX:
\bibliography{chapter1,chapter2,chapter3}
```

### BibLaTeX Integration

**Modern BibTeX:**

```bash
# Export with complete metadata
lixplore -A -q "topic" -m 200 -D --enrich -X bibtex -o refs.bib

# In LaTeX (with biblatex):
\usepackage[backend=biber,style=authoryear]{biblatex}
\addbibresource{refs.bib}
\printbibliography
```

---

## Cloud Services

### Dropbox Integration

**Sync exports to cloud:**

```bash
# Create symlink to Dropbox
ln -s ~/Dropbox/Research/Lixplore_Exports ~/exports_link

# Export directly to Dropbox
lixplore -P -q "topic" -m 50 -X xlsx -o ~/Dropbox/Research/results.xlsx

# Automatic sync workflow
lixplore -P -q "weekly update" -m 30 -X xlsx -o ~/Dropbox/Research/weekly_$(date +%Y%m%d).xlsx
```

### Google Drive Integration

**Using gdrive CLI:**

```bash
# Install gdrive
# https://github.com/prasmussen/gdrive

# Upload export
lixplore -P -q "research" -m 100 -X xlsx -o results.xlsx
gdrive upload exports/excel/results.xlsx

# Sync folder
gdrive sync upload ~/exports ~/Research/Lixplore
```

### OneDrive Integration

**Using onedrive-d:**

```bash
# Sync exports to OneDrive
ln -s ~/OneDrive/Research ~/lixplore_sync

# Export to OneDrive
lixplore -P -q "topic" -m 50 -X xlsx -o ~/OneDrive/Research/results.xlsx
```

---

## Programming Languages

### Python Integration

**Process Lixplore data in Python:**

```python
#!/usr/bin/env python3
import json
import pandas as pd
import subprocess

# Run Lixplore and capture JSON
result = subprocess.run([
    'lixplore', '-P', '-q', 'machine learning',
    '-m', '100', '-X', 'json', '-o', 'results.json'
], capture_output=True)

# Load JSON results
with open('exports/json/results.json') as f:
    data = json.load(f)

# Convert to pandas DataFrame
df = pd.DataFrame(data)

# Analysis
print(f"Total articles: {len(df)}")
print(f"\nArticles by year:")
print(df['year'].value_counts().sort_index())

# Filter and export
recent = df[df['year'] >= 2020]
recent.to_csv('recent_papers.csv', index=False)

# Visualization
import matplotlib.pyplot as plt

df['year'].value_counts().sort_index().plot(kind='bar')
plt.title('Publications by Year')
plt.xlabel('Year')
plt.ylabel('Count')
plt.savefig('pub_trends.png')
```

### R Integration

**Statistical analysis:**

```r
# Run Lixplore from R
system("lixplore -P -q 'statistics' -m 200 -X csv -o results.csv")

# Load CSV
library(tidyverse)
data <- read_csv("exports/csv/results.csv")

# Analysis
summary(data)

# Count by year
year_counts <- data %>%
  count(year) %>%
  arrange(year)

# Visualization
ggplot(year_counts, aes(x=year, y=n)) +
  geom_line() +
  geom_point() +
  labs(title="Publications Over Time",
       x="Year", y="Number of Publications")
```

### Bash Scripting

**Automated workflows:**

```bash
#!/bin/bash
# daily_update.sh - Daily literature monitoring

DATE=$(date +%Y%m%d)
QUERY="machine learning healthcare"

# Search
lixplore -A -q "$QUERY" \
  -d $(date -d '1 day ago' +%Y-%m-%d) $(date +%Y-%m-%d) \
  -m 50 \
  -D \
  -X xlsx \
  -o "daily_update_${DATE}.xlsx"

# Send email notification
if [ $? -eq 0 ]; then
    echo "Daily update completed: $DATE" | mail -s "Lixplore Daily Update" user@example.com
fi
```

---

## Workflow Automation

### Make Integration

**Makefile for reproducible research:**

```makefile
# Makefile for literature review

.PHONY: all search export analyze clean

all: search export analyze

search:
    lixplore -A -q "research topic" -m 500 -D -X json -o raw_data.json

export: search
    lixplore -A -q "research topic" -m 500 -D --enrich -X xlsx,bibtex -o refs

analyze: export
    python analyze_results.py
    Rscript visualize.R

clean:
    rm -f exports/*/*.csv exports/*/*.xlsx exports/*/*.json
```

### Git Integration

**Version control:**

```bash
# Initialize repo
git init literature_review
cd literature_review

# Create .gitignore
cat > .gitignore << EOF
exports/*/
*.pdf
.lixplore_cache.json
EOF

# Track searches and annotations
git add .lixplore_history.json
git add .lixplore_annotations.json
git commit -m "Initial literature search"

# Track exported bibliographies
git add refs.bib refs.xlsx
git commit -m "Added bibliography for Chapter 2"
```

### Docker Integration

**Containerized workflow:**

```dockerfile
# Dockerfile
FROM python:3.10-slim

RUN pip install lixplore

WORKDIR /workspace

CMD ["lixplore", "--help"]
```

```bash
# Build
docker build -t lixplore .

# Run
docker run -v $(pwd)/exports:/workspace/exports lixplore \
  lixplore -P -q "docker research" -m 50 -X csv
```

---

**Last Updated:** 2024-12-28
