#!/usr/bin/env python3

from lixplore.sources import pubmed, crossref, doaj, europepmc, arxiv
from lixplore.utils.terminal import open_in_new_terminal, open_article_in_terminal
from lixplore.utils.export import export_results
import json
import os
from difflib import SequenceMatcher
from datetime import datetime, timedelta

CACHE_FILE = os.path.expanduser("~/.lixplore_cache.json")
CACHE_EXPIRY_DAYS = 7  # Default cache expiration in days
HISTORY_FILE = os.path.expanduser("~/.lixplore_history.json")
MAX_HISTORY_ENTRIES = 100  # Maximum number of history entries to keep


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


def get_completeness_score(article):
    """
    Calculate how complete an article's metadata is.
    Returns a score based on number of filled fields.
    """
    score = 0
    fields = ['title', 'authors', 'abstract', 'journal', 'year', 'doi', 'url', 'source']

    for field in fields:
        value = article.get(field)
        if value:
            if isinstance(value, str) and value.strip():
                score += 1
            elif isinstance(value, list) and len(value) > 0:
                score += 1

    # Bonus for having DOI (most valuable field)
    if article.get('doi', '').strip():
        score += 2

    # Bonus for having abstract (indicates complete metadata)
    if article.get('abstract', '').strip():
        score += 1

    return score


def merge_duplicate_metadata(article1, article2):
    """
    Merge metadata from two duplicate articles.
    Takes best available data from both.
    """
    merged = {}
    fields = ['title', 'authors', 'abstract', 'journal', 'year', 'doi', 'url', 'source']

    for field in fields:
        val1 = article1.get(field)
        val2 = article2.get(field)

        if isinstance(val1, str) and isinstance(val2, str):
            # For strings, prefer longer/more complete value
            if val1 and val2:
                merged[field] = val1 if len(val1) >= len(val2) else val2
            else:
                merged[field] = val1 or val2
        elif isinstance(val1, list) and isinstance(val2, list):
            # For lists (like authors), combine and deduplicate
            combined = list(val1) if val1 else []
            if val2:
                for item in val2:
                    if item not in combined:
                        combined.append(item)
            merged[field] = combined
        else:
            # Take whichever is available
            merged[field] = val1 if val1 else val2

    return merged


def is_duplicate_with_strategy(article1, article2, strategy='auto', threshold=0.85):
    """
    Determine if two articles are duplicates using specified strategy.

    Args:
        article1, article2: Articles to compare
        strategy: 'auto', 'doi_only', 'title_only', 'strict', 'loose'
        threshold: Similarity threshold for title matching

    Returns:
        True if articles are duplicates
    """
    if strategy == 'doi_only':
        # Only match by DOI
        doi1 = article1.get("doi", "").strip()
        doi2 = article2.get("doi", "").strip()
        if doi1 and doi2:
            return normalize_string(doi1) == normalize_string(doi2)
        return False

    elif strategy == 'title_only':
        # Only match by title similarity
        title1 = article1.get("title", "")
        title2 = article2.get("title", "")
        return title_similarity(title1, title2, threshold=threshold)

    elif strategy == 'strict':
        # Higher thresholds for stricter matching
        return is_duplicate_with_strategy(article1, article2, strategy='auto', threshold=0.95)

    elif strategy == 'loose':
        # Lower thresholds for looser matching
        return is_duplicate_with_strategy(article1, article2, strategy='auto', threshold=0.75)

    else:  # 'auto' or default
        # Use existing multi-level logic with custom threshold
        doi1 = article1.get("doi", "").strip()
        doi2 = article2.get("doi", "").strip()

        if doi1 and doi2:
            return normalize_string(doi1) == normalize_string(doi2)

        title1 = article1.get("title", "")
        title2 = article2.get("title", "")

        if title_similarity(title1, title2, threshold=threshold):
            authors1 = article1.get("authors", [])
            authors2 = article2.get("authors", [])

            if authors1 and authors2:
                return authors_match(authors1, authors2, min_common=1)
            else:
                return True

        authors1 = article1.get("authors", [])
        authors2 = article2.get("authors", [])

        if authors1 and authors2 and len(authors1) >= 2 and len(authors2) >= 2:
            if authors_match(authors1, authors2, min_common=min(3, min(len(authors1), len(authors2)))):
                if title1 and title2:
                    similarity = SequenceMatcher(None, normalize_string(title1), normalize_string(title2)).ratio()
                    if similarity >= (threshold - 0.15):  # Slightly lower for author-confirmed
                        return True

        return False


def deduplicate_advanced(results, strategy='auto', title_threshold=0.85, keep_preference='most_complete', merge_metadata=False):
    """
    Enhanced deduplication with configurable strategies.

    Args:
        results: List of article dictionaries
        strategy: Deduplication strategy ('auto', 'doi_only', 'title_only', 'strict', 'loose')
        title_threshold: Similarity threshold for title matching (0.0-1.0)
        keep_preference: Which duplicate to keep ('first', 'most_complete', 'prefer_doi')
        merge_metadata: If True, merge metadata from duplicates

    Returns:
        Deduplicated list of articles
    """
    if not results:
        return []

    unique = []
    duplicates_found = []

    for article in results:
        is_dup = False
        dup_index = -1

        for idx, unique_article in enumerate(unique):
            if is_duplicate_with_strategy(article, unique_article, strategy, title_threshold):
                is_dup = True
                dup_index = idx
                break

        if is_dup:
            duplicates_found.append((article, dup_index))

            if merge_metadata:
                # Merge metadata from duplicate into existing unique entry
                unique[dup_index] = merge_duplicate_metadata(unique[dup_index], article)
            elif keep_preference == 'most_complete':
                # Replace if new article has more complete metadata
                if get_completeness_score(article) > get_completeness_score(unique[dup_index]):
                    unique[dup_index] = article
            elif keep_preference == 'prefer_doi':
                # Replace if new article has DOI and existing doesn't
                if article.get('doi', '').strip() and not unique[dup_index].get('doi', '').strip():
                    unique[dup_index] = article
            # For 'first', do nothing (keep existing)
        else:
            unique.append(article)

    duplicate_count = len(duplicates_found)
    if duplicate_count > 0:
        action = "merged metadata from" if merge_metadata else "removed"
        print(f"Deduplication ({strategy}): {action} {duplicate_count} duplicate(s)")

    return unique


def filter_by_date(results, date_range):
    # TODO: implement date filtering
    return results


def paginate_results(results, page=1, page_size=20):
    """
    Paginate results for display.

    Args:
        results: List of all results
        page: Page number (1-indexed)
        page_size: Number of results per page

    Returns:
        Tuple of (paginated_results, total_pages, start_index, end_index)
    """
    total_results = len(results)
    total_pages = (total_results + page_size - 1) // page_size  # Ceiling division

    # Validate page number
    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages if total_pages > 0 else 1

    # Calculate indices
    start_index = (page - 1) * page_size
    end_index = min(start_index + page_size, total_results)

    # Get paginated results
    paginated = results[start_index:end_index]

    return paginated, total_pages, start_index, end_index


def make_clickable_link(url: str, text: str) -> str:
    """
    Create a clickable hyperlink using OSC 8 terminal escape sequences.
    Supported by modern terminals (iTerm2, GNOME Terminal, etc.)

    Args:
        url: The URL to link to
        text: The visible text

    Returns:
        Formatted string with hyperlink
    """
    return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"


def show_results(results, args):
    """Show search results with pagination support and optional abstracts/detailed view."""
    total_results = len(results)

    # Check if pagination is needed
    page = getattr(args, 'page', 1)
    page_size = getattr(args, 'page_size', 20)
    show_pdf_links = getattr(args, 'show_pdf_links', False)

    # Fetch PDF links if requested
    pdf_links = {}
    if show_pdf_links:
        print("\nChecking for open access PDFs...")
        from lixplore.utils.pdf_downloader import get_pdf_links_batch
        pdf_links = get_pdf_links_batch(results)
        if pdf_links:
            print(f"Found {len(pdf_links)} PDF(s) available\n")
        else:
            print("Info: No open access PDFs found\n")

    # Only paginate if results exceed page size
    if total_results > page_size:
        paginated, total_pages, start_idx, end_idx = paginate_results(results, page, page_size)

        # Show pagination info
        print(f"\n📄 Page {page} of {total_pages} | Showing {start_idx + 1}-{end_idx} of {total_results} results")
        print(f"   Use -p {page + 1} to see next page" if page < total_pages else "   (Last page)")
        print("")

        # Display paginated results
        for i, r in enumerate(paginated, start=start_idx + 1):
            title = r.get('title', 'No title')
            print(f"[{i}] {title}")

            # Show PDF link if available
            if show_pdf_links and (i - 1) in pdf_links:
                pdf_url = pdf_links[i - 1]
                clickable = make_clickable_link(pdf_url, "Open PDF")
                print(f"    {clickable} → {pdf_url}")

        # Show abstracts for paginated results if requested
        if args.abstract:
            print("\n--- Abstracts ---")
            for i, r in enumerate(paginated, start=start_idx + 1):
                print(f"[{i}] {r.get('abstract', 'No abstract available.')}")
    else:
        # No pagination needed - show all results
        for i, r in enumerate(results, start=1):
            title = r.get('title', 'No title')
            print(f"[{i}] {title}")

            # Show PDF link if available
            if show_pdf_links and (i - 1) in pdf_links:
                pdf_url = pdf_links[i - 1]
                clickable = make_clickable_link(pdf_url, "Open PDF")
                print(f"    {clickable} → {pdf_url}")

        if args.abstract:
            print("\n--- Abstracts ---")
            for i, r in enumerate(results, start=1):
                print(f"[{i}] {r.get('abstract', 'No abstract available.')}")

    # Detailed view is independent of pagination
    if args.number:
        # args.number is a list (because nargs="+"), loop over it
        for n in args.number:
            idx = n - 1
            if 0 <= idx < total_results:
                print("\n=== Detailed View ===")
                print(json.dumps(results[idx], indent=2, ensure_ascii=False))
            else:
                print(f"Invalid selection: {n}")


def save_to_history(query, sources, result_count):
    """
    Save search to history file.

    Args:
        query: Search query string
        sources: List of sources searched
        result_count: Number of results found
    """
    history_entry = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "sources": sources if sources else [],
        "result_count": result_count
    }

    # Load existing history
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except (json.JSONDecodeError, IOError):
            history = []

    # Add new entry at the beginning (most recent first)
    history.insert(0, history_entry)

    # Keep only the most recent MAX_HISTORY_ENTRIES
    history = history[:MAX_HISTORY_ENTRIES]

    # Save updated history
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except IOError as e:
        # Silently fail if we can't write history (not critical)
        pass


def show_history():
    """Display search history."""
    if not os.path.exists(HISTORY_FILE):
        print("No search history found.")
        print("Run a search to start building history (e.g., lixplore -P -q \"cancer\" -m 10)")
        return

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    except (json.JSONDecodeError, IOError):
        print("Error reading history file.")
        return

    if not history:
        print("No search history found.")
        return

    print(f"\n{'='*80}")
    print(f"SEARCH HISTORY ({len(history)} searches)")
    print(f"{'='*80}\n")

    for i, entry in enumerate(history, 1):
        timestamp = entry.get("timestamp", "Unknown time")
        query = entry.get("query", "Unknown query")
        sources = entry.get("sources", [])
        result_count = entry.get("result_count", 0)

        # Parse timestamp for display
        try:
            dt = datetime.fromisoformat(timestamp)
            time_str = dt.strftime("%Y-%m-%d %H:%M:%S")

            # Calculate how long ago
            now = datetime.now()
            delta = now - dt
            if delta.days > 0:
                ago = f"{delta.days} day{'s' if delta.days != 1 else ''} ago"
            elif delta.seconds >= 3600:
                hours = delta.seconds // 3600
                ago = f"{hours} hour{'s' if hours != 1 else ''} ago"
            elif delta.seconds >= 60:
                minutes = delta.seconds // 60
                ago = f"{minutes} minute{'s' if minutes != 1 else ''} ago"
            else:
                ago = "just now"
        except (ValueError, AttributeError):
            time_str = timestamp
            ago = ""

        # Format sources
        source_names = {
            "pubmed": "PubMed",
            "crossref": "Crossref",
            "doaj": "DOAJ",
            "europepmc": "EuropePMC",
            "arxiv": "arXiv"
        }

        sources_display = []
        for src in sources:
            # Handle custom API format "custom:springer"
            if src.startswith("custom:"):
                api_name = src.split(":", 1)[1]
                sources_display.append(f"{api_name} (custom)")
            else:
                sources_display.append(source_names.get(src, src))

        sources_str = ", ".join(sources_display) if sources_display else "Unknown"

        print(f"[{i}] {time_str} ({ago})")
        print(f"    Query: {query}")
        print(f"    Sources: {sources_str}")
        print(f"    Results: {result_count}")
        print()

    print(f"{'='*80}")
    print(f"History file: {HISTORY_FILE}")
    print(f"Showing {len(history)} most recent searches (max: {MAX_HISTORY_ENTRIES})")
    print(f"{'='*80}\n")


def export_to_format(results, format, filename=None, fields=None, compress=False):
    """
    Export results to specified format.

    Args:
        results: List of article dictionaries
        format: Export format ('csv', 'json', 'bibtex', 'ris', etc.')
        filename: Optional output filename
        fields: Optional list of field names to export
        compress: If True, compress exported file to ZIP
    """
    from lixplore.utils.export import compress_export
    exported_path = export_results(results, format, filename, fields)

    # Compress if requested
    if compress and exported_path:
        compress_export(exported_path, remove_original=False)

    return exported_path


def batch_export(results, formats, output_base=None, fields=None, compress=False):
    """
    Export results to multiple formats simultaneously.

    Args:
        results: List of article dictionaries
        formats: List of format names ('csv', 'ris', 'bibtex', etc.)
        output_base: Optional base filename (without extension)
        fields: Optional list of field names to export
        compress: If True, compress each exported file to ZIP

    Returns:
        List of exported file paths
    """
    if not results:
        print("No results to export.")
        return []

    if not formats:
        print("No export formats specified.")
        return []

    print(f"Batch exporting to {len(formats)} format(s): {', '.join(formats)}")

    exported_files = []
    for format in formats:
        # Generate format-specific filename if base provided
        if output_base:
            # Get appropriate extension for format
            ext_map = {
                'csv': 'csv',
                'json': 'json',
                'bibtex': 'bib',
                'ris': 'ris',
                'endnote': 'xml',
                'enw': 'enw',
                'xlsx': 'xlsx',
                'xml': 'xml'
            }
            ext = ext_map.get(format, format)
            filename = f"{output_base}.{ext}"
        else:
            filename = None

        # Export to this format
        exported_path = export_to_format(results, format, filename, fields, compress)
        if exported_path:
            exported_files.append(exported_path)

    print(f"\nBatch export complete: {len(exported_files)} file(s) created")
    return exported_files


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


def save_results(results, query=None, sources=None):
    """
    Save search results to cache with timestamp and metadata.

    Args:
        results: List of article dictionaries
        query: Search query string (optional)
        sources: List of sources searched (optional)
    """
    cache_data = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "sources": sources,
        "count": len(results),
        "results": results
    }
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=2)


def load_cached_results(check_expiry=True, force_refresh=False):
    """
    Load previously cached search results with expiration checking.

    Args:
        check_expiry: If True, check if cache has expired (default: True)
        force_refresh: If True, ignore cache and return None (default: False)

    Returns:
        List of article dictionaries or None if no cache/expired
    """
    if force_refresh:
        return None

    if not os.path.exists(CACHE_FILE):
        return None

    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache_data = json.load(f)

        # Handle old cache format (just array of results)
        if isinstance(cache_data, list):
            print("Cache format outdated, will refresh...")
            return None

        # Check expiration if enabled
        if check_expiry and "timestamp" in cache_data:
            cached_time = datetime.fromisoformat(cache_data["timestamp"])
            expiry_time = cached_time + timedelta(days=CACHE_EXPIRY_DAYS)

            if datetime.now() > expiry_time:
                print(f"Cache expired (older than {CACHE_EXPIRY_DAYS} days)")
                return None

            # Show cache age
            age = datetime.now() - cached_time
            if age.days > 0:
                print(f"Using cached results ({age.days} day(s) old)")
            else:
                hours = age.seconds // 3600
                print(f"Using cached results ({hours} hour(s) old)")

        # Return just the results array
        return cache_data.get("results", [])

    except Exception as e:
        print(f"Error loading cached results: {e}")
        return None


def load_results():
    """Legacy function for backward compatibility."""
    cached = load_cached_results(check_expiry=False)
    return cached if cached else []

