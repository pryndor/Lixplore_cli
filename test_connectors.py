#!/usr/bin/env python3

"""
Test script for all Lixplore CLI connectors
Tests PubMed, Crossref, DOAJ, EuropePMC, and arXiv
"""

import sys
from lixplore.sources import pubmed, crossref, doaj, europepmc, arxiv


def test_source(source_name, source_module, query, max_results=5):
    """Test a single source connector"""
    print(f"\n{'='*60}")
    print(f"Testing {source_name}")
    print(f"{'='*60}")
    print(f"Query: '{query}'")
    print(f"Max results: {max_results}")
    print("-" * 60)

    try:
        results = source_module.search(query, max_results)

        if not results:
            print(f"❌ No results returned from {source_name}")
            return False

        print(f"✅ {source_name} returned {len(results)} results\n")

        # Display first result in detail
        if results:
            first = results[0]
            print(f"Sample result:")
            print(f"  Title: {first.get('title', 'N/A')[:80]}...")
            print(f"  Authors: {', '.join(first.get('authors', [])[:3])}{'...' if len(first.get('authors', [])) > 3 else ''}")
            print(f"  Journal: {first.get('journal', 'N/A')}")
            print(f"  Year: {first.get('year', 'N/A')}")
            print(f"  DOI: {first.get('doi', 'N/A')}")
            print(f"  URL: {first.get('url', 'N/A')}")
            print(f"  Abstract: {first.get('abstract', 'N/A')[:100]}...")

        return True

    except Exception as e:
        print(f"❌ Error testing {source_name}: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all connector tests"""
    print("\n" + "="*60)
    print("LIXPLORE CLI - CONNECTOR TEST SUITE")
    print("="*60)

    # Test configuration
    test_queries = {
        "pubmed": "diabetes treatment",
        "crossref": "machine learning",
        "doaj": "climate change",
        "europepmc": "COVID-19",
        "arxiv": "neural networks"
    }

    results_summary = {}

    # Test each connector
    sources = [
        ("PubMed", pubmed, test_queries["pubmed"]),
        ("Crossref", crossref, test_queries["crossref"]),
        ("DOAJ", doaj, test_queries["doaj"]),
        ("EuropePMC", europepmc, test_queries["europepmc"]),
        ("arXiv", arxiv, test_queries["arxiv"])
    ]

    for name, module, query in sources:
        success = test_source(name, module, query, max_results=5)
        results_summary[name] = "✅ PASSED" if success else "❌ FAILED"

    # Print summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")

    for source, status in results_summary.items():
        print(f"{source:15} {status}")

    print(f"{'='*60}\n")

    # Check if all passed
    all_passed = all("PASSED" in status for status in results_summary.values())

    if all_passed:
        print("🎉 All connectors working successfully!")
        return 0
    else:
        print("⚠️  Some connectors failed. Check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
