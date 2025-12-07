#!/usr/bin/env python3

"""
Crossref API connector for Lixplore CLI
API Documentation: https://api.crossref.org/swagger-ui/index.html
No authentication required
"""

from typing import List, Dict
import requests


class CrossrefSource:
    """
    Crossref search source for literature
    """

    def __init__(self):
        self.base_url = "https://api.crossref.org/works"

    def search(self, query: str, max_results: int = 10) -> List[Dict]:
        results = []
        try:
            params = {
                "query": query,
                "rows": max_results,
                "select": "DOI,title,author,abstract,container-title,published,URL"
            }

            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            items = data.get("message", {}).get("items", [])

            for item in items:
                article_data = self.parse_article(item)
                results.append(article_data)

        except requests.exceptions.RequestException as e:
            print(f"[Crossref Error] {e}")
        except Exception as e:
            print(f"[Crossref Error] {e}")

        return results

    def parse_article(self, item: Dict) -> Dict:
        # Title
        title = ""
        if "title" in item and item["title"]:
            title = item["title"][0] if isinstance(item["title"], list) else item["title"]

        # Authors
        authors_list = []
        if "author" in item:
            for author in item["author"]:
                name_parts = []
                if "given" in author:
                    name_parts.append(author["given"])
                if "family" in author:
                    name_parts.append(author["family"])
                if name_parts:
                    authors_list.append(" ".join(name_parts))

        # Abstract
        abstract = item.get("abstract", "")

        # Journal
        journal = ""
        if "container-title" in item and item["container-title"]:
            journal = item["container-title"][0] if isinstance(item["container-title"], list) else item["container-title"]

        # Year
        year = ""
        if "published" in item:
            pub_date = item["published"]
            if "date-parts" in pub_date and pub_date["date-parts"]:
                year = str(pub_date["date-parts"][0][0]) if pub_date["date-parts"][0] else ""

        # DOI
        doi = item.get("DOI", "")

        # URL
        url = item.get("URL", "")
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
            "source": "crossref"
        }


# Wrapper function for dispatcher
def search(query: str, max_results: int = 10) -> List[Dict]:
    return CrossrefSource().search(query, max_results)
