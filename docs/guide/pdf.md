# PDF Management Guide

> **Complete guide for PDF downloading, viewing, and organization**

## Table of Contents

- [PDF Sources](#pdf-sources)
- [Download Methods](#download-methods)
- [Configuration](#configuration)
- [Organization](#organization)
- [Troubleshooting](#troubleshooting)

---

## PDF Sources

Lixplore attempts PDF download in this order:

1. **PubMed Central (PMC)** - Open access biomedical articles
2. **arXiv** - Preprints (physics, CS, math)
3. **DOI Resolution** - Publisher links via Unpaywall
4. **SciHub** - Fallback (optional, user-configured)

### Source Comparison

| Source | Coverage | Speed | Reliability | Legal Status |
|--------|----------|-------|-------------|--------------|
| PMC | Biomedical OA | Fast | High | ✓ Legal |
| arXiv | STEM preprints | Fast | High | ✓ Legal |
| Unpaywall | All OA | Medium | High | ✓ Legal |
| SciHub | Paywalled | Slow | Variable | ⚠️ Gray area |

---

## Download Methods

### Method 1: Show PDF Links (No Download)

Display clickable links without downloading:

```bash
lixplore -x -q "neural networks" -m 15 --show-pdf-links
```

**Output:**
```
[1] Deep Learning with Neural Networks
    Open PDF → https://arxiv.org/pdf/2103.12345.pdf

[2] Convolutional Neural Networks for Image Recognition
    Open PDF → https://arxiv.org/pdf/2104.67890.pdf
```

**Best for:**
- Quick preview
- Selective download
- Modern terminals (iTerm2, GNOME Terminal, Windows Terminal)

### Method 2: Download All PDFs

Download PDFs for all search results:

```bash
lixplore -J -q "open access research" -m 10 --download-pdf
```

**Process:**
```
Checking for open access PDFs...
[1/10] Downloading: paper1.pdf... ✓
[2/10] Downloading: paper2.pdf... ✓
[3/10] Not available: paper3
[4/10] Downloading: paper4.pdf... ✓
...
Downloaded 7/10 PDFs to ~/Lixplore_PDFs/
```

### Method 3: Download Specific Articles

Download PDFs for selected articles only:

```bash
lixplore -P -q "cancer" -m 30 --download-pdf --pdf-numbers 1 3 5 7
```

**Best for:**
- After reviewing abstracts
- High-priority articles only
- Bandwidth conservation

### Method 4: With SciHub Fallback

Use SciHub for articles not available via legal sources:

```bash
# Setup SciHub mirror (one-time)
lixplore --set-scihub-mirror https://sci-hub.se

# Download with SciHub fallback
lixplore -P -q "research" -m 10 --download-pdf --use-scihub
```

**⚠️ Disclaimer:** Use SciHub responsibly. Check your institution's policies.

---

## Configuration

### Check PDF Directory

```bash
lixplore --show-pdf-dir
```

**Output:**
```
PDF download directory: /home/user/Lixplore_PDFs/
Total PDFs downloaded: 342
```

### Set SciHub Mirror

```bash
lixplore --set-scihub-mirror https://sci-hub.se
```

**Active Mirrors (as of Dec 2024):**
- https://sci-hub.se
- https://sci-hub.st
- https://sci-hub.ru
- https://sci-hub.tw

**Note:** Mirrors change frequently. Check https://sci-hub.now.sh for current list.

### Change PDF Directory

Edit configuration file:
```bash
nano ~/.lixplore/config.json
```

```json
{
  "pdf_download_dir": "/path/to/custom/directory"
}
```

---

## Organization

### Default Organization

```
~/Lixplore_PDFs/
├── paper_title_1.pdf
├── paper_title_2.pdf
├── paper_title_3.pdf
└── ...
```

### Recommended Organization

**By Topic:**
```bash
# Create topic folders
mkdir -p ~/Lixplore_PDFs/Machine_Learning
mkdir -p ~/Lixplore_PDFs/Cancer_Research
mkdir -p ~/Lixplore_PDFs/Climate_Change

# Download to specific folder (manual move after download)
lixplore -x -q "machine learning" -m 20 --download-pdf
# Then: mv ~/Lixplore_PDFs/ml*.pdf ~/Lixplore_PDFs/Machine_Learning/
```

**By Date:**
```bash
# Create monthly folders
mkdir -p ~/Lixplore_PDFs/2024-12
mkdir -p ~/Lixplore_PDFs/2024-11

# Move downloaded PDFs by month
mv ~/Lixplore_PDFs/*.pdf ~/Lixplore_PDFs/2024-12/
```

**By Project:**
```bash
# Project-based organization
mkdir -p ~/Lixplore_PDFs/PhD_Chapter1
mkdir -p ~/Lixplore_PDFs/PhD_Chapter2
mkdir -p ~/Lixplore_PDFs/Grant_Proposal

# Download and organize
lixplore -P -q "methodology chapter1 topic" -m 15 --download-pdf
# Move to project folder
```

---

## Complete Workflows

### Workflow 1: Open Access Literature Review

```bash
# Step 1: Search open access sources
lixplore -J -q "public health interventions" -m 30 --show-pdf-links

# Step 2: Review abstracts and select
lixplore -J -q "public health interventions" -m 30 -a

# Step 3: Download selected PDFs
lixplore -J -q "public health interventions" -m 30 --download-pdf --pdf-numbers 1 3 5 8 12

# Step 4: Annotate
lixplore --annotate 1 --rating 5 --tags "important,read"
```

### Workflow 2: arXiv Latest Papers

```bash
# Step 1: Get latest CS papers
lixplore -x -q "deep learning" -d 2024-12-01 2024-12-31 -m 20 --sort newest

# Step 2: Show PDF links (all arXiv papers have PDFs)
lixplore -x -q "deep learning" -d 2024-12-01 2024-12-31 -m 20 --show-pdf-links

# Step 3: Download all
lixplore -x -q "deep learning" -d 2024-12-01 2024-12-31 -m 20 --download-pdf

# Step 4: Organize
mv ~/Lixplore_PDFs/*.pdf ~/Papers/DeepLearning/Dec2024/
```

### Workflow 3: Multi-Source with Selective Download

```bash
# Step 1: Comprehensive search
lixplore -A -q "cancer immunotherapy" -m 100 -D --sort newest

# Step 2: Review with abstracts
lixplore -A -q "cancer immunotherapy" -m 100 -D --sort newest -a

# Step 3: Annotate high-priority
lixplore --annotate 2 --priority high --tags "must-read"
lixplore --annotate 5 --priority high --tags "must-read"
lixplore --annotate 8 --priority high --tags "must-read"

# Step 4: Download PDFs for high-priority only
lixplore -A -q "cancer immunotherapy" -m 100 -D --download-pdf --pdf-numbers 2 5 8

# Step 5: Try SciHub for unavailable
lixplore -A -q "cancer immunotherapy" -m 100 -D --download-pdf --pdf-numbers 2 5 8 --use-scihub
```

### Workflow 4: Systematic PDF Collection

```bash
# Comprehensive PDF collection for lit review
lixplore -s JX -q "machine learning healthcare" \
  -m 50 \
  -D \
  --sort newest \
  --download-pdf \
  -X xlsx \
  -o ml_healthcare_refs.xlsx

# Result: PDFs + Excel spreadsheet with metadata
```

---

## PDF Naming

### Default Naming Convention

```
ArticleTitle_FirstAuthor_Year.pdf
```

**Examples:**
```
Deep_Learning_LeCun_2015.pdf
CRISPR_Gene_Editing_Doudna_2012.pdf
```

### Handle Long Titles

Long titles are truncated:
```
Very_Long_Article_Title_About_Machine_Learning_Applications_In_Healthcare_Smith_2024.pdf
↓
Very_Long_Article_Title_About_Mach..._Smith_2024.pdf
```

### Handle Special Characters

Special characters removed:
```
"Machine Learning: A New Approach" → Machine_Learning_A_New_Approach.pdf
```

---

## Integration with Reference Managers

### Export PDFs + Metadata to Zotero

```bash
# Step 1: Download PDFs
lixplore -P -q "research" -m 20 --download-pdf

# Step 2: Export to Zotero with file attachments
lixplore -P -q "research" -m 20 --add-to-zotero

# Step 3: Manually attach PDFs in Zotero (if needed)
```

### Export for Mendeley with PDF Paths

```bash
# Export RIS with PDF locations
lixplore -P -q "research" -m 20 --download-pdf --export-for-mendeley
```

---

## Best Practices

### 1. Start with Open Access Sources

```bash
# DOAJ + arXiv = maximum PDF availability
lixplore -s JX -q "query" -m 30 --download-pdf
```

### 2. Use PDF Links for Preview

```bash
# Check availability first
lixplore -J -q "query" -m 20 --show-pdf-links

# Then download selected
lixplore -J -q "query" -m 20 --download-pdf --pdf-numbers 1 3 5
```

### 3. Organize Immediately

```bash
# Create organization system before mass download
mkdir -p ~/Papers/{Topic1,Topic2,Topic3}

# Download per topic
lixplore -P -q "topic1" -m 20 --download-pdf
mv ~/Lixplore_PDFs/*.pdf ~/Papers/Topic1/
```

### 4. Backup PDFs

```bash
# Regular backups
rsync -av ~/Lixplore_PDFs/ ~/Backups/PDFs/

# Cloud sync (Dropbox, Google Drive, etc.)
ln -s ~/Lixplore_PDFs ~/Dropbox/Research/PDFs
```

### 5. SciHub as Last Resort

```bash
# Try legal sources first
lixplore -P -q "research" -m 10 --download-pdf

# If many failed, then try SciHub
lixplore -P -q "research" -m 10 --download-pdf --use-scihub
```

---

## Troubleshooting

### Problem: No PDFs downloaded

**Solution 1: Check source**
```bash
# Use open access sources
lixplore -J -q "query" -m 10 --download-pdf  # DOAJ
lixplore -x -q "query" -m 10 --download-pdf  # arXiv
```

**Solution 2: Try SciHub**
```bash
lixplore --set-scihub-mirror https://sci-hub.se
lixplore -P -q "query" -m 10 --download-pdf --use-scihub
```

### Problem: PDF download fails

**Check internet connection:**
```bash
ping arxiv.org
ping www.ncbi.nlm.nih.gov
```

**Check PDF directory permissions:**
```bash
ls -ld ~/Lixplore_PDFs/
chmod 755 ~/Lixplore_PDFs/
```

### Problem: SciHub mirror not working

**Update mirror:**
```bash
# Try different mirrors
lixplore --set-scihub-mirror https://sci-hub.st
lixplore --set-scihub-mirror https://sci-hub.ru
```

### Problem: PDF links not clickable

**Requirements:**
- Modern terminal emulator
- iTerm2 (macOS)
- GNOME Terminal (Linux)
- Windows Terminal (Windows)

**Alternative:**
```bash
# Copy URL manually
lixplore -J -q "query" -m 10 --show-pdf-links
# Copy-paste URL to browser
```

---

## PDF Statistics

### Check Download Stats

```bash
lixplore --show-pdf-dir
```

### Count PDFs by Topic

```bash
# Count PDFs in organized folders
ls ~/Papers/MachineLearning/*.pdf | wc -l
ls ~/Papers/Genetics/*.pdf | wc -l
```

### Find Duplicate PDFs

```bash
# Find files with same size
find ~/Lixplore_PDFs -type f -exec ls -l {} \; | sort -k5 -n | uniq -D -w 50
```

---

**Last Updated:** 2024-12-28
