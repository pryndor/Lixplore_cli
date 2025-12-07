#!/usr/bin/env python3

"""
Europe PMC API connector for Lixplore CLI
API Documentation: https://europepmc.org/RestfulWebService
No authentication required
"""

from typing import List, Dict
import requests


class EuropePMCSource:
    """
    Europe PMC search source for life sciences literature
    """

    def __init__(self):
        self.base_url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"

    def search(self, query: str, max_results: int = 10) -> List[Dict]:
        results = []
        try:
            params = {
                "query": query,
                "pageSize": max_results,
                "format": "json"
            }

            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            items = data.get("resultList", {}).get("result", [])

            for item in items:
                article_data = self.parse_article(item)
                results.append(article_data)

        except requests.exceptions.RequestException as e:
            print(f"[EuropePMC Error] {e}")
        except Exception as e:
            print(f"[EuropePMC Error] {e}")

        return results

    def parse_article(self, item: Dict) -> Dict:
        # Title
        title = item.get("title", "")

        # Authors
        authors_list = []
        author_string = item.get("authorString", "")
        if author_string:
            # Europe PMC provides authors as a comma-separated string
            authors_list = [a.strip() for a in author_string.split(",")]

        # Abstract
        abstract = item.get("abstract", "")

        # Journal
        journal = item.get("journalTitle", "")

        # Year
        year = str(item.get("pubYear", ""))

        # DOI
        doi = item.get("doi", "")

        # URL
        url = ""
        pmid = item.get("pmid", "")
        pmcid = item.get("pmcid", "")

        if pmcid:
            url = f"https://europepmc.org/article/PMC/{pmcid}"
        elif pmid:
            url = f"https://europepmc.org/article/MED/{pmid}"
        elif doi:
            url = f"https://doi.org/{doi}"

        return {
            "title": title,
            "authors": authors_list,
            "abstract": abstract,
            "journal": journal,
            "year": year,
            "doi": doi,
            "url": url,
            "source": "europepmc"
        }


# Wrapper function for dispatcher
def search(query: str, max_results: int = 10) -> List[Dict]:
    return EuropePMCSource().search(query, max_results)
