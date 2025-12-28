# Zotero Integration

Lixplore integrates with Zotero, a popular reference management tool, allowing you to directly add search results to your Zotero library.

---

## Overview

Zotero integration features:

- Direct import of search results to Zotero
- Automatic collection organization  
- Batch import capabilities
- Metadata preservation

---

## Setup

### Step 1: Get Zotero API Credentials

1. Log in to your Zotero account at https://www.zotero.org/
2. Go to Settings → Feeds/API
3. Create a new API key with write permissions
4. Copy your API key and User ID

### Step 2: Configure Lixplore

```bash
lixplore --configure-zotero YOUR_API_KEY YOUR_USER_ID
```

Example:
```bash
lixplore --configure-zotero abc123def456ghi789 1234567
```

### Step 3: Verify Configuration

```bash
# List your Zotero collections
lixplore --show-zotero-collections
```

---

## Basic Usage

### Add Results to Zotero

```bash
# Search and add to Zotero
lixplore -P -q "machine learning" -m 50 --add-to-zotero
```

All search results will be added to your Zotero library.

### Add to Specific Collection

```bash
# Add to a specific collection
lixplore -P -q "cancer research" -m 100 --add-to-zotero --zotero-collection ABCD1234
```

Where `ABCD1234` is your collection ID (get it from `--show-zotero-collections`).

---

## Workflows

### Workflow 1: Search and Import

```bash
# 1. Search multiple sources
lixplore -A -q "CRISPR therapy" -m 100 -D

# 2. Review results interactively
lixplore -i

# 3. Add selected results to Zotero
lixplore --add-to-zotero --zotero-collection MY_COLLECTION
```

### Workflow 2: Batch Import with Filtering

```bash
# Search, filter by date, then import
lixplore -P -q "climate change" -d 2023-01-01 2024-12-31 -m 200 --add-to-zotero
```

### Workflow 3: Multiple Collections

```bash
# Import different topics to different collections
lixplore -P -q "AI ethics" -m 50 --add-to-zotero --zotero-collection AI_ETHICS_COL
lixplore -P -q "ML healthcare" -m 50 --add-to-zotero --zotero-collection ML_HEALTH_COL
```

---

## Advanced Features

### Automatic Tagging

Results imported to Zotero include:

- Source tag (e.g., "PubMed", "arXiv")
- Query tag (your search query)
- Date imported tag

### Metadata Preservation

All available metadata is preserved:

- Title
- Authors
- Abstract
- DOI
- Publication year
- Journal
- PMID (if from PubMed)
- arXiv ID (if from arXiv)
- URLs

### Duplicate Handling

Zotero automatically handles duplicates based on DOI/PMID.

---

## Collection Management

### List Collections

```bash
lixplore --show-zotero-collections
```

Output:
```
Your Zotero Collections:
1. Research Papers (ID: ABCD1234)
2. PhD Thesis (ID: EFGH5678)
3. Literature Review (ID: IJKL9012)
4. To Read (ID: MNOP3456)
```

### Organize by Topic

Create collections in Zotero web interface, then import:

```bash
# Import COVID research to COVID collection
lixplore -P -q "COVID-19 vaccine" -m 100 --add-to-zotero --zotero-collection COVID_COL

# Import AI research to AI collection
lixplore -P -q "deep learning" -m 100 --add-to-zotero --zotero-collection AI_COL
```

---

## Integration with Other Features

### Zotero + Annotations

```bash
# 1. Search and annotate
lixplore -P -q "research topic" -m 50
lixplore --annotate 5 --rating 5 --tags "important"

# 2. Export annotated items to Zotero
lixplore --filter-annotations --rating 5 --add-to-zotero
```

### Zotero + Export

```bash
# Export to both Zotero and local file
lixplore -P -q "topic" -m 100 --add-to-zotero -X bibtex -o backup.bib
```

### Zotero + Automation

```bash
# Daily cron job: search and import to Zotero
0 9 * * * lixplore -P -q "daily topic" -m 20 --add-to-zotero --zotero-collection DAILY
```

---

## Troubleshooting

### Authentication Error

```bash
Error: Zotero authentication failed
```

Solutions:
1. Verify your API key is correct
2. Check API key has write permissions
3. Reconfigure: `lixplore --configure-zotero YOUR_KEY YOUR_ID`

### Collection Not Found

```bash
Error: Collection ID 'ABCD1234' not found
```

Solution: List collections with `--show-zotero-collections` and verify the ID.

### Import Failed

```bash
Error: Failed to import items to Zotero
```

Check:
1. Internet connection
2. Zotero server status
3. API rate limits (max 1 request/second)

### Duplicate Items

If items are being duplicated in Zotero:

1. Ensure items have DOI or PMID
2. Check Zotero duplicate detection settings
3. Use deduplicate flag: `-D`

---

## Best Practices

### 1. Organize with Collections

Create collections before importing:

```bash
# In Zotero: Create collections like "Current Research", "To Read", "Cited"
# Then import to appropriate collection
```

### 2. Use Tags Effectively

Lixplore automatically adds tags. Use them in Zotero for filtering:

- Tag: "PubMed" → All PubMed articles
- Tag: "cancer treatment" → All from this query
- Tag: "2025-01-15" → All imported on this date

### 3. Backup Before Bulk Import

Before importing hundreds of articles:

```bash
# Export Zotero library as backup
# Settings → Export Library → Zotero RDF
```

### 4. Rate Limiting

For large imports, use batches:

```bash
# Instead of -m 1000, do:
lixplore -P -q "topic" -m 100 --add-to-zotero
# Wait a few minutes, then:
lixplore -P -q "topic" -m 100 -p 2 --add-to-zotero
```

### 5. Verify Imports

After importing, check in Zotero web/desktop:

1. Verify item count
2. Check metadata completeness
3. Verify collection assignment

---

## Alternatives to Zotero Integration

If you prefer not to use direct integration:

### Export to BibTeX/RIS

```bash
# Export to file, then import to Zotero manually
lixplore -P -q "topic" -m 100 -X bibtex -o results.bib

# In Zotero: File → Import → Select results.bib
```

### Export for Mendeley

```bash
lixplore --export-for-mendeley
```

This creates a Mendeley-compatible format.

---

## API Rate Limits

Zotero API limits:

- **Write requests**: 1 request per second
- **Daily limit**: Varies by account type

Lixplore automatically respects these limits.

---

## Configuration Storage

Zotero credentials are stored in:

```
~/.lixplore/zotero_config.json
```

**Security Note**: This file contains your API key. Keep it secure.

```bash
# Set secure permissions
chmod 600 ~/.lixplore/zotero_config.json
```

---

## Example Workflows

### Literature Review Workflow

```bash
# 1. Create collection in Zotero: "My Literature Review"
# 2. Get collection ID
lixplore --show-zotero-collections

# 3. Search and import
lixplore -A -q "your review topic" -m 500 -D --enrich --add-to-zotero --zotero-collection REVIEW_COL

# 4. Organize in Zotero desktop app
```

### Weekly Research Updates

```bash
# Create a weekly cron job
# crontab -e
0 9 * * 1 lixplore -A -q "field of study" -m 50 --sort newest --add-to-zotero --zotero-collection WEEKLY
```

### Thesis Research

```bash
# Search and carefully curate
lixplore -P -q "thesis topic" -m 200 -i

# Annotate important ones
lixplore --annotate <id> --rating 5 --tags "cite,important"

# Import high-rated to Zotero
lixplore --filter-annotations --rating 5 --add-to-zotero --zotero-collection THESIS
```

---

## Summary

- Configure once with `--configure-zotero`
- Import results with `--add-to-zotero`
- Organize with `--zotero-collection`
- List collections with `--show-zotero-collections`
- Automatic metadata and tagging
- Integrates with annotations and automation

---

**Next**: [Back to Advanced Features](automation.md) | [View Examples](../examples/workflows.md)
