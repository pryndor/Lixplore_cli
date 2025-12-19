# lixplore

> Academic literature search and export tool for multiple databases (PubMed, Crossref, DOAJ, EuropePMC, arXiv).
> Export results in various formats (CSV, Excel, JSON, BibTeX, RIS, EndNote, XML).
> More information: <https://github.com/yourusername/lixplore>.

- Search PubMed for a query:

`lixplore -P -q "{{cancer treatment}}" -m {{10}}`

- Search multiple sources (PubMed + arXiv):

`lixplore -s PX -q "{{machine learning}}" -m {{20}}`

- Search all sources with deduplication:

`lixplore -A -q "{{COVID-19}}" -m {{50}} -D`

- Search and export to Excel:

`lixplore -P -q "{{diabetes}}" -m {{15}} -X xlsx -o {{results.xlsx}}`

- Search with date filter and show abstracts:

`lixplore -P -q "{{neuroscience}}" -d {{2020-01-01}} {{2024-12-31}} -m {{10}} -a`

- Search by author:

`lixplore -P -au "{{Smith J}}" -m {{10}} -a`

- Export to EndNote Tagged format:

`lixplore -P -q "{{quantum physics}}" -m {{20}} -X enw -o {{physics_papers.enw}}`

- Search by DOI:

`lixplore -DOI "{{10.1038/nature12345}}"`

- Boolean AND operator (both terms required):

`lixplore -P -q "{{cancer AND treatment}}" -m {{10}}`

- Boolean OR operator (either term):

`lixplore -P -q "{{cancer OR tumor}}" -m {{10}}`

- Boolean NOT operator (exclude term):

`lixplore -P -q "{{diabetes NOT type1}}" -m {{10}}`

- Complex boolean query with parentheses:

`lixplore -P -q "{{(cancer OR tumor) AND treatment}}" -m {{20}}`

- Review article in separate terminal (two-step workflow):

`lixplore -P -q "{{paracetamol}}" -m {{10}} && lixplore -R {{2}}`

- Review multiple articles from cached results:

`lixplore -R {{1 5 9}}`

- Search and review in one command:

`lixplore -P -q "{{diabetes}}" -m {{10}} -R {{1 3 5}}`

- Export odd-numbered articles (smart selection):

`lixplore -P -q "{{research}}" -m {{50}} -S odd -X csv`

- Export first 10 articles:

`lixplore -P -q "{{cancer}}" -m {{50}} -S first:10 -X xlsx`

- Export specific range (articles 10-20):

`lixplore -P -q "{{biology}}" -m {{50}} -S 10-20 -X enw`

- Sort by newest and export top 10:

`lixplore -P -q "{{COVID-19}}" -m {{50}} --sort newest -S first:10 -X xlsx`

- Sort by oldest (historical research):

`lixplore -P -q "{{diabetes}}" -m {{50}} --sort oldest -X csv`

- Sort by journal alphabetically:

`lixplore -A -q "{{AI research}}" -m {{50}} -D --sort journal -X xlsx`
