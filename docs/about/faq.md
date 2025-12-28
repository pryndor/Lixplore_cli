# Frequently Asked Questions (FAQ)

---

## General Questions

### What is Lixplore?

Lixplore is a command-line tool for searching, filtering, exporting, and managing academic literature from multiple sources including PubMed, arXiv, Crossref, DOAJ, and EuropePMC.

### Is Lixplore free?

Yes, Lixplore is completely free and open source under the MIT License.

### Does Lixplore include AI/ML models?

No. Lixplore is purely a search and export tool. It has no machine learning dependencies, making it lightweight and fast. However, it's easy to integrate with AI services like OpenAI or Gemini through JSON export.

### What platforms does Lixplore support?

Lixplore works on Linux, macOS, and Windows with Python 3.8 or higher.

---

## Installation & Setup

### How do I install Lixplore?

```bash
pip install lixplore
```

See the [Installation Guide](../getting-started/installation.md) for details.

### I get "command not found" after installing

Add pip's bin directory to your PATH:

```bash
export PATH=$PATH:~/.local/bin
```

Add this to your `~/.bashrc` or `~/.zshrc` to make it permanent.

### How do I upgrade to the latest version?

```bash
pip install --upgrade lixplore
```

---

## Usage Questions

### How many results can I fetch?

You can fetch as many as you want using the `-m` flag. For example:

```bash
lixplore -P -q "topic" -m 1000
```

Note: With `-A` (all sources), `-m` applies per source.

### Why do I get more results than I requested?

When using `-A` (all sources), the `-m` flag applies **per source**. For example:

```bash
lixplore -A -q "topic" -m 50
# Returns: 5 sources × 50 = 250 results
```

Use `-D` (deduplicate) to reduce duplicates:

```bash
lixplore -A -q "topic" -m 50 -D
```

### How do I search specific date ranges?

Use the `-d` flag:

```bash
lixplore -P -q "topic" -d 2023-01-01 2024-12-31
```

### Can I search by author?

Yes, use the `-au` flag:

```bash
lixplore -P -au "Smith J" -m 50
```

### How do I find open access PDFs?

```bash
# Show clickable PDF links
lixplore -x -q "topic" -m 50 --show-pdf-links

# Download PDFs
lixplore -x -q "topic" -m 50 --download-pdf
```

---

## Export Questions

### What export formats are supported?

Lixplore supports 10+ formats:

- CSV, Excel (XLSX), JSON, XML
- BibTeX, RIS
- EndNote (Tagged & XML)
- Citations (APA, MLA, Chicago, Harvard, Vancouver, IEEE)

### How do I export to Excel?

```bash
lixplore -P -q "topic" -m 100 -X xlsx -o results.xlsx
```

### How do I export only specific fields?

Use `--export-fields`:

```bash
lixplore -P -q "topic" -m 100 -X csv --export-fields title authors year doi -o results.csv
```

### Can I export in multiple formats at once?

Yes:

```bash
lixplore -P -q "topic" -m 100 -X csv,bibtex,xlsx
```

Add `--zip` to package them:

```bash
lixplore -P -q "topic" -m 100 -X csv,bibtex,xlsx --zip
```

---

## Annotation Questions

### How do I annotate articles?

```bash
# First, search to see results with numbers
lixplore -P -q "topic" -m 50

# Then annotate by number
lixplore --annotate 5 --rating 5 --tags "important,cite"
lixplore --annotate 12 --comment "Interesting methodology"
```

### Where are annotations stored?

In `~/.lixplore_annotations.json`

You can back up this file to preserve your annotations.

### How do I view my annotations?

```bash
# List all
lixplore --list-annotations

# Filter by rating
lixplore --filter-annotations --rating 5

# Search annotations
lixplore --search-annotations "CRISPR"
```

### How do I export annotations?

```bash
lixplore --export-annotations markdown  # Markdown format
lixplore --export-annotations json      # JSON format
lixplore --export-annotations csv       # CSV format
```

---

## Interactive Mode Questions

### How do I use interactive mode?

```bash
# Launch with search results
lixplore -P -q "topic" -m 50 -i

# Or launch standalone
lixplore -i
```

### What's the difference between -i and --tui?

- `-i` or `--interactive`: Simple TUI for browsing results
- `--tui`: Enhanced TUI with more features (search, stats, etc.)

### Can I annotate in interactive mode?

Yes, the enhanced TUI (`--tui`) supports annotations. The simple TUI (`-i`) is for browsing only.

---

## Automation Questions

### Can I use Lixplore in cron jobs?

Yes! Lixplore is designed for automation:

```bash
# Add to crontab
0 9 * * * lixplore -P -q "topic" -m 50 -X csv -o /path/to/daily_$(date +\%Y\%m\%d).csv
```

See [Automation Guide](../advanced/automation.md) for more examples.

### How do I save search configurations?

Use profiles:

```bash
# Save configuration
lixplore -P -q "test" -m 100 -D --sort newest --save-profile my_profile

# Reuse configuration
lixplore -q "new topic" --load-profile my_profile
```

### Where are files saved?

- **PDFs**: `~/Lixplore_PDFs/`
- **Exports**: `./exports/` (or specify with `-o`)
- **Annotations**: `~/.lixplore_annotations.json`
- **Cache**: `~/.lixplore_cache.json`
- **Profiles**: `~/.lixplore/profiles.json`

---

## Performance Questions

### How fast is Lixplore?

Lixplore is very fast:

- No ML overhead
- Efficient API calls
- 7-day result caching
- Parallel source queries

### Does Lixplore cache results?

Yes, results are cached for 7 days. To refresh:

```bash
lixplore -P -q "topic" -m 50 --refresh
```

### Why is my first search slow?

The first search to each API may be slower. Subsequent searches use caching and are much faster.

---

## Integration Questions

### Can I integrate with OpenAI/Gemini?

Yes! Export to JSON and pipe to your AI script:

```bash
lixplore -P -q "topic" -m 100 -X json | python3 ai_analysis.py
```

See [AI Integration Guide](../advanced/ai-integration.md).

### Does Lixplore work with Zotero?

Yes:

```bash
lixplore --configure-zotero YOUR_API_KEY YOUR_USER_ID
lixplore -P -q "topic" -m 50 --add-to-zotero
```

See [Zotero Integration](../advanced/zotero.md).

### Can I use with other tools?

Yes, Lixplore integrates well with:

- `jq` for JSON processing
- `csvkit` for CSV analysis
- Citation managers (BibTeX, RIS, EndNote)
- Spreadsheet software (Excel, LibreOffice)
- Any tool that accepts JSON, CSV, or XML

---

## Troubleshooting

### "No results found"

Try:
1. Broaden your query
2. Check spelling
3. Try different sources (`-A` for all)
4. Remove date filters
5. Use `--refresh` to bypass cache

### "API error" or "Connection failed"

Check:
1. Internet connection
2. API service status (PubMed, arXiv, etc.)
3. Try again later (may be temporary)

### Results look duplicated

Use deduplication:

```bash
lixplore -A -q "topic" -m 100 -D
```

### Export file is empty

Check:
1. Search returned results
2. Output path is writable
3. Correct export format specified

### "Permission denied" when saving files

Either:
1. Specify a path you have write access to: `-o ~/results.xlsx`
2. Run from a directory where you have write permissions

---

## Feature Requests

### How do I request a new feature?

Open an issue on GitHub:
https://github.com/pryndor/Lixplore_cli/issues

### Can you add support for [database X]?

Possibly! Either:
1. Open a feature request on GitHub
2. Use the [Custom API feature](../advanced/custom-apis.md) to add it yourself

### Will you add a GUI?

Lixplore is designed as a CLI-first tool for automation and scripting. However, the interactive TUI modes provide a visual interface.

---

## Contributing

### How can I contribute?

See [Contributing Guide](contributing.md).

### I found a bug

Report it on GitHub:
https://github.com/pryndor/Lixplore_cli/issues

### Can I add my own features?

Yes! Lixplore is open source. Fork, modify, and submit a pull request.

---

## Licensing

### What license is Lixplore under?

MIT License. See [License](license.md).

### Can I use Lixplore commercially?

Yes, the MIT license allows commercial use.

### Do I need to cite Lixplore in my research?

Not required, but appreciated! Citation info coming soon.

---

## Still Have Questions?

- Check the [full documentation](../index.md)
- Open an issue: https://github.com/pryndor/Lixplore_cli/issues
- View examples: [Workflows](../examples/workflows.md)

