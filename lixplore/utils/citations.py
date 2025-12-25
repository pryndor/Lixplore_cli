#!/usr/bin/env python3

"""
Citation formatting utilities for Lixplore - support for APA, MLA, Chicago, and IEEE styles
"""

from typing import Dict, List


def format_authors_apa(authors: List[str]) -> str:
    """Format authors for APA style: Last, F. M."""
    if not authors:
        return ""

    formatted = []
    for author in authors:
        parts = author.split()
        if len(parts) >= 2:
            # Assume last name is last, first name(s) are first
            last = parts[-1]
            initials = '. '.join([p[0] for p in parts[:-1]]) + '.'
            formatted.append(f"{last}, {initials}")
        else:
            formatted.append(author)

    if len(formatted) == 1:
        return formatted[0]
    elif len(formatted) == 2:
        return f"{formatted[0]}, & {formatted[1]}"
    else:
        return ', '.join(formatted[:-1]) + f", & {formatted[-1]}"


def format_authors_mla(authors: List[str]) -> str:
    """Format authors for MLA style: Last, First"""
    if not authors:
        return ""

    formatted = []
    for author in authors:
        parts = author.split()
        if len(parts) >= 2:
            last = parts[-1]
            first = ' '.join(parts[:-1])
            formatted.append(f"{last}, {first}")
        else:
            formatted.append(author)

    if len(formatted) == 1:
        return formatted[0]
    elif len(formatted) == 2:
        return f"{formatted[0]}, and {formatted[1]}"
    else:
        return ', '.join(formatted[:-1]) + f", and {formatted[-1]}"


def format_authors_chicago(authors: List[str]) -> str:
    """Format authors for Chicago style: Last, First"""
    # Chicago uses same format as MLA
    return format_authors_mla(authors)


def format_authors_ieee(authors: List[str]) -> str:
    """Format authors for IEEE style: F. M. Last"""
    if not authors:
        return ""

    formatted = []
    for author in authors:
        parts = author.split()
        if len(parts) >= 2:
            last = parts[-1]
            initials = '. '.join([p[0] for p in parts[:-1]]) + '.'
            formatted.append(f"{initials} {last}")
        else:
            formatted.append(author)

    if len(formatted) <= 3:
        return ', '.join(formatted)
    else:
        return ', '.join(formatted[:3]) + ', et al.'


def format_citation_apa(article: Dict) -> str:
    """
    Format article as APA citation.
    Format: Author, A. A. (Year). Title. Journal, volume(issue), pages. DOI
    """
    parts = []

    # Authors
    authors = article.get('authors', [])
    if authors:
        parts.append(format_authors_apa(authors))

    # Year
    year = article.get('year', '')
    if year:
        parts.append(f"({year}).")

    # Title
    title = article.get('title', '')
    if title:
        parts.append(f"{title}.")

    # Journal
    journal = article.get('journal', '')
    if journal:
        parts.append(f"*{journal}*.")

    # DOI or URL
    doi = article.get('doi', '')
    url = article.get('url', '')
    if doi:
        parts.append(f"https://doi.org/{doi}")
    elif url:
        parts.append(url)

    return ' '.join(parts)


def format_citation_mla(article: Dict) -> str:
    """
    Format article as MLA citation.
    Format: Author. "Title." Journal vol.issue (Year): pages. DOI
    """
    parts = []

    # Authors
    authors = article.get('authors', [])
    if authors:
        parts.append(format_authors_mla(authors) + '.')

    # Title in quotes
    title = article.get('title', '')
    if title:
        parts.append(f'"{title}."')

    # Journal in italics
    journal = article.get('journal', '')
    if journal:
        parts.append(f'*{journal}*')

    # Year
    year = article.get('year', '')
    if year:
        parts.append(f'({year}).')

    # DOI or URL
    doi = article.get('doi', '')
    url = article.get('url', '')
    if doi:
        parts.append(f"DOI: {doi}")
    elif url:
        parts.append(url)

    return ' '.join(parts)


def format_citation_chicago(article: Dict) -> str:
    """
    Format article as Chicago citation.
    Format: Author. "Title." Journal vol, no. issue (Year): pages. DOI
    """
    parts = []

    # Authors
    authors = article.get('authors', [])
    if authors:
        parts.append(format_authors_chicago(authors) + '.')

    # Title in quotes
    title = article.get('title', '')
    if title:
        parts.append(f'"{title}."')

    # Journal in italics
    journal = article.get('journal', '')
    if journal:
        parts.append(f'*{journal}*')

    # Year
    year = article.get('year', '')
    if year:
        parts.append(f'({year}).')

    # DOI or URL
    doi = article.get('doi', '')
    url = article.get('url', '')
    if doi:
        parts.append(f"https://doi.org/{doi}")
    elif url:
        parts.append(url)

    return ' '.join(parts)


def format_citation_ieee(article: Dict) -> str:
    """
    Format article as IEEE citation.
    Format: [1] F. M. Last, "Title," Journal, vol. X, Year. DOI
    """
    parts = []

    # Authors
    authors = article.get('authors', [])
    if authors:
        parts.append(format_authors_ieee(authors) + ',')

    # Title in quotes
    title = article.get('title', '')
    if title:
        parts.append(f'"{title},"')

    # Journal in italics
    journal = article.get('journal', '')
    if journal:
        parts.append(f'*{journal}*,')

    # Year
    year = article.get('year', '')
    if year:
        parts.append(f'{year}.')

    # DOI or URL
    doi = article.get('doi', '')
    url = article.get('url', '')
    if doi:
        parts.append(f"DOI: {doi}")
    elif url:
        parts.append(url)

    return ' '.join(parts)


def format_citations(articles: List[Dict], style: str) -> List[str]:
    """
    Format list of articles using specified citation style.

    Args:
        articles: List of article dictionaries
        style: Citation style ('apa', 'mla', 'chicago', 'ieee')

    Returns:
        List of formatted citations
    """
    style = style.lower()

    formatters = {
        'apa': format_citation_apa,
        'mla': format_citation_mla,
        'chicago': format_citation_chicago,
        'ieee': format_citation_ieee
    }

    formatter = formatters.get(style)
    if not formatter:
        raise ValueError(f"Unsupported citation style: {style}")

    citations = []
    for i, article in enumerate(articles, start=1):
        if style == 'ieee':
            # IEEE uses numbered citations
            citation = f"[{i}] {formatter(article)}"
        else:
            citation = formatter(article)
        citations.append(citation)

    return citations
