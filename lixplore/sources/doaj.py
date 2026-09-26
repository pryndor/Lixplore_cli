#!/usr/bin/env python3

"""
DOAJ (Directory of Open Access Journals) API connector for Lixplore CLI
API Documentation: https://doaj.org/api/docs
No authentication required
"""

from typing import List, Dict, Optional
from datetime import date
import requests


class DOAJSource:
    """
    DOAJ search source for open access literature
    """

    def __init__(self):
        self.base_url = "https://doaj.org/api/v3/search/articles"

    def search(self, query: str, max_results: int = 10, since: Optional[date] = None) -> List[Dict]:
        results = []
        try:
            # DOAJ API v3 - query is part of the URL path
            url = f"{self.base_url}/{query}"
            params = {
                "pageSize": max_results,
                "page": 1
            }
            if since:
                # DOAJ rejects range queries, so sort newest-first and cut below
                params["sort"] = "created_date:desc"

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            items = data.get("results", [])

            for item in items:
                if since and item.get("created_date", "")[:10] < since.isoformat():
                    break
                article_data = self.parse_article(item)
                results.append(article_data)

        except requests.exceptions.RequestException as e:
            print(f"[DOAJ Error] {e}")
        except Exception as e:
            print(f"[DOAJ Error] {e}")

        return results

    def parse_article(self, item: Dict) -> Dict:
        bibjson = item.get("bibjson", {})

        # Title
        title = bibjson.get("title", "")

        # Authors
        authors_list = []
        if "author" in bibjson:
            for author in bibjson["author"]:
                name = author.get("name", "")
                if name:
                    authors_list.append(name)

        # Abstract
        abstract = bibjson.get("abstract", "")

        # Journal
        journal = bibjson.get("journal", {}).get("title", "")

        # Year
        year = ""
        if "year" in bibjson:
            year = str(bibjson["year"])
        elif "month" in bibjson:
            year = bibjson.get("month", "").split("-")[0] if "-" in bibjson.get("month", "") else ""

        # DOI
        doi = ""
        identifiers = bibjson.get("identifier", [])
        for ident in identifiers:
            if ident.get("type") == "doi":
                doi = ident.get("id", "")
                break

        # URL
        url = ""
        links = bibjson.get("link", [])
        for link in links:
            if link.get("type") == "fulltext":
                url = link.get("url", "")
                break

        if not url and doi:
            url = f"https://doi.org/{doi}"

        return {
            "title": title,
            "authors": authors_list,
            "abstract": abstract,
            "journal": journal,
            "year": year,
            "doi": doi,
            "url": url,
            "source": "doaj"
        }


# Wrapper function for dispatcher
def search(query: str, max_results: int = 10, since: Optional[date] = None) -> List[Dict]:
    return DOAJSource().search(query, max_results, since)
