# Your First Search

Step-by-step tutorial for your first Lixplore search.

---

## Step 1: Simple Search

Let's search PubMed for recent COVID-19 research:

```bash
lixplore -P -q "COVID-19 vaccine" -m 20
```

**What this does:**
- `-P`: Search PubMed
- `-q "COVID-19 vaccine"`: Search query
- `-m 20`: Get 20 results

**Expected output:**
```
Searching for query: COVID-19 vaccine
Sources: PubMed
  Searching PubMed...

Found 20 results:
[1] Effectiveness of COVID-19 vaccines...
[2] Safety profile of mRNA vaccines...
...
```

---

## Step 2: Add Abstracts

Now let's see abstracts:

```bash
lixplore -P -q "COVID-19 vaccine" -m 10 -a
```

**New flag:**
- `-a`: Show abstracts

---

## Step 3: Export Results

Export to Excel:

```bash
lixplore -P -q "COVID-19 vaccine" -m 50 -X xlsx -o covid_research.xlsx
```

**New flags:**
- `-X xlsx`: Export to Excel format
- `-o covid_research.xlsx`: Output filename

Check the file: `covid_research.xlsx` is created in the current directory.

---

## Step 4: Filter by Date

Search only recent publications:

```bash
lixplore -P -q "COVID-19 vaccine" -d 2024-01-01 2024-12-31 -m 30
```

**New flag:**
- `-d 2024-01-01 2024-12-31`: Date range filter

---

## Step 5: Search Multiple Sources

Search across all databases:

```bash
lixplore -A -q "machine learning healthcare" -m 50 -D
```

**New flags:**
- `-A`: All sources (PubMed, arXiv, Crossref, DOAJ, EuropePMC)
- `-D`: Deduplicate results

**Note:** With `-A`, `-m 50` means 50 per source = 250 total results.

---

## Step 6: Interactive Browsing

Browse results interactively:

```bash
lixplore -P -q "CRISPR therapy" -m 50 -i
```

**New flag:**
- `-i`: Interactive mode

**In interactive mode:**
- Use arrow keys to navigate
- Press Enter to view details
- Press 'q' to quit

---

## Step 7: Find Open Access PDFs

```bash
lixplore -x -q "neural networks" -m 20 --show-pdf-links
```

**What this does:**
- `-x`: Search arXiv (preprint server)
- `--show-pdf-links`: Show clickable PDF links

**Output:**
```
[1] Deep Learning with Neural Networks
    Open PDF → https://arxiv.org/pdf/2306.12345.pdf
```

Click the link to open the PDF!

---

## Step 8: Annotate Important Papers

```bash
# Step 1: Search
lixplore -P -q "stem cell research" -m 30

# Step 2: Annotate article #5
lixplore --annotate 5 --rating 5 --tags "important,cite" --comment "Groundbreaking work"

# Step 3: View your annotations
lixplore --list-annotations
```

---

## Complete Example: Literature Review

Let's do a complete literature review workflow:

```bash
# 1. Comprehensive search across all sources
lixplore -A -q "cancer immunotherapy" -m 100 -D --sort newest

# 2. Browse interactively
lixplore -i

# 3. Annotate key papers (replace numbers with actual article numbers)
lixplore --annotate 3 --rating 5 --tags "key-paper,cite"
lixplore --annotate 7 --rating 4 --tags "methodology"
lixplore --annotate 12 --rating 5 --tags "results,important"

# 4. Export top 50 to Excel
lixplore -S first:50 -X xlsx -o cancer_immuno_review.xlsx

# 5. Export to BibTeX for citations
lixplore -S first:50 -X bibtex -o references.bib

# 6. Export your annotations
lixplore --export-annotations markdown -o my_notes.md
```

---

## What You've Learned

- [x] Basic search with `-P -q -m`
- [x] Show abstracts with `-a`
- [x] Export to Excel with `-X xlsx`
- [x] Filter by date with `-d`
- [x] Search all sources with `-A -D`
- [x] Interactive browsing with `-i`
- [x] Find PDFs with `--show-pdf-links`
- [x] Annotate papers with `--annotate`
- [x] Complete workflow: search → annotate → export

---

## Next Steps

- Explore all [command-line flags](../reference/flags-overview.md)
- Learn [advanced filtering](../guide/filtering.md)
- See [real-world examples](../examples/workflows.md)
- Set up [automation](../advanced/automation.md)

---

**Congratulations!** You're ready to use Lixplore for your research.
