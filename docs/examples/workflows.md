# Common Research Workflows

> **Step-by-step workflows for common research tasks**

## Table of Contents

- [Literature Review](#literature-review)
- [Systematic Review](#systematic-review)
- [Current Awareness](#current-awareness)
- [Bibliography Building](#bibliography-building)
- [Grant Writing](#grant-writing)
- [Thesis/Dissertation](#thesisdissertation)

---

## Literature Review

### Basic Literature Review

**Goal:** Comprehensive overview of a research topic

```bash
# Step 1: Broad search across all sources
lixplore -A -q "machine learning healthcare" -m 200 -D

# Step 2: Filter to recent research (last 5 years)
lixplore -A -q "machine learning healthcare" \
  -d 2020-01-01 2024-12-31 \
  -m 200 \
  -D

# Step 3: Sort by newest and review abstracts
lixplore -A -q "machine learning healthcare" \
  -d 2020-01-01 2024-12-31 \
  -m 200 \
  -D \
  --sort newest \
  -a

# Step 4: Annotate important papers
lixplore --annotate 3 --rating 5 --tags "foundational,must-cite" --priority high
lixplore --annotate 7 --rating 4 --tags "relevant,methodology"
lixplore --annotate 12 --rating 5 --tags "recent,important"

# Step 5: Export top 50 papers
lixplore -A -q "machine learning healthcare" \
  -d 2020-01-01 2024-12-31 \
  -m 200 \
  -D \
  --sort newest \
  -S first:50 \
  --enrich \
  -X xlsx,bibtex \
  -o ml_healthcare_review

# Step 6: Generate statistics
lixplore -A -q "machine learning healthcare" \
  -d 2020-01-01 2024-12-31 \
  -m 200 \
  -D \
  --stat \
  --stat-top 20

# Step 7: Export annotations
lixplore --filter-annotations "min_rating=4"
lixplore --export-annotations markdown
```

---

## Systematic Review

### PRISMA-Style Systematic Review

**Goal:** Rigorous, reproducible literature review

```bash
# IDENTIFICATION PHASE
# Step 1: Comprehensive multi-source search
lixplore -A -q "(diabetes OR 'diabetes mellitus') AND (treatment OR therapy)" \
  -m 1000 \
  -X csv \
  -o identification_all.csv

# Step 2: Save search parameters
lixplore -A -q "..." -m 1000 --save-profile systematic_diabetes

# SCREENING PHASE
# Step 3: Remove duplicates (strict)
lixplore -A -q "..." \
  -m 1000 \
  -D strict \
  --dedup-keep most_complete \
  --dedup-merge \
  -X csv \
  -o screening_deduped.csv

# Step 4: Apply inclusion criteria (date filter)
lixplore -A -q "..." \
  -m 1000 \
  -d 2015-01-01 2024-12-31 \
  -D strict \
  -X csv \
  -o screening_dated.csv

# Step 5: Title/abstract screening
lixplore -A -q "..." \
  -d 2015-01-01 2024-12-31 \
  -m 1000 \
  -D strict \
  -a

# Manual screening with annotations
lixplore --annotate 5 --tags "include,full-text-review" --priority high
lixplore --annotate 12 --tags "exclude,wrong-population" --priority low

# ELIGIBILITY PHASE
# Step 6: Export included studies
lixplore --filter-annotations "tag=include"
lixplore --export-annotations csv

# Step 7: Full-text retrieval
lixplore -A -q "..." \
  -d 2015-01-01 2024-12-31 \
  -m 1000 \
  -D strict \
  -S $(cat included_numbers.txt) \
  --download-pdf \
  --use-scihub

# INCLUDED PHASE
# Step 8: Final export for analysis
lixplore --filter-annotations "tag=include,tag=full-text-reviewed"
lixplore --export-annotations markdown
lixplore -A -q "..." --load-profile systematic_diabetes -X enw,bibtex,xlsx

# Step 9: Generate PRISMA flow diagram data
lixplore -A -q "..." -m 1000 --stat
# Total identified: 1000
# After deduplication: 750
# After screening: 150
# After full-text: 45
```

---

## Current Awareness

### Weekly Research Updates

**Goal:** Stay current in your field

```bash
# Monday Morning Routine
# Step 1: Last week's papers
lixplore -s PC -q "machine learning" \
  -d 2024-12-15 2024-12-22 \
  -m 100 \
  -D \
  --sort newest \
  -S first:20 \
  -X xlsx \
  -o weekly_ml_$(date +%Y%m%d).xlsx

# Step 2: arXiv latest (very recent)
lixplore -x -q "deep learning" \
  -d 2024-12-15 2024-12-22 \
  -m 50 \
  --sort newest \
  --show-pdf-links

# Step 3: Author alerts (favorite researchers)
lixplore -P -au "LeCun Y" -d 2024-12-01 2024-12-31 -m 10 --sort newest
lixplore -P -au "Hinton G" -d 2024-12-01 2024-12-31 -m 10 --sort newest

# Step 4: Annotate interesting papers
lixplore --annotate 2 --tags "read-this-week" --priority high

# Step 5: Create reading list
lixplore --filter-annotations "tag=read-this-week"
```

### Monthly Topic Monitoring

```bash
# Monitor specific research area
# Step 1: Monthly search
lixplore -A -q "CRISPR gene editing clinical trials" \
  -d 2024-12-01 2024-12-31 \
  -m 200 \
  -D \
  --sort newest \
  --stat

# Step 2: Compare to last month
lixplore -A -q "CRISPR gene editing clinical trials" \
  -d 2024-11-01 2024-11-30 \
  -m 200 \
  -D \
  --stat

# Step 3: Track trends
# Note publication counts, top journals, top authors

# Step 4: Export highlights
lixplore -A -q "CRISPR gene editing clinical trials" \
  -d 2024-12-01 2024-12-31 \
  -m 200 \
  -D \
  --sort newest \
  -S first:10 \
  -X xlsx \
  -o crispr_highlights_dec2024.xlsx
```

---

## Bibliography Building

### LaTeX Bibliography

**Goal:** Create BibTeX file for LaTeX document

```bash
# Step 1: Gather references
lixplore -C -q "topic1" -m 50 -D --enrich -X bibtex -o refs_topic1.bib
lixplore -C -q "topic2" -m 50 -D --enrich -X bibtex -o refs_topic2.bib
lixplore -C -q "topic3" -m 50 -D --enrich -X bibtex -o refs_topic3.bib

# Step 2: Combine (if needed)
cat refs_topic*.bib > all_refs.bib

# Step 3: Clean duplicates
lixplore -C -q "all topics combined" -m 200 -D strict --enrich -X bibtex -o final_refs.bib

# Step 4: Verify entries
# Check BibTeX file has all required fields
grep '@' final_refs.bib | wc -l
```

### EndNote Library

**Goal:** Build EndNote library

```bash
# Step 1: Search and export
lixplore -P -q "systematic review topic" \
  -m 200 \
  -D \
  --enrich \
  -X enw \
  -o endnote_library.enw

# Step 2: Import to EndNote
# File → Import → File → Choose endnote_library.enw

# Step 3: Continue adding
lixplore -P -q "additional topic" \
  -m 100 \
  -D \
  --enrich \
  -X enw \
  -o endnote_additional.enw
```

### Zotero Integration

**Goal:** Build Zotero library directly

```bash
# Step 1: Configure Zotero (one-time)
lixplore --configure-zotero YOUR_API_KEY YOUR_USER_ID

# Step 2: Create collection (in Zotero UI)
lixplore --show-zotero-collections
# Note collection key: ABC123DEF

# Step 3: Add papers directly
lixplore -P -q "research topic" \
  -m 100 \
  -D \
  --add-to-zotero \
  --zotero-collection ABC123DEF

# Step 4: Continue adding to same collection
lixplore -C -q "related topic" \
  -m 50 \
  -D \
  --add-to-zotero \
  --zotero-collection ABC123DEF
```

---

## Grant Writing

### Grant Literature Support

**Goal:** Build literature base for grant proposal

```bash
# BACKGROUND SECTION
# Step 1: Foundational papers (historical)
lixplore -P -q "foundational topic" \
  -d 1990-01-01 2010-12-31 \
  -m 100 \
  --sort oldest \
  -S first:20 \
  --annotate-tag "grant-background"

# Step 2: Recent advances (last 3 years)
lixplore -A -q "recent advances topic" \
  -d 2022-01-01 2024-12-31 \
  -m 150 \
  -D \
  --sort newest \
  -S first:30 \
  --annotate-tag "grant-recent"

# PRELIMINARY DATA SECTION
# Step 3: Methodology papers
lixplore -P -q "methodology approach" \
  -m 50 \
  -D \
  --annotate-tag "grant-methods"

# INNOVATION SECTION
# Step 4: Gap analysis (what's missing)
lixplore -A -q "related approaches" -m 200 -D --stat
# Identify gaps in literature

# SIGNIFICANCE SECTION
# Step 5: Impact papers (highly cited)
lixplore -C -q "clinical impact topic" \
  -m 100 \
  -D \
  --sort newest \
  --annotate-tag "grant-significance"

# FINAL COMPILATION
# Step 6: Export all tagged papers
lixplore --filter-annotations "tag=grant"
lixplore --export-annotations markdown
lixplore --export-annotations csv

# Step 7: Create formatted bibliography
lixplore -A -q "all grant topics" -m 500 -D --enrich -c apa -o grant_refs.txt
```

---

## Thesis/Dissertation

### Chapter-by-Chapter Workflow

**Goal:** Organize literature by dissertation chapter

```bash
# CHAPTER 1: INTRODUCTION
# Historical overview
lixplore -P -q "topic history background" \
  -d 1970-01-01 2010-12-31 \
  -m 100 \
  --sort oldest \
  --annotate-tag "chapter1,introduction,history"

# Current state
lixplore -A -q "current state topic" \
  -d 2020-01-01 2024-12-31 \
  -m 150 \
  -D \
  --annotate-tag "chapter1,introduction,current"

# CHAPTER 2: LITERATURE REVIEW
lixplore -A -q "comprehensive topic review" \
  -m 500 \
  -D strict \
  --enrich \
  --annotate-tag "chapter2,lit-review"

# Export chapter 2 bibliography
lixplore --search-annotations "chapter2"
lixplore --export-annotations markdown

# CHAPTER 3: METHODOLOGY
lixplore -P -q "methodological approach" \
  -m 100 \
  -D \
  --annotate-tag "chapter3,methodology"

# CHAPTER 4: RESULTS
lixplore -C -q "similar results analysis" \
  -m 75 \
  -D \
  --annotate-tag "chapter4,results,comparison"

# CHAPTER 5: DISCUSSION
lixplore -A -q "interpretation implications" \
  -m 200 \
  -D \
  --annotate-tag "chapter5,discussion"

# FINAL BIBLIOGRAPHY EXPORT
# All chapters
lixplore --list-annotations
lixplore --export-annotations markdown

# Per chapter
lixplore --search-annotations "chapter1"
lixplore --export-annotations markdown
# Repeat for each chapter

# Create master bibliography
lixplore -A -q "all dissertation topics" \
  -m 1000 \
  -D strict \
  --enrich \
  -X bibtex \
  -o dissertation_refs.bib
```

---

## Best Practices

### 1. Document Your Process

```bash
# Save search parameters
lixplore -A -q "topic" -m 200 -D --save-profile project_name

# Keep log of searches
echo "$(date): Searched topic XYZ, 200 results, 150 after dedup" >> research_log.txt
```

### 2. Regular Backups

```bash
# Backup annotations
cp ~/.lixplore_annotations.json ~/Backup/annotations_$(date +%Y%m%d).json

# Backup exported files
cp exports/*.xlsx ~/Backup/exports/
```

### 3. Version Control

```bash
# Track bibliography changes
git add dissertation_refs.bib
git commit -m "Updated bibliography with latest papers"
```

### 4. Collaboration

```bash
# Share search profiles
lixplore --list-profiles
# Send profile file to collaborator

# Export for team
lixplore -A -q "team topic" -m 300 -D -X xlsx -o team_refs.xlsx
# Share team_refs.xlsx
```

---

**Last Updated:** 2024-12-28
