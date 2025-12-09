#!/usr/bin/env python3
"""
Test script to verify deduplication logic
"""

from lixplore.dispatcher import deduplicate

# Test cases for deduplication
test_results = [
    # Case 1: Exact duplicate by DOI
    {
        "title": "Machine Learning in Healthcare",
        "doi": "10.1234/example.001",
        "authors": ["Smith J", "Doe A"]
    },
    {
        "title": "Machine Learning in Healthcare",
        "doi": "10.1234/example.001",
        "authors": ["Smith, John", "Doe, Alice"]  # Different author format
    },

    # Case 2: Same article, one without DOI (should be caught by title similarity)
    {
        "title": "Deep Learning for Medical Imaging",
        "doi": "",
        "authors": ["Johnson B", "Lee C"]
    },
    {
        "title": "Deep Learning for Medical Imaging",
        "doi": "",
        "authors": ["Johnson B", "Lee C"]
    },

    # Case 3: Preprint vs published (slight title difference, same authors)
    {
        "title": "Novel Approach to Cancer Detection",
        "doi": "",
        "authors": ["Brown M", "Taylor R", "Wilson K"]
    },
    {
        "title": "A Novel Approach to Cancer Detection Using AI",  # Slightly different
        "doi": "10.5678/published.002",
        "authors": ["Brown M", "Taylor R", "Wilson K"]
    },

    # Case 4: Different articles (should NOT be deduplicated)
    {
        "title": "Quantum Computing Applications",
        "doi": "10.9999/quantum.001",
        "authors": ["Einstein A", "Bohr N"]
    },
    {
        "title": "Neural Networks for Image Recognition",
        "doi": "10.8888/neural.002",
        "authors": ["Turing A", "von Neumann J"]
    },

    # Case 5: Similar title but different authors (should NOT be deduplicated)
    {
        "title": "COVID-19 Vaccine Efficacy Study",
        "doi": "",
        "authors": ["Wang X", "Zhang Y"]
    },
    {
        "title": "COVID-19 Vaccine Efficacy Study",
        "doi": "",
        "authors": ["Miller P", "Garcia R"]  # Completely different authors
    },
]

if __name__ == "__main__":
    print("=" * 60)
    print("DEDUPLICATION TEST")
    print("=" * 60)
    print(f"\nTotal articles before deduplication: {len(test_results)}")
    print("\nOriginal articles:")
    for i, article in enumerate(test_results, 1):
        doi = article.get('doi') or '(no DOI)'
        authors = ', '.join(article.get('authors', []))
        print(f"{i}. {article['title']}")
        print(f"   DOI: {doi}")
        print(f"   Authors: {authors}")
        print()

    # Run deduplication
    unique_results = deduplicate(test_results)

    print("\n" + "=" * 60)
    print(f"Total articles after deduplication: {len(unique_results)}")
    print("=" * 60)
    print("\nUnique articles:")
    for i, article in enumerate(unique_results, 1):
        doi = article.get('doi') or '(no DOI)'
        authors = ', '.join(article.get('authors', []))
        print(f"{i}. {article['title']}")
        print(f"   DOI: {doi}")
        print(f"   Authors: {authors}")
        print()

    print("\n" + "=" * 60)
    print("EXPECTED BEHAVIOR:")
    print("=" * 60)
    print("- Articles 1 & 2: Should be merged (same DOI) → 1 unique")
    print("- Articles 3 & 4: Should be merged (same title, no DOI) → 1 unique")
    print("- Articles 5 & 6: Should be merged (similar title, same authors) → 1 unique")
    print("- Articles 7 & 8: Should be kept separate (different content) → 2 unique")
    print("- Articles 9 & 10: Should be kept separate (same title, different authors) → 2 unique")
    print(f"\nExpected unique count: 7 (3 merged groups + 2 separate pairs)")
    print(f"Actual unique count: {len(unique_results)}")

    # Verify specific expectations
    titles = [article.get('title', '') for article in unique_results]
    dois = [article.get('doi', '') for article in unique_results]

    checks = {
        "Merged by DOI (articles 1&2)": any('Machine Learning in Healthcare' in t for t in titles),
        "Merged by title (articles 3&4)": any('Deep Learning for Medical Imaging' in t for t in titles),
        "Merged by title+authors (articles 5&6)": titles.count('Novel Approach to Cancer Detection') == 1 or
                                                    any('Novel Approach to Cancer Detection' in t for t in titles),
        "Separate COVID articles": titles.count('COVID-19 Vaccine Efficacy Study') == 2,
        "Has Quantum article": any('Quantum Computing' in t for t in titles),
        "Has Neural Networks article": any('Neural Networks' in t for t in titles),
    }

    print("\nDetailed checks:")
    all_passed = True
    for check_name, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check_name}")
        if not passed:
            all_passed = False

    if len(unique_results) == 7 and all_passed:
        print("\n✅ DEDUPLICATION TEST PASSED!")
    else:
        print("\n❌ DEDUPLICATION TEST FAILED!")
        if len(unique_results) != 7:
            print(f"   Expected 7 unique articles, got {len(unique_results)}")
