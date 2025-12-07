from lixplore.sources.pubmed import PubMedSource
import json


# Initialize PubMed source
pubmed = PubMedSource(email="balathepharmacist@gmail.com")

# Run a query
results = pubmed.search("diabetes", max_results=20)

# Save to file
with open("results.json", "w") as f:
    json.dump(results, f, indent=2)

print("Saved", len(results), "results to results.json")

