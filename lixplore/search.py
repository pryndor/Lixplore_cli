#!/usr/bin/env
# search.py

from .sources.pubmed import PubMedSource
#from lixplore.sources import springer
#from lixplore.sources import crossref
#from lixplore.sources import doaj
#from lixplore.sources import europepmc

#def search_crossref(query, args):
 #   return [
  #      {"title": "Example Crossref Result", "doi": "10.1234/example.doi", "year": 2023}
   # ]

def search_pubmed(query, args=None):
    """
    Search PubMed using PubMedSource class
    :param query: Search string
    :param args: Optional arguments (like max_results)
    :return: List of dicts with article info
    """
    max_results = 10  # default
    if args and "max_results" in args:
        max_results = args["max_results"]

    # Create an instance of PubMedSource
    pubmed = PubMedSource()

    # Perform the search
    results = pubmed.search(query=query, max_results=max_results)

    return results

