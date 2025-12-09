#!/usr/bin/env python3

import argparse
import json
from os import stat
from . import dispatcher


def add_commands(parser: argparse.ArgumentParser):
    """Register CLI arguments for lixplore."""

    # Source selection options
    parser.add_argument(
        "-P", "--pubmed", action="store_true",
        help="Search PubMed"
    )
    parser.add_argument(
        "-C", "--crossref", action="store_true",
        help="Search Crossref"
    )
    parser.add_argument(
        "-J", "--doaj", action="store_true",
        help="Search DOAJ (Directory of Open Access Journals)"
    )
    parser.add_argument(
        "-E", "--europepmc", action="store_true",
        help="Search EuropePMC"
    )
    parser.add_argument(
        "-X", "--arxiv", action="store_true",
        help="Search arXiv"
    )
    parser.add_argument(
        "-A", "--all", action="store_true",
        help="Search across all sources (PubMed, Crossref, DOAJ, EuropePMC, arXiv)"
    )
    parser.add_argument(
        "-s", "--sources", type=str,
        help="Combined source selection (e.g., 'PX' for PubMed+arXiv, 'PCE' for PubMed+Crossref+EuropePMC, 'A' for all)"
    )
    parser.add_argument(
        "-q", "--query", type=str,
        help="Query string to search"
    )
    parser.add_argument(
        "-d", "--date", nargs=2, metavar=("FROM", "TO"),
        help="Filter with date range (YYYY-MM-DD YYYY-MM-DD)"
    )
    parser.add_argument(
        "-a", "--abstract", action="store_true",
        help="Show abstracts of results"
    )
    parser.add_argument(
        "-N", "--number", type=int, nargs="+", default=[],
        help="Select an article number for deeper view (1-based index)"
    )
    parser.add_argument(
        "-Z", "--zotero", action="store_true",
        help="Export results to Zotero"
    )
    parser.add_argument(
        "-H", "--history", action="store_true",
        help="Show search history"
    )
    parser.add_argument(
        "-D", "--deduplicate", action="store_true",
        help="Remove duplicate results"
    )

    # Extended options
    parser.add_argument(
        "-au", "--author", type=str,
        help="Search articles by author name"
    )
    parser.add_argument(
        "-DOI", "--doi", type=str,
        help="Search article by DOI"
    )

    parser.add_argument(
        "-m", "--max_results", type=int, default=10,
        help="Maximum fetch the number by choice by user (default=10)"
    )

    parser.add_argument(
        "-st", "--stat",
        type=int,
        default=50,
        help="Getting statistics for count of selected parameter"
    )

    parser.set_defaults(func=run_main)


def run_main(args):
    """Main handler for CLI options."""

    # If user only wants history
    if args.history:
        dispatcher.show_history()
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

    if args.zotero and results:
        print("Exporting results to Zotero")
        dispatcher.export_zotero(results)

    # 🔹 Show results (titles + optional inline abstracts)
    if results:
        print(f"\nFound {len(results)} results:")
        dispatcher.show_results(results, args)

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

