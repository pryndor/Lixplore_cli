# 🎯 Lixplore Enhanced TUI - Complete Guide

## ✅ What Changed?

Lixplore now has **TWO MODES** instead of four:

### Before (Complex):
1. CLI flags (command line)
2. Shell mode (`--shell`)
3. Wizard mode (`--wizard`)
4. TUI mode (`-i`)

### After (Simple):
1. **Enhanced TUI** (default - 90% of users)
2. **CLI flags** (automation - 10% of users)

---

## 🚀 The New Experience

### Just Type `lixplore` - That's It!

```bash
$ lixplore

📚 Launching Enhanced TUI mode...

╔═══════════════════════════════════════════════════════════════╗
║                 📚 LIXPLORE - ENHANCED MODE 📚                ║
║          Academic Literature Search & Management             ║
╚═══════════════════════════════════════════════════════════════╝

Main Menu:

  1. 🔍 Search for Articles
  2. 📝 Browse My Annotations
  3. 📊 View Statistics
  4. 💾 Export Annotations
  5. ❓ Help & Guide
  6. 🚪 Exit

Your choice [1]:
```

**That's the entire interface!** No flags to memorize, no commands to learn.

---

## 📋 What's in the Enhanced TUI?

### 1. 🔍 **Search for Articles**

Guided search workflow:
- Choose database (PubMed, arXiv, Crossref, EuropePMC, or All)
- Enter search query
- Set max results
- Show abstracts (optional)
- Remove duplicates (optional)
- Browse results immediately

**Example flow:**
```
What do you want to search for?: cancer treatment

Which database?
  → 1. PubMed (Biomedical & life sciences)
    2. arXiv (Physics, math, CS, etc.)
    3. Crossref (Scholarly works with DOIs)
    4. EuropePMC (European biomedical literature)
    5. All databases (Comprehensive search)

Your choice [1]: 1

How many results? [20]: 50

Show abstracts? [y/N]: n

🔍 Searching for: 'cancer treatment'...

✓ Found 50 articles!

Browse results now? [Y/n]: y
```

### 2. 📖 **Results Browser**

Interactive table with:
- Article number, rating, title, year, source
- Shows existing ratings (⭐⭐⭐⭐⭐)
- Pagination (10 per page)

**Commands:**
- `n` - Next page
- `p` - Previous page
- `v` - View article details
- `a` - Annotate article
- `s` - Select for export
- `e` - Export selected
- `b` - Back to menu
- `q` - Quit

### 3. 📝 **Annotation Interface**

When you annotate an article:
- Add/update rating (1-5 stars)
- Add tags (comma-separated)
- Add comments/notes
- Set priority (low/medium/high)
- Set read status (unread/reading/read)

**Shows existing annotations:**
```
📝 ANNOTATE ARTICLE #5

Normothermic versus Hypothermic Machine Perfusion...

This article already has annotations:
  Rating: ⭐⭐⭐⭐⭐
  Tags: important, RCT

Add/update rating? [Y/n]: y

Rating (1-5 stars) [5]: 5

Add/update tags? [Y/n]: y

Examples: important, cite-in-paper, methodology, review-later
Tags (comma-separated): important,methodology,kidney-transplant

Add a comment/note? [Y/n]: y

Your comment: Excellent study design. Sample size calculation in methods.

✓ Annotation saved successfully!
```

### 4. 📝 **Browse My Annotations**

View options:
1. All annotations
2. High-rated (4-5 stars)
3. Unread articles
4. High priority
5. Search by keyword
6. Back to main menu

**Displays as table:**
```
Found 15 annotation(s):

# │ Rating  │ Title                        │ Tags          │ Status
──┼─────────┼──────────────────────────────┼───────────────┼─────────
1 │ ⭐⭐⭐⭐⭐ │ Normothermic versus Hypot... │ important,RCT │ Unread
2 │ ⭐⭐⭐⭐   │ Suppressing Mitochondrial... │ interesting   │ Reading
3 │ ⭐⭐⭐⭐⭐ │ CRISPR Gene Editing in... │ cite,seminal  │ Read
```

### 5. 📊 **Statistics Dashboard**

Beautiful visual statistics:
```
📊 ANNOTATION STATISTICS

Total Annotated Articles: 25

Rating Distribution:
  ⭐⭐⭐⭐⭐ (5): ████████████ 12
  ⭐⭐⭐⭐ (4): ██████ 6
  ⭐⭐⭐ (3): ████ 4
  ⭐⭐ (2): ██ 2
  ⭐ (1): █ 1

Read Status:
  Read: 12
  Reading: 8
  Unread: 5

Priority:
  High: 8
  Medium: 12
  Low: 5

Comments:
  Articles with comments: 18
  Total comments: 24

Tags:
  Unique tags: 15
  Tags: important, methodology, RCT, cite-in-paper, ...
```

### 6. 💾 **Export Annotations**

Three export formats:
1. Markdown (readable, nice formatting)
2. JSON (backup, programmatic access)
3. CSV (spreadsheet, Excel)

### 7. ❓ **Help & Guide**

Built-in comprehensive help:
- Main menu options explained
- Tips and best practices
- Keyboard shortcuts
- Annotation workflow guide
- CLI usage reference

---

## 💻 CLI Mode (For Automation)

CLI flags are still available for scripting and automation:

```bash
# Quick search and export
lixplore -P -q "cancer treatment" -m 50 -X xlsx

# Automated daily monitoring
lixplore -P -q "CRISPR therapy" -m 10 -X csv >> daily_papers.csv

# Batch processing
for topic in "AI" "ML" "DL"; do
  lixplore -x -q "$topic" -m 100 -X json -o "${topic}.json"
done

# Integration with other tools
lixplore -P -q "immunotherapy" -m 100 -X json | jq '.[] | .title'
```

**Essential CLI Flags:**
- `-P`, `-A`, `-x`, `-C`, `-E` - Source selection
- `-q <query>` - Search query
- `-m <number>` - Max results
- `-X <format>` - Export format
- `-o <file>` - Output file
- `--annotate`, `--rating`, `--tags` - Annotation flags

---

## 🎯 Which Mode Should I Use?

### Use **TUI** (default) when:
- ✅ Doing interactive research
- ✅ Browsing and annotating
- ✅ Managing your library
- ✅ Exploring results visually
- ✅ You're a beginner
- ✅ You want guided workflows

### Use **CLI** when:
- ✅ Automating tasks (scripts, cron jobs)
- ✅ Running on remote servers
- ✅ CI/CD pipelines
- ✅ Batch processing
- ✅ Quick one-off commands
- ✅ Integration with other tools

---

## 📊 Feature Comparison

| Feature | Enhanced TUI | CLI Flags |
|---------|--------------|-----------|
| **Search articles** | ✅ Guided | ✅ One command |
| **Browse results** | ✅ Visual table | ❌ Text output |
| **Annotate** | ✅ Interactive | ✅ Via flags |
| **View annotations** | ✅ Filtered views | ✅ List command |
| **Statistics** | ✅ Visual charts | ✅ Text stats |
| **Export** | ✅ Menu selection | ✅ Via flags |
| **Help** | ✅ Built-in guide | ✅ --help |
| **Automation** | ❌ Interactive only | ✅ Full support |
| **Scripting** | ❌ No | ✅ Yes |
| **Learning curve** | ⭐ Easy | ⭐⭐⭐ Hard |
| **Speed (interactive)** | ⭐⭐⭐ Fast | ⭐ Slow |
| **Speed (automation)** | ❌ N/A | ⭐⭐⭐ Fast |

---

## 🔄 Migration Guide

### From Shell Mode (`--shell`):

**Before:**
```bash
lixplore --shell

lixplore> search "cancer" -P -m 20
lixplore> annotate 5 --rating 5
lixplore> exit
```

**After:**
```bash
lixplore  # Launches TUI by default

# Select: 1. Search for Articles
# Follow guided prompts
# Browse results → Annotate directly in UI
```

### From Wizard Mode (`--wizard`):

**Before:**
```bash
lixplore --wizard

# Follow wizard prompts...
```

**After:**
```bash
lixplore  # Same guided experience, better UI

# All wizard features built into TUI main menu
```

### From Old TUI (`-i`):

**Before:**
```bash
lixplore -P -q "cancer" -m 20 -i
```

**After:**
```bash
lixplore  # Launch TUI first

# Select: 1. Search for Articles
# Search from within TUI
```

**OR use CLI directly:**
```bash
lixplore -P -q "cancer" -m 20  # No -i needed
```

---

## ⚡ Quick Start Examples

### Example 1: First-Time User

```bash
$ lixplore

# [TUI launches]
# Select: 1. Search for Articles
# Enter: "diabetes treatment"
# Choose: PubMed
# Results: 20
# Browse → Annotate interesting ones
# Exit when done
```

### Example 2: Literature Review

```bash
$ lixplore

# 1. Search for Articles → "cancer immunotherapy" → 50 results
# Browse → Annotate high-quality papers (5 stars)
# Tag them: "cite-in-paper", "important"
# Add comments on why they're relevant

# 2. Browse My Annotations → High-rated (4-5 stars)
# Review your selections

# 3. Export Annotations → Markdown
# Get formatted export for your bibliography
```

### Example 3: Daily Monitoring (CLI)

```bash
# Add to crontab
0 9 * * * lixplore -P -q "CRISPR 2025" -m 10 -X csv >> new_papers.csv
```

---

## 🎨 Tips & Best Practices

### For TUI Users:

1. **Rate as you read**
   - 5 stars = Must-read, cite in paper
   - 4 stars = Very good, important
   - 3 stars = Good, relevant
   - 2 stars = OK, maybe useful
   - 1 star = Not relevant

2. **Use consistent tags**
   - Topic tags: `immunology`, `methodology`, `clinical-trial`
   - Action tags: `cite-in-paper`, `review-later`, `share-with-team`
   - Quality tags: `seminal`, `important`, `interesting`

3. **Add specific comments**
   - ✅ "Figure 3 shows biomarker data I need"
   - ✅ "Methods section has sample size calculation"
   - ❌ "Good paper" (too vague)

4. **Export regularly**
   - Weekly backup to JSON
   - Export filtered lists (e.g., high-rated papers)

5. **Use read status tracking**
   - Unread → Papers to read
   - Reading → Currently analyzing
   - Read → Already reviewed

### For CLI Users:

1. **Create aliases**
   ```bash
   alias lxp='lixplore -P -m 20'
   alias lxe='lixplore -P -m 50 -X xlsx'
   ```

2. **Use shell scripts**
   ```bash
   #!/bin/bash
   # fetch_papers.sh
   lixplore -P -q "$1" -m 100 -X json -o "papers_$1.json"
   ```

3. **Combine with other tools**
   ```bash
   lixplore -P -q "AI" -m 100 -X json | \
     jq '.[] | select(.year >= 2023) | .title'
   ```

---

## 🐛 Troubleshooting

### TUI doesn't launch

**Issue:** Running `lixplore` shows error instead of TUI

**Solution:** Make sure Rich library is installed:
```bash
pip install rich
```

### Can't see colors/formatting

**Issue:** TUI looks plain or broken

**Solution:**
1. Update Rich: `pip install --upgrade rich`
2. Use a modern terminal (iTerm2, Windows Terminal, etc.)

### Want old behavior back

**Issue:** Prefer CLI over TUI

**Solution:** Just provide a query:
```bash
lixplore -P -q "your query" -m 20
```

This skips TUI and uses CLI directly.

---

## 📚 Summary

**Lixplore is now simpler:**
- Type `lixplore` → Beautiful TUI appears
- Type `lixplore -P -q "query"` → CLI search

**90% of users** will love the TUI.
**10% of users** (automation, scripts) will use CLI.

Everyone wins! 🎉

---

## 🚀 Get Started

```bash
# Interactive mode (TUI)
lixplore

# Quick CLI search
lixplore -P -q "your topic" -m 20 -X xlsx

# Explicit TUI launch
lixplore --tui

# Help
lixplore --help
```

**The best academic literature tool just got even better!** 📚

---

*Last updated: 2025-12-28*
*Version: 2.5 (Enhanced TUI)*
