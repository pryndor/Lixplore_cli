# Lixplore Automation & Cron Job Guide

## Overview
Lixplore is perfect for automation - daily monitoring, batch processing, and scheduled searches.

---

## 1. Cron Job Examples

### Daily Literature Monitoring
Monitor new publications on specific topics every day.

#### Example 1: Daily COVID-19 Research Monitor
```bash
# Add to crontab: crontab -e
# Runs every day at 9 AM
0 9 * * * /home/user/.pyenv/versions/lixplore-env/bin/lixplore -P -q "COVID-19 treatment 2025" -m 20 -X csv -o /home/user/covid_papers_$(date +\%Y\%m\%d).csv

# With deduplication and sorting
0 9 * * * /home/user/.pyenv/versions/lixplore-env/bin/lixplore -A -q "COVID-19" -m 50 -D --sort newest -S first:10 -X xlsx -o /home/user/reports/covid_latest.xlsx
```

#### Example 2: Weekly Research Digest
```bash
# Runs every Monday at 8 AM
0 8 * * 1 /home/user/.pyenv/versions/lixplore-env/bin/lixplore -P -q "machine learning" -m 100 --sort newest -X bibtex -o /home/user/weekly/ml_$(date +\%Y_week\%U).bib
```

#### Example 3: Multi-Topic Daily Monitoring
```bash
# Create a shell script: ~/scripts/daily_literature.sh
#!/bin/bash

LIXPLORE="/home/user/.pyenv/versions/lixplore-env/bin/lixplore"
DATE=$(date +%Y%m%d)
OUTPUT_DIR="/home/user/research/daily"

# Topic 1: AI Research
$LIXPLORE -A -q "artificial intelligence" -m 50 -D -X csv -o "$OUTPUT_DIR/ai_$DATE.csv"

# Topic 2: Cancer Treatment
$LIXPLORE -P -q "cancer immunotherapy" -m 30 -X xlsx -o "$OUTPUT_DIR/cancer_$DATE.xlsx"

# Topic 3: Climate Science
$LIXPLORE -s PX -q "climate change" -m 40 -D -X json -o "$OUTPUT_DIR/climate_$DATE.json"

echo "Daily literature update complete: $DATE" | mail -s "Lixplore Daily Report" user@example.com
```

```bash
# Add to crontab
0 7 * * * /home/user/scripts/daily_literature.sh
```

---

## 2. Automation Patterns

### Pattern 1: Search → Annotate → Export
```bash
# Search, annotate important ones, export annotated
lixplore -P -q "CRISPR therapy" -m 50 -X json -o results.json

# Later, annotate the important ones (manually or via script)
lixplore --annotate 5 --rating 5 --tags "important,cite"
lixplore --annotate 12 --rating 4 --tags "interesting"

# Export only annotated articles
lixplore --export-annotations markdown
```

### Pattern 2: Continuous Monitoring with Dedup
```bash
# Day 1: Search and save
lixplore -A -q "quantum computing" -m 100 -D -X csv -o quantum_baseline.csv

# Day 2+: New results only (use date filter)
lixplore -A -q "quantum computing" -d 2025-01-01 2025-01-31 -m 100 -D -X csv -o quantum_january.csv
```

### Pattern 3: Batch Export Multiple Formats
```bash
# Export in all formats for different tools
lixplore -P -q "neuroscience" -m 100 -X csv,bibtex,ris,xlsx --zip
# Creates: results.zip containing all formats
```

### Pattern 4: Profile-Based Automation
```bash
# Create a profile once
lixplore -P -q "test" -X bibtex --sort newest -S first:20 --save-profile nature_style

# Reuse in automation
lixplore -P -q "stem cells" -m 100 --load-profile nature_style
lixplore -P -q "gene therapy" -m 100 --load-profile nature_style
```

---

## 3. File Storage Locations

### Automatic Organization
All files are automatically organized:

```
~/
├── Lixplore_PDFs/              # Downloaded PDFs
│   ├── pubmed/
│   ├── arxiv/
│   └── scihub/
│
├── .lixplore_cache.json        # Search cache (7 days)
├── .lixplore_annotations.json  # Annotations database
│
├── .lixplore/                  # Configuration
│   ├── profiles.json           # Export profiles
│   ├── templates/              # Custom templates
│   └── apis/                   # Custom API configs
│
└── exports/                    # All exports
    ├── csv/
    ├── excel/
    ├── json/
    ├── bibtex/
    ├── ris/
    ├── endnote_tagged/
    ├── endnote_xml/
    ├── xml/
    └── citations/
```

---

## 4. PDF Download Automation

### Automatic PDF Downloads
```bash
# Download PDFs for open access articles
lixplore -P -q "open access" -m 20 --download-pdf

# Download specific articles
lixplore -P -q "research" -m 50 --download-pdf --pdf-numbers 1 3 5 8

# With SciHub fallback (configure first)
lixplore --set-scihub-mirror https://sci-hub.se
lixplore -P -q "article" -m 20 --download-pdf --use-scihub
```

### Show PDF Links (No Download)
```bash
# Just show clickable links in terminal
lixplore -x -q "machine learning" -m 10 --show-pdf-links

# In modern terminals (iTerm2, GNOME Terminal, Windows Terminal)
# Links are clickable - click to open in browser!
```

---

## 5. Cron Job Best Practices

### 1. Use Full Paths
```bash
# ✗ BAD
0 9 * * * lixplore -P -q "test" -X csv

# ✓ GOOD
0 9 * * * /home/user/.pyenv/versions/lixplore-env/bin/lixplore -P -q "test" -X csv -o /full/path/output.csv
```

### 2. Log Output
```bash
# Redirect output to log file
0 9 * * * /path/to/lixplore -P -q "topic" -m 50 -X csv >> /home/user/logs/lixplore.log 2>&1
```

### 3. Email Results
```bash
# Email when done
0 9 * * * /path/to/lixplore -P -q "topic" -m 50 -X csv && echo "Search complete" | mail -s "Lixplore Done" user@example.com
```

### 4. Error Handling
```bash
#!/bin/bash
# Script: ~/scripts/safe_lixplore.sh

LIXPLORE="/path/to/lixplore"
OUTPUT="/home/user/results/daily_$(date +%Y%m%d).csv"

if $LIXPLORE -P -q "research topic" -m 50 -X csv -o "$OUTPUT" 2>&1; then
    echo "Success: $OUTPUT created"
else
    echo "Error: Lixplore failed" | mail -s "Lixplore Error" user@example.com
    exit 1
fi
```

---

## 6. Advanced Automation Examples

### Research Assistant Bot
```bash
#!/bin/bash
# Daily research assistant

TOPICS=("AI" "machine learning" "deep learning" "neural networks")
DATE=$(date +%Y%m%d)
LIXPLORE="/path/to/lixplore"

for topic in "${TOPICS[@]}"; do
    echo "Searching: $topic"
    $LIXPLORE -A -q "$topic" -m 50 -D --sort newest -S first:10 \
              -X csv -o "results/${topic// /_}_$DATE.csv"
done

# Combine all results
cat results/*_$DATE.csv > combined_$DATE.csv

# Email summary
echo "Daily research update complete" | mail -s "Research Bot Report" user@example.com
```

### Literature Review Pipeline
```bash
#!/bin/bash
# Comprehensive literature review automation

# 1. Search multiple sources
lixplore -A -q "systematic review cancer treatment" -m 200 -D --enrich -X json -o phase1.json

# 2. Export for different tools
lixplore --load-profile my_review -X bibtex,ris,xlsx --zip

# 3. Export high-quality subset
lixplore -P -q "cancer treatment" -m 200 --sort newest -S first:50 -X xlsx -o top50.xlsx

# 4. Generate statistics
lixplore -P -q "cancer treatment" -m 200 --stat --stat-top 20 > statistics.txt
```

---

## 7. Integration with Other Tools

### Pipe to jq (JSON processing)
```bash
# Extract titles only
lixplore -P -q "AI" -m 20 -X json | jq '.[] | .title'

# Filter by year
lixplore -P -q "research" -m 100 -X json | jq '.[] | select(.year >= 2023)'
```

### Pipe to csvkit
```bash
# Search and analyze with csvkit
lixplore -P -q "data science" -m 100 -X csv -o results.csv
csvstat results.csv
csvcut -c title,year,journal results.csv | csvlook
```

### Integration with Zotero
```bash
# Automatic Zotero import (requires configuration)
lixplore --configure-zotero YOUR_API_KEY YOUR_USER_ID
lixplore -P -q "research" -m 50 --add-to-zotero --zotero-collection COLLECTION_KEY
```

---

## 8. Cron Schedule Examples

```bash
# Every day at 9 AM
0 9 * * * /path/to/command

# Every Monday at 8 AM
0 8 * * 1 /path/to/command

# Every hour
0 * * * * /path/to/command

# Every 6 hours
0 */6 * * * /path/to/command

# First day of month at midnight
0 0 1 * * /path/to/command

# Every weekday at 7 AM
0 7 * * 1-5 /path/to/command
```

---

## Summary

Lixplore is fully automation-ready:
- ✓ All operations via CLI (no GUI needed)
- ✓ Automatic file organization
- ✓ Cache management
- ✓ Error handling
- ✓ Multiple export formats
- ✓ Profile/template system
- ✓ Perfect for cron jobs

Set it and forget it!
