#!/usr/bin/env python3

"""
arXiv API connector for Lixplore CLI
API Documentation: https://arxiv.org/help/api/user-manual
No authentication required
"""

from typing import List, Dict
import requests
import xml.etree.ElementTree as ET


class ArxivSource:
    """
    arXiv search source for preprints and scientific papers
    """

    def __init__(self):
        self.base_url = "http://export.arxiv.org/api/query"

    def search(self, query: str, max_results: int = 10) -> List[Dict]:
        results = []
        try:
            params = {
                "search_query": f"all:{query}",
                "start": 0,
                "max_results": max_results
            }

            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()

            # Parse XML response
            root = ET.fromstring(response.content)

            # Define namespace
            ns = {
                'atom': 'http://www.w3.org/2005/Atom',
                'arxiv': 'http://arxiv.org/schemas/atom'
            }

            entries = root.findall('atom:entry', ns)

            for entry in entries:
                article_data = self.parse_article(entry, ns)
                results.append(article_data)

        except requests.exceptions.RequestException as e:
            print(f"[arXiv Error] {e}")
        except Exception as e:
            print(f"[arXiv Error] {e}")

        return results

    def parse_article(self, entry, ns: Dict) -> Dict:
        # Title
        title_elem = entry.find('atom:title', ns)
        title = title_elem.text.strip().replace('\n', ' ') if title_elem is not None else ""

        # Authors
        authors_list = []
        for author in entry.findall('atom:author', ns):
            name_elem = author.find('atom:name', ns)
            if name_elem is not None:
                authors_list.append(name_elem.text.strip())

        # Abstract
        summary_elem = entry.find('atom:summary', ns)
        abstract = summary_elem.text.strip().replace('\n', ' ') if summary_elem is not None else ""

        # Journal (arXiv category)
        category_elem = entry.find('arxiv:primary_category', ns)
        journal = ""
        if category_elem is not None:
            journal = f"arXiv:{category_elem.get('term', '')}"

        # Year
        published_elem = entry.find('atom:published', ns)
        year = ""
        if published_elem is not None:
            year = published_elem.text[:4]  # Extract year from ISO date

        # DOI
        doi_elem = entry.find('arxiv:doi', ns)
        doi = doi_elem.text.strip() if doi_elem is not None else ""

        # URL
        url = ""
        id_elem = entry.find('atom:id', ns)
        if id_elem is not None:
            url = id_elem.text.strip()

        return {
            "title": title,
            "authors": authors_list,
            "abstract": abstract,
            "journal": journal,
            "year": year,
            "doi": doi,
            "url": url,
            "source": "arxiv"
        }


# Wrapper function for dispatcher
def search(query: str, max_results: int = 10) -> List[Dict]:
    return ArxivSource().search(query, max_results)
