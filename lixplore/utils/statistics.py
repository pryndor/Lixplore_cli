#!/usr/bin/env python3
"""
Statistics Dashboard for Literature Analysis

Provides statistical analysis and visualization of search results including:
- Publication trends over years
- Top journals and authors
- Research field distribution
- Source distribution
"""

from collections import Counter, defaultdict
from typing import List, Dict, Optional
import sys


def _supports_unicode() -> bool:
    """Check if terminal supports Unicode."""
    try:
        "█▓▒░".encode(sys.stdout.encoding or "utf-8")
        return True
    except:
        return False


def create_bar_chart(data: Dict[str, int], title: str, max_width: int = 50, top_n: int = 10) -> str:
    """
    Create an ASCII bar chart.

    Args:
        data: Dictionary of labels to counts
        title: Chart title
        max_width: Maximum width of bars
        top_n: Number of top items to show

    Returns:
        Formatted chart string
    """
    if not data:
        return f"\n{title}\n{'=' * 60}\nNo data available.\n"

    unicode_ok = _supports_unicode()
    bar_char = "█" if unicode_ok else "#"

    # Sort by count descending and take top N
    sorted_items = sorted(data.items(), key=lambda x: x[1], reverse=True)[:top_n]

    if not sorted_items:
        return f"\n{title}\n{'=' * 60}\nNo data available.\n"

    max_count = max(count for _, count in sorted_items)
    max_label_len = max(len(str(label)) for label, _ in sorted_items)

    lines = []
    lines.append("")
    lines.append(title)
    lines.append("=" * 60)

    for label, count in sorted_items:
        # Calculate bar length
        bar_length = int((count / max_count) * max_width) if max_count > 0 else 0
        bar = bar_char * bar_length

        # Format label with padding
        label_str = str(label).ljust(max_label_len)

        # Format count
        lines.append(f"{label_str} │ {bar} {count}")

    lines.append("")
    return "\n".join(lines)


def create_histogram(data: List[int], title: str, bins: int = 10) -> str:
    """
    Create a histogram for numerical data.

    Args:
        data: List of numerical values
        title: Chart title
        bins: Number of bins

    Returns:
        Formatted histogram string
    """
    if not data:
        return f"\n{title}\n{'=' * 60}\nNo data available.\n"

    unicode_ok = _supports_unicode()
    bar_char = "█" if unicode_ok else "#"

    # Calculate bin ranges
    min_val = min(data)
    max_val = max(data)
    bin_size = (max_val - min_val) / bins if bins > 0 else 1

    # Create bins
    bin_counts = [0] * bins
    for value in data:
        if bin_size > 0:
            bin_index = min(int((value - min_val) / bin_size), bins - 1)
            bin_counts[bin_index] += 1

    # Format output
    lines = []
    lines.append("")
    lines.append(title)
    lines.append("=" * 60)

    max_count = max(bin_counts) if bin_counts else 0

    for i, count in enumerate(bin_counts):
        range_start = min_val + (i * bin_size)
        range_end = min_val + ((i + 1) * bin_size)
        bar_length = int((count / max_count) * 40) if max_count > 0 else 0
        bar = bar_char * bar_length

        lines.append(f"{int(range_start):4d}-{int(range_end):4d} │ {bar} {count}")

    lines.append("")
    return "\n".join(lines)


def analyze_publication_trends(results: List[Dict]) -> Dict[int, int]:
    """
    Analyze publication trends by year.

    Args:
        results: List of article dictionaries

    Returns:
        Dictionary mapping year to count
    """
    year_counts = Counter()

    for article in results:
        year = article.get('year')
        if year:
            try:
                year_int = int(year)
                if 1900 <= year_int <= 2100:  # Sanity check
                    year_counts[year_int] += 1
            except (ValueError, TypeError):
                pass

    return dict(year_counts)


def analyze_top_journals(results: List[Dict], top_n: int = 10) -> Dict[str, int]:
    """
    Analyze top journals.

    Args:
        results: List of article dictionaries
        top_n: Number of top journals to return

    Returns:
        Dictionary of journal names to counts
    """
    journal_counts = Counter()

    for article in results:
        journal = article.get('journal')
        if journal and journal.strip():
            journal_counts[journal.strip()] += 1

    return dict(journal_counts.most_common(top_n))


def analyze_top_authors(results: List[Dict], top_n: int = 10) -> Dict[str, int]:
    """
    Analyze top authors.

    Args:
        results: List of article dictionaries
        top_n: Number of top authors to return

    Returns:
        Dictionary of author names to counts
    """
    author_counts = Counter()

    for article in results:
        authors = article.get('authors')
        if authors:
            if isinstance(authors, list):
                for author in authors:
                    if author and author.strip():
                        author_counts[author.strip()] += 1
            elif isinstance(authors, str):
                # Split by common delimiters
                for delimiter in [',', ';', ' and ']:
                    if delimiter in authors:
                        author_list = authors.split(delimiter)
                        for author in author_list:
                            if author and author.strip():
                                author_counts[author.strip()] += 1
                        break
                else:
                    # Single author
                    if authors.strip():
                        author_counts[authors.strip()] += 1

    return dict(author_counts.most_common(top_n))


def analyze_source_distribution(results: List[Dict]) -> Dict[str, int]:
    """
    Analyze distribution of sources.

    Args:
        results: List of article dictionaries

    Returns:
        Dictionary of source names to counts
    """
    source_counts = Counter()

    for article in results:
        source = article.get('source', 'Unknown')
        source_counts[source] += 1

    return dict(source_counts)


def calculate_basic_stats(results: List[Dict]) -> Dict[str, any]:
    """
    Calculate basic statistics.

    Args:
        results: List of article dictionaries

    Returns:
        Dictionary of basic statistics
    """
    total = len(results)
    with_abstract = sum(1 for r in results if r.get('abstract'))
    with_doi = sum(1 for r in results if r.get('doi'))
    with_authors = sum(1 for r in results if r.get('authors'))

    # Year statistics
    years = []
    for article in results:
        year = article.get('year')
        if year:
            try:
                year_int = int(year)
                if 1900 <= year_int <= 2100:
                    years.append(year_int)
            except (ValueError, TypeError):
                pass

    return {
        'total': total,
        'with_abstract': with_abstract,
        'with_doi': with_doi,
        'with_authors': with_authors,
        'abstract_percentage': (with_abstract / total * 100) if total > 0 else 0,
        'doi_percentage': (with_doi / total * 100) if total > 0 else 0,
        'oldest_year': min(years) if years else None,
        'newest_year': max(years) if years else None,
        'year_range': f"{min(years)}-{max(years)}" if years else "N/A"
    }


def generate_statistics_report(results: List[Dict], top_n: int = 10) -> str:
    """
    Generate comprehensive statistics report.

    Args:
        results: List of article dictionaries
        top_n: Number of top items to show in rankings

    Returns:
        Formatted statistics report
    """
    if not results:
        return "\nNo results to analyze.\n"

    unicode_ok = _supports_unicode()
    separator = "━" * 60 if unicode_ok else "=" * 60

    lines = []
    lines.append("")
    lines.append("LITERATURE STATISTICS DASHBOARD")
    lines.append(separator)
    lines.append("")

    # Basic Statistics
    basic_stats = calculate_basic_stats(results)
    lines.append("📈 Basic Statistics" if unicode_ok else "BASIC STATISTICS")
    lines.append("-" * 60)
    lines.append(f"Total Articles: {basic_stats['total']}")
    lines.append(f"With Abstract: {basic_stats['with_abstract']} ({basic_stats['abstract_percentage']:.1f}%)")
    lines.append(f"With DOI: {basic_stats['with_doi']} ({basic_stats['doi_percentage']:.1f}%)")
    lines.append(f"With Authors: {basic_stats['with_authors']}")
    lines.append(f"Year Range: {basic_stats['year_range']}")
    lines.append("")

    # Source Distribution
    source_dist = analyze_source_distribution(results)
    lines.append(create_bar_chart(
        source_dist,
        "SOURCE DISTRIBUTION",
        max_width=40,
        top_n=20
    ))

    # Publication Trends
    year_trends = analyze_publication_trends(results)
    if year_trends:
        lines.append(create_bar_chart(
            year_trends,
            "📅 Publication Trends by Year" if unicode_ok else "PUBLICATION TRENDS BY YEAR",
            max_width=40,
            top_n=15
        ))

    # Top Journals
    top_journals = analyze_top_journals(results, top_n)
    if top_journals:
        lines.append(create_bar_chart(
            top_journals,
            f"Top {top_n} Journals" if unicode_ok else f"TOP {top_n} JOURNALS",
            max_width=40,
            top_n=top_n
        ))

    # Top Authors
    top_authors = analyze_top_authors(results, top_n)
    if top_authors:
        lines.append(create_bar_chart(
            top_authors,
            f"👥 Top {top_n} Authors" if unicode_ok else f"TOP {top_n} AUTHORS",
            max_width=40,
            top_n=top_n
        ))

    lines.append(separator)
    lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    # Test with sample data
    sample_results = [
        {'title': 'Article 1', 'year': 2020, 'journal': 'Nature', 'authors': ['Smith J', 'Doe A'], 'source': 'PubMed', 'abstract': 'Test', 'doi': '10.1234/test'},
        {'title': 'Article 2', 'year': 2021, 'journal': 'Science', 'authors': ['Smith J'], 'source': 'PubMed', 'abstract': 'Test'},
        {'title': 'Article 3', 'year': 2020, 'journal': 'Nature', 'authors': ['Johnson B'], 'source': 'Crossref'},
        {'title': 'Article 4', 'year': 2022, 'journal': 'Cell', 'authors': ['Smith J', 'Lee C'], 'source': 'PubMed', 'abstract': 'Test', 'doi': '10.1234/test2'},
        {'title': 'Article 5', 'year': 2021, 'journal': 'Nature', 'authors': ['Doe A'], 'source': 'arXiv'},
    ]

    print(generate_statistics_report(sample_results, top_n=3))
