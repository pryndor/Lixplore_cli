#!/usr/bin/env python3

from lixplore.sources import pubmed, crossref, doaj, europepmc, arxiv
from lixplore.utils.terminal import open_in_new_terminal, open_article_in_terminal
from lixplore.utils.export import export_results
import json
import os
from difflib import SequenceMatcher

CACHE_FILE = os.path.expanduser("~/.lixplore_cache.json")


# ===== Extra helpers =====
def show_abstract(result):
    """Open abstract in a new terminal window."""
    abstract = result.get("abstract", "No abstract available.")
    open_in_new_terminal(abstract)


def show_authors(result):
    """Open author list in a new terminal window."""
    authors = ", ".join(result.get("authors", []))
    open_in_new_terminal(authors or "No authors available.")


# ===== Main handler =====
def handle(args):
    results = []

    if args.pubmed:
        results = search("pubmed", args.query, 10)
    elif args.all:
        for src in ["pubmed", "crossref", "doaj", "europepmc", "arxiv"]:
            results += search(src, args.query, 10)
    else:
        print("Please choose -P (PubMed) or -A (All sources).")
        return

    if args.date:
        results = filter_by_date(results, args.date)

    if args.deduplicate:
        results = deduplicate(results)

    show_results(results, args)

    if args.zotero:
        export_zotero(results)

    if args.history:
        show_history()


# ===== Logic functions =====
def search(source, query, limit=10):
    if source == "pubmed":
        return pubmed.search(query, limit)
    elif source == "crossref":
        return crossref.search(query, limit)
    elif source == "doaj":
        return doaj.search(query, limit)
    elif source == "europepmc":
        return europepmc.search(query, limit)
    elif source == "arxiv":
        return arxiv.search(query, limit)
    return []


def normalize_string(s):
    """Normalize string for comparison (lowercase, strip whitespace)."""
    if not s:
        return ""
    return " ".join(s.lower().strip().split())


def title_similarity(title1, title2, threshold=0.85):
    """
    Calculate similarity between two titles using SequenceMatcher.
    Returns True if similarity >= threshold.
    """
    if not title1 or not title2:
        return False

    norm_title1 = normalize_string(title1)
    norm_title2 = normalize_string(title2)

    if not norm_title1 or not norm_title2:
        return False

    similarity = SequenceMatcher(None, norm_title1, norm_title2).ratio()
    return similarity >= threshold


def normalize_author_name(name):
    """
    Normalize author name for comparison.
    Handles formats like: 'Smith J', 'J Smith', 'Smith, John', 'John Smith'
    """
    if not name:
        return ""

    # Remove common punctuation and normalize whitespace
    name = name.replace(",", " ").replace(".", " ")
    parts = [p.strip() for p in name.split() if p.strip()]

    # Convert to lowercase and sort to handle different name orders
    return " ".join(sorted([p.lower() for p in parts]))


def authors_match(authors1, authors2, min_common=2):
    """
    Check if two author lists have significant overlap.
    Returns True if they share at least min_common authors.
    """
    if not authors1 or not authors2:
        return False

    # Normalize all author names
    norm_authors1 = set(normalize_author_name(a) for a in authors1)
    norm_authors2 = set(normalize_author_name(a) for a in authors2)

    # Remove empty strings
    norm_authors1.discard("")
    norm_authors2.discard("")

    if not norm_authors1 or not norm_authors2:
        return False

    # Count common authors
    common = len(norm_authors1 & norm_authors2)
    return common >= min_common


def is_duplicate(article1, article2):
    """
    Determine if two articles are duplicates using multi-level matching:
    1. Primary: DOI exact match
    2. Secondary: Title similarity (if no DOI)
    3. Tertiary: Author name matching (as additional confirmation)
    """
    # Level 1: DOI matching (most reliable)
    doi1 = article1.get("doi", "").strip()
    doi2 = article2.get("doi", "").strip()

    if doi1 and doi2:
        # Both have DOIs - compare them
        return normalize_string(doi1) == normalize_string(doi2)

    # Level 2: Title similarity (for articles without DOI or with only one DOI)
    title1 = article1.get("title", "")
    title2 = article2.get("title", "")

    if title_similarity(title1, title2):
        # Titles are very similar, check authors for additional confirmation
        authors1 = article1.get("authors", [])
        authors2 = article2.get("authors", [])

        # If we have author info, use it to confirm; otherwise trust title similarity
        if authors1 and authors2:
            # Require at least some author overlap
            return authors_match(authors1, authors2, min_common=1)
        else:
            # No author info available, rely on title similarity
            return True

    # Level 3: Strong author matching with similar (but not identical) titles
    # This catches cases where titles differ slightly (e.g., preprint vs published)
    authors1 = article1.get("authors", [])
    authors2 = article2.get("authors", [])

    if authors1 and authors2 and len(authors1) >= 2 and len(authors2) >= 2:
        # Check if many authors match AND titles are somewhat similar
        if authors_match(authors1, authors2, min_common=min(3, min(len(authors1), len(authors2)))):
            # Also check if titles are at least somewhat similar (lower threshold)
            if title1 and title2:
                similarity = SequenceMatcher(None, normalize_string(title1), normalize_string(title2)).ratio()
                if similarity >= 0.7:  # Lower threshold for author-confirmed matches
                    return True

    return False


def deduplicate(results):
    """
    Remove duplicate articles using multi-level deduplication:
    1. Primary: DOI matching
    2. Secondary: Title similarity
    3. Tertiary: Author name matching
    """
    if not results:
        return []

    unique = []

    for article in results:
        is_dup = False

        for unique_article in unique:
            if is_duplicate(article, unique_article):
                is_dup = True
                break

        if not is_dup:
            unique.append(article)

    duplicate_count = len(results) - len(unique)
    if duplicate_count > 0:
        print(f"Removed {duplicate_count} duplicate(s)")

    return unique


def filter_by_date(results, date_range):
    # TODO: implement date filtering
    return results


def show_results(results, args):
    """Show search results and optionally abstracts/detailed view."""
    for i, r in enumerate(results, start=1):
        print(f"[{i}] {r.get('title', 'No title')}")

    if args.abstract:
        print("\n--- Abstracts ---")
        for i, r in enumerate(results, start=1):
            print(f"[{i}] {r.get('abstract', 'No abstract available.')}")

    if args.number:
        # args.number is a list (because nargs="+"), loop over it
        for n in args.number:
            idx = n - 1
            if 0 <= idx < len(results):
                print("\n=== Detailed View ===")
                print(json.dumps(results[idx], indent=2, ensure_ascii=False))
            else:
                print(f"Invalid selection: {n}")


def export_zotero(results):
    # TODO: connect to Zotero
    print("Exporting to Zotero...")


def show_history():
    # TODO: implement persistent history
    print("Search history not yet implemented")


def export_to_format(results, format, filename=None):
    """
    Export results to specified format.
    
    Args:
        results: List of article dictionaries
        format: Export format ('csv', 'json', 'bibtex', 'ris')
        filename: Optional output filename
    """
    export_results(results, format, filename)


def review_articles(results, article_numbers):
    """
    Open selected articles in separate terminal windows for detailed review.
    
    Args:
        results: List of article dictionaries
        article_numbers: List of article numbers to review (1-based index)
    """
    if not results:
        print("No results to review.")
        return
    
    for num in article_numbers:
        if 1 <= num <= len(results):
            article = results[num - 1]
            print(f"Opening article #{num} in separate terminal window...")
            open_article_in_terminal(article, num)
        else:
            print(f"Warning: Article #{num} is out of range (1-{len(results)})")


def save_results(results):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


def load_cached_results():
    """
    Load previously cached search results.
    
    Returns:
        List of article dictionaries or None if no cache exists
    """
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading cached results: {e}")
            return None
    return None


def load_results():
    if not os.path.exists(CACHE_FILE):
        return []
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

