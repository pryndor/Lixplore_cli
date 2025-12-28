# 🚀 Lixplore Interactive Modes Guide

## Overview

Lixplore now offers **two powerful interactive modes** to make your research workflow easier:

1. **Shell Mode** - Persistent terminal session (like OpenBB Terminal)
2. **Wizard Mode** - Guided step-by-step workflows

These modes eliminate the need to memorize 25+ command-line flags!

---

## 🐚 Shell Mode (Interactive Terminal)

### What is Shell Mode?

Shell Mode provides a **persistent interactive terminal** where you can run commands without typing `lixplore` repeatedly. It's inspired by professional tools like OpenBB Terminal.

### How to Launch

```bash
lixplore --shell
```

### Features

✅ **No repetitive typing** - Just type commands directly
✅ **Command history** - Use arrow keys to recall previous commands
✅ **Tab completion** - Fast command entry (if supported)
✅ **Persistent session** - Search results stay in memory
✅ **Built-in help** - Type `help` or `help <command>` for guidance
✅ **Integrated workflows** - Search → Annotate → Export in one session

---

### Shell Mode Commands

#### **Search Commands**

```bash
# Basic search
lixplore> search "cancer treatment" -P -m 20

# Search with options
lixplore> search "machine learning" -x -m 30 -a

# Search all sources with dedup
lixplore> search "diabetes" -A -D -m 50
```

**Search Options:**
- `-P` = PubMed
- `-A` = All sources
- `-C` = Crossref
- `-E` = EuropePMC
- `-x` = arXiv
- `-m N` = Max results
- `-a` = Show abstracts
- `-D` = Remove duplicates

#### **View Commands**

```bash
# List last search results
lixplore> list

# View specific article details
lixplore> view 5

# List all annotations
lixplore> list annotations

# List filtered annotations
lixplore> list annotations -f "min_rating=4"
lixplore> list annotations -f "priority=high"
lixplore> list annotations -f "read_status=unread"
```

#### **Annotation Commands**

```bash
# Quick annotation
lixplore> annotate 5 --rating 5

# Full annotation
lixplore> annotate 3 --rating 5 --tags "important,cite" --comment "Excellent RCT study"

# With priority and status
lixplore> annotate 7 --rating 4 --priority high --status read --tags "methodology"

# Add comment only
lixplore> annotate 3 --comment "Check figure 3 for biomarker data"

# Search annotations
lixplore> search-annotations "methodology"
```

#### **Export Commands**

```bash
# Export to markdown
lixplore> export markdown

# Export to JSON
lixplore> export json

# Export to CSV
lixplore> export csv
```

#### **Statistics**

```bash
# View annotation stats
lixplore> stats
```

#### **Utility Commands**

```bash
# Launch wizard from shell
lixplore> wizard

# Clear screen
lixplore> clear

# Show help
lixplore> help
lixplore> help search
lixplore> help annotate

# Exit shell
lixplore> exit
lixplore> quit
```

---

### Complete Shell Mode Workflow Example

```bash
$ lixplore --shell

╔════════════════════════════════════════════════════════════════╗
║                 LIXPLORE INTERACTIVE SHELL                     ║
║                                                                ║
║  Welcome to Lixplore! Type 'help' for commands.               ║
║  Type 'wizard' for guided workflow assistance.                ║
║  Type 'exit' or 'quit' to leave.                              ║
╚════════════════════════════════════════════════════════════════╝

lixplore> search "kidney transplant" -P -m 20

🔍 Searching for: 'kidney transplant'
📊 Max results: 20

✓ Found 20 articles (stored for annotation)
💡 Use 'annotate <N>' to annotate an article

lixplore> view 5

================================================================================
ARTICLE #5
================================================================================
Title: Normothermic versus Hypothermic Machine Perfusion...
Authors: Slagter Julia S, Bouari Sarah, Rijkse Elsaline...
Year: 2025
Journal: American Journal of Transplantation
DOI: 10.1016/j.ajt.2025.12.021
================================================================================

lixplore> annotate 5 --rating 5 --tags "important,RCT" --comment "Excellent methodology"

✓ Article #5 annotated successfully!
  Title: Normothermic versus Hypothermic Machine Perfusion...
  Rating: ⭐⭐⭐⭐⭐
  Tags: important, RCT
  Comment: Excellent methodology

lixplore> annotate 7 --rating 4 --tags "background" --priority medium

✓ Article #7 annotated successfully!

lixplore> list annotations

================================================================================
ANNOTATED ARTICLES (2)
================================================================================

[1] Normothermic versus Hypothermic Machine Perfusion...
    Rating: ⭐⭐⭐⭐⭐ (5/5)
    Tags: important, RCT
    Status: Unread | Priority: Medium
    Comments: 1

[2] Another article title...
    Rating: ⭐⭐⭐⭐ (4/5)
    Tags: background
    Status: Unread | Priority: Medium

lixplore> export markdown

✓ Annotations exported to: lixplore_annotations_20251228_123045.md

lixplore> stats

================================================================================
ANNOTATION STATISTICS
================================================================================

Total Annotated Articles: 2

Rating Distribution:
  ⭐⭐⭐⭐⭐ (5): █ 1
  ⭐⭐⭐⭐ (4): █ 1

lixplore> exit

Goodbye! 👋
```

---

## 🧙 Wizard Mode (Guided Workflows)

### What is Wizard Mode?

Wizard Mode provides **step-by-step guidance** for common tasks. Perfect for new users or when you forget command syntax!

### How to Launch

```bash
# Launch from command line
lixplore --wizard

# Launch from shell mode
lixplore> wizard
```

### Features

✅ **Guided prompts** - Answer questions, no flags to remember
✅ **Smart defaults** - Sensible defaults for most choices
✅ **Multiple workflows** - Search, annotate, view, export, download PDFs
✅ **Beginner-friendly** - Learn as you go
✅ **Examples provided** - See suggested values for tags, comments

---

### Wizard Workflows

#### 1️⃣ **Search for Articles**

```
┌────────────────────────────────────┐
│  📚 SEARCH FOR ARTICLES            │
└────────────────────────────────────┘

What do you want to search for?: cancer treatment

Which database?
  → 1. PubMed (biomedical & life sciences)
    2. arXiv (physics, math, CS, etc.)
    3. Crossref (scholarly works with DOIs)
    4. EuropePMC (European biomedical)
    5. All databases (slower but comprehensive)

Your choice [1]: 1

How many results do you want? [10]: 20

Show abstracts? [Y/n]: n

🚀 Running: search "cancer treatment" -P -m 20
```

#### 2️⃣ **Annotate an Article**

```
┌────────────────────────────────────┐
│  📝 ANNOTATE AN ARTICLE            │
└────────────────────────────────────┘

Which article number do you want to annotate?: 5

Do you want to rate this article? [Y/n]: y

Rating (1-5 stars) [4]: 5

Do you want to add tags? [Y/n]: y

💡 Examples: important, cite-in-paper, methodology, review-later
Tags (comma-separated): important,RCT,methodology

Do you want to add a comment/note? [Y/n]: y

Your comment: Excellent RCT study. Sample size calculation in methods.

Priority level?
  1. Low
  → 2. Medium
    3. High

Your choice [2]: 3

Read status?
  → 1. Unread
    2. Currently reading
    3. Finished reading

Your choice [1]: 3

🚀 Annotating article #5...

✓ Article #5 annotated successfully!
```

#### 3️⃣ **View Annotations**

```
┌────────────────────────────────────┐
│  👀 VIEW ANNOTATIONS               │
└────────────────────────────────────┘

What do you want to see?
  → 1. List all annotated articles
    2. List high-rated articles (4-5 stars)
    3. List unread articles
    4. List high-priority articles
    5. Search annotations by keyword

Your choice [1]: 2

🚀 Running: list annotations -f "min_rating=4"
```

#### 4️⃣ **Export Annotations**

```
┌────────────────────────────────────┐
│  💾 EXPORT ANNOTATIONS             │
└────────────────────────────────────┘

Export format?
  → 1. Markdown (readable, nice formatting)
    2. JSON (backup, programmatic access)
    3. CSV (spreadsheet, Excel)

Your choice [1]: 1

💡 Your annotations will be exported to:
   lixplore_annotations_markdown

Proceed with export? [Y/n]: y

🚀 Exporting...

✓ Annotations exported to: lixplore_annotations_20251228.md
```

#### 5️⃣ **Download PDFs**

```
┌────────────────────────────────────┐
│  📄 DOWNLOAD PDFs                  │
└────────────────────────────────────┘

⚠️  PDF download requires search results first

Which articles? (e.g., 1 3 5 or 1-10): 1 5 7

Use SciHub as fallback? [y/N]: n

💡 To download PDFs, use this command:
  lixplore --download-pdf --pdf-numbers 1 5 7
```

---

## 🎯 When to Use Which Mode?

### Use **Shell Mode** when:
- ✅ You're doing multiple operations in sequence
- ✅ You want to search, annotate, and export in one session
- ✅ You're comfortable with command syntax
- ✅ You want the fastest workflow (no prompts)
- ✅ You're working like a power user

### Use **Wizard Mode** when:
- ✅ You're new to Lixplore
- ✅ You forgot command syntax
- ✅ You want guided assistance
- ✅ You prefer answering questions over typing flags
- ✅ You're teaching someone to use Lixplore

### Use **Command Line** when:
- ✅ You want to automate with scripts
- ✅ You need to run a single command quickly
- ✅ You're integrating with other tools

---

## 💡 Pro Tips

### Shell Mode Tips

1. **Use command history** - Press ↑/↓ to recall commands
2. **Chain workflows** - Search → View → Annotate → Export in one session
3. **Keep it open** - Leave shell running while you work
4. **Use help** - Type `help <command>` when stuck

### Wizard Mode Tips

1. **Accept defaults** - Just press Enter for sensible defaults
2. **Examples are guides** - Look at example tags/comments provided
3. **Learn as you go** - Wizard shows you the actual commands
4. **Multiple tasks** - Wizard asks if you want to do more

### Combined Usage

**Best Workflow:**
```bash
# Start in shell mode
lixplore --shell

# Use wizard when needed
lixplore> wizard
  [Guided workflow]

# Return to shell for quick commands
lixplore> list annotations
lixplore> export markdown
```

---

## 🆚 Mode Comparison

| Feature | Shell Mode | Wizard Mode | Command Line |
|---------|-----------|-------------|--------------|
| **Speed** | ⚡⚡⚡ Fast | ⚡ Slower | ⚡⚡⚡ Fast |
| **Ease** | ⚡⚡ Moderate | ⚡⚡⚡ Easy | ⚡ Hard |
| **Guidance** | Basic help | Full guidance | Man page |
| **Persistence** | Session | Task-based | One-shot |
| **Scripting** | No | No | Yes |
| **Best For** | Power users | Beginners | Automation |

---

## 📚 Quick Reference

### Shell Mode Commands

```bash
search <query> [options]     # Search articles
list                         # List search results
list annotations             # List annotations
view <N>                     # View article details
annotate <N> [options]       # Annotate article
search-annotations <keyword> # Search annotations
export <format>              # Export annotations
stats                        # Show statistics
wizard                       # Launch wizard
help                         # Show help
exit                         # Quit shell
```

### Wizard Mode Workflows

```
1. Search for articles
2. Annotate an article
3. View my annotations
4. Export annotations
5. Download PDFs
6. Exit wizard
```

---

## 🎓 Examples

### Example 1: Literature Review in Shell Mode

```bash
$ lixplore --shell

lixplore> search "cancer immunotherapy" -P -m 50
lixplore> view 5
lixplore> annotate 5 --rating 5 --tags "must-read,checkpoint-inhibitors"
lixplore> annotate 12 --rating 4 --tags "interesting"
lixplore> annotate 18 --rating 5 --tags "cite-in-paper"
lixplore> list annotations -f "min_rating=4"
lixplore> export markdown
lixplore> exit
```

### Example 2: New User with Wizard

```bash
$ lixplore --wizard

[Chooses: Search for articles]
  Database: PubMed
  Query: diabetes treatment
  Results: 30

[Chooses: Annotate an article]
  Article: #5
  Rating: 5 stars
  Tags: important, seminal
  Comment: First RCT on metformin

[Chooses: View my annotations]
  Shows: All annotated articles

[Chooses: Export annotations]
  Format: Markdown
  Exported successfully!
```

---

## 🚀 Getting Started

### For Beginners

```bash
# Start with wizard mode
lixplore --wizard
```

Follow the prompts - it's that easy!

### For Experienced Users

```bash
# Jump into shell mode
lixplore --shell

# Run your workflow
lixplore> search "your topic" -P -m 20
lixplore> annotate 5 --rating 5 --tags "important"
lixplore> export markdown
```

---

## ❓ FAQ

**Q: Can I use shell mode and wizard mode together?**
A: Yes! Type `wizard` inside shell mode to launch guided workflows.

**Q: Do my annotations persist across sessions?**
A: Yes! All annotations are saved to `~/.lixplore_annotations.json`

**Q: Can I exit shell mode anytime?**
A: Yes! Type `exit`, `quit`, or press Ctrl+D

**Q: Does wizard mode require internet?**
A: Only for searching articles. Viewing/exporting annotations works offline.

**Q: Can I script with shell mode?**
A: No, shell mode is interactive. Use command-line mode for scripting.

---

## 🎉 Summary

Lixplore now has **3 ways to work**:

1. **Command Line** - Traditional flags (for scripting)
2. **Shell Mode** - Persistent session (for power users)
3. **Wizard Mode** - Guided workflows (for beginners)

Choose what works best for you! 🚀

---

**Happy Researching! 📚**

For more help:
- `lixplore --help`
- `man lixplore`
- [GitHub Issues](https://github.com/yourusername/lixplore/issues)
