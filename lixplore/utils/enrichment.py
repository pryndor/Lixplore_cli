#!/usr/bin/env python3

"""
Metadata enrichment utilities for Lixplore - enrich articles using external APIs
"""

import time
import requests
from typing import Dict, List


# Rate limiting settings
RATE_LIMIT_DELAY = 0.5  # seconds between API calls


def validate_doi(doi: str) -> bool:
    """
    Validate DOI format and check if it resolves.

    Args:
        doi: DOI string

    Returns:
        True if valid and resolvable
    """
    if not doi:
        return False

    # Clean DOI (remove https://doi.org/ prefix if present)
    doi = doi.replace('https://doi.org/', '').replace('http://doi.org/', '')

    # Basic format validation (10.xxxx/yyyy pattern)
    if not doi.startswith('10.'):
        return False

    # Try to resolve DOI
    try:
        response = requests.head(f'https://doi.org/{doi}', timeout=5, allow_redirects=True)
        return response.status_code == 200
    except:
        return False


def resolve_doi(doi: str) -> Dict:
    """
    Resolve DOI to full metadata using doi.org API.

    Args:
        doi: DOI string

    Returns:
        Metadata dictionary or None if resolution fails
    """
    if not doi:
        return None

    # Clean DOI
    doi = doi.replace('https://doi.org/', '').replace('http://doi.org/', '')

    try:
        # Use content negotiation to get JSON metadata
        headers = {'Accept': 'application/vnd.citationstyles.csl+json'}
        response = requests.get(f'https://doi.org/{doi}', headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            # Extract relevant fields
            return {
                'title': data.get('title', ''),
                'authors': [f"{a.get('given', '')} {a.get('family', '')}".strip()
                           for a in data.get('author', [])],
                'journal': data.get('container-title', ''),
                'year': str(data.get('published-print', {}).get('date-parts', [['']])[0][0] or
                          data.get('published-online', {}).get('date-parts', [['']])[0][0] or ''),
                'doi': doi,
                'abstract': data.get('abstract', '')
            }
    except:
        pass

    return None


def find_missing_doi(article: Dict) -> str:
    """
    Attempt to find DOI for article without one.
    Uses title + authors to search CrossRef.

    Args:
        article: Article dictionary

    Returns:
        DOI string or empty string
    """
    title = article.get('title', '')
    if not title:
        return ''

    try:
        # Search CrossRef by title
        params = {
            'query.title': title,
            'rows': 1
        }
        response = requests.get('https://api.crossref.org/works', params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            items = data.get('message', {}).get('items', [])
            if items:
                # Check if title matches closely
                found_title = ' '.join(items[0].get('title', []))
                if found_title.lower().strip() == title.lower().strip():
                    return items[0].get('DOI', '')
    except:
        pass

    return ''


def enrich_from_crossref(article: Dict) -> Dict:
    """
    Enrich article metadata using CrossRef API.
    Looks up by DOI if available, otherwise by title.

    Args:
        article: Article dictionary

    Returns:
        Enriched article dictionary
    """
    enriched = article.copy()

    # Try DOI lookup first
    doi = article.get('doi', '').strip()
    if doi:
        metadata = resolve_doi(doi)
        if metadata:
            # Fill missing fields
            for key, value in metadata.items():
                if value and not enriched.get(key):
                    enriched[key] = value
            return enriched

    # Try title lookup
    title = article.get('title', '')
    if title:
        doi = find_missing_doi(article)
        if doi:
            enriched['doi'] = doi
            # Resolve the found DOI
            metadata = resolve_doi(doi)
            if metadata:
                for key, value in metadata.items():
                    if value and not enriched.get(key):
                        enriched[key] = value

    return enriched


def enrich_from_pubmed(article: Dict) -> Dict:
    """
    Enrich article metadata using PubMed API.
    Looks up by PMID/DOI or title.

    Args:
        article: Article dictionary

    Returns:
        Enriched article dictionary
    """
    enriched = article.copy()

    # Try to use existing PubMed source module
    try:
        from lixplore.sources import pubmed

        # Search by title
        title = article.get('title', '')
        if title:
            results = pubmed.search(title, max_results=1)
            if results and len(results) > 0:
                match = results[0]
                # Fill missing fields
                for key in ['authors', 'abstract', 'journal', 'year', 'doi']:
                    if match.get(key) and not enriched.get(key):
                        enriched[key] = match[key]
    except:
        pass

    return enriched


def enrich_from_arxiv(article: Dict) -> Dict:
    """
    Enrich article metadata using arXiv API.
    Looks up by arXiv ID or title.

    Args:
        article: Article dictionary

    Returns:
        Enriched article dictionary
    """
    enriched = article.copy()

    # Try to use existing arXiv source module
    try:
        from lixplore.sources import arxiv

        # Search by title
        title = article.get('title', '')
        if title:
            results = arxiv.search(title, max_results=1)
            if results and len(results) > 0:
                match = results[0]
                # Fill missing fields
                for key in ['authors', 'abstract', 'journal', 'year']:
                    if match.get(key) and not enriched.get(key):
                        enriched[key] = match[key]
    except:
        pass

    return enriched


def enrich_article(article: Dict, apis: List[str] = None) -> Dict:
    """
    Enrich single article using specified APIs.

    Args:
        article: Article dictionary
        apis: List of APIs to use ('crossref', 'pubmed', 'arxiv', 'all')

    Returns:
        Enriched article dictionary
    """
    if not apis or 'all' in apis:
        apis = ['crossref', 'pubmed', 'arxiv']

    enriched = article.copy()

    # Try each API in order
    for api in apis:
        if api == 'crossref':
            enriched = enrich_from_crossref(enriched)
        elif api == 'pubmed':
            enriched = enrich_from_pubmed(enriched)
        elif api == 'arxiv':
            enriched = enrich_from_arxiv(enriched)

        # Rate limiting
        time.sleep(RATE_LIMIT_DELAY)

    return enriched


def enrich_results(results: List[Dict], apis: List[str] = None, show_progress: bool = True) -> List[Dict]:
    """
    Enrich multiple articles with metadata.

    Args:
        results: List of article dictionaries
        apis: APIs to use for enrichment (default: all available)
        show_progress: Show progress indicator

    Returns:
        List of enriched articles
    """
    if not results:
        return []

    if not apis:
        apis = ['all']

    if show_progress:
        print(f"Enriching {len(results)} article(s) using: {', '.join(apis)}")

    enriched_results = []
    for i, article in enumerate(results, 1):
        if show_progress and i % 5 == 0:
            print(f"  Progress: {i}/{len(results)} articles enriched...")

        enriched = enrich_article(article, apis)
        enriched_results.append(enriched)

    if show_progress:
        print(f"✓ Enrichment complete: {len(enriched_results)} articles")

    return enriched_results


def resolve_all_dois(results: List[Dict]) -> List[Dict]:
    """
    Validate existing DOIs and find missing ones.

    Args:
        results: List of article dictionaries

    Returns:
        List with resolved/validated DOIs
    """
    print(f"Resolving DOIs for {len(results)} article(s)...")

    resolved_results = []
    found_count = 0
    validated_count = 0

    for i, article in enumerate(results, 1):
        result = article.copy()
        doi = article.get('doi', '').strip()

        if doi:
            # Validate existing DOI
            if validate_doi(doi):
                validated_count += 1
            else:
                # Try to resolve anyway
                metadata = resolve_doi(doi)
                if metadata:
                    validated_count += 1
        else:
            # Try to find missing DOI
            doi = find_missing_doi(article)
            if doi:
                result['doi'] = doi
                found_count += 1

        resolved_results.append(result)

        # Rate limiting
        time.sleep(RATE_LIMIT_DELAY)

    print(f"✓ DOI resolution complete:")
    print(f"  - Validated: {validated_count} existing DOIs")
    print(f"  - Found: {found_count} missing DOIs")

    return resolved_results
