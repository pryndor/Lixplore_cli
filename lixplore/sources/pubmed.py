#!/usr/bin/env python3

"""
PubMed search source using NCBI Entrez API
"""

from typing import List, Dict, Optional
from datetime import date

# Total matches the API reported for the last date-bounded search (alerts use
# it to say how many papers were published, beyond the ones fetched)
last_total: Optional[int] = None
from Bio import Entrez
import os
import json
import time

# Load configuration
def _load_config():
    """Load email from config.json, fallback to environment or default.

    Looks in config.json of a source checkout first, then in
    ~/.lixplore/config.json (works for pip, AUR and Homebrew installs):
        {"pubmed": {"email": "you@example.org", "api_key": "..."}}
    """
    config_paths = [
        os.path.join(os.path.dirname(__file__), "..", "..", "config.json"),
        os.path.join(os.path.expanduser("~"), ".lixplore", "config.json"),
    ]
    for config_path in config_paths:
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            email = config.get("pubmed", {}).get("email", "")
            api_key = config.get("pubmed", {}).get("api_key", "")
            if email and email != "your_email@example.com":
                return email, api_key
        except (OSError, ValueError, AttributeError):
            pass

    # Fallback to environment variable or default
    email = os.environ.get("PUBMED_EMAIL", "user@example.com")
    api_key = os.environ.get("PUBMED_API_KEY", "")
    return email, api_key

# Configure Entrez
_email, _api_key = _load_config()
Entrez.email = _email
Entrez.tool = "lixplore"
if _api_key:
    Entrez.api_key = _api_key

# NCBI sometimes answers HTTP 200 with an error inside the XML while its search
# backend is down ("Search Backend failed ... Cannot connect to SOLR").
# Biopython retries HTTP 5xx itself but not these, so retry them here.
_TRANSIENT = ("temporarily unavailable", "search backend failed", "solr", "try again later")
_RETRY_DELAYS = (3, 8)


def _is_transient(error: Exception) -> bool:
    return any(t in str(error).lower() for t in _TRANSIENT)


def _entrez(call, **params):
    """Run an Entrez call and parse it, retrying NCBI's temporary errors."""
    for delay in _RETRY_DELAYS + (None,):
        try:
            handle = call(**params)
            try:
                return Entrez.read(handle)
            finally:
                handle.close()
        except RuntimeError as e:
            if delay is None or not _is_transient(e):
                raise
            time.sleep(delay)


class PubMedSource:
    """
    PubMed search source for Lixplore CLI
    """

   # def __init__(self, email: str = None, api_key: str = None):
    #    # Configure Entrez
     #   Entrez.email = email or "your_email@example.com"
      #  if api_key:
       #     Entrez.api_key = api_key

    def search(self, query: str, max_results: int = 10, since: Optional[date] = None) -> List[Dict]:
        global last_total
        last_total = None
        results = []
        try:
            # Step 1: Search IDs
            params = {"db": "pubmed", "term": query, "retmax": max_results}
            if since:
                # Entrez date = when the record was added to PubMed
                params.update(datetype="edat", mindate=since.strftime("%Y/%m/%d"),
                              maxdate=date.today().strftime("%Y/%m/%d"), sort="pub_date")
            record = _entrez(Entrez.esearch, **params)
            id_list = record.get("IdList", [])
            if since:
                last_total = int(record.get("Count", 0))

            # Step 2: Fetch details
            if id_list:
                records = _entrez(Entrez.efetch, db="pubmed", id=",".join(id_list), retmode="xml")

                for article in records["PubmedArticle"]:
                    article_data = self.parse_article(article)
                    results.append(article_data)

        except Exception as e:
            if _is_transient(e):
                print("[PubMed Error] PubMed (NCBI) is temporarily unavailable; "
                      f"please try again in a few minutes. NCBI said: {e}")
            else:
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
        # Some records only have a free-text date such as "2001 May 1-15"
        year = pub_date.get("Year", "") or str(pub_date.get("MedlineDate", ""))[:4]

        # DOI
        doi = ""
        if "ELocationID" in article_info:
            for eid in article_info["ELocationID"]:
                if eid.attributes.get("EIdType") == "doi":
                    doi = str(eid)
        if not doi:
            # Older records carry the DOI only in the PubmedData ID list
            for aid in article.get("PubmedData", {}).get("ArticleIdList", []):
                if aid.attributes.get("IdType") == "doi":
                    doi = str(aid)
                    break

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
def search(query: str, max_results: int = 10, since: Optional[date] = None) -> List[Dict]:
    return PubMedSource().search(query, max_results, since)

