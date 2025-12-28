# Annotation System Flags

> **Complete documentation for article annotation and organization flags**

## Table of Contents

- [Overview](#overview)
- [Creating Annotations](#creating-annotations)
- [Viewing Annotations](#viewing-annotations)
- [Managing Annotations](#managing-annotations)
- [Annotation Workflows](#annotation-workflows)

---

## Overview

The annotation system allows you to rate, tag, comment on, and organize research articles for better literature management.

**Total Annotation Flags:** 13

**Features:**
- 5-star rating system
- Comments and notes
- Tag organization
- Read status tracking (unread, reading, read)
- Priority levels (low, medium, high)

**Storage:** Annotations saved in `~/.lixplore_annotations.json`

---

## Creating Annotations

### `--annotate`

**Description:** Annotate specific article from last search.

**Syntax:**
```bash
lixplore --annotate N [--comment TEXT] [--rating 1-5] [--tags TAGS] [--read-status STATUS] [--priority LEVEL]
```

**Type:** Integer (article number)

#### Examples

**Example 1: Basic Annotation**
```bash
# Search first
lixplore -P -q "cancer treatment" -m 20

# Annotate article #5
lixplore --annotate 5 --rating 5 --tags "important,methodology"
```

**Example 2: Full Annotation**
```bash
lixplore --annotate 3 \
  --rating 4 \
  --tags "review,cite-in-paper" \
  --comment "Excellent methodology section, relevant for my research" \
  --read-status reading \
  --priority high
```

**Example 3: Quick Rating**
```bash
lixplore --annotate 7 --rating 5
```

**Example 4: Add Comment Only**
```bash
lixplore --annotate 2 --comment "Follow up on this author's other work"
```

**Example 5: Mark as Read**
```bash
lixplore --annotate 10 --read-status read
```

**Example 6: Set Priority**
```bash
lixplore --annotate 1 --priority high --tags "must-read"
```

**Example 7: Multiple Tags**
```bash
lixplore --annotate 4 --tags "methodology,statistics,cite,review-later"
```

**Example 8: Update Existing Annotation**
```bash
# Add to existing annotation
lixplore --annotate 5 --comment "Additional notes after reading" --read-status read
```

---

### `--comment`

**Description:** Add comment/note to article (use with --annotate).

**Syntax:**
```bash
lixplore --annotate N --comment "TEXT"
```

**Type:** String value

#### Examples

**Example 1: Research Note**
```bash
lixplore --annotate 3 --comment "Key findings: p < 0.001 for intervention group"
```

**Example 2: Methodology Note**
```bash
lixplore --annotate 5 --comment "Uses novel statistical approach - investigate further"
```

**Example 3: Citation Reminder**
```bash
lixplore --annotate 7 --comment "Cite in introduction, relevant background"
```

---

### `--rating`

**Description:** Rate article 1-5 stars (use with --annotate).

**Syntax:**
```bash
lixplore --annotate N --rating [1-5]
```

**Type:** Integer (1-5)

#### Examples

**Example 1: Excellent Paper**
```bash
lixplore --annotate 2 --rating 5 --tags "excellent,must-cite"
```

**Example 2: Good Reference**
```bash
lixplore --annotate 8 --rating 4
```

**Example 3: Poor Quality**
```bash
lixplore --annotate 12 --rating 2 --comment "Weak methodology"
```

**Rating Guide:**
- ⭐⭐⭐⭐⭐ (5) - Excellent, must-cite
- ⭐⭐⭐⭐ (4) - Very good, relevant
- ⭐⭐⭐ (3) - Good, useful reference
- ⭐⭐ (2) - Fair, limited usefulness
- ⭐ (1) - Poor quality

---

### `--tags`

**Description:** Add comma-separated tags (use with --annotate).

**Syntax:**
```bash
lixplore --annotate N --tags "TAG1,TAG2,TAG3"
```

**Type:** Comma-separated string

#### Examples

**Example 1: Research Tags**
```bash
lixplore --annotate 3 --tags "methodology,statistics,relevant"
```

**Example 2: Organization Tags**
```bash
lixplore --annotate 5 --tags "chapter2,lit-review,must-cite"
```

**Example 3: Action Tags**
```bash
lixplore --annotate 7 --tags "read-later,print,discuss-with-advisor"
```

**Example 4: Topic Tags**
```bash
lixplore --annotate 9 --tags "machine-learning,healthcare,predictive-models"
```

**Suggested Tag Categories:**
- **Importance:** important, must-read, must-cite, key-paper
- **Topic:** methodology, results, review, meta-analysis
- **Action:** read-later, print, email, discuss
- **Project:** chapter1, chapter2, introduction, discussion
- **Quality:** excellent, good, questionable, weak-methods

---

### `--read-status`

**Description:** Set read status (use with --annotate).

**Syntax:**
```bash
lixplore --annotate N --read-status [unread|reading|read]
```

**Type:** String choice

**Options:**
- `unread` - Not yet started
- `reading` - Currently reading
- `read` - Completed

#### Examples

**Example 1: Mark as Reading**
```bash
lixplore --annotate 5 --read-status reading
```

**Example 2: Mark as Read with Rating**
```bash
lixplore --annotate 3 --read-status read --rating 5
```

**Example 3: Unread Priority**
```bash
lixplore --annotate 7 --read-status unread --priority high
```

---

### `--priority`

**Description:** Set priority level (use with --annotate).

**Syntax:**
```bash
lixplore --annotate N --priority [low|medium|high]
```

**Type:** String choice

**Options:**
- `high` - Must read soon
- `medium` - Normal priority (default)
- `low` - Read if time permits

#### Examples

**Example 1: High Priority**
```bash
lixplore --annotate 2 --priority high --tags "deadline,important"
```

**Example 2: Low Priority**
```bash
lixplore --annotate 10 --priority low --read-status unread
```

---

## Viewing Annotations

### `--show-annotation`

**Description:** Show annotation for specific article.

**Syntax:**
```bash
lixplore --show-annotation N
```

**Type:** Integer (article number from last search)

#### Examples

**Example 1: View Annotation**
```bash
# Search first
lixplore -P -q "cancer" -m 20

# View annotation for article #5
lixplore --show-annotation 5
```

**Example 2: Check Before Update**
```bash
lixplore --show-annotation 3
# Then update:
lixplore --annotate 3 --comment "Additional notes"
```

---

### `--list-annotations`

**Description:** List all annotated articles.

**Syntax:**
```bash
lixplore --list-annotations
```

**Type:** Boolean flag

#### Examples

**Example 1: View All Annotations**
```bash
lixplore --list-annotations
```

**Example 2: Filter High Priority**
```bash
lixplore --filter-annotations "priority=high"
```

---

### `--filter-annotations`

**Description:** Filter annotations by criteria.

**Syntax:**
```bash
lixplore --filter-annotations "KEY=VALUE,KEY=VALUE"
```

**Type:** String (comma-separated filters)

**Filter Keys:**
- `min_rating` - Minimum rating (1-5)
- `max_rating` - Maximum rating (1-5)
- `read_status` - Read status (unread, reading, read)
- `priority` - Priority level (low, medium, high)
- `tag` - Tag name (must contain tag)

#### Examples

**Example 1: High-Rated Papers**
```bash
lixplore --filter-annotations "min_rating=4"
```

**Example 2: High Priority Unread**
```bash
lixplore --filter-annotations "priority=high,read_status=unread"
```

**Example 3: Specific Tag**
```bash
lixplore --filter-annotations "tag=must-cite"
```

**Example 4: Reading List**
```bash
lixplore --filter-annotations "read_status=reading"
```

**Example 5: Excellence Filter**
```bash
lixplore --filter-annotations "min_rating=5,priority=high"
```

**Example 6: Multiple Criteria**
```bash
lixplore --filter-annotations "min_rating=4,read_status=read,priority=high"
```

---

### `--search-annotations`

**Description:** Search annotations by keyword.

**Syntax:**
```bash
lixplore --search-annotations "KEYWORD"
```

**Type:** String value

**Searches In:**
- Article titles
- Comments/notes
- Tags

#### Examples

**Example 1: Search Comments**
```bash
lixplore --search-annotations "methodology"
```

**Example 2: Search Tags**
```bash
lixplore --search-annotations "machine-learning"
```

**Example 3: Search Titles**
```bash
lixplore --search-annotations "CRISPR"
```

---

## Managing Annotations

### `--export-annotations`

**Description:** Export all annotations to file.

**Syntax:**
```bash
lixplore --export-annotations [markdown|json|csv]
```

**Type:** String choice

**Formats:**
- `markdown` - Human-readable Markdown
- `json` - Structured JSON data
- `csv` - Spreadsheet format

#### Examples

**Example 1: Markdown Export**
```bash
lixplore --export-annotations markdown
```
Creates: `lixplore_annotations_TIMESTAMP.md`

**Example 2: JSON Export**
```bash
lixplore --export-annotations json
```
Creates: `lixplore_annotations_TIMESTAMP.json`

**Example 3: CSV Export**
```bash
lixplore --export-annotations csv
```
Creates: `lixplore_annotations_TIMESTAMP.csv`

---

### `--annotation-stats`

**Description:** Show annotation statistics.

**Syntax:**
```bash
lixplore --annotation-stats
```

**Type:** Boolean flag

**Statistics Shown:**
- Total annotated articles
- Rating distribution
- Read status breakdown
- Priority distribution
- Comment count
- Unique tags count

#### Examples

**Example 1: View Statistics**
```bash
lixplore --annotation-stats
```

**Output:**
```
ANNOTATION STATISTICS
Total Annotated Articles: 42

Rating Distribution:
  ⭐⭐⭐⭐⭐ (5): ████████ 8
  ⭐⭐⭐⭐ (4): ████████████ 12
  ⭐⭐⭐ (3): ██████ 6

Read Status:
  Read: 25
  Reading: 10
  Unread: 7

Priority:
  High: 15
  Medium: 20
  Low: 7

Tags: 67 unique tags
```

---

### `--delete-annotation`

**Description:** Delete annotation for specific article.

**Syntax:**
```bash
lixplore --delete-annotation N
```

**Type:** Integer (article number from last search)

#### Examples

**Example 1: Delete Annotation**
```bash
# Search first
lixplore -P -q "cancer" -m 20

# Delete annotation for article #5
lixplore --delete-annotation 5
```

---

## Annotation Workflows

### Workflow 1: Paper Review

```bash
# 1. Search for papers
lixplore -P -q "machine learning healthcare" -m 30 -a

# 2. Initial screening (rate based on abstracts)
lixplore --annotate 3 --rating 5 --tags "relevant,must-read" --priority high
lixplore --annotate 7 --rating 4 --tags "relevant" --priority medium
lixplore --annotate 12 --rating 2 --tags "not-relevant" --priority low

# 3. Mark for reading
lixplore --annotate 3 --read-status reading

# 4. After reading, add detailed notes
lixplore --annotate 3 \
  --comment "Excellent RCT design. N=500, p<0.001. Key for my methodology chapter." \
  --tags "relevant,must-cite,methodology,chapter2" \
  --read-status read

# 5. View high-priority unread papers
lixplore --filter-annotations "priority=high,read_status=unread"
```

### Workflow 2: Literature Review

```bash
# 1. Comprehensive search
lixplore -A -q "cancer immunotherapy" -m 200 -D --sort newest

# 2. Quick screening - mark important ones
lixplore --annotate 1 --rating 5 --priority high
lixplore --annotate 5 --rating 5 --priority high
lixplore --annotate 8 --rating 4 --priority medium

# 3. Add topical tags
lixplore --annotate 1 --tags "checkpoint-inhibitors,melanoma"
lixplore --annotate 5 --tags "CAR-T,leukemia"

# 4. Export must-cite papers
lixplore --filter-annotations "min_rating=5"
lixplore --export-annotations markdown
```

### Workflow 3: Reading List Management

```bash
# 1. Find papers and create reading list
lixplore -P -q "systematic review methodology" -m 50 --sort newest
lixplore --annotate 1 --read-status unread --priority high --tags "learn,methodology"
lixplore --annotate 3 --read-status unread --priority high --tags "learn,methodology"
lixplore --annotate 5 --read-status unread --priority medium --tags "reference"

# 2. Start reading
lixplore --filter-annotations "read_status=unread,priority=high"
lixplore --annotate 1 --read-status reading

# 3. Complete reading and annotate
lixplore --annotate 1 \
  --read-status read \
  --rating 5 \
  --comment "Best guide on systematic reviews. Reference for methods section."

# 4. Check progress
lixplore --annotation-stats
```

### Workflow 4: Organization by Project

```bash
# Tag by dissertation chapter
lixplore --annotate 1 --tags "chapter1,introduction,background"
lixplore --annotate 5 --tags "chapter2,methodology,statistics"
lixplore --annotate 10 --tags "chapter3,results,analysis"
lixplore --annotate 15 --tags "chapter4,discussion,implications"

# Find all chapter 2 papers
lixplore --search-annotations "chapter2"
lixplore --filter-annotations "tag=methodology"

# Export chapter-specific bibliography
lixplore --search-annotations "chapter2"
lixplore --export-annotations markdown
```

---

## Best Practices

### 1. Consistent Tagging System

**Create Tag Vocabulary:**
- Topics: `methodology`, `results`, `review`, `meta-analysis`
- Quality: `excellent`, `good`, `fair`, `poor`
- Action: `read-later`, `cite`, `discuss`, `follow-up`
- Project: `chapter1`, `chapter2`, `intro`, `discussion`

### 2. Rate Immediately After Reading

```bash
# Don't wait - annotate while fresh
lixplore --annotate 5 \
  --rating 5 \
  --read-status read \
  --comment "Detailed notes here..." \
  --tags "relevant,cite"
```

### 3. Use Priority for Time Management

```bash
# High priority = read this week
lixplore --annotate 1 --priority high --read-status unread

# Medium = read this month
lixplore --annotate 5 --priority medium --read-status unread

# Low = read if time permits
lixplore --annotate 10 --priority low --read-status unread
```

### 4. Regular Exports for Backup

```bash
# Weekly backup
lixplore --export-annotations json
lixplore --export-annotations markdown
```

### 5. Review Statistics Periodically

```bash
# Monthly check-in
lixplore --annotation-stats
lixplore --filter-annotations "read_status=unread,priority=high"
```

---

## Tips & Tricks

### Quick Rating Scale

- **5 stars:** Foundational paper, must cite
- **4 stars:** Very relevant, high quality
- **3 stars:** Useful reference, good to have
- **2 stars:** Tangentially relevant
- **1 star:** Not useful / poor quality

### Effective Commenting

**Good Comments:**
- "RCT, N=500, primary outcome p<0.001, relevant for methods"
- "Cite in intro for background on X"
- "Methodology section: novel approach to Y"

**Avoid:**
- "Good paper" (not specific)
- "Read this" (use priority/read-status instead)

### Tag Organization

**Use Hierarchical Tags:**
- `topic-subtopic`: e.g., `ML-neural-networks`, `stats-regression`
- `project-chapter`: e.g., `diss-chapter2`, `paper1-methods`

---

**Last Updated:** 2024-12-28
