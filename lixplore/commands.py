#!/usr/bin/env python3

import argparse
import json
import os
from . import dispatcher


def add_commands(parser: argparse.ArgumentParser):
    """Register CLI arguments for lixplore."""
    
    # Custom description and epilog for detailed help
    parser.description = """
Lixplore - Academic Literature Search & Export Tool

Search across multiple academic databases (PubMed, Crossref, DOAJ, EuropePMC, arXiv)
and export results in various formats (CSV, Excel, JSON, BibTeX, RIS, EndNote, XML).
"""
    
    parser.epilog = """
EXAMPLES:
  Basic search:
    lixplore -P -q "cancer treatment" -m 10
    
  Multi-source search with export:
    lixplore -s PX -q "machine learning" -m 20 -X xlsx -o ml_papers.xlsx
    
  Search all sources with deduplication:
    lixplore -A -q "COVID-19" -m 50 -D -X csv
    
  Search with date filter and abstracts:
    lixplore -P -q "diabetes" -d 2020-01-01 2024-12-31 -m 15 -a
    
  Search by author:
    lixplore -P -au "Smith J" -m 10 -a
    
  Export to EndNote:
    lixplore -P -q "neuroscience" -m 30 -X enw -o neuro_papers.enw
    
  Review articles in separate terminal (two-step):
    lixplore -P -q "paracetamol" -m 10       # Step 1: Search
    lixplore -R 1 5 9                         # Step 2: Review articles #1, #5, #9
    # In review window: Press 'q' or Ctrl+C to close

SOURCE CODES (for -s flag):
  P = PubMed       C = Crossref     J = DOAJ
  E = EuropePMC    X = arXiv        A = All sources
  
  Examples: -s PX (PubMed+arXiv), -s PCE (PubMed+Crossref+EuropePMC)

EXPORT FORMATS:
  csv      - CSV format (Excel, Google Sheets)
  xlsx     - Microsoft Excel format with formatting
  json     - JSON structured data
  bibtex   - BibTeX format for LaTeX citations
  ris      - RIS format (Zotero, Mendeley, RefWorks)
  enw      - EndNote Tagged format (recommended for EndNote)
  endnote  - EndNote XML format
  xml      - Generic XML format

EXPORT LOCATIONS:
  All exports are automatically saved to organized folders:
    exports/csv/              - CSV files
    exports/excel/            - Excel files
    exports/json/             - JSON files
    exports/bibtex/           - BibTeX files
    exports/ris/              - RIS files
    exports/endnote_tagged/   - EndNote .enw files
    exports/endnote_xml/      - EndNote XML files
    exports/xml/              - Generic XML files

For more information, visit: https://github.com/yourusername/lixplore
"""

    # ===== SOURCE SELECTION =====
    source_group = parser.add_argument_group(
        '[SOURCE SELECTION]',
        'Choose which academic databases to search'
    )
    
    source_group.add_argument(
        "-P", "--pubmed", action="store_true",
        help="Search PubMed (biomedical and life sciences literature)"
    )
    source_group.add_argument(
        "-C", "--crossref", action="store_true",
        help="Search Crossref (scholarly works with DOIs)"
    )
    source_group.add_argument(
        "-J", "--doaj", action="store_true",
        help="Search DOAJ - Directory of Open Access Journals"
    )
    source_group.add_argument(
        "-E", "--europepmc", action="store_true",
        help="Search EuropePMC (Europe PubMed Central)"
    )
    source_group.add_argument(
        "-x", "--arxiv", action="store_true",
        help="Search arXiv (preprint repository for physics, math, CS, etc.)"
    )
    source_group.add_argument(
        "-A", "--all", action="store_true",
        help="Search ALL sources at once (PubMed, Crossref, DOAJ, EuropePMC, arXiv)"
    )
    source_group.add_argument(
        "-s", "--sources", type=str, metavar="CODES",
        help="Combined source selection using codes: P=PubMed, C=Crossref, J=DOAJ, E=EuropePMC, X=arXiv, A=All. Example: -s PX for PubMed+arXiv, -s PCJE for multiple"
    )
    source_group.add_argument(
        "--custom-api", type=str, metavar="NAME",
        help="Use a custom API source (Springer, BASE, etc.). Must be configured in ~/.lixplore/apis/ or ~/.lixplore/custom_apis.json. Example: --custom-api springer"
    )
    
    # ===== SEARCH PARAMETERS =====
    search_group = parser.add_argument_group(
        '[SEARCH PARAMETERS]',
        'Define what and how to search'
    )
    
    search_group.add_argument(
        "-q", "--query", type=str, metavar="TEXT",
        help="Search query string. Supports Boolean operators: AND, OR, NOT, parentheses for grouping. Examples: -q \"cancer treatment\" | -q \"cancer AND treatment\" | -q \"(cancer OR tumor) AND treatment\" | -q \"diabetes NOT type1\""
    )
    search_group.add_argument(
        "-au", "--author", type=str, metavar="NAME",
        help="Search by author name. Example: -au \"Smith J\" or -au \"Einstein A\""
    )
    search_group.add_argument(
        "-DOI", "--doi", type=str, metavar="DOI",
        help="Search for a specific article by DOI. Example: -DOI \"10.1038/nature12345\""
    )
    search_group.add_argument(
        "-m", "--max_results", type=int, default=10, metavar="N",
        help="Maximum number of results to fetch per source (default: 10). Example: -m 50"
    )
    
    # ===== FILTERING & PROCESSING =====
    filter_group = parser.add_argument_group(
        '[FILTERING & PROCESSING]',
        'Filter and process search results'
    )
    
    filter_group.add_argument(
        "-d", "--date", nargs=2, metavar=("FROM", "TO"),
        help="Filter by publication date range in YYYY-MM-DD format. Example: -d 2020-01-01 2024-12-31"
    )
    filter_group.add_argument(
        "-D", "--deduplicate", nargs="?", const="auto", metavar="STRATEGY",
        choices=["auto", "doi_only", "title_only", "strict", "loose"],
        help="Remove duplicate results. Strategies: auto (default, multi-level), doi_only (DOI matching only), title_only (title similarity only), strict (high threshold 0.95), loose (low threshold 0.75). Example: -D or -D strict"
    )
    filter_group.add_argument(
        "--dedup-threshold", type=float, default=0.85, metavar="FLOAT",
        help="Title similarity threshold for deduplication (0.0-1.0). Default: 0.85. Example: --dedup-threshold 0.9"
    )
    filter_group.add_argument(
        "--dedup-keep", type=str,
        choices=["first", "most_complete", "prefer_doi"],
        default="most_complete", metavar="STRATEGY",
        help="Which duplicate to keep: first (chronological), most_complete (most metadata), prefer_doi (prefer entries with DOI). Default: most_complete"
    )
    filter_group.add_argument(
        "--dedup-merge", action="store_true",
        help="Merge metadata from duplicates instead of discarding. Combines best data from all duplicates."
    )
    filter_group.add_argument(
        "--sort", type=str, choices=["relevant", "newest", "oldest", "journal", "author"],
        default="relevant", metavar="ORDER",
        help="Sort results by: relevant (default/original order), newest (latest first), oldest (earliest first), journal (alphabetical), author (by first author). Example: --sort newest"
    )
    filter_group.add_argument(
        "--enrich", nargs="*", metavar="API",
        choices=["crossref", "pubmed", "arxiv", "all"],
        help="Enrich metadata using external APIs. Use without arguments for all, or specify: crossref, pubmed, arxiv. Automatically validates and finds missing DOIs. Example: --enrich or --enrich crossref pubmed"
    )

    # ===== DISPLAY OPTIONS =====
    display_group = parser.add_argument_group(
        '[DISPLAY OPTIONS]',
        'Control how results are displayed'
    )
    
    display_group.add_argument(
        "-a", "--abstract", action="store_true",
        help="Display abstracts along with titles in the results"
    )
    display_group.add_argument(
        "-i", "--interactive", action="store_true",
        help="Launch simple interactive TUI mode for searching and browsing (can be used standalone: lixplore -i)"
    )
    display_group.add_argument(
        "-N", "--number", type=int, nargs="+", default=[], metavar="N",
        help="View detailed information for specific article(s) by number. Example: -N 1 or -N 1 2 3"
    )
    display_group.add_argument(
        "-R", "--review", type=int, nargs="+", default=[], metavar="N",
        help="Open article(s) in separate terminal window for detailed review. Two modes: 1) With search: -P -q 'query' -R 1 2, or 2) Standalone: lixplore -R 1 2 (uses cached results). Close window with 'q' or Ctrl+C. Example: -R 1 or -R 1 2 3"
    )
    display_group.add_argument(
        "--stat", action="store_true",
        help="Show comprehensive statistics dashboard with visualizations (publication trends, top journals, top authors, source distribution)"
    )
    display_group.add_argument(
        "--stat-top", type=int, default=10, metavar="N",
        help="Number of top items to show in statistics rankings (default: 10)"
    )
    display_group.add_argument(
        "-p", "--page", type=int, default=1, metavar="N",
        help="Page number to display when results exceed page size (default: 1). Example: -p 2"
    )
    display_group.add_argument(
        "--page-size", type=int, default=20, metavar="N",
        help="Number of results to display per page (default: 20). Example: --page-size 50"
    )
    display_group.add_argument(
        "--show-pdf-links", action="store_true",
        help="Display PDF links for open access articles (from PMC, arXiv, Unpaywall). Links are clickable in modern terminals. Example: -P -q 'cancer' --show-pdf-links"
    )

    # ===== EXPORT & OUTPUT =====
    export_group = parser.add_argument_group(
        '[EXPORT & OUTPUT]',
        'Export results in various formats'
    )
    
    export_group.add_argument(
        "-X", "--export", type=str,
        metavar="FORMAT",
        help="Export results to format(s). Single format: csv, json, bibtex, ris, endnote (XML), enw (EndNote Tagged), xlsx (Excel), xml. Multiple formats (comma-separated): csv,ris,bibtex. Files saved to exports/ folder. Example: -X csv or -X csv,ris,bibtex"
    )
    export_group.add_argument(
        "-o", "--output", type=str, metavar="FILE",
        help="Custom output filename for export (default: auto-generated with timestamp). Example: -o my_results.csv"
    )
    export_group.add_argument(
        "-S", "--select", nargs="+", default=[], metavar="SELECTION",
        help="Select article(s) to export. Supports: numbers (1 3 5), ranges (1-10), keywords (odd, even, first:N, last:N, top:N). Examples: -S 1 3 5 | -S odd | -S even | -S 1-10 | -S first:5 | -S last:3 | -S top:10. Without this flag, all results are exported."
    )
    export_group.add_argument(
        "--export-fields", type=str, nargs="+", metavar="FIELD",
        help="Select specific fields to export. Available fields: title, authors, abstract, journal, year, doi, url, source. Example: --export-fields title authors year doi"
    )
    export_group.add_argument(
        "--zip", action="store_true",
        help="Compress exported file(s) to ZIP format. Example: -X csv --zip"
    )
    export_group.add_argument(
        "-c", "--citations", type=str,
        choices=["apa", "mla", "chicago", "ieee"],
        metavar="STYLE",
        help="Export as formatted citations. Styles: apa, mla, chicago, ieee. Example: -c apa or --citations apa"
    )
    export_group.add_argument(
        "--save-profile", type=str, metavar="NAME",
        help="Save current export settings as a reusable profile. Example: --save-profile my_nature_export"
    )
    export_group.add_argument(
        "--load-profile", type=str, metavar="NAME",
        help="Load previously saved export profile. Example: --load-profile my_nature_export"
    )
    export_group.add_argument(
        "--template", type=str, metavar="NAME",
        help="Use predefined export template. Available: nature, science, ieee. Example: --template nature. Use --list-templates to see all"
    )
    export_group.add_argument(
        "--download-pdf", action="store_true",
        help="Download full-text PDFs for search results. Tries PMC, arXiv, DOI resolution, and optionally SciHub. PDFs saved to ~/Lixplore_PDFs/"
    )
    export_group.add_argument(
        "--pdf-numbers", type=int, nargs="+", metavar="N",
        help="Download PDFs only for specific article numbers. Example: --pdf-numbers 1 3 5"
    )
    export_group.add_argument(
        "--use-scihub", action="store_true",
        help="Use SciHub as fallback for PDF download (requires --set-scihub-mirror configuration). Use at your own discretion."
    )
    export_group.add_argument(
        "--add-to-zotero", action="store_true",
        help="Add search results to Zotero library (requires Zotero API configuration)"
    )
    export_group.add_argument(
        "--zotero-collection", type=str, metavar="KEY",
        help="Zotero collection key to add items to (use with --add-to-zotero)"
    )
    export_group.add_argument(
        "--export-for-mendeley", action="store_true",
        help="Export results as RIS file for Mendeley Desktop import"
    )

    # ===== UTILITY =====
    utility_group = parser.add_argument_group(
        '[UTILITY]',
        'Additional utility options'
    )
    
    utility_group.add_argument(
        "-H", "--history", action="store_true",
        help="Show search history"
    )
    utility_group.add_argument(
        "--refresh", action="store_true",
        help="Bypass cache and fetch fresh results (ignore cached data)"
    )
    utility_group.add_argument(
        "--examples", action="store_true",
        help="Show quick examples (tldr-style) and exit"
    )
    utility_group.add_argument(
        "--list-profiles", action="store_true",
        help="List all saved export profiles"
    )
    utility_group.add_argument(
        "--delete-profile", type=str, metavar="NAME",
        help="Delete saved export profile"
    )
    utility_group.add_argument(
        "--list-templates", action="store_true",
        help="List all available export templates"
    )
    utility_group.add_argument(
        "--list-custom-apis", action="store_true",
        help="List all configured custom API sources"
    )
    utility_group.add_argument(
        "--create-api-examples", action="store_true",
        help="Create example custom API configurations (Springer, BASE, etc.)"
    )
    utility_group.add_argument(
        "--set-scihub-mirror", type=str, metavar="URL",
        help="Configure SciHub mirror URL for PDF downloads. Example: --set-scihub-mirror https://sci-hub.se"
    )
    utility_group.add_argument(
        "--show-pdf-dir", action="store_true",
        help="Show PDF download directory location"
    )
    utility_group.add_argument(
        "--configure-zotero", nargs=2, metavar=("API_KEY", "USER_ID"),
        help="Configure Zotero API access. Get API key from https://www.zotero.org/settings/keys"
    )
    utility_group.add_argument(
        "--show-zotero-collections", action="store_true",
        help="List Zotero collections with their keys"
    )

    # ===== INTERACTIVE MODES =====
    mode_group = parser.add_argument_group(
        '[INTERACTIVE MODES]',
        'Enhanced interactive experiences for easier usage'
    )

    mode_group.add_argument(
        "--tui", action="store_true",
        help="Launch enhanced TUI (Text User Interface) mode - the primary interactive interface. Includes search, annotation, statistics, and export in a beautiful visual interface. This is the DEFAULT when no query is provided."
    )
    mode_group.add_argument(
        "--shell", action="store_true",
        help="[Deprecated - use --tui instead] Launch interactive shell mode."
    )
    mode_group.add_argument(
        "--wizard", action="store_true",
        help="[Deprecated - use --tui instead] Launch wizard mode."
    )

    # ===== ANNOTATIONS =====
    annotation_group = parser.add_argument_group(
        '[ANNOTATIONS]',
        'Annotate, rate, and organize articles'
    )

    annotation_group.add_argument(
        "--annotate", type=int, metavar="N",
        help="Annotate article #N from last search. Use with --comment, --rating, --tags, etc. Example: --annotate 5 --rating 4 --tags 'important,methodology'"
    )
    annotation_group.add_argument(
        "--comment", type=str, metavar="TEXT",
        help="Add comment/note to article (use with --annotate). Example: --annotate 3 --comment 'Excellent methodology section'"
    )
    annotation_group.add_argument(
        "--rating", type=int, choices=[1, 2, 3, 4, 5], metavar="1-5",
        help="Rate article 1-5 stars (use with --annotate). Example: --annotate 3 --rating 5"
    )
    annotation_group.add_argument(
        "--tags", type=str, metavar="TAGS",
        help="Add comma-separated tags (use with --annotate). Example: --annotate 3 --tags 'important,review-later,cite'"
    )
    annotation_group.add_argument(
        "--read-status", type=str, choices=['unread', 'reading', 'read'], metavar="STATUS",
        help="Set read status: unread, reading, read (use with --annotate). Example: --annotate 3 --read-status read"
    )
    annotation_group.add_argument(
        "--priority", type=str, choices=['low', 'medium', 'high'], metavar="LEVEL",
        help="Set priority level: low, medium, high (use with --annotate). Example: --annotate 3 --priority high"
    )
    annotation_group.add_argument(
        "--show-annotation", type=int, metavar="N",
        help="Show annotation for article #N from last search"
    )
    annotation_group.add_argument(
        "--list-annotations", action="store_true",
        help="List all annotated articles"
    )
    annotation_group.add_argument(
        "--filter-annotations", type=str, metavar="FILTERS",
        help="Filter annotations. Format: key=value,key=value. Keys: min_rating, read_status, priority, tag. Example: --filter-annotations 'min_rating=4,priority=high'"
    )
    annotation_group.add_argument(
        "--search-annotations", type=str, metavar="QUERY",
        help="Search annotations by keyword in comments, tags, or title. Example: --search-annotations 'methodology'"
    )
    annotation_group.add_argument(
        "--export-annotations", type=str, choices=['markdown', 'json', 'csv'], metavar="FORMAT",
        help="Export all annotations to file. Formats: markdown, json, csv. Example: --export-annotations markdown"
    )
    annotation_group.add_argument(
        "--annotation-stats", action="store_true",
        help="Show annotation statistics (total, ratings distribution, tags, etc.)"
    )
    annotation_group.add_argument(
        "--delete-annotation", type=int, metavar="N",
        help="Delete annotation for article #N from last search"
    )

    parser.set_defaults(func=run_main)


def sort_results(results, sort_order):
    """
    Sort results based on specified order.
    
    Args:
        results: List of article dictionaries
        sort_order: Sort order (relevant, newest, oldest, journal, author)
    
    Returns:
        Sorted list of articles
    """
    if not results or sort_order == "relevant":
        # Keep original order (most relevant from API)
        return results
    
    sorted_results = results.copy()
    
    if sort_order == "newest":
        # Sort by year descending (newest first)
        sorted_results.sort(key=lambda x: x.get('year', 0), reverse=True)
    
    elif sort_order == "oldest":
        # Sort by year ascending (oldest first)
        sorted_results.sort(key=lambda x: x.get('year', 9999))
    
    elif sort_order == "journal":
        # Sort by journal name alphabetically
        sorted_results.sort(key=lambda x: (x.get('journal', '') or '').lower())
    
    elif sort_order == "author":
        # Sort by first author's last name
        def get_first_author_last_name(article):
            authors = article.get('authors', [])
            if authors and len(authors) > 0:
                # Get first author, try to extract last name
                first_author = authors[0]
                # Assume last name is the last word
                parts = first_author.split()
                return parts[-1].lower() if parts else ''
            return ''
        
        sorted_results.sort(key=get_first_author_last_name)
    
    return sorted_results


def parse_selection(selection_args, total_results):
    """
    Parse selection arguments and return list of article indices.
    
    Supports:
    - Numbers: 1 3 5
    - Ranges: 1-10, 5-15
    - Keywords: odd, even
    - First N: first:5, top:5
    - Last N: last:3
    
    Args:
        selection_args: List of selection arguments
        total_results: Total number of results available
    
    Returns:
        List of article numbers (1-based)
    """
    selected = set()
    
    for arg in selection_args:
        arg = str(arg).lower()
        
        # Keyword: odd
        if arg == 'odd':
            selected.update(range(1, total_results + 1, 2))
        
        # Keyword: even
        elif arg == 'even':
            selected.update(range(2, total_results + 1, 2))
        
        # Keyword: first:N or top:N
        elif arg.startswith('first:') or arg.startswith('top:'):
            try:
                n = int(arg.split(':')[1])
                selected.update(range(1, min(n + 1, total_results + 1)))
            except (ValueError, IndexError):
                print(f"Warning: Invalid format '{arg}'. Use 'first:N' or 'top:N'")
        
        # Keyword: last:N
        elif arg.startswith('last:'):
            try:
                n = int(arg.split(':')[1])
                start = max(1, total_results - n + 1)
                selected.update(range(start, total_results + 1))
            except (ValueError, IndexError):
                print(f"Warning: Invalid format '{arg}'. Use 'last:N'")
        
        # Range: 1-10
        elif '-' in arg and not arg.startswith('-'):
            try:
                start, end = arg.split('-')
                start, end = int(start), int(end)
                if start > end:
                    start, end = end, start
                selected.update(range(start, min(end + 1, total_results + 1)))
            except ValueError:
                print(f"Warning: Invalid range '{arg}'. Use format: 1-10")
        
        # Single number
        else:
            try:
                num = int(arg)
                if 1 <= num <= total_results:
                    selected.add(num)
                else:
                    print(f"Warning: Article #{num} is out of range (1-{total_results})")
            except ValueError:
                print(f"Warning: Unrecognized selection '{arg}'")
    
    return sorted(list(selected))


def _supports_unicode_output() -> bool:
    """Return True if stdout can encode common Unicode characters (emojis/box)."""
    import sys
    test_string = "═│"
    try:
        test_string.encode(sys.stdout.encoding or "utf-8")
        return True
    except Exception:
        return False


def _examples_text(unicode_ok: bool) -> str:
    if unicode_ok:
        return """
╔═══════════════════════════════════════════════════════════════════════╗
║                    LIXPLORE - Quick Examples                          ║
╚═══════════════════════════════════════════════════════════════════════╝

BASIC SEARCH
  Search PubMed for a query:
    $ lixplore -P -q "cancer treatment" -m 10

  Search with abstracts:
    $ lixplore -P -q "diabetes" -m 5 -a

MULTI-SOURCE SEARCH
  Search PubMed + arXiv:
    $ lixplore -s PX -q "machine learning" -m 20

  Search all sources with deduplication:
    $ lixplore -A -q "COVID-19" -m 50 -D

EXPORT RESULTS
  Export to Excel:
    $ lixplore -P -q "neuroscience" -m 15 -X xlsx -o brain_research.xlsx

  Export to EndNote Tagged:
    $ lixplore -P -q "quantum physics" -m 20 -X enw -o physics.enw

  Export to CSV:
    $ lixplore -P -q "climate change" -m 30 -X csv

  Export to BibTeX:
    $ lixplore -P -q "artificial intelligence" -m 25 -X bibtex

ADVANCED SEARCH
  Search with date filter:
    $ lixplore -P -q "vaccine development" -d 2020-01-01 2024-12-31 -m 15

  Search by author:
    $ lixplore -P -au "Smith J" -m 10 -a

  Search by DOI:
    $ lixplore -DOI "10.1038/nature12345"

🔤 BOOLEAN OPERATORS (Advanced Query Syntax)
  AND operator (both terms required):
    $ lixplore -P -q "cancer AND treatment" -m 10

  OR operator (either term):
    $ lixplore -P -q "cancer OR tumor" -m 10

  NOT operator (exclude term):
    $ lixplore -P -q "diabetes NOT type1" -m 10

  Complex queries with parentheses:
    $ lixplore -P -q "(cancer OR tumor) AND (treatment OR therapy)" -m 20

  Combine with other features:
    $ lixplore -A -q "COVID-19 AND vaccine" -m 50 -D --sort newest -X xlsx

🔄 COMBINED FEATURES
  Multi-source search with export and deduplication:
    $ lixplore -s PCE -q "gene therapy" -m 30 -D -X xlsx -o genes.xlsx

  Search with date filter, abstracts, and export:
    $ lixplore -P -q "cancer immunotherapy" -d 2023-01-01 2024-12-31 -a -m 20 -X json

📖 REVIEW ARTICLES (Two-Step Workflow)
  Step 1 - Search and cache results:
    $ lixplore -P -q "diabetes" -m 10

  Step 2 - Review specific articles:
    $ lixplore -R 2           # Review article #2
    $ lixplore -R 1 5 9       # Review multiple articles

  One-step (search + review):
    $ lixplore -P -q "aspirin" -m 10 -R 1 3 5

  In review window:
    Press 'q' or Ctrl+C to close (won't close with other keys)

🔢 SMART SELECTION (Export Specific Articles)
  Export odd-numbered articles:
    $ lixplore -P -q "research" -m 50 -S odd -X csv

  Export even-numbered articles:
    $ lixplore -P -q "study" -m 50 -S even -X xlsx

  Export first 10 articles:
    $ lixplore -P -q "cancer" -m 50 -S first:10 -X enw

  Export last 5 articles:
    $ lixplore -P -q "science" -m 30 -S last:5 -X csv

  Export specific range:
    $ lixplore -P -q "biology" -m 50 -S 10-20 -X xlsx

  Mixed selection (combine patterns):
    $ lixplore -P -q "chemistry" -m 50 -S 1 3 5-10 odd -X csv

SORT RESULTS
  Sort by newest (latest first):
    $ lixplore -P -q "COVID-19" -m 50 --sort newest

  Sort by oldest (historical research):
    $ lixplore -P -q "diabetes" -m 50 --sort oldest

  Sort by journal (alphabetical):
    $ lixplore -A -q "AI" -m 50 -D --sort journal

  Sort by author (alphabetical):
    $ lixplore -P -q "physics" -m 50 --sort author

  Combine sort + selection + export:
    $ lixplore -P -q "cancer" -m 50 --sort newest -S first:10 -X xlsx

PDF LINKS (Display without downloading)
  Show clickable PDF links for open access articles:
    $ lixplore -x -q "neural networks" -m 10 --show-pdf-links

  Combine with abstracts:
    $ lixplore -P -q "cancer" -m 20 -a --show-pdf-links

  Multi-source with PDF links:
    $ lixplore -A -q "COVID-19" -m 50 -D --show-pdf-links

  Links work in modern terminals (iTerm2, GNOME Terminal, Windows Terminal)
  Click to open PDF in browser - no download required!

SOURCE CODES (for -s flag)
  P = PubMed       C = Crossref      J = DOAJ
  E = EuropePMC    X = arXiv         A = All sources

EXPORT FORMATS
  csv      - CSV (Excel, Google Sheets)
  xlsx     - Excel with formatting
  json     - JSON structured data
  bibtex   - BibTeX for LaTeX
  ris      - RIS (Zotero, Mendeley)
  enw      - EndNote Tagged (recommended)
  endnote  - EndNote XML
  xml      - Generic XML

Export locations: All files saved to exports/ folder
   (organized by format: exports/csv/, exports/excel/, etc.)

TIP: Use -D flag when searching multiple sources to remove duplicates
TIP: Use -a flag to see abstracts in results
TIP: Use -R for detailed review in separate windows (press 'q' to close)
TIP: Use -S with keywords (odd, even, first:N, last:N) for smart selection
TIP: Use --sort newest to get latest research first
TIP: Use --show-pdf-links to see clickable PDF links (works in modern terminals!)
TIP: Results are cached - review later with: lixplore -R 1 2 3
TIP: Combine features: --sort newest -S first:10 -X xlsx
TIP: Use --help for complete documentation
TIP: Use 'man lixplore' for detailed manual page

For more information: lixplore --help
"""
    else:
        return """
=======================================================================
                         LIXPLORE - Quick Examples                      
=======================================================================

BASIC SEARCH
  Search PubMed for a query:
    $ lixplore -P -q "cancer treatment" -m 10

  Search with abstracts:
    $ lixplore -P -q "diabetes" -m 5 -a

MULTI-SOURCE SEARCH
  Search PubMed + arXiv:
    $ lixplore -s PX -q "machine learning" -m 20

  Search all sources with deduplication:
    $ lixplore -A -q "COVID-19" -m 50 -D

EXPORT RESULTS
  Export to Excel:
    $ lixplore -P -q "neuroscience" -m 15 -X xlsx -o brain_research.xlsx

  Export to EndNote Tagged:
    $ lixplore -P -q "quantum physics" -m 20 -X enw -o physics.enw

  Export to CSV:
    $ lixplore -P -q "climate change" -m 30 -X csv

  Export to BibTeX:
    $ lixplore -P -q "artificial intelligence" -m 25 -X bibtex

ADVANCED SEARCH
  Search with date filter:
    $ lixplore -P -q "vaccine development" -d 2020-01-01 2024-12-31 -m 15

  Search by author:
    $ lixplore -P -au "Smith J" -m 10 -a

  Search by DOI:
    $ lixplore -DOI "10.1038/nature12345"

BOOLEAN OPERATORS (Advanced Query Syntax)
  AND operator (both terms required):
    $ lixplore -P -q "cancer AND treatment" -m 10

  OR operator (either term):
    $ lixplore -P -q "cancer OR tumor" -m 10

  NOT operator (exclude term):
    $ lixplore -P -q "diabetes NOT type1" -m 10

  Complex queries with parentheses:
    $ lixplore -P -q "(cancer OR tumor) AND (treatment OR therapy)" -m 20

  Combine with other features:
    $ lixplore -A -q "COVID-19 AND vaccine" -m 50 -D --sort newest -X xlsx

COMBINED FEATURES
  Multi-source search with export and deduplication:
    $ lixplore -s PCE -q "gene therapy" -m 30 -D -X xlsx -o genes.xlsx

  Search with date filter, abstracts, and export:
    $ lixplore -P -q "cancer immunotherapy" -d 2023-01-01 2024-12-31 -a -m 20 -X json

REVIEW ARTICLES (Two-Step Workflow)
  Step 1 - Search and cache results:
    $ lixplore -P -q "diabetes" -m 10

  Step 2 - Review specific articles:
    $ lixplore -R 2           # Review article #2
    $ lixplore -R 1 5 9       # Review multiple articles

  One-step (search + review):
    $ lixplore -P -q "aspirin" -m 10 -R 1 3 5

  In review window:
    Press 'q' or Ctrl+C to close (won't close with other keys)

SMART SELECTION (Export Specific Articles)
  Export odd-numbered articles:
    $ lixplore -P -q "research" -m 50 -S odd -X csv

  Export even-numbered articles:
    $ lixplore -P -q "study" -m 50 -S even -X xlsx

  Export first 10 articles:
    $ lixplore -P -q "cancer" -m 50 -S first:10 -X enw

  Export last 5 articles:
    $ lixplore -P -q "science" -m 30 -S last:5 -X csv

  Export specific range:
    $ lixplore -P -q "biology" -m 50 -S 10-20 -X xlsx

  Mixed selection (combine patterns):
    $ lixplore -P -q "chemistry" -m 50 -S 1 3 5-10 odd -X csv

SORT RESULTS
  Sort by newest (latest first):
    $ lixplore -P -q "COVID-19" -m 50 --sort newest

  Sort by oldest (historical research):
    $ lixplore -P -q "diabetes" -m 50 --sort oldest

  Sort by journal (alphabetical):
    $ lixplore -A -q "AI" -m 50 -D --sort journal

  Sort by author (alphabetical):
    $ lixplore -P -q "physics" -m 50 --sort author

  Combine sort + selection + export:
    $ lixplore -P -q "cancer" -m 50 --sort newest -S first:10 -X xlsx

SOURCE CODES (for -s flag)
  P = PubMed       C = Crossref      J = DOAJ
  E = EuropePMC    X = arXiv         A = All sources

EXPORT FORMATS
  csv      - CSV (Excel, Google Sheets)
  xlsx     - Excel with formatting
  json     - JSON structured data
  bibtex   - BibTeX for LaTeX
  ris      - RIS (Zotero, Mendeley)
  enw      - EndNote Tagged (recommended)
  endnote  - EndNote XML
  xml      - Generic XML

Export locations: All files saved to exports/ folder
 (organized by format: exports/csv/, exports/excel/, etc.)

TIP: Use -D flag when searching multiple sources to remove duplicates
TIP: Use -a flag to see abstracts in results
TIP: Use -R for detailed review in separate windows (press 'q' to close)
TIP: Use -S with keywords (odd, even, first:N, last:N) for smart selection
TIP: Use --sort newest to get latest research first
TIP: Results are cached - review later with: lixplore -R 1 2 3
TIP: Combine features: --sort newest -S first:10 -X xlsx
TIP: Use --help for complete documentation
TIP: Use 'man lixplore' for detailed manual page

For more information: lixplore --help
"""


def show_examples():
    """Display tldr-style quick examples."""
    unicode_ok = _supports_unicode_output()
    print(_examples_text(unicode_ok))


def run_main(args):
    """Main handler for CLI options."""

    # Handle interactive modes first (only if used standalone, without search)
    # If -i is used WITH search flags, it will be handled later after the search
    has_search_params = (args.query or args.author or args.doi or
                         any([args.pubmed, args.crossref, args.doaj,
                              args.europepmc, args.arxiv, getattr(args, 'all', False),
                              args.sources]))

    if args.interactive and not has_search_params:
        # Launch simple interactive TUI standalone
        from lixplore.utils.interactive_tui import launch_interactive_mode
        launch_interactive_mode([])
        return

    if args.tui:
        from lixplore.utils.enhanced_tui import launch_enhanced_tui
        launch_enhanced_tui()
        return

    # Deprecated modes (kept for backwards compatibility)
    if args.shell:
        print("Note: --shell is deprecated.")
        from lixplore.utils.shell_mode import launch_shell
        launch_shell()
        return

    if args.wizard:
        print("Note: --wizard is deprecated.")
        from lixplore.utils.wizard_mode import launch_wizard
        launch_wizard()
        return

    # If user only wants examples
    if args.examples:
        show_examples()
        return

    # If user only wants history
    # Handle annotation commands
    from lixplore.utils.annotations import AnnotationManager, display_annotation

    # Annotation-only commands (don't require search)
    if args.list_annotations:
        manager = AnnotationManager()
        filter_params = None

        if hasattr(args, 'filter_annotations') and args.filter_annotations:
            # Parse filter string: "min_rating=4,priority=high"
            filter_params = {}
            for item in args.filter_annotations.split(','):
                if '=' in item:
                    key, value = item.split('=', 1)
                    key = key.strip()
                    value = value.strip()

                    if key == 'min_rating':
                        filter_params['min_rating'] = int(value)
                    elif key == 'max_rating':
                        filter_params['max_rating'] = int(value)
                    elif key == 'read_status':
                        filter_params['read_status'] = value
                    elif key == 'priority':
                        filter_params['priority'] = value
                    elif key == 'tag':
                        filter_params['tags'] = [value]

        annotations = manager.list_all(filter_params)

        if not annotations:
            print("No annotated articles found.")
            if filter_params:
                print("Try removing filters or annotate some articles first.")
        else:
            print(f"\n{'='*80}")
            print(f"ANNOTATED ARTICLES ({len(annotations)})")
            print(f"{'='*80}\n")

            for i, item in enumerate(annotations, 1):
                annotation = item['annotation']
                info = annotation.get('article_info', {})

                print(f"[{i}] {info.get('title', 'No title')}")

                # Show rating
                if annotation.get('rating'):
                    stars = '' * annotation['rating']
                    print(f"    Rating: {stars} ({annotation['rating']}/5)")

                # Show tags
                if annotation.get('tags'):
                    print(f"    Tags: {', '.join(annotation['tags'])}")

                # Show status and priority
                print(f"    Status: {annotation.get('read_status', 'unread').title()} | Priority: {annotation.get('priority', 'medium').title()}")

                # Show comment count
                comments_count = len(annotation.get('comments', []))
                if comments_count > 0:
                    print(f"    Comments: {comments_count}")

                print()

            print(f"{'='*80}\n")
        return

    if args.search_annotations:
        manager = AnnotationManager()
        results = manager.search_annotations(args.search_annotations)

        if not results:
            print(f"No annotations found matching: '{args.search_annotations}'")
        else:
            print(f"\n{'='*80}")
            print(f"SEARCH RESULTS ({len(results)} matches)")
            print(f"{'='*80}\n")

            for i, item in enumerate(results, 1):
                annotation = item['annotation']
                info = annotation.get('article_info', {})

                print(f"[{i}] {info.get('title', 'No title')}")
                print(f"    Match type: {item['match_type']}")
                print(f"    Match: {item['match_text'][:100]}...")
                print()

            print(f"{'='*80}\n")
        return

    if args.export_annotations:
        manager = AnnotationManager()
        output_file = manager.export_annotations(format=args.export_annotations)
        print(f"Annotations exported to: {output_file}")
        return

    if args.annotation_stats:
        manager = AnnotationManager()
        stats = manager.get_statistics()

        print(f"\n{'='*80}")
        print("ANNOTATION STATISTICS")
        print(f"{'='*80}\n")

        print(f"Total Annotated Articles: {stats['total']}")

        if stats['total'] == 0:
            print("\nNo annotations yet. Start annotating articles with:")
            print("  lixplore -P -q 'query' -m 10")
            print("  lixplore --annotate 1 --rating 5 --tags 'important'")
            print(f"{'='*80}\n")
            return

        # Rating distribution
        if stats['by_rating']:
            print(f"\nRating Distribution:")
            for rating in sorted(stats['by_rating'].keys(), reverse=True):
                count = stats['by_rating'][rating]
                stars = '' * rating
                bar = '█' * count
                print(f"  {stars} ({rating}): {bar} {count}")

        # Read status
        if stats['by_status']:
            print(f"\nRead Status:")
            for status, count in stats['by_status'].items():
                print(f"  {status.title()}: {count}")

        # Priority
        if stats['by_priority']:
            print(f"\nPriority:")
            for priority, count in stats['by_priority'].items():
                print(f"  {priority.title()}: {count}")

        # Comments
        print(f"\nComments:")
        print(f"  Articles with comments: {stats['with_comments']}")
        print(f"  Total comments: {stats['total_comments']}")

        # Tags
        print(f"\nTags:")
        print(f"  Unique tags: {stats['total_tags']}")
        if stats['unique_tags']:
            print(f"  Tags: {', '.join(stats['unique_tags'][:20])}")
            if len(stats['unique_tags']) > 20:
                print(f"        ... and {len(stats['unique_tags']) - 20} more")

        print(f"\n{'='*80}\n")
        return

    # Handle template and profile management commands
    from lixplore.utils import profiles
    from lixplore.utils import template_engine
    from lixplore.utils import custom_apis

    # Handle PDF downloader configuration commands
    from lixplore.utils import pdf_downloader

    if args.set_scihub_mirror:
        pdf_downloader.set_scihub_mirror(args.set_scihub_mirror)
        return

    if args.show_pdf_dir:
        print(f"PDF download directory: {pdf_downloader.PDF_DIR}")
        if os.path.exists(pdf_downloader.PDF_DIR):
            # Count PDFs
            pdf_count = sum(1 for root, dirs, files in os.walk(pdf_downloader.PDF_DIR)
                          for f in files if f.endswith('.pdf'))
            print(f"Total PDFs downloaded: {pdf_count}")
        else:
            print("(Directory does not exist yet - will be created on first download)")
        return

    # Handle reference manager configuration commands
    from lixplore.utils import reference_managers

    if args.configure_zotero:
        api_key, user_id = args.configure_zotero
        reference_managers.configure_zotero(api_key, user_id)
        return

    if args.show_zotero_collections:
        reference_managers.show_zotero_collections()
        return

    # Handle custom API management commands
    if args.list_custom_apis:
        api_list = custom_apis.list_custom_apis()
        if api_list:
            print("Configured custom API sources:")
            for api in api_list:
                config = custom_apis.load_custom_api_config(api)
                if config:
                    print(f"  • {api}")
                    if 'description' in config:
                        print(f"      {config['description']}")
                    if 'requires_auth' in config and config['requires_auth']:
                        print(f"      Requires authentication")
        else:
            print("No custom APIs configured.")
            print("Run: lixplore --create-api-examples to create example configurations")
        return

    if args.create_api_examples:
        custom_apis.create_example_configs()
        return

    if args.list_templates:
        template_names = template_engine.list_templates()
        if template_names:
            print("Available export templates:")
            for name in template_names:
                template = template_engine.load_template(name.replace(' (user)', ''))
                if template:
                    print(f"  • {name}")
                    if 'description' in template:
                        print(f"      {template['description']}")
                    if 'format' in template:
                        print(f"      Format: {template['format']}")
        else:
            print("No templates found.")
        return

    if args.list_profiles:
        profile_names = profiles.list_profiles()
        if profile_names:
            print("Saved export profiles:")
            for name in profile_names:
                profile = profiles.load_profile(name)
                print(f"  • {name}")
                if 'export_format' in profile:
                    print(f"      Format: {profile['export_format']}")
                if 'citation_style' in profile:
                    print(f"      Citation: {profile['citation_style']}")
        else:
            print("No saved profiles found.")
            print("Save a profile with: --save-profile <name>")
        return

    if args.delete_profile:
        if profiles.delete_profile(args.delete_profile):
            print(f"Profile '{args.delete_profile}' deleted successfully")
        return

    # Load template if specified
    if args.template:
        template = template_engine.load_template(args.template)
        if template:
            print(f"Loading template: {args.template}")
            args = template_engine.apply_template_to_args(args, template)
        else:
            print(f"Error: Template '{args.template}' not found")
            print("Use --list-templates to see available templates")
            return

    # Load profile if specified (profiles override templates)
    if args.load_profile:
        profile = profiles.load_profile(args.load_profile)
        if profile:
            print(f"Loading profile: {args.load_profile}")
            args = profiles.apply_profile_to_args(args, profile)
        else:
            print(f"Error: Profile '{args.load_profile}' not found")
            print("Use --list-profiles to see available profiles")
            return

    if args.history:
        dispatcher.show_history()
        return

    # If user only wants to review cached results (no new search)
    if args.review and not any([args.pubmed, args.crossref, args.doaj, args.europepmc, args.arxiv, args.all, args.sources, args.query]):
        # Load cached results and review (ignore --refresh flag for standalone review)
        cached_results = dispatcher.load_cached_results(check_expiry=True, force_refresh=False)
        if cached_results:
            print(f"Loading cached results ({len(cached_results)} articles)...")
            print("\nCached results:")
            for i, result in enumerate(cached_results, 1):
                print(f"[{i}] {result.get('title', 'No title')}")
            print("")
            dispatcher.review_articles(cached_results, args.review)
        else:
            print("No cached results found. Please run a search first.")
            print("Example: lixplore -P -q \"paracetamol\" -m 5")
        return

    # Determine which sources to search
    sources_to_search = []
    use_custom_api = False
    custom_api_name = None

    # Check for custom API first (takes precedence)
    if hasattr(args, 'custom_api') and args.custom_api:
        use_custom_api = True
        custom_api_name = args.custom_api
        # Custom API is handled separately, not added to sources_to_search

    # Source letter mapping
    source_map = {
        'P': 'pubmed',
        'C': 'crossref',
        'J': 'doaj',
        'E': 'europepmc',
        'X': 'arxiv',
        'A': 'all'
    }

    # Check for combined sources flag (-s/--sources)
    if hasattr(args, 'sources') and args.sources:
        sources_str = args.sources.upper()

        # If 'A' is in the string, search all sources
        if 'A' in sources_str:
            sources_to_search = ["pubmed", "crossref", "doaj", "europepmc", "arxiv"]
        else:
            # Parse each character
            for char in sources_str:
                if char in source_map and source_map[char] != 'all':
                    source = source_map[char]
                    if source not in sources_to_search:
                        sources_to_search.append(source)
                elif char not in [' ', ',']:  # Ignore spaces and commas
                    print(f"Warning: Unknown source code '{char}' - ignoring")

    # Check for -A/--all flag
    elif args.all:
        sources_to_search = ["pubmed", "crossref", "doaj", "europepmc", "arxiv"]

    # Fall back to individual source flags
    else:
        if args.pubmed:
            sources_to_search.append("pubmed")
        if args.crossref:
            sources_to_search.append("crossref")
        if args.doaj:
            sources_to_search.append("doaj")
        if args.europepmc:
            sources_to_search.append("europepmc")
        if args.arxiv:
            sources_to_search.append("arxiv")

    # Check if at least one source is selected (either standard or custom)
    if not sources_to_search and not use_custom_api:
        print("Error: Please specify at least one source to search:")
        print("  -s PX           Combined sources (P=PubMed, C=Crossref, J=DOAJ, E=EuropePMC, X=arXiv, A=All)")
        print("  -P or --pubmed      Search PubMed")
        print("  -C or --crossref    Search Crossref")
        print("  -J or --doaj        Search DOAJ")
        print("  -E or --europepmc   Search EuropePMC")
        print("  -x or --arxiv       Search arXiv")
        print("  -A or --all         Search all sources")
        print("  --custom-api NAME   Search custom API (Springer, BASE, etc.)")
        print("\nFor interactive mode, use: lixplore -i")
        print("\nExamples:")
        print("  lixplore -P -q 'search term' -m 20       # PubMed search")
        print("  lixplore -s PX -q 'search term'          # PubMed + arXiv")
        print("  lixplore -s PCE -q 'search term'         # PubMed + Crossref + EuropePMC")
        print("  lixplore -i                              # Interactive TUI mode")
        print("  lixplore --custom-api springer -q 'term' # Custom API (requires configuration)")
        return

    results = []
    query = None

    #  Build query based on search type
    if args.query:
        query = args.query
        print(f"Searching for query: {query}")
    elif args.author:
        # Note: Author search syntax is PubMed-specific
        query = f"{args.author}[Author]" if "pubmed" in sources_to_search else args.author
        print(f"Searching articles by author: {args.author}")
    elif args.doi:
        query = args.doi
        print(f"Fetching article with DOI: {args.doi}")
    else:
        print("Error: Please provide a query, author, or DOI to search:")
        print("  -q, --query QUERY      Search query")
        print("  -au, --author AUTHOR   Search by author")
        print("  -DOI DOI               Fetch article by DOI")
        print("\nFor interactive mode, use: lixplore -i")
        print("\nExample: lixplore -P -q \"cancer treatment\" -m 20")
        return

    #  Display selected sources
    source_names = {
        "pubmed": "PubMed",
        "crossref": "Crossref",
        "doaj": "DOAJ",
        "europepmc": "EuropePMC",
        "arxiv": "arXiv"
    }

    # Show standard sources if any
    if sources_to_search:
        selected_names = [source_names[src] for src in sources_to_search]
        print(f"Sources: {', '.join(selected_names)}")

    # Show custom API if selected
    if use_custom_api:
        print(f"Custom API: {custom_api_name}")

    #  Execute search on selected sources
    for src in sources_to_search:
        print(f"  Searching {source_names[src]}...")
        src_results = dispatcher.search(
            source=src,
            query=query,
            limit=args.max_results,
        )
        results.extend(src_results)

    #  Execute search on custom API if selected
    if use_custom_api:
        print(f"  Searching {custom_api_name} (custom API)...")
        custom_results = custom_apis.call_custom_api(custom_api_name, query, args.max_results)
        results.extend(custom_results)

    if (len(sources_to_search) > 1) or (len(sources_to_search) > 0 and use_custom_api):
        print(f"Total results before deduplication: {len(results)}")

    #  Post-processing
    if args.deduplicate and results:
        print("Removing duplicates")
        results = dispatcher.deduplicate_advanced(
            results,
            strategy=args.deduplicate,
            title_threshold=args.dedup_threshold,
            keep_preference=args.dedup_keep,
            merge_metadata=args.dedup_merge
        )

    #  Enrich metadata if requested
    if args.enrich is not None and results:
        from lixplore.utils.enrichment import enrich_results
        # If --enrich used without arguments, use all APIs
        apis = args.enrich if args.enrich else ['all']
        results = enrich_results(results, apis, show_progress=True)

    #  Sort results if requested
    if results and args.sort and args.sort != "relevant":
        results = sort_results(results, args.sort)
        print(f"Results sorted by: {args.sort}")

    #  Export to file format if requested
    if args.export and results:
        # Check if multiple formats specified (comma-separated)
        formats = [f.strip() for f in args.export.split(',')]

        # Validate formats
        valid_formats = ["csv", "json", "bibtex", "ris", "endnote", "enw", "xlsx", "xml"]
        invalid_formats = [f for f in formats if f not in valid_formats]
        if invalid_formats:
            print(f"Error: Invalid export format(s): {', '.join(invalid_formats)}")
            print(f"Valid formats: {', '.join(valid_formats)}")
            return

        # Filter results if specific articles selected
        if args.select:
            # Parse selection arguments (supports: numbers, ranges, keywords)
            selected_numbers = parse_selection(args.select, len(results))

            if selected_numbers:
                selected_results = [results[num - 1] for num in selected_numbers]
                print(f"Selected articles: {', '.join(f'#{n}' for n in selected_numbers)}")
                print(f"Exporting {len(selected_results)} selected article(s)...")

                # Use batch export if multiple formats, otherwise single export
                if len(formats) > 1:
                    # Extract base filename from output (remove extension)
                    output_base = args.output.rsplit('.', 1)[0] if args.output else None
                    dispatcher.batch_export(selected_results, formats, output_base, args.export_fields, args.zip)
                else:
                    dispatcher.export_to_format(selected_results, formats[0], args.output, args.export_fields, args.zip)
            else:
                print("No valid articles selected for export.")
        else:
            # Export all results
            if len(formats) > 1:
                # Batch export: Extract base filename from output (remove extension)
                output_base = args.output.rsplit('.', 1)[0] if args.output else None
                dispatcher.batch_export(results, formats, output_base, args.export_fields, args.zip)
            else:
                # Single format export
                dispatcher.export_to_format(results, formats[0], args.output, args.export_fields, args.zip)

    #  Export as formatted citations if requested
    if args.citations and results:
        from lixplore.utils.export import export_to_citations, compress_export
        print(f"Generating {args.citations.upper()} style citations...")
        exported_path = export_to_citations(results, args.citations, args.output, args.export_fields)
        if args.zip and exported_path:
            compress_export(exported_path, remove_original=False)

    #  Save profile if requested (after export completes)
    if args.save_profile:
        config = profiles.create_profile_from_args(args)
        if config:  # Only save if there are settings to save
            if profiles.save_profile(args.save_profile, config):
                print(f"Profile '{args.save_profile}' saved successfully")
                print(f"  Settings saved: {', '.join(config.keys())}")
            else:
                print(f"Error: Could not save profile '{args.save_profile}'")
        else:
            print("Warning: No export settings to save in profile")

    #  Show results (titles + optional inline abstracts)
    # Display results BEFORE review so users don't see them again after closing review windows
    if results:
        print(f"\nFound {len(results)} results:")
        dispatcher.show_results(results, args)

        # Save results to cache for later review
        all_sources = sources_to_search.copy()
        if use_custom_api:
            all_sources.append(f"custom:{custom_api_name}")
        dispatcher.save_results(results, query=query, sources=all_sources)

        # Save to search history
        dispatcher.save_to_history(query=query, sources=all_sources, result_count=len(results))

        # If user requested detailed view(s) via -N, print them inline
        if args.number:
            for n in args.number:
                if not isinstance(n, int):
                    print(f"Invalid selection (not an integer): {n}")
                    continue
                if 1 <= n <= len(results):
                    idx = n - 1
                    print("\n=== Detailed View ===")
                    # print dict as readable JSON
                    print(json.dumps(results[idx], indent=2, ensure_ascii=False))
                else:
                    print(f"Selection out of range: {n} (valid 1..{len(results)})")

        #  Download PDFs if requested
        if args.download_pdf:
            pdf_numbers = args.pdf_numbers if args.pdf_numbers else None
            pdf_downloader.download_multiple_pdfs(
                results,
                article_numbers=pdf_numbers,
                use_scihub=args.use_scihub
            )

        #  Add to Zotero if requested
        if args.add_to_zotero:
            collection_key = args.zotero_collection if hasattr(args, 'zotero_collection') and args.zotero_collection else None
            reference_managers.add_to_zotero(results, collection_key=collection_key)

        #  Export for Mendeley if requested
        if args.export_for_mendeley:
            reference_managers.export_for_mendeley(results)

        #  Show statistics dashboard if requested
        if args.stat:
            from lixplore.utils.statistics import generate_statistics_report
            stats_report = generate_statistics_report(results, top_n=args.stat_top)
            print(stats_report)

        #  Launch interactive mode if requested
        if args.interactive:
            from lixplore.utils.interactive_tui import launch_interactive_mode
            launch_interactive_mode(results)
            return  # Interactive mode handles everything

        #  Review articles in separate terminal if requested
        # This comes AFTER showing results so user sees the list, then reviews, then returns without duplication
        if args.review:
            dispatcher.review_articles(results, args.review)

        #  Handle annotations for articles from search results
        if args.annotate or args.show_annotation or args.delete_annotation:
            manager = AnnotationManager()

            # Annotate article
            if args.annotate:
                article_num = args.annotate
                if 1 <= article_num <= len(results):
                    article = results[article_num - 1]

                    # Collect annotation data
                    tags_list = None
                    if args.tags:
                        tags_list = [t.strip() for t in args.tags.split(',')]

                    # Add annotation
                    article_id = manager.annotate(
                        article=article,
                        comment=args.comment if hasattr(args, 'comment') and args.comment else None,
                        rating=args.rating if hasattr(args, 'rating') and args.rating else None,
                        tags=tags_list,
                        read_status=args.read_status if hasattr(args, 'read_status') and args.read_status else None,
                        priority=args.priority if hasattr(args, 'priority') and args.priority else None
                    )

                    print(f"\nAnnotation saved for article #{article_num}: {article.get('title', 'No title')[:60]}...")

                    # Show the annotation
                    annotation = manager.get_annotation(article_id)
                    if annotation:
                        display_annotation(annotation, article_id)
                else:
                    print(f"Error: Article #{article_num} is out of range (1-{len(results)})")

            # Show annotation
            if args.show_annotation:
                article_num = args.show_annotation
                if 1 <= article_num <= len(results):
                    article = results[article_num - 1]
                    annotation = manager.get_annotation_for_article(article)

                    if annotation:
                        article_id = manager._get_article_id(article)
                        display_annotation(annotation, article_id)
                    else:
                        print(f"\nNo annotation found for article #{article_num}")
                        print(f"Add annotation with: lixplore --annotate {article_num} --rating 5 --tags 'important'")
                else:
                    print(f"Error: Article #{article_num} is out of range (1-{len(results)})")

            # Delete annotation
            if args.delete_annotation:
                article_num = args.delete_annotation
                if 1 <= article_num <= len(results):
                    article = results[article_num - 1]
                    article_id = manager._get_article_id(article)

                    if manager.remove_annotation(article_id):
                        print(f"Annotation deleted for article #{article_num}")
                    else:
                        print(f"No annotation found for article #{article_num}")
                else:
                    print(f"Error: Article #{article_num} is out of range (1-{len(results)})")

    else:
        print("No results found.")

