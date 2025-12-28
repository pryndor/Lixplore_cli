# Lixplore TUI Mode - Complete User Guide

## Understanding the Two Displays

When you run `lixplore -A -q "cancer" -m 50 -i`, you see TWO displays:

### Display 1: Regular Search Results (20 per page)
```
📄 Page 1 of 13 | Showing 1-20 of 250 results
   Use -p 2 to see next page

[1] Empty node packet in endometrial cancer...
[2] Incidence of Shoulder Impairment in Breast Cancer...
...
[20] Primary Well-Differentiated Neuroendocrine Tumor...
```
**This is just a preview** - you scroll past this to get to TUI mode.

### Display 2: Interactive TUI Mode (10 per page)
```
┌─────────────────────────────────────────────────────────────┐
│          Search Results (Page 1/5)                          │
├──┬──┬───────────────────────────────────────────┬──────┬────┤
│ #│✓ │Title                                     │Year  │Src │
├──┼──┼───────────────────────────────────────────┼──────┼────┤
│ 1│  │Empty node packet in endometrial cancer   │2024  │PM  │
│ 2│  │Incidence of Shoulder Impairment...       │2024  │PM  │
│ 3│  │Comment on Pagetoid Spread...             │2024  │PM  │
│ 4│  │Beyond Reverse Transcription...           │2024  │PM  │
│ 5│  │Malnutrition at diagnosis of ALL...       │2025  │PM  │
│ 6│  │Immunization recommendations...           │2025  │PM  │
│ 7│  │Biomarkers.                               │2025  │PM  │
│ 8│  │Functionalized Biomimetic Carrier...      │2024  │PM  │
│ 9│  │Memory Deficits in Cancer Patients...     │2025  │PM  │
│10│  │Ophthalmological Findings...              │2025  │PM  │
└──┴──┴───────────────────────────────────────────┴──────┴────┘

Commands: [n]ext [p]prev [v]iew [s]elect [e]xport [q]uit [h]elp

>
```
**This is where you work** - the interactive interface.

---

## Complete Command Reference

### 📍 NAVIGATION COMMANDS

#### Command: `n` or `next`
**What it does:** Go to the next page of results

**Example:**
```
> n
```
**Result:** Shows articles 11-20

#### Command: `p` or `prev` or `previous`
**What it does:** Go to the previous page

**Example:**
```
> p
```
**Result:** Goes back to articles 1-10

#### Command: `g<NUMBER>`
**What it does:** Jump directly to a specific page

**Examples:**
```
> g3         # Jump to page 3 (shows articles 21-30)
> g1         # Jump back to page 1 (articles 1-10)
> g5         # Jump to page 5 (articles 41-50)
```

---

### 📄 ARTICLE COMMANDS

#### Command: `v` or `view`
**What it does:** View detailed information about a specific article

**How to use:**
```
> v
Enter article number to view: 5
```

**What you'll see:**
```
┌─────────────────────────────────────────────────────────────┐
│                    Article Details                           │
├──────────────────────────────────────────────────────────────┤
│ Article #5                                                   │
│                                                              │
│ Title: Malnutrition at diagnosis of acute lymphoblastic     │
│ leukemia negatively affects survival in children            │
│                                                              │
│ Authors: Garcia-Lopez E, Andrade-Gonzalez A, Martinez-Reyes │
│ B, Jimenez-Morales S, Medina-Sanson A...                    │
│                                                              │
│ Journal: Frontiers in Nutrition  Year: 2025                 │
│                                                              │
│ DOI: 10.3389/fnut.2024.1502986                              │
│                                                              │
│ URL: https://pubmed.ncbi.nlm.nih.gov/39810960               │
│                                                              │
│ Source: pubmed                                               │
│                                                              │
│ Abstract:                                                    │
│ Background: Acute lymphoblastic leukemia (ALL) is the most  │
│ common pediatric cancer. Nutritional status at diagnosis    │
│ has been associated with survival outcomes. This study...   │
└──────────────────────────────────────────────────────────────┘

Press Enter to return
```

**Tip:** View articles before selecting them to make sure they're relevant!

---

#### Command: `s` or `select`
**What it does:** Toggle selection on/off for a specific article (adds/removes checkmark ✓)

**How to use:**
```
> s
Enter article number to toggle selection: 5
✓ Article #5 selected
```

**Select multiple articles:**
```
> s
Enter article number to toggle selection: 5
✓ Article #5 selected

> s
Enter article number to toggle selection: 12
✓ Article #12 selected

> s
Enter article number to toggle selection: 23
✓ Article #23 selected

3 article(s) selected
```

**Deselect an article:**
```
> s
Enter article number to toggle selection: 12
Article #12 deselected

2 article(s) selected
```

**Important:** You can select articles from different pages! For example:
- Page 1: Select #2, #5, #8
- Page 2: Select #15, #18 (navigate with `n`)
- Page 3: Select #25 (navigate with `n`)
- Total: 6 articles selected from across 3 pages

---

#### Command: `e` or `export`
**What it does:** Export all selected articles to a file

**How to use:**
```
> e

Available export formats:
  1. CSV
  2. JSON
  3. BibTeX
  4. RIS
  5. Excel
  6. EndNote

Select format (1-6): 5

Exporting 3 article(s) to Excel...
✓ Exported to: exports/excel/cancer_2024-12-27_154523.xlsx
```

**Available Formats:**
1. **CSV** - For Excel/Google Sheets (simple)
2. **JSON** - For programming/data analysis
3. **BibTeX** - For LaTeX citations
4. **RIS** - For Zotero, Mendeley, RefWorks
5. **Excel** - For Microsoft Excel (formatted with headers)
6. **EndNote** - For EndNote reference manager

**Note:** If you try to export without selecting any articles:
```
> e
No articles selected. Select articles first with 's' command.
```

---

### ℹ️ OTHER COMMANDS

#### Command: `h` or `help`
**What it does:** Show the help screen with all available commands

```
> h
```

**Shows:**
```
┌─────────────────────────────────────────────────────────────┐
│                           Help                               │
├──────────────────────────────────────────────────────────────┤
│ Navigation Commands:                                         │
│   n, next      - Go to next page                            │
│   p, prev      - Go to previous page                        │
│   g<N>         - Go to page N (e.g., g3)                    │
│                                                              │
│ Article Commands:                                            │
│   v, view      - View detailed article information          │
│   s, select    - Toggle article selection                   │
│   e, export    - Export selected articles                   │
│                                                              │
│ Other Commands:                                              │
│   h, help      - Show this help                             │
│   q, quit      - Exit interactive mode                      │
│                                                              │
│ Tips:                                                        │
│   - Select multiple articles before exporting               │
│   - Use arrow keys in prompts to navigate history           │
│   - Press Ctrl+C to cancel any prompt                       │
└──────────────────────────────────────────────────────────────┘

Press Enter to continue
```

---

#### Command: `q` or `quit` or `exit`
**What it does:** Exit TUI mode and return to terminal

```
> q

Exiting interactive mode...
$
```

---

## Complete Workflow Examples

### Example 1: Quick Review and Export
**Goal:** Find 5 relevant cancer articles and export to Excel

```bash
# Step 1: Launch
lixplore -P -q "cancer treatment" -m 50 -i

# Step 2: Browse page 1
> v
Enter article number to view: 1
[Read abstract, decide if relevant]
Press Enter to return

> s
Enter article number to toggle selection: 1
✓ Article #1 selected

# Step 3: Continue selecting
> v
Enter article number to view: 3
[Read abstract]
Press Enter to return

> s
Enter article number to toggle selection: 3
✓ Article #3 selected

# Step 4: Check next page
> n
[Now showing articles 11-20]

> v
Enter article number to view: 12
[Read abstract]
Press Enter to return

> s
Enter article number to toggle selection: 12
✓ Article #12 selected

# Step 5: Select a couple more
> s
Enter article number to toggle selection: 15
✓ Article #15 selected

> s
Enter article number to toggle selection: 18
✓ Article #18 selected

5 article(s) selected

# Step 6: Export
> e
Select format (1-6): 5
Exporting 5 article(s) to Excel...
✓ Exported to: exports/excel/cancer_treatment_2024-12-27.xlsx

# Step 7: Exit
> q
```

---

### Example 2: Comprehensive Literature Review
**Goal:** Review 100 articles, select best 20, export to BibTeX

```bash
# Launch with 100 results
lixplore -A -q "machine learning healthcare" -m 100 -D -i

# TUI shows: Page 1/10 (10 results per page)

# Browse and select from multiple pages
> v
[View article 1]
> s
[Select article 1]

> n  # Page 2
> v
[View article 15]
> s
[Select article 15, 17, 19]

> g5  # Jump to page 5
> s
[Select articles 45, 47]

> g10  # Jump to page 10
> s
[Select articles 95, 98, 100]

# Continue until 20 articles selected

20 article(s) selected

# Export to BibTeX for LaTeX
> e
Select format (1-6): 3
✓ Exported to: exports/bibtex/ml_healthcare.bib

> q
```

---

### Example 3: Reviewing Specific Pages
**Goal:** Only interested in recent articles (page 1-2)

```bash
lixplore -P -q "COVID-19 vaccine" -m 50 --sort newest -i

# Page 1 (most recent)
> v
[View articles 1, 3, 5, 7]
> s
[Select articles 1, 3, 5, 7]

# Page 2
> n
> v
[View articles 11, 13, 15]
> s
[Select articles 11, 13, 15]

7 article(s) selected

# Export
> e
Select format (1-6): 4  # RIS for Zotero
✓ Exported

> q
```

---

## Tips & Tricks

### 1. **View Before Select**
Always use `v` to read the abstract before selecting:
```
> v
Enter article number: 5
[Read full abstract]
Press Enter

> s
Enter article number: 5  # Now select it
```

### 2. **Selection Across Pages**
Your selections persist across pages:
```
Page 1: Select #2, #5
> n
Page 2: Select #12, #15
> p
Page 1: Still shows #2, #5 selected (✓)
```

### 3. **Jump to Specific Pages**
Instead of pressing `n` multiple times:
```
> g5     # Jump straight to page 5
```

### 4. **Quick Navigation Pattern**
```
> n      # Next page
> n      # Next page
> p      # Oops, go back
> g1     # Jump to start
```

### 5. **Multiple Exports**
You can export multiple times with different selections:
```
# First export
> s
[Select articles 1, 2, 3]
> e
[Export to Excel]

# Deselect and select different ones
> s
[Deselect 1, 2, 3]
> s
[Select articles 10, 11, 12]
> e
[Export to BibTeX]
```

### 6. **Cancel Commands**
Press `Ctrl+C` to cancel any prompt:
```
> v
Enter article number: ^C
> _  # Back to main prompt
```

---

## Understanding the Display

### Table Columns
```
│ # │✓ │Title                    │Year │Source   │
│ 5 │✓ │Article title here...    │2024 │PubMed   │
  │   │                          │     │
  │   │                          │     └─── Source database
  │   │                          └────────── Publication year
  │   └───────────────────────────────────── Title (truncated)
  └──────────────────────────────────────── Checkmark if selected
  └──────────────────────────────────────── Article number
```

### Page Information
```
Page 1/5
 │    │
 │    └── Total pages (50 results ÷ 10 per page = 5 pages)
 └───────── Current page
```

### Selection Counter
```
3 article(s) selected
│
└── Total number of selected articles across all pages
```

---

## Common Issues & Solutions

### Issue 1: "Already on last page"
```
> n
Already on last page
```
**Solution:** You're on the last page. Use `p` to go back or `g1` to jump to start.

### Issue 2: "Invalid article number"
```
> s
Enter article number: 150
Invalid article number. Must be 1-50
```
**Solution:** Enter a valid article number within the range of your results.

### Issue 3: "No articles selected"
```
> e
No articles selected. Select articles first with 's' command.
```
**Solution:** Select at least one article with `s` before exporting.

### Issue 4: Can't find where article went
You selected article #35 but don't see it on current page.

**Solution:** Article #35 is on page 4. Navigate there:
```
> g4     # Jump to page 4
```
Page 4 shows articles 31-40, so #35 will be visible with a checkmark (✓).

---

## Keyboard Shortcuts Summary

| Command | Shortcut | Full Command | Description |
|---------|----------|--------------|-------------|
| Next page | `n` | `next` | Go to next page |
| Previous page | `p` | `prev` or `previous` | Go to previous page |
| Goto page | `g3` | - | Jump to page 3 |
| View article | `v` | `view` | View article details |
| Select/deselect | `s` | `select` | Toggle selection |
| Export | `e` | `export` | Export selected articles |
| Help | `h` | `help` | Show help screen |
| Quit | `q` | `quit` or `exit` | Exit TUI mode |
| Cancel | `Ctrl+C` | - | Cancel current prompt |

---

## Why Two Different Result Displays?

**Regular Display (20 results):**
- Quick preview of search results
- Shows before TUI launches
- Good for seeing if search query worked

**TUI Display (10 results per page):**
- Interactive browsing mode
- Smaller pages for easier reading
- Allows selection and export
- Better for detailed review

Think of it this way:
1. **Regular display** = Quick preview
2. **TUI mode** = Detailed workspace

---

## Practice Exercise

Try this to learn TUI mode:

```bash
# 1. Start with small search
lixplore -P -q "aspirin" -m 30 -i

# 2. In TUI mode:
> h          # Read help
> v          # View article 1
> s          # Select article 1
> n          # Next page
> v          # View article 12
> s          # Select article 12
> g1         # Jump back to page 1
> s          # Deselect article 1
> g2         # Jump to page 2
> s          # Select article 15
> e          # Export (choose Excel)
> q          # Quit
```

---

**Happy researching with Lixplore TUI mode!** 🎉
