#!/usr/bin/env python3

"""
PubMed search source using NCBI Entrez API
"""

from typing import List, Dict
from Bio import Entrez
import os
import json

# Load configuration
def _load_config():
    """Load email from config.json, fallback to environment or default"""
    config_path = os.path.join(os.path.dirname(__file__), "..", "..", "config.json")
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            email = config.get("pubmed", {}).get("email", "")
            api_key = config.get("pubmed", {}).get("api_key", "")
            if email and email != "your_email@example.com":
                return email, api_key
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    # Fallback to environment variable or default
    email = os.environ.get("PUBMED_EMAIL", "user@example.com")
    api_key = os.environ.get("PUBMED_API_KEY", "")
    return email, api_key

# Configure Entrez
_email, _api_key = _load_config()
Entrez.email = _email
if _api_key:
    Entrez.api_key = _api_key


class PubMedSource:
    """
    PubMed search source for Lixplore CLI
    """

   # def __init__(self, email: str = None, api_key: str = None):
    #    # Configure Entrez
     #   Entrez.email = email or "your_email@example.com"
      #  if api_key:
       #     Entrez.api_key = api_key

    def search(self, query: str, max_results: int = 10) -> List[Dict]:
        results = []
        try:
            # Step 1: Search IDs
            handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
            record = Entrez.read(handle)
            handle.close()
            id_list = record.get("IdList", [])

            # Step 2: Fetch details
            if id_list:
                handle = Entrez.efetch(db="pubmed", id=",".join(id_list), retmode="xml")
                records = Entrez.read(handle)
                handle.close()

                for article in records["PubmedArticle"]:
                    article_data = self.parse_article(article)
                    results.append(article_data)

        except Exception as e:
            print(f"[PubMed Error] {e}")

        return results

    def parse_article(self, article) -> Dict:
        medline = article["MedlineCitation"]
        article_info = medline["Article"]

        # Title
        title = article_info.get("ArticleTitle", "")

        # Authors
        authors_list = []
        if "AuthorList" in article_info:
            for author in article_info["AuthorList"]:
                name_parts = []
                if "LastName" in author:
                    name_parts.append(author["LastName"])
                if "ForeName" in author:
                    name_parts.append(author["ForeName"])
                if name_parts:
                    authors_list.append(" ".join(name_parts))

        # Abstract
        abstract = ""
        if "Abstract" in article_info and "AbstractText" in article_info["Abstract"]:
            if isinstance(article_info["Abstract"]["AbstractText"], list):
                abstract = " ".join(article_info["Abstract"]["AbstractText"])
            else:
                abstract = article_info["Abstract"]["AbstractText"]

        # Journal & Year
        journal = article_info.get("Journal", {}).get("Title", "")
        pub_date = article_info.get("Journal", {}).get("JournalIssue", {}).get("PubDate", {})
        year = pub_date.get("Year", "")

        # DOI
        doi = ""
        if "ELocationID" in article_info:
            for eid in article_info["ELocationID"]:
                if eid.attributes.get("EIdType") == "doi":
                    doi = str(eid)

        # PubMed URL
        pmid = medline.get("PMID", "")
        url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else ""

        return {
            "title": title,
            "authors": authors_list,
            "abstract": abstract,
            "journal": journal,
            "year": year,
            "doi": doi,
            "url": url,
            "source": "pubmed"
        }


# 🔑 Wrapper so dispatcher can call pubmed.search()
def search(query: str, max_results: int = 10) -> List[Dict]:
    return PubMedSource().search(query, max_results)

