# TUI Mode - Quick Command Reference

## ✅ FIXED: Command Line Now Shows Correctly

### **What You Should See Now:**
```
Commands: (n)ext (p)rev (v)iew (s)elect (e)xport (q)uit (h)elp

>
```

### **Before (Broken):**
```
Commands: ext rev iew elect xport uit elp
         ↑ Missing letters!
```

---

## What Each Command Does

### Navigation Commands

#### `n` or `next`
**What:** Move to next page
**Type:** `n` then press Enter
**Example:**
```
> n
[Shows next 10 articles]
```

#### `p` or `prev`
**What:** Move to previous page
**Type:** `p` then press Enter
**Example:**
```
> p
[Shows previous 10 articles]
```

#### `g<NUMBER>`
**What:** Jump to specific page
**Type:** `g3` (for page 3) then press Enter
**Example:**
```
> g5
[Jumps to page 5]
```

---

### Article Commands

#### `v` or `view`
**What:** View full details of an article
**Type:** `v` then article number
**Example:**
```
> v
Enter article number to view: 12
[Shows full details of article #12]
Press Enter to return
```

#### `s` or `select`
**What:** Select/deselect article (toggle checkmark ✓)
**Type:** `s` then article number
**Example:**
```
> s
Enter article number to toggle selection: 12
✓ Article #12 selected
```

#### `e` or `export`
**What:** Export all selected articles
**Type:** `e` then choose format
**Example:**
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
✓ Exported to: exports/excel/results.xlsx
```

---

### Other Commands

#### `h` or `help`
**What:** Show help screen
**Type:** `h` then press Enter
**Example:**
```
> h
[Shows full help with all commands]
```

#### `q` or `quit`
**What:** Exit TUI mode
**Type:** `q` then press Enter
**Example:**
```
> q
Exiting interactive mode...
$
```

---

## Complete Workflow Example

```bash
# 1. Start
$ lixplore -P -q "cancer" -m 30 -i

# 2. TUI launches - you see:
┌────────────────────────────────────────┐
│ Page 1/3                               │
├──┬──┬────────────────┬──────┬──────────┤
│ 1│  │Article 1...    │2024  │PubMed    │
│ 2│  │Article 2...    │2023  │PubMed    │
...
│10│  │Article 10...   │2024  │PubMed    │
└──┴──┴────────────────┴──────┴──────────┘

Commands: (n)ext (p)rev (v)iew (s)elect (e)xport (q)uit (h)elp
           ↑     ↑     ↑      ↑        ↑       ↑      ↑
         Works! Works! Works! Works!  Works!  Works! Works!

> v                           ← Type 'v'
Enter article number: 1       ← Type '1'
[Shows article 1 details]
Press Enter                   ← Press Enter

> s                           ← Type 's'
Enter article number: 1       ← Type '1'
✓ Article #1 selected        ← Checkmark added!

> n                           ← Type 'n' (next page)
[Shows articles 11-20]

> s                           ← Type 's'
Enter article number: 15      ← Type '15'
✓ Article #15 selected

2 article(s) selected         ← Counter shows 2

> e                           ← Type 'e'
Select format (1-6): 5        ← Type '5' for Excel
✓ Exported to: exports/excel/cancer.xlsx

> q                           ← Type 'q' to quit
Exiting interactive mode...
$
```

---

## Keyboard Shortcuts (What to Type)

| Want to... | Type | Description |
|------------|------|-------------|
| **Next page** | `n` | Shows articles 11-20, 21-30, etc. |
| **Previous page** | `p` | Go back one page |
| **Jump to page 5** | `g5` | Skip directly to page 5 |
| **View article 12** | `v` then `12` | See full details |
| **Select article 12** | `s` then `12` | Add checkmark ✓ |
| **Deselect article 12** | `s` then `12` | Remove checkmark |
| **Export to Excel** | `e` then `5` | Export selected to .xlsx |
| **Export to BibTeX** | `e` then `3` | Export for LaTeX |
| **Export to RIS** | `e` then `4` | Export for Zotero/Mendeley |
| **Show help** | `h` | Display all commands |
| **Quit** | `q` | Exit and return to terminal |

---

## Tips & Tricks

### ✅ Tip 1: You Can Select from Multiple Pages!
```
Page 1: Select #2, #5
> n
Page 2: Select #12, #15
> n
Page 3: Select #25
> e  ← Exports all 5 articles!
```

### ✅ Tip 2: View Before Selecting
```
> v          # View article first
Enter: 5
[Read abstract]
Press Enter

> s          # Then select if relevant
Enter: 5
✓ Selected
```

### ✅ Tip 3: Quick Jump
```
# Instead of pressing 'n' 5 times:
> n
> n
> n
> n
> n

# Just type:
> g6         # Jump straight to page 6!
```

### ✅ Tip 4: Export Multiple Times
```
# First export
> s
[Select 1, 2, 3]
> e
[Export to Excel]

# Second export
> s
[Deselect 1, 2, 3]
> s
[Select 10, 11, 12]
> e
[Export to BibTeX]
```

---

## Troubleshooting

### Problem: "Commands: ext rev iew..." (letters cut off)
**Solution:** This is now FIXED! Update your code and you'll see:
```
Commands: (n)ext (p)rev (v)iew (s)elect (e)xport (q)uit (h)elp
```

### Problem: "Already on last page"
**Cause:** You're on the last page already
**Solution:** Type `p` to go back or `g1` to go to first page

### Problem: "Invalid article number"
**Cause:** Article number doesn't exist
**Solution:** Enter a number between 1 and total results (e.g., 1-50)

### Problem: "No articles selected"
**Cause:** You tried to export without selecting anything
**Solution:** Select at least one article with `s` before using `e`

---

## Remember

1. **Type the letter + Enter** for each command
2. **Selections persist** across pages
3. **View before selecting** to avoid exporting irrelevant articles
4. **You can select from different pages** - all selections are remembered
5. **Export as many times as you want** with different selections

---

**Happy researching!** 🎉
