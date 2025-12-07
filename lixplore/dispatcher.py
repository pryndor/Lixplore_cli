#!/usr/bin/env python3

from lixplore.sources import pubmed, crossref, doaj, europepmc, arxiv
from lixplore.utils.terminal import open_in_new_terminal
import json
import os

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


def deduplicate(results):
    seen = set()
    unique = []
    for r in results:
        key = r.get("doi") or r.get("title")
        if key not in seen:
            seen.add(key)
            unique.append(r)
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


def save_results(results):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


def load_results():
    if not os.path.exists(CACHE_FILE):
        return []
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

