from lixplore.sources.pubmed import PubMedSource

if __name__ == "__main__":
    source = PubMedSource()
    results = source.search("pharmacovigilance", max_results=5)
    for r in results:
        print(r)

