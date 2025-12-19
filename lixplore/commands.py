#!/usr/bin/env python3

import argparse
import json
from os import stat
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
        "-D", "--deduplicate", action="store_true",
        help="Remove duplicate results when searching multiple sources (recommended with -A or -s)"
    )
    filter_group.add_argument(
        "--sort", type=str, choices=["relevant", "newest", "oldest", "journal", "author"],
        default="relevant", metavar="ORDER",
        help="Sort results by: relevant (default/original order), newest (latest first), oldest (earliest first), journal (alphabetical), author (by first author). Example: --sort newest"
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
        "-N", "--number", type=int, nargs="+", default=[], metavar="N",
        help="View detailed information for specific article(s) by number. Example: -N 1 or -N 1 2 3"
    )
    display_group.add_argument(
        "-R", "--review", type=int, nargs="+", default=[], metavar="N",
        help="Open article(s) in separate terminal window for detailed review. Two modes: 1) With search: -P -q 'query' -R 1 2, or 2) Standalone: lixplore -R 1 2 (uses cached results). Close window with 'q' or Ctrl+C. Example: -R 1 or -R 1 2 3"
    )
    display_group.add_argument(
        "-st", "--stat", type=int, default=50, metavar="N",
        help="Get statistics for the specified count (default: 50)"
    )
    
    # ===== EXPORT & OUTPUT =====
    export_group = parser.add_argument_group(
        '[EXPORT & OUTPUT]',
        'Export results in various formats'
    )
    
    export_group.add_argument(
        "-X", "--export", type=str, 
        choices=["csv", "json", "bibtex", "ris", "endnote", "enw", "xlsx", "xml"],
        metavar="FORMAT",
        help="Export results to specified format: csv, json, bibtex, ris, endnote (XML), enw (EndNote Tagged), xlsx (Excel), xml. Files saved to exports/ folder"
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
        "-Z", "--zotero", action="store_true",
        help="Export results to Zotero reference manager"
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
        "--examples", action="store_true",
        help="Show quick examples (tldr-style) and exit"
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
    test_string = "📚═"
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

📚 BASIC SEARCH
  Search PubMed for a query:
    $ lixplore -P -q "cancer treatment" -m 10

  Search with abstracts:
    $ lixplore -P -q "diabetes" -m 5 -a

📦 MULTI-SOURCE SEARCH
  Search PubMed + arXiv:
    $ lixplore -s PX -q "machine learning" -m 20

  Search all sources with deduplication:
    $ lixplore -A -q "COVID-19" -m 50 -D

💾 EXPORT RESULTS
  Export to Excel:
    $ lixplore -P -q "neuroscience" -m 15 -X xlsx -o brain_research.xlsx

  Export to EndNote Tagged:
    $ lixplore -P -q "quantum physics" -m 20 -X enw -o physics.enw

  Export to CSV:
    $ lixplore -P -q "climate change" -m 30 -X csv

  Export to BibTeX:
    $ lixplore -P -q "artificial intelligence" -m 25 -X bibtex

🎯 ADVANCED SEARCH
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

📊 SORT RESULTS
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

📊 SOURCE CODES (for -s flag)
  P = PubMed       C = Crossref      J = DOAJ
  E = EuropePMC    X = arXiv         A = All sources

💾 EXPORT FORMATS
  csv      - CSV (Excel, Google Sheets)
  xlsx     - Excel with formatting
  json     - JSON structured data
  bibtex   - BibTeX for LaTeX
  ris      - RIS (Zotero, Mendeley)
  enw      - EndNote Tagged (recommended)
  endnote  - EndNote XML
  xml      - Generic XML

📁 Export locations: All files saved to exports/ folder
   (organized by format: exports/csv/, exports/excel/, etc.)

💡 TIP: Use -D flag when searching multiple sources to remove duplicates
💡 TIP: Use -a flag to see abstracts in results
💡 TIP: Use -R for detailed review in separate windows (press 'q' to close)
💡 TIP: Use -S with keywords (odd, even, first:N, last:N) for smart selection
💡 TIP: Use --sort newest to get latest research first
💡 TIP: Results are cached - review later with: lixplore -R 1 2 3
💡 TIP: Combine features: --sort newest -S first:10 -X xlsx
💡 TIP: Use --help for complete documentation
💡 TIP: Use 'man lixplore' for detailed manual page

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

    # If user only wants examples
    if args.examples:
        show_examples()
        return

    # If user only wants history
    if args.history:
        dispatcher.show_history()
        return
    
    # If user only wants to review cached results (no new search)
    if args.review and not any([args.pubmed, args.crossref, args.doaj, args.europepmc, args.arxiv, args.all, args.sources, args.query]):
        # Load cached results and review
        cached_results = dispatcher.load_cached_results()
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

    # Check if at least one source is selected
    if not sources_to_search:
        print("Error: Please specify at least one source to search:")
        print("  -s PX           Combined sources (P=PubMed, C=Crossref, J=DOAJ, E=EuropePMC, X=arXiv, A=All)")
        print("  -P or --pubmed      Search PubMed")
        print("  -C or --crossref    Search Crossref")
        print("  -J or --doaj        Search DOAJ")
        print("  -E or --europepmc   Search EuropePMC")
        print("  -X or --arxiv       Search arXiv")
        print("  -A or --all         Search all sources")
        print("\nExamples:")
        print("  lixplore -s PX -q 'search term'      # PubMed + arXiv")
        print("  lixplore -s PCE -q 'search term'     # PubMed + Crossref + EuropePMC")
        print("  lixplore -P -C -E -q 'search term'   # Same as above (old syntax)")
        return

    results = []
    query = None

    # 🔹 Build query based on search type
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
        print("Error: Please provide a search query (-q), author (-au), or DOI (-DOI)")
        return

    # 🔹 Display selected sources
    source_names = {
        "pubmed": "PubMed",
        "crossref": "Crossref",
        "doaj": "DOAJ",
        "europepmc": "EuropePMC",
        "arxiv": "arXiv"
    }
    selected_names = [source_names[src] for src in sources_to_search]
    print(f"Sources: {', '.join(selected_names)}")

    # 🔹 Execute search on selected sources
    for src in sources_to_search:
        print(f"  Searching {source_names[src]}...")
        src_results = dispatcher.search(
            source=src,
            query=query,
            limit=args.max_results,
        )
        results.extend(src_results)

    if len(sources_to_search) > 1:
        print(f"Total results before deduplication: {len(results)}")

    # 🔹 Post-processing
    if args.deduplicate and results:
        print("Removing duplicates")
        results = dispatcher.deduplicate(results)
    
    # 🔹 Sort results if requested
    if results and args.sort and args.sort != "relevant":
        results = sort_results(results, args.sort)
        print(f"Results sorted by: {args.sort}")

    if args.zotero and results:
        print("Exporting results to Zotero")
        dispatcher.export_zotero(results)
    
    # 🔹 Export to file format if requested
    if args.export and results:
        # Filter results if specific articles selected
        if args.select:
            # Parse selection arguments (supports: numbers, ranges, keywords)
            selected_numbers = parse_selection(args.select, len(results))
            
            if selected_numbers:
                selected_results = [results[num - 1] for num in selected_numbers]
                print(f"Selected articles: {', '.join(f'#{n}' for n in selected_numbers)}")
                print(f"Exporting {len(selected_results)} selected article(s)...")
                dispatcher.export_to_format(selected_results, args.export, args.output)
            else:
                print("No valid articles selected for export.")
        else:
            # Export all results
            dispatcher.export_to_format(results, args.export, args.output)
    
    # 🔹 Review articles in separate terminal if requested
    if args.review and results:
        dispatcher.review_articles(results, args.review)

    # 🔹 Show results (titles + optional inline abstracts)
    if results:
        print(f"\nFound {len(results)} results:")
        dispatcher.show_results(results, args)
        
        # Save results to cache for later review
        dispatcher.save_results(results)

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
    else:
        print("No results found.")

