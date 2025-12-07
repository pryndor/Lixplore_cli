#!/usr/bin/env python3

import litstudy

def test_scopus_search():
    """Search directly in Scopus (requires API key)."""
    print("=== Scopus Search Test ===")
    try:
        docs = litstudy.search_scopus("pharmacovigilance biosimilars", limit=5)
        for d in docs:
            print(f"Title   : {d.title}")
            print(f"Authors : {', '.join(d.authors)}")
            print(f"Year    : {d.year}")
            print(f"DOI     : {d.doi}")
            print(f"URL     : {d.url}")
            print("-" * 40)
    except Exception as e:
        print("Scopus API search failed:", e)


def test_scopus_refine():
    """Take some docs from Crossref and refine with Scopus metadata."""
    print("=== Scopus Refine Test ===")
    docs = litstudy.search_crossref("pharmacovigilance biosimilars", limit=3)
    scopus_docs, remaining = litstudy.refine_scopus(docs)

    print(f"Found in Scopus: {len(scopus_docs)}")
    for d in scopus_docs:
        print(f"[Scopus] {d.title} — {d.doi}")

    print(f"Remaining (not found in Scopus): {len(remaining)}")


def test_scopus_csv():
    """Load articles from a Scopus CSV export (works without API)."""
    print("=== Scopus CSV Load Test ===")
    path = "scopus_export.csv"  # replace with your CSV path
    try:
        docs = litstudy.load_scopus_csv(path)
        for d in docs:
            print(f"Title   : {d.title}")
            print(f"DOI     : {d.doi}")
            print(f"Year    : {d.year}")
            print("-" * 40)
    except FileNotFoundError:
        print("No CSV file found. Export one from Scopus and try again.")


if __name__ == "__main__":
    # Run all tests
    test_scopus_search()
    test_scopus_refine()
    test_scopus_csv()

