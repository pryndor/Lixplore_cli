#!/usr/bin/env python3
"""
PDF Download Integration

Downloads full-text PDFs from various sources:
- PubMed Central (PMC) - Open access
- arXiv - Preprint repository
- DOI resolution - Publisher websites
- SciHub - Optional, user-configured

Respects copyright and prioritizes legal open-access sources.
"""

import os
import requests
import re
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote


# PDF download directory
PDF_DIR = os.path.expanduser("~/Lixplore_PDFs")

# SciHub mirrors (user can configure)
SCIHUB_CONFIG = os.path.expanduser("~/.lixplore/scihub_mirror.txt")


def ensure_pdf_directory():
    """Create PDF download directory if it doesn't exist."""
    if not os.path.exists(PDF_DIR):
        os.makedirs(PDF_DIR, exist_ok=True)


def get_scihub_mirror() -> Optional[str]:
    """
    Get configured SciHub mirror.

    Returns:
        SciHub mirror URL or None if not configured
    """
    if os.path.exists(SCIHUB_CONFIG):
        try:
            with open(SCIHUB_CONFIG, 'r') as f:
                mirror = f.read().strip()
                if mirror:
                    return mirror
        except:
            pass
    return None


def set_scihub_mirror(mirror_url: str):
    """
    Configure SciHub mirror.

    Args:
        mirror_url: SciHub mirror URL (e.g., https://sci-hub.se)
    """
    os.makedirs(os.path.dirname(SCIHUB_CONFIG), exist_ok=True)
    with open(SCIHUB_CONFIG, 'w') as f:
        f.write(mirror_url.strip())
    print(f"SciHub mirror configured: {mirror_url}")


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for filesystem.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Limit length
    filename = filename[:200]
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    return filename if filename else "article"


def download_pdf_from_url(url: str, output_path: str, timeout: int = 30) -> bool:
    """
    Download PDF from URL.

    Args:
        url: PDF URL
        output_path: Output file path
        timeout: Request timeout in seconds

    Returns:
        True if successful, False otherwise
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout, stream=True)
        response.raise_for_status()

        # Check if response is actually a PDF
        content_type = response.headers.get('content-type', '').lower()
        if 'pdf' not in content_type and 'application/octet-stream' not in content_type:
            # Check first few bytes for PDF signature
            first_bytes = response.content[:4]
            if first_bytes != b'%PDF':
                return False

        # Download file
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return True

    except Exception as e:
        # Clean up partial download
        if os.path.exists(output_path):
            os.remove(output_path)
        return False


def try_pmc_download(article: Dict, output_dir: str) -> Optional[str]:
    """
    Try downloading from PubMed Central (open access).

    Args:
        article: Article dictionary
        output_dir: Output directory

    Returns:
        Downloaded file path or None
    """
    # Check if article has PMC ID
    pmc_id = None

    # Try to find PMC ID in URL
    url = article.get('url', '')
    if 'pmc' in url.lower():
        match = re.search(r'PMC(\d+)', url, re.IGNORECASE)
        if match:
            pmc_id = match.group(1)

    if not pmc_id:
        return None

    # Try PMC OA service
    pdf_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmc_id}/pdf/"

    title = article.get('title', 'article')
    filename = sanitize_filename(f"{title[:100]}.pdf")
    output_path = os.path.join(output_dir, filename)

    if download_pdf_from_url(pdf_url, output_path):
        return output_path

    return None


def try_arxiv_download(article: Dict, output_dir: str) -> Optional[str]:
    """
    Try downloading from arXiv.

    Args:
        article: Article dictionary
        output_dir: Output directory

    Returns:
        Downloaded file path or None
    """
    # Check if article is from arXiv
    if article.get('source', '').lower() != 'arxiv':
        return None

    url = article.get('url', '')
    if not url or 'arxiv' not in url.lower():
        return None

    # Extract arXiv ID
    match = re.search(r'(\d{4}\.\d{4,5})', url)
    if not match:
        return None

    arxiv_id = match.group(1)
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

    title = article.get('title', 'article')
    filename = sanitize_filename(f"{title[:100]}.pdf")
    output_path = os.path.join(output_dir, filename)

    if download_pdf_from_url(pdf_url, output_path):
        return output_path

    return None


def try_doi_resolution(article: Dict, output_dir: str) -> Optional[str]:
    """
    Try resolving DOI to find PDF link.

    Args:
        article: Article dictionary
        output_dir: Output directory

    Returns:
        Downloaded file path or None
    """
    doi = article.get('doi')
    if not doi:
        return None

    # Try common open-access patterns
    # Unpaywall API (open access)
    try:
        email = "lixplore@example.com"  # Replace with actual email for API
        unpaywall_url = f"https://api.unpaywall.org/v2/{doi}?email={email}"

        response = requests.get(unpaywall_url, timeout=10)
        if response.status_code == 200:
            data = response.json()

            # Check for open access PDF
            if data.get('is_oa'):
                best_oa_location = data.get('best_oa_location')
                if best_oa_location:
                    pdf_url = best_oa_location.get('url_for_pdf')
                    if pdf_url:
                        title = article.get('title', 'article')
                        filename = sanitize_filename(f"{title[:100]}.pdf")
                        output_path = os.path.join(output_dir, filename)

                        if download_pdf_from_url(pdf_url, output_path):
                            return output_path
    except:
        pass

    return None


def try_scihub_download(article: Dict, output_dir: str) -> Optional[str]:
    """
    Try downloading from SciHub (if configured by user).

    Note: SciHub access may violate publisher ToS. User discretion advised.

    Args:
        article: Article dictionary
        output_dir: Output directory

    Returns:
        Downloaded file path or None
    """
    scihub_mirror = get_scihub_mirror()
    if not scihub_mirror:
        return None

    doi = article.get('doi')
    if not doi:
        return None

    try:
        # Construct SciHub URL
        scihub_url = f"{scihub_mirror}/{doi}"

        # Get SciHub page
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        }
        response = requests.get(scihub_url, headers=headers, timeout=15)
        response.raise_for_status()

        # Find PDF link in page
        # SciHub typically embeds PDF or provides download button
        pdf_match = re.search(r'(https?://[^"\']+\.pdf[^"\']*)', response.text)
        if pdf_match:
            pdf_url = pdf_match.group(1)

            title = article.get('title', 'article')
            filename = sanitize_filename(f"{title[:100]}.pdf")
            output_path = os.path.join(output_dir, filename)

            if download_pdf_from_url(pdf_url, output_path):
                return output_path

    except:
        pass

    return None


def download_article_pdf(article: Dict, use_scihub: bool = False) -> Tuple[bool, str]:
    """
    Download PDF for an article, trying multiple sources.

    Priority order:
    1. PubMed Central (open access)
    2. arXiv (preprints)
    3. DOI resolution (Unpaywall)
    4. SciHub (if enabled and configured)

    Args:
        article: Article dictionary
        use_scihub: Whether to try SciHub as fallback

    Returns:
        Tuple of (success: bool, message: str)
    """
    ensure_pdf_directory()

    title = article.get('title', 'Unknown')
    source = article.get('source', 'Unknown')

    # Create source-specific subdirectory
    source_dir = os.path.join(PDF_DIR, sanitize_filename(source))
    os.makedirs(source_dir, exist_ok=True)

    # Try PMC first (for PubMed articles)
    if source.lower() == 'pubmed':
        result = try_pmc_download(article, source_dir)
        if result:
            return True, f"Downloaded from PMC: {result}"

    # Try arXiv
    result = try_arxiv_download(article, source_dir)
    if result:
        return True, f"Downloaded from arXiv: {result}"

    # Try DOI resolution / Unpaywall
    result = try_doi_resolution(article, source_dir)
    if result:
        return True, f"Downloaded (open access): {result}"

    # Try SciHub as last resort (if enabled)
    if use_scihub:
        result = try_scihub_download(article, source_dir)
        if result:
            return True, f"Downloaded via SciHub: {result}"

    return False, f"✗ PDF not available: {title[:60]}..."


def download_multiple_pdfs(articles: List[Dict], article_numbers: List[int] = None,
                          use_scihub: bool = False) -> Dict[str, any]:
    """
    Download PDFs for multiple articles.

    Args:
        articles: List of article dictionaries
        article_numbers: Optional list of specific article numbers to download (1-indexed)
        use_scihub: Whether to try SciHub as fallback

    Returns:
        Dictionary with download statistics
    """
    # Determine which articles to download
    if article_numbers:
        to_download = []
        for num in article_numbers:
            if 1 <= num <= len(articles):
                to_download.append(articles[num - 1])
            else:
                print(f"Warning: Article #{num} is out of range")
    else:
        to_download = articles

    if not to_download:
        return {'success': 0, 'failed': 0, 'total': 0}

    print(f"\n📥 Downloading {len(to_download)} PDF(s)...")
    if use_scihub:
        scihub_mirror = get_scihub_mirror()
        if scihub_mirror:
            print(f"   Using SciHub mirror: {scihub_mirror}")
        else:
            print(f"   SciHub not configured, will skip SciHub downloads")
            print(f"   Configure with: lixplore --set-scihub-mirror <url>")

    print("")

    success_count = 0
    failed_count = 0

    for i, article in enumerate(to_download, 1):
        print(f"[{i}/{len(to_download)}] ", end="", flush=True)
        success, message = download_article_pdf(article, use_scihub)

        if success:
            print(message)
            success_count += 1
        else:
            print(message)
            failed_count += 1

    print(f"\nDownload Summary: {success_count} successful, {failed_count} failed")
    print(f"PDFs saved to: {PDF_DIR}")

    return {
        'success': success_count,
        'failed': failed_count,
        'total': len(to_download)
    }


def get_pdf_link(article: Dict) -> Optional[str]:
    """
    Get PDF link for an article without downloading.
    Tries multiple sources in priority order:
    1. PMC (PubMed Central)
    2. arXiv
    3. Unpaywall (open access)

    Args:
        article: Article dictionary with metadata

    Returns:
        PDF URL if available, None otherwise
    """
    # Try PMC first
    pmcid = article.get('pmcid') or article.get('pmc')
    if pmcid:
        pmcid = pmcid.replace('PMC', '')
        pmc_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmcid}/pdf/"
        return pmc_url

    # Try arXiv
    arxiv_id = article.get('arxiv_id')
    if not arxiv_id:
        # Try to extract from URL (e.g., http://arxiv.org/abs/2306.04338v1)
        url = article.get('url', '')
        if 'arxiv.org' in url:
            match = re.search(r'arxiv\.org/abs/([0-9]+\.[0-9]+(?:v[0-9]+)?)', url)
            if match:
                arxiv_id = match.group(1)

    if arxiv_id:
        # Remove version suffix for PDF URL (e.g., 2306.04338v1 -> 2306.04338)
        arxiv_id_clean = re.sub(r'v\d+$', '', arxiv_id)
        return f"https://arxiv.org/pdf/{arxiv_id_clean}.pdf"

    # Try Unpaywall (DOI-based)
    doi = article.get('doi')
    if doi:
        try:
            email = "lixplore@example.com"
            unpaywall_url = f"https://api.unpaywall.org/v2/{doi}?email={email}"

            response = requests.get(unpaywall_url, timeout=5)
            if response.status_code == 200:
                data = response.json()

                # Check for open access PDF
                if data.get('is_oa'):
                    best_oa_location = data.get('best_oa_location')
                    if best_oa_location:
                        pdf_url = best_oa_location.get('url_for_pdf')
                        if pdf_url:
                            return pdf_url
        except:
            pass

    return None


def get_pdf_links_batch(articles: List[Dict]) -> Dict[int, str]:
    """
    Get PDF links for multiple articles efficiently.

    Args:
        articles: List of article dictionaries

    Returns:
        Dictionary mapping article index to PDF URL
    """
    pdf_links = {}

    for i, article in enumerate(articles):
        pdf_url = get_pdf_link(article)
        if pdf_url:
            pdf_links[i] = pdf_url

    return pdf_links


if __name__ == "__main__":
    # Test PDF downloader
    test_article = {
        'title': 'Test Article',
        'doi': '10.1038/nature12345',
        'source': 'PubMed'
    }

    success, msg = download_article_pdf(test_article, use_scihub=False)
    print(msg)
